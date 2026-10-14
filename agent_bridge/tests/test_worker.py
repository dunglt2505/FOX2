from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from fox2_agent_bridge.app import BridgeApp
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import DatabaseError, LockHeld, TransportFailure, WorkspaceBlocked
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now
from fox2_agent_bridge.worker import BackgroundWorker, LocalWake, control_worker
from test_delivery_hotfix import recovery


class Mailbox:
    def __init__(self):
        self.sha = "b" * 40
        self.blobs = {}
        self.calls = {name: 0 for name in ("query", "fetch", "scan", "read")}
        self.offline = False
        self.fetch_error = False

    def publish(self, identity="dispatch-1", auto=True):
        path = f"docs/agent_handoff/task/dispatch/{identity}.json"
        self.blobs[path] = json.dumps({"dispatch_id": identity, "agent": {"product": "CODEX"},
                                      "runtime_contract": {"auto_execute": auto}}).encode()
        self.sha = ("c" if self.sha == "b" * 40 else "d") * 40
        return path

    def initialize(self): pass

    def query_control_sha(self, branch):
        self.calls["query"] += 1
        if self.offline:
            raise TransportFailure("offline fixture")
        return self.sha

    def fetch_control(self, branch, expected_sha):
        self.calls["fetch"] += 1
        assert expected_sha == self.sha
        if self.fetch_error:
            raise TransportFailure("fetch fixture failed")
        return expected_sha

    def tree_candidates(self, sha):
        self.calls["scan"] += 1
        return [{"control_commit_sha": sha, "dispatch_path": path,
                 "dispatch_blob_sha": "e" * 40, "discovery_state": "DISCOVERED"}
                for path in self.blobs]

    def changed_candidates(self, sha): return self.tree_candidates(sha)
    def is_ancestor(self, old, new): return True
    def commits_between(self, old, new): return (new,)

    def read_dispatch_blob(self, sha, path):
        self.calls["read"] += 1
        assert sha == self.sha
        return self.blobs[path], "e" * 40


class FakeWake:
    def __init__(self):
        self.now = 0.0
        self.waits = []
        self.closed = False
        self.callback = None

    def wait(self, seconds):
        self.waits.append(seconds)
        if self.callback:
            return self.callback(seconds)
        self.now += seconds
        return False

    def set(self): pass
    def close(self): self.closed = True


@pytest.fixture
def system(bridge_config, monkeypatch):
    app = BridgeApp(bridge_config)
    app.start()
    mailbox = Mailbox()
    wake = FakeWake()
    launches = []

    def execute(core, *, dispatch_path, control_sha, worker_stop_sequence, **kwargs):
        raw, _ = mailbox.read_dispatch_blob(control_sha, dispatch_path)
        identity = json.loads(raw)["dispatch_id"]
        assert core.ledger.claim_dispatch(dispatch_id=identity, payload_hash="fixture",
            execution_id=identity, observed_at_utc=utc_now(), worker_stop_sequence=worker_stop_sequence)
        launches.append(identity)
        core.ledger.finish_execution(dispatch_id=identity, execution_id=identity,
            dispatch_state="PUSHED_UNREVIEWED", execution_state="PUSHED_UNREVIEWED",
            finished_at_utc=utc_now())
        return SimpleNamespace(status="PUSHED_UNREVIEWED", as_dict=lambda: {"status": "PUSHED_UNREVIEWED"})

    monkeypatch.setattr(BridgeE2ERunner, "run_once", execute)
    worker = BackgroundWorker(app, transport=mailbox, wake=wake, clock=lambda: wake.now)
    yield SimpleNamespace(app=app, mailbox=mailbox, wake=wake, launches=launches, worker=worker)
    app.shutdown()


def test_idle_unchanged_zero_fetch_scan_and_agent(system):
    s = system
    assert s.worker.iteration()["state"]["delay_seconds"] == 30
    baseline = dict(s.mailbox.calls)
    for _ in range(3):
        assert s.worker.iteration()["poll"]["status"] == "NO_CHANGE"
    assert s.mailbox.calls == {**baseline, "query": baseline["query"] + 3}
    assert s.launches == []


def test_changed_exact_fetch_then_execute_once_and_terminal_resume(system):
    s = system
    s.worker.iteration()
    s.mailbox.publish()
    assert len(s.worker.iteration()["executions"]) == 1
    assert s.mailbox.calls["fetch"] == 2
    s.app.ledger.worker_control("pause")
    s.worker.iteration()
    s.app.ledger.worker_control("resume")
    s.worker.iteration()
    assert s.launches == ["dispatch-1"]


def test_changed_without_opt_in_never_executes(system):
    system.mailbox.publish(auto=False)
    system.worker.iteration()
    assert system.mailbox.calls["fetch"] == 1
    assert system.launches == []


def test_backoff_capped_persisted_and_contact_resets(system):
    s = system
    s.mailbox.offline = True
    assert [s.worker.iteration()["state"]["delay_seconds"] for _ in range(6)] == [30, 60, 120, 300, 300, 300]
    reopened = SQLiteLedger(s.app.config.database_path)
    assert reopened.worker_state()["failures"] == 4
    s.mailbox.offline = False
    s.mailbox.fetch_error = True
    assert s.worker.iteration()["state"]["delay_seconds"] == 30
    assert reopened.worker_state()["failures"] == 0
    s.mailbox.fetch_error = False
    assert s.worker.iteration()["state"]["delay_seconds"] == 30


def test_pause_persists_and_resume_discovers_pending_without_fetch(system):
    s = system
    s.app.ledger.worker_control("pause")
    s.mailbox.publish()
    s.worker.iteration()
    assert s.launches == []
    restarted = BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake())
    assert restarted.ledger.worker_state()["paused"] is True
    s.app.ledger.worker_control("resume")
    before = s.mailbox.calls["fetch"]
    restarted.iteration()
    assert s.launches == ["dispatch-1"]
    assert s.mailbox.calls["fetch"] == before


def test_task_published_while_stopped_discovered_on_restart(system):
    s = system
    s.worker.iteration()
    s.app.shutdown()
    s.mailbox.publish()
    s.app.start()
    restarted = BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake())
    restarted.iteration()
    assert s.launches == ["dispatch-1"]


def test_crash_after_discovery_cursor_commit_loses_no_dispatch(system, monkeypatch):
    s = system
    s.mailbox.publish()
    monkeypatch.setattr(s.worker.ops, "run_discovered", lambda **kwargs: (_ for _ in ()).throw(RuntimeError("crash")))
    with pytest.raises(RuntimeError):
        s.worker.iteration()
    state = s.app.ledger.worker_state()
    assert state["processed_sha"] is None
    assert s.app.ledger.get_control_cursor(s.app.config.repository, s.app.config.control_branch) == s.mailbox.sha
    restarted = BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake())
    restarted.iteration()
    assert s.launches == ["dispatch-1"]


def test_crash_after_execution_before_processed_checkpoint_never_replays(system, monkeypatch):
    s = system
    s.mailbox.publish()
    original = s.app.ledger.worker_state
    def crash(**updates):
        if "processed_sha" in updates:
            raise RuntimeError("checkpoint crash")
        return original(**updates)
    monkeypatch.setattr(s.app.ledger, "worker_state", crash)
    with pytest.raises(RuntimeError):
        s.worker.iteration()
    monkeypatch.setattr(s.app.ledger, "worker_state", original)
    BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake()).iteration()
    assert s.launches == ["dispatch-1"]


@pytest.mark.parametrize("terminal", ["INTERRUPTED", "DELIVERY_RECOVERY_REQUIRED", "PUSHED_UNREVIEWED"])
def test_restart_reconciliation_never_relaunches_claimed_dispatch(system, terminal):
    s = system
    s.mailbox.publish()
    s.app.ledger.claim_dispatch(dispatch_id="dispatch-1", payload_hash="fixture",
                               execution_id="prior", observed_at_utc=utc_now())
    if terminal != "INTERRUPTED":
        s.app.ledger.finish_execution(dispatch_id="dispatch-1", execution_id="prior",
            dispatch_state=terminal, execution_state=terminal, finished_at_utc=utc_now())
    s.app.shutdown()
    s.app.start()
    BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake()).iteration()
    assert s.app.ledger.dispatch_state("dispatch-1")["state"] == terminal
    assert s.launches == []


@pytest.mark.parametrize("control", ["pause", "stop"])
def test_control_inside_claim_transaction_blocks_launch(system, control):
    s = system
    s.app.ledger.worker_control(control)
    with pytest.raises(WorkspaceBlocked, match="before dispatch claim"):
        s.app.ledger.claim_dispatch(dispatch_id="new", payload_hash="fixture", execution_id="new",
            observed_at_utc=utc_now(), worker_stop_sequence=s.worker.stop_sequence)
    assert s.app.ledger.dispatch_state("new") is None


def test_pause_does_not_abandon_already_claimed_task(system, monkeypatch):
    s = system
    original = s.app.ledger.finish_execution
    def pause_during_task(**kwargs):
        assert s.app.ledger.dispatch_status("dispatch-1")["execution_state"] == "RUNNING"
        s.app.ledger.worker_control("pause")
        return original(**kwargs)
    monkeypatch.setattr(s.app.ledger, "finish_execution", pause_during_task)
    s.mailbox.publish()
    s.worker.iteration()
    assert s.app.ledger.dispatch_state("dispatch-1")["state"] == "PUSHED_UNREVIEWED"
    s.app.ledger.worker_control("resume")
    s.worker.iteration()
    assert s.launches == ["dispatch-1"]


def test_second_worker_profile_cannot_start(system):
    competing = BridgeApp(system.app.config)
    with pytest.raises(LockHeld):
        competing.start()
    assert not competing._started
    assert system.launches == []


def test_two_workers_in_same_runtime_cannot_run(system):
    s = system
    s.app._worker_guard.acquire()
    try:
        with pytest.raises(LockHeld, match="another Worker"):
            s.worker.run()
    finally:
        s.app._worker_guard.release()
    assert s.mailbox.calls["query"] == 0
    assert s.wake.closed


def test_fake_clock_healthy_wait_check_now_and_graceful_stop(system):
    s = system
    def wake(seconds):
        assert seconds == 30
        s.wake.now += 0.01
        if len(s.wake.waits) == 1:
            s.app.ledger.worker_control("check-now")
        else:
            s.app.ledger.worker_control("stop")
        return True
    s.wake.callback = wake
    s.worker.run()
    assert s.wake.waits == [30, 30]
    assert s.wake.now == 0.02
    assert s.mailbox.calls["query"] == 2
    assert s.wake.closed


def test_windows_local_wake_cross_handle_no_listener(tmp_path):
    owner = LocalWake(tmp_path)
    control = LocalWake(tmp_path)
    try:
        assert owner.wait(0) is False
        control.set()
        assert owner.wait(0) is True
        assert owner.wait(0) is False
    finally:
        owner.close()
        control.close()


def test_worker_controls_cli_operate_while_runtime_lock_held(system, monkeypatch, capsys):
    from fox2_agent_bridge.__main__ import main
    monkeypatch.setattr(BridgeApp, "from_file", classmethod(lambda cls, config_path=None: system.app))
    monkeypatch.setattr("fox2_agent_bridge.worker.LocalWake", lambda profile: FakeWake())
    for command in ("pause", "status", "resume", "check-now", "stop"):
        assert main([f"worker-{command}"]) == 0
        assert "paused" in json.loads(capsys.readouterr().out)
    assert system.app._started
    assert system.launches == []


def test_worker_state_preserves_existing_rows_and_future_schema_refusal(system):
    s = system
    s.app.ledger.worker_control("pause")
    s.app.ledger.worker_state(observed_sha="a" * 40)
    assert s.app.ledger.worker_state()["paused"] is True
    with s.app.ledger.connect() as connection:
        connection.execute("UPDATE bridge_meta SET value='999' WHERE key='schema_version'")
    with pytest.raises(DatabaseError, match="supported ledger schema"):
        s.app.ledger.worker_control("resume")
    with pytest.raises(DatabaseError):
        s.app.ledger.worker_state()


def test_worker_reuses_real_e2e_hotfix_route(recovery, monkeypatch):
    r = recovery
    # Run the actual E2E method with the Worker checkpoint, not another executor.
    calls = []
    monkeypatch.setattr(r.runner, "_resolve_worktree", lambda payload: (r.worktree, "a" * 40))
    monkeypatch.setattr(r.runner, "_resolve_prompt", lambda payload: "prompt")
    monkeypatch.setattr("fox2_agent_bridge.e2e_runner.CodexAdapter.run_prompt",
                        lambda *a, **k: calls.append("agent") or r.agent)
    monkeypatch.setattr(r.runner, "_commit_and_push_codex_result", lambda **kwargs: ("f" * 40, ()))
    # A supplied fetched SHA must avoid a second poll/query/fetch.
    def forbidden(*a, **k): raise AssertionError("redundant Git contact")
    monkeypatch.setattr(r.transport, "query_control_sha", forbidden)
    monkeypatch.setattr(r.transport, "fetch_control", forbidden)
    result = r.runner.run_once(dispatch_path=r.path, control_sha="b" * 40, worker_stop_sequence=0)
    assert result.status == "PUSHED_UNREVIEWED"
    assert calls == ["agent"]


def test_multiple_pending_dispatches_drain_before_idle_checkpoint(system):
    s = system
    s.mailbox.publish("first")
    s.mailbox.publish("second")
    s.worker.iteration()
    assert set(s.launches) == {"first", "second"}
    assert s.app.ledger.worker_state()["processed_sha"] == s.mailbox.sha
    before = dict(s.mailbox.calls)
    s.worker.iteration()
    assert s.mailbox.calls == {**before, "query": before["query"] + 1}


def test_cursor_discovery_transaction_failure_is_retryable(system, monkeypatch):
    s = system
    s.mailbox.publish()
    original = s.app.ledger.record_poll_success
    def fail(**kwargs):
        raise DatabaseError("discovery commit failed")
    monkeypatch.setattr(s.app.ledger, "record_poll_success", fail)
    with pytest.raises(DatabaseError):
        s.worker.iteration()
    assert s.app.ledger.get_control_cursor(s.app.config.repository, s.app.config.control_branch) is None
    monkeypatch.setattr(s.app.ledger, "record_poll_success", original)
    BackgroundWorker(s.app, transport=s.mailbox, wake=FakeWake()).iteration()
    assert s.launches == ["dispatch-1"]


def test_successful_ref_observation_survives_offline_contact(system):
    s = system
    s.worker.iteration()
    s.mailbox.offline = True
    s.worker.iteration()
    assert SQLiteLedger(s.app.config.database_path).worker_state()["observed_sha"] == "b" * 40


def test_transient_blob_read_failure_cannot_checkpoint_away_valid_dispatch(system, monkeypatch):
    s = system
    s.mailbox.publish()
    original = s.mailbox.read_dispatch_blob
    def fail(*args): raise TransportFailure("interrupted blob read")
    monkeypatch.setattr(s.mailbox, "read_dispatch_blob", fail)
    assert s.worker.iteration()["state"]["poll_status"] == "EXECUTION_BLOCKED"
    assert s.app.ledger.worker_state()["processed_sha"] is None
    monkeypatch.setattr(s.mailbox, "read_dispatch_blob", original)
    s.worker.iteration()
    assert s.launches == ["dispatch-1"]


def test_production_git_fetch_is_exact_control_ref_and_pinned(tmp_path, monkeypatch):
    import subprocess
    from fox2_agent_bridge.dispatch_poller import GitTransport, CONTROL_REF, OBSERVED_REF_PREFIX
    transport = GitTransport(git_executable="git", store_path=tmp_path / "control.git")
    calls = []
    def run(arguments, **kwargs):
        calls.append(arguments)
        return subprocess.CompletedProcess(arguments, 0, "a" * 40 if arguments[0] == "rev-parse" else "", "")
    monkeypatch.setattr(transport, "_run", run)
    assert transport.fetch_control("work/control", "a" * 40) == "a" * 40
    assert calls == [
        ["fetch", "--no-tags", "--no-write-fetch-head", "origin", f"+refs/heads/work/control:{CONTROL_REF}"],
        ["rev-parse", "--verify", f"{CONTROL_REF}^{{commit}}"],
        ["update-ref", f"{OBSERVED_REF_PREFIX}/{'a' * 40}", "a" * 40],
    ]
