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
