"""Small immutable models shared across Bridge core components."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from pathlib import Path


class Status(StrEnum):
    READY = "READY"
    UNAVAILABLE = "UNAVAILABLE"
    UNVERIFIED = "UNVERIFIED"
    BLOCKED = "BLOCKED"


class AuthStatus(StrEnum):
    AUTHENTICATED = "AUTHENTICATED"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True)
class ToolCapability:
    name: str
    status: Status
    evidence: str


@dataclass(frozen=True)
class ToolRecord:
    tool_name: str
    configured_path: Path | None
    executable_path: Path | None
    version: str | None
    available: bool
    version_exit_code: int | None
    version_stdout_available: bool
    version_stderr_available: bool
    auth_status: AuthStatus
    capabilities: tuple[ToolCapability, ...]
    observed_at: datetime
    error: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "tool_name": self.tool_name,
            "configured_path": str(self.configured_path) if self.configured_path else None,
            "executable_path": str(self.executable_path) if self.executable_path else None,
            "version": self.version,
            "available": self.available,
            "version_exit_code": self.version_exit_code,
            "version_stdout_available": self.version_stdout_available,
            "version_stderr_available": self.version_stderr_available,
            "auth_status": self.auth_status.value,
            "capabilities": [
                {
                    "name": capability.name,
                    "status": capability.status.value,
                    "evidence": capability.evidence,
                }
                for capability in self.capabilities
            ],
            "observed_at": self.observed_at.isoformat(),
            "error": self.error,
        }
