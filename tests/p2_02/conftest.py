"""Deterministic offline fixtures; never imported by application code."""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import socket
import sys
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'backend/src'))
from fox2.contracts.market import MarketObservation
from fox2.ports.outcomes import IngestAudit
from fox2.store import SQLiteStore, PromotionEvidence
from fox2.validation.semantics import CapabilityContext


@pytest.fixture(autouse=True)
def offline(monkeypatch):
    attempts = []
    def denied(*args, **kwargs):
        attempts.append('NETWORK_ATTEMPT')
        raise AssertionError('P2-02 network forbidden')
    for name in ('connect', 'connect_ex', 'bind', 'listen', 'sendto'):
        monkeypatch.setattr(socket.socket, name, denied)
    monkeypatch.setattr(socket, 'create_connection', denied)
    monkeypatch.setattr(socket, 'getaddrinfo', denied)
    yield attempts
    assert not attempts


class Harness:
    def __init__(self, root):
        self.root = root
        self.now = datetime(2026, 10, 14, 3, tzinfo=timezone.utc)
        self.order = 1
        self.parent = None
        self.verified = True
        self.ref = 'isolated-proof'
        self.counter = 0
        self.hook = lambda stage: None
        self.store = self.open()

    def proof(self, observation):
        kind = {'quote': 'QUOTE', 'bars': 'BARS', 'index_summary': 'INDEX'}[observation.payload.kind]
        return PromotionEvidence(CapabilityContext(kind, self.now, use_context='RETAINED_USE',
                session_mapping_verified=True, adjustment_evidence_verified=True, coverage_verified=True),
                self.ref, self.verified, self.verified, self.order, self.parent)

    def open(self, **extra):
        args = dict(profile='ISOLATED_TEST', instrument_registry=lambda i: i.startswith('TEST:') and i != 'TEST:UNKNOWN',
                    clock=lambda: self.now, evidence=self.proof, fault_hook=lambda stage: self.hook(stage))
        args.update(extra)
        return SQLiteStore(self.root, **args)

    def observation(self, *, bars=False, start=None, provisional=True, **changes):
        event = self.now - timedelta(minutes=5)
        if bars:
            start = start or self.now - timedelta(days=1)
            payload = dict(kind='bars', timeframe='1D', **{'from': (start-timedelta(days=2)).isoformat(),
                'to': (self.now+timedelta(days=1)).isoformat()}, items=[dict(start_at=start.isoformat(),
                end_at=(start+timedelta(hours=6)).isoformat(), update_at=event.isoformat(),
                open=100., high=110., low=90., close=105., volume=100., turnover=10000., provisional=provisional, revision=0)], gaps=[])
        else:
            payload = dict(kind='quote', last_price=100., reference_price=100., ceiling_price=107., floor_price=93.,
                           cumulative_volume=100., cumulative_turnover=10000.)
        data = dict(profile='ISOLATED_TEST', instrument_id='TEST:AAA', symbol='AAA', instrument_type='STOCK',
            venue='HOSE', board_id='G1', record_id='upstream-event-1', revision=0, source_id='isolated-source',
            origin_provider='ISOLATED_TEST', source_revision='provider-label-unchanged', retrieval_channel='TEST_FIXTURE',
            event_at=event.isoformat(), as_of=event.isoformat(), received_at=self.now.isoformat(), first_available_at=None,
            data_mode='SYNTHETIC', freshness_state='LATEST_VALID', quality='VALID', mapping_state='VERIFIED',
            completeness='COMPLETE', price_basis='RAW', price_unit='VND_PER_SHARE', volume_unit='SHARES', turnover_unit='VND',
            adjustment_version=None, calendar_version='isolated-calendar', session='REGULAR', freshness_policy_version=None,
            rights=dict(read='VERIFIED', redisplay='VERIFIED', retained_use='VERIFIED', evidence_ref='isolated-rights',
                        verified_until=(self.now+timedelta(days=3)).isoformat()),
            selection_audit_id='isolated-selection', selection_reason='ISOLATED_TEST_ONLY', missing_fields=[], payload=payload)
        data.update(changes)
        import json
        return MarketObservation.model_validate_json(json.dumps(data, default=lambda v: v.isoformat()))

    def ingest(self, observation, *, audit_id=None, raw=None, received=None):
        self.counter += 1
        return self.store.append_and_promote(observation, IngestAudit(audit_id or f'receipt-{self.counter}',
                received or self.now, raw or f'{self.counter:064x}'))


@pytest.fixture
def h(tmp_path):
    return Harness(tmp_path / 'fox2-isolated')
