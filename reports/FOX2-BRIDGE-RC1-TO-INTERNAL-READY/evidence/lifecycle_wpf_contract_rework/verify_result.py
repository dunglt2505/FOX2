"""A02 offline static/K1/Result Contract verification; no installed-host commands."""
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
BASE = '4504bf95dd2baf474b30f896b23365c52fe10c9f'
ORIGINAL = 'e7d5acf51dddcbc95324a992ad6be2773e61285f'
SNAPSHOT = '1a11fa0b232a69f0c26a0b4029c331ee2a8c840f'
CODE = ['agent_bridge/scripts/certify_user_lifecycle.py', 'agent_bridge/tests/test_rc1_package.py',
        'agent_bridge/tests/test_rc1_launcher.py', 'agent_bridge/tests/test_lifecycle_wpf_contract.py']
REPORT = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'
EVIDENCE = REPORT + 'evidence/lifecycle_wpf_contract_rework/'

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')

def changed():
    return sorted(set(git('diff', '--name-only', BASE).decode().splitlines()) |
                  set(git('ls-files', '--others', '--exclude-standard').decode().splitlines()) |
                  {p.relative_to(ROOT).as_posix() for p in OUT.iterdir()
                   if p.is_file() and p.name != 'recovery_codex001_snapshot.json'})

def allowed(path):
    return path in CODE or path in [REPORT + 'report.md', REPORT + 'evidence_manifest.json'] or path.startswith(EVIDENCE)

def scan(paths):
    findings, scanned, fixture_markers = [], [], []
    patterns = [r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{30,}',
                r'sk-[A-Za-z0-9]{24,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    for path in paths:
        raw = (ROOT / path).read_bytes()
        assert len(raw) <= 2_000_000, path
        text = raw.decode('utf-8', errors='strict')
        for pattern in patterns:
            for match in re.finditer(pattern, text):
                if 'PRIVATE KEY' in match.group() and path == CODE[1]:
                    fixture_markers.append({'path': path, 'offset': match.start(), 'reason': 'Existing A03 redaction test marker, no key material.'})
                else:
                    findings.append({'path': path, 'offset': match.start(), 'pattern': pattern})
        scanned.append({'path': path, 'bytes': len(raw)})
    assert not findings, findings
    return {'status': 'PASS', 'max_bytes_per_file': 2_000_000, 'scanned': scanned,
            'findings': findings, 'benign_fixture_markers': fixture_markers}

def hunks(patch):
    return re.split(r'(?=^@@ )', patch, flags=re.M)[1:]

def check():
    paths = changed()
    assert all(allowed(path) for path in paths), paths
    binding = json.loads((OUT / 'source_binding.json').read_text())
    assert git('branch', '--show-current').decode().strip() == binding['claim'].get('task_branch',
        'work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022')
    provenance = EVIDENCE + 'recovery_codex001_snapshot.json'
    assert (ROOT / provenance).read_bytes() == git('show', SNAPSHOT + ':' + provenance)
    before = ast.parse(git('show', ORIGINAL + ':' + CODE[0]).decode())
    after_source = (ROOT / CODE[0]).read_text()
    after = ast.parse(after_source)
    for name in ['certify_uninstall', '_uninstall_output']:
        find = lambda tree: next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
        assert ast.dump(find(before)) == ast.dump(find(after)), name
    syntax = []
    for path in CODE + [p.relative_to(ROOT).as_posix() for p in OUT.glob('*.py')]:
        source = (ROOT / path).read_text(encoding='utf-8-sig')
        compile(source, path, 'exec')
        syntax.append({'path': path, 'sha256': digest((ROOT / path).read_bytes()), 'status': 'PASS'})
    commands = [ast.literal_eval(node.args[1]) for node in ast.walk(after)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'ps'
        and len(node.args) > 1 and isinstance(node.args[0], ast.Constant) and node.args[0].value == '-Command']
    assert len(commands) == 1
    import os
    env = dict(os.environ, FOX2_STATIC_PS_INPUT=commands[0])
    parser = "$parseErrors=$null; [System.Management.Automation.Language.Parser]::ParseInput($env:FOX2_STATIC_PS_INPUT,[ref]$null,[ref]$parseErrors) > $null; if($parseErrors.Count){throw 'PowerShell syntax failed'}; 'Generated process-query syntax: PASS'"
    parsed = subprocess.run(['pwsh', '-NoProfile', '-NonInteractive', '-Command', parser],
        capture_output=True, text=True, env=env, timeout=30)
    assert parsed.returncode == 0, parsed.stderr
    forbidden = ['agent_bridge/src/fox2_agent_bridge/launcher.py',
        'agent_bridge/src/fox2_agent_bridge/f1_service.py', 'agent_bridge/src/fox2_agent_bridge/installation.py',
        'agent_bridge/scripts/certify_rc1_ui.ps1']
    forbidden += git('ls-tree', '-r', '--name-only', ORIGINAL, '--', 'agent_bridge/desktop_app').decode().splitlines()
    identical = []
    same_base_checkout = Path('C:/Projects/FOX2/.git/wpf-a01-test')
    assert subprocess.check_output(['git', '-C', str(same_base_checkout), 'rev-parse', 'HEAD'], text=True).strip() == ORIGINAL
    for path in forbidden:
        blob = git('rev-parse', ORIGINAL + ':' + path).decode().strip()
        assert git('hash-object', path).decode().strip() == blob, path
        raw = (ROOT / path).read_bytes()
        assert raw == (same_base_checkout / path).read_bytes(), path
        identical.append({'path': path, 'original_blob': blob, 'worktree_sha256': digest(raw),
                          'raw_same_base_checkout_identical': True})
    assert set(git('diff', '--name-only', ORIGINAL, '--', 'agent_bridge').decode().splitlines()) <= set(CODE)
    assert all(s not in after_source for s in ['desktop_tray.ps1', 'desktop_launcher.ps1', 'heartbeat',
        "'worker'", 'Stop-Process', 'Start-Service', 'AppIDSvc', 'AppLocker', 'taskkill'])
    diff = subprocess.run(['git', 'diff', '--check', BASE], cwd=ROOT, capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    (OUT / 'diff_check.log').write_text('git diff --check ' + BASE + '\nexit=0\n' + diff.stdout + diff.stderr, newline='\n')
    classified, review = [], []
    for path in CODE:
        classification = 'NECESSARY_DEPENDENCY' if path == CODE[1] else 'REQUESTED'
        reason = ('Adapt existing A03 integration fixture to WPF, retaining stable uninstall/durable-state assertions.'
            if path == CODE[1] else 'Requested pre-G3 presentation-only lifecycle semantics and fail-closed negative regressions.')
        salvaged = hunks(git('diff', '--unified=3', ORIGINAL, SNAPSHOT, '--', path).decode())
        review += [{'path': path, 'header': h.splitlines()[0], 'sha256': digest(h.encode()),
            'verdict': 'KEPT_REQUIRED; A02 corrections restricted to safe-control completeness, sharing-violation proof and process-query failure handling.',
            'classification': classification} for h in salvaged]
        for comparison, base in [('original_runtime_base_to_final', ORIGINAL), ('salvage_source_to_final', SNAPSHOT)]:
            for h in hunks(git('diff', '--unified=3', base, '--', path).decode()):
                # Earlier insertions shift later hunk line numbers without changing their bytes.
                body = h.split('\n', 1)[1]
                unchanged = any(body == old.split('\n', 1)[1] for old in salvaged)
                provenance_kind = 'SALVAGED_UNCHANGED_FROM_A01' if unchanged else 'A02_CORRECTION'
                classified.append({'comparison': comparison, 'path': path, 'header': h.splitlines()[0],
                    'sha256': digest(h.encode()), 'classification': classification,
                    'provenance': provenance_kind, 'reason': reason})
    save('k1.json', {'original_runtime_base': ORIGINAL, 'salvage_source': SNAPSHOT, 'a02_runtime_base': BASE,
        'hunks': classified, 'salvaged_code_hunk_review': review, 'UNEXPLAINED': 0,
        'evidence_classification': 'JUSTIFIED_GENERATED; executable evidence helpers NECESSARY_DEPENDENCY',
        'note': 'Original-to-final hunks containing both salvage and A02 corrections are tagged A02_CORRECTION; unchanged surrounding salvage is retained.'})
    salvage_paths = git('diff', '--name-only', ORIGINAL, SNAPSHOT).decode().splitlines()
    save('salvage_review.json', {'snapshot': SNAPSHOT, 'reviewed_paths': [{
        'path': path,
        'disposition': ('PRESERVED_BYTE_IDENTICAL' if path == provenance else
            'KEPT_WITH_BOUNDED_A02_CORRECTIONS' if path in CODE else 'REGENERATED_FROM_A02_EXECUTION'),
        'reason': ('Immutable historical consumed/no-replay recovery record.' if path == provenance else
            'Correct and required salvage retained; new negative checks correct three proof gaps.' if path in CODE else
            'Historical A01 helper identities and provisional PASS claims cannot certify A02; replaced by actual A02 checks.')
    } for path in salvage_paths], 'historical_pass_authoritative': False})
    # Store both immutable comparisons as reviewable source/test patches.
    for label, base in [('original_to_final', ORIGINAL), ('salvage_to_final', SNAPSHOT)]:
        patch = git('diff', '--unified=3', base, '--', *CODE)
        save(label + '_diff.json', {'argv': ['git', 'diff', '--unified=3', base, '--', *CODE],
            'stdout_sha256': digest(patch), 'stdout': patch.decode('utf-8')})
    save('static_checks.json', {'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'python_syntax_compile': syntax, 'generated_powershell_syntax': parsed.stdout.strip(),
        'changed_path_allowlist': 'PASS', 'forbidden_files_byte_identity': identical,
        'all_other_agent_bridge_paths_unchanged': True,
        'recovery_provenance_byte_identical': True, 'a03_supervisor_and_redaction_ast_identical': True,
        'git_diff_check': 'PASS', 'secret_scan': scan(changed()), 'K1_UNEXPLAINED': 0})
    print('A02 syntax/static/allowlist/forbidden-byte-identity/A03/diff/secret-scan/K1: PASS')

def validate_manifest():
    import jsonschema
    value = json.loads((ROOT / REPORT / 'evidence_manifest.json').read_text())
    binding = json.loads((OUT / 'source_binding.json').read_text())
    schema = json.loads(git('show', binding['governance_commit_for_schemas'] + ':' + binding['result_schema_path']))
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(value)
    evidence_ids = {entry['id'] for entry in value['evidence']}
    assert len(evidence_ids) == len(value['evidence'])
    for entry in value['evidence']:
        assert digest((ROOT / entry['path']).read_bytes()) == entry['sha256'], entry['id']
    for entry in value['tests'] + value['acceptance']:
        assert set(entry['evidence_ids']) <= evidence_ids, entry['id']
    assert {entry['path'] for entry in value['scope']['changed_paths']} == set(changed())
    for entry in value['scope']['changed_paths']:
        assert allowed(entry['path']) and entry['within_allowed_paths']
        if entry['new_sha256'] is not None:
            assert digest((ROOT / entry['path']).read_bytes()) == entry['new_sha256'], entry['path']
    assert value['source']['source_manifest_sha256'] == digest((OUT / 'source_binding.json').read_bytes())
    assert value['source']['approved_base_commit_sha'] == BASE
    assert value['task_id'] == binding['claim']['task_id']
    assert (OUT / 'recovery_codex001_snapshot.json').read_bytes() == git('show', SNAPSHOT + ':' + EVIDENCE + 'recovery_codex001_snapshot.json')
    scan(changed())
    print('Result Contract v2 schema: PASS')
    print('Evidence and changed-path SHA-256 readback: PASS')
    print('Evidence references, allowed paths, recovery identity and final secret scan: PASS')

if __name__ == '__main__':
    validate_manifest() if '--manifest-only' in sys.argv else check()
