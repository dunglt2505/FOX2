"""Bounded offline source/package and Result Contract checks; never activate F1."""
from datetime import datetime, UTC
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[4]
BASE = '0962ec74617613ff01a629926e64b7ae8b122979'
WP = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'
OUT = ROOT / WP / 'evidence/samehost'
PRODUCT = {
    'agent_bridge/src/fox2_agent_bridge/f1_policy.py',
    'agent_bridge/src/fox2_agent_bridge/f1_service.py',
    'agent_bridge/scripts/f1_policy_artifact.py',
    'agent_bridge/tests/test_f1_policy.py',
    'agent_bridge/tests/test_f1_host_fence.py',
}


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8',
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        raise RuntimeError('check failed: ' + repr(command) + '\n' +
                           result.stdout[-2000:] + result.stderr[-2000:])
    return result.stdout


def changed():
    paths = set(run(['git', 'diff', '--name-only', BASE]).splitlines())
    paths.update(run(['git', 'ls-files', '--others', '--exclude-standard']).splitlines())
    return sorted(paths)


def classify(path):
    if path in PRODUCT or path == WP + 'report.md':
        return 'REQUESTED', 'Same-host policy, dual HostFence, offline artifacts, regression or required report.'
    if path in {WP + 'evidence/samehost/' + p for p in ('verify_build.py', 'assemble_evidence.py')}:
        return 'NECESSARY_DEPENDENCY', 'Repeatable bounded scope, syntax, package and delivery verification.'
    if path == WP + 'evidence_manifest.json' or path.startswith(WP + 'evidence/samehost/'):
        return 'JUSTIFIED_GENERATED', 'Required bounded A01 source/test/K1/result evidence; historical bytes retained.'
    raise AssertionError('path not in this implementation allowlist: ' + path)


def hunks(path):
    prior = subprocess.run(['git', 'cat-file', '-e', BASE + ':' + path], cwd=ROOT,
                           capture_output=True)
    if prior.returncode == 0:
        diff = run(['git', 'diff', '--unified=0', BASE, '--', path])
        return re.findall(r'^@@.*?@@', diff, re.M)
    return ['ALL_ADDED_CONTENT']


def verify_common():
    paths = changed()
    for name in paths:
        classify(name)
        if name.endswith('.py'):
            compile((ROOT / name).read_text(encoding='utf-8'), name, 'exec')
    run(['git', 'diff', '--check', BASE])
    # Identical pre-existing historical receipts, evidence and admission probe.
    protected = [WP + p for p in ('preexec/', 'evidence/g2/', 'evidence/g3/',
        'evidence/samehost/samehost_build_a01_live_admission.json', 'evidence/f1_strictmode_20261021/')]
    assert not run(['git', 'diff', '--name-only', BASE, '--', *protected]).strip()
    credential = re.compile(r'(?i)(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{20,}|'
        r'AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|'
        r'authorization["\x27]?\s*[:=]\s*["\x27]?Bearer\s+[A-Za-z0-9._~-]{16,})')
    for name in paths:
        assert not credential.search((ROOT / name).read_text(encoding='utf-8')), 'credential pattern: ' + name
    binding = json.loads((OUT / 'source_binding.json').read_text())
    for source in binding['sources']:
        raw = subprocess.check_output(['git', 'show', source['commit'] + ':' + source['path']], cwd=ROOT)
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
    return dict(allowlist='PASS', changed_paths=paths, diff_check='PASS', bounded_secret_scan='PASS',
        source_blobs='PASS', historical_evidence_unchanged='PASS', syntax='PASS',
        host_mutation=False, observed_at_utc=datetime.now(UTC).isoformat())


def static():
    result = verify_common()
    scripts = sorted((ROOT / 'agent_bridge/scripts').glob('f1_*.ps1'))
    for script in scripts:
        command = ("$t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile('" +
            str(script).replace("'", "''") + "', [ref]$t, [ref]$e) | Out-Null; " +
            "if ($e.Count) { throw 'PowerShell syntax failure' }; 'PARSE_PASS'")
        assert 'PARSE_PASS' in run(['pwsh', '-NoProfile', '-NonInteractive', '-Command', command])
    for name in PRODUCT:
        source = (ROOT / name).read_text(encoding='utf-8').lower()
        for prohibited in ('set-applockerpolicy', 'start-service ', 'stop-service ', 'new-service ',
                           'sc.exe create', 'sc.exe delete', 'restart-computer', 'icacls '):
            assert prohibited not in source, 'activation command in changed product: ' + name
    builder_path = ROOT / 'agent_bridge/scripts/build_user_package.py'
    spec = importlib.util.spec_from_file_location('samehost_package_check', builder_path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    with tempfile.TemporaryDirectory(prefix='samehost-wheel-contract-') as directory:
        wheel = Path(directory) / 'fixture.whl'
        package = ROOT / 'agent_bridge/src/fox2_agent_bridge'
        with zipfile.ZipFile(wheel, 'w') as archive:
            for p in sorted(package.rglob('*.py')):
                archive.write(p, 'fox2_agent_bridge/' + p.relative_to(package).as_posix())
        verified = builder.verify_wheel_source_modules(wheel, ROOT / 'agent_bridge')
        assert all('fox2_agent_bridge/' + n in verified for n in ('f1_service.py', 'f1_policy.py',
            'f1_authority.py', 'f1_protocol.py', 'f1_windows.py', 'f1_broker_store.py', 'f1_reconcile.py'))
    result.update(powershell_scripts_parsed=len(scripts), wheel_source_modules=len(verified),
                  full_release_package='NOT_RUN_BUILD_SOURCE_ONLY')
    (OUT / 'static-01.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(result))


def delivery():
    result = verify_common()
    manifest = json.loads((ROOT / WP / 'evidence_manifest.json').read_text())
    schema = json.loads(run(['git', 'show', BASE + ':docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json']))
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(manifest)
    assert manifest['task_id'] == 'FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01'
    ids = {e['id'] for e in manifest['evidence']}
    assert len(ids) == len(manifest['evidence'])
    for e in manifest['evidence']:
        assert hashlib.sha256((ROOT / e['path']).read_bytes()).hexdigest() == e['sha256'], e['path']
    assert {e['path'] for e in manifest['scope']['changed_paths']} == set(changed())
    for p in manifest['scope']['changed_paths']:
        if p['new_sha256'] is not None:
            assert hashlib.sha256((ROOT / p['path']).read_bytes()).hexdigest() == p['new_sha256'], p['path']
    for check in manifest['tests'] + manifest['acceptance']:
        assert set(check['evidence_ids']) <= ids
    k1 = json.loads((OUT / 'k1.json').read_text())
    assert k1['unexplained_hunks'] == 0
    assert {p['path'] for p in k1['paths']} == set(changed())
    for p in k1['paths']:
        assert p['classification'] == classify(p['path'])[0]
        assert p['hunks'] == hunks(p['path']), 'K1 hunk coverage mismatch: ' + p['path']
    result.update(result_schema='PASS', evidence_hashes='PASS', changed_hashes='PASS', k1='PASS',
                  g3_physical_enforcement='NOT_RUN', chat_acceptance='PENDING')
    print(json.dumps(result))


if __name__ == '__main__':
    if sys.argv[1:] == ['--delivery']:
        delivery()
    elif not sys.argv[1:]:
        static()
    else:
        raise SystemExit('usage: verify_build.py [--delivery]')
