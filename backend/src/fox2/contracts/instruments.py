"""Verified search metadata; DTO creation alone does not verify an instrument."""
from typing import Annotated, Literal
from pydantic import Field
from .base import DTO

class Instrument(DTO):
    instrument_id: Annotated[str, Field(min_length=1)]
    symbol: Annotated[str, Field(min_length=1)]
    instrument_type: Literal["STOCK", "INDEX", "UNKNOWN"]
    venue: Literal["HOSE", "HNX", "UPCOM", "UNKNOWN"]
    board_id: str | None

class InstrumentSearchResult(DTO):
    items: Annotated[list[Instrument], Field(max_length=100)]
    universe_source: str | None
    universe_revision: str | None
    coverage: Literal["COMPLETE", "PARTIAL", "UNKNOWN"]
    cursor: str | None
