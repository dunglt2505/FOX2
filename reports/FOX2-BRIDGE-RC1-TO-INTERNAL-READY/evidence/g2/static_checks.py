"""Syntax, allowlist, package-module and non-activation static checks."""
import ast
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[4]


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if result.returncode:
        raise RuntimeError('static check failed: ' + result.stdout[-1000:] + result.stderr[-1000:])
    return result.stdout


def main():
    run(['git', 'diff', '--check'])
    changed = set(run(['git', 'diff', '--name-only', '94c936b1d93bbfcee5818db24dd75bd9bb32733f']).splitlines())
    changed.update(run(['git', 'ls-files', '--others', '--exclude-standard']).splitlines())
    existing = {'ledger.py', 'launcher.py', 'desktop.py', 'app.py', 'ops_runner.py',
                'e2e_runner.py', 'installation.py', 'startup.py'}
    test_names = {'test_runtime_ledger.py', 'test_rc1_launcher.py', 'test_desktop.py',
        'test_ops_runner.py', 'test_e2e_runner.py', 'test_installation.py', 'test_rc1_package.py'}
    reports = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'
    for name in changed:
        p = Path(name)
        allowed = (name.startswith('agent_bridge/src/fox2_agent_bridge/') and
                   (p.name in existing or p.match('f1_*.py')) or
                   name.startswith('agent_bridge/tests/') and
                   (p.name in test_names or p.match('test_f1_*.py')) or
                   name.startswith('agent_bridge/scripts/') and
                   (p.name in ('build_user_package.py', 'install_user.ps1') or
                    p.match('f1_*.py') or p.match('f1_*.ps1')) or
                   name in (reports + 'report.md', reports + 'evidence_manifest.json') or
                   name.startswith(reports + 'evidence/g2/'))
        assert allowed, 'out-of-scope write: ' + name
        if p.suffix == '.py':
            compile(p.read_text(encoding='utf-8'), name, 'exec')
    scripts = sorted((ROOT / 'agent_bridge/scripts').glob('f1_*.ps1'))
    for script in scripts:
        command = ("$t=$null; $e=$null; [System.Management.Automation.Language.Parser]::ParseFile(" +
            "'" + str(script).replace("'", "''") + "', [ref]$t, [ref]$e) | Out-Null; " +
            "if ($e.Count) { throw 'PowerShell syntax failure' }; 'PARSE_PASS'")
        assert 'PARSE_PASS' in run(['pwsh', '-NoProfile', '-NonInteractive', '-Command', command])
        source = script.read_text(encoding='utf-8').lower()
        for forbidden in ('set-applockerpolicy -', 'start-service ', 'new-service ', 'sc.exe create',
                          'register-scheduledtask ', '-verb runas'):
            assert forbidden not in source
    builder_path = ROOT / 'agent_bridge/scripts/build_user_package.py'
    spec = importlib.util.spec_from_file_location('f1_static_package_builder', builder_path)
    builder = importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)
    with tempfile.TemporaryDirectory(prefix='f1-wheel-contract-') as directory:
        wheel = Path(directory) / 'fixture.whl'
        package = ROOT / 'agent_bridge/src/fox2_agent_bridge'
        with zipfile.ZipFile(wheel, 'w') as archive:
            for p in sorted(package.rglob('*.py')):
                archive.write(p, 'fox2_agent_bridge/' + p.relative_to(package).as_posix())
        verified = builder.verify_wheel_source_modules(wheel, ROOT / 'agent_bridge')
        assert all('fox2_agent_bridge/' + n in verified for n in (
            'f1_service.py', 'f1_windows.py', 'f1_authority.py', 'f1_protocol.py',
            'f1_policy.py', 'f1_client.py', 'f1_broker_store.py', 'f1_reconcile.py'))
    print(json.dumps({'syntax': 'PASS', 'allowlist': 'PASS', 'diff_check': 'PASS',
        'powershell_scripts_parsed': len(scripts), 'wheel_source_contract_modules': len(verified),
        'actual_offline_package_build': 'NOT_RUN_NO_ISOLATED_BUILD_ENV',
        'effective_policy_mutation': False, 'service_install_start': False}))


if __name__ == '__main__':
    main()
