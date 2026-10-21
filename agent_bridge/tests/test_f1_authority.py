"""Source-level engine tests using fake OS fences/spawn. NOT G3 enforcement."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
import sqlite3

import pytest

from fox2_agent_bridge.f1_authority import ApprovedTask, Authority
from fox2_agent_bridge.f1_broker_store import BrokerEpoch, F1BrokerStore
from fox2_agent_bridge.f1_protocol import AuthorityDeny, Peer, Request
from fox2_agent_bridge.f1_service import route

PACKAGE, SOURCE = 'a' * 64, 'b' * 40
PEER = Peer('S-1-5-21-123', 7, 1234, 100)


class Clock:
    wall = 100
    tick = 10


class Child:
    resumed = False
    closed = False
    expires_at = 0

    def resume(self):
        self.resumed = True

    def close(self):
        self.closed = True


class Spawner:
    def __init__(self, store):
        self.store = store
        self.children = []
        self.hook = lambda: None

    def prepare(self, task, peer):
        with sqlite3.connect(self.store.path) as con:
            assert con.execute('SELECT reason FROM consumed WHERE dispatch_id=?',
                               (task.request.dispatch_id,)).fetchone() == ('SPAWN_INTENT',)
        self.hook()
        child = Child()
        self.children.append(child)
        return child


@pytest.fixture
def engine(tmp_path):
    store = F1BrokerStore(tmp_path / 'protected-fixture.db')
    store.initialize()
    clock, spawner = Clock(), Spawner(store)
    state = {'reason': None, 'calls': 0}

    def fence(task):
        state['calls'] += 1
        if state['reason']:
            raise AuthorityDeny(state['reason'])

    authority = Authority(store, fence=fence, spawner=spawner,
                          clock=lambda: clock.wall, monotonic=lambda: clock.tick)
    authority.start(BrokerEpoch(1, 'p' * 64, SOURCE, PACKAGE, 1000))
    request = Request(1, 'FOX2-F1-fixture', 'c' * 64, 'd' * 64, PACKAGE,
                      'CODEX', 'e' * 64, authority.epoch)
    task = ApprovedTask(request, PEER.sid, PEER.session, 500, ('sealed.exe',),
                        'fixture', (), 'fixture.db')
    authority.stage((task,))
    return authority, store, clock, spawner, task, state


def test_service_owned_persist_before_spawn_no_bearer_and_global_concurrency(engine):
    authority, store, _, spawner, task, _ = engine
    with ThreadPoolExecutor(max_workers=16) as pool:
        decisions = list(pool.map(lambda _: authority.claim_and_spawn(asdict(task.request), PEER), range(32)))
    assert sum(r['decision'] == 'STARTED' for r in decisions) == 1
    assert store.consumed_ids() == (task.request.dispatch_id,)
    assert len(spawner.children) == 1 and spawner.children[0].resumed
    assert all('lease' not in str(r) and 'token' not in r for r in decisions)


@pytest.mark.parametrize('field,value', [
    ('protocol_version', True), ('dispatch_id', 'FOX2-forged'),
    ('immutable_task_sha', 'f' * 64), ('source_digest', 'f' * 64),
    ('package_digest', 'f' * 64), ('requested_actor', 'COPILOT'),
    ('request_nonce', 'f' * 64), ('epoch', 2), ('epoch', True),
])
def test_forged_request_has_no_consumption_or_spawn(engine, field, value):
    authority, store, _, spawner, task, _ = engine
    request = {**asdict(task.request), field: value}
    assert authority.claim_and_spawn(request, PEER)['decision'] == 'DENY'
    assert store.consumed_ids() == () and spawner.children == []


@pytest.mark.parametrize('peer', [replace(PEER, sid='S-1-5-18'), replace(PEER, session=8),
                                  replace(PEER, pid=0), replace(PEER, token=0)])
def test_only_server_derived_peer_matches_staged_actor(engine, peer):
    authority, store, _, _, task, _ = engine
    assert authority.claim_and_spawn(asdict(task.request), peer)['reason'] == 'CALLER_IDENTITY'
    request = {**asdict(task.request), 'caller_sid': PEER.sid}
    assert authority.claim_and_spawn(request, peer)['reason'] == 'REQUEST_SHAPE'
    assert not store.consumed_ids()


@pytest.mark.parametrize('reason', ['SERVICE_ABSENT', 'SERVICE_DRIFT', 'POLICY_BINDING',
    'SERVICE_NOT_RUNNING', 'SEALED_FILE_DRIFT', 'PAUSED_OR_STOPPED', 'CONTROLS_MISSING'])
def test_fence_loss_revokes_and_cannot_resume_in_same_epoch(engine, reason):
    authority, store, _, spawner, task, state = engine
    state['reason'] = reason
    assert authority.claim_and_spawn(asdict(task.request), PEER)['reason'] == reason
    state['reason'] = None
    assert authority.claim_and_spawn(asdict(task.request), PEER)['reason'] == 'AUTHORITY_REVOKED'
    assert not store.consumed_ids() and not spawner.children


def test_restart_increments_epoch_revokes_leases_preserves_consumption(engine):
    authority, store, clock, spawner, task, _ = engine
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'STARTED'
    authority.revoke()
    assert spawner.children[0].closed
    restarted = Authority(F1BrokerStore(store.path), fence=lambda _: None, spawner=spawner,
                          clock=lambda: clock.wall, monotonic=lambda: clock.tick)
    restarted.start(BrokerEpoch(1, 'new-policy', SOURCE, PACKAGE, 1000))
    assert restarted.epoch == 2
    new_task = replace(task, request=replace(task.request, epoch=2))
    restarted.stage((new_task,))
    assert restarted.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'DENY'
    assert restarted.claim_and_spawn(asdict(new_task.request), PEER)['reason'] == 'CONSUMED_OR_EXPIRED'
    assert store.consumed_ids() == (task.request.dispatch_id,)


def test_ambiguous_spawn_failure_permanently_consumes(engine):
    authority, store, _, spawner, task, _ = engine
    def ambiguous():
        raise OSError('synthetic post-create uncertainty')
    spawner.hook = ambiguous
    assert authority.claim_and_spawn(asdict(task.request), PEER)['reason'] == 'AUTHORITY_UNCERTAIN'
    assert store.consumed_ids() == (task.request.dispatch_id,)
    assert authority.closed


@pytest.mark.parametrize('change', ['expired', 'revoked', 'clock', 'policy'])
def test_pre_resume_recheck_cannot_spawn_and_retains_claim(engine, change):
    authority, store, clock, spawner, task, state = engine
    def hook():
        if change == 'expired': clock.wall = 160
        elif change == 'clock': clock.wall = 99
        elif change == 'revoked': authority.revoke()
        elif change == 'policy': state['reason'] = 'POLICY_BINDING'
    spawner.hook = hook
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'DENY'
    assert store.consumed_ids() == (task.request.dispatch_id,)
    assert not spawner.children[0].resumed and spawner.children[0].closed


def test_expiry_clock_monotonic_and_shutdown_rollback(engine):
    authority, store, clock, spawner, task, _ = engine
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'STARTED'
    clock.wall = 160
    authority.monitor()
    assert spawner.children[0].closed
    authority.revoke()  # rollback preserves tombstones and returns positive authority to DENY
    assert store.consumed_ids() == (task.request.dispatch_id,)
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'DENY'


def test_wall_clock_rollback_versus_elapsed_uptime_latches_revocation(engine):
    authority, store, clock, _, task, _ = engine
    clock.tick += 20
    assert authority.claim_and_spawn(asdict(task.request), PEER)['reason'] == 'CLOCK_ROLLBACK'
    assert authority.closed and not store.consumed_ids()


def test_privileged_routes_outcomes_and_non_granting_inspection(engine):
    authority, store, _, _, task, _ = engine
    for op in ('revoke', 'reconcile_and_stage', 'unknown'):
        assert route(authority, {}, {'operation': op, 'request': None}, PEER)['decision'] == 'DENY'
    assert not authority.closed
    assert authority.inspect()['decision'] == 'DENY'
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'STARTED'
    assert authority.report_outcome(task.request.dispatch_id, 'EXITED', PEER)['decision'] == 'RECORDED'
    assert authority.report_outcome(task.request.dispatch_id, 'EXITED', PEER)['decision'] == 'RECORDED'
    assert authority.report_outcome(task.request.dispatch_id, 'FAILED', PEER)['decision'] == 'DENY'
    route(authority, {}, {'operation': 'revoke', 'request': None}, replace(PEER, administrator=True))
    assert authority.closed and store.consumed_ids() == (task.request.dispatch_id,)


def test_spawn_intent_is_durably_one_use(engine):
    authority, store, _, _, task, _ = engine
    values = dict(dispatch_id=task.request.dispatch_id, lease_id='internal-only',
                  epoch=authority.epoch, package_sha256=PACKAGE, now=100)
    assert store.claim(**values, expires_at=150)
    assert store.take_spawn_intent(**values)
    assert not F1BrokerStore(store.path).take_spawn_intent(**values)


def test_heartbeat_time_floor_survives_restart_and_failed_revoke_kills_jobs(engine, monkeypatch):
    authority, store, clock, spawner, task, _ = engine
    assert authority.claim_and_spawn(asdict(task.request), PEER)['decision'] == 'STARTED'
    clock.wall = 120; clock.tick = 30
    authority.monitor()
    assert not F1BrokerStore(store.path).observe_trusted_time(119)
    def failed_storage(**kwargs):
        raise sqlite3.DatabaseError('synthetic corruption')
    monkeypatch.setattr(store, 'revoke_from_privileged_service', failed_storage)
    authority.revoke()
    assert authority.closed and authority.storage_uncertain and spawner.children[0].closed


def test_revoked_adoption_cannot_reactivate_after_restart_or_rollback(engine):
    authority, store, clock, spawner, task, _ = engine
    authority.revoke()
    restarted = Authority(F1BrokerStore(store.path), fence=lambda _: None, spawner=spawner,
                          clock=lambda: clock.wall, monotonic=lambda: clock.tick)
    restarted.start(BrokerEpoch(1, 'p' * 64, SOURCE, PACKAGE, 1000))
    assert restarted.epoch == 2
    with pytest.raises(AuthorityDeny, match='ADOPTION_REVOKED'):
        restarted.stage((replace(task, request=replace(task.request, epoch=2)),))
    assert restarted.closed and not spawner.children
    # Only a separately administered, newly sealed adoption plan can restage.
    # Changing an IPC epoch/nonce or reopening the store cannot do so.
    assert store.service_plan_revoked('p' * 64)
