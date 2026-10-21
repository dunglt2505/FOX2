from __future__ import annotations

import sqlite3
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import SimpleNamespace

import pytest

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


def test_existing_single_root_metadata_cannot_admit_direct_installed_claim(
    tmp_path: Path, monkeypatch,
) -> None:
    """Existing v5 SINGLE_ROOT state cannot authorize a direct installed claim."""
    root = tmp_path / "installed-current-root"
    ledger = SQLiteLedger(root / "data" / "bridge.db")
    assert ledger.initialize() == SCHEMA_VERSION  # Seed an older local-only authority.
    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "SINGLE_ROOT"

    monkeypatch.setattr("fox2_agent_bridge.ledger.BRIDGE_ROOT", root)
    assert not SQLiteLedger(ledger.database_path).claim_dispatch(
        dispatch_id="existing-single-root", payload_hash="a" * 64,
        execution_id="must-not-spawn", observed_at_utc=utc_now(),
    )
    with ledger.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


def test_installed_root_alternate_db_and_normalized_alias_fail_closed(
    tmp_path: Path, monkeypatch,
) -> None:
    """Customized DB within the installed root cannot mint or use authority."""
    root = tmp_path / "installed-current-root"
    alternate = root / "data" / "alternate-bridge.db"
    ledger = SQLiteLedger(alternate)
    ledger.initialize()  # Ordinary single-root fixture before installed-root binding.
    monkeypatch.setattr("fox2_agent_bridge.ledger.BRIDGE_ROOT", root)

    # Both canonical path and noncanonical relative path must be refused.
    alias = root / "data" / ".." / "data" / "alternate-bridge.db"
    for candidate in (alternate, alias):
        probe = SQLiteLedger(candidate)
        assert not probe.claim_dispatch(
            dispatch_id="alias-identity", payload_hash="a" * 64,
            execution_id="blocked-alias", observed_at_utc=utc_now(),
        )
        assert probe.initialize() == SCHEMA_VERSION
        assert not probe.claim_dispatch(
            dispatch_id="alias-identity", payload_hash="a" * 64,
            execution_id="blocked-after-init", observed_at_utc=utc_now(),
        )

    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "DENY_CROSS_ROOT_UNKNOWN"
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0



def test_forged_installed_authority_cannot_bypass_claim_time_root_fence(
    tmp_path: Path, monkeypatch,
) -> None:
    """A writable SQLite metadata edit is never host retirement evidence."""
    root = tmp_path / "installed-root"
    monkeypatch.setattr("fox2_agent_bridge.ledger.BRIDGE_ROOT", root)
    ledger = SQLiteLedger(root / "data" / "bridge.db")
    assert ledger.initialize() == SCHEMA_VERSION
    with ledger.connect() as connection:
        connection.execute(
            "UPDATE bridge_meta SET value='SINGLE_ROOT' "
            "WHERE key='claim_authority'"
        )
        connection.execute(
            "INSERT OR REPLACE INTO bridge_meta (key,value) VALUES (?,?)",
            ("f1_retirement_attested", "true"),
        )
        connection.execute(
            "INSERT OR REPLACE INTO bridge_meta (key,value) VALUES (?,?)",
            ("f1_epoch", "999999999"),
        )
    for probe in (ledger, SQLiteLedger(root / "data" / "bridge.db")):
        assert not probe.claim_dispatch(
            dispatch_id="forged-proof", payload_hash="a" * 64,
            execution_id="never-spawn", observed_at_utc=utc_now(),
            honor_controls=False,
        )
    with ledger.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


def test_independent_legacy_root_can_reclaim_same_identity_without_os_fence(
    tmp_path: Path, monkeypatch,
) -> None:
    """Document the real F1 blocker: separate SQLite files are not one writer.

    This is a synthetic counterexample, not permission to start legacy Bridge.
    The legacy fixture deliberately uses a separate unfenced v5-style ledger.
    """
    current_root = tmp_path / "current"
    old_root = tmp_path / "legacy"
    current = SQLiteLedger(current_root / "data" / "bridge.db")
    legacy = SQLiteLedger(old_root / "data" / "bridge.db")
    assert current.initialize() == SCHEMA_VERSION
    assert legacy.initialize() == SCHEMA_VERSION
    monkeypatch.setattr("fox2_agent_bridge.ledger.BRIDGE_ROOT", current_root)
    identity = "same-git-dispatch-across-two-sqlite-files"
    assert not current.claim_dispatch(
        dispatch_id=identity, payload_hash="a" * 64,
        execution_id="current-blocked", observed_at_utc=utc_now(),
    )
    assert legacy.claim_dispatch(
        dispatch_id=identity, payload_hash="a" * 64,
        execution_id="old-writer-simulated", observed_at_utc=utc_now(),
    )
    assert not legacy.claim_dispatch(
        dispatch_id=identity, payload_hash="a" * 64,
        execution_id="old-writer-replay", observed_at_utc=utc_now(),
    )
    with current.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0
    with legacy.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 1

def test_denied_ledger_rolls_back_abrupt_precommit_process_exit(
    tmp_path: Path,
) -> None:
    """Synthetic child dies mid-SQLite transaction; no uncommitted claim survives."""
    database = tmp_path / "crash-before-commit.db"
    ledger = SQLiteLedger(database)
    ledger.initialize(cross_root_authority_unknown=True)
    script = (
        "import os,sqlite3,sys;"
        "db=sqlite3.connect(sys.argv[1]);"
        "db.execute('BEGIN IMMEDIATE');"
        "db.execute(\"INSERT INTO dispatches (dispatch_id,state,created_at_utc,updated_at_utc) "
        "VALUES ('crash-probe','CLAIMED','now','now')\");"
        "os._exit(71)"
    )
    outcome = subprocess.run(
        [sys.executable, "-c", script, str(database)],
        capture_output=True, text=True, timeout=20, check=False,
    )
    assert outcome.returncode == 71, outcome.stderr
    reopened = SQLiteLedger(database)
    assert reopened.initialize() == SCHEMA_VERSION
    assert not reopened.claim_dispatch(
        dispatch_id="crash-probe", payload_hash="a" * 64,
        execution_id="no-replay", observed_at_utc=utc_now(),
    )
    with reopened.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0
        assert connection.execute(
            "SELECT value FROM bridge_meta WHERE key='claim_authority'"
        ).fetchone()["value"] == "DENY_CROSS_ROOT_UNKNOWN"


def test_denied_e2e_dispatch_never_reaches_agent_or_result_preparation(
    bridge_config, tmp_path: Path, monkeypatch,
) -> None:
    """F0 current-root denial must stop before *any* adapter/spawn checkpoint."""
    from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
    from fox2_agent_bridge.errors import ReplayBlocked

    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize(cross_root_authority_unknown=True)
    identity = "FOX2-F0-NO-SPAWN"
    calls = []

    class PassiveTransport:
        def query_control_sha(self, branch):
            return "a" * 40

        def fetch_control(self, branch, commit_sha):
            return None

        def read_dispatch_blob(self, commit_sha, dispatch_path):
            return b"{}", "b" * 40

    runner = BridgeE2ERunner(
        bridge_config, ledger, transport=PassiveTransport(),
        can_claim=lambda: True,
    )
    monkeypatch.setattr(
        "fox2_agent_bridge.e2e_runner.DispatchPoller",
        lambda *args, **kwargs: SimpleNamespace(
            poll_once=lambda: SimpleNamespace(status="NO_CHANGE")
        ),
    )
    monkeypatch.setattr(runner, "_validate_dispatch",
        lambda *args, **kwargs: {
            "dispatch_id": identity,
            "_payload_sha256": "c" * 64,
            "_agent_product": "CODEX",
        })
    monkeypatch.setattr(runner, "_resolve_worktree",
        lambda payload: (tmp_path / "never-create-worktree", "d" * 40))
    monkeypatch.setattr(runner, "_resolve_prompt", lambda payload: "fixture")

    def forbidden(*args, **kwargs):
        calls.append("POST_CLAIM")
        pytest.fail("denied claim must never prepare or spawn an Agent")

    monkeypatch.setattr(runner, "_prepare_required_parents", forbidden)
    with pytest.raises(ReplayBlocked):
        runner.run_once(dispatch_path="fixture/blocked-dispatch.json")

    assert calls == []
    with ledger.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0



@pytest.mark.parametrize("control", ["pause", "request-exit", "malformed"])
def test_pause_stop_or_corruption_after_claim_blocks_agent_spawn(
    bridge_config, tmp_path: Path, monkeypatch, control,
) -> None:
    """A local control change after durable claim must not invoke a paid CLI.

    This is an offline local guard only, not host-enforced F1 authority.
    """
    from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
    from fox2_agent_bridge.errors import AgentNotStarted

    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    identity = f"FOX2-PRE-SPAWN-{control}"
    invoked = []

    class PassiveTransport:
        def query_control_sha(self, branch):
            return "a" * 40

        def fetch_control(self, branch, commit_sha):
            return None

        def read_dispatch_blob(self, commit_sha, dispatch_path):
            return b"{}", "b" * 40

    runner = BridgeE2ERunner(
        bridge_config, ledger, transport=PassiveTransport(),
        can_claim=lambda: True,
    )
    monkeypatch.setattr(
        "fox2_agent_bridge.e2e_runner.DispatchPoller",
        lambda *args, **kwargs: SimpleNamespace(
            poll_once=lambda: SimpleNamespace(status="NO_CHANGE")
        ),
    )
    monkeypatch.setattr(runner, "_validate_dispatch", lambda *args, **kwargs: {
        "dispatch_id": identity,
        "_payload_sha256": "c" * 64,
        "_agent_product": "CODEX",
        "branch": "work/offline-fixture",
        "prompt": {"sha256": "e" * 64},
        "agent": {"product": "CODEX"},
        "delivery_owner": "BRIDGE",
    })
    monkeypatch.setattr(runner, "_resolve_worktree",
                        lambda payload: (tmp_path / "worktree", "d" * 40))
    monkeypatch.setattr(runner, "_resolve_prompt", lambda payload: "fixture")

    def change_control(*, payload, worktree):
        if control == "malformed":
            with ledger.connect() as connection:
                connection.execute(
                    "UPDATE worker_state SET payload=? WHERE id=1",
                    ('{"paused":"false"}',),
                )
        else:
            ledger.control(control)

    monkeypatch.setattr(runner, "_prepare_required_parents", change_control)

    def forbidden_adapter(*args, **kwargs):
        invoked.append("AGENT_INVOKED")
        pytest.fail("paid Agent adapter must not be created after PAUSE/STOP")

    monkeypatch.setitem(
        __import__("fox2_agent_bridge.e2e_runner", fromlist=["_ADAPTERS"])._ADAPTERS,
        "CODEX", forbidden_adapter,
    )
    with pytest.raises(AgentNotStarted):
        runner.run_once(dispatch_path="fixture/after-claim.json")
    assert invoked == []
    with ledger.connect() as connection:
        assert connection.execute(
            "SELECT COUNT(*) FROM dispatches WHERE dispatch_id=?",
            (identity,),
        ).fetchone()[0] == 1
        assert connection.execute(
            "SELECT COUNT(*) FROM executions WHERE dispatch_id=?",
            (identity,),
        ).fetchone()[0] == 1
    assert not ledger.claim_dispatch(
        dispatch_id=identity, payload_hash="c" * 64,
        execution_id="replay-must-fail", observed_at_utc=utc_now(),
    )


@pytest.mark.parametrize("payload", [
    '{"paused":"true"}', '{"stop_requested":1}', '[]', '{',
])
def test_spawn_permitted_fails_closed_on_invalid_local_control_payload(
    tmp_path: Path, payload,
) -> None:
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    assert ledger.spawn_permitted()
    with ledger.connect() as connection:
        connection.execute(
            "UPDATE worker_state SET payload=? WHERE id=1", (payload,)
        )
    assert not ledger.spawn_permitted()


def test_configured_alternate_runtime_root_cannot_grant_claim_authority(
    bridge_config, tmp_path: Path, monkeypatch,
) -> None:
    """A --config root outside the default install is still a runtime, not proof."""
    from fox2_agent_bridge.desktop import initialize_runtime

    monkeypatch.setattr("fox2_agent_bridge.desktop.LEGACY_ROOT", tmp_path / "absent-legacy")
    # Seed preexisting SINGLE_ROOT metadata, as well as testing a fresh root.
    for preexisting in (False, True):
        if preexisting:
            with SQLiteLedger(bridge_config.database_path).connect() as connection:
                connection.execute("UPDATE bridge_meta SET value='SINGLE_ROOT' WHERE key='claim_authority'")
        ledger = initialize_runtime(bridge_config)
        assert not ledger.claim_dispatch(
            dispatch_id=f"alternate-{preexisting}", payload_hash="a" * 64,
            execution_id="forbidden", observed_at_utc=utc_now(), honor_controls=False,
        )
        reopened = SQLiteLedger(bridge_config.database_path)
        reopened.initialize()
        assert not reopened.claim_dispatch(
            dispatch_id="after-reopen", payload_hash="a" * 64,
            execution_id="forbidden-reopen", observed_at_utc=utc_now(),
        )
        with ledger.connect() as connection:
            assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 0
            assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 0


@pytest.mark.parametrize("boundary,expected_stage,expected_state", [
    ("after-claim", "UNKNOWN", "NEEDS_RECONCILIATION"),
    ("before-adapter", "CLAIMED", "SAFE_NOT_STARTED"),
    ("inside-fake-adapter", "RUNNING", "NEEDS_RECONCILIATION"),
    ("after-synthetic-child", "RUNNING", "NEEDS_RECONCILIATION"),
])
def test_abrupt_runner_exit_preserves_consumption_without_replay(
    tmp_path: Path, boundary, expected_stage, expected_state,
) -> None:
    """Kill a synthetic runner at real checkpoints; no paid CLI is involved."""
    from fox2_agent_bridge.desktop import reconcile

    database = tmp_path / "abrupt-runner.db"
    marker = tmp_path / "fake-adapter-entered"
    script = r'''
import os, sys, subprocess
from pathlib import Path
from types import SimpleNamespace
from fox2_agent_bridge.config import BridgeConfig
from fox2_agent_bridge.ledger import SQLiteLedger
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
import fox2_agent_bridge.e2e_runner as module
database, marker, boundary = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
ledger = SQLiteLedger(database)
ledger.initialize()
config = BridgeConfig(bridge_root=database.parent, database_path=database)
transport = SimpleNamespace(query_control_sha=lambda _: 'a'*40,
    fetch_control=lambda *_: None, read_dispatch_blob=lambda *_: (b'{}', 'b'*40))
module.DispatchPoller = lambda *a, **k: SimpleNamespace(poll_once=lambda: SimpleNamespace(status='NO_CHANGE'))
runner = BridgeE2ERunner(config, ledger, transport=transport)
payload = {'dispatch_id':'synthetic-crash', '_payload_sha256':'c'*64,
    '_agent_product':'CODEX', 'agent':{'product':'CODEX'}, 'branch':'work/synthetic-crash'}
runner._validate_dispatch = lambda *a, **k: payload
runner._resolve_worktree = lambda _: (database.parent / 'unused-worktree', 'd'*40)
runner._resolve_prompt = lambda _: 'synthetic only'
def forbidden(*a, **k):
    raise AssertionError('unexpected result verification or publication')
runner._verify_result = forbidden
runner._commit_and_push_codex_result = forbidden
original_claim = ledger.claim_dispatch
def claim(**kwargs):
    result = original_claim(**kwargs)
    assert result
    if boundary == 'after-claim':
        os._exit(72)
    return result
ledger.claim_dispatch = claim
def prepare(**kwargs):
    if boundary == 'before-adapter':
        os._exit(72)
runner._prepare_required_parents = prepare
class FakeAdapter:
    def __init__(self, config): pass
    def run_prompt(self, **kwargs):
        marker.write_text('synthetic adapter entered; no CLI spawned')
        if boundary == 'after-synthetic-child':
            # A harmless Python child substitutes for the Agent process. Its
            # marker proves the child executed before the supervisor exited.
            subprocess.run([sys.executable, '-c',
                'import pathlib,sys; pathlib.Path(sys.argv[1]).write_text("synthetic child exited")',
                str(marker) + '.child'], check=True, timeout=10)
        os._exit(72)
module._ADAPTERS = {'CODEX': FakeAdapter}
runner.run_once(dispatch_path='synthetic-only')
raise AssertionError('crash injection not reached')
'''
    outcome = subprocess.run(
        [sys.executable, "-c", script, str(database), str(marker), boundary],
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert outcome.returncode == 72, outcome.stderr
    assert marker.exists() == (boundary in {"inside-fake-adapter", "after-synthetic-child"})
    assert Path(str(marker) + ".child").exists() == (boundary == "after-synthetic-child")
    ledger = SQLiteLedger(database)
    ledger.initialize()
    assert ledger.dispatch_status("synthetic-crash")["stage"] == expected_stage
    # Reconciliation cannot call a verifier for these uncertain/pre-start stages.
    def forbidden(**kwargs):
        pytest.fail("uncertain crash must not verify/publish/relaunch")
    assert reconcile(ledger, SimpleNamespace(_verify_result=forbidden))[0]["outcome"] == expected_state
    assert reconcile(ledger, None) == []
    assert not ledger.claim_dispatch(
        dispatch_id="synthetic-crash", payload_hash="c" * 64,
        execution_id="replay", observed_at_utc=utc_now(),
    )
    with ledger.connect() as connection:
        assert connection.execute("SELECT COUNT(*) FROM dispatches").fetchone()[0] == 1
        assert connection.execute("SELECT COUNT(*) FROM executions").fetchone()[0] == 1


@pytest.mark.parametrize("stage", ["AGENT_EXITED", "PUBLISHING"])
@pytest.mark.parametrize("metadata", [
    {"post_start_failure": "capacity_unavailable"},
    {"requested": {"model_policy": "PINNED", "model": "gpt-6.1-sol"}, "observed_model": "different"},
    {"requested": {"reasoning_effort": "medium"}, "observed_reasoning_effort": "low"},
    {"requested": {"permission_profile": "FULL_ACCESS"}, "observed_permission_profile": "different"},
])
def test_restart_configuration_failure_cannot_promote_or_verify_result(tmp_path, stage, metadata):
    """Exit zero cannot bypass a durable post-start/configuration failure."""
    from fox2_agent_bridge.desktop import reconcile

    ledger = SQLiteLedger(tmp_path / "failed-configuration.db")
    ledger.initialize()
    assert ledger.claim_dispatch(dispatch_id="failed-config", payload_hash="a" * 64,
        execution_id="e", observed_at_utc=utc_now())
    ledger.checkpoint("e", stage, {"agent_exit_code": 0, "agent_metadata": metadata})
    def forbidden(**kwargs):
        pytest.fail("configuration failure must block result verification")
    assert reconcile(ledger, SimpleNamespace(_verify_result=forbidden))[0]["outcome"] == "NEEDS_RECONCILIATION"
    assert not ledger.claim_dispatch(dispatch_id="failed-config", payload_hash="a" * 64,
        execution_id="replay", observed_at_utc=utc_now())
    assert reconcile(ledger, None) == []
