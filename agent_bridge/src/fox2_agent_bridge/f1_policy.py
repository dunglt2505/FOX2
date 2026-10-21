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
MODES = ('Enabled', 'AuditOnly', 'NotConfigured')
F1_DESCRIPTION = 'FOX2 F1 exact inventoried identity'


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
                    package_digest: str, baseline_xml: bytes | str | None = None,
                    conditional_modes: dict[str, str] | None = None) -> tuple[bytes, dict]:
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
    modes = {'Msi': 'NotConfigured', 'Dll': 'NotConfigured'}
    if conditional_modes is not None:
        if (set(conditional_modes) - set(modes)
                or any(m not in MODES for m in conditional_modes.values())):
            raise ValueError('explicit conditional Msi/Dll modes required')
        modes.update(conditional_modes)
    if baseline_xml is None:
        raise ValueError('reviewed same-host baseline required')
    baseline = _parse_policy(baseline_xml, final=False)
    if any(not any(r.tag != 'RuleCollectionExtensions' and r.get('Action') == 'Allow' for r in c)
           for c in baseline if c.get('Type') in ('Exe', 'Script')):
        raise ValueError('reviewed host coverage required for Exe/Script')
    # A reviewed baseline is input, never inferred from event logs or package DLLs.
    root = ET.Element('AppLockerPolicy', Version='1')
    f1_ids = []
    for collection in COLLECTIONS:
        mode = 'Enabled' if collection in ('Exe', 'Script') else modes[collection]
        rules = ET.SubElement(root, 'RuleCollection', Type=collection, EnforcementMode=mode)
        previous = next(c for c in baseline if c.get('Type') == collection)
        # Never silently disable a pre-existing host enforcement surface.
        if collection in modes and previous.get('EnforcementMode') != mode:
            raise ValueError('conditional mode must explicitly preserve reviewed baseline')
        for rule in previous:
            if rule.tag != 'RuleCollectionExtensions':
                if rule.get('Description', '').startswith('FOX2 F1'):
                    raise ValueError('baseline cannot supply F1 controls')
                rules.append(rule)
        for item in sorted((a for a in artifacts if a.collection == collection),
                           key=lambda a: (a.disposition, a.applocker_hash, a.principal)):
            material = json.dumps(asdict(item), sort_keys=True, separators=(',', ':'))
            rule = ET.SubElement(rules, 'FileHashRule',
                Id=str(uuid.uuid5(NAMESPACE, source_commit + package_digest + material)),
                Name=item.name, Description=F1_DESCRIPTION,
                UserOrGroupSid=item.principal, Action=item.disposition)
            f1_ids.append(rule.get('Id'))
            condition = ET.SubElement(ET.SubElement(rule, 'Conditions'), 'FileHashCondition')
            ET.SubElement(condition, 'FileHash', Type='SHA256', Data='0x' + item.applocker_hash.upper(),
                          SourceFileName=item.name, SourceFileLength=str(item.length))
        if collection in ('Exe', 'Dll'):
            extensions = ET.SubElement(rules, 'RuleCollectionExtensions')
            ET.SubElement(ET.SubElement(extensions, 'ThresholdExtensions'), 'Services',
                          EnforcementMode='Enabled')
            ET.SubElement(ET.SubElement(extensions, 'RedstoneExtensions'), 'SystemApps', Allow='Enabled')
    xml = ET.tostring(root, encoding='utf-8', xml_declaration=True) + b'\n'
    effective = effective_policy_digest(xml)
    control = f1_control_digest(xml, f1_ids)
    manifest = {'format': 'FOX2_F1_POLICY_ARTIFACT_2', 'source_commit': source_commit,
                'package_digest': package_digest, 'policy_digest': effective,
                'effective_policy_digest': effective, 'f1_control_digest': control,
                'f1_rule_ids': sorted(f1_ids), 'conditional_modes': modes,
                'baseline_xml_sha256': (hashlib.sha256(baseline_xml.encode() if isinstance(
                    baseline_xml, str) else baseline_xml).hexdigest() if baseline_xml is not None else None),
                'baseline_review': 'REQUIRED_G3_HOST_COMPATIBILITY_AND_PATH_ACL',
                'xml_sha256': hashlib.sha256(xml).hexdigest(),
                'inventory': sorted((asdict(a) for a in artifacts),
                                    key=lambda a: (a['collection'], a['applocker_hash'], a['principal'])),
                'host_enforcement': 'NOT_RUN_G3'}
    return xml, manifest


def policy_digest(xml: bytes | str) -> str:
    """Compatibility alias for the complete policy; never sufficient for HostFence."""
    return effective_policy_digest(xml)


def _canonical(node):
    if (node.text or '').strip() or (node.tail or '').strip():
        raise ValueError('unexpected policy text')
    return [node.tag, sorted(node.attrib.items()),
            sorted((_canonical(n) for n in node), key=lambda n: json.dumps(n, sort_keys=True))]


def _digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def _shape(node, tag, attributes, children=()):
    if (node.tag != tag or set(node.attrib) != set(attributes)
            or sorted(n.tag for n in node) != sorted(children)):
        raise ValueError('unsupported policy XML shape: ' + str(node.tag))


def _safe_path(value: str) -> None:
    # Deliberately narrow grammar: no aliases, UNC, ADS, traversal, short names,
    # wildcards in directory names, or arbitrary environment variables. Actual
    # ownership/DACLs of every relied-upon tree remain a mandatory G3 check.
    path = value.lower()
    anchors = ('%windir%\\system32\\', '%windir%\\syswow64\\', '%windir%\\systemapps\\',
               '%programfiles%\\', '%programfiles(x86)%\\',
               'c:\\windows\\system32\\', 'c:\\windows\\syswow64\\',
               'c:\\windows\\systemapps\\', 'c:\\program files\\', 'c:\\program files (x86)\\')
    anchor = next((a for a in anchors if path.startswith(a)), None)
    if anchor is None:
        raise ValueError('user-writable or unrestricted baseline path')
    relative = path[len(anchor):]
    parts = relative.split('\\')
    if (not relative or any(not re.fullmatch(r'[a-z0-9_ .()\-]+|\*', p) for p in parts)
            or any(p in ('.', '..') or p.endswith(('.', ' ')) for p in parts)
            or any('*' in p for p in parts[:-1])
            or (parts[-1] == '*' and len(parts) < 2)
            or any(p in ('temp', 'tasks', 'spool', 'drivers', 'logfiles', 'tracing') for p in parts)):
        raise ValueError('user-writable or unrestricted baseline path')


def _validate_rule(rule):
    attributes = ('Id', 'Name', 'Description', 'UserOrGroupSid', 'Action')
    _shape(rule, rule.tag, attributes, ('Conditions',))
    if (rule.tag not in ('FileHashRule', 'FilePathRule', 'FilePublisherRule')
            or rule.get('Action') not in ('Allow', 'Deny')
            or not re.fullmatch(r'S-1-(?:[0-9]+-)*[0-9]+', rule.get('UserOrGroupSid', ''))
            or not 1 <= len(rule.get('Name', '')) <= 256
            or len(rule.get('Description', '')) > 1024):
        raise ValueError('unsupported policy rule')
    rule.set('Id', str(uuid.UUID(rule.get('Id'))))
    conditions = rule[0]
    tag = {'FileHashRule': 'FileHashCondition', 'FilePathRule': 'FilePathCondition',
           'FilePublisherRule': 'FilePublisherCondition'}[rule.tag]
    _shape(conditions, 'Conditions', (), (tag,))
    condition = conditions[0]
    if rule.tag == 'FileHashRule':
        _shape(condition, tag, (), ('FileHash',))
        h = condition[0]
        _shape(h, 'FileHash', ('Type', 'Data', 'SourceFileName', 'SourceFileLength'))
        if (h.get('Type') != 'SHA256' or not re.fullmatch(r'0x[0-9a-fA-F]{64}', h.get('Data', ''))
                or not re.fullmatch(r'[0-9]{1,20}', h.get('SourceFileLength', ''))
                or not h.get('SourceFileName')):
            raise ValueError('invalid exact hash condition')
        h.set('Data', h.get('Data').upper().replace('0X', '0x'))
        h.set('SourceFileLength', str(int(h.get('SourceFileLength'))))
    elif rule.tag == 'FilePathRule':
        _shape(condition, tag, ('Path',))
        _safe_path(condition.get('Path', ''))
    else:
        _shape(condition, tag, ('PublisherName', 'ProductName', 'BinaryName'), ('BinaryVersionRange',))
        if (not condition.get('PublisherName') or any(c in condition.get('PublisherName') for c in '*?')
                or any(not condition.get(a) for a in ('ProductName', 'BinaryName'))):
            raise ValueError('reviewed exact publisher identity required')
        version = condition[0]
        _shape(version, 'BinaryVersionRange', ('LowSection', 'HighSection'))
        for v in version.attrib.values():
            if v != '*' and not re.fullmatch(r'[0-9]{1,5}(?:\.[0-9]{1,5}){3}', v):
                raise ValueError('unsupported publisher version')


def _validate_extensions(node):
    _shape(node, 'RuleCollectionExtensions', (), ('ThresholdExtensions', 'RedstoneExtensions'))
    threshold = node.find('ThresholdExtensions')
    redstone = node.find('RedstoneExtensions')
    _shape(threshold, 'ThresholdExtensions', (), ('Services',))
    _shape(threshold[0], 'Services', ('EnforcementMode',))
    _shape(redstone, 'RedstoneExtensions', (), ('SystemApps',))
    _shape(redstone[0], 'SystemApps', ('Allow',))
    if threshold[0].get('EnforcementMode') != 'Enabled' or redstone[0].get('Allow') != 'Enabled':
        raise ValueError('service and system-code enforcement required')


def _parse_policy(xml: bytes | str, *, final: bool = True):
    raw = xml.encode('utf-8') if isinstance(xml, str) else xml
    # Reject non-UTF8 encodings too: DTD/entity scans must not be bypassed by UTF16.
    if len(raw) > 8_000_000 or b'<!' in raw or b'\x00' in raw:
        raise ValueError('unsupported policy XML')
    if b'<?' in re.sub(br'^\s*<\?xml\s[^?]*\?>', b'', raw):
        raise ValueError('unsupported policy processing instruction')
    try:
        root = ET.fromstring(raw.decode('utf-8-sig'))
    except (ET.ParseError, UnicodeError) as exc:
        raise ValueError('unsupported policy XML') from exc
    if root.tag != 'AppLockerPolicy' or root.attrib != {'Version': '1'}:
        raise ValueError('unsupported policy root')
    collections = list(root)
    if (len(collections) != 4 or {c.get('Type') for c in collections} != set(COLLECTIONS)
            or any(c.tag != 'RuleCollection' or set(c.attrib) != {'Type', 'EnforcementMode'}
                   or c.get('EnforcementMode') not in MODES for c in collections)):
        raise ValueError('explicit supported collection modes required')
    ids = set()
    for c in collections:
        if final and c.get('Type') in ('Exe', 'Script') and c.get('EnforcementMode') != 'Enabled':
            raise ValueError('mandatory Exe/Script must enforce')
        extensions = c.findall('RuleCollectionExtensions')
        if len(extensions) > 1 or (extensions and c.get('Type') not in ('Exe', 'Dll')):
            raise ValueError('unsupported collection extensions')
        for r in c:
            if r.tag == 'RuleCollectionExtensions':
                _validate_extensions(r)
            else:
                _validate_rule(r)
                if r.get('Id') in ids:
                    raise ValueError('duplicate policy rule identity')
                ids.add(r.get('Id'))
        if (final and c.get('Type') in ('Exe', 'Dll')
                and c.get('EnforcementMode') == 'Enabled' and not extensions):
            raise ValueError('service and system-code enforcement required')
    _canonical(root)  # Reject text at every depth before using any subset.
    return root


def effective_policy_digest(xml: bytes | str) -> str:
    """Complete reviewed policy identity; formatting/rule order are immaterial."""
    return _digest(_canonical(_parse_policy(xml)))


def f1_control_digest(xml: bytes | str, expected_rule_ids: list[str] | tuple[str, ...]) -> str:
    """Bind a sealed expected selector, never discover controls by display name alone.

    IDs are deterministic at generation from source/package/exact inventory.
    The digest includes actual principals/actions/hashes, modes and extensions.
    Missing/duplicate/extra reserved controls are rejected, not silently omitted.
    """
    if (not isinstance(expected_rule_ids, (tuple, list)) or not expected_rule_ids
            or any(not isinstance(i, str) or str(uuid.UUID(i)) != i for i in expected_rule_ids)
            or len(set(expected_rule_ids)) != len(expected_rule_ids)):
        raise ValueError('sealed F1 rule selector required')
    root = _parse_policy(xml)
    selected, seen = [], set()
    for collection in root:
        controls = ET.Element('RuleCollection', **collection.attrib)
        f1_rules = []
        for rule in collection:
            identity = rule.get('Id')
            if identity in expected_rule_ids:
                if rule.tag != 'FileHashRule' or rule.get('Description') != F1_DESCRIPTION:
                    raise ValueError('F1 controls must be exact inventoried hashes')
                f1_rules.append(rule)
                controls.append(rule)
                seen.add(identity)
            elif rule.get('Description', '').startswith('FOX2 F1'):
                raise ValueError('unexpected F1 control identity')
            elif rule.tag == 'RuleCollectionExtensions':
                controls.append(rule)
        if collection.get('Type') in ('Exe', 'Script') and any(
                not any(r.get('Action') == a for r in f1_rules) for a in ('Allow', 'Deny')):
            raise ValueError('mandatory current and legacy F1 controls required')
        # Exact baseline allows must not contradict an explicit F1 hash deny.
        denies = [r for r in f1_rules if r.get('Action') == 'Deny']
        for rule in collection:
            if (rule.tag == 'FileHashRule' and rule.get('Action') == 'Allow'
                    and rule.get('Id') not in expected_rule_ids):
                for blocked in denies:
                    if (rule.find('.//FileHash').get('Data') == blocked.find('.//FileHash').get('Data')
                            and ('S-1-1-0' in (rule.get('UserOrGroupSid'), blocked.get('UserOrGroupSid'))
                                 or rule.get('UserOrGroupSid') == blocked.get('UserOrGroupSid'))):
                        raise ValueError('baseline conflicts with explicit F1 deny')
        selected.append(_canonical(controls))
    if seen != set(expected_rule_ids):
        raise ValueError('missing F1 control identity')
    return _digest(sorted(selected, key=lambda c: json.dumps(c, sort_keys=True)))


def transition_artifact(*, local_snapshot: bytes, effective_snapshot: bytes,
                        final_xml: bytes, f1_rule_ids: list[str], rollback_artifact: bytes) -> tuple[bytes, dict]:
    """Offline audit XML and evidence contract; no readiness/adoption authority.

    Snapshot bytes are retained exactly for rollback, including unsupported prior
    host-policy types. Physical G3 must separately verify compatibility, service
    state, snapshot files and rollback tooling before any Enforce transition.
    """
    for value in (local_snapshot, effective_snapshot, rollback_artifact):
        if not isinstance(value, bytes) or not value or len(value) > 8_000_000:
            raise ValueError('bounded pre-enforcement and rollback artifacts required')
    for snapshot in (local_snapshot, effective_snapshot):
        # Preserve prior host semantics without restricting snapshots to the new
        # supported rule set (e.g. an existing Appx collection must roll back).
        if b'<!' in snapshot or b'\x00' in snapshot:
            raise ValueError('unsupported snapshot XML')
        try:
            prior = ET.fromstring(snapshot.decode('utf-8-sig'))
        except (ET.ParseError, UnicodeError) as exc:
            raise ValueError('invalid snapshot XML') from exc
        if prior.tag != 'AppLockerPolicy' or prior.attrib != {'Version': '1'}:
            raise ValueError('invalid snapshot policy root')
    root = _parse_policy(final_xml)
    final_digest = effective_policy_digest(final_xml)
    control_digest = f1_control_digest(final_xml, f1_rule_ids)
    for collection in root:
        if collection.get('EnforcementMode') == 'Enabled':
            collection.set('EnforcementMode', 'AuditOnly')
    audit_xml = ET.tostring(root, encoding='utf-8', xml_declaration=True) + b'\n'
    return audit_xml, {
        'format': 'FOX2_F1_AUDIT_TO_ENFORCE_1',
        'pre_enforcement_local_xml_sha256': hashlib.sha256(local_snapshot).hexdigest(),
        'pre_enforcement_effective_xml_sha256': hashlib.sha256(effective_snapshot).hexdigest(),
        'audit_xml_sha256': hashlib.sha256(audit_xml).hexdigest(),
        'audit_policy_digest': _digest(_canonical(_parse_policy(audit_xml, final=False))),
        'effective_policy_digest': final_digest, 'f1_control_digest': control_digest,
        'rollback_artifact_sha256': hashlib.sha256(rollback_artifact).hexdigest(),
        'host_compatibility': 'NOT_RUN_G3', 'rollback_validation': 'NOT_RUN_G3',
        'service_and_protected_root_snapshot': 'REQUIRED_G3',
        'host_mutation': False, 'adoption_authority': False}


def model_decision(manifest: dict, collection: str, applocker_hash: str,
                   principal: str = 'S-1-1-0') -> str:
    """F1 exact-identity fixture ONLY, never evaluate the host baseline here."""
    if manifest.get('conditional_modes', {}).get(collection, 'Enabled') != 'Enabled':
        return 'NotEnforced'
    matching = [a['disposition'] for a in manifest['inventory']
                if a['collection'] == collection and a['applocker_hash'] == applocker_hash
                and a['principal'] in ('S-1-1-0', principal)]
    return 'Allow' if matching and 'Deny' not in matching else 'Deny'
