"""Trusted-observer integration with fake OS responses, not host enforcement."""
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from fox2_agent_bridge import f1_service
from fox2_agent_bridge.f1_protocol import AuthorityDeny
from fox2_agent_bridge.f1_service import HostFence
from test_f1_policy import build


@pytest.fixture
def host(tmp_path, monkeypatch):
    root = tmp_path / 'sealed'; root.mkdir()
    executable = root / 'runtime/Scripts/python.exe'
    executable.parent.mkdir(parents=True); executable.write_bytes(b'sealed-fixture')
    database = root / 'broker.sqlite'; database.write_bytes(b'fixture-not-opened')
    xml, manifest = build()
    plan = {'adoption': 'G3_G4_VERIFIED', 'service_start_type': 3,
        'runtime_bindings': {str(executable): hashlib.sha256(executable.read_bytes()).hexdigest(),
            str(Path(f1_service.__file__).resolve()): hashlib.sha256(Path(f1_service.__file__).read_bytes()).hexdigest()},
        'policy_digest': manifest['policy_digest']}
    path = root / 'adoption.json'; path.write_text(json.dumps(plan))
    state = {'change': None}
    expected = '"' + str(executable) + '" -I -B -m fox2_agent_bridge.f1_service --scm'
    def protected(path, **kwargs):
        if state['change'] == 'acl': raise AuthorityDeny('USER_WRITABLE_AUTHORITY')
    def pid(name=None):
        if state['change'] == 'appidsvc' and name == 'AppIDSvc':
            raise AuthorityDeny('SERVICE_NOT_RUNNING')
        return os.getpid() + (1 if state['change'] == 'service_pid' else 0)
    def system(buffer, size):
        buffer.value = 'C:/Windows/System32'
        return len(buffer.value)
    api = SimpleNamespace(require_system=lambda: None, protected=protected, service_pid=pid,
        service_config=lambda: (('wrong-image' if state['change'] == 'service_config' else expected),
                                 'LocalSystem', 0x10, 3),
        k=SimpleNamespace(GetSystemDirectoryW=system), check=lambda ok: bool(ok))
    monkeypatch.setattr(f1_service.sys, 'executable', str(executable))
    monkeypatch.setattr(f1_service.subprocess, 'run', lambda *a, **k: SimpleNamespace(
        returncode=1 if state['change'] == 'unreadable_policy' else 0,
        stdout='<AppLockerPolicy Version="1" />' if state['change'] == 'policy' else xml.decode()))
    fence = HostFence(api, root, plan, hashlib.sha256(path.read_bytes()).hexdigest())
    return fence, state, root, executable


@pytest.mark.parametrize('change', ['appidsvc', 'service_pid', 'service_config', 'acl',
                                   'policy', 'unreadable_policy', 'runtime', 'extra_runtime', 'plan'])
def test_real_fence_logic_denies_observer_and_protected_binding_drift(host, change):
    fence, state, root, executable = host
    fence(None)  # Source fixture's healthy observer baseline, no creation API.
    if change == 'runtime': executable.write_bytes(b'tampered')
    elif change == 'extra_runtime': (executable.parent / 'injected.dll').write_bytes(b'unbound')
    elif change == 'plan': (root / 'adoption.json').write_text('{}')
    else: state['change'] = change
    with pytest.raises((AuthorityDeny, ValueError)):
        fence(None)
