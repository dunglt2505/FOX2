from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import replace
from types import SimpleNamespace
from pathlib import Path

import pytest

from fox2_agent_bridge.__main__ import build_parser
from fox2_agent_bridge.codex_adapter import CodexRunResult
from fox2_agent_bridge.dispatch_poller import _git_error_text, GitTransport
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import WorkspaceBlocked, TransportFailure
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now
from fox2_agent_bridge.ops_runner import BridgeOps
from test_e2e_runner import _dispatch_payload


@pytest.mark.parametrize("staged", [True, False])
@pytest.mark.parametrize("content,passes", [(b"hello\r\n", True), (b"hello \r\n", False), (b"hello\t\n", False)])
def test_staged_whitespace_preserves_bytes(tmp_path, bridge_config, content, passes, staged):
    # Build an index with Git plumbing; no task-worktree staging or history changes.
    git = shutil.which("git")
    def run(*args, data=None):
        return subprocess.run([git, "-C", str(tmp_path), *args], input=data,
                              capture_output=True, check=True).stdout.strip()
    run("init")
    (tmp_path / ".gitattributes").write_bytes(b"reports/** -text\n")
    (tmp_path / "reports").mkdir()
    target = tmp_path / "reports" / "evidence.txt"
    target.write_bytes(content)
    blob = run("hash-object", "-w", "--stdin", data=content if staged else b"old\n").decode()
    run("update-index", "--add", "--cacheinfo", "100644", blob, "reports/evidence.txt")
    config = replace(bridge_config, tool_paths={"git": Path(git)})
    runner = BridgeE2ERunner(config, SQLiteLedger(tmp_path / "unused.db"))
    args = ["-C", str(tmp_path), "-c",
            "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol",
            "diff", *(["--cached"] if staged else []), "--check"]
    if passes:
        runner._git(args)
    else:
        with pytest.raises(WorkspaceBlocked, match="trailing whitespace"):
            runner._git(args)
    assert target.read_bytes() == content


@pytest.mark.parametrize("stdout,stderr", [("useful stdout diagnostic", ""), ("", "useful stderr diagnostic")])
def test_git_diagnostics_both_wrappers(tmp_path, bridge_config, monkeypatch, stdout, stderr):
    result = subprocess.CompletedProcess([], 1, stdout, stderr)
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: result)
    runner = BridgeE2ERunner(bridge_config, SQLiteLedger(tmp_path / "unused.db"))
    with pytest.raises(WorkspaceBlocked, match="useful"):
        runner._git(["diff", "--check"])
    transport = GitTransport(git_executable="git", store_path=tmp_path / "control.git")
    with pytest.raises(TransportFailure, match="useful"):
        transport._run(["diff", "--check"])


def test_combined_diagnostic_is_bounded_and_redacted():
    secret = "github_pat_" + "A" * 30
    out = "https://user:private@github.com/repo token=private " + secret + "x" * 3000
    err = "password=private Bearer abcdef " + "y" * 3000
    message = _git_error_text(subprocess.CompletedProcess([], 1, out.encode(), err.encode()))
    assert len(message) <= 2000
    assert "stdout:" in message and "stderr:" in message
    assert "private" not in message and secret not in message and "abcdef" not in message


@pytest.fixture
def recovery(tmp_path, bridge_config, monkeypatch):
    monkeypatch.setattr("fox2_agent_bridge.config.WORKTREE_ROOT", tmp_path / "worktrees")
    config = replace(bridge_config, worktree_root=tmp_path / "worktrees")
    worktree = config.worktree_root / "task"
    worktree.mkdir(parents=True)
    (worktree / ".git").write_text("gitdir: fake")
    payload = _dispatch_payload(worktree)
    payload["agent"] = {"product": "CODEX", "interface": "OPENAI_CODEX_CLI"}
    payload["execution_path"] = "BRIDGE_DIRECT_CODEX_CLI"
    payload["runtime_contract"] = {"auto_execute": True}
    payload["acceptance"] = {"stdout_contains": "READY", "required_paths": ["reports/FOX2-BRIDGE-E2E-CANARY/result.txt"]}
    target = worktree / "reports/FOX2-BRIDGE-E2E-CANARY/result.txt"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"result\r\n")
    raw = json.dumps(payload).encode()
    path = "docs/agent_handoff/task/dispatch/" + payload["dispatch_id"] + ".json"
    class Transport:
        def query_control_sha(self, branch): return "b" * 40
        def fetch_control(self, branch, sha): return sha
        def read_dispatch_blob(self, sha, dispatch_path):
            assert dispatch_path == path
            return self.raw, "e" * 40
    transport = Transport()
    transport.raw = raw
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    runner = BridgeE2ERunner(config, ledger, transport=transport)
    agent = CodexRunResult("CODEX_EXITED", 0, "READY", "", "codex", str(worktree))
    state = {"head": "a" * 40, "remote": "a" * 40, "branch": payload["branch"],
             "paths": ["reports/FOX2-BRIDGE-E2E-CANARY/result.txt"], "dirty": True,
             "fail_push": False, "calls": []}
    def git(args, **kwargs):
        state["calls"].append(args)
        if "--show-toplevel" in args: out = str(worktree)
        elif "--show-current" in args: out = state["branch"]
        elif "get-url" in args: out = "https://github.com/dunglt2505/FOX2.git"
        elif "rev-parse" in args: out = "a" * 40 if args[-1] == "HEAD^" else state["head"]
        elif "--porcelain" in args: out = " M result" if state["dirty"] else ""
        elif "--name-only" in args or "ls-files" in args: out = "\n".join(state["paths"])
        elif "commit" in args:
            state["head"] = "f" * 40
            state["dirty"] = False
            out = "committed"
        elif "push" in args:
            if state["fail_push"]: raise WorkspaceBlocked("push failure")
            state["remote"] = state["head"]
            out = "pushed"
        else: out = ""
        return subprocess.CompletedProcess(args, 0, out, "")
    monkeypatch.setattr(runner, "_git", git)
    monkeypatch.setattr(runner, "_remote_branch_head", lambda branch: state["remote"])
    def forbidden(*a, **k): raise AssertionError("Agent called during recovery")
    monkeypatch.setattr("fox2_agent_bridge.e2e_runner.CodexAdapter.run_prompt", forbidden)
    monkeypatch.setattr("fox2_agent_bridge.e2e_runner.CopilotAdapter.run_prompt", forbidden)
    return SimpleNamespace(config=config, runner=runner, ledger=ledger, payload=payload,
                           raw=raw, path=path, transport=transport, agent=agent, state=state,
                           worktree=worktree, monkeypatch=monkeypatch)


def seed(r):
    r.ledger.claim_dispatch(dispatch_id=r.payload["dispatch_id"], payload_hash=hashlib.sha256(r.raw).hexdigest(),
                            execution_id="execution", observed_at_utc=utc_now())
    payload = r.runner._validate_dispatch(r.raw, dispatch_path=r.path, observed_blob_sha="e" * 40)
    r.runner._save_delivery_context(payload, r.path, "b" * 40, "e" * 40, "execution",
                                    r.worktree, "a" * 40, r.agent)


def test_successful_agent_delivery_failure_is_terminal_and_not_selected(recovery):
    r = recovery
    r.monkeypatch.setattr("fox2_agent_bridge.e2e_runner.DispatchPoller.poll_once", lambda self: SimpleNamespace(status="NO_CHANGE"))
    r.monkeypatch.setattr(r.runner, "_resolve_worktree", lambda payload: (r.worktree, "a" * 40))
    r.monkeypatch.setattr(r.runner, "_resolve_prompt", lambda payload: "prompt")
    calls = []
    r.monkeypatch.setattr("fox2_agent_bridge.e2e_runner.CodexAdapter.run_prompt", lambda *a, **k: calls.append("agent") or r.agent)
    def fail(**kwargs): raise WorkspaceBlocked("delivery validation failed")
    r.monkeypatch.setattr(r.runner, "_commit_and_push_codex_result", fail)
    with pytest.raises(WorkspaceBlocked): r.runner.run_once(dispatch_path=r.path)
    status = r.ledger.dispatch_status(r.payload["dispatch_id"])
    assert status["dispatch_state"] == status["execution_state"] == "DELIVERY_RECOVERY_REQUIRED"
    assert status["result"]["agent_stdout"] == "READY"
    assert r.state["dirty"] and (r.worktree / "reports/FOX2-BRIDGE-E2E-CANARY/result.txt").read_bytes() == b"result\r\n"
    r.ledger.record_poll_success(repository=r.config.repository, control_branch=r.config.control_branch,
        previous_cursor=None, observed_remote_sha="b" * 40, status="INITIALIZED", observed_at_utc=utc_now(),
        candidates=[{"control_commit_sha": "b" * 40, "dispatch_path": r.path,
                     "dispatch_blob_sha": "e" * 40, "discovery_state": "DISCOVERED"}])
    ops = BridgeOps(r.config, r.ledger, transport=r.transport)
    assert ops.run_next().status == "NO_ELIGIBLE_DISPATCH"
    assert calls == ["agent"]


def test_valid_recovery_commits_pushes_once_and_verifies_remote(recovery):
    r = recovery
    seed(r)
    result = r.runner.recover_delivery(dispatch_path=r.path)
    assert result.status == "PUSHED_UNREVIEWED"
    assert result.after_head == r.state["remote"] == "f" * 40
    assert sum("commit" in c for c in r.state["calls"]) == 1
    assert sum("push" in c for c in r.state["calls"]) == 1
    checks = [c for c in r.state["calls"] if "--check" in c]
    assert len(checks) == 2 and all("core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol" in c for c in checks)
    with pytest.raises(WorkspaceBlocked, match="not awaiting"):
        r.runner.recover_delivery(dispatch_path=r.path)
    assert sum("push" in c for c in r.state["calls"]) == 1


@pytest.mark.parametrize("drift", ["head", "branch", "remote", "scope", "dispatch", "marker", "required"])
def test_recovery_fails_closed(recovery, drift):
    r = recovery
    seed(r)
    if drift in {"head", "branch", "remote"}: r.state[drift] = "9" * 40
    elif drift == "scope": r.state["paths"].append("product/forbidden.py")
    elif drift == "dispatch": r.transport.raw = r.raw.replace(b"READY", b"OTHER")
    elif drift == "required": (r.worktree / "reports/FOX2-BRIDGE-E2E-CANARY/result.txt").unlink()
    else:
        context = r.ledger.dispatch_status(r.payload["dispatch_id"])["result"]
        context["agent_stdout"] = "missing marker"
        r.runner._persist_delivery(context)
    with pytest.raises(WorkspaceBlocked): r.runner.recover_delivery(dispatch_path=r.path)
    assert not any("commit" in c or "push" in c for c in r.state["calls"])
    assert r.ledger.dispatch_state(r.payload["dispatch_id"])["state"] == "DELIVERY_RECOVERY_REQUIRED"


def test_retry_after_commit_does_not_commit_again(recovery):
    r = recovery
    seed(r)
    r.state["fail_push"] = True
    with pytest.raises(WorkspaceBlocked, match="push failure"):
        r.runner.recover_delivery(dispatch_path=r.path)
    assert r.ledger.dispatch_status(r.payload["dispatch_id"])["result"]["delivery_head"] == "f" * 40
    r.state["fail_push"] = False
    assert r.runner.recover_delivery(dispatch_path=r.path).status == "PUSHED_UNREVIEWED"
    assert sum("commit" in c for c in r.state["calls"]) == 1


def test_recovery_cli_requires_exact_dispatch_path():
    args = build_parser().parse_args(["recover-delivery", "--dispatch-path", "exact.json"])
    assert args.command == "recover-delivery" and args.dispatch_path == "exact.json"


def test_recovery_requires_exact_remote_result_sha(recovery):
    r = recovery
    seed(r)
    def no_remote_change(args, **kwargs):
        if "push" in args:
            r.state["calls"].append(args)
            return subprocess.CompletedProcess(args, 0, "", "")
        return original(args, **kwargs)
    original = r.runner._git
    r.monkeypatch.setattr(r.runner, "_git", no_remote_change)
    with pytest.raises(WorkspaceBlocked, match="not pushed"):
        r.runner.recover_delivery(dispatch_path=r.path)
    assert r.ledger.dispatch_state(r.payload["dispatch_id"])["state"] == "DELIVERY_RECOVERY_REQUIRED"


def test_already_pushed_recovery_does_not_push_again(recovery):
    r = recovery
    seed(r)
    r.runner._checkpoint_commit(r.payload["dispatch_id"], "f" * 40)
    r.state.update(head="f" * 40, remote="f" * 40, dirty=False)
    assert r.runner.recover_delivery(dispatch_path=r.path).status == "PUSHED_UNREVIEWED"
    assert not any("commit" in c or "push" in c for c in r.state["calls"])
