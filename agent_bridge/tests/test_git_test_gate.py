"""Required-test success and negatives on a real isolated bare Git remote."""
from __future__ import annotations

from types import SimpleNamespace
import subprocess
import sys

import pytest

from fox2_agent_bridge.errors import WorkspaceBlocked
from fox2_agent_bridge.git_test_gate import verify_test_evidence
from test_git_wip_checkpoint import wip_env, git


def publish_result(e, verifier=None):
    e.runner.required_test_verifier = verifier
    payload = {
        "delivery_owner": "BRIDGE", "branch": e.grant.task_branch,
        "dispatch_id": e.dispatch, "allowed_code_paths": ["src/**"],
        "allowed_report_paths": ["reports/**"], "required_tests": ["python-smoke"],
    }
    result = e.runner._commit_and_push_codex_result(
        payload=payload, worktree=e.worktree, before_head=e.base, agent_stdout="PASS")
    return result, payload


@pytest.mark.parametrize("verifier", [
    None,
    lambda root, tree, names: {"tree_sha": tree, "results": {}},
    lambda root, tree, names: {"tree_sha": tree, "results": {names[0]: "FAIL"}},
    lambda root, tree, names: {"tree_sha": "a" * 40, "results": {names[0]: "PASS"}},
])
def test_missing_failed_or_stale_required_tests_never_commit_or_push(wip_env, verifier):
    e = wip_env
    with pytest.raises(WorkspaceBlocked, match="required tests"):
        publish_result(e, verifier)
    assert git(["-C", str(e.worktree), "rev-parse", "HEAD"]).stdout.strip() == e.base
    assert git(["--git-dir", str(e.bare), "rev-parse",
                "refs/heads/" + e.grant.task_branch]).stdout.strip() == e.base


def test_host_test_command_pass_publishes_exact_tested_tree(wip_env):
    def verify(root, tree, names):
        result = subprocess.run([sys.executable, "src/result.py"], cwd=root,
                                capture_output=True, timeout=10)
        return {"tree_sha": tree, "results": {names[0]: "PASS" if result.returncode == 0 else "FAIL"}}
    (head, paths), payload = publish_result(wip_env, verify)
    assert paths == ("src/result.py",)
    evidence = payload["_bridge_test_evidence"]
    assert evidence["status"] == "PASS"
    assert git(["-C", str(wip_env.worktree), "rev-parse", f"{head}^{{tree}}"]
               ).stdout.strip() == evidence["tree_sha"]


@pytest.mark.parametrize("mutation", ["tracked", "index", "untracked"])
def test_changes_during_host_tests_block_before_commit(wip_env, mutation):
    e = wip_env
    def verify(root, tree, names):
        if mutation == "untracked":
            (root / "new.txt").write_text("new untested output")
        else:
            (root / "src/result.py").write_text("print('untested')\n")
            if mutation == "index":
                git(["-C", str(root), "add", "--", "src/result.py"])
        return {"tree_sha": tree, "results": {names[0]: "PASS"}}
    with pytest.raises(WorkspaceBlocked, match="changed during"):
        publish_result(e, verify)
    assert git(["-C", str(e.worktree), "rev-parse", "HEAD"]).stdout.strip() == e.base


def test_crash_resume_rejects_missing_test_evidence_before_network_push(wip_env):
    e = wip_env
    git(["-C", str(e.worktree), "add", "--", "src/result.py"])
    git(["-C", str(e.worktree), "commit", "-m", "persisted untested result"])
    head = git(["-C", str(e.worktree), "rev-parse", "HEAD"]).stdout.strip()
    context = {
        "payload": {"delivery_owner": "BRIDGE", "branch": e.grant.task_branch,
                    "worktree": str(e.worktree), "allowed_code_paths": ["src/**"],
                    "allowed_report_paths": [], "required_tests": ["python-smoke"]},
        "before_head": e.base, "expected_result_sha": head, "agent_exit_code": 0,
    }
    with pytest.raises(WorkspaceBlocked, match="required tests"):
        e.runner._reconcile_publishing(context)
    assert git(["--git-dir", str(e.bare), "rev-parse",
                "refs/heads/" + e.grant.task_branch]).stdout.strip() == e.base


def test_invalid_required_test_contract_fails_closed():
    with pytest.raises(WorkspaceBlocked, match="invalid required"):
        verify_test_evidence(["same", "same"], "a" * 40, {})


def test_agent_owned_result_cannot_use_stdout_as_required_test_proof(wip_env):
    e = wip_env
    git(["-C", str(e.worktree), "add", "--", "src/result.py"])
    git(["-C", str(e.worktree), "commit", "-m", "Agent fixture result"])
    git(["-C", str(e.worktree), "push", "origin", e.grant.task_branch])
    payload = {"delivery_owner": "AGENT", "branch": e.grant.task_branch,
               "allowed_code_paths": ["src/**"], "allowed_report_paths": [],
               "required_tests": ["python-smoke"]}
    with pytest.raises(WorkspaceBlocked, match="no trusted Bridge"):
        e.runner._verify_result(payload=payload, worktree=e.worktree,
                               before_head=e.base, agent_stdout="ALL TESTS PASS",
                               agent_label="CODEX")


def test_host_test_timeout_is_a_blocker_and_keeps_task_ref(wip_env):
    def timeout(root, tree, names):
        raise subprocess.TimeoutExpired("admitted-test", 10)
    with pytest.raises(WorkspaceBlocked, match="verifier failed"):
        publish_result(wip_env, timeout)
    assert git(["--git-dir", str(wip_env.bare), "rev-parse",
                "refs/heads/" + wip_env.grant.task_branch]).stdout.strip() == wip_env.base
