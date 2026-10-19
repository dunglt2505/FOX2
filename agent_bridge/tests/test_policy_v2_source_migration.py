"""Policy v2.0.0 source-binding migration; no external system, Agent or broker required."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

from fox2_agent_bridge import project_dictionary as binding

ROOT = Path(__file__).resolve().parents[2]
NEW_SOURCE = "b25f7f728de67cf8595bf24f22fcbd79ef50babc"
NEW_DICTIONARY = "docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json"
NEW_POLICY = "docs/governance/FOX2_POLICY_V2.0.0.md"
NEW_ROUTING = "docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md"


def git_bytes(path: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{NEW_SOURCE}:{path}"],
        capture_output=True, check=True
    ).stdout


def test_policy_v2_source_exact_bindings():
    raw = git_bytes(NEW_DICTIONARY)
    dictionary = json.loads(raw)
    assert binding.SOURCE_COMMIT == NEW_SOURCE
    assert binding.SOURCE_PATH == NEW_DICTIONARY
    assert binding.SOURCE_SHA256 == hashlib.sha256(raw).hexdigest()
    assert dictionary["dictionary_version"] == binding.DICTIONARY_VERSION == "1.3"
    assert binding.CURRENT["policy"] == dictionary["current"]["policy"] == {
        "version": "2.0.0", "path": NEW_POLICY
    }
    assert binding.CURRENT["routing_index"] == dictionary["current"]["routing_index"] == {
        "version": "1.4.0", "path": NEW_ROUTING
    }
    for key in ("policy", "routing_index", "git_first_protocol",
                "preexec_evidence_protocol", "preflight_receipt_schema",
                "chat_preflight_intake"):
        expected = hashlib.sha256(git_bytes(binding.CURRENT[key]["path"])).hexdigest()
        assert binding.CURRENT_CONTRACT_SHA256[key] == expected


def test_policy_v2_generator_drift_against_pinned_source():
    generator_path = ROOT / "agent_bridge/scripts/generate_project_dictionary.py"
    spec = importlib.util.spec_from_file_location("project_dictionary_generator_v13", generator_path)
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    assert generator.SOURCE_COMMIT == NEW_SOURCE
    assert generator.SOURCE_PATH == NEW_DICTIONARY
    expected = generator.generate(generator.source_bytes())
    assert expected == (ROOT / "agent_bridge/src/fox2_agent_bridge/project_dictionary.py").read_bytes()
    assert b"\r" not in expected
def test_v2_owner_override_not_synthetic_pass():
    source = git_bytes(NEW_POLICY).decode("utf-8")
    assert "AUTHORIZED_BY_OWNER_OVERRIDE" in source
    assert "PASS_TO_ASSIGN" in source
    assert "`BLOCKED`" in source
    assert "`OWNER_OVERRIDDEN_GATE`" in source
    assert "CODE-FIRST" in source and "CHAT-FIRST" in source
    assert binding.IDENTIFIERS["preflight_statuses"] == ["PASS", "BLOCKED", "INFRA_FAILED"]
