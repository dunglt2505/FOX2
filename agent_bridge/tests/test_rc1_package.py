"""Windows path aliases and incomplete RC1 publications fail before installation."""
import hashlib
import json
import zipfile

import pytest
from fox2_agent_bridge.installation import verified_package
from test_installation import package
from fox2_agent_bridge import installation
from fox2_agent_bridge.process_lock import ProcessLock
from fox2_agent_bridge.errors import LockHeld


@pytest.mark.parametrize('name', ['desktop/CON.dll', 'desktop/name.dll.', 'desktop/name.dll ', 'desktop/aux.exe'])
def test_windows_aliases_rejected_before_extraction(tmp_path, name):
    path, sha = package(tmp_path, {name: b'payload'})
    with pytest.raises(ValueError, match='unsafe'):
        verified_package(path, sha)


def test_case_collision_rejected_before_extraction(tmp_path):
    path, sha = package(tmp_path, {'desktop/a.dll': b'a', 'desktop/A.dll': b'b'})
    with pytest.raises(ValueError, match='unsafe'):
        verified_package(path, sha)


def test_incomplete_rc1_desktop_rejected_before_installation(tmp_path):
    path, sha = package(tmp_path, {'desktop/FOX2.Bridge.Desktop.exe': b'partial'}, desktop='NET8_WPF_SELF_CONTAINED_WIN_X64')
    with pytest.raises(ValueError, match='incomplete Desktop'):
        verified_package(path, sha)


def test_live_desktop_blocks_uninstall_before_any_file_deletion(tmp_path, monkeypatch):
    root = tmp_path / 'owned'; monkeypatch.setattr(installation, 'BRIDGE_ROOT', root)
    version = root / 'versions' / ('a' * 64); version.mkdir(parents=True)
    (version / 'receipt.json').write_text('{}')
    (version / 'keep.exe').write_bytes(b'owned-presentation')
    (root / 'current.json').write_text(json.dumps({'package_sha256': 'a' * 64}))
    with ProcessLock(root.parent / 'BridgeDesktop/desktop.lock'):
        with pytest.raises(LockHeld): installation.uninstall(root=root)
    assert (version / 'keep.exe').read_bytes() == b'owned-presentation'
    assert (root / 'current.json').is_file()


def _load_offline_package_builder():
    """Load build logic without installing, packaging or executing Bridge."""
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / "scripts" / "build_user_package.py"
    spec = importlib.util.spec_from_file_location("_fox2_package_builder_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _isolated_environment_fixture(**overrides):
    info = {
        "isolated": True, "setuptools": "80.9.0", "wheel": "0.46.0",
        "python": "3.13", "platform": "win32",
        "dependencies": {
            "jsonschema": "4.25.0", "attrs": "25.3.0",
            "referencing": "0.36.2", "rpds-py": "0.26.0",
            "jsonschema-specifications": "2025.4.1",
        },
    }
    info.update(overrides)
    return info


def test_package_deps_come_from_selected_isolated_build_python(monkeypatch):
    """A caller's installed metadata is not an authoritative wheel pin."""
    from pathlib import Path

    module = _load_offline_package_builder()
    invoked = []

    def fake_run(argv, **kwargs):
        invoked.append(tuple(argv))
        return json.dumps(_isolated_environment_fixture())

    monkeypatch.setattr(module, "run", fake_run)
    selected = Path("synthetic") / "Scripts" / "python.exe"
    result = module.inspect_build_environment(selected)

    assert len(invoked) == 1
    assert invoked[0][:3] == (selected, "-I", "-c")
    interpreter_source = invoked[0][3]
    assert "importlib.metadata as m" in interpreter_source
    assert "m.version(name) for name in names" in interpreter_source
    assert result["dependencies"] == _isolated_environment_fixture()["dependencies"]


@pytest.mark.parametrize(
    "override",
    [
        {"isolated": False},
        {"python": "unknown"},
        {"platform": ""},
        {"setuptools": "79.9.9"},
        {"setuptools": "90.0.0"},
        {"dependencies": {"jsonschema": "4.25.0"}},
        {"dependencies": {**_isolated_environment_fixture()["dependencies"], "attrs": ""}},
    ],
)
def test_package_builder_denies_unverified_or_incomplete_build_environment(
    monkeypatch, override
):
    """No package build proceeds on mismatched or incomplete selected venv."""
    from pathlib import Path

    module = _load_offline_package_builder()
    monkeypatch.setattr(
        module, "run",
        lambda argv, **kwargs: json.dumps(_isolated_environment_fixture(**override)),
    )
    with pytest.raises(ValueError, match="isolated setuptools"):
        module.inspect_build_environment(Path("synthetic") / "Scripts" / "python.exe")


@pytest.mark.parametrize(
    "status_lines, expected",
    [
        ("", "PASS"),
        ("?? agent_bridge/src/fox2_agent_bridge/new_untracked.py\n", "DENY"),
        (" M agent_bridge/scripts/build_user_package.py\n", "DENY"),
        ("?? agent_bridge/src/fox2_agent_bridge/__pycache__/thing.pyc\n", "PASS"),
    ],
)
def test_package_source_commit_provenance_rejects_dirty_packaged_code(
    monkeypatch, status_lines, expected
):
    """Provenance cannot claim a Git source if packaged code is uncommitted."""
    from types import SimpleNamespace

    module = _load_offline_package_builder()
    observed = []
    fixed = "a" * 40

    def fake_git(argv, **kwargs):
        observed.append(tuple(argv))
        assert kwargs["capture_output"] is True
        if "rev-parse" in argv:
            return SimpleNamespace(returncode=0, stdout=fixed + "\n")
        if "status" in argv:
            return SimpleNamespace(returncode=0, stdout=status_lines)
        raise AssertionError("unexpected git operation")

    monkeypatch.setattr(module.subprocess, "run", fake_git)
    if expected == "DENY":
        with pytest.raises(ValueError, match="uncommitted code"):
            module.source_git_commit()
    else:
        assert module.source_git_commit() == fixed
    assert len(observed) == 2


def test_package_source_commit_fails_closed_on_unverified_git(monkeypatch):
    from types import SimpleNamespace

    module = _load_offline_package_builder()
    monkeypatch.setattr(
        module.subprocess, "run",
        lambda argv, **kwargs: SimpleNamespace(returncode=1, stdout=""),
    )
    with pytest.raises(ValueError, match="immutable Git source commit"):
        module.source_git_commit()


def _wheel_source_fixture(tmp_path, *, omit=None, corrupt=None):
    """Only throwaway wheel/module bytes; no user installation is involved."""
    staged = tmp_path / "stage"
    source = staged / "src" / "fox2_agent_bridge"
    source.mkdir(parents=True)
    expected = {
        "__init__.py": b"",
        "ledger.py": b"# durable ledger\n",
        "desktop.py": b"# runtime defaults deny\n",
    }
    for name, data in expected.items():
        (source / name).write_bytes(data)
    wheel = tmp_path / "fox2_agent_bridge-0.0.0-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w") as archive:
        for name, data in expected.items():
            if name != omit:
                archive.writestr(
                    "fox2_agent_bridge/" + name,
                    b"altered bytes" if name == corrupt else data,
                )
    return staged, wheel


def test_package_wheel_modules_match_staged_source_hashes(tmp_path):
    import hashlib

    module = _load_offline_package_builder()
    source, wheel = _wheel_source_fixture(tmp_path)
    hashes = module.verify_wheel_source_modules(wheel, source)

    assert hashes["fox2_agent_bridge/ledger.py"] == hashlib.sha256(
        (source / "src/fox2_agent_bridge/ledger.py").read_bytes()
    ).hexdigest()
    assert set(hashes) == {
        "fox2_agent_bridge/__init__.py",
        "fox2_agent_bridge/ledger.py",
        "fox2_agent_bridge/desktop.py",
    }


@pytest.mark.parametrize(
    "variant, name",
    [
        ("omit", "ledger.py"),
        ("corrupt", "desktop.py"),
    ],
)
def test_package_wheel_disagrees_with_source_fails_closed(tmp_path, variant, name):
    module = _load_offline_package_builder()
    source, wheel = _wheel_source_fixture(tmp_path, **{variant: name})
    with pytest.raises(ValueError, match="wheel module"):
        module.verify_wheel_source_modules(wheel, source)


def _load_lifecycle_harness():
    """Import only: no real host lifecycle or installed command is executed."""
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parents[1] / 'scripts/certify_user_lifecycle.py'
    spec = importlib.util.spec_from_file_location('_fox2_lifecycle_test', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def lifecycle_fixture(tmp_path):
    root = tmp_path / 'Bridge'
    sha = 'a' * 64
    version = root / 'versions' / sha
    version.mkdir(parents=True)
    (root / 'current.json').write_text(json.dumps({'package_sha256': sha}))
    (root / 'uninstall.ps1').write_text('# fixture supervisor, never executed')
    for directory in ('config', 'data', 'logs', 'reports'):
        (root / directory).mkdir()
        (root / directory / 'keep').write_bytes(b'durable fixture')
    (root / 'config/bridge.toml').write_bytes(b'# durable config')
    (root / 'data/bridge.db').write_bytes(b'durable database fixture')
    (root / 'data/manual_consumption.json').write_text(json.dumps({'dispatch_ids': ['consumed']}))
    return root, sha, tmp_path / 'lifecycle.json'


@pytest.mark.parametrize('exit_code', [0, 17])
def test_lifecycle_main_uses_external_supervisor_and_checkpoints_before_reinstall(
    lifecycle_fixture, monkeypatch, capsys, exit_code
):
    """Exercise the entire harness with host/process/install boundaries replaced."""
    import shutil
    import subprocess

    module = _load_lifecycle_harness()
    root, sha, evidence = lifecycle_fixture
    durable = {p: p.read_bytes() for directory in ('config', 'data', 'logs', 'reports')
               for p in (root / directory).iterdir()}
    monkeypatch.setattr(module, 'BRIDGE_ROOT', root)
    monkeypatch.setenv('PYTHONPATH', 'invalid-inherited-path')
    monkeypatch.setenv('PYTHONHOME', 'invalid-inherited-home')
    monkeypatch.setenv('FOX2_LIFECYCLE_SENTINEL', 'preserved')
    supervisor_calls = []
    install_calls = []
    stopped = False
    reinstalled = False
    presentation_live = False
    launch_calls = []
    ui_actions = []
    lock = root.parent / 'BridgeDesktop/desktop.lock'
    lock.parent.mkdir()
    lock.write_bytes(b'presentation lock fixture')
    desktop = root / 'versions' / sha / 'payload/desktop/FOX2.Bridge.Desktop.exe'
    desktop.parent.mkdir(parents=True)
    desktop.write_bytes(b'presentation fixture')
    path_open = module.Path.open

    def open_lock(path, *args, **kwargs):
        if path == lock and presentation_live:
            error = PermissionError('fixture WPF FileShare.None')
            error.winerror = 32
            raise error
        return path_open(path, *args, **kwargs)

    monkeypatch.setattr(module.Path, 'open', open_lock)

    def child(argv, **kwargs):
        nonlocal stopped, presentation_live
        assert not supervisor_calls, 'no command may follow a failed supervisor'
        if argv[-1] == str(root / 'uninstall.ps1'):
            assert stopped and not presentation_live and ui_actions == ['inspect', 'check', 'exit']
            assert len(launch_calls) == 2
            assert argv == [r'C:\Program Files\PowerShell\7\pwsh.exe',
                            '-NoProfile', '-NonInteractive', '-File', str(root / 'uninstall.ps1')]
            assert kwargs['cwd'] == root
            assert kwargs['capture_output'] and kwargs['text'] and kwargs['timeout'] == 90
            assert kwargs['errors'] == 'replace'
            assert not {'PYTHONPATH', 'PYTHONHOME'} & {k.upper() for k in kwargs['env']}
            assert kwargs['env']['FOX2_LIFECYCLE_SENTINEL'] == 'preserved'
            assert not module.Path(argv[0]).is_relative_to(root / 'versions')
            supervisor_calls.append(argv)
            if exit_code == 0:
                shutil.rmtree(root / 'versions')
                (root / 'current.json').unlink()
            return subprocess.CompletedProcess(argv, exit_code,
                'supervisor-output password="private fixture value"\n' + 'x' * 5000,
                'supervisor-error Bearer fixture-value\n' + 'e' * 5000)
        if '-Command' in argv:
            if 'Get-ScheduledTask' in argv[-1]:
                payload = {'run_level': 'Limited', 'logon_type': 'Interactive',
                           'action': 'launch.ps1', 'instances': 'IgnoreNew'}
                return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')
            assert "Name='FOX2.Bridge.Desktop.exe'" in argv[-1]
            payload = [{'ProcessId': 1234, 'ExecutablePath': str(desktop)}] if presentation_live else []
            return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')
        if '-File' in argv:
            if argv[-1] == str(root / 'launch.ps1'):
                launch_calls.append(argv)
                presentation_live = True
                return subprocess.CompletedProcess(argv, 0, '', '')
            assert module.Path(argv[argv.index('-File') + 1]).name == 'certify_rc1_ui.ps1'
            action = argv[-1]
            ui_actions.append(action)
            payload = {'screens': ['Dashboard', 'Activity', 'Agents', 'Diagnostics', 'Artifacts', 'Settings'],
                       'process_id': 1234, 'check_now_enabled': False}
            output = json.dumps(payload) if action == 'inspect' else 'PAUSED_CHECK_DISABLED'
            if action == 'exit':
                stopped = True
                presentation_live = False
                output = 'EXIT_INVOKED'
            return subprocess.CompletedProcess(argv, 0, output, '')
        assert argv[1:4] == ['-I', '-m', 'fox2_agent_bridge']
        args = argv[4:]
        assert args[0] != 'uninstall', 'installed Python must never uninstall'
        assert args[0] != 'worker' and args != ['control', 'request-exit']
        if args == ['control', 'status']:
            payload = {'paused': True, 'state': 'STOPPED' if stopped else 'PAUSED',
                       'stop_requested': stopped, 'setup_complete': True, 'current_dispatch': None}
        elif args[0] == 'status':
            payload = {'dispatch': {'dispatch_state': 'NEEDS_RECONCILIATION'}}
        else:
            payload = {'status': 'FIXTURE_OK'}
        return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')

    # After success, remaining installed control calls are permitted only after
    # the reinstall stub verifies that the uninstall evidence was already saved.
    def run(argv, **kwargs):
        if reinstalled:
            assert argv[4] in {'setup', 'status', 'control'}
            payload = ({'dispatch': {'dispatch_state': 'NEEDS_RECONCILIATION'}}
                       if argv[4] == 'status' else {'paused': True, 'setup_complete': True,
                       'current_dispatch': None, 'state': 'STOPPED'})
            return subprocess.CompletedProcess(argv, 0, json.dumps(payload), '')
        return child(argv, **kwargs)

    def reinstall(package, expected_sha):
        nonlocal reinstalled
        saved = json.loads(evidence.read_text())['uninstall']
        assert saved['status'] == 'UNINSTALLED' and saved['exit_code'] == 0
        assert all(saved['post_uninstall'].values())
        install_calls.append((package, expected_sha))
        reinstalled = True
        (root / 'versions' / sha).mkdir(parents=True)
        (root / 'current.json').write_text(json.dumps({'package_sha256': sha}))
        return {'status': 'INSTALLED'}

    monkeypatch.setattr(module.subprocess, 'run', run)
    monkeypatch.setattr(module, 'install', reinstall)
    if exit_code:
        with pytest.raises(RuntimeError, match='evidence persisted; no retry'):
            module.main(root / 'fixture.zip', sha, evidence)
        assert not install_calls and 'USER_LIFECYCLE=PASS' not in capsys.readouterr().out
    else:
        module.main(root / 'fixture.zip', sha, evidence)
        assert len(install_calls) == 1
        assert 'USER_LIFECYCLE=PASS' in capsys.readouterr().out
    saved = json.loads(evidence.read_text())
    result = saved['uninstall']
    assert saved['worker_f1_health'] == 'NOT_APPLICABLE_PRE_G3'
    assert saved['presentation']['count'] == 1 and saved['presentation']['two_launches']
    assert saved['presentation_lock_released'] and saved['graceful_exit']['explicit_ui_exit']
    assert len(supervisor_calls) == 1 and result['exit_code'] == exit_code
    assert result['supervisor']['kind'] == 'STABLE_EXTERNAL_POWERSHELL7'
    assert result['supervisor']['path'] == 'BridgeRoot/uninstall.ps1'
    assert len(result['supervisor']['sha256']) == 64
    assert result['stdout'].startswith('supervisor-output')
    assert len(result['stdout']) == module.UNINSTALL_OUTPUT_LIMIT
    assert result['stderr'].startswith('supervisor-error')
    assert len(result['stderr']) == module.UNINSTALL_OUTPUT_LIMIT
    assert 'private fixture value' not in evidence.read_text()
    assert 'fixture-value' not in evidence.read_text()
    assert result['post_uninstall']['current_pointer_absent'] == (exit_code == 0)
    assert result['post_uninstall']['versions_absent'] == (exit_code == 0)
    assert result['post_uninstall']['configuration_preserved']
    assert result['post_uninstall']['database_preserved']
    assert result['post_uninstall']['consumption_file_preserved']
    assert all(p.read_bytes() == original for p, original in durable.items())
    if exit_code == 0:
        assert len(saved['durable_consumption']) == 4
        assert set(saved['durable_consumption'].values()) == {'NEEDS_RECONCILIATION'}


@pytest.mark.parametrize('failure', ['timeout', 'start', 'incomplete', 'config', 'consumption', 'unreadable_checks'])
def test_lifecycle_uninstall_failure_always_persists_and_stops(lifecycle_fixture, monkeypatch, failure):
    import subprocess

    module = _load_lifecycle_harness()
    root, _, evidence = lifecycle_fixture
    before = (root / 'config/bridge.toml').read_bytes()
    calls = []

    def run(argv, **kwargs):
        calls.append(argv)
        if failure == 'timeout':
            raise subprocess.TimeoutExpired(argv, 90, b'partial password=fixture-private', b'partial error')
        if failure == 'start':
            raise OSError('private host details')
        if failure == 'unreadable_checks':
            (root / 'config/bridge.toml').unlink()
            return subprocess.CompletedProcess(argv, 23, 'failed stdout', 'failed stderr')
        if failure in {'config', 'consumption'}:
            (root / 'current.json').unlink()
            (root / 'versions' / ('a' * 64)).rmdir()
            path = root / ('config/bridge.toml' if failure == 'config' else 'data/manual_consumption.json')
            path.write_bytes(b'changed')
        return subprocess.CompletedProcess(argv, 0, 'supervisor finished', '')

    monkeypatch.setattr(module.subprocess, 'run', run)
    with pytest.raises(RuntimeError, match='no retry'):
        module.certify_uninstall(root, root.parent / 'pwsh.exe', before, {}, evidence)
    result = json.loads(evidence.read_text())['uninstall']
    assert len(calls) == 1
    assert result['status'] == {'timeout': 'SUPERVISOR_TIMEOUT', 'start': 'SUPERVISOR_START_FAILED',
                               'unreadable_checks': 'SUPERVISOR_FAILED'}.get(
        failure, 'POSTCONDITION_FAILED')
    assert 'fixture-private' not in evidence.read_text() and 'private host details' not in evidence.read_text()
    if failure == 'timeout':
        assert result['exit_code'] is None and result['stdout'].startswith('partial')
        assert result['stderr'] == 'partial error'
    if failure == 'unreadable_checks':
        assert result['exit_code'] == 23 and result['post_uninstall'] == {'checks_unavailable': True}
        assert result['stdout'] == 'failed stdout' and result['stderr'] == 'failed stderr'


@pytest.mark.parametrize('installed_parent', [False, True])
def test_lifecycle_rejects_installed_supervisor_or_parent_before_launch(
    lifecycle_fixture, monkeypatch, installed_parent
):
    module = _load_lifecycle_harness()
    root, sha, evidence = lifecycle_fixture
    installed_python = root / 'versions' / sha / 'runtime/Scripts/python.exe'
    pwsh = root.parent / 'pwsh.exe' if installed_parent else installed_python
    if installed_parent:
        monkeypatch.setattr(module.sys, 'executable', str(installed_python))
    monkeypatch.setattr(module.subprocess, 'run', lambda *a, **k: pytest.fail('must fail before launch'))
    with pytest.raises(ValueError, match='stable external supervisors'):
        module.certify_uninstall(root, pwsh, b'# durable config', {}, evidence)


def test_lifecycle_uninstall_output_redacts_before_limit():
    module = _load_lifecycle_harness()
    values = ['ghp_' + 'x' * 30, 'sk-' + 'x' * 30, 'Bearer fixture',
              'https://fixture:private@example.invalid/', 'api_key="private fixture"',
              '-----BEGIN PRIVATE KEY-----\nfixture\n-----END PRIVATE KEY-----']
    for value in values:
        assert 'private' not in module._uninstall_output(value).lower()
        assert 'fixture' not in module._uninstall_output(value).lower() or value.startswith('https')
        assert len(module._uninstall_output('x' * 4090 + value)) <= module.UNINSTALL_OUTPUT_LIMIT
