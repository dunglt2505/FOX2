from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

from fox2_agent_bridge.ledger import SCHEMA_VERSION, SQLiteLedger, utc_now
from fox2_agent_bridge.models import AuthStatus
from fox2_agent_bridge.runtime_tools import _find_executable, discover_tool
from fox2_agent_bridge.hashing import HashSource, hash_git_blob_bytes, hash_working_tree_bytes


def test_absolute_executable_path_is_resolved() -> None:
    record = discover_tool("python", Path(sys.executable))

    assert record.available
    assert record.executable_path == Path(sys.executable).resolve()


def test_path_fallback_is_used_when_configured_executable_is_missing(
    monkeypatch, tmp_path: Path
) -> None:
    monkeypatch.setattr("fox2_agent_bridge.runtime_tools.shutil.which", lambda name: sys.executable)

    executable, error = _find_executable("python", tmp_path / "missing-python.exe")

    assert executable == Path(sys.executable).resolve()
    assert error is None


def test_missing_executable_is_reported_without_throwing(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr("fox2_agent_bridge.runtime_tools.shutil.which", lambda name: None)

    record = discover_tool("python", tmp_path / "missing-python.exe")

    assert not record.available
    assert record.executable_path is None
    assert "not found" in (record.error or "")


def test_version_invocation_captures_version_output() -> None:
    record = discover_tool("python", Path(sys.executable))

    assert record.version
    assert record.version.startswith("Python ")
    assert record.available
    assert record.version_exit_code == 0
    assert record.version_stdout_available
    assert not record.version_stderr_available


def test_unimplemented_tool_authentication_remains_unverified() -> None:
    record = discover_tool("copilot", Path(sys.executable))

    assert record.auth_status is AuthStatus.UNVERIFIED


def test_git_blob_and_working_tree_hash_inputs_are_distinct() -> None:
    git_hash = hash_git_blob_bytes(b"line\n")
    working_hash = hash_working_tree_bytes(b"line\r\n")

    assert git_hash.source is HashSource.GIT_BLOB_BYTES
    assert working_hash.source is HashSource.WORKING_TREE_BYTES
    assert git_hash.digest != working_hash.digest


def test_sqlite_initializes_and_records_schema_version(tmp_path: Path) -> None:
    database = tmp_path / "data" / "bridge.db"
    ledger = SQLiteLedger(database)

    assert ledger.initialize() == SCHEMA_VERSION
    with ledger.connect() as connection:
        row = connection.execute(
            "SELECT value FROM bridge_meta WHERE key = 'schema_version'"
        ).fetchone()
    assert row["value"] == str(SCHEMA_VERSION)
    assert set(ledger.table_names()) == {
        "bridge_meta",
        "dispatches",
        "executions",
        "review_events",
        "control_cursors",
        "poll_observations",
        "candidate_discoveries",
    }


def test_dispatch_id_uniqueness_is_enforced(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()
    with ledger.connect() as connection:
        connection.execute(
            "INSERT INTO dispatches (dispatch_id, state, created_at_utc, updated_at_utc) "
            "VALUES (?, ?, ?, ?)",
            ("dispatch-1", "RECEIVED", now, now),
        )
        try:
            connection.execute(
                "INSERT INTO dispatches (dispatch_id, state, created_at_utc, updated_at_utc) "
                "VALUES (?, ?, ?, ?)",
                ("dispatch-1", "RECEIVED", now, now),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("duplicate dispatch_id was accepted")


def test_review_key_uniqueness_is_enforced(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()
    with ledger.connect() as connection:
        connection.execute(
            "INSERT INTO dispatches (dispatch_id, state, created_at_utc, updated_at_utc) "
            "VALUES (?, ?, ?, ?)",
            ("dispatch-1", "RECEIVED", now, now),
        )
        connection.execute(
            "INSERT INTO review_events (event_id, review_key, dispatch_id, state, created_at_utc) "
            "VALUES (?, ?, ?, ?, ?)",
            ("event-1", "review-1", "dispatch-1", "PENDING", now),
        )
        try:
            connection.execute(
                "INSERT INTO review_events "
                "(event_id, review_key, dispatch_id, state, created_at_utc) "
                "VALUES (?, ?, ?, ?, ?)",
                ("event-2", "review-1", "dispatch-1", "PENDING", now),
            )
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("duplicate review_key was accepted")


def test_finish_execution_persists_result_and_status(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()
    assert ledger.claim_dispatch(
        dispatch_id="dispatch-result",
        payload_hash="a" * 64,
        execution_id="execution-result",
        observed_at_utc=now,
    )

    ledger.finish_execution(
        dispatch_id="dispatch-result",
        execution_id="execution-result",
        dispatch_state="PUSHED_UNREVIEWED",
        execution_state="PUSHED_UNREVIEWED",
        finished_at_utc=utc_now(),
        result={"after_head": "b" * 40, "changed_paths": ["reports/x.txt"]},
    )

    status = ledger.dispatch_status("dispatch-result")
    assert status is not None
    assert status["dispatch_state"] == "PUSHED_UNREVIEWED"
    assert status["execution_state"] == "PUSHED_UNREVIEWED"
    assert status["result"]["after_head"] == "b" * 40


def test_recover_interrupted_executions_terminalizes_running_rows(tmp_path: Path) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    now = utc_now()
    assert ledger.claim_dispatch(
        dispatch_id="dispatch-stale",
        payload_hash="c" * 64,
        execution_id="execution-stale",
        observed_at_utc=now,
    )

    recovered = ledger.recover_interrupted_executions(finished_at_utc=utc_now())

    assert recovered == 1
    status = ledger.dispatch_status("dispatch-stale")
    assert status is not None
    assert status["dispatch_state"] == "INTERRUPTED"
    assert status["execution_state"] == "INTERRUPTED"
    assert status["error_code"] == "STALE_EXECUTION"
