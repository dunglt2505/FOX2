from __future__ import annotations

import hashlib
import json
from pathlib import Path

from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now


def _dispatch_payload(worktree: Path) -> dict[str, object]:
    return {
        "schema_version": "0.6",
        "project": "FOX2",
        "type": "NORMAL_AGENT_DISPATCH",
        "dispatch_id": "FOX2-BRIDGE-E2E-CANARY-001",
        "wp_id": "FOX2-BRIDGE-E2E-CANARY",
        "repository": "dunglt2505/FOX2",
        "control_ref": "refs/heads/work/FOX2-LOCAL-DISPATCH-chat",
        "agent": {
            "product": "COPILOT",
            "interface": "GITHUB_COPILOT_CLI",
        },
        "execution_path": "BRIDGE_DIRECT_COPILOT_CLI",
        "worktree": str(worktree),
        "branch": "work/FOX2-BRIDGE-E2E-CANARY-copilot",
        "base_sha": "a" * 40,
        "prompt": {
            "git_commit": "b" * 40,
            "path": "docs/agent_handoff/BRIDGE/FOX2_BRIDGE_E2E_CANARY_PROMPT.md",
            "git_blob_sha1": "c" * 40,
            "sha256": "d" * 64,
        },
        "allowed_code_paths": [],
        "allowed_report_paths": ["reports/FOX2-BRIDGE-E2E-CANARY/**"],
        "permissions": {
            "code_allowed": True,
            "git_code_push": True,
            "git_report_write": True,
            "git_report_push": True,
            "pr_create": False,
            "merge_allowed": False,
            "production_provider": False,
            "broker_write": False,
            "live": False,
        },
        "max_runs": 1,
    }


def test_dispatch_validation_accepts_minimal_canary(bridge_config, tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(bridge_config, ledger)
    payload = _dispatch_payload(
        bridge_config.worktree_root / "FOX2-BRIDGE-E2E-CANARY-COPILOT"
    )
    raw = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")

    validated = runner._validate_dispatch(
        raw,
        dispatch_path=(
            "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY/dispatch/"
            "FOX2-BRIDGE-E2E-CANARY-001.json"
        ),
        observed_blob_sha="e" * 40,
    )

    assert validated["dispatch_id"] == "FOX2-BRIDGE-E2E-CANARY-001"
    assert validated["_payload_sha256"] == hashlib.sha256(raw).hexdigest()


def test_path_scope_allows_only_declared_tree() -> None:
    patterns = ("reports/FOX2-BRIDGE-E2E-CANARY/**",)
    assert BridgeE2ERunner._path_allowed(
        "reports/FOX2-BRIDGE-E2E-CANARY/bridge_called_copilot.txt",
        patterns,
    )
    assert not BridgeE2ERunner._path_allowed("agent_bridge/src/unexpected.py", patterns)


def test_dispatch_claim_is_single_use(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()

    first = ledger.claim_dispatch(
        dispatch_id="FOX2-BRIDGE-E2E-CANARY-001",
        payload_hash="1" * 64,
        execution_id="execution-1",
        observed_at_utc=now,
    )
    second = ledger.claim_dispatch(
        dispatch_id="FOX2-BRIDGE-E2E-CANARY-001",
        payload_hash="1" * 64,
        execution_id="execution-2",
        observed_at_utc=now,
    )

    assert first is True
    assert second is False
    assert ledger.dispatch_state("FOX2-BRIDGE-E2E-CANARY-001")["state"] == "CLAIMED"
