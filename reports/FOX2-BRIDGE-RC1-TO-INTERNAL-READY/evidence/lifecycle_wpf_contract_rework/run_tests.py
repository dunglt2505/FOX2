"""Run offline pytest in a short, exact-byte detached A02 test worktree."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
TEST_ROOT = Path('C:/Projects/FOX2/.git/wpf-a02-test')
BASE = '4504bf95dd2baf474b30f896b23365c52fe10c9f'
CODE = ['agent_bridge/scripts/certify_user_lifecycle.py', 'agent_bridge/tests/test_rc1_package.py',
        'agent_bridge/tests/test_rc1_launcher.py', 'agent_bridge/tests/test_lifecycle_wpf_contract.py']
git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT), *a])
assert subprocess.check_output(['git', '-C', str(TEST_ROOT), 'rev-parse', 'HEAD'], text=True).strip() == BASE
for relative in CODE:
    (TEST_ROOT / relative).write_bytes((ROOT / relative).read_bytes())
identical = []
for relative in git('ls-files', 'agent_bridge').decode().splitlines():
    raw = (ROOT / relative).read_bytes()
    assert raw == (TEST_ROOT / relative).read_bytes(), relative
    identical.append({'path': relative, 'sha256': hashlib.sha256(raw).hexdigest()})
(OUT / 'test_snapshot_identity.json').write_text(json.dumps({
    'base': BASE, 'test_worktree': str(TEST_ROOT), 'files': identical,
    'note': 'Exact-byte source/test snapshot. Short path avoids known MAX_PATH fixture creation issues. No tests edited/skipped or permanent config changed.'
}, indent=2) + '\n', encoding='utf-8', newline='\n')
suite = sys.argv[1]
longpaths = '--longpaths' in sys.argv
assert suite in ['focused', 'full']
paths = ['agent_bridge/tests'] if suite == 'full' else [
    'agent_bridge/tests/test_lifecycle_wpf_contract.py', 'agent_bridge/tests/test_rc1_launcher.py',
    'agent_bridge/tests/test_rc1_package.py', 'agent_bridge/tests/test_installation.py']
name = suite + ('_longpaths' if longpaths else '_initial')
env = dict(os.environ, PYTHONPATH=str(TEST_ROOT / 'agent_bridge/src'))
env.pop('PYTHONHOME', None)
if longpaths:
    index = int(env.get('GIT_CONFIG_COUNT', '0'))
    env.update(GIT_CONFIG_COUNT=str(index + 1))
    env['GIT_CONFIG_KEY_' + str(index)] = 'core.longpaths'
    env['GIT_CONFIG_VALUE_' + str(index)] = 'true'
argv = [sys.executable, '-m', 'pytest', *paths, '-v', '--tb=short']
started = datetime.now(timezone.utc).isoformat()
with (OUT / (name + '.log')).open('w', encoding='utf-8') as log:
    process = subprocess.run(argv, cwd=TEST_ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
record = {'name': name, 'suite': suite, 'argv': argv, 'cwd': str(TEST_ROOT),
    'environment': {'PYTHONPATH': env['PYTHONPATH'], 'process_core_longpaths': longpaths},
    'started_at_utc': started, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
    'exit_code': process.returncode, 'status': 'PASS' if process.returncode == 0 else 'FAIL',
    'log': name + '.log', 'output_tail': (OUT / (name + '.log')).read_text().strip().splitlines()[-1]}
(OUT / (name + '_run.json')).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8', newline='\n')
print(json.dumps(record, indent=2))
sys.exit(process.returncode)
