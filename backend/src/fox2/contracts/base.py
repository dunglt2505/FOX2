"""Immutable DTO base; JSON input is parsed with strict field types."""
from pydantic import BaseModel, ConfigDict

class DTO(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, strict=True,
                              allow_inf_nan=False, populate_by_name=True)
