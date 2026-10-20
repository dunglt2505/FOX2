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
