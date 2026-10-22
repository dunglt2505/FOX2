"""Offline Phase-2 WPF contract fixtures; every subprocess is intercepted."""
import importlib.util
import errno
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
               'observations': 0, 'control_reads': 0, 'already_live': False,
               'denial': 'sharing',
               'state': {'paused': True, 'setup_complete': True,
                         'current_dispatch': None, 'state': 'STOPPED'}}
    monkeypatch.setattr(module, 'installed_version', lambda _: {
        'package_sha256': 'b' * 64 if fixture['variant'] == 'pointer_drift' else sha})
    ticks = iter(range(1000))
    monkeypatch.setattr(module.time, 'monotonic', lambda: next(ticks))
    monkeypatch.setattr(module.time, 'sleep', lambda _: None)
    path_open = Path.open

    def open_lock(path, *args, **kwargs):
        if path == lock and args == ('r+b',):
            fixture['events'].append('lock_probe')
            assert args == ('r+b',) and not kwargs
            live = fixture['already_live'] or fixture['launches'] > 0
            if (live and not fixture['exited'] and fixture['variant'] != 'live_lock_free' or
                    fixture['variant'] == 'pre_denied' or
                    fixture['exited'] and fixture['variant'] == 'lock_retained'):
                if fixture['denial'] == 'unrelated':
                    raise OSError(errno.EIO, 'private fixture path must not escape')
                error = PermissionError(errno.EACCES, 'private fixture path must not escape')
                if fixture['denial'] != 'eacces':
                    error.winerror = 5 if fixture['variant'] == 'lock_access_denied' else 32
                raise error
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
                "$ErrorActionPreference='Stop'; "
                'ConvertTo-Json -Compress -InputObject @(Get-CimInstance Win32_Process '
                '-Filter "Name=\'FOX2.Bridge.Desktop.exe\'" | Select-Object ProcessId,ExecutablePath)')
            fixture['events'].append('observe')
            fixture['observations'] += 1
            if variant == 'observe_failure':
                return subprocess.CompletedProcess(argv, 1, '', 'fixture query failure')
            if variant == 'observe_timeout':
                raise subprocess.TimeoutExpired(argv, kwargs['timeout'])
            record = {'ProcessId': 42, 'ExecutablePath': str(desktop)}
            if variant == 'pid_changed' and fixture['observations'] > (1 if fixture['already_live'] else 2):
                record['ProcessId'] = 43
            if variant == 'invalid_pid':
                record['ProcessId'] = 0
            if variant == 'old_package':
                record['ExecutablePath'] = str(root / 'versions' / ('b' * 64) / desktop.name)
            if variant == 'unknown_path':
                record['ExecutablePath'] = None
            records = [record, record] if variant == 'duplicate' else [record]
            if (not fixture['already_live'] and not fixture['launches'] or
                    variant == 'missing' or fixture['exited'] and variant != 'exit_timeout'):
                records = []
            output = json.dumps(records)
            if variant == 'null_after_exit' and fixture['exited']:
                output = 'null'
        elif argv[-1] == str(root / 'launch.ps1'):
            fixture['events'].append('launch')
            fixture['launches'] += 1
            if variant == 'lock_missing' and lock.exists():
                lock.unlink()
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
                if variant == 'lock_replaced':
                    lock.rename(lock.with_suffix('.old'))
                    lock.write_bytes(b'replacement')
                output = 'WRONG' if variant == 'exit_marker' else 'EXIT_INVOKED'
            else:
                pytest.fail('unexpected UI action')
        return subprocess.CompletedProcess(argv, 0, output, '')

    monkeypatch.setattr(module.subprocess, 'run', run)

    def cli(*args):
        assert args == ('control', 'status'), 'No Worker/F1/control mutation permitted'
        state = dict(fixture['state'])
        fixture['control_reads'] += 1
        if fixture['variant'] == 'unsafe_before_exit' and fixture['control_reads'] > 1:
            state['current_dispatch'] = 'active'
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
    'old_package', 'unknown_path', 'pointer_drift', 'duplicate', 'missing', 'invalid_pid',
    'pre_denied', 'lock_missing', 'lock_replaced',
    'live_lock_free', 'lock_access_denied', 'launch_failure', 'inspect_failure', 'check_failure', 'exit_failure',
    'wrong_ui_pid', 'navigation', 'enabled_check', 'check_marker', 'exit_marker',
    'exit_timeout', 'lock_retained', 'unsafe_after_exit', 'not_stopped_after_exit',
    'observe_failure', 'observe_timeout', 'null_after_exit', 'pid_changed', 'unsafe_before_exit',
])
def test_presentation_failure_checkpoints_before_uninstall(presentation, variant):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture['variant'] = variant
    with pytest.raises((RuntimeError, PermissionError, subprocess.TimeoutExpired)):
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


@pytest.mark.parametrize('field', ['paused', 'setup_complete', 'current_dispatch'])
def test_missing_safe_control_field_rejected_before_launch(presentation, field):
    module, root, sha, cli, evidence, fixture, _ = presentation
    del fixture['state'][field]
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


@pytest.mark.parametrize('continuation', [False, True])
def test_main_stops_before_uninstall_when_presentation_gate_fails(tmp_path, monkeypatch, continuation):
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

    def fail_gate(*args, **kwargs):
        assert kwargs == {'continuation': continuation}
        raise RuntimeError('fixture presentation rejected')

    monkeypatch.setattr(module.subprocess, 'run', child)
    monkeypatch.setattr(module, 'certify_presentation', fail_gate)
    monkeypatch.setattr(module, 'certify_uninstall', lambda *a: pytest.fail('must not uninstall'))
    monkeypatch.setattr(module, 'install', lambda *a: pytest.fail('must not reinstall'))
    with pytest.raises(RuntimeError, match='presentation rejected'):
        module.main(tmp_path / 'unused.zip', 'a' * 64, tmp_path / 'evidence.json',
                    continuation=continuation)


@pytest.mark.parametrize('continuation,already_live,denial,launches', [
    (False, False, 'sharing', 2), (False, False, 'eacces', 2),
    (True, True, 'sharing', 0), (True, True, 'eacces', 0),
    (True, False, 'sharing', 1), (True, False, 'eacces', 1),
])
def test_differential_lock_proof(presentation, continuation, already_live, denial, launches):
    module, root, sha, cli, evidence, fixture, lock = presentation
    fixture.update(already_live=already_live, denial=denial)
    checkpoints = []
    write_json = module.write_json

    def checkpoint(path, results):
        checkpoints.append(json.loads(json.dumps(results)))
        write_json(path, results)

    module.write_json = checkpoint
    results = {}
    module.certify_presentation(root, sha, 'fixture-pwsh7', cli, results, evidence,
                                continuation=continuation)
    assert fixture['launches'] == launches
    probes = results['presentation_lock_probes']
    assert ('pre_live' in probes) is not already_live
    assert probes['post_exit']['classification'] == 'OPENABLE'
    assert results['presentation_lock_status'] == 'PRESENTATION_LOCK_HELD'
    assert results['live_presentation_lock_held'] and results['presentation_lock_released']
    assert results['worker_f1_health'] == 'NOT_APPLICABLE_PRE_G3'
    if already_live and denial == 'eacces':
        assert checkpoints[0]['presentation_lock_status'] == 'PROVISIONAL_ACCESS_DENIED'
        assert 'live_presentation_lock_held' not in checkpoints[0]
    assert lock.read_bytes() == b'unchanged lock bytes'
    assert 'private fixture path' not in evidence.read_text()


@pytest.mark.parametrize('variant', [
    'lock_retained', 'live_lock_free', 'old_package', 'unknown_path', 'pointer_drift',
    'duplicate', 'invalid_pid', 'pid_changed', 'wrong_ui_pid', 'navigation', 'enabled_check',
    'unsafe_before_exit', 'unsafe_after_exit', 'not_stopped_after_exit', 'lock_replaced',
])
def test_continuation_fails_closed_without_launch(presentation, variant):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture.update(already_live=True, denial='eacces', variant=variant)
    with pytest.raises(RuntimeError):
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, {}, evidence,
                                    continuation=True)
    assert fixture['launches'] == 0
    proof = json.loads(evidence.read_text())
    assert proof['presentation_status'] == 'FAILED_BEFORE_UNINSTALL'
    if variant not in {'unsafe_after_exit', 'not_stopped_after_exit'}:
        assert not proof.get('live_presentation_lock_held', False)
    if variant == 'lock_retained':
        assert fixture['exited']
        assert proof['presentation_lock_probes']['post_exit']['classification'] == 'ACCESS_DENIED_REQUIRES_DIFFERENTIAL'


@pytest.mark.parametrize('continuation', [False, True])
def test_unrelated_oserror_is_bounded_and_rejected(presentation, continuation):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture.update(already_live=continuation, denial='unrelated')
    with pytest.raises(RuntimeError, match='denial is not proven') as failure:
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, {}, evidence,
                                    continuation=continuation)
    probe = json.loads(evidence.read_text())['presentation_lock_probes']['live']
    assert probe == {'exception_class': 'OSError', 'errno': errno.EIO,
                     'winerror': None, 'classification': 'UNRELATED_OSERROR'}
    assert 'private fixture path' not in str(failure.value) + evidence.read_text()


def test_pre_live_denial_stops_before_launch(presentation):
    module, root, sha, cli, evidence, fixture, _ = presentation
    fixture.update(variant='pre_denied', denial='eacces')
    with pytest.raises(RuntimeError, match='Pre-live'):
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, {}, evidence)
    assert fixture['launches'] == 0


@pytest.mark.parametrize('continuation', [False, True])
@pytest.mark.parametrize('denial', ['sharing', 'eacces'])
def test_absent_pre_live_lock_requires_sharing_violation(presentation, monkeypatch, continuation, denial):
    module, root, sha, cli, evidence, fixture, lock = presentation
    fixture['denial'] = denial
    lock.unlink()
    run = module.subprocess.run

    def create_on_launch(argv, **kwargs):
        if argv[-1] == str(root / 'launch.ps1') and not lock.exists():
            with open(lock, 'xb') as stream:
                stream.write(b'unchanged lock bytes')
        return run(argv, **kwargs)

    monkeypatch.setattr(module.subprocess, 'run', create_on_launch)
    results = {}
    if denial == 'eacces':
        with pytest.raises(RuntimeError, match='lacks pre-live openability proof'):
            module.certify_presentation(root, sha, 'fixture-pwsh7', cli, results, evidence,
                                        continuation=continuation)
        proof = json.loads(evidence.read_text())
        assert proof['presentation_status'] == 'FAILED_BEFORE_UNINSTALL'
        assert proof['presentation_lock_probes']['live']['classification'] == 'ACCESS_DENIED_REQUIRES_DIFFERENTIAL'
        assert not proof.get('live_presentation_lock_held', False)
        assert 'presentation_lock_status' not in proof
        assert not fixture['exited'] and 'inspect' not in fixture['events']
    else:
        module.certify_presentation(root, sha, 'fixture-pwsh7', cli, results, evidence,
                                    continuation=continuation)
        assert results['presentation_lock_status'] == 'PRESENTATION_LOCK_HELD'
        assert results['presentation_lock_probes']['post_exit']['classification'] == 'OPENABLE'
    assert fixture['launches'] == (1 if continuation else 2)
    assert results['presentation_lock_probes']['pre_live']['classification'] == 'ABSENT'
    assert lock.read_bytes() == b'unchanged lock bytes'
