"""Separate process/source diagnostics; no market observation wrapper."""
from typing import Literal
from pydantic import AwareDatetime
from .base import DTO
from .market import CONTRACT_VERSION

Capability = Literal["QUOTE", "BARS", "INDEX"]

class ProcessHealth(DTO):
    contract_version: Literal["market-data-v0.4-candidate"] = CONTRACT_VERSION
    status: Literal["OK", "UNHEALTHY"]
    provider_enabled: bool

class SourceHealth(DTO):
    capability: Capability
    readiness: Literal["UNKNOWN", "UNAVAILABLE"]
    state: Literal["UNKNOWN", "UNAVAILABLE"]
    gap_state: Literal["UNKNOWN"]
    rights_state: Literal["UNKNOWN"]
    verified_until: AwareDatetime | None
    reason: Literal["NOT_INTEGRATED"]
