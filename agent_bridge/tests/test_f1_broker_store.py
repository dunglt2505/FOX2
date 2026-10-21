"""F1 broker-storage offline contract tests; no host admission or Agent spawn."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from fox2_agent_bridge.f1_broker_store import BrokerEpoch, F1BrokerStore

PACKAGE = "a" * 64
SOURCE = "b" * 40


def new_store(tmp_path: Path) -> F1BrokerStore:
    store = F1BrokerStore(tmp_path / "privileged-host-fixture" / "global.db")
    store.initialize()
    return store


def epoch(n: int = 1, expires_at: int = 500) -> BrokerEpoch:
    return BrokerEpoch(n, "synthetic-windows-policy", SOURCE, PACKAGE, expires_at)


def test_unprovisioned_broker_is_deny_by_default(tmp_path: Path) -> None:
    store = new_store(tmp_path)
    assert not store.claim(dispatch_id="D", lease_id="L", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    assert not store.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                     package_sha256=PACKAGE, now=100)
    assert store.consumed_ids() == ()


def test_historical_consumed_ids_block_positive_claim_and_cannot_import_late(
    tmp_path: Path,
) -> None:
    store = new_store(tmp_path)
    store.import_consumed(["old-dispatch", "uncertain-crash"])
    store.provision_from_privileged_service(epoch())
    assert not store.claim(dispatch_id="old-dispatch", lease_id="L1", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    assert not store.claim(dispatch_id="uncertain-crash", lease_id="L2", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    with pytest.raises(ValueError, match="cannot import"):
        store.import_consumed(["new-historical"])
    assert store.consumed_ids() == ("old-dispatch", "uncertain-crash")


def test_single_global_claim_survives_restart_and_duplicate_race(
    tmp_path: Path,
) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    def race(n: int) -> bool:
        other = F1BrokerStore(store.path)
        return other.claim(dispatch_id="same-id", lease_id=f"lease-{n}",
                           epoch=1, package_sha256=PACKAGE, now=100,
                           expires_at=200)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(race, range(20)))
    assert sum(results) == 1
    assert store.consumed_ids() == ("same-id",)
    restarted = F1BrokerStore(store.path)
    assert not restarted.claim(dispatch_id="same-id", lease_id="again",
                               epoch=1, package_sha256=PACKAGE, now=101,
                               expires_at=220)


def test_expiry_package_epoch_and_revocation_are_fail_closed(
    tmp_path: Path,
) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    assert not store.claim(dispatch_id="wrong-package", lease_id="A", epoch=1,
                           package_sha256="f" * 64, now=100, expires_at=200)
    assert not store.claim(dispatch_id="wrong-epoch", lease_id="B", epoch=2,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    assert not store.claim(dispatch_id="expired", lease_id="C", epoch=1,
                           package_sha256=PACKAGE, now=500, expires_at=501)
    assert not store.claim(dispatch_id="overlong", lease_id="D", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=501)
    assert store.claim(dispatch_id="valid", lease_id="E", epoch=1,
                       package_sha256=PACKAGE, now=100, expires_at=200)
    assert store.spawn_permitted(dispatch_id="valid", lease_id="E", epoch=1,
                                 package_sha256=PACKAGE, now=199)
    assert not store.spawn_permitted(dispatch_id="valid", lease_id="E", epoch=1,
                                     package_sha256=PACKAGE, now=200)
    assert not store.spawn_permitted(dispatch_id="valid", lease_id="E", epoch=1,
                                     package_sha256="f" * 64, now=101)
    store.revoke_from_privileged_service()
    assert not store.spawn_permitted(dispatch_id="valid", lease_id="E", epoch=1,
                                     package_sha256=PACKAGE, now=101)
    assert not store.claim(dispatch_id="after-revoke", lease_id="F", epoch=1,
                           package_sha256=PACKAGE, now=101, expires_at=200)
    assert store.consumed_ids() == ("valid",)


def test_new_epoch_invalidates_old_leases_without_replay(
    tmp_path: Path,
) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    assert store.claim(dispatch_id="D1", lease_id="L1", epoch=1,
                       package_sha256=PACKAGE, now=100, expires_at=200)
    with pytest.raises(ValueError, match="rollback/reuse"):
        store.provision_from_privileged_service(epoch())
    store.provision_from_privileged_service(epoch(2))
    assert not store.spawn_permitted(dispatch_id="D1", lease_id="L1", epoch=1,
                                     package_sha256=PACKAGE, now=101)
    assert not store.claim(dispatch_id="D1", lease_id="L2", epoch=2,
                           package_sha256=PACKAGE, now=101, expires_at=200)
    assert store.claim(dispatch_id="D2", lease_id="L3", epoch=2,
                       package_sha256=PACKAGE, now=101, expires_at=200)
    assert store.consumed_ids() == ("D1", "D2")


def test_historical_import_is_transactional_and_rejects_ambiguous_inventory(
    tmp_path: Path,
) -> None:
    store = new_store(tmp_path)
    with pytest.raises(ValueError, match="duplicate"):
        store.import_consumed(["D", "D"])
    with pytest.raises(ValueError, match="invalid"):
        store.import_consumed([])
    assert store.consumed_ids() == ()


def test_trusted_time_floor_survives_restart_and_denies_rollback(tmp_path: Path) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    assert store.claim(dispatch_id="D", lease_id="L", epoch=1,
                       package_sha256=PACKAGE, now=100, expires_at=300)
    assert store.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                 package_sha256=PACKAGE, now=150)
    assert not store.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                     package_sha256=PACKAGE, now=149)
    restarted = F1BrokerStore(store.path)
    assert not restarted.claim(dispatch_id="D2", lease_id="L2", epoch=1,
                               package_sha256=PACKAGE, now=149, expires_at=250)
    assert not restarted.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                         package_sha256=PACKAGE, now=149)
    assert restarted.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                     package_sha256=PACKAGE, now=151)
    assert store.consumed_ids() == ("D",)


def test_denied_expiry_advances_floor_and_epoch_does_not_reset_it(tmp_path: Path) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    assert not store.claim(dispatch_id="expired", lease_id="L", epoch=1,
                           package_sha256=PACKAGE, now=500, expires_at=501)
    assert not store.claim(dispatch_id="backdated", lease_id="L2", epoch=1,
                           package_sha256=PACKAGE, now=101, expires_at=200)
    store.provision_from_privileged_service(epoch(2, expires_at=900))
    assert not store.claim(dispatch_id="backdated", lease_id="L3", epoch=2,
                           package_sha256=PACKAGE, now=499, expires_at=600)
    assert store.claim(dispatch_id="fresh", lease_id="L4", epoch=2,
                       package_sha256=PACKAGE, now=501, expires_at=600)
    assert store.consumed_ids() == ("fresh",)


def test_invalid_clock_and_identity_types_fail_closed(tmp_path: Path) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch())
    for value in (True, False, 100.5, "100", -1):
        assert not store.claim(dispatch_id="D", lease_id="L", epoch=1,
                               package_sha256=PACKAGE, now=value, expires_at=200)
        assert not store.spawn_permitted(dispatch_id="D", lease_id="L", epoch=1,
                                         package_sha256=PACKAGE, now=value)
    assert not store.claim(dispatch_id=123, lease_id="L", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    assert not store.claim(dispatch_id="D", lease_id="L", epoch=True,
                           package_sha256=PACKAGE, now=100, expires_at=200)
    assert not store.claim(dispatch_id="D", lease_id="L", epoch=1,
                           package_sha256=PACKAGE, now=100, expires_at=True)
    assert store.consumed_ids() == ()


def test_initialize_migrates_prior_offline_authority_schema(tmp_path: Path) -> None:
    import sqlite3

    path = tmp_path / "old-core.db"
    with sqlite3.connect(path) as con:
        con.execute("CREATE TABLE authority (id INTEGER PRIMARY KEY, epoch INTEGER,"
                    "policy_id TEXT, source_commit TEXT, package_sha256 TEXT,"
                    "expires_at INTEGER, revoked INTEGER)")
        con.execute("INSERT INTO authority VALUES (1,1,'old',?,?,500,0)",
                    (SOURCE, PACKAGE))
    store = F1BrokerStore(path)
    store.initialize()
    with sqlite3.connect(path) as con:
        cols = {row[1] for row in con.execute("PRAGMA table_info(authority)")}
        assert "time_floor" in cols
        assert con.execute("SELECT epoch,time_floor FROM authority").fetchone() == (1, 0)
    store.provision_from_privileged_service(epoch(2, expires_at=900))
    assert store.claim(dispatch_id="new", lease_id="L", epoch=2,
                       package_sha256=PACKAGE, now=100, expires_at=200)
    store.initialize()  # idempotent; must not reset the durable time floor
    with sqlite3.connect(path) as con:
        assert con.execute("SELECT time_floor FROM authority").fetchone()[0] == 100


def test_already_expired_lease_request_still_fences_clock_rewind(tmp_path: Path) -> None:
    store = new_store(tmp_path)
    store.provision_from_privileged_service(epoch(1, expires_at=900))
    assert not store.claim(dispatch_id="expired-request", lease_id="L1", epoch=1,
                           package_sha256=PACKAGE, now=700, expires_at=700)
    assert not F1BrokerStore(store.path).claim(
        dispatch_id="rewind", lease_id="L2", epoch=1,
        package_sha256=PACKAGE, now=699, expires_at=800)
    assert store.claim(dispatch_id="later", lease_id="L3", epoch=1,
                       package_sha256=PACKAGE, now=701, expires_at=800)
