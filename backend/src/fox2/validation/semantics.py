"""Offline market invariants. This module does not select sources or certify LIVE."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Literal
from fox2.contracts.market import MarketObservation, Quote, Bars, IndexSummary
from fox2.contracts.health import Capability

@dataclass(frozen=True)
class CapabilityContext:
    capability: Capability
    evaluated_at: datetime
    use_context: Literal["DISPLAY", "READ", "RETAINED_USE", "ANALYSIS"] = "DISPLAY"
    freshness_budget: timedelta | None = None
    transport_verified: bool = False
    subscriptions_verified: bool = False
    session_mapping_verified: bool = False
    adjustment_evidence_verified: bool = False
    coverage_verified: bool = False
    relevant_gap: bool | None = None

    def __post_init__(self):
        if self.evaluated_at.utcoffset() != timedelta(0):
            raise ValueError("evaluation time must be UTC")
        if self.capability not in ("QUOTE", "BARS", "INDEX"):
            raise ValueError("unsupported capability")
        if self.use_context not in ("DISPLAY", "READ", "RETAINED_USE", "ANALYSIS"):
            raise ValueError("unsupported use context")
        if self.freshness_budget is not None and self.freshness_budget <= timedelta(0):
            raise ValueError("freshness budget must be positive")

@dataclass(frozen=True)
class SemanticVerdict:
    status: Literal["PASS", "PARTIAL", "FAIL"]
    errors: tuple[str, ...] = ()
    unknowns: tuple[str, ...] = ()


def validate_semantics(o: MarketObservation, c: CapabilityContext) -> SemanticVerdict:
    errors, unknowns = [], []
    def require(test, reason):
        if not test:
            errors.append(reason)
    def utc(value, name):
        if value is not None:
            require(value.utcoffset() == timedelta(0), "NON_UTC:" + name)
    # Observation timestamps remain independent of envelope.generated_at.
    for name in ("event_at", "as_of", "received_at", "first_available_at"):
        utc(getattr(o, name), name)
    utc(o.rights.verified_until, "rights.verified_until")
    if o.payload is None:
        require(o.data_mode == "UNAVAILABLE" or o.freshness_state == "ENTITLEMENT_BLOCKED", "ABSENT_PAYLOAD_MODE")
        for name in ("source_id", "record_id", "revision", "event_at", "as_of", "received_at", "first_available_at"):
            require(getattr(o, name) is None, "ABSENT_OBSERVATION:" + name)
        require(bool(o.selection_reason), "MISSING_UNAVAILABLE_REASON")
        return SemanticVerdict("FAIL" if errors else "PASS", tuple(errors))
    kind = {"QUOTE": "quote", "BARS": "bars", "INDEX": "index_summary"}[c.capability]
    require(o.payload.kind == kind, "CAPABILITY_MISMATCH")
    require(o.freshness_state != "ENTITLEMENT_BLOCKED", "BLOCKED_PAYLOAD")
    require(o.data_mode != "UNAVAILABLE", "UNAVAILABLE_PAYLOAD")
    require(o.quality != "INVALID", "INVALID_QUALITY")
    if o.profile == "INVESTOR":
        require(o.data_mode != "SYNTHETIC" and o.retrieval_channel != "TEST_FIXTURE", "INVESTOR_FIXTURE")
    for name in ("record_id", "source_id", "origin_provider", "received_at", "first_available_at"):
        require(getattr(o, name) is not None, "MISSING_OBSERVATION:" + name)
    if o.received_at and o.first_available_at:
        require(o.first_available_at >= o.received_at, "AVAILABILITY_BEFORE_RECEIPT")
        require(o.first_available_at <= c.evaluated_at, "AVAILABILITY_IN_FUTURE")
    for name in ("event_at", "as_of"):
        value = getattr(o, name)
        if value is None:
            require(name in o.missing_fields, "UNDECLARED_MISSING:" + name)
            unknowns.append("MISSING:" + name)
        elif o.received_at:
            require(value <= o.received_at, "TIME_AFTER_RECEIPT:" + name)
    if o.event_at and o.as_of:
        require(o.event_at <= o.as_of, "EVENT_AFTER_AS_OF")
    if isinstance(o.payload, Quote):
        for name in ("last_price", "reference_price", "ceiling_price", "floor_price"):
            value = getattr(o.payload, name)
            if value is not None:
                require(value > 0, "NONPOSITIVE_PRICE:" + name)
        if o.payload.ceiling_price is not None and o.payload.floor_price is not None:
            require(o.payload.floor_price <= o.payload.ceiling_price, "QUOTE_BOUNDS")
    elif isinstance(o.payload, IndexSummary):
        if o.payload.value is not None:
            require(o.payload.value > 0, "NONPOSITIVE_INDEX")
        require(o.instrument_type == "INDEX", "INDEX_TYPE")
    elif isinstance(o.payload, Bars):
        p = o.payload
        utc(p.from_at, "bars.from"); utc(p.to, "bars.to")
        require(timedelta(0) < p.to - p.from_at <= timedelta(days=366), "BARS_WINDOW")
        for bar in p.items:
            require(bar.high >= max(bar.open, bar.close, bar.low), "OHLC_HIGH")
            require(bar.low <= min(bar.open, bar.close, bar.high), "OHLC_LOW")
            utc(bar.start_at, "bar.start_at"); utc(bar.end_at, "bar.end_at"); utc(bar.update_at, "bar.update_at")
            require(p.from_at <= bar.start_at < p.to, "BAR_OUTSIDE_WINDOW")
            if bar.end_at is not None:
                require(bar.start_at < bar.end_at <= p.to, "BAR_INTERVAL")
                require(c.session_mapping_verified, "SESSION_MAPPING_UNVERIFIED")
            else:
                unknowns.append("UNKNOWN_BAR_END")
                require(bar.provisional is not False, "CLOSED_BAR_WITHOUT_END")
            if bar.update_at is not None:
                require(bar.start_at <= bar.update_at, "BAR_UPDATE_BEFORE_START")
                if o.received_at:
                    require(bar.update_at <= o.received_at, "BAR_UPDATE_AFTER_RECEIPT")
            else:
                unknowns.append("UNKNOWN_BAR_UPDATE")
            for name in ("volume", "turnover"):
                if getattr(bar, name) is None:
                    unknowns.append("MISSING:bar." + name)
        for gap in p.gaps:
            utc(gap.from_at, "gap.from"); utc(gap.to, "gap.to")
            require(p.from_at <= gap.from_at < gap.to <= p.to, "GAP_INTERVAL")
        if p.gaps:
            require(o.completeness != "COMPLETE", "COMPLETE_WITH_GAPS")
    # Null amounts remain null; genuine zero never becomes missing.
    if not isinstance(o.payload, Bars):
        for name, value in o.payload.model_dump().items():
            if name != "kind" and value is None:
                require("payload." + name in o.missing_fields, "UNDECLARED_MISSING:payload." + name)
                unknowns.append("MISSING:payload." + name)
    if o.price_basis == "ADJUSTED":
        require(bool(o.adjustment_version) and c.adjustment_evidence_verified, "ADJUSTMENT_UNVERIFIED")
    for name in ("price_unit", "volume_unit", "turnover_unit", "price_basis", "mapping_state"):
        if getattr(o, name) in ("UNKNOWN", "BLOCKED"):
            unknowns.append("UNVERIFIED:" + name)
    if o.payload.kind == "quote":
        require(o.price_unit in ("VND_PER_SHARE", "UNKNOWN"), "QUOTE_UNIT")
    if o.payload.kind == "bars":
        require(o.price_unit in ("VND_PER_SHARE", "INDEX_POINTS", "UNKNOWN"), "BARS_UNIT")
    if o.payload.kind == "index_summary":
        require(o.price_unit in ("INDEX_POINTS", "UNKNOWN"), "INDEX_UNIT")
    if o.data_mode == "PROVIDER_NATIVE_UNVERIFIED":
        require(o.mapping_state == "UNKNOWN" and o.quality in ("PARTIAL", "UNKNOWN"), "NATIVE_CLASSIFICATION")
        require(o.freshness_state not in ("LIVE", "PERIODIC_LIVE", "EOD_CONFIRMED"), "NATIVE_FRESHNESS")
        require(c.use_context != "ANALYSIS", "NATIVE_ANALYSIS_FORBIDDEN")
        unknowns.append("NATIVE_DIAGNOSTIC_ONLY")
    if o.data_mode == "VERIFIED_PROVIDER":
        require(o.mapping_state == "VERIFIED", "VERIFIED_PROVIDER_MAPPING")
        require(all(getattr(o, name) != "UNKNOWN" for name in
                    ("price_unit", "volume_unit", "turnover_unit", "price_basis")),
                "VERIFIED_PROVIDER_UNITS_BASIS")
    if o.data_mode in ("VERIFIED_PROVIDER", "PROVIDER_NATIVE_UNVERIFIED"):
        required_rights = ["read"]
        if c.use_context in ("DISPLAY", "ANALYSIS"):
            required_rights.append("redisplay")
        if c.use_context == "RETAINED_USE" or o.retrieval_channel == "LOCAL_STORE":
            required_rights.append("retained_use")
        for name in required_rights:
            require(getattr(o.rights, name) == "VERIFIED", "RIGHTS:" + name)
        require(bool(o.rights.evidence_ref) and o.rights.verified_until is not None, "RIGHTS_EVIDENCE")
        if o.rights.verified_until:
            require(c.evaluated_at < o.rights.verified_until, "RIGHTS_EXPIRED")
    if o.completeness == "COMPLETE":
        require(c.coverage_verified, "COVERAGE_UNVERIFIED")
    if o.freshness_state in ("LIVE", "PERIODIC_LIVE", "EOD_CONFIRMED"):
        require(o.data_mode == "VERIFIED_PROVIDER" and o.mapping_state == "VERIFIED", "FRESH_MAPPING")
        require(o.quality == "VALID" and o.completeness == "COMPLETE", "FRESH_QUALITY")
        require(not unknowns, "FRESH_UNKNOWN_FIELDS")
        require(bool(o.calendar_version and o.session and o.freshness_policy_version), "FRESH_POLICY")
        require(c.session_mapping_verified and c.relevant_gap is False, "FRESH_SESSION_GAP")
        if o.freshness_state in ("LIVE", "PERIODIC_LIVE"):
            require(c.transport_verified and c.subscriptions_verified, "LIVE_TRANSPORT")
            require(c.freshness_budget is not None and o.as_of is not None, "LIVE_FRESHNESS_UNKNOWN")
            if c.freshness_budget is not None and o.as_of is not None:
                require(timedelta(0) <= c.evaluated_at - o.as_of <= c.freshness_budget, "LIVE_STALE")
    return SemanticVerdict("FAIL" if errors else "PARTIAL" if unknowns else "PASS",
                           tuple(dict.fromkeys(errors)), tuple(dict.fromkeys(unknowns)))
