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
