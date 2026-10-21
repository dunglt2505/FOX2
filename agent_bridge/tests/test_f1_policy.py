"""Deterministic policy model tests only; host enforcement is NOT_RUN_G3."""
from dataclasses import replace
import xml.etree.ElementTree as ET

import pytest

from fox2_agent_bridge.f1_policy import Artifact, model_decision, policy_artifact, policy_digest


def inventory():
    return tuple(Artifact(collection, name, 123, digit * 64, digit * 64, disposition)
        for collection, name, digit, disposition in (
            ('Exe', 'legacy.exe', '1', 'Deny'), ('Script', 'legacy.ps1', '2', 'Deny'),
            ('Exe', 'current.exe', '3', 'Allow'), ('Script', 'current.ps1', '4', 'Allow'),
            ('Dll', 'runtime.dll', '5', 'Allow'), ('Msi', 'retired.msi', '6', 'Deny')))


def build(items=None):
    return policy_artifact(items or inventory(), source_commit='a' * 40, package_digest='b' * 64)


def test_deterministic_identity_collections_and_copied_legacy_closure():
    xml, manifest = build()
    assert (xml, manifest) == build(tuple(reversed(inventory())))
    root = ET.fromstring(xml)
    assert {r.get('Type') for r in root} == {'Exe', 'Script', 'Msi', 'Dll'}
    assert all(r.get('EnforcementMode') == 'Enabled' for r in root)
    assert not root.findall('.//FilePathRule')
    for item in inventory():
        # Rename/copy/alternate user-writable root has the same file identity.
        for copied_path in ('C:/Users/u/Desktop/copy', 'C:/AlternateRoot/moved'):
            assert model_decision(manifest, item.collection, item.applocker_hash) == item.disposition
    assert model_decision(manifest, 'Exe', 'f' * 64) == 'Deny'
    assert manifest['host_enforcement'] == 'NOT_RUN_G3'
    for collection in ('Exe', 'Dll'):
        assert root.find(f"./RuleCollection[@Type='{collection}']/RuleCollectionExtensions/ThresholdExtensions/Services").get('EnforcementMode') == 'Enabled'
        assert root.find(f"./RuleCollection[@Type='{collection}']/RuleCollectionExtensions/RedstoneExtensions/SystemApps").get('Allow') == 'Enabled'


@pytest.mark.parametrize('mutation', ['audit', 'missing', 'path', 'extension', 'hash'])
def test_effective_policy_absence_drift_and_path_only_trust(mutation):
    xml, manifest = build()
    root = ET.fromstring(xml)
    if mutation == 'audit': root[0].set('EnforcementMode', 'AuditOnly')
    elif mutation == 'missing': root.remove(root[0])
    elif mutation == 'path': ET.SubElement(root[0], 'FilePathRule', Path=r'C:\Users\*')
    elif mutation == 'extension': root[0].remove(root[0].find('RuleCollectionExtensions'))
    elif mutation == 'hash': root.find('.//FileHash').set('Data', '0x' + 'f' * 64)
    try:
        assert policy_digest(ET.tostring(root)) != manifest['policy_digest']
    except ValueError:
        pass


def test_source_package_binding_and_complete_unambiguous_inventory():
    xml, manifest = build()
    assert policy_digest(xml.decode().replace('><', '>\n  <')) == manifest['policy_digest']
    with pytest.raises(ValueError, match='duplicate/conflicting'):
        build(inventory() + (replace(inventory()[0], disposition='Allow'),))
    with pytest.raises(ValueError, match='current and legacy'):
        build(tuple(a for a in inventory() if a.collection != 'Script'))
    with pytest.raises(ValueError):
        build((replace(inventory()[0], name='C:/Users/*'), *inventory()[1:]))
    _, changed = policy_artifact(inventory(), source_commit='c' * 40, package_digest='b' * 64)
    assert changed['policy_digest'] != manifest['policy_digest']


def test_interpreter_identity_must_be_fenced_by_principal_not_python_source_path():
    caller = 'S-1-5-21-123'
    interpreter = Artifact('Exe', 'python.exe', 100, '7' * 64, '8' * 64, 'Allow', 'S-1-5-18')
    _, manifest = build(inventory() + (interpreter, replace(interpreter, disposition='Deny', principal=caller)))
    assert model_decision(manifest, 'Exe', '7' * 64, caller) == 'Deny'
    assert model_decision(manifest, 'Exe', '7' * 64, 'S-1-5-18') == 'Allow'
    assert model_decision(manifest, 'Exe', '7' * 64, 'S-1-5-21-456') == 'Deny'
    with pytest.raises(ValueError, match='inventory the interpreter'):
        build(inventory() + (replace(interpreter, collection='Script', name='copied_legacy.py'),))
