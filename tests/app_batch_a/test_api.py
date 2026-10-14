from datetime import timedelta
from dataclasses import asdict
import json
import pytest

from fox2.config import Settings
from fox2.contracts.market import MarketDataEnvelope, IndexSummary
from fox2.main import create_app
from fox2.runtime import OfflineRuntime
from fox2.store import SQLiteStore
from fox2.dsm import CapabilityPolicy


def policy(capability):
    return CapabilityPolicy(capability, timedelta(minutes=10), 'offline-v1', 'isolated-calendar',
                            'REGULAR', mapping_verified=True, session_mapping_verified=True,
                            coverage_verified=True, relevant_gap=False)


WINDOW = '?from=2026-10-13T00:00:00Z&to=2026-10-14T00:00:00Z'


def test_exact_route_allowlist():
    routes = {(r.path, frozenset(r.methods)) for r in create_app().routes}
    assert routes == {(p, frozenset({m})) for p, m in [
        ('/api/health', 'GET'), ('/api/data-sources/health', 'GET'), ('/api/market/overview', 'GET'),
        ('/api/stocks', 'GET'), ('/api/stocks/{symbol}', 'GET'), ('/api/stocks/{symbol}/bars', 'GET'),
        ('/api/watchlist', 'GET'), ('/api/watchlist', 'PUT')]}


def test_default_no_metadata_no_store_no_values(client_request, no_network):
    app = create_app()
    assert client_request(app, '/api/health').json()['provider_enabled'] is False
    assert client_request(app, '/api/stocks').json() == dict(items=[], universe_source=None,
        universe_revision=None, coverage='UNKNOWN', cursor=None)
    assert client_request(app, '/api/market/overview').json() == []
    assert client_request(app, '/api/stocks/AAA').status_code == 404
    assert client_request(app, '/api/watchlist').status_code == 503
    sources = client_request(app, '/api/data-sources/health').json()
    assert len(sources) == 3 and all(s['state'] == 'UNKNOWN' and s['readiness'] == 'UNAVAILABLE' for s in sources)
    assert no_network == []


def test_configured_empty_store_unavailable_envelopes(configured, client_request):
    app, runtime, _ = configured
    for path in ('/api/stocks/AAA', '/api/stocks/AAA/bars' + WINDOW, '/api/market/overview?symbols=IDX'):
        response = client_request(app, path)
        assert response.status_code == 200
        value = response.json()
        envelope = value['quote'] if isinstance(value, dict) and 'quote' in value else value[0] if isinstance(value, list) else value
        dto = MarketDataEnvelope.model_validate_json(json.dumps(envelope))
        assert dto.data.payload is None and dto.data.data_mode == 'UNAVAILABLE'
        assert dto.data.selection_reason == 'NOT_FOUND'
        for name in ('source_id', 'record_id', 'revision', 'event_at', 'as_of', 'received_at', 'first_available_at', 'origin_provider'):
            assert getattr(dto.data, name) is None
        assert dto.data.rights.read == 'UNKNOWN'
    assert len(runtime.selection_audits) == 3
    assert all(not a.accepted for a in runtime.selection_audits)


def test_search_pagination_and_provenance(configured, client_request):
    app, _, _ = configured
    first = client_request(app, '/api/stocks?limit=1').json()
    assert first['items'][0]['symbol'] == 'AAA' and first['coverage'] == 'PARTIAL'
    assert first['universe_source'] == 'ISOLATED_TEST_UNIVERSE'
    second = client_request(app, '/api/stocks?limit=1&cursor=' + first['cursor']).json()
    assert second['items'][0]['symbol'] == 'BBB' and second['cursor'] is None
    assert client_request(app, '/api/stocks?query=B&cursor=' + first['cursor']).status_code == 422
    assert client_request(app, '/api/stocks?query=NOPE').json()['items'] == []


@pytest.mark.parametrize('suffix', [
    '?limit=0', '?limit=101', '?limit=true', '?query=' + 'X' * 33,
    '?cursor=private-secret', '?query=%00', '?limit=1&limit=2', '?provider=true'])
def test_invalid_search(configured, client_request, suffix):
    r = client_request(configured[0], '/api/stocks' + suffix)
    assert r.status_code == 422 and r.json() == {'detail': 'Invalid request'}


@pytest.mark.parametrize('suffix', ['', '?from=2026-10-13&to=2026-10-14',
    '?from=2026-10-13T00:00:00&to=2026-10-14T00:00:00',
    '?from=2026-10-13T00:00:00%2B07:00&to=2026-10-14T00:00:00%2B07:00',
    '?from=2026-10-14T00:00:00Z&to=2026-10-13T00:00:00Z',
    '?from=2025-01-01T00:00:00Z&to=2026-10-14T00:00:00Z',
    '?from=2026-10-13T00:00:00Z&to=2026-10-13T01:00:00Z',
    WINDOW + '&timeframe=1m', WINDOW + '&basis=private-secret', WINDOW + '&broker=true'])
def test_invalid_bars(configured, client_request, suffix):
    assert client_request(configured[0], '/api/stocks/AAA/bars' + suffix).status_code == 422


@pytest.mark.parametrize('path,status', [('/api/stocks/ZZZ', 404), ('/api/stocks/aaa', 422),
    ('/api/stocks/IDX', 404), ('/api/market/overview?symbols=AAA', 404),
    ('/api/market/overview?symbols=IDX&symbols=IDX', 422), ('/api/account', 404),
    ('/api/orders', 404), ('/api/broker', 404)])
def test_unknown_invalid_and_private_paths(configured, client_request, path, status):
    assert client_request(configured[0], path).status_code == status


def investor_store(h, registry):
    # Isolated test claims simulate the accepted provider DTO path; never real licensed data.
    return SQLiteStore(h.root / 'fox2-investor-protocol-test', profile='INVESTOR',
                       instrument_registry=registry.contains, clock=lambda: h.now, evidence=h.proof)


def investor_candidate(h, **changes):
    return h.observation(profile='INVESTOR', data_mode='VERIFIED_PROVIDER',
                         retrieval_channel='HISTORICAL_API', origin_provider='TEST_PROTOCOL_ONLY',
                         freshness_policy_version='offline-v1', **changes)


def test_real_sqlite_dsm_quote_zero_null_rights_and_freshness(h, registry, client_request):
    store = investor_store(h, registry)
    o = investor_candidate(h)
    o = o.model_copy(update={'payload': o.payload.model_copy(update={
        'cumulative_volume': 0., 'cumulative_turnover': None}), 'missing_fields': ['payload.cumulative_turnover']})
    h.store = store
    assert h.ingest(o).promoted
    runtime = OfflineRuntime(Settings(), registry=registry, repository=store,
                             policies={'QUOTE': policy('QUOTE')}, clock=lambda: h.now)
    app = create_app(runtime=runtime)
    r = client_request(app, '/api/stocks/AAA').json()['quote']['data']
    assert r['payload']['last_price'] == 100. and r['payload']['cumulative_volume'] == 0.
    assert r['payload']['cumulative_turnover'] is None
    assert r['retrieval_channel'] == 'LOCAL_STORE' and r['origin_provider'] == 'TEST_PROTOCOL_ONLY'
    assert r['as_of'] != client_request(app, '/api/stocks/AAA').json()['quote']['generated_at']
    assert client_request(app, '/api/stocks/AAA/bars' + WINDOW).json()['data']['payload'] is None
    h.now += timedelta(minutes=11)
    assert client_request(app, '/api/stocks/AAA').json()['quote']['data']['selection_reason'] == 'UNKNOWN'
    h.now -= timedelta(minutes=11)
    import sqlite3
    with sqlite3.connect(store.path) as c:
        key = c.execute('SELECT series_key FROM series').fetchone()[0]
    store.revoke_rights(key, 'test-revocation')
    assert client_request(app, '/api/stocks/AAA').json()['quote']['data']['selection_reason'] == 'RIGHTS_BLOCKED'
    assert all('last_price' not in json.dumps(asdict(a), default=str) for a in runtime.selection_audits)


@pytest.mark.parametrize('change', ['synthetic', 'fixture', 'mapping', 'rights', 'calendar', 'stale', 'policy'])
def test_investor_rejects_insufficient_evidence(h, registry, client_request, change):
    o = investor_candidate(h, first_available_at=h.now)
    if change == 'synthetic': o = o.model_copy(update={'data_mode': 'SYNTHETIC'})
    if change == 'fixture': o = o.model_copy(update={'retrieval_channel': 'TEST_FIXTURE'})
    if change == 'mapping': o = o.model_copy(update={'mapping_state': 'UNKNOWN'})
    if change == 'rights': o = o.model_copy(update={'rights': o.rights.model_copy(update={'redisplay': 'UNKNOWN'})})
    if change == 'calendar': o = o.model_copy(update={'calendar_version': None})
    if change == 'stale': o = o.model_copy(update={'as_of': h.now - timedelta(days=1), 'event_at': h.now - timedelta(days=1)})
    class Memory:
        def get_observation(self, *args): return o
    runtime = OfflineRuntime(Settings(), registry=registry, repository=Memory(),
        policies={} if change == 'policy' else {'QUOTE': policy('QUOTE')}, clock=lambda: h.now)
    r = client_request(create_app(runtime=runtime), '/api/stocks/AAA')
    assert r.status_code == 200 and r.json()['quote']['data']['payload'] is None


def test_bars_and_index_capability_paths(h, registry, client_request):
    store = investor_store(h, registry)
    h.store = store
    bars = investor_candidate(h, bars=True, provisional=False)
    assert h.ingest(bars).promoted
    index = investor_candidate(h, instrument_id='TEST:IDX', symbol='IDX', instrument_type='INDEX',
        price_basis='NOT_APPLICABLE', price_unit='INDEX_POINTS', volume_unit='NOT_APPLICABLE', turnover_unit='NOT_APPLICABLE')
    index = index.model_copy(update={'payload': IndexSummary(kind='index_summary', value=1000., change_value=None,
        change_percent=None, up_count=None, down_count=None, unchanged_count=None, volume=None, turnover=None),
        'missing_fields': ['payload.' + f for f in ('change_value', 'change_percent', 'up_count', 'down_count', 'unchanged_count', 'volume', 'turnover')]})
    assert h.ingest(index).promoted
    runtime = OfflineRuntime(Settings(), registry=registry, repository=store,
        policies={c: policy(c) for c in ('QUOTE', 'BARS', 'INDEX')}, clock=lambda: h.now)
    app = create_app(runtime=runtime)
    result = client_request(app, '/api/stocks/AAA/bars' + WINDOW)
    assert result.status_code == 200 and result.json()['data']['payload']['kind'] == 'bars'
    for extra in ('&basis=ADJUSTED', '&basis=UNKNOWN'):
        assert client_request(app, '/api/stocks/AAA/bars' + WINDOW + extra).json()['data']['payload'] is None
    assert client_request(app, '/api/stocks/AAA').json()['quote']['data']['payload'] is None
    idx = client_request(app, '/api/market/overview?symbols=IDX').json()[0]['data']
    assert idx['payload']['kind'] == 'index_summary' and idx['payload']['value'] == 1000.
    assert idx['payload']['volume'] is None


def test_unsafe_root_is_sanitized(tmp_path, registry, client_request):
    for root in ('relative', str(tmp_path / 'not-fox2'), str(__import__('pathlib').Path.cwd() / 'fox2-illegal')):
        settings = Settings(store_root=root)
        runtime = OfflineRuntime(settings, registry=registry)
        app = create_app(settings, runtime=runtime)
        for path in ('/api/stocks/AAA', '/api/watchlist'):
            response = client_request(app, path)
            assert response.status_code == 503 and response.json() == {'detail': 'Service unavailable'}
            assert root not in response.text


def test_bar_range_outside_available_window(h, registry, client_request):
    h.store = investor_store(h, registry)
    assert h.ingest(investor_candidate(h, bars=True, provisional=False)).promoted
    runtime = OfflineRuntime(Settings(), registry=registry, repository=h.store,
        policies={'BARS': policy('BARS')}, clock=lambda: h.now)
    app = create_app(runtime=runtime)
    response = client_request(app, '/api/stocks/AAA/bars?from=2026-10-01T00:00:00Z&to=2026-10-14T00:00:00Z')
    assert response.status_code == 200
    assert response.json()['data']['payload'] is None
    assert response.json()['data']['selection_reason'] == 'BARS_COVERAGE_UNKNOWN'


def test_corrupt_store_read_is_sanitized(configured, client_request):
    app, runtime, _ = configured
    store = runtime.repository._open()
    store.path.write_bytes(b'not a SQLite database TEST_SENTINEL_SECRET')
    for path in ('/api/watchlist', '/api/stocks/AAA', '/api/stocks/AAA/bars' + WINDOW,
                 '/api/market/overview?symbols=IDX'):
        response = client_request(app, path)
        assert response.status_code == 503 and response.json() == {'detail': 'Service unavailable'}


def test_registry_rejects_unverified_or_ambiguous_metadata(registry):
    from fox2.application.registry import InstrumentRegistry
    item = registry.resolve('AAA')
    with pytest.raises(ValueError): InstrumentRegistry([item])
    with pytest.raises(ValueError):
        InstrumentRegistry([item, item], source='ISOLATED_TEST', revision='v1', coverage='PARTIAL')
