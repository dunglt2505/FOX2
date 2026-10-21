"""F1 offline cross-root consumed-ID reconciliation; NEVER an authority grant.

Read-only SQLite inspection for a *quiesced, externally fenced* host.
The caller must independently verify that no legacy/current writer can run,
that every historical root/marker was discovered, and that the snapshot
covers WAL/sidecars. A result here is NOT proof of any of those conditions.
No positive installed claims or Agent execution are wired to this module.
"""
from __future__ import annotations

import hashlib
from contextlib import closing
import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote


class ReconciliationHold(ValueError):
    """Ambiguous, missing or inconsistent historical consumption: STOP."""


@dataclass(frozen=True)
class ReconciliationSnapshot:
    consumed_ids: tuple[str, ...]
    inventory_sha256: str
    roots_checked: int
    # This is intentionally not an admission/provisioning token.


def _inspect_root(path: Path) -> dict[str, str]:
    """Inspect one existing SQLite ledger without creating/migrating it."""
    if not path.is_file():
        raise ReconciliationHold("missing historical ledger")
    # Resolve file identity, not user-supplied relative aliases.
    uri = "file:" + quote(str(path.resolve()), safe="/:") + "?mode=ro"
    try:
        with closing(sqlite3.connect(uri, uri=True, timeout=5)) as con:
            con.row_factory = sqlite3.Row
            con.execute("PRAGMA query_only=ON")
            con.execute("BEGIN")
            integrity = con.execute("PRAGMA quick_check").fetchone()
            if integrity is None or integrity[0] != "ok":
                raise ReconciliationHold("ledger integrity not verified")
            names = {row[0] for row in con.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
            if not {"dispatches", "executions"} <= names:
                raise ReconciliationHold("unsupported historical ledger schema")
            columns = {
                row[1] for row in con.execute("PRAGMA table_info(dispatches)")
            }
            if not {"dispatch_id", "state", "payload_hash"} <= columns:
                raise ReconciliationHold("missing dispatch identity columns")
            ec = {row[1] for row in con.execute("PRAGMA table_info(executions)")}
            if not {"dispatch_id", "state"} <= ec:
                raise ReconciliationHold("missing execution identity columns")
            dispatches = con.execute(
                "SELECT dispatch_id, state, payload_hash FROM dispatches"
            ).fetchall()
            executions = con.execute(
                "SELECT dispatch_id, state FROM executions"
            ).fetchall()
            seen: dict[str, str] = {}
            for row in dispatches:
                identity, state, payload = row
                if (not isinstance(identity, str) or not identity or
                        len(identity) > 256 or not isinstance(state, str) or
                        not state):
                    raise ReconciliationHold("invalid dispatch identity/state")
                if identity in seen:
                    raise ReconciliationHold("duplicate dispatch identity in root")
                if payload is not None and not isinstance(payload, str):
                    raise ReconciliationHold("invalid historical payload digest")
                seen[identity] = payload or ""
            for row in executions:
                identity, state = row
                if (not isinstance(identity, str) or identity not in seen or
                        not isinstance(state, str) or not state):
                    raise ReconciliationHold("orphan or malformed execution")
                # Unknown, running and failed executions remain CONSUMED.
            return seen
    except ReconciliationHold:
        raise
    except (sqlite3.Error, OSError, ValueError) as exc:
        raise ReconciliationHold("historical ledger cannot be read safely") from exc


def reconcile_consumed(
    roots: tuple[Path, ...], *, manual_consumed: tuple[str, ...],
    inventory_complete: bool = False,
) -> ReconciliationSnapshot:
    """Fail closed unless caller asserts inventory coverage for offline review.

    inventory_complete is a *caller statement*, not a trusted host attestation.
    Never pass this result directly to broker.provision_from_privileged_service.
    """
    if not inventory_complete or len(roots) < 2:
        raise ReconciliationHold("cross-root inventory incomplete")
    canonical = [p.resolve() for p in roots]
    if len(set(canonical)) != len(canonical):
        raise ReconciliationHold("duplicate or aliased root")
    if (any(not isinstance(x, str) or not x or len(x) > 256
            for x in manual_consumed) or
            len(set(manual_consumed)) != len(manual_consumed)):
        raise ReconciliationHold("invalid manual consumed marker inventory")
    combined: dict[str, tuple[str, str]] = {}
    for path in canonical:
        for identity, payload in _inspect_root(path).items():
            if identity in combined:
                # Even identical payload across roots cannot establish which
                # executor ran. Require independent incident disposition.
                raise ReconciliationHold("cross-root duplicate dispatch identity")
            combined[identity] = (str(path), payload)
    for identity in manual_consumed:
        if identity in combined:
            # Manual markers may duplicate DB records legitimately; preserve
            # consumption but require explicit independent reconciliation.
            raise ReconciliationHold("manual marker overlaps ledger identity")
        combined[identity] = ("MANUAL_CONSUMED", "")
    identities = tuple(sorted(combined))
    digest = hashlib.sha256(json.dumps(
        identities, ensure_ascii=True, separators=(",", ":")
    ).encode("ascii")).hexdigest()
    return ReconciliationSnapshot(identities, digest, len(canonical))
