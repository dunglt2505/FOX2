"""Fail-closed source selection against frozen store and semantic ports."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Callable, Mapping
from uuid import uuid4

from fox2.contracts.health import Capability, SourceHealth
from fox2.contracts.market import MarketObservation, Bars
from fox2.ports.outcomes import SelectionDecision, Unavailable, UseContext
from fox2.ports.store import StoreReadPort
from fox2.validation.schema import MarketValidator
from fox2.validation.semantics import CapabilityContext


@dataclass(frozen=True)
class CapabilityPolicy:
    """Trusted, locally supplied evidence; no implicit provider thresholds.

    Calendar/policy versions bind evidence to the candidate. Freshness measures
    as_of (snapshot currency), never event age (which may represent no trades).
    """
    capability: Capability
    freshness_budget: timedelta
    freshness_policy_version: str
    calendar_version: str
    session: str
    mapping_verified: bool = False
    session_mapping_verified: bool = False
    coverage_verified: bool = False
    relevant_gap: bool | None = None
    adjustment_evidence_verified: bool = False
    transport_verified: bool = False
    subscriptions_verified: bool = False

    def __post_init__(self):
        if self.capability not in ('QUOTE', 'BARS', 'INDEX'):
            raise ValueError('unsupported capability')
        if self.freshness_budget <= timedelta(0):
            raise ValueError('freshness budget must be positive')
        if not all((self.freshness_policy_version, self.calendar_version, self.session)):
            raise ValueError('policy identity required')


@dataclass(frozen=True)
class SelectionAuditRecord:
    selection_audit_id: str
    capability: str
    instrument_id: str
    use_context: str
    source_id: str | None
    record_id: str | None
    accepted: bool
    reason_codes: tuple[str, ...]
    evaluated_at: datetime


def _digest(value: object) -> str:
    # Never persist user/provider supplied strings or secret-like identifiers.
    return sha256(str(value).encode('utf-8')).hexdigest()


class DataSourceManager:
    def __init__(self, store: StoreReadPort, *,
                 policies: Mapping[Capability, CapabilityPolicy] | None = None,
                 profile: str = 'INVESTOR', provider_enabled: bool = False,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc),
                 audit_id_factory: Callable[[], str] = lambda: uuid4().hex,
                 audit_sink: Callable[[SelectionAuditRecord], None] = lambda record: None):
        if profile not in ('INVESTOR', 'ISOLATED_TEST'):
            raise ValueError('unsupported profile')
        self._store = store
        self._policies = dict(policies or {})
        self._profile = profile
        self._provider_enabled = provider_enabled
        self._clock = clock
        self._id_factory = audit_id_factory
        self._sink = audit_sink
        self._sequence = 0

    def source_health(self, capability: Capability) -> SourceHealth:
        return SourceHealth(capability=capability, readiness='UNAVAILABLE',
                            state='UNKNOWN', gap_state='UNKNOWN', rights_state='UNKNOWN',
                            verified_until=None, reason='NOT_INTEGRATED')

    def select(self, capability: Capability, instrument_id: str,
               use_context: UseContext) -> SelectionDecision:
        now = self._clock()
        if now.utcoffset() != timedelta(0):
            raise ValueError('evaluation time must be UTC')
        self._sequence += 1
        audit_id = 'dsm-' + _digest(f'{self._id_factory()}:{self._sequence}')
        candidate = None

        def finish(value, reason):
            accepted = isinstance(value, MarketObservation)
            self._sink(SelectionAuditRecord(
                audit_id, capability if capability in ('QUOTE', 'BARS', 'INDEX') else 'INVALID',
                _digest(instrument_id), use_context if use_context in
                ('READ', 'DISPLAY', 'ANALYSIS', 'RETAINED_USE') else 'INVALID',
                _digest(candidate.source_id) if candidate and candidate.source_id else None,
                _digest(candidate.record_id) if candidate and candidate.record_id else None,
                accepted, (reason,), now))
            return SelectionDecision(capability, audit_id, value)

        if (capability not in ('QUOTE', 'BARS', 'INDEX') or
                use_context not in ('READ', 'DISPLAY', 'ANALYSIS', 'RETAINED_USE') or
                not isinstance(instrument_id, str) or not instrument_id.strip()):
            return finish(Unavailable('INVALID_CANDIDATE'), 'INVALID_REQUEST')
        if self._provider_enabled:
            return finish(Unavailable('UNKNOWN'), 'NOT_INTEGRATED')
        try:
            value = self._store.get_observation(instrument_id, capability, now)
        except Exception:
            return finish(Unavailable('UNSAFE_STORE'), 'UNSAFE_STORE')
        if isinstance(value, Unavailable):
            return finish(value, value.reason)
        if not isinstance(value, MarketObservation):
            return finish(Unavailable('INVALID_CANDIDATE'), 'INVALID_CANDIDATE')
        candidate = value
        try:
            # model_copy can bypass DTO validation; do not trust such store values.
            value = MarketObservation.model_validate_json(value.model_dump_json())
        except (ValueError, TypeError, AttributeError):
            return finish(Unavailable('INVALID_CANDIDATE'), 'INVALID_CANDIDATE')
        if (value.instrument_id != instrument_id or value.payload is None or
                value.payload.kind != {'QUOTE': 'quote', 'BARS': 'bars', 'INDEX': 'index_summary'}[capability]):
            return finish(Unavailable('INVALID_CANDIDATE'), 'IDENTITY_CAPABILITY_MISMATCH')
        if self._profile == 'INVESTOR' and (value.profile != 'INVESTOR' or
                value.data_mode == 'SYNTHETIC' or value.retrieval_channel == 'TEST_FIXTURE'):
            return finish(Unavailable('INVALID_CANDIDATE'), 'INVESTOR_FIXTURE')
        if (value.retrieval_channel == 'UNAVAILABLE' or not value.source_id or
                not value.record_id or not value.origin_provider or
                (value.quality != 'VALID' and value.data_mode != 'PROVIDER_NATIVE_UNVERIFIED')):
            return finish(Unavailable('INVALID_CANDIDATE'), 'PROVENANCE_OR_QUALITY_INVALID')
        required = ['read', 'retained_use']  # Local store retained-use protection.
        if use_context in ('DISPLAY', 'ANALYSIS'):
            required.append('redisplay')
        rights = value.rights
        if (any(getattr(rights, field) != 'VERIFIED' for field in required) or
                not rights.evidence_ref or rights.verified_until is None or
                rights.verified_until.utcoffset() != timedelta(0) or now >= rights.verified_until):
            return finish(Unavailable('RIGHTS_BLOCKED'), 'RIGHTS_BLOCKED')
        policy = self._policies.get(capability)
        if policy is None or policy.capability != capability:
            return finish(Unavailable('UNKNOWN'), 'POLICY_UNKNOWN')
        context = CapabilityContext(capability, now, use_context,
            policy.freshness_budget, policy.transport_verified, policy.subscriptions_verified,
            policy.session_mapping_verified, policy.adjustment_evidence_verified,
            policy.coverage_verified, policy.relevant_gap)
        verdict = MarketValidator().validate_semantics(value, context)
        if value.data_mode == 'PROVIDER_NATIVE_UNVERIFIED':
            return finish(Unavailable('UNKNOWN'), 'NATIVE_DIAGNOSTIC_ONLY')
        if (not policy.mapping_verified or value.mapping_state != 'VERIFIED' or
                any(getattr(value, f) in ('UNKNOWN', 'BLOCKED') for f in
                    ('price_unit', 'volume_unit', 'turnover_unit', 'price_basis')) or
                not policy.session_mapping_verified or not policy.coverage_verified or
                policy.relevant_gap is not False or value.completeness != 'COMPLETE' or
                value.calendar_version != policy.calendar_version or value.session != policy.session or
                value.freshness_policy_version != policy.freshness_policy_version):
            return finish(Unavailable('UNKNOWN'), 'EVIDENCE_UNKNOWN')
        if value.freshness_state in ('LIVE', 'PERIODIC_LIVE') and not (
                policy.transport_verified and policy.subscriptions_verified):
            return finish(Unavailable('UNKNOWN'), 'TRANSPORT_UNKNOWN')
        if value.freshness_state not in ('LATEST_VALID', 'EOD_CONFIRMED', 'LIVE', 'PERIODIC_LIVE'):
            return finish(Unavailable('UNKNOWN'), 'FRESHNESS_BLOCKED')
        if value.as_of is None or not timedelta(0) <= now - value.as_of <= policy.freshness_budget:
            return finish(Unavailable('UNKNOWN'), 'FRESHNESS_UNKNOWN_OR_STALE')
        if isinstance(value.payload, Bars) and (value.payload.gaps or not value.payload.items):
            return finish(Unavailable('UNKNOWN'), 'BARS_GAP_OR_COVERAGE')
        if verdict.status != 'PASS':
            # Missing amounts may remain missing on a safe quote/index. All other
            # semantic unknowns block selection; no zero substitution occurs.
            only_amounts_missing = (not verdict.errors and all(
                code.startswith('MISSING:payload.') for code in verdict.unknowns))
            if not only_amounts_missing:
                return finish(Unavailable('INVALID_CANDIDATE' if verdict.errors else 'UNKNOWN'),
                              'SEMANTIC_INVALID' if verdict.errors else 'SEMANTIC_UNKNOWN')
        selected = value.model_copy(deep=True, update={
            'selection_audit_id': audit_id, 'selection_reason': 'OFFLINE_POLICY_VERIFIED'})
        return finish(selected, 'OFFLINE_POLICY_VERIFIED')
