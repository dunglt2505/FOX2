"""Preference shape; verified ID lookup and atomic CAS belong to later WPs."""
from typing import Annotated
from pydantic import AwareDatetime, Field, field_validator
from .base import DTO

InstrumentIds = Annotated[list[Annotated[str, Field(min_length=1)]], Field(max_length=100)]

class WatchlistPreference(DTO):
    version: Annotated[int, Field(ge=0)]
    items: InstrumentIds
    updated_at: AwareDatetime | None

    @field_validator("items")
    @classmethod
    def unique_ids(cls, items):
        if len(set(items)) != len(items):
            raise ValueError("duplicate instrument IDs")
        return items

class WatchlistReplace(DTO):
    expected_version: Annotated[int, Field(ge=0)]
    items: InstrumentIds

    @field_validator("items")
    @classmethod
    def unique_ids(cls, items):
        return WatchlistPreference.unique_ids(items)
