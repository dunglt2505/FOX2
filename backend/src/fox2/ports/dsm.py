"""Selection interface only; P2-03 owns per-use rights/freshness decisions.

No history-to-quote fallback. Every decision has a selection audit identity;
missing/blocked observations are explicit Unavailable values.
"""
from typing import Protocol
from fox2.contracts.health import Capability
from .outcomes import UseContext, SelectionDecision

class DSMSelectPort(Protocol):
    def select(self, capability: Capability, instrument_id: str,
               use_context: UseContext) -> SelectionDecision: ...
