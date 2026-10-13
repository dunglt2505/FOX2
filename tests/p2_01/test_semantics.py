from datetime import datetime, timezone, timedelta
from dataclasses import replace
import pytest
from fox2.validation.schema import MarketValidator
from fox2.validation.semantics import CapabilityContext

v = MarketValidator()
CTX = CapabilityContext("QUOTE",datetime(2026,10,13,3,tzinfo=timezone.utc))

def verdict(payload,kind="quote",context=CTX):
    shape = v.validate_shape(payload,kind)
    assert shape.shape_passed, shape.errors
    return v.validate_semantics(shape.envelope.data,context)

def test_shape_pass_is_not_semantic_pass(quote_payload):
    quote_payload["data"]["payload"]["last_price"] = 0
    assert verdict(quote_payload).status == "FAIL"
    assert "NONPOSITIVE_PRICE:last_price" in verdict(quote_payload).errors

def test_valid_isolated_quote_and_missing_zero(quote_payload):
    assert verdict(quote_payload).status == "PASS"
    p = quote_payload["data"]["payload"]
    assert p["cumulative_volume"] == 0
    p["cumulative_turnover"] = None
    quote_payload["data"]["missing_fields"] = ["payload.cumulative_turnover"]
    result = verdict(quote_payload)
    assert result.status == "PARTIAL"
    assert "MISSING:payload.cumulative_volume" not in result.unknowns
    assert v.validate_shape(quote_payload,"quote").envelope.data.payload.cumulative_turnover is None

def test_missing_not_declared(quote_payload):
    quote_payload["data"]["payload"]["cumulative_volume"] = None
    assert "UNDECLARED_MISSING:payload.cumulative_volume" in verdict(quote_payload).errors

def test_unavailable_no_generated_at_substitution(unavailable_payload):
    assert verdict(unavailable_payload).status == "PASS"
    assert v.validate_shape(unavailable_payload,"quote").envelope.data.as_of is None
    unavailable_payload["generated_at"] = "2040-01-01T00:00:00Z"
    assert verdict(unavailable_payload).status == "PASS"

@pytest.mark.parametrize("field,value,reason", [
    ("event_at","2026-10-13T02:00:02Z","TIME_AFTER_RECEIPT:event_at"),
    ("as_of","2026-10-13T01:00:00Z","EVENT_AFTER_AS_OF"),
    ("first_available_at","2026-10-13T02:00:00Z","AVAILABILITY_BEFORE_RECEIPT"),
    ("first_available_at","2026-10-14T02:00:00Z","AVAILABILITY_IN_FUTURE"),
    ("event_at","2026-10-13T09:00:00+07:00","NON_UTC:event_at")])
def test_observation_time_order(quote_payload,field,value,reason):
    quote_payload["data"][field] = value
    quote_payload["generated_at"] = "2040-01-01T00:00:00Z"
    assert reason in verdict(quote_payload).errors

@pytest.mark.parametrize("patch,reason", [(dict(high=99),"OHLC_HIGH"),
    (dict(low=101),"OHLC_LOW"),(dict(end_at="2026-10-12T01:00:00Z"),"BAR_INTERVAL"),
    (dict(update_at="2026-10-12T01:00:00Z"),"BAR_UPDATE_BEFORE_START"),
    (dict(end_at=None),"CLOSED_BAR_WITHOUT_END")])
def test_bar_negatives(bars_payload,patch,reason):
    bars_payload["data"]["payload"]["items"][0].update(patch)
    result = verdict(bars_payload,"bars",replace(CTX,capability="BARS",session_mapping_verified=True))
    assert reason in result.errors

def test_bar_zero_null_and_unknown_end(bars_payload):
    ctx = replace(CTX,capability="BARS",session_mapping_verified=True)
    result = verdict(bars_payload,"bars",ctx)
    assert result.status == "PARTIAL"
    assert result.unknowns == ("MISSING:bar.turnover",)
    bar = bars_payload["data"]["payload"]["items"][0]
    bar.update(end_at=None,provisional=True)
    assert "UNKNOWN_BAR_END" in verdict(bars_payload,"bars",ctx).unknowns

def test_closed_bar_requires_calendar(bars_payload):
    assert "SESSION_MAPPING_UNVERIFIED" in verdict(bars_payload,"bars",replace(CTX,capability="BARS")).errors

def test_gap_and_window(bars_payload):
    bars_payload["data"]["payload"]["gaps"] = [{"from":"2026-10-12T01:00:00Z",
        "to":"2026-10-12T00:00:00Z","reason":"test-gap","capability":"BARS"}]
    assert "GAP_INTERVAL" in verdict(bars_payload,"bars",replace(CTX,capability="BARS")).errors

def provider(o):
    # Simulated provider metadata exists only inside the isolated test harness.
    o.update(profile="INVESTOR",data_mode="VERIFIED_PROVIDER",retrieval_channel="WEBSOCKET")
    o["rights"].update(read="VERIFIED",redisplay="VERIFIED",retained_use="VERIFIED",
                      evidence_ref="test-evidence",verified_until="2026-10-14T00:00:00Z")

def test_rights_and_expiry(quote_payload):
    o = quote_payload["data"]; provider(o)
    assert verdict(quote_payload).status == "PASS"
    o["rights"]["verified_until"] = "2026-10-13T03:00:00Z"
    assert "RIGHTS_EXPIRED" in verdict(quote_payload).errors
    o["rights"]["redisplay"] = "UNKNOWN"
    assert "RIGHTS:redisplay" in verdict(quote_payload).errors

def test_retained_use(quote_payload):
    o = quote_payload["data"]; provider(o)
    o["retrieval_channel"] = "LOCAL_STORE"; o["rights"]["retained_use"] = "BLOCKED"
    assert "RIGHTS:retained_use" in verdict(quote_payload).errors

def test_live_requires_actual_context(quote_payload):
    o=quote_payload["data"]; provider(o)
    o.update(freshness_state="LIVE",completeness="COMPLETE",calendar_version="test-calendar",
             session="test-session",freshness_policy_version="test-policy")
    assert verdict(quote_payload).status == "FAIL"
    ctx=replace(CTX,transport_verified=True,subscriptions_verified=True,session_mapping_verified=True,
                coverage_verified=True,relevant_gap=False,freshness_budget=timedelta(hours=2))
    assert verdict(quote_payload,context=ctx).status == "PASS"
    assert "LIVE_STALE" in verdict(quote_payload,context=replace(ctx,freshness_budget=timedelta(seconds=1))).errors
    o["price_unit"]="UNKNOWN"
    assert not v.validate_shape(quote_payload,"quote").shape_passed

def test_unit_basis_native_and_capability(quote_payload):
    o=quote_payload["data"]; o["price_unit"]="INDEX_POINTS"
    assert "QUOTE_UNIT" in verdict(quote_payload).errors
    o["price_unit"]="UNKNOWN"
    assert verdict(quote_payload).status == "PARTIAL"
    o.update(price_basis="ADJUSTED",adjustment_version="test-adjustment")
    assert "ADJUSTMENT_UNVERIFIED" in verdict(quote_payload).errors
    assert "CAPABILITY_MISMATCH" in verdict(quote_payload,context=replace(CTX,capability="INDEX")).errors
    o.update(data_mode="PROVIDER_NATIVE_UNVERIFIED",mapping_state="UNKNOWN",quality="PARTIAL")
    o["rights"].update(read="VERIFIED",redisplay="VERIFIED",evidence_ref="test-evidence",
                      verified_until="2026-10-14T00:00:00Z")
    assert "NATIVE_ANALYSIS_FORBIDDEN" in verdict(quote_payload,context=replace(CTX,use_context="ANALYSIS")).errors

def test_context_requires_utc():
    with pytest.raises(ValueError): CapabilityContext("QUOTE",datetime(2026,10,13))

def test_verified_provider_cannot_claim_unknown_mapping(quote_payload):
    o=quote_payload["data"]; provider(o)
    o["mapping_state"]="UNKNOWN"
    assert "VERIFIED_PROVIDER_MAPPING" in verdict(quote_payload).errors
    o["price_basis"]="UNKNOWN"
    assert "VERIFIED_PROVIDER_UNITS_BASIS" in verdict(quote_payload).errors
