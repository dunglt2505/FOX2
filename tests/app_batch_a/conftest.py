"""Test-only offline universe/market claims, never loaded by investor runtime."""
import asyncio
import importlib.util
from pathlib import Path
import socket
import sys
from datetime import timedelta

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend/src'))
spec = importlib.util.spec_from_file_location('batch_store_harness', ROOT / 'tests/p2_02/conftest.py')
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)

from fox2.application.registry import InstrumentRegistry
from fox2.config import Settings
from fox2.contracts.instruments import Instrument
from fox2.dsm import CapabilityPolicy
from fox2.main import create_app


@pytest.fixture(scope='session')
def offline_runner():
    loop = asyncio.new_event_loop()  # Harness wakeup socket before denial on Windows.
    yield loop.run_until_complete
    loop.close()


@pytest.fixture(autouse=True)
def no_network(monkeypatch, offline_runner):
    attempts = []
    def deny(*args, **kwargs):
        attempts.append('FORBIDDEN_NETWORK')
        raise AssertionError('Offline runtime attempted transport')
    for name in ('connect', 'connect_ex', 'bind', 'listen', 'sendto'):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ('getaddrinfo', 'create_connection', 'gethostbyname', 'gethostbyname_ex', 'gethostbyaddr'):
        monkeypatch.setattr(socket, name, deny)
    monkeypatch.setattr(httpx.HTTPTransport, '__init__', deny)
    monkeypatch.setattr(httpx.AsyncHTTPTransport, '__init__', deny)
    yield attempts
    assert attempts == []


@pytest.fixture
def registry():
    return InstrumentRegistry([
        Instrument(instrument_id='TEST:AAA', symbol='AAA', instrument_type='STOCK', venue='HOSE', board_id='G1'),
        Instrument(instrument_id='TEST:BBB', symbol='BBB', instrument_type='STOCK', venue='HNX', board_id='G1'),
        Instrument(instrument_id='TEST:IDX', symbol='IDX', instrument_type='INDEX', venue='HOSE', board_id='G1'),
    ], source='ISOLATED_TEST_UNIVERSE', revision='test-v1', coverage='PARTIAL')


@pytest.fixture
def h(tmp_path):
    return upstream.Harness(tmp_path / 'fox2-batch-test')


def policy(capability):
    return CapabilityPolicy(capability, timedelta(minutes=10), 'offline-v1', 'isolated-calendar',
                            'REGULAR', mapping_verified=True, session_mapping_verified=True,
                            coverage_verified=True, relevant_gap=False)


@pytest.fixture
def client_request(offline_runner):
    # Explicit app/peer/headers, no live server or provider transport.
    def perform(app, path, *, method='GET', peer='127.0.0.1', headers=None, **kwargs):
        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(
                    app=app, client=(peer, 123), raise_app_exceptions=False),
                    base_url='http://127.0.0.1:8000') as client:
                return await client.request(method, path, headers=headers, **kwargs)
        return offline_runner(run())
    return perform


@pytest.fixture
def configured(tmp_path, registry):
    settings = Settings(store_root=str(tmp_path / 'fox2-configured'))
    from fox2.runtime import OfflineRuntime
    runtime = OfflineRuntime(settings, registry=registry)
    return create_app(settings, runtime=runtime), runtime, settings
