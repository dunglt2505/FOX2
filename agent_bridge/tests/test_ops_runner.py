from __future__ import annotations

import json
from pathlib import Path

from fox2_agent_bridge.ops_runner import BridgeOps
from fox2_agent_bridge.result_store import write_execution_report


def test_auto_execute_identity_requires_explicit_opt_in() -> None:
    enabled = json.dumps(
        {
            "dispatch_id": "FOX2-OPS-001",
            "agent": {"product": "CODEX"},
            "runtime_contract": {"auto_execute": True},
        }
    ).encode("utf-8")
    disabled = json.dumps(
        {
            "dispatch_id": "FOX2-OPS-002",
            "agent": {"product": "CODEX"},
            "runtime_contract": {"auto_execute": False},
        }
    ).encode("utf-8")

    assert BridgeOps._auto_execute_identity(enabled) == (True, "FOX2-OPS-001")
    copilot = json.dumps(
        {
            "dispatch_id": "FOX2-OPS-COPILOT",
            "agent": {"product": "COPILOT"},
            "runtime_contract": {"auto_execute": True},
        }
    ).encode("utf-8")

    assert BridgeOps._auto_execute_identity(disabled) == (False, None)
    assert BridgeOps._auto_execute_identity(copilot) == (False, None)
    assert BridgeOps._auto_execute_identity(b"not-json") == (False, None)


def test_runtime_report_is_atomically_written(tmp_path: Path) -> None:
    path = write_execution_report(
        bridge_root=tmp_path,
        dispatch_id="FOX2-OPS-REPORT-001",
        payload={"status": "PUSHED_UNREVIEWED", "after_head": "a" * 40},
    )

    assert path == tmp_path / "data" / "results" / "FOX2-OPS-REPORT-001.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["status"] == "PUSHED_UNREVIEWED"
    assert payload["after_head"] == "a" * 40
    assert not (path.parent / ".FOX2-OPS-REPORT-001.json.tmp").exists()
