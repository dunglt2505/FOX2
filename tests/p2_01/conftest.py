"""Offline harness: runtime never imports these fixtures."""
import copy
import asyncio
from pathlib import Path
import socket
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "backend" / "src"))

@pytest.fixture(scope="session")
def offline_runner():
    # Windows asyncio creates an internal loopback socketpair for wakeups.
    # Initialize harness before network denial/application imports, then deny
    # all connect/bind/DNS operations throughout application lifespan/requests.
    loop = asyncio.new_event_loop()
    yield loop.run_until_complete
    loop.close()

@pytest.fixture(autouse=True)
def deny_network(monkeypatch, offline_runner):
    attempts = []
    def denied(*args, **kwargs):
        attempts.append("NETWORK_ATTEMPT")
        raise AssertionError("Network disabled in P2-01")
    for name in ("connect", "connect_ex", "bind", "listen", "sendto"):
        monkeypatch.setattr(socket.socket, name, denied)
    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket, "getaddrinfo", denied)
    yield attempts
    assert attempts == [], "Unexpected socket/DNS activity"

@pytest.fixture
def quote_payload():
    return {
        "contract_version": "market-data-v0.4-candidate", "request_id": "test-request",
        "generated_at": "2026-10-13T03:00:00Z", "data": {
            "profile": "ISOLATED_TEST", "instrument_id": "TEST:AAA", "symbol": "AAA",
            "instrument_type": "STOCK", "venue": "HOSE", "board_id": "G1",
            "record_id": "test-observation", "revision": 0, "source_id": "isolated-test",
            "origin_provider": "ISOLATED_TEST", "source_revision": None,
            "retrieval_channel": "TEST_FIXTURE", "event_at": "2026-10-13T02:00:00Z",
            "as_of": "2026-10-13T02:00:00Z", "received_at": "2026-10-13T02:00:01Z",
            "first_available_at": "2026-10-13T02:00:01Z", "data_mode": "SYNTHETIC",
            "freshness_state": "LATEST_VALID", "quality": "VALID", "mapping_state": "VERIFIED",
            "completeness": "PARTIAL", "price_basis": "RAW", "price_unit": "VND_PER_SHARE",
            "volume_unit": "SHARES", "turnover_unit": "VND", "adjustment_version": None,
            "calendar_version": None, "session": None, "freshness_policy_version": None,
            "rights": {"read": "UNKNOWN", "redisplay": "UNKNOWN", "retained_use": "UNKNOWN",
                       "evidence_ref": None, "verified_until": None},
            "selection_audit_id": "test-selection", "selection_reason": "ISOLATED_TEST_ONLY",
            "missing_fields": [], "payload": {"kind": "quote", "last_price": 100,
                "reference_price": 100, "ceiling_price": 107, "floor_price": 93,
                "cumulative_volume": 0, "cumulative_turnover": 0}}}

@pytest.fixture
def unavailable_payload(quote_payload):
    p = copy.deepcopy(quote_payload)
    o = p["data"]
    o.update(profile="INVESTOR", data_mode="UNAVAILABLE", retrieval_channel="UNAVAILABLE",
             freshness_state="UNAVAILABLE", payload=None, quality="UNKNOWN",
             mapping_state="UNKNOWN", selection_reason="NOT_INTEGRATED")
    for k in ("source_id", "record_id", "revision", "event_at", "as_of", "received_at", "first_available_at"):
        o[k] = None
    return p

@pytest.fixture
def bars_payload(quote_payload):
    p = copy.deepcopy(quote_payload)
    p["data"]["payload"] = {"kind": "bars", "timeframe": "1D", "from": "2026-10-12T00:00:00Z",
        "to": "2026-10-14T00:00:00Z", "items": [{"start_at": "2026-10-12T02:00:00Z",
        "end_at": "2026-10-12T08:00:00Z", "update_at": "2026-10-12T08:00:01Z",
        "open": 100, "high": 110, "low": 90, "close": 105, "volume": 0,
        "turnover": None, "provisional": False, "revision": 0}], "gaps": []}
    return p
