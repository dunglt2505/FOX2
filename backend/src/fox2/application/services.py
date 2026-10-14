"""Per-request DISPLAY decisions and atomic local preference operations."""
from datetime import datetime, timezone
from typing import Callable, Protocol
from uuid import uuid4

from fox2.contracts.instruments import Instrument
from fox2.contracts.market import CONTRACT_VERSION, MarketDataEnvelope, MarketObservation, Rights
from fox2.contracts.watchlist import WatchlistPreference, WatchlistReplace
from fox2.ports.dsm import DSMSelectPort
from fox2.ports.preferences import PreferenceRepositoryPort
from fox2.ports.outcomes import PreferenceConflict, PreferenceFailure, Unavailable
from .registry import ApplicationError, InstrumentRegistry


class Preferences(PreferenceRepositoryPort, Protocol):
    def get_preferences(self) -> WatchlistPreference | PreferenceFailure: ...


def unavailable(instrument: Instrument, audit_id: str, reason: str) -> MarketObservation:
    return MarketObservation(
        profile='INVESTOR', **instrument.model_dump(), record_id=None, revision=None,
        source_id=None, origin_provider=None, source_revision=None,
        retrieval_channel='UNAVAILABLE', event_at=None, as_of=None, received_at=None,
        first_available_at=None, data_mode='UNAVAILABLE', freshness_state='UNAVAILABLE',
        quality='UNKNOWN', mapping_state='UNKNOWN', completeness='UNKNOWN',
        price_basis='UNKNOWN', price_unit='UNKNOWN', volume_unit='UNKNOWN', turnover_unit='UNKNOWN',
        adjustment_version=None, calendar_version=None, session=None, freshness_policy_version=None,
        rights=Rights(read='UNKNOWN', redisplay='UNKNOWN', retained_use='UNKNOWN',
                      evidence_ref=None, verified_until=None),
        selection_audit_id=audit_id, selection_reason=reason,
        missing_fields=['payload', 'event_at', 'as_of', 'received_at', 'first_available_at'], payload=None)


class MarketService:
    def __init__(self, registry: InstrumentRegistry, dsm: DSMSelectPort,
                 clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)):
        self.registry, self.dsm, self.clock = registry, dsm, clock

    def envelope(self, instrument: Instrument, capability: str, *,
                 start: datetime | None = None, end: datetime | None = None,
                 basis: str = 'RAW') -> MarketDataEnvelope:
        decision = self.dsm.select(capability, instrument.instrument_id, 'DISPLAY')
        value = decision.observation
        if isinstance(value, Unavailable):
            if value.reason == 'UNSAFE_STORE':
                raise ApplicationError(503, 'Service unavailable')
            value = unavailable(instrument, decision.selection_audit_id, value.reason)
        elif (value.profile != 'INVESTOR' or value.data_mode == 'SYNTHETIC' or
              value.retrieval_channel == 'TEST_FIXTURE' or
              any(getattr(value, field) != getattr(instrument, field) for field in
                  ('instrument_id', 'symbol', 'instrument_type', 'venue', 'board_id'))):
            value = unavailable(instrument, decision.selection_audit_id, 'INVALID_CANDIDATE')
        if capability == 'BARS' and value.payload is not None:
            bars = value.payload
            if value.price_basis != basis or basis == 'UNKNOWN':
                value = unavailable(instrument, decision.selection_audit_id, 'UNSUPPORTED_BASIS')
            elif start < bars.from_at or end > bars.to:
                value = unavailable(instrument, decision.selection_audit_id, 'BARS_COVERAGE_UNKNOWN')
            else:
                items = [b for b in bars.items if start <= b.start_at < end]
                if not items:
                    value = unavailable(instrument, decision.selection_audit_id, 'BARS_COVERAGE_UNKNOWN')
                else:
                    value = value.model_copy(update={'payload': bars.model_copy(update={
                        'from_at': start, 'to': end, 'items': items})}, deep=True)
        return MarketDataEnvelope(contract_version=CONTRACT_VERSION, request_id=uuid4().hex,
                                  generated_at=self.clock(), data=value)


class WatchlistService:
    def __init__(self, repository: Preferences):
        self.repository = repository

    @staticmethod
    def result(value) -> WatchlistPreference:
        if isinstance(value, PreferenceConflict):
            raise ApplicationError(409, 'Watchlist version conflict')
        if isinstance(value, PreferenceFailure):
            if value.reason == 'UNSAFE_STORE':
                raise ApplicationError(503, 'Service unavailable')
            raise ApplicationError(422, 'Invalid watchlist items')
        if not isinstance(value, WatchlistPreference):
            raise ApplicationError(503, 'Service unavailable')
        return value

    def read(self) -> WatchlistPreference:
        return self.result(self.repository.get_preferences())

    def replace(self, request: WatchlistReplace) -> WatchlistPreference:
        return self.result(self.repository.replace_if_version(request.expected_version, request.items))
