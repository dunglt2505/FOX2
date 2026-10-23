"""Real loopback HTTP checks; launches only owned test ASGI children.

Prerequisite: Vite at 127.0.0.1:5173. Test SQLite lives outside Git and is kept
for inspection. Any critical Origin-guard failure stops execution immediately.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import http.client
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
CHILD = ROOT / 'tests/app_batch_b/local_test_backend.py'


def request(path, *, port=8000, method='GET', body=None, headers=None):
    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
    data = None if body is None else json.dumps(body)
    fields = {'Accept': 'application/json'}
    if body is not None:
        fields['Content-Type'] = 'application/json'
    fields.update(headers or {})
    try:
        connection.request(method, path, body=data, headers=fields)
        response = connection.getresponse()
        text = response.read().decode()
        try:
            value = json.loads(text)
        except ValueError:
            value = text
        return response.status, value
    finally:
        connection.close()


def raw_request(headers, *, method='PUT'):
    """Preserve header duplicates/missing Host rather than dict normalization."""
    connection = http.client.HTTPConnection('127.0.0.1', 5173, timeout=5)
    try:
        connection.putrequest(method, '/api/watchlist', skip_host=True, skip_accept_encoding=True)
        for name, value in headers:
            connection.putheader(name, value)
        connection.putheader('Content-Length', '0')
        connection.endheaders()
        response = connection.getresponse()
        return response.status, response.read().decode()
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--evidence', required=True)
    args = parser.parse_args()
    evidence = Path(args.evidence).resolve()
    evidence.mkdir(parents=True, exist_ok=True)
    if (evidence / 'http-results.json').exists():
        raise RuntimeError('Evidence already exists; refusing overwrite')
    store = Path(tempfile.mkdtemp(prefix='fox2-ISOLATED_TEST-website-',
                                 dir=Path(os.environ['LOCALAPPDATA']) / 'FOX2'))
    observations = []
    children = []
    server_log = (evidence / 'asgi-output.txt').open('x', encoding='utf-8')

    def start(port=8000, unconfigured=False):
        # Never attach to or terminate an existing listener.
        import socket
        with socket.socket() as probe:
            if probe.connect_ex(('127.0.0.1', port)) == 0:
                raise RuntimeError(f'Port {port} occupied; refusing to replace service')
        command = [sys.executable, '-B', str(CHILD), '--store-root', str(store), '--port', str(port),
                   '--request-log', str(evidence / f'backend-{port}-requests.jsonl'),
                   '--outbound-log', str(evidence / f'outbound-{port}-{len(children)}.txt')]
        if unconfigured:
            command.append('--unconfigured')
        child = subprocess.Popen(command, cwd=ROOT, stdout=server_log, stderr=subprocess.STDOUT,
                                 env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        children.append(child)
        for _ in range(100):
            if child.poll() is not None:
                raise RuntimeError('Owned ASGI child exited during startup')
            try:
                if request('/api/health', port=port)[0] == 200:
                    return child
            except OSError:
                pass
            time.sleep(.1)
        raise RuntimeError('Owned ASGI child did not become ready')

    def check(name, callback, critical=False):
        try:
            detail = callback()
            record = {'name': name, 'result': 'PASS', 'detail': detail}
        except Exception as error:
            record = {'name': name, 'result': 'FAIL', 'critical': critical, 'detail': str(error)}
            observations.append(record)
            print(json.dumps(record), flush=True)
            raise
        observations.append(record)
        print(json.dumps(record), flush=True)

    def expected(path, code, **kwargs):
        status, value = request(path, **kwargs)
        assert status == code, f'{path}: expected HTTP {code}, observed {status}: {value}'
        return value

    def put(items, version, code=200, **kwargs):
        return expected('/api/watchlist', code, method='PUT',
                        body={'expected_version': version, 'items': items}, **kwargs)

    outcome = 'FAIL'
    try:
        backend = start()
        check('real_health_provider_disabled', lambda: health_check(expected))
        check('test_universe_provenance', lambda: universe_check(expected))
        check('market_unavailable_without_fake_values', lambda: market_check(expected))
        check('initial_watchlist', lambda: initial_check(expected))
        saved = put(['TEST:AAA', 'TEST:BBB'], 0)
        check('add_and_readback', lambda: equal_check(expected('/api/watchlist', 200), saved))
        check('CAS_409_preserves_winner', lambda: conflict_check(expected, put, saved))
        check('invalid_unknown_duplicate_101_rejected_422', lambda: invalid_check(expected, saved))
        check('remove_and_persist', lambda: remove_check(expected, put, saved))
        before_restart = expected('/api/watchlist', 200)
        backend.terminate()
        backend.wait(timeout=10)
        start()
        check('ASGI_process_restart_SQLite_persistence',
              lambda: equal_check(expected('/api/watchlist', 200), before_restart))
        check('CAS_concurrent_one_winner', lambda: concurrent_check(expected))
        check('exactly_100_then_101_rejected', lambda: limit_check(expected, put))
        check('HTTP_404_422', lambda: route_negative_check(expected))
        check('backend_Host_Origin_content_type_guards', lambda: guards_check(expected), critical=True)
        start(port=8001, unconfigured=True)
        check('real_HTTP_503_unconfigured_store',
              lambda: equal_check(expected('/api/watchlist', 503, port=8001), {'detail': 'Service unavailable'}))
        check('Vite_same_origin_proxy_health_watchlist_stock', lambda: proxy_check(expected))
        check('Vite_proxy_contract_409_422_100', lambda: proxy_contract_check(expected))
        check('four_routes_direct_HTTP_reload', lambda: reload_check(expected))
        check('ISOLATED_TEST_SQLite_profile', lambda: profile_check(store))
        # Important: checks the actual Website-facing boundary, not only ASGI.
        check('Vite_proxy_rejects_foreign_Origin_mutation',
              lambda: proxy_origin_check(expected, evidence), critical=True)
        check('Vite_proxy_ambiguous_headers_missing_origin_and_spoofs',
              lambda: proxy_header_check(expected, evidence), critical=True)
        check('Vite_trusted_origin_translated_backend_authority',
              lambda: translated_origin_check(evidence), critical=True)
        check('no_nonloopback_transport_attempts', lambda: outbound_check(evidence), critical=True)
        outcome = 'PASS'
    finally:
        for child in reversed(children):
            if child.poll() is None:
                child.terminate()
                child.wait(timeout=10)
        server_log.close()
        result = {'fixture': 'ISOLATED_TEST_UNIVERSE; no quotes/bars seeded',
                  'store_root': str(store), 'SQLite_profile': 'ISOLATED_TEST',
                  'result': outcome, 'checks': observations,
                  'browser': 'NOT_RUN_NO_BROWSER_SURFACE', 'owned_ASGI_children_stopped': True}
        (evidence / 'http-results.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')


def equal_check(observed, expected):
    assert observed == expected, f'{observed!r} != {expected!r}'
    return observed


def health_check(expected):
    health = expected('/api/health', 200)
    assert health['status'] == 'OK' and health['provider_enabled'] is False
    return health


def universe_check(expected):
    result = expected('/api/stocks?query=AAA&limit=20', 200)
    assert result['universe_source'] == 'ISOLATED_TEST_UNIVERSE'
    assert result['coverage'] == 'PARTIAL' and result['items'][0]['instrument_id'] == 'TEST:AAA'
    return result


def market_check(expected):
    paths = ['/api/market/overview', '/api/stocks/AAA',
             '/api/stocks/AAA/bars?from=2026-07-01T00:00:00Z&to=2026-10-01T00:00:00Z&timeframe=1D&basis=RAW']
    for path in paths:
        value = expected(path, 200)
        envelopes = value if isinstance(value, list) else [value.get('quote', value)]
        assert envelopes
        for envelope in envelopes:
            data = envelope['data']
            assert data['freshness_state'] == 'UNAVAILABLE' and data['payload'] is None
            assert data['as_of'] is None and data['selection_audit_id']
    sources = expected('/api/data-sources/health', 200)
    assert all(source['state'] == 'UNKNOWN' for source in sources)
    return {'payload': None, 'as_of': None, 'freshness': 'UNAVAILABLE', 'source_state': 'UNKNOWN'}


def initial_check(expected):
    return equal_check(expected('/api/watchlist', 200), {'version': 0, 'items': [], 'updated_at': None})


def conflict_check(expected, put, saved):
    put([], 0, code=409)
    return equal_check(expected('/api/watchlist', 200), saved)


def invalid_check(expected, saved):
    cases = [['TEST:UNKNOWN'], ['AAA'], ['TEST:AAA', 'TEST:AAA'],
             [f'TEST:S{i:03}' for i in range(100)] + ['TEST:AAA'], [42], ['']]
    for items in cases:
        expected('/api/watchlist', 422, method='PUT', body={'expected_version': saved['version'], 'items': items})
        equal_check(expected('/api/watchlist', 200), saved)
    return {'rejected_cases': len(cases), 'prior_preserved': True}


def remove_check(expected, put, saved):
    changed = put(['TEST:BBB'], saved['version'])
    return equal_check(expected('/api/watchlist', 200), changed)


def concurrent_check(expected):
    version = expected('/api/watchlist', 200)['version']
    def update(item):
        return request('/api/watchlist', method='PUT', body={'expected_version': version, 'items': [item]})
    with ThreadPoolExecutor(max_workers=2) as executor:
        values = list(executor.map(update, ['TEST:AAA', 'TEST:BBB']))
    assert sorted(status for status, _ in values) == [200, 409]
    winner = next(body for status, body in values if status == 200)
    equal_check(expected('/api/watchlist', 200), winner)
    return {'statuses': sorted(status for status, _ in values), 'winner_preserved': True}


def limit_check(expected, put):
    version = expected('/api/watchlist', 200)['version']
    saved = put([f'TEST:S{i:03}' for i in range(100)], version)
    assert len(saved['items']) == 100
    put(saved['items'] + ['TEST:AAA'], saved['version'], code=422)
    equal_check(expected('/api/watchlist', 200), saved)
    return {'100': 200, '101': 422}


def route_negative_check(expected):
    for path, status in [('/api/stocks/UNKNOWN', 404), ('/api/no-such-route', 404),
                         ('/api/stocks?query=AAA&limit=101', 422), ('/api/stocks/AAA?extra=1', 422),
                         ('/api/stocks/AAA/bars?from=bad&to=bad', 422)]:
        expected(path, status)
    return {'404': True, '422': True}


def guards_check(expected):
    saved = expected('/api/watchlist', 200)
    body = {'expected_version': saved['version'], 'items': []}
    for headers, status in [({'Host': 'evil.example'}, 400),
                            ({'Origin': 'https://evil.example'}, 403),
                            ({'Origin': 'http://127.0.0.1:5173'}, 403),
                            ({'Origin': 'null'}, 403),
                            ({'Content-Type': 'text/plain'}, 415)]:
        expected('/api/watchlist', status, method='PUT', body=body, headers=headers)
        equal_check(expected('/api/watchlist', 200), saved)
    expected('/api/health', 200, headers={'Origin': 'http://127.0.0.1:8000'})
    return {'foreign_host': 400, 'foreign_origin': 403, 'content_type': 415, 'state_preserved': True}


def proxy_check(expected):
    health = expected('/api/health', 200, port=5173)
    assert health['provider_enabled'] is False
    expected('/api/watchlist', 200, port=5173)
    expected('/api/stocks/AAA', 200, port=5173)
    current = expected('/api/watchlist', 200, port=5173)
    expected('/api/watchlist', 200, port=5173, method='PUT',
             headers={'Origin': 'http://127.0.0.1:5173'},
             body={'expected_version': current['version'], 'items': current['items']})
    return 'Actual Vite proxy GET and same-origin JSON PUT reached accepted backend'


def reload_check(expected):
    for path in ['/overview', '/watchlist', '/stocks/AAA', '/settings/data-sources']:
        html = expected(path, 200, port=5173, headers={'Accept': 'text/html'})
        assert '<div id="root">' in html and '/src/main.tsx' in html
    return 'Four direct HTTP GETs returned Vite entry; browser rendering NOT_RUN'


def profile_check(store):
    with sqlite3.connect(store / 'fox2.sqlite3') as connection:
        rows = dict(connection.execute('SELECT key,value FROM store_metadata'))
        assert 'ISOLATED_TEST' in rows.values()
    return rows


def receipt_count(evidence):
    return len((evidence / 'backend-8000-requests.jsonl').read_text(encoding='utf-8').splitlines())


def proxy_origin_check(expected, evidence):
    current = expected('/api/watchlist', 200)
    before = receipt_count(evidence)
    # Empty list only, in an explicitly isolated test store. No market writes.
    status, response = request('/api/watchlist', port=5173, method='PUT',
        headers={'Origin': 'https://evil.example'},
        body={'expected_version': current['version'], 'items': []})
    assert status == 403, (f'CRITICAL: Vite foreign Origin expected 403, observed {status}; '
                           f'prior_version={current["version"]}; response={response}')
    assert receipt_count(evidence) == before, 'Rejected request reached backend'
    equal_check(expected('/api/watchlist', 200), current)
    return {'foreign_origin': status, 'state_preserved': True, 'upstream_requests': 0}


def proxy_header_check(expected, evidence):
    current = expected('/api/watchlist', 200)
    trusted = 'http://127.0.0.1:5173'
    authority = ('Host', '127.0.0.1:5173')
    cases = []
    for origin in ['null', 'not-an-origin', 'https://127.0.0.1:5173',
                   'http://localhost:5173', 'http://127.0.0.1:51730',
                   trusted + '.evil.example', trusted + '/', trusted + '/path',
                   trusted + '?x=1', trusted + '#fragment',
                   'http://user@127.0.0.1:5173', trusted + ', ' + trusted,
                   'http://127.0.0.1:8000', 'http://127.0.0.1:05173']:
        cases.append(('origin:' + origin, [authority, ('Origin', origin)], 403))
    cases.extend([
        ('missing Origin PUT', [authority], 403),
        ('duplicate identical Origin', [authority, ('Origin', trusted), ('origin', trusted)], 400),
        ('duplicate foreign Origin', [authority, ('Origin', trusted), ('Origin', 'null')], 400),
        ('duplicate identical Host', [authority, authority, ('Origin', trusted)], 400),
        ('duplicate foreign Host', [authority, ('host', 'evil.example'), ('Origin', trusted)], 400),
        ('missing Host', [('Origin', trusted)], 400),
        ('wrong Host', [('Host', 'evil.example'), ('Origin', trusted)], 400),
        ('localhost alias Host', [('Host', 'localhost:5173'), ('Origin', trusted)], 400),
        ('wrong port Host', [('Host', '127.0.0.1:5174'), ('Origin', trusted)], 400),
        ('duplicate content-type', [authority, ('Origin', trusted),
            ('Content-Type', 'application/json'), ('content-type', 'text/plain')], 400),
    ])
    results = []
    for name, headers, code in cases:
        before = receipt_count(evidence)
        status, body = raw_request(headers)
        assert status == code, f'{name}: expected {code}, observed {status}: {body}'
        assert receipt_count(evidence) == before, f'{name}: reached backend'
        equal_check(expected('/api/watchlist', 200), current)
        results.append({'case': name, 'status': status, 'upstream_requests': 0, 'state_preserved': True})
    for method in ['POST', 'PATCH', 'DELETE']:
        before = receipt_count(evidence)
        status, _ = raw_request([authority], method=method)
        assert status == 403 and receipt_count(evidence) == before
        results.append({'case': 'missing Origin ' + method, 'status': status, 'upstream_requests': 0})
    # A supplied foreign Origin must also be rejected for read-only requests.
    before = receipt_count(evidence)
    expected('/api/health', 403, port=5173, headers={'Origin': 'null'})
    assert receipt_count(evidence) == before
    results.append({'case': 'null Origin GET', 'status': 403, 'upstream_requests': 0})
    equal_check(expected('/api/watchlist', 200), current)
    return results


def proxy_contract_check(expected):
    headers = {'Origin': 'http://127.0.0.1:5173'}
    current = expected('/api/watchlist', 200, port=5173)
    items = current['items']
    assert len(items) == 100
    for invalid in [['TEST:UNKNOWN'], ['TEST:AAA', 'TEST:AAA'], items + ['TEST:AAA']]:
        expected('/api/watchlist', 422, port=5173, method='PUT', headers=headers,
                 body={'expected_version': current['version'], 'items': invalid})
        equal_check(expected('/api/watchlist', 200, port=5173), current)
    expected('/api/watchlist', 409, port=5173, method='PUT', headers=headers,
             body={'expected_version': current['version'] - 1, 'items': []})
    equal_check(expected('/api/watchlist', 200, port=5173), current)
    expected('/api/watchlist', 415, port=5173, method='PUT',
             headers={**headers, 'Content-Type': 'text/plain'}, body={'expected_version': current['version'], 'items': []})
    equal_check(expected('/api/watchlist', 200, port=5173), current)
    return {'saved_items': 100, 'unknown_duplicate_101': 422, 'CAS': 409, 'content_type': 415, 'prior_preserved': True}


def translated_origin_check(evidence):
    rows = [json.loads(row) for row in (evidence / 'backend-8000-requests.jsonl').read_text(encoding='utf-8').splitlines()]
    puts = [row for row in rows if row['method'] == 'PUT' and row['origin'] == 'http://127.0.0.1:8000']
    assert puts and all(row['host'] == '127.0.0.1:8000' for row in puts)
    return {'trusted_PUT_backend_receipts': len(puts), 'translated_origin': 'http://127.0.0.1:8000'}


def outbound_check(evidence):
    logs = list(evidence.glob('outbound-*.txt'))
    assert len(logs) == 3
    assert all(not path.read_text(encoding='utf-8') for path in logs), 'Forbidden transport attempt recorded'
    return {'guarded_ASGI_processes': len(logs), 'nonloopback_attempts': 0}


if __name__ == '__main__':
    main()
