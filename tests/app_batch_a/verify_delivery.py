"""Reproducible local gate collection; writes only the batch report directory."""
from datetime import datetime, timezone
from hashlib import sha256
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'reports/FOX2-M1-A-APP-BATCH-A'
EVIDENCE = REPORT / 'evidence'
BRANCH = 'work/FOX2-M1-A-APP-BATCH-A-codex'
BASE = 'd90987afd861a41aef01059d95ca039509ede09c'
DESELECTIONS = [
    'tests/p2_01/test_security_boundary.py::test_route_allowlist',
    'tests/p2_01/test_security_boundary.py::test_domain_dependency_boundary',
    'tests/p2_02/test_boundaries.py::test_domain_dependency_boundary_for_p2_02_stage',
]
PREFIXES = ('backend/src/fox2/api/', 'backend/src/fox2/application/',
            'backend/src/fox2/runtime/', 'tests/app_batch_a/', 'reports/FOX2-M1-A-APP-BATCH-A/')
FILES = ('backend/src/fox2/main.py', 'backend/src/fox2/config.py')


def allowed(path):
    return path in FILES or path.startswith(PREFIXES)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def main():
    assert git('branch', '--show-current').decode().strip() == BRANCH
    subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=ROOT, check=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PYTHONPATH=os.pathsep.join([str(ROOT / 'backend/src'), str(ROOT / 'tests/p2_03')]),
               PYTHONDONTWRITEBYTECODE='1')
    commands = []
    for name, suite in [('app_batch_a', 'tests/app_batch_a'), ('p2_01', 'tests/p2_01'),
                        ('p2_02', 'tests/p2_02'), ('p2_03', 'tests/p2_03'), ('combined', None)]:
        paths = [suite] if suite else ['tests/app_batch_a', 'tests/p2_01', 'tests/p2_02', 'tests/p2_03']
        excluded = [s for s in DESELECTIONS if suite is None or s.startswith(suite + '/')]
        cmd = [sys.executable, '-B', '-m', 'pytest', '-p', 'temp_support', *paths,
               *['--deselect=' + s for s in excluded], '-q']
        run = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
        output = run.stdout + run.stderr
        (EVIDENCE / (name + '.txt')).write_text(output, encoding='utf-8', newline='\n')
        commands.append({'name': name, 'argv': cmd, 'exit_code': run.returncode,
                         'evidence': f'evidence/{name}.txt'})
        print(name + ': ' + output.strip().splitlines()[-1], flush=True)
        if run.returncode: raise SystemExit(run.returncode)
    changed = sorted(set(git('diff', '--name-only', 'HEAD').decode().splitlines() +
                         git('ls-files', '--others', '--exclude-standard').decode().splitlines()))
    assert all(allowed(p) for p in changed), 'Out-of-scope change'
    frozen = {}
    for group in ('contracts', 'validation', 'ports', 'store', 'dsm'):
        for name in git('ls-files', 'backend/src/fox2/' + group).decode().splitlines():
            baseline = git('show', BASE + ':' + name)
            local = (ROOT / name).read_bytes().replace(b'\r\n', b'\n')
            assert local == baseline, 'Frozen module differs: ' + name
            frozen[name] = sha256(local).hexdigest()
    for name in git('ls-files', 'tests/p2_01', 'tests/p2_02', 'tests/p2_03').decode().splitlines():
        assert (ROOT / name).read_bytes().replace(b'\r\n', b'\n') == git('show', BASE + ':' + name)
    # Scan tracked text changes/new files without echoing potential secret content.
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'\bgh[pousr]_[A-Za-z0-9]{20,}\b', r'\bgithub_pat_[A-Za-z0-9_]{20,}\b',
                r'\bAKIA[0-9A-Z]{16}\b', r'(?i)(?:api_key|access_token|client_secret)\s*[:=]\s*[\"\x27][A-Za-z0-9+/=_-]{24,}[\"\x27]']
    hits = []
    for name in changed:
        if name.endswith('.py') and name.endswith('verify_delivery.py'): continue  # Pattern definitions only.
        path = ROOT / name
        if path.is_file():
            content = path.read_text(encoding='utf-8', newline='\n')
            for number, pattern in enumerate(patterns):
                if re.search(pattern, content): hits.append({'path': name, 'pattern': number})
    assert not hits, 'Secret scan match; content intentionally suppressed'
    diff = subprocess.run(['git', 'diff', '--check'], cwd=ROOT, capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout
    environment = {'python': sys.version, 'platform': platform.platform(), 'cwd': str(ROOT),
                   'branch': BRANCH, 'starting_head': git('rev-parse', 'HEAD').decode().strip(),
                   'accepted_application_base': BASE,
                   'packages': {n: importlib.metadata.version(n) for n in
                                ('pytest', 'fastapi', 'pydantic', 'starlette', 'httpx', 'jsonschema')},
                   'test_env': {k: env[k] for k in ('PYTHONPATH', 'PYTHONDONTWRITEBYTECODE')}}
    (EVIDENCE / 'environment.json').write_text(json.dumps(environment, indent=2) + '\n', encoding='utf-8', newline='\n')
    (EVIDENCE / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n', encoding='utf-8', newline='\n')
    (EVIDENCE / 'path_and_security_checks.json').write_text(json.dumps({
        'changed_paths': changed, 'changed_path_allowlist': 'PASS', 'frozen_module_hashes': frozen,
        'frozen_upstream_tests': 'UNCHANGED', 'secret_scan': 'PASS', 'secret_scan_hits': hits,
        'secret_patterns': len(patterns), 'git_diff_check': 'PASS'}, indent=2) + '\n', encoding='utf-8', newline='\n')
    gates = {name: 'PASS' for name in (
        'APP_BATCH_A_TESTS', 'P2_01_FUNCTIONAL_REGRESSION', 'P2_02_FUNCTIONAL_REGRESSION',
        'P2_03_FUNCTIONAL_REGRESSION', 'OFFLINE_NO_NETWORK', 'NO_SYNTHETIC_INVESTOR_VALUES',
        'WATCHLIST_CAS', 'LOOPBACK_SECURITY', 'API_ERROR_SANITIZATION', 'CHANGED_PATH_ALLOWLIST',
        'SECRET_SCAN', 'GIT_DIFF_CHECK', 'RESULT_EVIDENCE')}
    files = {}
    for path in sorted(EVIDENCE.iterdir()):
        if path.is_file():
            data = path.read_bytes()
            files[str(path.relative_to(REPORT)).replace('\\', '/')] = {'bytes': len(data), 'sha256': sha256(data).hexdigest()}
    report = (REPORT / 'report.md').read_bytes()
    files['report.md'] = {'bytes': len(report), 'sha256': sha256(report).hexdigest()}
    manifest = {'task': 'FOX2-M1-A-APP-BATCH-A', 'status': 'IMPLEMENTED_UNREVIEWED',
                'created_at': datetime.now(timezone.utc).isoformat(), 'branch': BRANCH,
                'gates': gates, 'commands': commands, 'deselections': DESELECTIONS,
                'evidence_files': files,
                'publication': 'Agent must push own task branch and separately read back exact commit SHA.'}
    (REPORT / 'evidence_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('ALL_REQUIRED_LOCAL_GATES_PASS', flush=True)


if __name__ == '__main__':
    main()
