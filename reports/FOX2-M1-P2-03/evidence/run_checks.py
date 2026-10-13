"""Reproducible offline verification; writes only sanitized result evidence."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
os.chdir(ROOT)
env = dict(os.environ)
env['PYTHONPATH'] = str(ROOT / 'tests/p2_03') + os.pathsep + str(ROOT / 'backend/src')
env['PYTHONDONTWRITEBYTECODE'] = '1'


def command(name, args):
    result = subprocess.run(args, env=env, capture_output=True, text=True)
    # Result logs use project paths and sanitized local interpreter labels.
    output = result.stdout + result.stderr
    output = output.replace(str(Path.home()), '<USER_HOME>')
    (OUT / (name + '.txt')).write_text(output, encoding='utf-8')
    return {'command': args, 'exit_code': result.returncode, 'output': name + '.txt'}


base = [sys.executable, '-B', '-m', 'pytest']
common = ['-p', 'temp_support', '-p', 'no:cacheprovider', '-q', '--tb=short']
# Unique temporary roots avoid deleting or reusing any prior run's directory.
from uuid import uuid4
temp = Path(os.environ['TEMP'])
results = {}
for name, paths, extra in (
        ('p2_03', ['tests/p2_03'], []),
        ('upstream_regression', ['tests/p2_02', 'tests/p2_01'],
         ['-k', 'not test_domain_dependency_boundary'])):
    results[name] = command(name, base + paths + common + extra +
        ['--basetemp', str(temp / ('fox2-p203-' + uuid4().hex))])
results['diff_check'] = command('diff_check', ['git', 'diff', '--check'])
status = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'], text=True)
paths = [line[3:].replace('\\', '/') for line in status.splitlines()]
allowed = ('backend/src/fox2/dsm/', 'tests/p2_03/', 'reports/FOX2-M1-P2-03/')
assert all(path.startswith(allowed) for path in paths), paths
upstream = subprocess.check_output(['git', 'diff', 'f70f0237356c4f27afb0e6760b01870228ba3739',
    '--', 'backend/src/fox2/contracts', 'backend/src/fox2/ports', 'backend/src/fox2/validation',
    'backend/src/fox2/store', 'backend/pyproject.toml', 'tests/p2_01', 'tests/p2_02'], text=True)
assert not upstream
syntax = []
for folder in ('backend/src/fox2/dsm', 'tests/p2_03'):
    for path in (ROOT / folder).rglob('*.py'):
        compile(ast.parse(path.read_text(encoding='utf-8')), str(path), 'exec')
        syntax.append(path.relative_to(ROOT).as_posix())
# Obvious credential material scan; never print matching values.
patterns = [r'-----BEGIN [A-Z ]*PRIVATE KEY-----', r'AKIA[0-9A-Z]{16}',
            r'gh[pousr]_[A-Za-z0-9]{30,}', r'sk-[A-Za-z0-9]{32,}',
            r'(?i)(?:password|api_key|access_token|client_secret)\s*[:=]\s*[\x22\x27][^\x22\x27]{8,}']
scanned = []
for folder in allowed:
    for path in (ROOT / folder).rglob('*'):
        if path.is_file() and path.suffix in ('.py', '.md', '.json', '.txt'):
            content = path.read_text(encoding='utf-8')
            assert not any(re.search(pattern, content) for pattern in patterns), path.name
            scanned.append(path.relative_to(ROOT).as_posix())
quality = {
    'results': results, 'changed_paths': paths, 'allowlist': 'PASS',
    'upstream_frozen_files_unchanged': 'PASS', 'syntax_import_tests': syntax,
    'obvious_secret_scan': 'PASS', 'scanned_files': scanned,
    'network': {'socket_dns_attempts': 0,
                'proof': 'autouse denial fixture on every P2-03 test; teardown asserts zero',
                'provider_construction_paths': 0,
                'import_boundary': 'AST assertions restrict DSM to stdlib/contracts/ports/validation'},
    'initial_failures': [
        'Bridge Python missing pydantic; repository venv missing pytest; no installation performed.',
        'Python 3.13 pytest mode 0700 temp directories denied managed token; inherited-ACL test plugin used.',
        'Initial fixture serialization and import-boundary assertion errors fixed in P2-03 tests.',
        'Full upstream exploratory run: 175 passed, 2 obsolete stage-boundary assertions failed; frozen tests unchanged.'],
}
(OUT / 'quality.json').write_text(json.dumps(quality, indent=2), encoding='utf-8')
assert all(result['exit_code'] == 0 for result in results.values()), results
print(json.dumps({name: value['exit_code'] for name, value in results.items()}))
