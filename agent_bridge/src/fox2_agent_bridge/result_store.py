"""Atomic runtime JSON reports for FOX2 Bridge executions."""

from __future__ import annotations

import json
import re
from pathlib import Path

from .errors import DatabaseError
from .logging_config import redact_context

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
    temporary = directory / f".{dispatch_id}.json.tmp"
    try:
        directory.mkdir(parents=True, exist_ok=True)
        temporary.write_text(
            json.dumps(redact_context(payload), ensure_ascii=True, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        temporary.replace(path)
        return path
    except OSError as exc:
        raise DatabaseError(f"cannot write execution report: {exc}") from exc
