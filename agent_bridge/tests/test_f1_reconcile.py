"""Offline F1 historical-root reconciliation; all fixtures synthetic."""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from fox2_agent_bridge.f1_reconcile import ReconciliationHold, reconcile_consumed


def root(path: Path, dispatches: tuple[tuple[str, str, str | None], ...] = (),
         executions: tuple[tuple[str, str], ...] = ()) -> Path:
    with sqlite3.connect(path) as con:
        con.execute("CREATE TABLE dispatches (dispatch_id TEXT, state TEXT, payload_hash TEXT)")
        con.execute("CREATE TABLE executions (dispatch_id TEXT, state TEXT)")
        con.executemany("INSERT INTO dispatches VALUES (?,?,?)", dispatches)
        con.executemany("INSERT INTO executions VALUES (?,?)", executions)
    return path


def test_reconcile_two_disjoint_roots_and_manual_consumed(tmp_path: Path) -> None:
    a = root(tmp_path / "old.db", (("D1", "CLAIMED", "h1"),),
             (("D1", "RUNNING"),))
    b = root(tmp_path / "new.db", (("D2", "FAILED", "h2"),))
    result = reconcile_consumed((a, b), manual_consumed=("M1",),
                                inventory_complete=True)
    assert result.consumed_ids == ("D1", "D2", "M1")
    assert result.roots_checked == 2
    assert len(result.inventory_sha256) == 64
    assert reconcile_consumed((b, a), manual_consumed=("M1",),
                              inventory_complete=True).inventory_sha256 == result.inventory_sha256


@pytest.mark.parametrize("case", ["no_attestation", "one_root", "missing", "alias"])
def test_incomplete_root_inventory_is_hold(tmp_path: Path, case: str) -> None:
    a = root(tmp_path / "old.db")
    b = root(tmp_path / "new.db")
    roots = {"no_attestation": (a, b), "one_root": (a,),
             "missing": (a, tmp_path / "missing.db"), "alias": (a, a)}[case]
    with pytest.raises(ReconciliationHold):
        reconcile_consumed(roots, manual_consumed=(),
                           inventory_complete=case != "no_attestation")


@pytest.mark.parametrize("case", ["same_hash", "different_hash", "manual_overlap"])
def test_duplicate_consumption_is_ambiguous_even_if_hash_matches(
    tmp_path: Path, case: str,
) -> None:
    a = root(tmp_path / "old.db", (("D", "CLAIMED", "h"),))
    b = root(tmp_path / "new.db", (("D", "CLAIMED", "h" if case == "same_hash" else "z"),)
             if case != "manual_overlap" else ())
    with pytest.raises(ReconciliationHold):
        reconcile_consumed((a, b), manual_consumed=("D",) if case == "manual_overlap" else (),
                           inventory_complete=True)


@pytest.mark.parametrize("case", ["orphan", "empty_id", "empty_state", "duplicate_local"])
def test_invalid_rows_hold_without_writing(tmp_path: Path, case: str) -> None:
    entries = {
        "orphan": (),
        "empty_id": (("", "CLAIMED", "h"),),
        "empty_state": (("D", "", "h"),),
        "duplicate_local": (("D", "CLAIMED", "h"), ("D", "CLAIMED", "h")),
    }[case]
    executions = (("MISSING", "RUNNING"),) if case == "orphan" else ()
    a = root(tmp_path / "old.db", entries, executions)
    b = root(tmp_path / "new.db")
    with pytest.raises(ReconciliationHold):
        reconcile_consumed((a, b), manual_consumed=(), inventory_complete=True)
    assert a.exists() and b.exists()


def test_invalid_manual_marker_and_missing_tables_fail_closed(tmp_path: Path) -> None:
    a = root(tmp_path / "old.db")
    b = tmp_path / "new.db"
    sqlite3.connect(b).close()
    with pytest.raises(ReconciliationHold):
        reconcile_consumed((a, b), manual_consumed=(), inventory_complete=True)
    b.unlink()
    root(b)
    for manual in (("D", "D"), ("",), ("X" * 257,)):
        with pytest.raises(ReconciliationHold):
            reconcile_consumed((a, b), manual_consumed=manual, inventory_complete=True)

@pytest.mark.parametrize("sidecar", ["-wal", "-shm"])
def test_sidecars_hold_to_prevent_missing_uncheckpointed_claims(
    tmp_path: Path, sidecar: str,
) -> None:
    a = root(tmp_path / "old.db", (("D", "CLAIMED", "h"),))
    b = root(tmp_path / "new.db")
    marker = Path(str(a) + sidecar)
    marker.write_bytes(b"unverified-sidecar")
    with pytest.raises(ReconciliationHold, match="sidecar"):
        reconcile_consumed((a, b), manual_consumed=(), inventory_complete=True)
    assert marker.read_bytes() == b"unverified-sidecar"


def test_read_only_reconciliation_does_not_create_sqlite_sidecars(
    tmp_path: Path,
) -> None:
    a = root(tmp_path / "old.db", (("D", "FAILED", "h"),))
    b = root(tmp_path / "new.db")
    assert reconcile_consumed((a, b), manual_consumed=(),
                              inventory_complete=True).consumed_ids == ("D",)
    for path in (a, b):
        assert not Path(str(path) + "-wal").exists()
        assert not Path(str(path) + "-shm").exists()

def test_orphan_review_event_is_held_as_ambiguous_history(tmp_path: Path) -> None:
    a = root(tmp_path / "old.db", (("D", "CLAIMED", "h"),))
    b = root(tmp_path / "new.db")
    with sqlite3.connect(a) as con:
        con.execute("CREATE TABLE review_events (dispatch_id TEXT)")
        con.execute("INSERT INTO review_events VALUES ('MISSING')")
    with pytest.raises(ReconciliationHold, match="review event"):
        reconcile_consumed((a, b), manual_consumed=(), inventory_complete=True)
