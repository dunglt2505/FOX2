"""Trusted-observer integration with fake OS responses, not host enforcement."""
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import xml.etree.ElementTree as ET

import pytest

from fox2_agent_bridge import f1_service
from fox2_agent_bridge.f1_protocol import AuthorityDeny
from fox2_agent_bridge.f1_service import HostFence
from fox2_agent_bridge.f1_policy import effective_policy_digest
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
        'effective_policy_digest': manifest['effective_policy_digest'],
        'f1_control_digest': manifest['f1_control_digest'], 'f1_rule_ids': manifest['f1_rule_ids']}
    path = root / 'adoption.json'; path.write_text(json.dumps(plan))
    state = {'change': None, 'xml': xml.decode()}
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
        stdout='<AppLockerPolicy Version="1" />' if state['change'] == 'policy' else state['xml']))
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


@pytest.mark.parametrize('identity', ['effective_policy_digest', 'f1_control_digest', 'f1_rule_ids'])
def test_host_fence_requires_each_sealed_dual_identity(host, identity):
    fence, state, root, executable = host
    fence(None)
    del fence.plan[identity]
    # Reseal fixture plan to test contract validation beyond raw plan sealing.
    path = root / 'adoption.json'; path.write_text(json.dumps(fence.plan))
    fence.plan_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(AuthorityDeny, match='POLICY_CONTRACT'):
        fence(None)


def test_full_digest_match_cannot_mask_f1_subset_drift(host):
    fence, state, root, executable = host
    fence(None)
    policy = ET.fromstring(state['xml'])
    policy.find('.//FileHash').set('Data', '0x' + 'f' * 64)
    state['xml'] = ET.tostring(policy).decode()
    fence.plan['effective_policy_digest'] = effective_policy_digest(state['xml'])
    path = root / 'adoption.json'; path.write_text(json.dumps(fence.plan))
    fence.plan_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(AuthorityDeny, match='F1_CONTROL_BINDING'):
        fence(None)


def test_host_baseline_drift_denies_even_with_unchanged_f1_controls(host):
    fence, state, root, executable = host
    policy = ET.fromstring(state['xml'])
    policy.find('.//FilePathCondition').set('Path', r'%PROGRAMFILES%\OtherReviewedHost\*')
    state['xml'] = ET.tostring(policy).decode()
    with pytest.raises(AuthorityDeny, match='EFFECTIVE_POLICY_BINDING'):
        fence(None)
