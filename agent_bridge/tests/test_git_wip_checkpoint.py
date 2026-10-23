"""WIP Git recovery tests: local bare remote only, no Agent/process/real host."""
from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import WorkspaceBlocked
from fox2_agent_bridge.git_wip_checkpoint import WipGrant
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now


def git(args, *, binary=False, extra_env=None, check=True):
    import os
    result = subprocess.run(
        ["git", *args], capture_output=True, text=not binary,
        encoding=None if binary else "utf-8",
        env={**os.environ, **extra_env} if extra_env else None,
        check=False)
    if check and result.returncode:
        raise WorkspaceBlocked("fixture Git error: " + str(result.stderr)[-250:])
    return result


@pytest.fixture
def wip_env(tmp_path):
    bare = tmp_path / "bare.git"
    worktree = tmp_path / "task"
    git(["init", "--bare", str(bare)])
    git(["init", str(worktree)])
    git(["-C", str(worktree), "config", "user.name", "WIP test"])
    git(["-C", str(worktree), "config", "user.email", "wip@local.invalid"])
    branch = "work/FOX2-wip-task"
    git(["-C", str(worktree), "checkout", "-b", branch])
    (worktree / "src").mkdir()
    (worktree / "src" / "result.py").write_text("print('base')\n")
    git(["-C", str(worktree), "add", "--", "src/result.py"])
    git(["-C", str(worktree), "commit", "-m", "base"])
    git(["-C", str(worktree), "remote", "add", "origin", str(bare)])
    git(["-C", str(worktree), "push", "origin", branch])
    base = git(["-C", str(worktree), "rev-parse", "HEAD"]).stdout.strip()
    (worktree / "src" / "result.py").write_text("print('partial WIP')\n")
    dispatch = "FOX2-DISPATCH-WIP-001"
    attempt = "FOX2-EXECUTION-001"
    wp = "FOX2-BRIDGE-RC1-TO-INTERNAL-READY"
    ledger = SQLiteLedger(tmp_path / "state.db")
    ledger.initialize()
    payload_sha = "d" * 64
    assert ledger.claim_dispatch(
        dispatch_id=dispatch, payload_hash=payload_sha,
        execution_id=attempt, observed_at_utc=utc_now())
    payload = {
        "delivery_owner": "BRIDGE", "dispatch_id": dispatch,
        "wp_id": wp, "branch": branch, "worktree": str(worktree),
        "allowed_code_paths": ["src/**"], "allowed_report_paths": ["reports/**"]
    }
    ledger.checkpoint(attempt, "AGENT_EXITED", {
        "payload": payload, "before_head": base, "agent_exit_code": 75,
        "execution_tuple": None})
    ledger.finish_execution(
        dispatch_id=dispatch, execution_id=attempt,
        dispatch_state="NEEDS_RECONCILIATION",
        execution_state="NEEDS_RECONCILIATION",
        finished_at_utc=utc_now(),
        result={"agent_exit_code": 75, "error": "QUOTA", "wip": "LOCAL_EVIDENCE"},
        error_code="QUOTA", error_message="fixture quota")
    runner = object.__new__(BridgeE2ERunner)
    runner.ledger = ledger
    runner.config = SimpleNamespace(
        tool_paths={"git": "git"}, local_repo=worktree, worktree_root=tmp_path)
    grant = WipGrant(
        dispatch_id=dispatch, execution_id=attempt, wp_id=wp,
        task_branch=branch, recovery_branch="work/FOX2-BRIDGE-WIP-A01",
        before_head=base, payload_sha256=payload_sha,
        grant_source_sha="a" * 40, grant_sha256="b" * 64,
        changed_paths=("src/result.py",),
        report_path=f"reports/{wp}/wip_incomplete.json",
        test_status="NOT_RUN", failure_kind="QUOTA")
    return SimpleNamespace(
        worktree=worktree, bare=bare, ledger=ledger, runner=runner,
        grant=grant, base=base, dispatch=dispatch, attempt=attempt)


def publish(env, *, grant=None, authority=None, quiescence=None, writer=None):
    return env.runner._publish_authorized_wip(
        grant=grant or env.grant,
        authority_verifier=authority if authority is not None else lambda _: True,
        quiescence_verifier=quiescence if quiescence is not None else lambda _: True,
        writer_verifier=writer if writer is not None else lambda _id, _root: True)


def test_wip_real_git_ref_sha_only_once_and_original_failure_preserved(wip_env):
    e = wip_env
    original_index = git(["-C", str(e.worktree), "ls-files", "--stage"]).stdout
    original_head = git(["-C", str(e.worktree), "rev-parse", "HEAD"]).stdout.strip()
    first = publish(e)
    assert first["status"] == "WIP_INCOMPLETE"
    assert first["acceptance"] == "NOT_ACCEPTED"
    assert first["test_status"] == "NOT_RUN"
    commit = first["remote_commit_sha"]
    assert len(commit) == 40 and commit != e.base
    assert commit == git(["--git-dir", str(e.bare), "rev-parse",
                          "refs/heads/" + e.grant.recovery_branch]).stdout.strip()
    assert e.base == git(["--git-dir", str(e.bare), "rev-parse",
                          "refs/heads/" + e.grant.task_branch]).stdout.strip()
    assert original_head == git(["-C", str(e.worktree), "rev-parse", "HEAD"]).stdout.strip()
    assert original_index == git(["-C", str(e.worktree), "ls-files", "--stage"]).stdout
    assert "src/result.py" in git(
        ["-C", str(e.worktree), "status", "--porcelain"]).stdout
    report_raw = git(["-C", str(e.worktree), "show",
                      f"{commit}:{e.grant.report_path}", "--"]).stdout
    manifest = json.loads(report_raw)
    assert manifest["status"] == "WIP_INCOMPLETE"
    assert manifest["acceptance"] == "NOT_ACCEPTED"
    assert manifest["test_status"] == "NOT_RUN"
    assert manifest["changed_paths"] == ["src/result.py"]
    assert e.ledger.wip_intent(e.attempt)["state"] == "REMOTE_VERIFIED"
    assert e.ledger.dispatch_status(e.dispatch)["dispatch_state"] == "NEEDS_RECONCILIATION"
    assert not e.ledger.claim_dispatch(
        dispatch_id=e.dispatch, payload_hash="d" * 64,
        execution_id="FOX2-EXECUTION-REPLAY", observed_at_utc=utc_now())
    again = publish(e)
    assert again["remote_commit_sha"] == commit
    assert git(["--git-dir", str(e.bare), "rev-list", "--count",
                "refs/heads/" + e.grant.recovery_branch]).stdout.strip() == "2"


@pytest.mark.parametrize("auth,quiet,writer", [
    (None, None, None),
    (lambda g: False, lambda i: True, lambda i, p: True),
    (lambda g: True, lambda i: False, lambda i, p: True),
    (lambda g: True, lambda i: True, None),
    (lambda g: True, lambda i: True, lambda i, p: False),
])
def test_wip_requires_real_host_verifier_callbacks(wip_env, auth, quiet, writer):
    with pytest.raises(WorkspaceBlocked):
        wip_env.runner._publish_authorized_wip(
            grant=wip_env.grant,
            authority_verifier=auth, quiescence_verifier=quiet,
            writer_verifier=writer)
    assert wip_env.ledger.wip_intent(wip_env.attempt) is None
    remote = git(["--git-dir", str(wip_env.bare), "show-ref",
                  "--verify", "refs/heads/" + wip_env.grant.recovery_branch],
                 check=False)
    assert remote.returncode != 0


@pytest.mark.parametrize("modifier", [
    lambda g: replace(g, recovery_branch=g.task_branch),
    lambda g: replace(g, recovery_branch="main"),
    lambda g: replace(g, recovery_branch="work/FOX2-invalid"),
    lambda g: replace(g, before_head="0" * 40),
    lambda g: replace(g, changed_paths=("../exfiltrate",)),
    lambda g: replace(g, changed_paths=("src/result.py", "unexpected.py")),
    lambda g: replace(g, test_status="PASS"),
    lambda g: replace(g, report_path="../bad"),
])
def test_wip_mismatched_or_unsafe_grant_denied(wip_env, modifier):
    with pytest.raises(WorkspaceBlocked):
        publish(wip_env, grant=modifier(wip_env.grant))
    assert wip_env.ledger.wip_intent(wip_env.attempt) is None


def test_wip_scope_drift_or_secret_blocks_before_durable_intent(wip_env):
    e = wip_env
    (e.worktree / "src" / "extra.py").write_text("unexpected")
    with pytest.raises(WorkspaceBlocked, match="differ"):
        publish(e)
    assert e.ledger.wip_intent(e.attempt) is None
    (e.worktree / "src" / "extra.py").unlink()
    (e.worktree / "src" / "result.py").write_text(
        "token = 'github_pat_" + "X" * 30 + "'\n")
    with pytest.raises(WorkspaceBlocked, match="secret"):
        publish(e)
    assert e.ledger.wip_intent(e.attempt) is None


def test_wip_existing_remote_branch_cannot_be_overwritten(wip_env):
    e = wip_env
    git(["-C", str(e.worktree), "push", "origin",
         f"{e.base}:refs/heads/{e.grant.recovery_branch}"])
    with pytest.raises(WorkspaceBlocked, match="already exists"):
        publish(e)
    assert e.ledger.wip_intent(e.attempt) is None


def test_wip_uncertain_push_recovers_same_committed_sha(wip_env, monkeypatch):
    e = wip_env
    original_git = e.runner._git
    seen = []
    def fails_once(args, **kwargs):
        if "push" in args and e.grant.recovery_branch in args[-1] and not seen:
            seen.append(True)
            raise WorkspaceBlocked("simulated network loss after durable intent")
        return original_git(args, **kwargs)
    monkeypatch.setattr(e.runner, "_git", fails_once)
    with pytest.raises(WorkspaceBlocked):
        publish(e)
    intent = e.ledger.wip_intent(e.attempt)
    assert intent["state"] == "PREPARED"
    committed = intent["commit_sha"]
    assert e.ledger.dispatch_status(e.dispatch)["dispatch_state"] == "NEEDS_RECONCILIATION"
    final = publish(e)
    assert final["remote_commit_sha"] == committed
    assert e.ledger.wip_intent(e.attempt)["state"] == "REMOTE_VERIFIED"


def test_ledger_wip_intent_is_immutable_and_does_not_mark_dispatch_done(wip_env):
    e = wip_env
    publish(e)
    intent = e.ledger.wip_intent(e.attempt)
    from fox2_agent_bridge.errors import DatabaseError
    with pytest.raises(DatabaseError, match="different immutable"):
        e.ledger.prepare_wip_intent(
            dispatch_id=e.dispatch, execution_id=e.attempt,
            intent_sha256="f" * 64, recovery_ref=e.grant.recovery_branch,
            before_head=e.base, commit_sha=intent["commit_sha"])
    assert e.ledger.dispatch_status(e.dispatch)["dispatch_state"] == "NEEDS_RECONCILIATION"


def test_wip_remote_lookup_uses_task_repo_even_from_another_repo(wip_env, tmp_path, monkeypatch):
    unrelated = tmp_path / "unrelated"
    git(["init", str(unrelated)])
    monkeypatch.chdir(unrelated)
    result = publish(wip_env)
    assert result["remote_commit_sha"] == wip_env.ledger.wip_intent(wip_env.attempt)["commit_sha"]


def test_wip_accepts_runner_generated_uuid_execution(wip_env):
    from uuid import uuid4
    e = wip_env
    execution = str(uuid4())
    # Fixture substitutes the runner's real UUID shape on the same consumed row.
    with e.ledger.connect() as conn:
        conn.execute("UPDATE executions SET execution_id=? WHERE execution_id=?",
                     (execution, e.attempt))
    grant = replace(e.grant, execution_id=execution)
    assert publish(e, grant=grant)["execution_id"] == execution


def test_wip_manifest_must_be_in_original_report_allowlist(wip_env):
    e = wip_env
    row = e.ledger.dispatch_status(e.dispatch)
    context = row["checkpoint"]
    context["payload"]["allowed_report_paths"] = ["reports/other/**"]
    e.ledger.checkpoint(e.attempt, "AGENT_EXITED", context)
    with pytest.raises(WorkspaceBlocked, match="outside dispatch scope"):
        publish(e)
    assert e.ledger.wip_intent(e.attempt) is None


def test_wip_lost_quiescence_after_commit_preserves_intent_without_push(wip_env):
    observations = iter((True, False))
    with pytest.raises(WorkspaceBlocked, match="changed before push"):
        publish(wip_env, quiescence=lambda _: next(observations))
    intent = wip_env.ledger.wip_intent(wip_env.attempt)
    assert intent["state"] == "PREPARED"
    assert git(["--git-dir", str(wip_env.bare), "show-ref", "--verify",
                "refs/heads/" + wip_env.grant.recovery_branch], check=False).returncode != 0
    assert publish(wip_env)["remote_commit_sha"] == intent["commit_sha"]


def test_wip_push_completed_but_readback_failed_reuses_same_sha(wip_env, monkeypatch):
    e = wip_env
    original = e.runner._git
    pushed = []
    def lost_readback(args, **kwargs):
        if "ls-remote" in args and pushed:
            raise WorkspaceBlocked("offline after push")
        result = original(args, **kwargs)
        if "push" in args:
            pushed.append(args)
        return result
    monkeypatch.setattr(e.runner, "_git", lost_readback)
    with pytest.raises(WorkspaceBlocked, match="offline"):
        publish(e)
    intent = e.ledger.wip_intent(e.attempt)
    assert intent["state"] == "PREPARED"
    monkeypatch.setattr(e.runner, "_git", original)
    assert publish(e)["remote_commit_sha"] == intent["commit_sha"]
    assert len(pushed) == 1


def test_wip_root_outside_host_boundary_never_stages_or_pushes(wip_env):
    from fox2_agent_bridge.errors import BridgeError
    e = wip_env
    e.runner.config.worktree_root = e.worktree / "other-root"
    with pytest.raises(BridgeError):
        publish(e)
    assert e.ledger.wip_intent(e.attempt) is None
    assert git(["--git-dir", str(e.bare), "show-ref", "--verify",
                "refs/heads/" + e.grant.recovery_branch], check=False).returncode != 0


def test_wip_writer_lease_revoked_before_push_preserves_exact_intent(wip_env):
    observations = iter((True, False))
    with pytest.raises(WorkspaceBlocked, match="changed before push"):
        publish(wip_env, writer=lambda _id, _root: next(observations))
    intent = wip_env.ledger.wip_intent(wip_env.attempt)
    assert intent["state"] == "PREPARED"
    assert publish(wip_env)["remote_commit_sha"] == intent["commit_sha"]
