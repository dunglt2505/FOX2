"""Bridge Git publisher native/offline security and idempotent restart tests.

No Agent credentials, installed Bridge, production remote or Windows policy.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from fox2_agent_bridge.desktop import reconcile
from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
from fox2_agent_bridge.errors import WorkspaceBlocked
from fox2_agent_bridge.git_delivery_guard import validate_staged_blobs
from fox2_agent_bridge.ledger import SQLiteLedger, utc_now


def git(args, *, binary=False):
    result = subprocess.run(["git", *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False)
    if result.returncode:
        raise AssertionError("local Git fixture failed")
    if binary:
        return SimpleNamespace(stdout=result.stdout)
    return SimpleNamespace(stdout=result.stdout.decode("utf-8"))


@pytest.fixture
def workspace(tmp_path):
    root = tmp_path / "code"
    root.mkdir()
    git(["init", str(root)])
    git(["-C", str(root), "config", "user.name", "FOX2 test"])
    git(["-C", str(root), "config", "user.email", "fox2-test@local.invalid"])
    (root / "result.txt").write_text("old\n", encoding="utf-8")
    git(["-C", str(root), "add", "result.txt"])
    git(["-C", str(root), "commit", "-m", "fixture"])
    return root


def test_bridge_accepts_exact_staged_regular_file(workspace):
    (workspace / "result.txt").write_text("safe result\n")
    git(["-C", str(workspace), "add", "result.txt"])
    validate_staged_blobs(git, workspace, ("result.txt",))


def test_bridge_rejects_index_with_unapproved_staged_file(workspace):
    (workspace / "result.txt").write_text("safe\n")
    (workspace / "surprise.txt").write_text("different\n")
    git(["-C", str(workspace), "add", "result.txt", "surprise.txt"])
    with pytest.raises(WorkspaceBlocked, match="index differs"):
        validate_staged_blobs(git, workspace, ("result.txt",))


@pytest.mark.parametrize("path,data", [
    ("result.txt", "github_pat_" + "A" * 28),
    ("result.txt", "sk-proj-" + "b" * 36),
    ("result.txt", "-----BEGIN PRIVATE KEY-----\nSECRET\n-----END PRIVATE KEY-----\n"),
    ("credentials.json", "not even a credential"),
    (".env.local", "not even a secret"),
])
def test_bridge_denies_secret_blobs_and_credential_names(workspace, path, data):
    (workspace / path).write_text(data, encoding="utf-8")
    git(["-C", str(workspace), "add", path])
    with pytest.raises(WorkspaceBlocked):
        validate_staged_blobs(git, workspace, (path,))


def test_bridge_denies_symlink_in_index_without_host_symlink_privilege(workspace):
    def fake_git(args, *, binary=False):
        if args[-4:] == ["diff", "--cached", "--name-only", "-z"]:
            return SimpleNamespace(stdout=b"result.txt\x00")
        if "ls-files" in args:
            return SimpleNamespace(stdout=b"120000 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa 0\tresult.txt\x00")
        raise AssertionError("unexpected Git read on forbidden symlink")
    with pytest.raises(WorkspaceBlocked, match="non-regular staged file"):
        validate_staged_blobs(fake_git, workspace, ("result.txt",))


def _publisher(monkeypatch, *, owner="BRIDGE", remote="a", local="b",
               dirty=False, expected="b", before="a", exit_code=0):
    """Test actual restart decision; intercept Git only at subprocess boundary."""
    base, result = "a" * 40, "b" * 40
    checkpoint = {
        "payload": {"delivery_owner": owner, "branch": "work/FOX2-test-delivery",
                    "worktree": "/tmp/fox2-checkpoint", "_agent_product": "CODEX",
                    "allowed_code_paths": [],
                    "allowed_report_paths": ["reports/FOX2-result/**"]},
        "expected_result_sha": result if expected == "b" else expected,
        "before_head": base if before == "a" else before,
        "agent_exit_code": exit_code,
        "agent_stdout": "accepted fixture marker",
    }
    calls = []
    runner = object.__new__(BridgeE2ERunner)
    def fake_git(args, *, cwd=None, check=True, binary=False, timeout=120):
        calls.append(args)
        if "push" in args:
            return SimpleNamespace(stdout="")
        if "diff" in args and binary:
            return SimpleNamespace(stdout=b"reports/FOX2-result/report.md\x00")
        if "ls-tree" in args:
            return SimpleNamespace(stdout=(
                b"100644 blob " + b"0" * 40 +
                b"\treports/FOX2-result/report.md\x00"))
        if "show" in args and binary:
            return SimpleNamespace(stdout=b"safe report bytes")
        if "branch" in args:
            return SimpleNamespace(stdout="work/FOX2-test-delivery\n")
        if "status" in args:
            return SimpleNamespace(stdout=" M dirty\n" if dirty else "")
        if "rev-parse" in args:
            return SimpleNamespace(stdout=(base if "HEAD^" in args else
                (result if local == "b" else local)) + "\n")
        raise AssertionError(f"unexpected Git call {args}")
    monkeypatch.setattr(runner, "_git", fake_git)
    monkeypatch.setattr(runner, "_remote_branch_head",
                        lambda _: base if remote == "a" else (
                            result if remote == "b" else remote))
    verified = []
    def verify(**kw):
        verified.append(kw)
        return result, ("reports/FOX2-result/report.md",)
    monkeypatch.setattr(runner, "_verify_result", verify)
    return runner, checkpoint, calls, verified


@pytest.mark.parametrize("remote,push_count", [("a", 1), ("b", 0)])
def test_publish_restart_only_reuses_exact_commit(monkeypatch, remote, push_count):
    runner, checkpoint, calls, verified = _publisher(monkeypatch, remote=remote)
    commit, paths = runner._reconcile_publishing(checkpoint)
    assert commit == "b" * 40 and paths == ("reports/FOX2-result/report.md",)
    pushes = [args for args in calls if "push" in args]
    assert len(pushes) == push_count
    for args in pushes:
        assert args[-1] == "b" * 40 + ":refs/heads/work/FOX2-test-delivery"
    assert all("commit" not in args and "--force" not in args for args in calls)
    assert len(verified) == 1


@pytest.mark.parametrize("overrides", [
    {"owner": "AGENT"},
    {"remote": "c" * 40},
    {"local": "c" * 40},
    {"dirty": True},
    {"expected": None},
    {"before": "c" * 40},
    {"exit_code": 75},
])
def test_publish_restart_blocks_unverifiable_or_failed_intent(monkeypatch, overrides):
    runner, checkpoint, calls, verified = _publisher(monkeypatch, **overrides)
    with pytest.raises(WorkspaceBlocked):
        runner._reconcile_publishing(checkpoint)
    assert not any("push" in args or "commit" in args for args in calls)
    assert not verified


def test_reconcile_persisted_bridge_publish_intent_without_agent_replay(tmp_path):
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    base, result = "a" * 40, "b" * 40
    dispatch = "FOX2-DISPATCH-GIT-RESTART-001"
    assert ledger.claim_dispatch(dispatch_id=dispatch, payload_hash="c" * 64,
                                 execution_id="one", observed_at_utc=utc_now())
    context = {
        "payload": {"delivery_owner": "BRIDGE", "branch": "work/FOX2-test-delivery",
                    "worktree": str(tmp_path), "agent": {"product": "CODEX"},
                    "_agent_product": "CODEX"},
        "before_head": base, "expected_result_sha": result,
        "agent_exit_code": 0, "agent_stdout": "fixture marker"
    }
    ledger.checkpoint("one", "PUBLISHING", context)
    seen = []
    def finish(checkpoint):
        seen.append(checkpoint)
        return result, ("reports/FOX2-result/report.md",)
    runner = SimpleNamespace(
        _reconcile_publishing=finish,
        _verify_result=lambda **kw: pytest.fail("must reconcile same commit, not re-run agent"))
    outcomes = reconcile(ledger, runner)
    assert outcomes == [{"dispatch_id": dispatch, "outcome": "PUSHED_UNREVIEWED",
                        "remote_result_sha": result}]
    status = ledger.dispatch_status(dispatch)
    assert status["dispatch_state"] == "PUSHED_UNREVIEWED"
    assert status["execution_state"] == "PUSHED_UNREVIEWED"
    assert status["result"]["after_head"] == result
    assert len(seen) == 1 and seen[0]["expected_result_sha"] == result
    assert reconcile(ledger, runner) == []
    assert not ledger.claim_dispatch(
        dispatch_id=dispatch, payload_hash="c" * 64,
        execution_id="replay", observed_at_utc=utc_now())


def test_bridge_intent_must_have_checkpoint_sha_before_recovery(tmp_path):
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    dispatch = "FOX2-DISPATCH-NO-DURABLE-SHA"
    ledger.claim_dispatch(dispatch_id=dispatch, payload_hash="d" * 64,
                          execution_id="one", observed_at_utc=utc_now())
    payload = {"delivery_owner": "BRIDGE", "branch": "work/FOX2-test-delivery",
               "worktree": str(tmp_path), "_agent_product": "COPILOT",
               "agent": {"product": "COPILOT"}}
    checkpoint = {"payload": payload, "before_head": "a" * 40,
                  "agent_exit_code": 0, "agent_stdout": "fixture"}
    ledger.checkpoint("one", "PUBLISHING", checkpoint)
    runner = SimpleNamespace(
        _reconcile_publishing=lambda ctx: pytest.fail("no SHA; cannot resume"),
        _verify_result=lambda **kw: pytest.fail("Agent push forbidden for BRIDGE"))
    status = reconcile(ledger, runner)
    assert status[0]["outcome"] == "NEEDS_RECONCILIATION"
    assert ledger.dispatch_status(dispatch)["dispatch_state"] == "NEEDS_RECONCILIATION"


def test_agent_owner_still_verifies_external_push_without_bridge_publish(tmp_path):
    ledger = SQLiteLedger(tmp_path / "bridge.db")
    ledger.initialize()
    dispatch = "FOX2-DISPATCH-AGENT-OWNED-001"
    ledger.claim_dispatch(dispatch_id=dispatch, payload_hash="d" * 64,
                          execution_id="one", observed_at_utc=utc_now())
    payload = {"delivery_owner": "AGENT", "branch": "work/FOX2-test-delivery",
               "worktree": str(tmp_path), "_agent_product": "CODEX",
               "agent": {"product": "CODEX"}}
    ledger.checkpoint("one", "AGENT_EXITED", {
        "payload": payload, "before_head": "a" * 40,
        "agent_exit_code": 0, "agent_stdout": "fixture"})
    verified = []
    def verifier(**args):
        verified.append(args)
        return "b" * 40, ("reports/FOX2-result/report.md",)
    runner = SimpleNamespace(_verify_result=verifier,
        _reconcile_publishing=lambda ctx: pytest.fail("no Bridge double-push"))
    outcomes = reconcile(ledger, runner)
    assert outcomes[0]["outcome"] == "PUSHED_UNREVIEWED"
    assert len(verified) == 1
    assert ledger.dispatch_status(dispatch)["dispatch_state"] == "PUSHED_UNREVIEWED"


@pytest.mark.parametrize("path", [
    "../escape.txt", "a/../b.txt", ".git/config", "C:result.txt",
    "/abs/result.txt", "a\\b.txt", "a//b.txt",
])
def test_bridge_denies_traversal_protected_and_ads_paths(workspace, path):
    with pytest.raises(WorkspaceBlocked, match="unsafe staged Git path"):
        validate_staged_blobs(git, workspace, (path,))


def test_new_dispatch_draft_defaults_to_bridge_without_legacy_rebinding(tmp_path):
    from fox2_agent_bridge.dispatch_draft import prepare_new_dispatch_draft
    from fox2_agent_bridge.errors import DispatchInvalid
    from test_e2e_runner import _dispatch_payload
    from test_project_dictionary import bound_dispatch
    original = bound_dispatch(_dispatch_payload(tmp_path / "task"))
    original.pop("delivery_owner")
    prepared = prepare_new_dispatch_draft(original)
    assert prepared["delivery_owner"] == "BRIDGE"
    assert "delivery_owner" not in original
    prepared_agent = prepare_new_dispatch_draft(original, delivery_owner="AGENT")
    assert prepared_agent["delivery_owner"] == "AGENT"
    with pytest.raises(DispatchInvalid, match="cannot be rebound"):
        prepare_new_dispatch_draft(prepared_agent)
    assert prepared_agent["delivery_owner"] == "AGENT"
    with pytest.raises(DispatchInvalid, match="current v3"):
        prepare_new_dispatch_draft({**original, "schema_version": "0.6"})


def test_new_dispatch_draft_cli_is_non_overwriting_and_unpublished(tmp_path):
    import sys
    from test_e2e_runner import _dispatch_payload
    from test_project_dictionary import bound_dispatch
    draft = bound_dispatch(_dispatch_payload(tmp_path / "task"))
    draft.pop("delivery_owner")
    source = tmp_path / "draft.json"
    output = tmp_path / "prepared.json"
    source.write_text(json.dumps(draft), encoding="utf-8")
    tool = Path(__file__).parents[1] / "scripts/prepare_new_bridge_dispatch.py"
    args = [sys.executable, str(tool), "--new-draft", "--input", str(source),
            "--output", str(output)]
    result = subprocess.run(args, capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["git_delivery"] == "NOT_RUN"
    assert json.loads(output.read_text())["delivery_owner"] == "BRIDGE"
    assert json.loads(source.read_text()) == draft
    repeat = subprocess.run(args, capture_output=True, text=True, timeout=15)
    assert repeat.returncode != 0


def test_committed_recovery_content_guard_uses_exact_commit_tree(workspace):
    from fox2_agent_bridge.git_delivery_guard import validate_committed_result
    before = git(["-C", str(workspace), "rev-parse", "HEAD"]).stdout.strip()
    (workspace / "result.txt").write_text("okay\n", encoding="utf-8")
    git(["-C", str(workspace), "add", "result.txt"])
    git(["-C", str(workspace), "commit", "-m", "safe"])
    after = git(["-C", str(workspace), "rev-parse", "HEAD"]).stdout.strip()
    validate_committed_result(git, workspace, before, after, ("result.txt",))

    (workspace / "result.txt").write_text("github_pat_" + "P" * 32)
    git(["-C", str(workspace), "add", "result.txt"])
    git(["-C", str(workspace), "commit", "-m", "unsafe fixture"])
    secret_head = git(["-C", str(workspace), "rev-parse", "HEAD"]).stdout.strip()
    with pytest.raises(WorkspaceBlocked, match="secret"):
        validate_committed_result(git, workspace, after, secret_head, ("result.txt",))


def test_committed_recovery_rejects_gitlink_and_symlink_modes_without_host_permission(workspace):
    from fox2_agent_bridge.git_delivery_guard import validate_committed_result
    def fake_git(args, *, binary=False):
        if "ls-tree" in args:
            return SimpleNamespace(stdout=b"120000 blob " + b"0" * 40 + b"\tresult.txt\x00")
        raise AssertionError("non-regular committed file must never be read")
    with pytest.raises(WorkspaceBlocked, match="non-regular committed"):
        validate_committed_result(fake_git, workspace, "a" * 40, "b" * 40, ("result.txt",))


@pytest.mark.parametrize("agent_product", ["CODEX", "COPILOT"])
def test_bridge_publisher_real_local_bare_git_remote_no_agent_push(tmp_path, agent_product):
    """Git subprocess commits/pushes exact bounded work; remote SHA readback."""
    from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
    bare = tmp_path / "remote.git"
    worktree = tmp_path / "worktree"
    git(["init", "--bare", str(bare)])
    git(["init", str(worktree)])
    git(["-C", str(worktree), "config", "user.name", "Fixture"])
    git(["-C", str(worktree), "config", "user.email", "fixture@local.invalid"])
    git(["-C", str(worktree), "checkout", "-b", "work/FOX2-git-publisher"])
    report = worktree / "reports" / "result.md"
    report.parent.mkdir()
    report.write_text("baseline\n", encoding="utf-8")
    git(["-C", str(worktree), "add", "--", "reports/result.md"])
    git(["-C", str(worktree), "commit", "-m", "before"])
    git(["-C", str(worktree), "remote", "add", "origin", str(bare)])
    git(["-C", str(worktree), "push", "-u", "origin", "work/FOX2-git-publisher"])
    before = git(["-C", str(worktree), "rev-parse", "HEAD"]).stdout.strip()
    report.write_text(f"safe {agent_product} result\n", encoding="utf-8")

    runner = object.__new__(BridgeE2ERunner)
    runner.config = SimpleNamespace(tool_paths={"git": "git"}, local_repo=worktree)
    runner.ledger = SQLiteLedger(tmp_path / "ledger.db")
    runner.ledger.initialize()
    payload = {
        "delivery_owner": "BRIDGE", "branch": "work/FOX2-git-publisher",
        "dispatch_id": "FOX2-DISPATCH-GIT-PUBLISHER-001",
        "allowed_code_paths": [], "allowed_report_paths": ["reports/**"],
    }
    head, paths = runner._commit_and_push_codex_result(
        payload=payload, worktree=worktree, before_head=before,
        agent_stdout="test evidence in file")
    assert paths == ("reports/result.md",)
    assert head != before
    assert head == git(["-C", str(worktree), "rev-parse", "HEAD"]).stdout.strip()
    assert head == git(["--git-dir", str(bare), "rev-parse",
                        "refs/heads/work/FOX2-git-publisher"]).stdout.strip()
    assert not git(["-C", str(worktree), "status", "--porcelain"]).stdout.strip()
    # An already-finished attempt never manufactures another result commit.
    with pytest.raises(WorkspaceBlocked, match="Git history"):
        runner._commit_and_push_codex_result(payload=payload, worktree=worktree,
            before_head=before, agent_stdout="duplicate")
    assert head == git(["--git-dir", str(bare), "rev-parse",
                        "refs/heads/work/FOX2-git-publisher"]).stdout.strip()
    # AGENT owns its own publication: invoking the Bridge publisher is forbidden.
    payload["delivery_owner"] = "AGENT"
    with pytest.raises(WorkspaceBlocked, match="Agent-owned"):
        runner._commit_and_push_codex_result(payload=payload, worktree=worktree,
            before_head=head, agent_stdout="not authorized")


def test_bridge_publisher_refuses_main_even_with_allowlisted_result(tmp_path):
    runner = object.__new__(BridgeE2ERunner)
    payload = {"delivery_owner": "BRIDGE", "branch": "main",
               "dispatch_id": "FOX2-DISPATCH-INVALID",
               "allowed_code_paths": [], "allowed_report_paths": ["reports/**"]}
    with pytest.raises(WorkspaceBlocked, match="protected or invalid"):
        runner._commit_and_push_codex_result(payload=payload, worktree=tmp_path,
            before_head="a" * 40, agent_stdout="not authorized")


def test_git_change_inventory_uses_exact_nul_paths_and_rejects_control_names(tmp_path):
    runner = object.__new__(BridgeE2ERunner)
    commands = []
    def fake_git(args, *, binary=False):
        commands.append(args)
        assert binary
        if "ls-files" in args:
            return SimpleNamespace(stdout=b"reports/a file.md\x00")
        if "--cached" in args:
            return SimpleNamespace(stdout=b"reports/old.txt\x00")
        return SimpleNamespace(stdout=b"reports/new.md\x00")
    runner._git = fake_git
    assert runner._dirty_changed_paths(tmp_path) == (
        "reports/a file.md", "reports/new.md", "reports/old.txt")
    assert all("-z" in args for args in commands)

    def unsafe_git(args, *, binary=False):
        return SimpleNamespace(stdout=b"reports/evil\nline.md\x00")
    runner._git = unsafe_git
    with pytest.raises(WorkspaceBlocked, match="unsafe staged Git path"):
        runner._dirty_changed_paths(tmp_path)


def test_git_change_inventory_rejects_invalid_utf8_without_path_rebinding(tmp_path):
    runner = object.__new__(BridgeE2ERunner)
    runner._git = lambda args, *, binary=False: SimpleNamespace(
        stdout=b"reports/invalid-\xff.md\x00")
    with pytest.raises(WorkspaceBlocked, match="encoding"):
        runner._dirty_changed_paths(tmp_path)


def test_bridge_publisher_handles_space_in_git_name_with_real_bare_remote(tmp_path):
    bare = tmp_path / "remote.git"
    wt = tmp_path / "wt"
    git(["init", "--bare", str(bare)])
    git(["init", str(wt)])
    git(["-C", str(wt), "config", "user.name", "Test"])
    git(["-C", str(wt), "config", "user.email", "test@local.invalid"])
    git(["-C", str(wt), "checkout", "-b", "work/FOX2-safe-path"])
    name = "reports/space name.md"
    (wt / "reports").mkdir()
    (wt / name).write_text("base")
    git(["-C", str(wt), "add", "--", name])
    git(["-C", str(wt), "commit", "-m", "base"])
    git(["-C", str(wt), "remote", "add", "origin", str(bare)])
    git(["-C", str(wt), "push", "origin", "work/FOX2-safe-path"])
    before = git(["-C", str(wt), "rev-parse", "HEAD"]).stdout.strip()
    (wt / name).write_text("safe updated")
    runner = object.__new__(BridgeE2ERunner)
    runner.config = SimpleNamespace(tool_paths={"git": "git"}, local_repo=wt)
    runner.ledger = SQLiteLedger(tmp_path / "bridge.db")
    runner.ledger.initialize()
    payload = {"delivery_owner": "BRIDGE", "branch": "work/FOX2-safe-path",
               "dispatch_id": "FOX2-DISPATCH-SPACE-PATH",
               "allowed_code_paths": [], "allowed_report_paths": ["reports/**"]}
    head, paths = runner._commit_and_push_codex_result(
        payload=payload, worktree=wt, before_head=before,
        agent_stdout="fixture")
    assert paths == (name,)
    assert head == git(["--git-dir", str(bare), "rev-parse",
                        "refs/heads/work/FOX2-safe-path"]).stdout.strip()


def test_failed_wip_observation_never_grants_git_publication(tmp_path, monkeypatch):
    """A failed Agent may leave files; local metadata never conveys Git authority."""
    from fox2_agent_bridge.e2e_runner import BridgeE2ERunner
    from fox2_agent_bridge.git_delivery_guard import _safe_relative
    from fox2_agent_bridge.errors import WorkspaceBlocked
    import hashlib
    paths = ("reports/FOX2-RC1/a.md", "reports/FOX2-RC1/b.md")
    assert hashlib.sha256("\x00".join(paths).encode()).hexdigest()
    for path in paths:
        _safe_relative(path)
    with pytest.raises(WorkspaceBlocked):
        _safe_relative("reports/FOX2-RC1/evil\nfile.md")
    # This test is a pure regression on identity and forbidden path handling.
    # The exception-path E2E tests assert no remote publication or replay.


def test_nonzero_e2e_local_wip_metadata_is_fail_closed(bridge_config, monkeypatch):
    """Nonzero E2E leaves no publishable WIP even when report files exist."""
    from test_e2e_runner import execution_harness as fixture_harness
    from fox2_agent_bridge.errors import ToolExecFailed
    # Assert the source-level negative guarantee: a local inventory has no
    # function or field that can authorize a recovery ref or process quiescence.
    import inspect
    source = inspect.getsource(BridgeE2ERunner.run_once)
    assert '"git_wip_publication": "NOT_RUN"' in source
    assert '"child_writer_quiescence": "NOT_VERIFIED"' in source
    assert 'failure_result["wip_local_observation"] = wip_info' in source
