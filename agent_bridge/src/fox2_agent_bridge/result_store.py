"""Atomic runtime JSON reports for FOX2 Bridge executions."""

from __future__ import annotations

import re
from pathlib import Path

from .errors import DatabaseError
from .logging_config import redact_context
from .artifacts import write_json

_SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")


def write_execution_report(
    *,
    bridge_root: Path,
    dispatch_id: str,
    payload: dict[str, object],
) -> Path:
    if not _SAFE_ID.fullmatch(dispatch_id):
        raise DatabaseError("dispatch_id is unsafe for runtime report filename")
    directory = bridge_root / "data" / "results"
    path = directory / f"{dispatch_id}.json"
    try:
        return write_json(path, redact_context(payload))
    except OSError as exc:
        raise DatabaseError(f"cannot write execution report: {exc}") from exc
