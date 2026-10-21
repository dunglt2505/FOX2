"""Deterministic AppLocker *artifacts*, never effective-policy mutation.

Hash values must come from Get-AppLockerFileInformation/New-AppLockerPolicy;
AppLocker PE hashes are not interchangeable with raw package SHA-256 values.
Every executable dependency must be inventoried, including Windows/runtime code.
G3 must validate inventory completeness and copied-artifact enforcement.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
import re
import uuid
import xml.etree.ElementTree as ET

COLLECTIONS = ('Exe', 'Script', 'Msi', 'Dll')
NAMESPACE = uuid.UUID('7d260028-fbdc-41a2-9cdc-7ee89bd9de46')


@dataclass(frozen=True)
class Artifact:
    collection: str
    name: str
    length: int
    applocker_hash: str
    raw_sha256: str
    disposition: str
    principal: str = 'S-1-1-0'

    def validate(self) -> None:
        if (self.collection not in COLLECTIONS or self.disposition not in ('Allow', 'Deny')
                or not re.fullmatch('[A-Za-z0-9._-]{1,160}', self.name)
                or type(self.length) is not int or self.length < 0
                or not re.fullmatch('[0-9a-f]{64}', self.applocker_hash)
                or not re.fullmatch('[0-9a-f]{64}', self.raw_sha256)
                or not re.fullmatch(r'S-1-(?:[0-9]+-)*[0-9]+', self.principal)):
            raise ValueError('invalid AppLocker artifact inventory')
        extensions = {'Exe': ('.exe', '.com'), 'Script': ('.ps1', '.bat', '.cmd', '.vbs', '.js'),
                      'Dll': ('.dll', '.ocx'), 'Msi': ('.msi', '.msp', '.mst')}
        if not self.name.lower().endswith(extensions[self.collection]):
            # Python modules are not an AppLocker Script collection surface.
            # Inventory their interpreter executable; never pretend .py hashes
            # enforce arbitrary Python imports or command-line code.
            raise ValueError('unsupported AppLocker surface; inventory the interpreter')


def policy_artifact(artifacts: tuple[Artifact, ...], *, source_commit: str,
                    package_digest: str) -> tuple[bytes, dict]:
    if (not re.fullmatch('[0-9a-f]{40}', source_commit)
            or not re.fullmatch('[0-9a-f]{64}', package_digest)):
        raise ValueError('exact source/package identity required')
    for item in artifacts:
        item.validate()
    identities = [(a.collection, a.applocker_hash, a.principal) for a in artifacts]
    if len(set(identities)) != len(identities):
        raise ValueError('duplicate/conflicting AppLocker identity')
    if any(not any(a.collection == c and a.disposition == d for a in artifacts)
           for c in ('Exe', 'Script') for d in ('Allow', 'Deny')):
        raise ValueError('current and legacy executable/script inventory required')
    # MSI and DLL are always enforced: this package contains DLLs and Python
    # native dependencies. Missing allows stay denied rather than broad paths.
    root = ET.Element('AppLockerPolicy', Version='1')
    for collection in COLLECTIONS:
        rules = ET.SubElement(root, 'RuleCollection', Type=collection, EnforcementMode='Enabled')
        for item in sorted((a for a in artifacts if a.collection == collection),
                           key=lambda a: (a.disposition, a.applocker_hash, a.principal)):
            material = json.dumps(asdict(item), sort_keys=True, separators=(',', ':'))
            rule = ET.SubElement(rules, 'FileHashRule',
                Id=str(uuid.uuid5(NAMESPACE, source_commit + package_digest + material)),
                Name=item.name, Description='FOX2 F1 exact inventoried identity',
                UserOrGroupSid=item.principal, Action=item.disposition)
            condition = ET.SubElement(ET.SubElement(rule, 'Conditions'), 'FileHashCondition')
            ET.SubElement(condition, 'FileHash', Type='SHA256', Data='0x' + item.applocker_hash.upper(),
                          SourceFileName=item.name, SourceFileLength=str(item.length))
        if collection in ('Exe', 'Dll'):
            extensions = ET.SubElement(rules, 'RuleCollectionExtensions')
            ET.SubElement(ET.SubElement(extensions, 'ThresholdExtensions'), 'Services',
                          EnforcementMode='Enabled')
            ET.SubElement(ET.SubElement(extensions, 'RedstoneExtensions'), 'SystemApps', Allow='Enabled')
    xml = ET.tostring(root, encoding='utf-8', xml_declaration=True) + b'\n'
    manifest = {'format': 'FOX2_F1_POLICY_ARTIFACT_1', 'source_commit': source_commit,
                'package_digest': package_digest, 'policy_digest': policy_digest(xml),
                'xml_sha256': hashlib.sha256(xml).hexdigest(),
                'inventory': sorted((asdict(a) for a in artifacts),
                                    key=lambda a: (a['collection'], a['applocker_hash'], a['principal'])),
                'host_enforcement': 'NOT_RUN_G3'}
    return xml, manifest


def policy_digest(xml: bytes | str) -> str:
    """Strict semantic identity; formatting/order differences alone are ignored."""
    if len(xml) > 8_000_000 or b'<!' in (xml.encode() if isinstance(xml, str) else xml):
        raise ValueError('unsupported policy XML')
    root = ET.fromstring(xml)
    if root.tag != 'AppLockerPolicy' or root.attrib != {'Version': '1'}:
        raise ValueError('unsupported policy root')
    collections = list(root)
    if (len(collections) != 4 or {c.get('Type') for c in collections} != set(COLLECTIONS)
            or any(c.tag != 'RuleCollection' or c.get('EnforcementMode') != 'Enabled'
                   for c in collections)):
        raise ValueError('all required collections must enforce')
    for c in collections:
        if any(r.tag not in ('FileHashRule', 'RuleCollectionExtensions') for r in c):
            raise ValueError('path/publisher or unknown rules outside sealed hash inventory')
        if c.get('Type') in ('Exe', 'Dll') and (
                c.find('./RuleCollectionExtensions/ThresholdExtensions/Services') is None
                or c.find('./RuleCollectionExtensions/ThresholdExtensions/Services').get(
                    'EnforcementMode') != 'Enabled'
                or c.find('./RuleCollectionExtensions/RedstoneExtensions/SystemApps') is None
                or c.find('./RuleCollectionExtensions/RedstoneExtensions/SystemApps').get('Allow') != 'Enabled'):
            raise ValueError('service and system-code enforcement required')

    def canonical(node):
        if (node.text or '').strip() or (node.tail or '').strip():
            raise ValueError('unexpected policy text')
        return [node.tag, sorted(node.attrib.items()),
                sorted((canonical(n) for n in node), key=lambda n: json.dumps(n, sort_keys=True))]
    return hashlib.sha256(json.dumps(canonical(root), separators=(',', ':')).encode()).hexdigest()


def model_decision(manifest: dict, collection: str, applocker_hash: str,
                   principal: str = 'S-1-1-0') -> str:
    """Fixture model ONLY, not Windows evaluation or enforcement certification."""
    matching = [a['disposition'] for a in manifest['inventory']
                if a['collection'] == collection and a['applocker_hash'] == applocker_hash
                and a['principal'] in ('S-1-1-0', principal)]
    return 'Allow' if matching and 'Deny' not in matching else 'Deny'
