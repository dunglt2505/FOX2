import copy
import hashlib
import json
from importlib.resources import files
import pytest
from pydantic import ValidationError
from fox2.contracts.market import MarketDataEnvelope
from fox2.contracts.health import ProcessHealth, SourceHealth
from fox2.contracts.instruments import InstrumentSearchResult
from fox2.contracts.watchlist import WatchlistPreference, WatchlistReplace
from fox2.validation.schema import MarketValidator

validator = MarketValidator()

def test_exact_published_schema():
    raw = files("fox2.contracts").joinpath("market_v0_4.schema.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == "821914afe00a7d17de2c9ec805982f72ecffb455dbeff781759db395bc57bd52"

@pytest.mark.parametrize("fixture,kind", [("quote_payload","quote"), ("bars_payload","bars"),
                                         ("unavailable_payload","quote")])
def test_market_families(request, fixture, kind):
    p = request.getfixturevalue(fixture)
    result = validator.validate_shape(p,kind)
    assert result.shape_passed, result.errors
    assert result.envelope.model_dump(mode="json",by_alias=True)["data"]["payload"] == p["data"]["payload"]

def test_index_family(quote_payload):
    o = quote_payload["data"]
    o.update(instrument_type="INDEX", price_unit="INDEX_POINTS")
    o["payload"] = dict(kind="index_summary", value=1000, change_value=-1, change_percent=-0.1,
                        up_count=1, down_count=2, unchanged_count=0, volume=0, turnover=0)
    assert validator.validate_shape(quote_payload,"index_summary").shape_passed

@pytest.mark.parametrize("field,value", [("contract_version","v0.4"), ("request_id",""),
    ("generated_at","invalid"), ("generated_at","2026-10-13T00:00:00"), ("data",[])])
def test_bad_envelope(quote_payload,field,value):
    quote_payload[field] = value
    assert not validator.validate_shape(quote_payload,"quote").shape_passed

@pytest.mark.parametrize("field", ["generated_at","request_id","data","contract_version"])
def test_required_envelope_fields(quote_payload,field):
    del quote_payload[field]
    assert not validator.validate_shape(quote_payload,"quote").shape_passed

@pytest.mark.parametrize("field", ["rights","source_revision","payload","first_available_at"])
def test_nullable_still_required(quote_payload,field):
    del quote_payload["data"][field]
    assert not validator.validate_shape(quote_payload,"quote").shape_passed

@pytest.mark.parametrize("value", [-1,"100",True,float("nan"),float("inf")])
def test_invalid_numeric_types(quote_payload,value):
    quote_payload["data"]["payload"]["last_price"] = value
    assert not validator.validate_shape(quote_payload,"quote").shape_passed

def test_extra_fields_and_kind(quote_payload):
    assert not validator.validate_shape(quote_payload,"bars").shape_passed
    quote_payload["data"]["arbitrary"] = "no"
    assert not validator.validate_shape(quote_payload,"quote").shape_passed

@pytest.mark.parametrize("patch", [dict(profile="INVESTOR"),dict(freshness_state="LIVE"),
    dict(price_basis="ADJUSTED"),dict(missing_fields=["x","x"])])
def test_published_conditionals(quote_payload,patch):
    quote_payload["data"].update(patch)
    assert not validator.validate_shape(quote_payload,"quote").shape_passed
    with pytest.raises(ValidationError):
        MarketDataEnvelope.model_validate_json(json.dumps(quote_payload))

def test_absent_observation_nulls(unavailable_payload):
    unavailable_payload["data"]["as_of"] = unavailable_payload["generated_at"]
    assert not validator.validate_shape(unavailable_payload,"quote").shape_passed

def test_nonmarket_families_are_separate():
    health = ProcessHealth(status="OK",provider_enabled=False)
    source = SourceHealth(capability="QUOTE",readiness="UNAVAILABLE",state="UNKNOWN",
        gap_state="UNKNOWN",rights_state="UNKNOWN",verified_until=None,reason="NOT_INTEGRATED")
    search = InstrumentSearchResult(items=[],universe_source=None,universe_revision=None,
                                    coverage="UNKNOWN",cursor=None)
    preference = WatchlistPreference(version=0,items=[],updated_at=None)
    for item in (health,source,search,preference):
        assert not validator.validate_shape(item.model_dump(mode="json"),"quote").shape_passed
    assert health.contract_version == "market-data-v0.4-candidate"
    assert preference.updated_at is None

@pytest.mark.parametrize("patch", [dict(version=-1),dict(items=["A","A"]),
    dict(items=[""]),dict(items=[str(n) for n in range(101)]),dict(version=True)])
def test_watchlist_invalid(patch):
    p = dict(version=0,items=[],updated_at=None); p.update(patch)
    with pytest.raises(ValidationError): WatchlistPreference.model_validate(p)

def test_replace_dto_and_verified_search_metadata():
    assert WatchlistReplace(expected_version=0,items=["TEST:A"]).items == ["TEST:A"]
    with pytest.raises(ValidationError): WatchlistReplace(expected_version=0,items=["A","A"])
    p = dict(items=[dict(instrument_id="TEST:A",symbol="A",instrument_type="STOCK",
             venue="HOSE",board_id="G1")],universe_source="isolated-test",universe_revision="1",
             coverage="PARTIAL",cursor=None)
    assert InstrumentSearchResult.model_validate(p).coverage == "PARTIAL"
