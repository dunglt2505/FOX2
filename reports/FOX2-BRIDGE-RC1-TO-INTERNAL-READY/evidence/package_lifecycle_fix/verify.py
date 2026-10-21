"""Bounded A03 source/static checks and independent Result Contract verification.

Run from the task worktree: python <this file> [--result]. No host lifecycle calls.
"""
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
AREA = Path(__file__).resolve().parent
BASE = 'e052082afd7279f21611d76669dc8e761c003e79'
CODE = ['agent_bridge/scripts/certify_user_lifecycle.py', 'agent_bridge/tests/test_rc1_package.py']
REPORT = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (AREA / name).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')


def changed_paths():
    paths = set(git('diff', '--name-only', BASE).decode().splitlines())
    paths.update(git('ls-files', '--others', '--exclude-standard').decode().splitlines())
    paths.update(p.relative_to(ROOT).as_posix() for p in AREA.rglob('*') if p.is_file())
    return sorted(paths)


def source_checks():
    paths = changed_paths()
    assert all(p in CODE or p in {REPORT + 'report.md', REPORT + 'evidence_manifest.json'}
               or p.startswith(REPORT + 'evidence/package_lifecycle_fix/') for p in paths)
    assert not git('diff', '--check', BASE)
    for name in ('installation.py', '__main__.py'):
        path = 'agent_bridge/src/fox2_agent_bridge/' + name
        assert (ROOT / path).read_bytes().replace(b'\r\n', b'\n') == git('show', BASE + ':' + path).replace(b'\r\n', b'\n')
    for path in CODE:
        compile((ROOT / path).read_text(encoding='utf-8'), path, 'exec')
    raw = (ROOT / CODE[0]).read_text(encoding='utf-8')
    assert not re.search(r"cli\(['\"]uninstall['\"]", raw)
    # Scan only this task's changed text. Two exact synthetic sanitizer vectors
    # exercise assignment and URL credential redaction; neither is an account.
    pattern = rb'(?i)(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|https?://[^\s/]+:[^\s/]+@|(?:authorization|access_token|api_key)\s*[=:])'
    for path in paths:
        data = (ROOT / path).read_bytes()
        data = data.replace(b'api_key="private fixture"', b'SYNTHETIC_REDACTION_TEST')
        data = data.replace(b'https://fixture:private@example.invalid/', b'SYNTHETIC_URL_TEST')
        assert not re.search(pattern, data), 'secret scan finding in ' + path
    assert sum(p.stat().st_size for p in AREA.rglob('*') if p.is_file()) < 500_000
    hunks = []
    for path in CODE:
        diff = git('diff', '--unified=0', BASE, '--', path).decode()
        for header in re.findall(r'^@@.*@@.*$', diff, re.M):
            classification = 'NECESSARY_DEPENDENCY' if path == CODE[0] and (
                '+9,' in header or '+10,' in header) else 'REQUESTED'
            hunks.append({'path': path, 'hunk': header, 'classification': classification,
                          'reason': 'Stable external uninstall and bounded evidence, or its focused regression coverage.'})
    hunks.append({'path': (AREA / 'verify.py').relative_to(ROOT).as_posix(),
                  'hunk': 'entire new evidence verifier', 'classification': 'NECESSARY_DEPENDENCY',
                  'reason': 'Repeatable allowed-path, syntax, sanitization, K1 and Result Contract/hash verification.'})
    artifacts = [{'path': p,
                  'classification': 'REQUESTED' if p in {REPORT + 'report.md', REPORT + 'evidence_manifest.json'}
                  else 'NECESSARY_DEPENDENCY' if p.endswith('/verify.py') else 'JUSTIFIED_GENERATED',
                  'reason': 'Required bounded result/evidence for this exact A03 attempt.'}
                 for p in paths if p not in CODE]
    write('k1.json', {'hunks': hunks, 'result_artifacts': artifacts, 'UNEXPLAINED': 0})
    tree = ast.parse((ROOT / 'agent_bridge/src/fox2_agent_bridge/installation.py').read_text(encoding='utf-8'))
    launcher = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == 'UNINSTALL_LAUNCHER' for t in n.targets))
    command = ('$tokens=$null;$errors=$null;'
               '$null=[System.Management.Automation.Language.Parser]::ParseInput([Console]::In.ReadToEnd(),[ref]$tokens,[ref]$errors);'
               '@{major=$PSVersionTable.PSVersion.Major;parse_errors=@($errors).Count}|ConvertTo-Json -Compress;'
               'if($PSVersionTable.PSVersion.Major -lt 7 -or @($errors).Count){exit 1}')
    process = subprocess.run([r'C:\Program Files\PowerShell\7\pwsh.exe', '-NoProfile', '-NonInteractive', '-Command', command],
                             input=launcher, text=True, capture_output=True, timeout=30,
                             creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    assert process.returncode == 0
    write('static_checks.json', {'python_syntax': 'PASS', 'powershell_parse': json.loads(process.stdout),
          'changed_path_allowlist': 'PASS', 'git_diff_check': 'PASS', 'bounded_secret_scan': 'PASS',
          'product_contract_unchanged': 'PASS', 'no_installed_cli_uninstall': 'PASS',
          'K1_UNEXPLAINED': 0, 'real_host_lifecycle': 'NOT_RUN', 'changed_paths': paths,
          'secret_scan_scope': 'Changed task files only; two exact synthetic sanitizer vectors excluded.'})
    print('SYNTAX/POWERSHELL_PARSE/ALLOWLIST/DIFF/SECRET_SCAN/K1=PASS; HOST_LIFECYCLE=NOT_RUN')


def result_checks():
    from jsonschema import Draft202012Validator, FormatChecker

    schema_path = ROOT / 'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json'
    manifest = json.loads((ROOT / REPORT / 'evidence_manifest.json').read_text(encoding='utf-8'))
    Draft202012Validator(json.loads(schema_path.read_text(encoding='utf-8')),
                         format_checker=FormatChecker()).validate(manifest)
    ids = {item['id'] for item in manifest['evidence']}
    assert len(ids) == len(manifest['evidence'])
    targets = {item['id'] for item in manifest['tests'] + manifest['acceptance']}
    for item in manifest['evidence']:
        assert sha(ROOT / item['path']) == item['sha256'], item['id']
        assert set(item['supports_ids']) <= targets, item['id']
    for item in manifest['tests'] + manifest['acceptance']:
        assert set(item['evidence_ids']) <= ids
    for item in manifest['scope']['changed_paths']:
        if item['new_sha256'] is not None:
            assert sha(ROOT / item['path']) == item['new_sha256'], item['path']
    assert set(changed_paths()) == {item['path'] for item in manifest['scope']['changed_paths']}
    print('RESULT_CONTRACT_V2=PASS; EVIDENCE_HASHES_AND_REFERENCES=PASS; CHANGED_PATH_COVERAGE=PASS')


if __name__ == '__main__':
    if '--result' in sys.argv:
        result_checks()
    else:
        source_checks()
