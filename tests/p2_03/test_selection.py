from dataclasses import asdict, replace, FrozenInstanceError
from datetime import timedelta
import ast
from pathlib import Path
import json
import sqlite3
import pytest

from fox2.dsm import DataSourceManager, CapabilityPolicy
from fox2.ports.outcomes import Unavailable
from fox2.contracts.market import IndexSummary


class MemoryStore:
    def __init__(self, value):
        self.value = value
        self.calls = []
    def get_observation(self, instrument, capability, cutoff):
        self.calls.append((instrument, capability, cutoff))
        return self.value


def policy(capability='QUOTE', **changes):
    return replace(CapabilityPolicy(capability, timedelta(minutes=10), 'offline-v1',
        'isolated-calendar', 'REGULAR', mapping_verified=True,
        session_mapping_verified=True, coverage_verified=True, relevant_gap=False), **changes)


def candidate(h, **changes):
    return h.observation(first_available_at=h.now, freshness_policy_version='offline-v1', **changes)


def manager(h, value=None, capability='QUOTE', **options):
    store = MemoryStore(value if value is not None else candidate(h))
    audits = []
    args = dict(policies={capability: policy(capability)}, profile='ISOLATED_TEST',
                clock=lambda: h.now, audit_sink=audits.append)
    args.update(options)
    return DataSourceManager(store, **args), store, audits


def test_positive_fresh_audit_immutable_copy(h):
    d, store, audits = manager(h, audit_id_factory=lambda: 'constant-secret-like-value')
    before = store.value.model_dump()
    a = d.select('QUOTE', 'TEST:AAA', 'READ')
    b = d.select('QUOTE', 'TEST:AAA', 'READ')
    assert not isinstance(a.observation, Unavailable)
    assert a.selection_audit_id != b.selection_audit_id
    assert a.observation.selection_audit_id == a.selection_audit_id
    assert store.value.model_dump() == before
    a.observation.missing_fields.append('copy-only')
    assert store.value.missing_fields == []
    assert len(audits) == 2 and all(x.accepted for x in audits)
    with pytest.raises(FrozenInstanceError): audits[0].accepted = False
    text = json.dumps(asdict(audits[0]), default=str)
    assert 'constant-secret' not in text and 'TEST:AAA' not in text and 'last_price' not in text


@pytest.mark.parametrize('capability', ['QUOTE', 'BARS', 'INDEX'])
def test_absence_preserved_without_timestamps(h, capability):
    d, store, audits = manager(h, Unavailable('NOT_FOUND'), capability)
    result = d.select(capability, 'TEST:AAA', 'READ')
    assert result.observation == Unavailable('NOT_FOUND')
    assert store.calls == [('TEST:AAA', capability, h.now)]
    assert not hasattr(result.observation, 'as_of') and not audits[0].accepted


@pytest.mark.parametrize('enabled', [False, True])
def test_provider_boundary(h, no_network, enabled):
    d, store, audits = manager(h, provider_enabled=enabled)
    result = d.select('QUOTE', 'TEST:AAA', 'READ')
    if enabled:
        assert result.observation == Unavailable('UNKNOWN') and store.calls == []
        assert audits[0].reason_codes == ('NOT_INTEGRATED',)
    health = d.source_health('QUOTE')
    assert health.readiness == 'UNAVAILABLE' and health.state == 'UNKNOWN'
    assert health.reason == 'NOT_INTEGRATED' and health.verified_until is None
    assert no_network == []


@pytest.mark.parametrize('use', ['READ', 'DISPLAY', 'ANALYSIS', 'RETAINED_USE'])
@pytest.mark.parametrize('right', ['read', 'redisplay', 'retained_use'])
@pytest.mark.parametrize('state', ['UNKNOWN', 'BLOCKED', 'VERIFIED'])
def test_rights_matrix(h, use, right, state):
    o = candidate(h)
    o = o.model_copy(update={'rights': o.rights.model_copy(update={right: state})})
    d, _, _ = manager(h, o)
    result = d.select('QUOTE', 'TEST:AAA', use).observation
    required = right in ('read', 'retained_use') or use in ('DISPLAY', 'ANALYSIS')
    assert isinstance(result, Unavailable) == (required and state != 'VERIFIED')
    if isinstance(result, Unavailable): assert result.reason == 'RIGHTS_BLOCKED'


def test_expiry_rechecked_without_cache(h):
    d, store, _ = manager(h)
    assert not isinstance(d.select('QUOTE', 'TEST:AAA', 'READ').observation, Unavailable)
    h.now = store.value.rights.verified_until
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('RIGHTS_BLOCKED')
    assert len(store.calls) == 2


def test_real_store_revocation_no_fallback(h):
    h.ingest(h.observation(freshness_policy_version='offline-v1'))
    d = DataSourceManager(h.store, policies={'QUOTE': policy()}, profile='ISOLATED_TEST', clock=lambda: h.now)
    assert not isinstance(d.select('QUOTE', 'TEST:AAA', 'READ').observation, Unavailable)
    with sqlite3.connect(h.store.path) as connection:
        key = connection.execute('SELECT series_key FROM series').fetchone()[0]
    h.store.revoke_rights(key, 'offline-revocation')
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('RIGHTS_BLOCKED')


@pytest.mark.parametrize('changes', [dict(profile='INVESTOR'), dict(data_mode='SYNTHETIC'), dict(retrieval_channel='TEST_FIXTURE')])
def test_investor_fixture_rejected(h, changes):
    d, _, _ = manager(h, candidate(h, **changes), profile='INVESTOR')
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('INVALID_CANDIDATE')


@pytest.mark.parametrize('requested', ['QUOTE', 'INDEX'])
def test_bars_never_cross_capability(h, requested):
    d, store, _ = manager(h, candidate(h, bars=True), requested)
    assert d.select(requested, 'TEST:AAA', 'READ').observation == Unavailable('INVALID_CANDIDATE')
    assert len(store.calls) == 1 and store.calls[0][1] == requested


@pytest.mark.parametrize('field,value', [('instrument_id','OTHER'), ('mapping_state','UNKNOWN'),
    ('price_unit','UNKNOWN'), ('volume_unit','UNKNOWN'), ('turnover_unit','UNKNOWN'),
    ('price_basis','UNKNOWN'), ('calendar_version',None), ('session',None),
    ('freshness_policy_version',None), ('completeness','PARTIAL'), ('quality','INVALID'),
    ('freshness_state','STALE'), ('freshness_state','GAP_RECOVERING'), ('as_of',None)])
def test_candidate_guards(h, field, value):
    d, _, _ = manager(h, candidate(h).model_copy(update={field:value}))
    assert isinstance(d.select('QUOTE', 'TEST:AAA', 'READ').observation, Unavailable)


@pytest.mark.parametrize('field,value', [('mapping_verified',False), ('session_mapping_verified',False),
    ('coverage_verified',False), ('relevant_gap',None), ('relevant_gap',True)])
def test_policy_guards(h, field, value):
    d, _, _ = manager(h, policies={'QUOTE':policy(**{field:value})})
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('UNKNOWN')


def test_missing_policy(h):
    d, _, _ = manager(h, policies={})
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('UNKNOWN')


@pytest.mark.parametrize('state', ['LIVE','PERIODIC_LIVE'])
def test_live_transport_evidence_required(h, state):
    d, _, _ = manager(h, candidate(h, freshness_state=state))
    assert d.select('QUOTE', 'TEST:AAA', 'READ').observation == Unavailable('UNKNOWN')


@pytest.mark.parametrize('capability', ['QUOTE','INDEX'])
def test_stale_snapshot(h, capability):
    o = candidate(h)
    if capability == 'INDEX':
        p = IndexSummary(kind='index_summary', value=100., change_value=1., change_percent=1.,
            up_count=1, down_count=1, unchanged_count=1, volume=0., turnover=0.)
        o = o.model_copy(update={'payload':p, 'instrument_type':'INDEX', 'price_unit':'INDEX_POINTS'})
    d, _, _ = manager(h, o, capability)
    h.now += timedelta(minutes=6)
    assert d.select(capability, 'TEST:AAA', 'READ').observation == Unavailable('UNKNOWN')


def test_no_trade_event_age_and_null_not_outage(h):
    o = candidate(h, event_at=h.now-timedelta(days=2), as_of=h.now)
    o = o.model_copy(update={'payload':o.payload.model_copy(update={'last_price':None}),
                            'missing_fields':['payload.last_price']})
    d, _, _ = manager(h, o)
    selected = d.select('QUOTE', 'TEST:AAA', 'READ').observation
    assert selected.payload.last_price is None and selected.freshness_state == 'LATEST_VALID'
    d, _, _ = manager(h, o, policies={'QUOTE':policy(session_mapping_verified=False)})
    assert isinstance(d.select('QUOTE','TEST:AAA','READ').observation, Unavailable)


@pytest.mark.parametrize('use', ['READ','ANALYSIS'])
def test_native_diagnostic_only(h, use):
    d, _, _ = manager(h, candidate(h, data_mode='PROVIDER_NATIVE_UNVERIFIED', mapping_state='UNKNOWN', quality='UNKNOWN'))
    assert isinstance(d.select('QUOTE','TEST:AAA',use).observation, Unavailable)


@pytest.mark.parametrize('negative', ['gap','calendar','coverage','adjustment','revision'])
def test_bars_evidence(h, negative):
    o = candidate(h, bars=True)
    p = policy('BARS')
    if negative == 'gap':
        from fox2.contracts.market import BarsGap
        gap = BarsGap(from_at=o.payload.from_at, to=o.payload.to, reason='offline-gap', capability='BARS')
        o = o.model_copy(update={'payload':o.payload.model_copy(update={'gaps':[gap]})})
    elif negative == 'calendar': p = replace(p, session_mapping_verified=False)
    elif negative == 'coverage': p = replace(p, coverage_verified=False)
    elif negative == 'adjustment': o = o.model_copy(update={'price_basis':'ADJUSTED','adjustment_version':'offline-adj'})
    else:
        item = o.payload.items[0].model_copy(update={'end_at':None, 'provisional':False})
        o = o.model_copy(update={'payload':o.payload.model_copy(update={'items':[item]})})
    d, _, _ = manager(h, o, 'BARS', policies={'BARS':p})
    assert isinstance(d.select('BARS','TEST:AAA','READ').observation, Unavailable)


def test_safe_bars_and_index(h):
    d, _, _ = manager(h, candidate(h,bars=True), 'BARS')
    assert not isinstance(d.select('BARS','TEST:AAA','READ').observation, Unavailable)
    p = IndexSummary(kind='index_summary', value=100., change_value=1., change_percent=1.,
        up_count=1, down_count=1, unchanged_count=1, volume=0., turnover=0.)
    o = candidate(h, instrument_type='INDEX', price_unit='INDEX_POINTS').model_copy(update={'payload':p})
    d, _, _ = manager(h, o, 'INDEX')
    assert not isinstance(d.select('INDEX','TEST:AAA','READ').observation, Unavailable)


def test_import_boundary_and_syntax():
    root = Path(__file__).resolve().parents[2] / 'backend/src/fox2/dsm'
    for path in root.rglob('*.py'):
        tree = ast.parse(path.read_text())
        compile(tree, str(path), 'exec')
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                assert not any(s in (node.module or '').split('.') for s in ('provider','api','frontend','bridge'))
                assert node.module != 'fox2.store'
            if isinstance(node, ast.Import):
                assert all(a.name.split('.')[0] in ('dataclasses','datetime','hashlib','typing','uuid') for a in node.names)


@pytest.mark.parametrize('capability,instrument,use', [('TICKS','TEST:AAA','READ'),('QUOTE','','READ'),('QUOTE','TEST:AAA','BAD')])
def test_invalid_input_audited_without_read(h, capability, instrument, use):
    d, store, audits = manager(h)
    assert d.select(capability,instrument,use).observation == Unavailable('INVALID_CANDIDATE')
    assert store.calls == [] and len(audits) == 1


@pytest.mark.parametrize('field,value', [('evidence_ref',None), ('verified_until',None)])
def test_missing_rights_evidence(h, field, value):
    o = candidate(h)
    o = o.model_copy(update={'rights':o.rights.model_copy(update={field:value})})
    d, _, _ = manager(h, o)
    assert d.select('QUOTE','TEST:AAA','READ').observation == Unavailable('RIGHTS_BLOCKED')


def test_malformed_candidate_and_store_failure_audited(h):
    o = candidate(h)
    o = o.model_copy(update={'payload':o.payload.model_copy(update={'last_price':-1.})})
    d, store, audits = manager(h, o)
    assert d.select('QUOTE','TEST:AAA','READ').observation == Unavailable('INVALID_CANDIDATE')
    def fail(*args): raise OSError('private-error-do-not-log')
    store.get_observation = fail
    assert d.select('QUOTE','TEST:AAA','READ').observation == Unavailable('UNSAFE_STORE')
    assert len(audits) == 2 and 'private-error' not in str(audits)


@pytest.mark.parametrize('capability', ['QUOTE','BARS','INDEX'])
def test_all_health_diagnostic_only(h, capability):
    d, _, _ = manager(h)
    health = d.source_health(capability)
    assert health.capability == capability and health.reason == 'NOT_INTEGRATED'
    assert health.readiness in ('UNKNOWN','UNAVAILABLE') and health.state in ('UNKNOWN','UNAVAILABLE')


@pytest.mark.parametrize('field,value', [('retrieval_channel','UNAVAILABLE'), ('source_id',''),
    ('record_id',''), ('origin_provider',''), ('quality','UNKNOWN')])
def test_provenance_quality_required(h, field, value):
    d, _, _ = manager(h, candidate(h).model_copy(update={field:value}))
    assert isinstance(d.select('QUOTE','TEST:AAA','READ').observation, Unavailable)


def test_investor_verified_local_candidate_and_sanitized_audit(h):
    o = candidate(h, profile='INVESTOR', data_mode='VERIFIED_PROVIDER',
        retrieval_channel='LOCAL_STORE', source_id='private-source-do-not-log',
        record_id='private-record-do-not-log')
    d, _, audits = manager(h, o, profile='INVESTOR')
    result = d.select('QUOTE','TEST:AAA','DISPLAY')
    assert not isinstance(result.observation, Unavailable)
    assert 'private-' not in str(audits) and audits[0].accepted
