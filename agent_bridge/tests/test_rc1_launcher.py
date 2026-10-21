"""Launcher creates presentation only; Worker/Agent require the F1 service."""
import subprocess
import ast
from pathlib import Path
import pytest
from fox2_agent_bridge import launcher


@pytest.mark.parametrize('desktop', ['valid', 'missing', 'spawn_failure'])
def test_launcher_independent_children_and_detached_handles(tmp_path, monkeypatch, desktop):
    root = tmp_path / 'owned'; version = root / 'versions' / ('a' * 64)
    python = version / 'runtime/Scripts/python.exe'; python.parent.mkdir(parents=True)
    python.write_bytes(b'owned-runtime-fixture')
    ui = version / 'payload/desktop/FOX2.Bridge.Desktop.exe'
    if desktop != 'missing':
        ui.parent.mkdir(parents=True); ui.write_bytes(b'owned-desktop-fixture')
    monkeypatch.setattr(launcher, 'BRIDGE_ROOT', root)
    monkeypatch.setattr(launcher, 'safe_root', lambda path: path)
    monkeypatch.setattr(launcher, 'installed_version', lambda path: {'package_sha256': 'a' * 64})
    monkeypatch.setattr(launcher.sys, 'executable', str(python))
    monkeypatch.setenv('PYTHONPATH', 'untrusted-source'); monkeypatch.setenv('PYTHONHOME', 'untrusted-home')
    calls = []
    def child(arguments, **kwargs):
        calls.append((arguments, kwargs))
        assert kwargs['stdin'] == kwargs['stdout'] == kwargs['stderr'] == subprocess.DEVNULL
        assert kwargs['close_fds'] is True
        assert kwargs['creationflags'] == subprocess.CREATE_NO_WINDOW
        assert not {'PYTHONPATH', 'PYTHONHOME'} & {k.upper() for k in kwargs['env']}
        assert kwargs['cwd'] == root
        if desktop == 'spawn_failure': raise OSError('UI failure')
        return object()
    monkeypatch.setattr(launcher.subprocess, 'Popen', child)
    result = launcher.launch()
    assert result['worker_started'] is False
    assert result['f1_authority']['decision'] == 'DENY'
    assert result['desktop_started'] == (desktop == 'valid')
    assert len(calls) == (0 if desktop == 'missing' else 1)
    if calls: assert calls[0][0] == [str(ui)]


def test_source_interpreter_cannot_launch_installed_worker(tmp_path, monkeypatch):
    root = tmp_path / 'owned'
    monkeypatch.setattr(launcher, 'BRIDGE_ROOT', root)
    monkeypatch.setattr(launcher, 'safe_root', lambda path: path)
    monkeypatch.setattr(launcher, 'installed_version', lambda path: {'package_sha256': 'a' * 64})
    def forbidden(*args, **kwargs): pytest.fail('unbound interpreter must not spawn')
    monkeypatch.setattr(launcher.subprocess, 'Popen', forbidden)
    with pytest.raises(ValueError, match='current installed interpreter'):
        launcher.launch()


def test_all_runtime_subprocesses_explicitly_hide_console_windows():
    source = Path(__file__).parents[1] / 'src/fox2_agent_bridge'
    found = 0
    for path in source.rglob('*.py'):
        for call in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
            if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and
                    isinstance(call.func.value, ast.Name) and call.func.value.id == 'subprocess' and
                    call.func.attr in {'run', 'Popen'}):
                assert 'creationflags' in {key.arg for key in call.keywords}, (path.name, call.lineno)
                found += 1
    assert found >= 15
