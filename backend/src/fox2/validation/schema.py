"""Shape verdicts only; never assert semantic validity."""
from dataclasses import dataclass
import json
from typing import Literal
from pydantic import ValidationError
from fox2.contracts.market import MarketDataEnvelope, MarketObservation
from fox2.contracts.market_schema import shape_errors
from .semantics import CapabilityContext, SemanticVerdict, validate_semantics

MarketKind = Literal["quote", "bars", "index_summary"]

@dataclass(frozen=True)
class ValidationResult:
    shape_passed: bool
    errors: tuple[str, ...] = ()
    envelope: MarketDataEnvelope | None = None

class MarketValidator:
    def validate_shape(self, payload: object, kind: MarketKind) -> ValidationResult:
        if kind not in ("quote", "bars", "index_summary"):
            return ValidationResult(False, ("UNSUPPORTED_KIND",))
        try:
            errors = shape_errors(payload)
            if errors:
                return ValidationResult(False, errors)
            envelope = MarketDataEnvelope.model_validate_json(json.dumps(payload, allow_nan=False))
        except (ValidationError, TypeError, ValueError, OverflowError):
            return ValidationResult(False, ("MALFORMED_PAYLOAD",))
        if envelope.data.payload is not None and envelope.data.payload.kind != kind:
            return ValidationResult(False, ("KIND_MISMATCH",))
        return ValidationResult(True, envelope=envelope)

    def validate_semantics(self, observation: MarketObservation,
                           capability_context: CapabilityContext) -> SemanticVerdict:
        return validate_semantics(observation, capability_context)
