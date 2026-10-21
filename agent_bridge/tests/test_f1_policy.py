"""Deterministic policy model tests only; host enforcement is NOT_RUN_G3."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET

import pytest

from fox2_agent_bridge.f1_policy import (Artifact, effective_policy_digest, f1_control_digest,
    model_decision, policy_artifact, policy_digest, transition_artifact)


def inventory():
    return tuple(Artifact(collection, name, 123, digit * 64, digit * 64, disposition)
        for collection, name, digit, disposition in (
            ('Exe', 'legacy.exe', '1', 'Deny'), ('Script', 'legacy.ps1', '2', 'Deny'),
            ('Exe', 'current.exe', '3', 'Allow'), ('Script', 'current.ps1', '4', 'Allow'),
            ('Dll', 'runtime.dll', '5', 'Allow'), ('Msi', 'retired.msi', '6', 'Deny')))


def baseline(path=r'%PROGRAMFILES%\ReviewedHost\*', modes=None):
    root = ET.Element('AppLockerPolicy', Version='1')
    for collection in ('Exe', 'Script', 'Msi', 'Dll'):
        c = ET.SubElement(root, 'RuleCollection', Type=collection,
                          EnforcementMode=(modes or {}).get(collection, 'NotConfigured'))
        if collection in ('Exe', 'Script'):
            rule = ET.SubElement(c, 'FilePathRule', Id=str(uuid.uuid5(uuid.NAMESPACE_URL, collection)),
                Name='Reviewed host coverage', Description='Fixture; requires physical G3 ACL review',
                UserOrGroupSid='S-1-1-0', Action='Allow')
            ET.SubElement(ET.SubElement(rule, 'Conditions'), 'FilePathCondition', Path=path)
    return ET.tostring(root)


def build(items=None, **kwargs):
    kwargs.setdefault('baseline_xml', baseline())
    return policy_artifact(items or inventory(), source_commit='a' * 40, package_digest='b' * 64,
                           **kwargs)


def test_deterministic_identity_collections_and_copied_legacy_closure():
    xml, manifest = build()
    assert (xml, manifest) == build(tuple(reversed(inventory())))
    root = ET.fromstring(xml)
    assert {r.get('Type') for r in root} == {'Exe', 'Script', 'Msi', 'Dll'}
    assert {r.get('Type'): r.get('EnforcementMode') for r in root} == {
        'Exe': 'Enabled', 'Script': 'Enabled', 'Msi': 'NotConfigured', 'Dll': 'NotConfigured'}
    assert len(root.findall('.//FilePathRule')) == 2
    for item in inventory():
        # Rename/copy/alternate user-writable root has the same file identity.
        for copied_path in ('C:/Users/u/Desktop/copy', 'C:/AlternateRoot/moved'):
            assert model_decision(manifest, item.collection, item.applocker_hash) == (
                item.disposition if item.collection in ('Exe', 'Script') else 'NotEnforced')
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
    _, changed = policy_artifact(inventory(), source_commit='c' * 40, package_digest='b' * 64,
                                 baseline_xml=baseline())
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


def test_baseline_changes_full_digest_only_and_order_is_immaterial():
    xml, manifest = build()
    changed, other = build(baseline_xml=baseline(r'%PROGRAMFILES%\AnotherReviewedHost\*'))
    assert other['effective_policy_digest'] != manifest['effective_policy_digest']
    assert other['f1_control_digest'] == manifest['f1_control_digest']
    root = ET.fromstring(changed)
    root[:] = reversed(list(root))
    for c in root:
        c[:] = reversed(list(c))
    reordered = ET.tostring(root)
    assert effective_policy_digest(reordered) == other['effective_policy_digest']
    assert f1_control_digest(reordered, other['f1_rule_ids']) == other['f1_control_digest']
    assert manifest['policy_digest'] == effective_policy_digest(xml)


@pytest.mark.parametrize('collection', ['Exe', 'Script'])
@pytest.mark.parametrize('mode', ['AuditOnly', 'NotConfigured'])
def test_mandatory_final_surfaces_cannot_be_disabled(collection, mode):
    xml, manifest = build()
    root = ET.fromstring(xml)
    root.find(f"./RuleCollection[@Type='{collection}']").set('EnforcementMode', mode)
    for digest in (lambda x: effective_policy_digest(x),
                   lambda x: f1_control_digest(x, manifest['f1_rule_ids'])):
        with pytest.raises(ValueError, match='mandatory Exe/Script'):
            digest(ET.tostring(root))


@pytest.mark.parametrize('mode', ['Enabled', 'AuditOnly', 'NotConfigured'])
def test_conditional_surfaces_are_explicit_and_not_inferred_from_dlls(mode):
    modes = {'Msi': mode, 'Dll': mode}
    xml, manifest = build(baseline_xml=baseline(modes=modes), conditional_modes=modes)
    assert manifest['conditional_modes'] == modes
    assert effective_policy_digest(xml) == manifest['effective_policy_digest']
    for c in ET.fromstring(xml):
        assert c.get('EnforcementMode') == ('Enabled' if c.get('Type') in ('Exe', 'Script') else mode)
    if mode != 'NotConfigured':
        with pytest.raises(ValueError, match='explicitly preserve'):
            build(baseline_xml=baseline(modes=modes))
    with pytest.raises(ValueError, match='conditional'):
        build(conditional_modes={'Exe': 'AuditOnly'})


@pytest.mark.parametrize('path', [r'C:\Users\*\*', r'%LOCALAPPDATA%\*', '*', r'C:\*',
    r'%WINDIR%\*', r'%WINDIR%\Temp\*', r'C:\Windows\System32\Tasks\*',
    r'%PROGRAMFILES%\*', r'%PROGRAMFILES%\Vendor\..\*', r'%PROGRAMFILES%\Vendor*\*',
    r'%PROGRAMFILES%\Vendor\file.exe:stream', r'\\server\share\*',
    r'%PROGRAMFILES%\Vendor\temp\*', r'%PROGRAMFILES%\Vendor\.. \*',
    r'%PROGRAMFILES%\Vendor\folder.\*', r'C:\PROGRA~1\Vendor\*'])
def test_user_writable_and_ambiguous_baseline_paths_rejected(path):
    with pytest.raises(ValueError, match='baseline path'):
        build(baseline_xml=baseline(path))


@pytest.mark.parametrize('path', [r'%WINDIR%\System32\cmd.exe',
    r'%WINDIR%\SystemApps\ReviewedApp\*', r'C:\Program Files\ReviewedHost\*'])
def test_bounded_windows_and_program_files_paths(path):
    build(baseline_xml=baseline(path))


def test_reviewed_publisher_and_hash_baseline_preserved_and_conflict_rejected():
    root = ET.fromstring(baseline())
    publisher = ET.SubElement(root[0], 'FilePublisherRule', Id=str(uuid.uuid4()),
        Name='Reviewed signed host app', Description='Reviewed publisher', UserOrGroupSid='S-1-1-0', Action='Allow')
    condition = ET.SubElement(ET.SubElement(publisher, 'Conditions'), 'FilePublisherCondition',
        PublisherName='O=REVIEWED VENDOR, C=US', ProductName='Host app', BinaryName='*')
    ET.SubElement(condition, 'BinaryVersionRange', LowSection='1.0.0.0', HighSection='*')
    xml, manifest = build(baseline_xml=ET.tostring(root))
    assert ET.fromstring(xml).find('.//FilePublisherRule') is not None
    publisher.find('.//FilePublisherCondition').set('PublisherName', '*')
    with pytest.raises(ValueError, match='publisher'):
        build(baseline_xml=ET.tostring(root))
    root = ET.fromstring(baseline())
    # A baseline exact allow for the retired F1 hash cannot be used as recovery.
    generated = ET.fromstring(xml)
    blocked = next(r for r in generated[0] if r.get('Action') == 'Deny')
    blocked.set('Id', str(uuid.uuid4())); blocked.set('Description', 'Baseline hash')
    blocked.set('Action', 'Allow'); root[0].append(blocked)
    with pytest.raises(ValueError, match='conflicts with explicit F1 deny'):
        build(baseline_xml=ET.tostring(root))
    blocked.find('.//FileHash').set('Data', '0x' + '9' * 64)
    composed, _ = build(baseline_xml=ET.tostring(root))
    assert len(ET.fromstring(composed).findall('.//FileHashRule')) == len(inventory()) + 1


@pytest.mark.parametrize('mutation', ['missing', 'id', 'principal', 'action', 'hash', 'name',
    'metadata', 'duplicate', 'extension', 'unknown', 'attribute', 'exception', 'text'])
def test_subset_drift_cannot_be_hidden_in_host_baseline(mutation):
    xml, manifest = build()
    root = ET.fromstring(xml)
    rule = next(r for r in root[0] if r.tag == 'FileHashRule' and r.get('Action') == 'Deny')
    if mutation == 'missing': root[0].remove(rule)
    elif mutation == 'id': rule.set('Id', str(uuid.uuid4()))
    elif mutation == 'principal': rule.set('UserOrGroupSid', 'S-1-5-18')
    elif mutation == 'action': rule.set('Action', 'Allow')
    elif mutation == 'hash': rule.find('.//FileHash').set('Data', '0x' + 'f' * 64)
    elif mutation == 'name': rule.set('Name', 'other.exe')
    elif mutation == 'metadata': rule.set('Description', 'Pretend baseline')
    elif mutation == 'duplicate': root[0].append(ET.fromstring(ET.tostring(rule)))
    elif mutation == 'extension': root[0].find('.//Services').set('EnforcementMode', 'NotConfigured')
    elif mutation == 'unknown': ET.SubElement(root[0], 'UnknownRule')
    elif mutation == 'attribute': rule.set('Bypass', 'true')
    elif mutation == 'exception': ET.SubElement(rule, 'Exceptions')
    elif mutation == 'text': rule.text = 'unexpected'
    try:
        assert f1_control_digest(ET.tostring(root), manifest['f1_rule_ids']) != manifest['f1_control_digest']
    except ValueError:
        pass


def test_no_implicit_isolated_policy_or_unsealed_selector_fallback():
    with pytest.raises(ValueError, match='same-host baseline'):
        policy_artifact(inventory(), source_commit='a' * 40, package_digest='b' * 64)
    xml, manifest = build()
    for ids in ([], ['invalid'], manifest['f1_rule_ids'] * 2):
        with pytest.raises(ValueError):
            f1_control_digest(xml, ids)
    for value in (b'<!DOCTYPE AppLockerPolicy><AppLockerPolicy Version="1"/>', xml.encode('utf-16') if isinstance(xml, str) else xml.decode().encode('utf-16')):
        with pytest.raises(ValueError):
            effective_policy_digest(value)


def test_audit_transition_binds_snapshots_final_controls_and_rollback_without_authority():
    xml, manifest = build()
    inputs = dict(local_snapshot=b'<AppLockerPolicy Version="1" />',
        effective_snapshot=b'<AppLockerPolicy Version="1"><RuleCollection Type="Appx" /></AppLockerPolicy>',
        final_xml=xml, f1_rule_ids=manifest['f1_rule_ids'], rollback_artifact=b'# reviewed rollback fixture')
    audit, contract = transition_artifact(**inputs)
    assert (audit, contract) == transition_artifact(**inputs)
    assert contract['effective_policy_digest'] == manifest['effective_policy_digest']
    assert contract['f1_control_digest'] == manifest['f1_control_digest']
    assert contract['pre_enforcement_local_xml_sha256'] == hashlib.sha256(inputs['local_snapshot']).hexdigest()
    assert contract['rollback_artifact_sha256'] == hashlib.sha256(inputs['rollback_artifact']).hexdigest()
    assert contract['adoption_authority'] is False and contract['host_mutation'] is False
    assert contract['rollback_validation'] == contract['host_compatibility'] == 'NOT_RUN_G3'
    assert all(c.get('EnforcementMode') == ('AuditOnly' if c.get('Type') in ('Exe', 'Script')
                                           else 'NotConfigured') for c in ET.fromstring(audit))
    with pytest.raises(ValueError, match='mandatory Exe/Script'):
        effective_policy_digest(audit)
    with pytest.raises(ValueError):
        transition_artifact(**{**inputs, 'rollback_artifact': b''})


def test_offline_cli_emits_dual_identity_audit_and_transition_artifacts(tmp_path):
    from dataclasses import asdict
    inventory_path = tmp_path / 'inventory.json'
    inventory_path.write_text(json.dumps({'artifacts': [asdict(a) for a in inventory()],
        'source_commit': 'a' * 40, 'package_digest': 'b' * 64}))
    baseline_path = tmp_path / 'baseline.xml'; baseline_path.write_bytes(baseline())
    snapshot = tmp_path / 'snapshot.xml'; snapshot.write_bytes(b'<AppLockerPolicy Version="1" />')
    rollback = tmp_path / 'rollback.ps1'; rollback.write_text('# offline identity fixture only')
    output = tmp_path / 'final.xml'
    script = Path(__file__).parents[1] / 'scripts/f1_policy_artifact.py'
    result = subprocess.run([sys.executable, str(script), '--inventory', str(inventory_path),
        '--baseline', str(baseline_path), '--output', str(output), '--local-snapshot', str(snapshot),
        '--effective-snapshot', str(snapshot), '--rollback-artifact', str(rollback)],
        capture_output=True, text=True, timeout=10)
    assert result.returncode == 0, result.stderr
    manifest = json.loads(output.with_suffix('.json').read_text())
    transition = json.loads(output.with_suffix('.transition.json').read_text())
    assert manifest['effective_policy_digest'] == transition['effective_policy_digest']
    assert manifest['f1_control_digest'] == transition['f1_control_digest']
    assert hashlib.sha256(output.with_suffix('.audit.xml').read_bytes()).hexdigest() == transition['audit_xml_sha256']
    assert transition['rollback_artifact_sha256'] == hashlib.sha256(rollback.read_bytes()).hexdigest()
