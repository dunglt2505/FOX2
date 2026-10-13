"""DTOs bound to schema blob fa395662b772658d782b46718b7eb8392f6bbf76.

The published literal retains `candidate`; release status does not rename it.
All fields, including nullable fields, are required. Shape is not semantic truth.
"""
from typing import Annotated, Literal
from pydantic import AwareDatetime, Field, model_validator
from .base import DTO
from .market_schema import shape_errors

CONTRACT_VERSION = "market-data-v0.4-candidate"

class Rights(DTO):
    read: Literal['VERIFIED', 'BLOCKED', 'UNKNOWN']
    redisplay: Literal['VERIFIED', 'BLOCKED', 'UNKNOWN']
    retained_use: Literal['VERIFIED', 'BLOCKED', 'UNKNOWN']
    evidence_ref: str | None
    verified_until: AwareDatetime | None

class Quote(DTO):
    kind: Literal['quote']
    last_price: Annotated[float, Field(ge=0)] | None
    reference_price: Annotated[float, Field(ge=0)] | None
    ceiling_price: Annotated[float, Field(ge=0)] | None
    floor_price: Annotated[float, Field(ge=0)] | None
    cumulative_volume: Annotated[float, Field(ge=0)] | None
    cumulative_turnover: Annotated[float, Field(ge=0)] | None

class BarsItem(DTO):
    start_at: AwareDatetime
    end_at: AwareDatetime | None
    update_at: AwareDatetime | None
    open: Annotated[float, Field(gt=0)]
    high: Annotated[float, Field(gt=0)]
    low: Annotated[float, Field(gt=0)]
    close: Annotated[float, Field(gt=0)]
    volume: Annotated[float, Field(ge=0)] | None
    turnover: Annotated[float, Field(ge=0)] | None
    provisional: bool | None
    revision: Annotated[int, Field(ge=0)]

class BarsGap(DTO):
    from_at: AwareDatetime = Field(alias="from")
    to: AwareDatetime
    reason: Annotated[str, Field(min_length=1)]
    capability: Literal['BARS', 'TICKS', 'QUOTE', 'INDEX']

class Bars(DTO):
    kind: Literal['bars']
    timeframe: Literal['1D']
    from_at: AwareDatetime = Field(alias="from")
    to: AwareDatetime
    items: list[BarsItem]
    gaps: list[BarsGap]

class IndexSummary(DTO):
    kind: Literal['index_summary']
    value: Annotated[float, Field(ge=0)] | None
    change_value: float | None
    change_percent: float | None
    up_count: Annotated[int, Field(ge=0)] | None
    down_count: Annotated[int, Field(ge=0)] | None
    unchanged_count: Annotated[int, Field(ge=0)] | None
    volume: Annotated[float, Field(ge=0)] | None
    turnover: Annotated[float, Field(ge=0)] | None

class MarketObservation(DTO):
    profile: Literal['INVESTOR', 'ISOLATED_TEST']
    instrument_id: str | None
    symbol: str | None
    instrument_type: Literal['STOCK', 'INDEX', 'UNKNOWN']
    venue: Literal['HOSE', 'HNX', 'UPCOM', 'UNKNOWN']
    board_id: str | None
    record_id: str | None
    revision: Annotated[int, Field(ge=0)] | None
    source_id: str | None
    origin_provider: str | None
    source_revision: str | None
    retrieval_channel: Literal['WEBSOCKET', 'HISTORICAL_API', 'LOCAL_STORE', 'TEST_FIXTURE', 'UNAVAILABLE']
    event_at: AwareDatetime | None
    as_of: AwareDatetime | None
    received_at: AwareDatetime | None
    first_available_at: AwareDatetime | None
    data_mode: Literal['VERIFIED_PROVIDER', 'PROVIDER_NATIVE_UNVERIFIED', 'UNAVAILABLE', 'SYNTHETIC']
    freshness_state: Literal['LIVE', 'PERIODIC_LIVE', 'LATEST_VALID', 'EOD_CONFIRMED', 'STALE', 'GAP_RECOVERING', 'DELAYED', 'ENTITLEMENT_BLOCKED', 'UNAVAILABLE']
    quality: Literal['VALID', 'PARTIAL', 'INVALID', 'UNKNOWN']
    mapping_state: Literal['VERIFIED', 'UNKNOWN', 'BLOCKED']
    completeness: Literal['COMPLETE', 'PARTIAL', 'UNKNOWN']
    price_basis: Literal['RAW', 'ADJUSTED', 'UNKNOWN', 'NOT_APPLICABLE']
    price_unit: Literal['VND_PER_SHARE', 'INDEX_POINTS', 'UNKNOWN', 'NOT_APPLICABLE']
    volume_unit: Literal['SHARES', 'UNKNOWN', 'NOT_APPLICABLE']
    turnover_unit: Literal['VND', 'UNKNOWN', 'NOT_APPLICABLE']
    adjustment_version: str | None
    calendar_version: str | None
    session: str | None
    freshness_policy_version: str | None
    rights: Rights
    selection_audit_id: Annotated[str, Field(min_length=1)]
    selection_reason: Annotated[str, Field(min_length=1)]
    missing_fields: list[str]
    payload: None | Quote | Bars | IndexSummary

class MarketDataEnvelope(DTO):
    contract_version: Literal["market-data-v0.4-candidate"]
    request_id: Annotated[str, Field(min_length=1)]
    generated_at: AwareDatetime
    data: MarketObservation

    @model_validator(mode="after")
    def published_shape(self):
        if shape_errors(self.model_dump(mode="json", by_alias=True)):
            raise ValueError("market envelope does not satisfy published shape")
        return self
