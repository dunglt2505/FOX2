"""F1 host-broker *storage core*; NOT a host authority or runtime admission.

This module is deliberately NOT wired into desktop/ledger/e2e_runner. A future
privileged Windows broker must own this database under an OS-enforced ACL,
authenticate every IPC peer, independently validate legacy-executor retirement,
and keep the authority provisioning/revocation methods inaccessible to Bridge.
An unprivileged import/call of this class is NOT proof of retirement.
"""
from __future__ import annotations

import sqlite3
from contextlib import closing
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BrokerEpoch:
    epoch: int
    policy_id: str
    source_commit: str
    package_sha256: str
    expires_at: int


class F1BrokerStore:
    """Atomic global consumed-ID and bounded lease storage for a host service.

    All time values are supplied by the *trusted service*, not by a caller.
    The service must enforce clock monotonicity/reboot fencing and OS policy.
    """

    def __init__(self, path: Path):
        self.path = Path(path)

    def _db(self) -> sqlite3.Connection:
        con = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA busy_timeout=15000")
        con.execute("PRAGMA synchronous=FULL")
        return con

    def initialize(self) -> None:
        # Only a privileged host service may create/manage the real DB.
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                con.execute("CREATE TABLE IF NOT EXISTS authority ("
                            "id INTEGER PRIMARY KEY CHECK(id=1), epoch INTEGER NOT NULL,"
                            "policy_id TEXT NOT NULL, source_commit TEXT NOT NULL,"
                            "package_sha256 TEXT NOT NULL, expires_at INTEGER NOT NULL,"
                            "revoked INTEGER NOT NULL CHECK(revoked IN (0,1)),"
                            "time_floor INTEGER NOT NULL DEFAULT 0 CHECK(time_floor>=0))")
                # Upgrade already-created offline broker fixtures without resetting authority.
                columns = {row[1] for row in con.execute("PRAGMA table_info(authority)")}
                if "time_floor" not in columns:
                    con.execute("ALTER TABLE authority ADD COLUMN time_floor INTEGER "
                                "NOT NULL DEFAULT 0 CHECK(time_floor>=0)")
                con.execute("CREATE TABLE IF NOT EXISTS consumed ("
                            "dispatch_id TEXT PRIMARY KEY, reason TEXT NOT NULL,"
                            "epoch INTEGER NOT NULL)")
                con.execute("CREATE TABLE IF NOT EXISTS leases ("
                            "dispatch_id TEXT PRIMARY KEY REFERENCES consumed(dispatch_id),"
                            "lease_id TEXT NOT NULL UNIQUE, epoch INTEGER NOT NULL,"
                            "package_sha256 TEXT NOT NULL, expires_at INTEGER NOT NULL,"
                            "revoked INTEGER NOT NULL CHECK(revoked IN (0,1)))")
                con.execute("COMMIT")
            except BaseException:
                con.execute("ROLLBACK")
                raise

    def import_consumed(self, identities: list[str]) -> None:
        """Before provisioning only: import every old-root/manual uncertain ID."""
        if not identities or any(not isinstance(x, str) or not x or len(x) > 256
                                 for x in identities):
            raise ValueError("invalid historical consumed identity inventory")
        if len(identities) != len(set(identities)):
            raise ValueError("duplicate historical identity inventory")
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                if con.execute("SELECT 1 FROM authority WHERE id=1").fetchone():
                    raise ValueError("cannot import after authority provisioning")
                for identity in identities:
                    con.execute("INSERT OR IGNORE INTO consumed VALUES (?,?,?)",
                                (identity, "HISTORICAL_UNCERTAIN", 0))
                con.execute("COMMIT")
            except BaseException:
                con.execute("ROLLBACK")
                raise

    def provision_from_privileged_service(self, epoch: BrokerEpoch) -> None:
        """Service-internal operation ONLY. Never expose through user IPC.

        Service must independently verify OS policy, old-writer retirement,
        exact package and immutable source before invoking this method.
        """
        if (epoch.epoch <= 0 or epoch.expires_at <= 0 or
                not epoch.policy_id or len(epoch.source_commit) != 40 or
                len(epoch.package_sha256) != 64):
            raise ValueError("invalid host epoch metadata")
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                prior = con.execute("SELECT epoch FROM authority WHERE id=1").fetchone()
                if prior is not None and epoch.epoch <= prior["epoch"]:
                    raise ValueError("epoch rollback/reuse")
                con.execute("INSERT INTO authority VALUES (1,?,?,?,?,?,0) "
                            "ON CONFLICT(id) DO UPDATE SET epoch=excluded.epoch,"
                            "policy_id=excluded.policy_id,"
                            "source_commit=excluded.source_commit,"
                            "package_sha256=excluded.package_sha256,"
                            "expires_at=excluded.expires_at,revoked=0",
                            (epoch.epoch, epoch.policy_id, epoch.source_commit,
                             epoch.package_sha256, epoch.expires_at))
                # Old leases never cross an epoch, including service restart.
                con.execute("UPDATE leases SET revoked=1 WHERE revoked=0")
                con.execute("COMMIT")
            except BaseException:
                con.execute("ROLLBACK")
                raise

    def revoke_from_privileged_service(self) -> None:
        """Service-internal; revocation is durable and invalidates all leases."""
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                con.execute("UPDATE authority SET revoked=1 WHERE id=1")
                con.execute("UPDATE leases SET revoked=1 WHERE revoked=0")
                con.execute("COMMIT")
            except BaseException:
                con.execute("ROLLBACK")
                raise

    @staticmethod
    def _advance_trusted_time(con: sqlite3.Connection, now: int) -> bool:
        """Persist a nondecreasing service-observed time, including DENY calls.

        This is a rollback detector, NOT a trusted clock or OS attestation.
        Only a privileged broker may supply now; a Bridge-supplied timestamp
        would render this guard meaningless.
        """
        if type(now) is not int or now < 0:
            return False
        row = con.execute("SELECT time_floor FROM authority WHERE id=1").fetchone()
        if row is None or now < row["time_floor"]:
            return False
        con.execute("UPDATE authority SET time_floor=? WHERE id=1", (now,))
        return True

    def claim(self, *, dispatch_id: str, lease_id: str, epoch: int,
              package_sha256: str, now: int, expires_at: int) -> bool:
        """Atomic global claim; failed/uncertain claims must not be replayed.

        Called ONLY inside authenticated service IPC, never from Bridge.
        """
        if (not isinstance(dispatch_id, str) or not isinstance(lease_id, str) or
                not dispatch_id or not lease_id or len(dispatch_id) > 256 or
                len(lease_id) > 256 or type(epoch) is not int or
                type(expires_at) is not int or type(now) is not int or
                expires_at <= now or now < 0):
            return False
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                if not self._advance_trusted_time(con, now):
                    con.execute("ROLLBACK")
                    return False
                row = con.execute("SELECT * FROM authority WHERE id=1").fetchone()
                allowed = bool(
                    row and not row["revoked"] and row["epoch"] == epoch and
                    row["package_sha256"] == package_sha256 and
                    now < row["expires_at"] and expires_at <= row["expires_at"]
                )
                if not allowed or con.execute(
                    "SELECT 1 FROM consumed WHERE dispatch_id=?", (dispatch_id,)
                ).fetchone():
                    con.execute("COMMIT")
                    return False
                con.execute("INSERT INTO consumed VALUES (?,?,?)",
                            (dispatch_id, "CLAIMED_UNCERTAIN", epoch))
                con.execute("INSERT INTO leases VALUES (?,?,?,?,?,0)",
                            (dispatch_id, lease_id, epoch, package_sha256, expires_at))
                con.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                con.execute("ROLLBACK")
                return False
            except BaseException:
                con.execute("ROLLBACK")
                raise

    def spawn_permitted(self, *, dispatch_id: str, lease_id: str, epoch: int,
                        package_sha256: str, now: int) -> bool:
        """Service-side live lease check; NOT a capability for client spawning.

        A privileged service must own actual spawn and the time source.
        Time-floor updates are durable even on an otherwise denied request.
        """
        if (type(now) is not int or now < 0 or type(epoch) is not int or
                not isinstance(dispatch_id, str) or
                not isinstance(lease_id, str)):
            return False
        with closing(self._db()) as con:
            con.execute("BEGIN IMMEDIATE")
            try:
                if not self._advance_trusted_time(con, now):
                    con.execute("ROLLBACK")
                    return False
                row = con.execute(
                    "SELECT a.revoked AS ar, a.epoch AS ae, a.package_sha256 AS ap,"
                    "a.expires_at AS ax, l.revoked AS lr, l.epoch AS le,"
                    "l.package_sha256 AS lp, l.expires_at AS lx "
                    "FROM authority a JOIN leases l ON a.id=1 "
                    "WHERE l.dispatch_id=? AND l.lease_id=?",
                    (dispatch_id, lease_id),
                ).fetchone()
                allowed = bool(row and not row["ar"] and not row["lr"] and
                               row["ae"] == epoch == row["le"] and
                               row["ap"] == package_sha256 == row["lp"] and
                               now < row["ax"] and now < row["lx"])
                con.execute("COMMIT")
                return allowed
            except BaseException:
                con.execute("ROLLBACK")
                raise

    def consumed_ids(self) -> tuple[str, ...]:
        with closing(self._db()) as con:
            return tuple(row[0] for row in con.execute(
                "SELECT dispatch_id FROM consumed ORDER BY dispatch_id"))
