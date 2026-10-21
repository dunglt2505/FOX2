"""Offline Phase-2 WPF contract fixtures; every subprocess is intercepted."""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest


def load_harness():
    path = Path(__file__).parents[1] / 'scripts/certify_user_lifecycle.py'
    spec = importlib.util.spec_from_file_location('_wpf_lifecycle_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def presentation(tmp_path, monkeypatch):
    module = load_harness()
    root = tmp_path / 'Bridge'
    sha = 'a' * 64
    desktop = root / 'versions' / sha / 'payload/desktop/FOX2.Bridge.Desktop.exe'
    desktop.parent.mkdir(parents=True)
    desktop.write_bytes(b'exact package fixture')
    lock = root.parent / 'BridgeDesktop/desktop.lock'
    lock.parent.mkdir()
    lock.write_bytes(b'unchanged lock bytes')
    fixture = {'variant': 'ok', 'events': [], 'exited': False, 'launches': 0,
               'state': {'paused': True, 'setup_complete': True,
                         'current_dispatch': None, 'state': 'STOPPED'}}
    monkeypatch.setattr(module, 'installed_version', lambda _: {
        'package_sha256': 'b' * 64 if fixture['variant'] == 'pointer_drift' else sha})
    ticks = iter(range(1000))
    monkeypatch.setattr(module.time, 'monotonic', lambda: next(ticks))
    monkeypatch.setattr(module.time, 'sleep', lambda _: None)
    path_open = Path.open

    def open_lock(path, *args, **kwargs):
        if path == lock:
            fixture['events'].append('lock_probe')
            if (not fixture['exited'] and fixture['variant'] != 'live_lock_free' or
                    fixture['variant'] == 'lock_retained'):
                raise PermissionError('fixture exclusive WPF lock')
        return path_open(path, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', open_lock)
    monkeypatch.setenv('PYTHONPATH', 'untrusted-fixture')
    monkeypatch.setenv('PYTHONHOME', 'untrusted-fixture')

    def run(argv, **kwargs):
        variant = fixture['variant']
        assert argv[:3] == ['fixture-pwsh7', '-NoProfile', '-NonInteractive']
        assert kwargs['capture_output'] and kwargs['text'] and kwargs['timeout'] <= 120
        assert not {'PYTHONPATH', 'PYTHONHOME'} & {k.upper() for k in kwargs['env']}
        output = ''
        if '-Command' in argv:
            assert argv[-1] == (
                'ConvertTo-Json -Compress -InputObject @(Get-CimInstance Win32_Process '
                '-Filter "Name=\'FOX2.Bridge.Desktop.exe\'" | Select-Object ProcessId,ExecutablePath)')
            fixture['events'].append('observe')
            record = {'ProcessId': 42, 'ExecutablePath': str(desktop)}
            if variant == 'old_package':
                record['ExecutablePath'] = str(root / 'versions' / ('b' * 64) / desktop.name)
            if variant == 'unknown_path':
                record['ExecutablePath'] = None
            records = [record, record] if variant == 'duplicate' else [record]
            if variant == 'missing' or fixture['exited'] and variant != 'exit_timeout':
                records = []
            output = json.dumps(records)
        elif argv[-1] == str(root / 'launch.ps1'):
            fixture['events'].append('launch')
            fixture['launches'] += 1
            assert argv[3:] == ['-WindowStyle', 'Hidden', '-File', str(root / 'launch.ps1')]
            if variant == 'launch_failure':
                return subprocess.CompletedProcess(argv, 1, '', '')
        else:
            assert argv[3:5] == ['-File', str(Path(module.__file__).with_name('certify_rc1_ui.ps1'))]
            assert argv[5] == '-Action'
            action = argv[6]
            fixture['events'].append(action)
            if variant == action + '_failure':
                return subprocess.CompletedProcess(argv, 1, '', '')
            if action == 'inspect':
                output = json.dumps({'screens': ['Dashboard', 'Activity', 'Agents', 'Diagnostics', 'Artifacts', 'Settings']
                    if variant != 'navigation' else ['Dashboard'],
                    'process_id': 7 if variant == 'wrong_ui_pid' else 42,
                    'check_now_enabled': variant == 'enabled_check'})
            elif action == 'check':
                output = 'WRONG' if variant == 'check_marker' else 'PAUSED_CHECK_DISABLED'
            elif action == 'exit':
                fixture['exited'] = True
                output = 'WRONG' if variant == 'exit_marker' else 'EXIT_INVOKED'
            else:
                pytest.fail('unexpected UI action')
        return subprocess.CompletedProcess(argv, 0, output, '')

    monkeypatch.setattr(module.subprocess, 'run', run)

    def cli(*args):
        assert args == ('control', 'status'), 'No Worker/F1/control mutation permitted'
        state = dict(fixture['state'])
        if fixture['variant'] == 'unsafe_after_exit' and fixture['exited']:
            state['paused'] = False
        if fixture['variant'] == 'not_stopped_after_exit' and fixture['exited']:
            state['state'] = 'PAUSED'
        return state

    return module, root, sha, cli, tmp_path / 'proof.json', fixture, lock


def test_launch_twice_exact_singleton_paused_ui_and_graceful_exit(presentation):
    module, root, sha, cli, evidence, fixture, lock = presentation
    results = {}
    module.certify_presentation(root, sha, 'fixture-pwsh7', cli, results, evidence)
    assert fixture['launches'] == 2
    assert fixture['events'].index('inspect') < fixture['events'].index('check') < fixture['events'].index('exit')
    assert fixture['events'][-2:] == ['observe', 'lock_probe']
    assert results['presentation']['package_sha256'] == sha
    assert results['presentation']['process_id'] == 42
    assert results['presentation']['count'] == 1
    assert results['live_presentation_lock_held'] and results['presentation_lock_released']
    assert results['graceful_exit']['presentation_count'] == 0
    assert results['worker_f1_health'] == 'NOT_APPLICABLE_PRE_G3'
    assert 'heartbeat' not in results and 'heartbeat' not in fixture['state']
    assert json.loads(evidence.read_text()) == results
    assert lock.read_bytes() == b'unchanged lock bytes'


@pytest.mark.parametrize('variant', [
    'old_package', 'unknown_path', 'pointer_drift', 'duplicate', 'missing',
    'live_lock_free', 'launch_failure', 'inspect_failure', 'check_failure', 'exit_failure',
    'wrong_ui_pid', 'navigation', 'enabled_check', 'check_marker', 'exit_marker',
    'exit_timeout', 'lock_retained', 'unsafe_after_exit', 'not_stopped_after_exit',
])
def test_presentation_failure_checkpoints_before_uninstall(presentation, variant):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture['variant'] = variant
    with pytest.raises((RuntimeError, PermissionError)):
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, {}, evidence)
    proof = json.loads(evidence.read_text())
    assert proof['presentation_status'] == 'FAILED_BEFORE_UNINSTALL'
    assert proof['worker_f1_health'] == 'NOT_APPLICABLE_PRE_G3'
    assert 'uninstall' not in proof and 'reinstall' not in proof


@pytest.mark.parametrize('unsafe', [
    {'paused': False}, {'setup_complete': False}, {'current_dispatch': 'active'},
    {'paused': None}, {'setup_complete': None},
])
def test_paused_setup_no_current_dispatch_required_before_launch(presentation, unsafe):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture['state'].update(unsafe)
    with pytest.raises(RuntimeError, match='Phase-2 requires'):
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, {}, evidence)
    assert fixture['launches'] == 0


def test_no_legacy_tray_worker_heartbeat_or_f1_g3_mutation():
    source = Path(load_harness().__file__).read_text()
    for forbidden in ('desktop_tray.ps1', 'desktop_launcher.ps1', 'heartbeat',
                      "cli('control','request-exit')", "'worker'", 'Start-Service',
                      'Stop-Process', 'taskkill', 'AppLocker', 'AppIDSvc', 'sc.exe'):
        assert forbidden not in source
    assert 'NOT_APPLICABLE_PRE_G3' in source


def test_main_stops_before_uninstall_when_presentation_gate_fails(tmp_path, monkeypatch):
    module = load_harness()
    root = tmp_path / 'Bridge'
    (root / 'config').mkdir(parents=True)
    (root / 'config/bridge.toml').write_bytes(b'fixture')
    monkeypatch.setattr(module, 'BRIDGE_ROOT', root)
    monkeypatch.setattr(module, 'installed_version', lambda _: {'package_sha256': 'a' * 64})

    def child(argv, **kwargs):
        if '-Command' in argv:
            payload = {'run_level': 'Limited', 'logon_type': 'Interactive',
                       'action': 'launch.ps1', 'instances': 'IgnoreNew'}
        else:
            assert argv[4:] in (['control', 'status'], ['setup'],
                                ['control', 'set-start-with-windows', '--enabled', 'true'])
            payload = {'paused': True, 'setup_complete': True, 'current_dispatch': None}
        return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')

    def fail_gate(*args):
        raise RuntimeError('fixture presentation rejected')

    monkeypatch.setattr(module.subprocess, 'run', child)
    monkeypatch.setattr(module, 'certify_presentation', fail_gate)
    monkeypatch.setattr(module, 'certify_uninstall', lambda *a: pytest.fail('must not uninstall'))
    monkeypatch.setattr(module, 'install', lambda *a: pytest.fail('must not reinstall'))
    with pytest.raises(RuntimeError, match='presentation rejected'):
        module.main(tmp_path / 'unused.zip', 'a' * 64, tmp_path / 'evidence.json')
