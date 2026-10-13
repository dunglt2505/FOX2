"""Structured errors used by Bridge bootstrap components."""

from __future__ import annotations


class BridgeError(Exception):
    """An expected Bridge failure with a stable machine-readable code."""

    code = "STARTUP_BLOCKED"

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


class ConfigInvalid(BridgeError):
    code = "CONFIG_INVALID"


class PathInvalid(BridgeError):
    code = "PATH_INVALID"


class ToolNotFound(BridgeError):
    code = "TOOL_NOT_FOUND"


class ToolExecFailed(BridgeError):
    code = "TOOL_EXEC_FAILED"


class AuthUnavailable(BridgeError):
    code = "AUTH_UNAVAILABLE"


class DatabaseError(BridgeError):
    code = "DATABASE_ERROR"


class LockHeld(BridgeError):
    code = "LOCK_HELD"


class LockError(BridgeError):
    code = "LOCK_ERROR"


class StartupBlocked(BridgeError):
    code = "STARTUP_BLOCKED"


class TransportFailure(BridgeError):
    code = "POLL_FAILED"

    def __init__(self, message: str, *, status: str = "POLL_FAILED", reason: str | None = None):
        super().__init__(message)
        self.status = status
        self.reason = reason

    def as_dict(self) -> dict[str, str]:
        result = super().as_dict()
        result["status"] = self.status
        if self.reason:
            result["reason"] = self.reason
        return result


class DispatchInvalid(BridgeError):
    code = "DISPATCH_INVALID"


class ReplayBlocked(BridgeError):
    code = "REPLAY_BLOCKED"


class WorkspaceBlocked(BridgeError):
    code = "WORKSPACE_BLOCKED"
