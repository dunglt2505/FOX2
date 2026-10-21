"""All installed orchestration paths delegate or deny before local creation."""
from types import SimpleNamespace

import pytest

from fox2_agent_bridge import e2e_runner, f1_client
from fox2_agent_bridge.app import BridgeApp
from fox2_agent_bridge.desktop import DesktopWorker
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import ReplayBlocked, StartupBlocked
from fox2_agent_bridge.ledger import SQLiteLedger
from fox2_agent_bridge.ops_runner import BridgeOps


def test_absent_service_is_deny_and_never_spawns():
    # No service is installed/started by this test, including on Windows.
    from fox2_agent_bridge.f1_windows import Win32
    from fox2_agent_bridge.f1_protocol import AuthorityDeny
    try:
        Win32().service_pid()
    except AuthorityDeny:
        assert f1_client.inspect_authority()['decision'] == 'DENY'
        assert f1_client.execute_dispatch('FOX2-fixture', 'a' * 64)['decision'] == 'DENY'
    else:
        pytest.skip('host already has an authority; absence cannot be tested here')


@pytest.mark.parametrize('entry', ['e2e', 'ops', 'desktop', 'app'])
@pytest.mark.parametrize('decision', ['DENY', 'STARTED'])
def test_installed_paths_cannot_reach_local_claim_or_adapter(
        bridge_config, monkeypatch, entry, decision):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize(cross_root_authority_unknown=True)
    ledger.update_worker(paused=False, stop_requested=False)
    transport = SimpleNamespace(query_control_sha=lambda _: 'a' * 40,
        fetch_control=lambda *_: None, read_dispatch_blob=lambda *_: (b'fixture', 'b' * 40))
    monkeypatch.setattr(e2e_runner, 'DispatchPoller', lambda *a, **k:
                        SimpleNamespace(poll_once=lambda: SimpleNamespace(status='NO_CHANGE')))
    monkeypatch.setattr(BridgeE2ERunner, '_validate_dispatch', lambda *a, **k:
                        {'dispatch_id': 'FOX2-fixture'})
    forbidden = lambda *a, **k: pytest.fail('installed path attempted caller-side creation/claim')
    monkeypatch.setattr(BridgeE2ERunner, '_resolve_worktree', forbidden)
    monkeypatch.setattr(SQLiteLedger, 'claim_dispatch', forbidden)
    monkeypatch.setattr(e2e_runner.CodexAdapter, 'run_prompt', forbidden)
    monkeypatch.setattr(e2e_runner.CopilotAdapter, 'run_prompt', forbidden)
    calls = []
    monkeypatch.setattr(f1_client, 'execute_dispatch', lambda *a:
        (calls.append(a) or {'decision': decision, 'reason': 'SERVICE_ABSENT'}))
    runner = BridgeE2ERunner(bridge_config, ledger, transport=transport)
    ops = BridgeOps(bridge_config, ledger, transport=transport)
    monkeypatch.setattr('fox2_agent_bridge.ops_runner.DispatchPoller', lambda *a, **k:
        SimpleNamespace(poll_once=lambda: SimpleNamespace(status='NO_CHANGE')))
    monkeypatch.setattr(ops, '_eligible_dispatch', lambda: ('fixture.json', 'FOX2-fixture'))
    if entry == 'e2e':
        invoke = lambda: runner.run_once(dispatch_path='fixture.json')
    elif entry == 'ops':
        invoke = ops.run_next
    elif entry == 'desktop':
        worker = DesktopWorker(bridge_config, ops=ops)
        worker.ledger = ledger
        invoke = worker.tick
    else:
        app = BridgeApp(bridge_config); app._started = True; app.ledger = ledger
        monkeypatch.setattr('fox2_agent_bridge.app.BridgeE2ERunner', lambda *a, **k: runner)
        invoke = lambda: app.e2e_once(dispatch_path='fixture.json')
    if decision == 'DENY' and entry != 'desktop':
        with pytest.raises(ReplayBlocked, match='F1 service denied'):
            invoke()
    else:
        result = invoke()
        if entry != 'desktop': assert result.status == 'F1_SERVICE_STARTED'
    assert len(calls) == 1
    assert not ledger.pending_executions()
    assert not ledger.spawn_permitted()


def test_smoke_and_forged_ledger_metadata_cannot_bypass_service(bridge_config, monkeypatch):
    ledger = SQLiteLedger(bridge_config.database_path)
    ledger.initialize()
    monkeypatch.setattr('fox2_agent_bridge.ledger.BRIDGE_ROOT', bridge_config.bridge_root)
    assert ledger.requires_service() and not ledger.spawn_permitted()
    app = BridgeApp(bridge_config); app._started = True; app.ledger = ledger
    with pytest.raises(StartupBlocked, match='F1 service'):
        app.copilot_smoke(worktree=bridge_config.worktree_root)


def test_installed_interpreter_cannot_use_forged_single_root_at_alternate_database(tmp_path, monkeypatch):
    from fox2_agent_bridge import ledger as module
    db = SQLiteLedger(tmp_path / 'alternate' / 'bridge.db')
    db.initialize()
    installed = tmp_path / 'installed'
    monkeypatch.setattr(module, 'BRIDGE_ROOT', installed)
    monkeypatch.setattr(module.sys, 'executable', str(installed / 'runtime/Scripts/python.exe'))
    assert db.requires_service() and not db.spawn_permitted()
    assert not db.claim_dispatch(dispatch_id='FOX2-forged', payload_hash='a' * 64,
        execution_id='fixture', observed_at_utc='2026-10-21T00:00:00+00:00')
