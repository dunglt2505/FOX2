"""Explicit offline P2-01 settings. Environment/credentials are never read."""
from typing import Literal
from pydantic import Field
from .contracts.base import DTO

class Settings(DTO):
    host: Literal["127.0.0.1"] = "127.0.0.1"
    port: int = Field(default=8000, ge=1, le=65535)
    provider_enabled: Literal[False] = False
    network_enabled: Literal[False] = False
    profile: Literal["INVESTOR"] = "INVESTOR"
