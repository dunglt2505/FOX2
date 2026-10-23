"""Offline G3 AppLocker baseline candidate safety; NOT host enforcement."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

from fox2_agent_bridge.f1_host_baseline import build_host_baseline_candidate
from fox2_agent_bridge.f1_policy import Artifact, policy_artifact

EMPTY = b'<?xml version="1.0" encoding="utf-8"?><AppLockerPolicy Version="1" />'
SHA = hashlib.sha256(EMPTY).hexdigest()


def proposal():
    return {
        "snapshot_sha256": SHA,
        "allow_paths": {
            "Exe": [r"%WINDIR%\System32\cmd.exe"],
            "Script": [r"%WINDIR%\System32\WindowsPowerShell\v1.0\profile.ps1"],
        },
    }


def build(value=None, local=EMPTY, effective=EMPTY):
    return build_host_baseline_candidate(
        local, effective, value if value is not None else proposal()
    )


def test_candidate_is_deterministic_and_audit_only_not_effective():
    candidate, report = build()
    assert (candidate, report) == build()
    root = ET.fromstring(candidate)
    assert {c.get("Type"): c.get("EnforcementMode") for c in root} == {
        "Exe": "AuditOnly", "Script": "AuditOnly",
        "Msi": "NotConfigured", "Dll": "NotConfigured"
    }
    assert len(root.findall(".//FilePathRule")) == 2
    assert report["candidate_rules"] == {"Exe": 1, "Script": 1}
    assert not report["policy_applied"] and not report["service_changed"]
    assert report["g3_enforcement"] == "NOT_RUN"
    assert report["host_path_acl_and_coverage_review"] == "REQUIRED_G3"
    assert report["internal_ready"] == "NOT_ATTESTED"
    assert b"Set-AppLockerPolicy" not in candidate
    assert "cmd.exe" not in json.dumps(report)


@pytest.mark.parametrize("bad", [
    r"C:\Users\Owner\Downloads\*",
    r"%PROGRAMFILES%\*",
    r"C:\Windows\*",
    r"%WINDIR%\Temp\*",
    r"\\server\share\*",
    r"%WINDIR%\System32\..\cmd.exe",
    "*",
])
def test_untrusted_and_overbroad_paths_are_rejected(bad):
    p = proposal()
    p["allow_paths"]["Exe"] = [bad]
    with pytest.raises(ValueError):
        build(p)


@pytest.mark.parametrize("invalid", [
    {"Exe": [] , "Script": [r"%WINDIR%\System32\cmd.exe"]},
    {"Exe": [r"%WINDIR%\System32\cmd.exe"]},
    {"Exe": [r"%WINDIR%\System32\cmd.exe"], "Script": ["*"]},
])
def test_missing_or_unsafe_coverage_rejected(invalid):
    p = proposal()
    p["allow_paths"] = invalid
    with pytest.raises(ValueError):
        build(p)


def test_no_silent_snapshot_or_proposal_rebinding():
    p = proposal()
    p["snapshot_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="digest mismatch"):
        build(p)
    with pytest.raises(ValueError, match="digest mismatch"):
        build(effective=EMPTY + b" ")
    nonempty = b'<AppLockerPolicy Version="1"><RuleCollection Type="Exe"/></AppLockerPolicy>'
    p["snapshot_sha256"] = hashlib.sha256(nonempty).hexdigest()
    with pytest.raises(ValueError, match="zero rule collections"):
        build(p, local=nonempty, effective=nonempty)
    for bad in (b'<!DOCTYPE AppLockerPolicy><AppLockerPolicy Version="1"/>',
                b'<AppLockerPolicy Version="1"/>'.decode().encode("utf-16")):
        p["snapshot_sha256"] = hashlib.sha256(bad).hexdigest()
        with pytest.raises(ValueError):
            build(p, local=bad, effective=bad)


def test_duplicate_path_and_unreviewed_proposal_keys_denied():
    p = proposal()
    p["allow_paths"]["Exe"].append(p["allow_paths"]["Exe"][0].upper())
    with pytest.raises(ValueError, match="duplicate"):
        build(p)
    p = proposal()
    p["approved"] = True
    with pytest.raises(ValueError, match="explicit proposal"):
        build(p)


def test_candidate_can_be_composed_offline_but_not_attested():
    candidate, _ = build()
    items = (
        Artifact("Exe", "legacy.exe", 5, "1" * 64, "2" * 64, "Deny"),
        Artifact("Exe", "current.exe", 6, "3" * 64, "4" * 64, "Allow"),
        Artifact("Script", "legacy.ps1", 7, "5" * 64, "6" * 64, "Deny"),
        Artifact("Script", "current.ps1", 8, "7" * 64, "8" * 64, "Allow"),
    )
    # The actual Owner snapshot is NOT a reviewed baseline for G2.
    with pytest.raises(ValueError):
        policy_artifact(
            items, source_commit="a" * 40, package_digest="b" * 64,
            baseline_xml=EMPTY
        )
    xml, manifest = policy_artifact(
        items, source_commit="a" * 40, package_digest="b" * 64,
        baseline_xml=candidate
    )
    root = ET.fromstring(xml)
    assert root.find("./RuleCollection[@Type='Exe']").get("EnforcementMode") == "Enabled"
    assert root.find("./RuleCollection[@Type='Script']").get("EnforcementMode") == "Enabled"
    assert manifest["host_enforcement"] == "NOT_RUN_G3"
    assert manifest["baseline_review"] == "REQUIRED_G3_HOST_COMPATIBILITY_AND_PATH_ACL"


def test_cli_only_creates_candidates_and_never_overwrites(tmp_path):
    base = tmp_path / "baseline.xml"
    effective = tmp_path / "effective.xml"
    allow = tmp_path / "allow.json"
    result = tmp_path / "candidate.xml"
    base.write_bytes(EMPTY)
    effective.write_bytes(EMPTY)
    allow.write_text(json.dumps(proposal()), encoding="utf-8")
    command = [
        sys.executable,
        str(__import__("pathlib").Path(__file__).parents[1]
            / "scripts/f1_host_baseline_candidate.py"),
        "--local-snapshot", str(base), "--effective-snapshot", str(effective),
        "--allow-manifest", str(allow), "--output", str(result)
    ]
    first = subprocess.run(command, capture_output=True, text=True, timeout=20)
    assert first.returncode == 0, first.stderr
    assert result.exists() and result.with_suffix(".review.json").exists()
    assert json.loads(first.stdout)["policy_applied"] is False
    second = subprocess.run(command, capture_output=True, text=True, timeout=20)
    assert second.returncode != 0
