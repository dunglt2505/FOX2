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
