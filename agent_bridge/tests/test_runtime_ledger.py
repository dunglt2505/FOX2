from __future__ import annotations

import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from fox2_agent_bridge.ledger import MIGRATIONS, SCHEMA_VERSION, SQLiteLedger, utc_now
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
        "worker_state",
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


def test_recover_interrupted_executions_retains_uncertainty(tmp_path: Path) -> None:
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
    assert status["dispatch_state"] == "NEEDS_RECONCILIATION"
    assert status["execution_state"] == "NEEDS_RECONCILIATION"
    assert status["error_code"] == "NEEDS_RECONCILIATION"


def test_cross_root_unknown_claim_denied_after_reopen_and_resume(tmp_path: Path) -> None:
    """Cross-root UNKNOWN is durable, never cleared by ordinary init/control."""
    database = tmp_path / "bridge.db"
    first = SQLiteLedger(database)
    assert first.initialize(cross_root_authority_unknown=True) == SCHEMA_VERSION

    with first.connect() as connection:
        value = connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"]
    assert value == "DENY_CROSS_ROOT_UNKNOWN"

    first.control("pause")
    first.control("resume")
    reopened = SQLiteLedger(database)
    assert reopened.initialize() == SCHEMA_VERSION
    for honor_controls in (False, True):
        assert not reopened.claim_dispatch(
            dispatch_id=f"denied-{honor_controls}",
            payload_hash="a" * 64,
            execution_id=f"blocked-{honor_controls}",
            observed_at_utc=utc_now(),
            honor_controls=honor_controls,
        )
    with reopened.connect() as connection:
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "DENY_CROSS_ROOT_UNKNOWN"
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


def test_missing_invalid_and_unknown_authority_never_creates_a_claim(tmp_path: Path) -> None:
    """No missing/corrupt authority token can silently authorize a direct call."""
    for variant in ("missing", "corrupt", "unknown"):
        ledger = SQLiteLedger(tmp_path / variant / "bridge.db")
        ledger.initialize()
        with ledger.connect() as connection:
            if variant == "missing":
                connection.execute(
                    "DELETE FROM bridge_meta WHERE key='claim_authority'"
                )
            else:
                value = "INVALID" if variant == "corrupt" else "DENY_CROSS_ROOT_UNKNOWN"
                connection.execute(
                    "UPDATE bridge_meta SET value=? WHERE key='claim_authority'",
                    (value,),
                )
        assert not ledger.claim_dispatch(
            dispatch_id=f"not-admitted-{variant}",
            payload_hash="a" * 64,
            execution_id=f"no-execution-{variant}",
            observed_at_utc=utc_now(),
        )
        with ledger.connect() as connection:
            assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
            assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


def test_schema_v4_upgrade_preserves_existing_unknown_authority(tmp_path: Path) -> None:
    """The new schema cannot replace an existing DENY with SINGLE_ROOT."""
    ledger = SQLiteLedger(tmp_path / "v4.db")
    with ledger.connect() as connection:
        connection.execute(
            "CREATE TABLE bridge_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
        )
        for version in (1, 2, 3, 4):
            for statement in MIGRATIONS[version]:
                connection.execute(statement)
        connection.execute(
            "INSERT INTO bridge_meta (key, value) VALUES (?, ?)",
            ("claim_authority", "DENY_CROSS_ROOT_UNKNOWN"),
        )
    assert ledger.initialize() == SCHEMA_VERSION
    assert not ledger.claim_dispatch(
        dispatch_id="blocked-v4", payload_hash="a" * 64,
        execution_id="e-v4", observed_at_utc=utc_now(),
    )
    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "DENY_CROSS_ROOT_UNKNOWN"


def test_cross_root_unknown_claims_deny_concurrent_callers(tmp_path: Path) -> None:
    """Concurrent calls to the same denied ledger do not create executions."""
    database = tmp_path / "concurrent-bridge.db"
    ledger = SQLiteLedger(database)
    ledger.initialize(cross_root_authority_unknown=True)

    def attempt(index: int) -> bool:
        independent = SQLiteLedger(database)
        return independent.claim_dispatch(
            dispatch_id="shared-identity", payload_hash="a" * 64,
            execution_id=f"blocked-{index}", observed_at_utc=utc_now(),
            honor_controls=True,
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        assert not any(pool.map(attempt, range(4)))

    with ledger.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


def test_single_root_atomic_claim_survives_reopen(tmp_path: Path) -> None:
    """Safety fence must not break already-proven single-DB claim uniqueness."""
    database = tmp_path / "single-root.db"
    ledger = SQLiteLedger(database)
    ledger.initialize()

    def attempt(index: int) -> bool:
        return SQLiteLedger(database).claim_dispatch(
            dispatch_id="once", payload_hash="a" * 64,
            execution_id=f"execution-{index}", observed_at_utc=utc_now(),
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        claimed = list(pool.map(attempt, range(4)))
    assert claimed.count(True) == 1
    assert claimed.count(False) == 3

    reopened = SQLiteLedger(database)
    assert reopened.initialize() == SCHEMA_VERSION
    assert not reopened.claim_dispatch(
        dispatch_id="once", payload_hash="a" * 64,
        execution_id="after-restart", observed_at_utc=utc_now(),
    )
    with reopened.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 1


def test_direct_current_root_initialization_cannot_grant_single_root_authority(
    tmp_path: Path, monkeypatch,
) -> None:
    """A direct SQLiteLedger caller must not bypass installed-root fencing."""
    current = tmp_path / "AppData" / "Local" / "FOX2" / "AgentBridge"
    monkeypatch.setattr("fox2_agent_bridge.ledger.BRIDGE_ROOT", current)
    ledger = SQLiteLedger(current / "data" / "bridge.db")
    assert ledger.initialize() == SCHEMA_VERSION
    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "DENY_CROSS_ROOT_UNKNOWN"

    assert not ledger.claim_dispatch(
        dispatch_id="direct-current", payload_hash="a" * 64,
        execution_id="blocked-direct", observed_at_utc=utc_now(),
    )
    assert not SQLiteLedger(current / "data" / "bridge.db").claim_dispatch(
        dispatch_id="direct-current", payload_hash="a" * 64,
        execution_id="blocked-after-reopen", observed_at_utc=utc_now(),
    )
