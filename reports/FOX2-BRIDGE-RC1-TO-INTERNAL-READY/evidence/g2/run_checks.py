"""Bounded local G2 command receipts. No Agent execution or host activation."""
from datetime import datetime, UTC
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
COMMANDS = {
    'focused': [sys.executable, '-m', 'pytest', '-q', 'agent_bridge/tests/test_f1_authority.py',
                'agent_bridge/tests/test_f1_policy.py', 'agent_bridge/tests/test_f1_consumers.py',
                'agent_bridge/tests/test_f1_host_fence.py'],
    'regression': [sys.executable, '-m', 'pytest', '-q', *['agent_bridge/tests/' + n for n in (
        'test_f1_broker_store.py', 'test_f1_reconcile.py', 'test_runtime_ledger.py',
        'test_rc1_launcher.py', 'test_desktop.py', 'test_ops_runner.py', 'test_e2e_runner.py',
        'test_installation.py', 'test_rc1_package.py')]],
    'full': [sys.executable, '-m', 'pytest', '-q', 'agent_bridge/tests'],
    'static': [sys.executable, str(OUT / 'static_checks.py')],
    'windows': [sys.executable, '-m', 'pytest', '-q', 'agent_bridge/tests/test_f1_windows.py'],
    'desktop-build': ['dotnet', 'build',
        'agent_bridge/desktop_app/src/FOX2.Bridge.Desktop/FOX2.Bridge.Desktop.csproj',
        '-c', 'Release', '-p:ContinuousIntegrationBuild=true'],
}


def run(name):
    command = COMMANDS[name]
    started = datetime.now(UTC).isoformat()
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'agent_bridge/src'),
           'PYTHONIOENCODING': 'utf-8', 'PYTHONDONTWRITEBYTECODE': '1',
           'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.longpaths', 'GIT_CONFIG_VALUE_0': 'true'}
    result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    receipt = {'id': name, 'command': [str(c) for c in command], 'cwd': str(ROOT),
        'started_at': started, 'finished_at': datetime.now(UTC).isoformat(),
        'exit_code': result.returncode, 'result': 'PASS' if result.returncode == 0 else 'FAIL',
        'environment_overrides': {'core.longpaths': 'true (per-child only)', 'bytecode': 'disabled'},
        'stdout_tail': result.stdout[-14000:], 'stderr_tail': result.stderr[-1500:]}
    # Keep failures and later rechecks distinct within the single A01 attempt.
    count = len(list(OUT.glob(name + '-*.json'))) + 1
    path = OUT / f'{name}-{count:02}.json'
    path.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps({'receipt': path.name, 'exit_code': result.returncode,
                      'summary': result.stdout[-5000:]}))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(run(sys.argv[1]))
