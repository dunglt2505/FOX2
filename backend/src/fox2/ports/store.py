"""Store contracts only; P2-02 owns atomic persistence and promotion.

instrument_id is verified source identity, never a display symbol. capability
is typed; at_or_before is a UTC availability cutoff (None = current). Missing or
unsafe reads return Unavailable. append_and_promote commits candidate/current/
audit atomically; duplicate/ambiguous candidates must not regress the pointer.
"""
from datetime import datetime
from typing import Protocol
from fox2.contracts.health import Capability
from fox2.contracts.market import MarketObservation
from .outcomes import ObservationOrUnavailable, IngestAudit, CommitResult

class StoreReadPort(Protocol):
    def get_observation(self, instrument_id: str, capability: Capability,
                        at_or_before: datetime | None) -> ObservationOrUnavailable: ...

class StoreWritePort(Protocol):
    def append_and_promote(self, candidate: MarketObservation,
                           ingest_audit: IngestAudit) -> CommitResult: ...
