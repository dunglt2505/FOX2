"""Trusted local dependencies, supplied explicitly; payload claims are not proof."""
from dataclasses import dataclass
from fox2.validation.semantics import CapabilityContext


@dataclass(frozen=True)
class PromotionEvidence:
    context: CapabilityContext
    evidence_ref: str
    identity_verified: bool = False
    lifecycle_verified: bool = False
    # A verified source ordering adapter may provide an integer sequence.
    # Never parse or lexically compare candidate.source_revision here.
    order: int | None = None
    predecessor_record_id: str | None = None
