"""Explicit test-only ASGI composition. Never imported by investor startup.

No quotes/bars are seeded. Only instrument identifiers and local preferences
are fixtures; the accepted DSM returns honest unavailable market envelopes.
"""
import argparse
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'backend/src'))

from fox2.application.registry import InstrumentRegistry
from fox2.config import Settings
from fox2.contracts.instruments import Instrument
from fox2.main import create_app
from fox2.runtime import OfflineRuntime
from fox2.store import SQLiteStore


def compose(store_root):
    stocks = ['AAA', 'BBB'] + [f'S{i:03}' for i in range(100)]
    instruments = [Instrument(instrument_id='TEST:' + symbol, symbol=symbol,
        instrument_type='STOCK', venue='HOSE', board_id='ISOLATED_TEST') for symbol in stocks]
    instruments.append(Instrument(instrument_id='TEST:IDX', symbol='IDX',
        instrument_type='INDEX', venue='HOSE', board_id='ISOLATED_TEST'))
    registry = InstrumentRegistry(instruments, source='ISOLATED_TEST_UNIVERSE',
                                  revision='website-http-v1', coverage='PARTIAL')
    store = SQLiteStore(Path(store_root), profile='ISOLATED_TEST', instrument_registry=registry.contains)
    settings = Settings()
    runtime = OfflineRuntime(settings, registry=registry, repository=store)
    return create_app(settings, runtime=runtime)


if __name__ == '__main__':
    import uvicorn
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store-root', required=True)
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--unconfigured', action='store_true')
    parser.add_argument('--request-log', type=Path)
    parser.add_argument('--outbound-log', type=Path)
    args = parser.parse_args()
    if args.outbound_log:
        import ipaddress
        import socket
        args.outbound_log.touch(exist_ok=False)

        def allowed(host):
            if host == 'localhost':
                return True
            try:
                return ipaddress.ip_address(host).is_loopback
            except ValueError:
                return False

        def denied():
            with args.outbound_log.open('a', encoding='utf-8') as receipt:
                receipt.write('FORBIDDEN_NON_LOOPBACK_TRANSPORT_ATTEMPT\n')
            raise RuntimeError('Test-only network boundary denied non-loopback transport')

        original_connect = socket.socket.connect
        original_connect_ex = socket.socket.connect_ex
        original_resolve = socket.getaddrinfo

        def connect(connection, address):
            if not isinstance(address, tuple) or not allowed(address[0]):
                denied()
            return original_connect(connection, address)

        def connect_ex(connection, address):
            if not isinstance(address, tuple) or not allowed(address[0]):
                denied()
            return original_connect_ex(connection, address)

        def resolve(host, *args, **kwargs):
            if not allowed(host):
                denied()
            return original_resolve(host, *args, **kwargs)

        socket.socket.connect = connect
        socket.socket.connect_ex = connect_ex
        socket.getaddrinfo = resolve

    app = create_app() if args.unconfigured else compose(args.store_root)
    if args.request_log:
        import json

        @app.middleware('http')
        async def record_test_request(request, call_next):
            # Test-only receipt proves rejected Website requests never reached
            # ASGI. No bodies, credentials or investor records are captured.
            with args.request_log.open('a', encoding='utf-8') as receipt:
                receipt.write(json.dumps({'method': request.method, 'path': request.url.path,
                    'host': request.headers.get('host'), 'origin': request.headers.get('origin')}) + '\n')
            return await call_next(request)

    print('ISOLATED_TEST_ONLY; registry=ISOLATED_TEST_UNIVERSE; no seeded market data', flush=True)
    uvicorn.run(app, host='127.0.0.1', port=args.port, log_level='warning')
