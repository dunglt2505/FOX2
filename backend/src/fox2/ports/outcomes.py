"""Frozen transport-independent outcome/error classifications for later WPs.

No I/O implementation. Failures are values with sanitized codes, not raw errors.
UNKNOWN never means absence proven; UNAVAILABLE carries no observation.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from fox2.contracts.health import Capability
from fox2.contracts.market import MarketObservation
from fox2.contracts.watchlist import WatchlistPreference

UseContext = Literal["DISPLAY", "READ", "RETAINED_USE", "ANALYSIS"]

@dataclass(frozen=True)
class Unavailable:
    reason: Literal["NOT_FOUND", "RIGHTS_BLOCKED", "UNKNOWN", "UNSAFE_STORE", "INVALID_CANDIDATE"]

ObservationOrUnavailable = MarketObservation | Unavailable

@dataclass(frozen=True)
class IngestAudit:
    audit_id: str
    received_at: datetime
    raw_sha256: str

@dataclass(frozen=True)
class CommitResult:
    status: Literal["COMMITTED", "UNCHANGED", "REJECTED", "UNAVAILABLE"]
    record_id: str | None
    revision: int | None
    promoted: bool
    reason: Literal["VALID", "DUPLICATE", "INVALID_CANDIDATE", "AMBIGUOUS_ORDER", "UNSAFE_STORE"]

@dataclass(frozen=True)
class SelectionDecision:
    capability: Capability
    selection_audit_id: str
    observation: ObservationOrUnavailable

@dataclass(frozen=True)
class PreferenceConflict:
    current_version: int

@dataclass(frozen=True)
class PreferenceFailure:
    reason: Literal["INVALID_ITEMS", "UNKNOWN_INSTRUMENT", "UNSAFE_STORE"]

PreferenceResultOrConflict = WatchlistPreference | PreferenceConflict | PreferenceFailure
