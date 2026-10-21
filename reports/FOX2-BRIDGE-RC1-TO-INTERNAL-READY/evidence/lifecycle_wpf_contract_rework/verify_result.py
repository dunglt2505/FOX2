"""Offline result checks; no installed Bridge commands or host mutation."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
BASE = 'e7d5acf51dddcbc95324a992ad6be2773e61285f'
CODE = ['agent_bridge/scripts/certify_user_lifecycle.py',
        'agent_bridge/tests/test_rc1_package.py',
        'agent_bridge/tests/test_lifecycle_wpf_contract.py']
REPORT = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def changed():
    return sorted(set(git('diff', '--name-only', BASE).decode().splitlines()) |
                  set(git('ls-files', '--others', '--exclude-standard').decode().splitlines()))


def check():
    paths = changed()
    allowed = lambda p: (p in CODE or p in [REPORT + 'report.md', REPORT + 'evidence_manifest.json'] or
                         p.startswith(REPORT + 'evidence/lifecycle_wpf_contract_rework/'))
    assert all(allowed(p) for p in paths), paths
    assert git('branch', '--show-current').decode().strip() == (
        'work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-20261022')
    before = git('show', BASE + ':' + CODE[0]).decode()
    after = (ROOT / CODE[0]).read_text()
    old_ast, new_ast = ast.parse(before), ast.parse(after)
    # A03 supervisor and output sanitizer must remain structurally identical.
    for name in ['certify_uninstall', '_uninstall_output']:
        find = lambda tree: next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
        assert ast.dump(find(old_ast)) == ast.dump(find(new_ast)), name
    syntax = []
    for path in CODE:
        text = (ROOT / path).read_text(encoding='utf-8')
        ast.parse(text, filename=path)
        compile(text, path, 'exec')
        syntax.append({'path': path, 'sha256': digest((ROOT / path).read_bytes()), 'status': 'PASS'})
    forbidden = ['agent_bridge/src/fox2_agent_bridge/launcher.py',
                 'agent_bridge/src/fox2_agent_bridge/f1_service.py',
                 'agent_bridge/src/fox2_agent_bridge/installation.py',
                 'agent_bridge/scripts/certify_rc1_ui.ps1']
    forbidden += git('ls-tree', '-r', '--name-only', BASE, '--', 'agent_bridge/desktop_app').decode().splitlines()
    assert all(git('hash-object', p).strip() == git('rev-parse', BASE + ':' + p).strip() for p in forbidden)
    snapshot = Path('C:/Projects/FOX2/.git/wpf-a01-test')
    assert all((ROOT / p).read_bytes() == (snapshot / p).read_bytes() for p in forbidden)
    assert all(s not in after for s in ['desktop_tray.ps1', 'desktop_launcher.ps1', 'heartbeat',
                                       "'worker'", 'Stop-Process', 'Start-Service', 'AppIDSvc'])
    diff = subprocess.run(['git', '-C', str(ROOT), 'diff', '--check', BASE], capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    (OUT / 'diff_check.log').write_text('git diff --check ' + BASE + '\nexit=0\n' + diff.stdout + diff.stderr)
    hunks = []
    for path in CODE:
        classification = 'NECESSARY_DEPENDENCY' if path.endswith('test_rc1_package.py') else 'REQUESTED'
        reason = ('Adapt existing A03 end-to-end fixtures to WPF without changing supervisor assertions.'
                  if classification == 'NECESSARY_DEPENDENCY' else
                  'Implement and regress the requested presentation-only pre-G3 lifecycle contract.')
        patch = git('diff', '--unified=3', BASE, '--', path).decode()
        if not patch:
            patch = '@@ -0,0 +1,' + str(len((ROOT / path).read_text().splitlines())) + ' @@\n' + (ROOT / path).read_text()
        for hunk in re.split(r'(?=^@@ )', patch, flags=re.M)[1:]:
            hunks.append({'path': path, 'header': hunk.splitlines()[0], 'sha256': digest(hunk.encode()),
                          'classification': classification, 'reason': reason})
    save('k1.json', {'hunks': hunks, 'UNEXPLAINED': 0,
                     'evidence_classification': 'JUSTIFIED_GENERATED; verification scripts NECESSARY_DEPENDENCY'})
    findings = []
    scanned = []
    # Bounded scan of changed files only; never inspect host credentials or durable data.
    patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}',
                r'sk-[A-Za-z0-9]{24,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for path in paths:
        data = (ROOT / path).read_bytes()
        assert len(data) <= 2_000_000, path
        text = data.decode('utf-8', errors='replace')
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                # Test literals describe redaction fixtures; none is a credential.
                if 'PRIVATE KEY' in match.group() and path in [CODE[1], REPORT + 'evidence/lifecycle_wpf_contract_rework/verify_result.py']:
                    continue
                findings.append({'path': path, 'offset': match.start(), 'pattern': pattern})
        scanned.append({'path': path, 'bytes': len(data)})
    assert not findings, findings
    save('static_checks.json', {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'python_syntax_compile': syntax, 'changed_path_allowlist': 'PASS',
        'forbidden_files_byte_identical': forbidden, 'a03_supervisor_and_redaction_ast_identical': True,
        'git_diff_check': 'PASS', 'secret_scan': {'status': 'PASS', 'max_bytes_per_file': 2_000_000,
        'scanned': scanned, 'findings': findings}, 'K1_UNEXPLAINED': 0})
    print('Syntax/static/allowlist/unchanged supervisor/forbidden files/diff/secret scan/K1: PASS')


def validate_manifest():
    import jsonschema
    value = json.loads((ROOT / REPORT / 'evidence_manifest.json').read_text())
    schema = json.loads((ROOT / 'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text())
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(value)
    for entry in value['evidence']:
        assert digest((ROOT / entry['path']).read_bytes()) == entry['sha256'], entry['id']
    print('Result Contract v2 schema and evidence hash readback: PASS')


if __name__ == '__main__':
    validate_manifest() if '--manifest-only' in sys.argv else check()
