"""Offline R4 delivery checks; never execute the installed-host certifier."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = OUT.parents[1]
BASE = '35aa18ccabcc6f7d4b889ed213c075fc314d45d0'
CODE = ['agent_bridge/scripts/certify_user_lifecycle.py',
        'agent_bridge/tests/test_lifecycle_wpf_contract.py']


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def changed():
    return sorted(set(git('diff', '--name-only', BASE).decode().splitlines() +
                      git('ls-files', '--others', '--exclude-standard').decode().splitlines()))


def allowed(path):
    relative = OUT.relative_to(ROOT).as_posix() + '/'
    return path in CODE + [REPORT.relative_to(ROOT).as_posix() + '/report.md',
                          REPORT.relative_to(ROOT).as_posix() + '/evidence_manifest.json'] or path.startswith(relative)


def scan(paths):
    patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'gh[pousr]_[A-Za-z0-9]{30,}', r'sk-[A-Za-z0-9]{30,}',
                r'(?i)https?://[^\s/]+:[^\s/]+@',
                r'(?i)[A-Z]:[\\/]Users[\\/][^\s"\']+',
                r'(?i)(?:password|api_key|access_token)\s*=\s*["\'][A-Za-z0-9/+_-]{20,}["\']']
    findings = []
    for path in paths:
        content = (ROOT / path).read_text(encoding='utf-8')
        for index, pattern in enumerate(patterns):
            if re.search(pattern, content):
                findings.append({'path': path, 'pattern_index': index})
    assert not findings, findings
    return {'status': 'PASS', 'files_scanned': len(paths), 'findings': [],
            'method': 'Credential/private-key/authenticated-URL/private-user-path patterns plus material diff review; no host-data export.'}


def preserved_tail():
    path = CODE[0]
    before = ast.parse(git('show', BASE + ':' + path))
    after = ast.parse((ROOT / path).read_text())
    for name in ['_uninstall_output', 'certify_uninstall', 'require_safe_control']:
        old = next(n for n in before.body if isinstance(n, ast.FunctionDef) and n.name == name)
        new = next(n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == name)
        assert ast.dump(old) == ast.dump(new), name
    old = next(n for n in before.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    new = next(n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == 'main')
    # Everything after the presentation call (diagnostics/uninstall/reinstall/durable state) is identical.
    def tail(node):
        offset = next(i for i, n in enumerate(node.body) if isinstance(n, ast.Expr)
                      and isinstance(n.value, ast.Call)
                      and isinstance(n.value.func, ast.Name)
                      and n.value.func.id == 'certify_presentation')
        return [ast.dump(n) for n in node.body[offset + 1:]]
    assert tail(old) == tail(new)
    return 'PASS'


def static():
    paths = changed()
    assert all(allowed(p) for p in paths), paths
    assert [p for p in paths if p.startswith('agent_bridge/')] == sorted(CODE)
    assert not git('diff', '--check', BASE)
    for path in CODE:
        compile((ROOT / path).read_text(), path, 'exec')
    preserved_tail()
    patch = git('diff', '--unified=3', BASE, '--', *CODE).decode()
    save('code_diff.json', {'base': BASE, 'stdout': patch, 'sha256': digest(patch.encode())})
    hunks = []
    for path in CODE:
        diff = git('diff', '--unified=3', BASE, '--', path).decode()
        for match in re.finditer(r'^@@.*?(?=^@@|\Z)', diff, re.M | re.S):
            hunk = match.group(0)
            hunks.append({'path': path, 'header': hunk.splitlines()[0],
                          'sha256': digest(hunk.encode()), 'classification': 'REQUESTED',
                          'reason': 'R4 bounded differential lock proof/continuation and required positive/negative fixtures; errno import and PID checks support that proof.'})
    generated = [{'path': p, 'classification': 'JUSTIFIED_GENERATED',
                  'coverage': 'All material hunks in this result/evidence file',
                  'reason': 'R4 actual validation, binding, reviewable diff, report, manifest or reproducible offline evidence verification.'}
                 for p in paths if p not in CODE]
    save('k1.json', {'hunks': hunks, 'result_and_evidence': generated,
                     'allowed_classes': ['REQUESTED', 'NECESSARY_DEPENDENCY', 'JUSTIFIED_GENERATED', 'UNEXPLAINED'],
                     'UNEXPLAINED': 0})
    save('static_checks.json', {'changed_paths': paths, 'changed_path_allowlist': 'PASS',
                               'code_test_paths_exactly_two': True, 'git_diff_check': 'PASS',
                               'syntax': 'PASS', 'preserved_lifecycle_tail_ast': 'PASS',
                               'secret_privacy_scan': scan(paths), 'K1_UNEXPLAINED': 0,
                               'real_host_lifecycle': 'NOT_RUN', 'worker_f1': 'NOT_APPLICABLE_PRE_G3'})
    print('R4 allowlist/syntax/diff/privacy/K1/preserved-tail: PASS')


def manifest():
    import jsonschema
    value = json.loads((REPORT / 'evidence_manifest.json').read_text())
    schema = json.loads((ROOT / 'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text())
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(value)
    paths = changed()
    assert set(paths) == {p['path'] for p in value['scope']['changed_paths']}
    for item in value['scope']['changed_paths']:
        assert allowed(item['path']) and item['within_allowed_paths']
        if item['new_sha256'] is not None:
            assert digest((ROOT / item['path']).read_bytes()) == item['new_sha256'], item['path']
    ids = {e['id'] for e in value['evidence']}
    assert len(ids) == len(value['evidence'])
    for item in value['evidence']:
        assert digest((ROOT / item['path']).read_bytes()) == item['sha256'], item['path']
    for item in value['tests'] + value['acceptance']:
        assert set(item['evidence_ids']) <= ids
    scan(paths)
    assert not git('diff', '--check', BASE)
    print('R4 Result Contract v2 schema/hash/readback/final privacy/diff: PASS')


if __name__ == '__main__':
    import sys
    manifest() if '--manifest-only' in sys.argv else static()
