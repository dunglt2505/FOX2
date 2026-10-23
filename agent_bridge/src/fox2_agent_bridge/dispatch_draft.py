"""Only for NEW, unpublished Dispatch v3 JSON drafts.

Select BRIDGE explicitly by default, preserve an already selected AGENT owner.
Never modify/normalize a locked historical dispatch or publish to Git here.
"""
from __future__ import annotations

from copy import deepcopy

from .dispatch_schema_v3_contract import DISPATCH_SCHEMA_V3
from .errors import DispatchInvalid
from .project_dictionary import CURRENT_DISPATCH_SCHEMA, IDENTIFIERS
from .schema_validation import validate_json_schema


def prepare_new_dispatch_draft(payload: dict, *,
                               delivery_owner: str = "BRIDGE") -> dict:
    if not isinstance(payload, dict):
        raise DispatchInvalid("new Dispatch draft must be an object")
    if payload.get("schema_version") != CURRENT_DISPATCH_SCHEMA:
        raise DispatchInvalid("new default applies only to current v3 drafts")
    if delivery_owner not in IDENTIFIERS["delivery_owners"]:
        raise DispatchInvalid("delivery owner must be AGENT or BRIDGE")
    if payload.get("delivery_owner") not in (None, delivery_owner):
        raise DispatchInvalid("existing immutable delivery owner cannot be rebound")
    if any(key.startswith("_") for key in payload):
        raise DispatchInvalid("normalized or runtime Dispatch is not a new draft")
    prepared = deepcopy(payload)
    prepared["delivery_owner"] = delivery_owner
    validate_json_schema(prepared, DISPATCH_SCHEMA_V3)
    return prepared
