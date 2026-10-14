import asyncio
import json
import sqlite3
import pytest

from fox2.main import create_app
from fox2.runtime import OfflineRuntime


def test_watchlist_roundtrip_conflict_and_restart(configured, client_request):
    app, _, settings = configured
    assert client_request(app, '/api/watchlist').json() == {'version': 0, 'items': [], 'updated_at': None}
    body = {'expected_version': 0, 'items': ['TEST:AAA', 'TEST:BBB']}
    first = client_request(app, '/api/watchlist', method='PUT', json=body)
    assert first.status_code == 200 and first.json()['version'] == 1
    assert first.json()['items'] == body['items'] and first.json()['updated_at'].endswith('Z')
    conflict = client_request(app, '/api/watchlist', method='PUT', json={'expected_version': 0, 'items': []})
    assert conflict.status_code == 409 and conflict.json() == {'detail': 'Watchlist version conflict'}
    restarted = create_app(settings, runtime=OfflineRuntime(settings, registry=configured[1].registry))
    assert client_request(restarted, '/api/watchlist').json() == first.json()
    cleared = client_request(restarted, '/api/watchlist', method='PUT', json={'expected_version': 1, 'items': []})
    assert cleared.status_code == 200 and cleared.json()['version'] == 2


@pytest.mark.parametrize('body', [
    {'expected_version': 0, 'items': ['TEST:AAA', 'TEST:AAA']},
    {'expected_version': 0, 'items': ['TEST:UNKNOWN']},
    {'expected_version': 0, 'items': ['AAA']},
    {'expected_version': 0, 'items': ['TEST:' + str(i) for i in range(101)]},
    {'expected_version': -1, 'items': []}, {'expected_version': True, 'items': []},
    {'expected_version': '0', 'items': []}, {'expected_version': 0, 'items': [42]},
    {'expected_version': 0, 'items': ['']}, {'expected_version': 0, 'items': 'TEST:AAA'},
    {'expected_version': 0, 'items': [], 'private': 'TEST_SENTINEL_SECRET'}, {}, []])
def test_invalid_watchlist_preserves_prior(configured, client_request, body):
    app, _, _ = configured
    prior = client_request(app, '/api/watchlist').json()
    r = client_request(app, '/api/watchlist', method='PUT', json=body)
    assert r.status_code == 422 and 'TEST_SENTINEL_SECRET' not in r.text
    assert client_request(app, '/api/watchlist').json() == prior


def test_concurrent_http_cas_one_winner(configured, offline_runner):
    import httpx
    app = configured[0]
    async def run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app, client=('127.0.0.1', 1)),
                                    base_url='http://127.0.0.1') as client:
            responses = await asyncio.gather(*[
                client.put('/api/watchlist', json={'expected_version': 0, 'items': [item]})
                for item in ('TEST:AAA', 'TEST:BBB')])
            assert sorted(r.status_code for r in responses) == [200, 409]
            winner = next(r.json() for r in responses if r.status_code == 200)
            assert (await client.get('/api/watchlist')).json() == winner
    offline_runner(run())


@pytest.mark.parametrize('stage', ['preference_begin', 'preference_validated', 'preference_updated', 'preference_commit'])
def test_store_failure_rolls_back_http(configured, client_request, stage):
    app, runtime, _ = configured
    first = client_request(app, '/api/watchlist', method='PUT', json={'expected_version': 0, 'items': ['TEST:AAA']}).json()
    store = runtime.repository._open()
    def fail(point):
        if point == stage: raise sqlite3.OperationalError('TEST_SENTINEL_SECRET private licensed data')
    store.hook = fail
    r = client_request(app, '/api/watchlist', method='PUT', json={'expected_version': 1, 'items': ['TEST:BBB']})
    assert r.status_code == 503 and r.json() == {'detail': 'Service unavailable'}
    store.hook = lambda point: None
    assert client_request(app, '/api/watchlist').json() == first


@pytest.mark.parametrize('host,origin,peer,status', [
    ('127.0.0.1:8000', None, '127.0.0.1', 200),
    ('localhost:8000', 'http://localhost:8000', '127.0.0.1', 200),
    ('[::1]:8000', 'http://[::1]:8000', '::1', 200),
    ('evil.example', None, '127.0.0.1', 400),
    ('127.0.0.1:invalid', None, '127.0.0.1', 400),
    ('127.0.0.1:', None, '127.0.0.1', 400),
    ('secret@127.0.0.1:8000', None, '127.0.0.1', 400),
    ('127.0.0.1:8000/path', None, '127.0.0.1', 400),
    ('127.0.0.1:0', None, '127.0.0.1', 400),
    ('127.0.0.1:8000', None, '192.0.2.1', 403),
    ('127.0.0.1:8000', 'null', '127.0.0.1', 403),
    ('127.0.0.1:8000', '', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'https://127.0.0.1:8000', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'http://127.0.0.1:9000', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'http://127.0.0.1:8000/', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'http://secret@127.0.0.1:8000', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'http://127.0.0.1:8000/?private=secret', '127.0.0.1', 403),
    ('127.0.0.1:8000', 'http://127.0.0.1:invalid', '127.0.0.1', 403)])
def test_guards_protect_preference_mutation(configured, client_request, host, origin, peer, status):
    headers = {'host': host}
    if origin is not None: headers['origin'] = origin
    r = client_request(configured[0], '/api/watchlist', method='PUT', peer=peer,
                       headers=headers, json={'expected_version': 0, 'items': ['TEST:AAA']})
    assert r.status_code == status
    current = client_request(configured[0], '/api/watchlist').json()
    assert current['version'] == (1 if status == 200 else 0)


@pytest.mark.parametrize('headers,status', [
    ({'content-type': 'text/plain'}, 415), ({'content-type': 'application/x-www-form-urlencoded'}, 415),
    ({'content-type': 'application/json; charset=utf-8'}, 200),
    ([('content-type', 'application/json'), ('content-type', 'text/plain')], 415),
    ([('host', '127.0.0.1'), ('host', 'evil.example'), ('content-type', 'application/json')], 400),
    ([('origin', 'http://127.0.0.1:8000'), ('origin', 'null'), ('content-type', 'application/json')], 400)])
def test_header_and_content_type_guards(configured, client_request, headers, status):
    body = json.dumps({'expected_version': 0, 'items': []})
    assert client_request(configured[0], '/api/watchlist', method='PUT', headers=headers, content=body).status_code == status


def test_missing_content_type_malformed_and_oversize_body(configured, client_request):
    app = configured[0]
    for body, headers, code in [('{}', {}, 415), ('{"private":"TEST_SENTINEL_SECRET",',
            {'content-type': 'application/json'}, 422), ('X' * 65537, {'content-type': 'application/json'}, 413)]:
        r = client_request(app, '/api/watchlist', method='PUT', content=body, headers=headers)
        assert r.status_code == code and 'TEST_SENTINEL_SECRET' not in r.text
    assert client_request(app, '/api/watchlist').json()['version'] == 0


def test_unexpected_failure_sanitized(configured, client_request):
    app, runtime, _ = configured
    def fail(*args): raise RuntimeError('TEST_SENTINEL_SECRET account=private filesystem_path=hidden')
    runtime.repository.get_preferences = fail
    r = client_request(app, '/api/watchlist')
    assert r.status_code == 503 and r.json() == {'detail': 'Service unavailable'}


def test_exactly_100_verified_preferences_accepted(tmp_path, client_request):
    from fox2.application.registry import InstrumentRegistry
    from fox2.contracts.instruments import Instrument
    from fox2.config import Settings
    registry = InstrumentRegistry([Instrument(instrument_id=f'TEST:{i}', symbol=f'S{i}',
        instrument_type='STOCK', venue='HOSE', board_id='G1') for i in range(100)],
        source='ISOLATED_TEST_UNIVERSE', revision='100-v1', coverage='PARTIAL')
    settings = Settings(store_root=str(tmp_path / 'fox2-max100'))
    app = create_app(settings, runtime=OfflineRuntime(settings, registry=registry))
    items = [f'TEST:{i}' for i in range(100)]
    r = client_request(app, '/api/watchlist', method='PUT', json={'expected_version': 0, 'items': items})
    assert r.status_code == 200 and r.json()['items'] == items
    assert client_request(app, '/api/watchlist').json() == r.json()
