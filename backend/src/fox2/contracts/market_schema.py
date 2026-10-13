"""Local published schema. No resolver, download or provider construction."""
import json
from importlib.resources import files
from jsonschema import Draft202012Validator, FormatChecker

_SCHEMA = json.loads(files("fox2.contracts").joinpath("market_v0_4.schema.json").read_bytes())
_VALIDATOR = Draft202012Validator(_SCHEMA, format_checker=FormatChecker())

def shape_errors(payload: object) -> tuple[str, ...]:
    # Do not expose values, raw errors or credentials from caller payloads.
    return tuple(sorted({"SHAPE:" + "/".join(str(p) for p in error.absolute_path)
                         for error in _VALIDATOR.iter_errors(payload)}))
