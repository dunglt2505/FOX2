"""Structured JSON file logging with key-based secret redaction."""

from __future__ import annotations

import json
import logging
import re
from datetime import UTC, datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

SECRET_KEY_PARTS = ("TOKEN", "SECRET", "PASSWORD", "API_KEY", "AUTHORIZATION")
SECRET_VALUE_PATTERNS = (
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
    re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"(?i)\bBearer\s+\S+"),
    re.compile(
        r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?"
        r"-----END [A-Z0-9 ]*PRIVATE KEY-----",
        re.DOTALL,
    ),
)


def _redact_string(value: str) -> str:
    for pattern in SECRET_VALUE_PATTERNS:
        value = pattern.sub("<REDACTED>", value)
    return value


def redact_context(value: Any, key: str = "") -> Any:
    upper_key = key.upper()
    if any(part in upper_key for part in SECRET_KEY_PARTS):
        return "<REDACTED>"
    if isinstance(value, dict):
        return {str(child_key): redact_context(child, str(child_key)) for child_key, child in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact_context(child, key) for child in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, str):
        return _redact_string(value)
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    return str(value)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "component": _redact_string(getattr(record, "component", "bridge")),
            "event": _redact_string(getattr(record, "event", record.getMessage())),
            "context": redact_context(getattr(record, "context", {})),
        }
        return json.dumps(payload, ensure_ascii=True, sort_keys=True)


def configure_logging(log_directory: Path) -> logging.Logger:
    log_directory.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("fox2_agent_bridge")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in tuple(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    handler = RotatingFileHandler(
        log_directory / "bridge.log",
        maxBytes=2_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(JsonFormatter())
    logger.addHandler(handler)
    return logger


def log_event(
    logger: logging.Logger,
    *,
    component: str,
    event: str,
    context: dict[str, Any] | None = None,
) -> None:
    logger.info(
        event,
        extra={
            "component": component,
            "event": event,
            "context": redact_context(context or {}),
        },
    )
