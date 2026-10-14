"""Minimal fail-closed JSON Schema validation used for the bound Dispatch v3 contract."""

from __future__ import annotations

from datetime import datetime
import json
import re
from typing import Any

from .errors import DispatchInvalid


def _matches_type(value: object, expected: str) -> bool:
    return {
        "object": lambda: isinstance(value, dict),
        "array": lambda: isinstance(value, list),
        "string": lambda: isinstance(value, str),
        "boolean": lambda: type(value) is bool,
        "null": lambda: value is None,
        "integer": lambda: type(value) is int,
        "number": lambda: type(value) in (int, float),
    }.get(expected, lambda: False)()


def _fail(path: str, message: str) -> None:
    raise DispatchInvalid(f"{path}: {message}")


def _validate_datetime(value: str, path: str) -> None:
    if "T" not in value:
        _fail(path, "must be RFC3339 date-time")
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise DispatchInvalid(f"{path}: must be RFC3339 date-time") from exc
    if parsed.tzinfo is None:
        _fail(path, "date-time must include UTC/offset timezone")


def validate_json_schema(value: Any, schema: dict[str, Any], *, path: str = "dispatch") -> None:
    """Validate the JSON-Schema subset used by FOX2 Dispatch v3.

    The schema itself is generated from the canonical repository source. This function
    intentionally supports only the keywords present in that contract and fails if an
    unsupported structural keyword is introduced, so schema evolution cannot silently
    outrun runtime validation.
    """

    supported = {
        "$schema", "$id", "title", "type", "additionalProperties", "required",
        "properties", "const", "pattern", "minLength", "maxLength", "enum",
        "items", "uniqueItems", "format",
    }
    unknown = set(schema) - supported
    if unknown:
        _fail(path, f"runtime validator does not support schema keyword(s): {sorted(unknown)}")

    expected_type = schema.get("type")
    if expected_type is not None:
        choices = [expected_type] if isinstance(expected_type, str) else expected_type
        if not isinstance(choices, list) or not choices or not all(isinstance(item, str) for item in choices):
            _fail(path, "schema type declaration is invalid")
        if not any(_matches_type(value, item) for item in choices):
            _fail(path, f"type mismatch; expected {choices}")

    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        _fail(path, f"must equal {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        _fail(path, f"must be one of {schema['enum']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            _fail(path, "string is shorter than minLength")
        if "maxLength" in schema and len(value) > int(schema["maxLength"]):
            _fail(path, "string is longer than maxLength")
        if "pattern" in schema and re.search(str(schema["pattern"]), value) is None:
            _fail(path, "string does not match required pattern")
        if schema.get("format") == "date-time":
            _validate_datetime(value, path)
        elif "format" in schema:
            _fail(path, f"unsupported string format {schema['format']!r}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
            _fail(path, "schema required declaration is invalid")
        missing = [item for item in required if item not in value]
        if missing:
            _fail(path, f"missing required field(s): {missing}")

        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            _fail(path, "schema properties declaration is invalid")
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                _fail(path, f"unexpected field(s): {extra}")

        for key, item in value.items():
            subschema = properties.get(key)
            if subschema is not None:
                validate_json_schema(item, subschema, path=f"{path}.{key}")

    if isinstance(value, list):
        if schema.get("uniqueItems") is True:
            encoded = [json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False) for item in value]
            if len(encoded) != len(set(encoded)):
                _fail(path, "array items must be unique")
        if "items" in schema:
            item_schema = schema["items"]
            if not isinstance(item_schema, dict):
                _fail(path, "schema items declaration is invalid")
            for index, item in enumerate(value):
                validate_json_schema(item, item_schema, path=f"{path}[{index}]")
