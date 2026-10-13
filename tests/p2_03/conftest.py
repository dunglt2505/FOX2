"""Offline test harness; upstream fixtures are read-only."""
import importlib.util
from pathlib import Path
import socket
import sys
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'backend/src'))
spec = importlib.util.spec_from_file_location('p2_02_fixture_reference', ROOT / 'tests/p2_02/conftest.py')
upstream = importlib.util.module_from_spec(spec)
spec.loader.exec_module(upstream)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    attempts = []
    def deny(*args, **kwargs):
        attempts.append('NETWORK_ATTEMPT')
        raise AssertionError('offline only')
    for name in ('connect', 'connect_ex', 'bind', 'listen', 'sendto', 'sendall', 'send'):
        monkeypatch.setattr(socket.socket, name, deny)
    for name in ('create_connection', 'getaddrinfo', 'gethostbyname', 'gethostbyname_ex', 'gethostbyaddr'):
        monkeypatch.setattr(socket, name, deny)
    yield attempts
    assert attempts == []


@pytest.fixture
def h(tmp_path):
    return upstream.Harness(tmp_path / 'fox2-dsm-isolated')
