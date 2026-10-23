"""Build an AppLocker host baseline CANDIDATE from reviewed path inputs.

Offline only: no default allow rules, host discovery, policy mutation or grant.
A G3 reviewer must verify every candidate path, ACL and complete machine coverage
before this output can be considered a reviewed input to f1_policy.policy_artifact.
"""
from __future__ import annotations

import hashlib
import json
import re
import uuid
import xml.etree.ElementTree as ET

from .f1_policy import _parse_policy, _safe_path

_TYPES = ("Exe", "Script")
_ALL_TYPES = ("Exe", "Script", "Msi", "Dll")
_NAMESPACE = uuid.UUID("10fc888e-5b88-47f8-bd41-069d6c32d0a5")


def _empty_host_snapshot(raw: bytes, expected_sha256: str) -> None:
    if not isinstance(raw, bytes) or not 1 <= len(raw) <= 8_000_000:
        raise ValueError("bounded original host XML snapshot required")
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("original host XML digest mismatch")
    if b"<!" in raw or b"\x00" in raw:
        raise ValueError("unsupported original host XML")
    if b"<?" in re.sub(br"^\s*<\?xml\s[^?]*\?>", b"", raw):
        raise ValueError("unsupported original host XML instruction")
    try:
        root = ET.fromstring(raw.decode("utf-8-sig"))
    except (UnicodeError, ET.ParseError) as exc:
        raise ValueError("invalid original host XML") from exc
    if (root.tag != "AppLockerPolicy" or root.attrib != {"Version": "1"}
            or len(root) or (root.text or "").strip()):
        raise ValueError("original host policy must have zero rule collections")


def build_host_baseline_candidate(
    local_snapshot: bytes, effective_snapshot: bytes, proposal: dict
) -> tuple[bytes, dict]:
    """Produce a candidate, never an approved baseline or a deployable policy.

    Proposal shape: {
      "snapshot_sha256": "<64 lowercase hex>",
      "allow_paths": {
        "Exe": ["%WINDIR%\\System32\\cmd.exe"],
        "Script": ["%WINDIR%\\System32\\WindowsPowerShell\\v1.0\\profile.ps1"]
      }
    }
    Paths are sample syntax only, never default host coverage.
    """
    if not isinstance(proposal, dict) or set(proposal) != {
            "snapshot_sha256", "allow_paths"}:
        raise ValueError("explicit proposal and original snapshot identity required")
    digest = proposal["snapshot_sha256"]
    if not isinstance(digest, str) or not re.fullmatch("[0-9a-f]{64}", digest):
        raise ValueError("invalid original snapshot SHA-256")
    _empty_host_snapshot(local_snapshot, digest)
    _empty_host_snapshot(effective_snapshot, digest)

    allowed = proposal["allow_paths"]
    if not isinstance(allowed, dict) or set(allowed) != set(_TYPES):
        raise ValueError("explicit Exe and Script coverage candidates required")
    for collection in _TYPES:
        entries = allowed[collection]
        if not isinstance(entries, list) or not 1 <= len(entries) <= 64:
            raise ValueError("bounded nonempty Exe/Script path review required")
        if any(not isinstance(path, str) or not 1 <= len(path) <= 260
               for path in entries):
            raise ValueError("invalid candidate allow path")
        if len({path.casefold() for path in entries}) != len(entries):
            raise ValueError("duplicate candidate path")
        for path in entries:
            _safe_path(path)

    root = ET.Element("AppLockerPolicy", Version="1")
    for collection in _ALL_TYPES:
        rules = ET.SubElement(
            root, "RuleCollection", Type=collection,
            EnforcementMode="AuditOnly" if collection in _TYPES else "NotConfigured"
        )
        for path in sorted(allowed.get(collection, []), key=str.casefold):
            identity = uuid.uuid5(_NAMESPACE, digest + "\n" + collection + "\n"
                                  + path.casefold())
            rule = ET.SubElement(
                rules, "FilePathRule", Id=str(identity),
                Name="FOX2 G3 host candidate path",
                Description="Unreviewed host coverage candidate; NOT G3 authorization",
                UserOrGroupSid="S-1-1-0", Action="Allow"
            )
            ET.SubElement(ET.SubElement(rule, "Conditions"),
                          "FilePathCondition", Path=path)
    result = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    _parse_policy(result, final=False)
    summary = {
        "schema": "FOX2_F1_HOST_BASELINE_CANDIDATE_1",
        "snapshot_sha256": digest,
        "candidate_sha256": hashlib.sha256(result).hexdigest(),
        "candidate_rules": {t: len(allowed[t]) for t in _TYPES},
        "exe_script_mode": "AUDIT_ONLY_CANDIDATE",
        "source_snapshot_collections": 0,
        "host_path_acl_and_coverage_review": "REQUIRED_G3",
        "csp_policy_channel": "NOT_VERIFIED",
        "real_installed_f1_package": "NOT_PROVIDED",
        "policy_applied": False,
        "service_changed": False,
        "g3_enforcement": "NOT_RUN",
        "g4_adoption": "NOT_RUN",
        "internal_ready": "NOT_ATTESTED",
    }
    return result, summary
