from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

from fox2_agent_bridge.__main__ import main
from fox2_agent_bridge.app import BridgeApp
from fox2_agent_bridge.config import CONTROL_BRANCH, REPOSITORY
from fox2_agent_bridge.dispatch_poller import (
    CANONICAL_REMOTE_URL,
    DispatchPoller,
    GitTransport,
    PollResult,
    canonical_repository_url,
)
from fox2_agent_bridge.errors import DatabaseError, TransportFailure
from fox2_agent_bridge.ledger import SCHEMA_VERSION, SQLiteLedger
from fox2_agent_bridge.logging_config import configure_logging


def run_git(cwd: Path, *arguments: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *arguments],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if check and result.returncode:
        raise AssertionError(f"git {arguments!r}: {result.stderr}")
    return result.stdout.strip()


@dataclass
class GitFixture:
    config: object
    ledger: SQLiteLedger
    remote: Path
    working: Path
    transport: GitTransport

    def commit_file(self, relative_path: str, content: str) -> str:
        path = self.working / Path(*relative_path.split("/"))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="")
        run_git(self.working, "add", "--", relative_path)
        run_git(self.working, "commit", "-m", f"update {relative_path}")
        sha = run_git(self.working, "rev-parse", "HEAD")
        run_git(self.working, "push", "origin", f"HEAD:{CONTROL_BRANCH}")
        return sha

    def poller(self, logger=None) -> DispatchPoller:
        return DispatchPoller(
            self.config,
            self.ledger,
            logger=logger,
            transport=self.transport,
        )


@pytest.fixture
def git_fixture(tmp_path: Path, bridge_config) -> GitFixture:
    remote = tmp_path / "remote.git"
    working = tmp_path / "working"
    run_git(tmp_path, "init", "--bare", str(remote))
    run_git(tmp_path, "init", "-b", CONTROL_BRANCH, str(working))
    run_git(working, "config", "user.name", "FOX2 Bridge Test")
    run_git(working, "config", "user.email", "bridge-test@example.invalid")
    run_git(working, "remote", "add", "origin", str(remote))

    seed = working / "README.txt"
    seed.write_text("fixture\n", encoding="utf-8")
    run_git(working, "add", "README.txt")
    run_git(working, "commit", "-m", "initial fixture")
    run_git(working, "push", "-u", "origin", CONTROL_BRANCH)

    ledger = SQLiteLedger(bridge_config.database_path)
    assert ledger.initialize() == SCHEMA_VERSION
    git_executable = Path(shutil.which("git") or "git")
    transport = GitTransport(
        git_executable=git_executable,
        store_path=bridge_config.bridge_root / "data" / "control.git",
        remote_url=str(remote),
        allow_local_remote=True,
    )
    return GitFixture(bridge_config, ledger, remote, working, transport)


def dispatch_path(name: str = "BRG-020.json", work_package: str = "BRG-020") -> str:
    return f"docs/agent_handoff/{work_package}/dispatch/{name}"


def test_control_branch_missing_is_reported_without_cursor(git_fixture: GitFixture) -> None:
    config = git_fixture.config
    object.__setattr__(config, "control_branch", "work/FOX2-NOT-CREATED")

    result = git_fixture.poller().poll_once()

    assert result.status == "CONTROL_BRANCH_UNAVAILABLE"
    assert result.reason == "CONTROL_BRANCH_UNAVAILABLE"
    assert git_fixture.ledger.get_control_cursor(REPOSITORY, config.control_branch) is None


def test_first_poll_scans_tip_as_unvalidated_candidates(git_fixture: GitFixture) -> None:
    git_fixture.commit_file(dispatch_path(), '{"not": "validated here"}')

    result = git_fixture.poller().poll_once()
    rows = git_fixture.ledger.list_candidate_discoveries(REPOSITORY, CONTROL_BRANCH)

    assert result.status == "CANDIDATES_DISCOVERED"
    assert result.previous_cursor is None
    assert result.observed_remote_sha == run_git(git_fixture.working, "rev-parse", "HEAD")
    assert result.new_candidate_count == 1
    assert result.candidates[0]["discovery_state"] == "DISCOVERED"
    assert len(result.observed_remote_sha or "") in {40, 64}
    assert rows[0]["trust_state"] == "UNVALIDATED_CANDIDATE"


def test_no_change_poll_does_not_advance_cursor_again(git_fixture: GitFixture) -> None:
    git_fixture.poller().poll_once()
    cursor = git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH)

    result = git_fixture.poller().poll_once()
    with git_fixture.ledger.connect() as connection:
        observation = connection.execute(
            "SELECT cursor_advanced FROM poll_observations "
            "WHERE status = 'NO_CHANGE' ORDER BY observed_at_utc DESC LIMIT 1"
        ).fetchone()

    assert result.status == "NO_CHANGE"
    assert result.new_candidate_count == 0
    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) == cursor
    assert observation["cursor_advanced"] == 0


def test_new_fast_forward_commit_advances_cursor(git_fixture: GitFixture) -> None:
    first = git_fixture.poller().poll_once()
    new_sha = git_fixture.commit_file(dispatch_path(), "{}")

    result = git_fixture.poller().poll_once()

    assert first.status == "INITIALIZED"
    assert result.status == "CANDIDATES_DISCOVERED"
    assert result.previous_cursor != new_sha
    assert result.observed_remote_sha == new_sha
    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) == new_sha


def test_non_dispatch_json_is_ignored(git_fixture: GitFixture) -> None:
    git_fixture.commit_file("docs/agent_handoff/BRG-020/dispatch-notes.json", "{}")
    git_fixture.poller().poll_once()

    assert git_fixture.ledger.list_candidate_discoveries(REPOSITORY, CONTROL_BRANCH) == ()


def test_duplicate_poll_is_idempotent(git_fixture: GitFixture) -> None:
    git_fixture.commit_file(dispatch_path(), "{}")
    first = git_fixture.poller().poll_once()
    second = git_fixture.poller().poll_once()

    assert first.new_candidate_count == 1
    assert second.status == "NO_CHANGE"
    assert len(git_fixture.ledger.list_candidate_discoveries(REPOSITORY, CONTROL_BRANCH)) == 1


def test_multiple_candidate_files_on_first_poll(git_fixture: GitFixture) -> None:
    git_fixture.commit_file(dispatch_path("one.json"), "{}")
    git_fixture.commit_file(dispatch_path("two.json"), "{}")

    result = git_fixture.poller().poll_once()

    assert result.new_candidate_count == 2
    assert {row["dispatch_path"] for row in result.candidates} == {
        dispatch_path("one.json"),
        dispatch_path("two.json"),
    }


def test_multiple_commits_between_polls_are_all_observed(git_fixture: GitFixture) -> None:
    git_fixture.poller().poll_once()
    first_sha = git_fixture.commit_file(dispatch_path("one.json"), "{}")
    second_sha = git_fixture.commit_file(dispatch_path("two.json"), "{}")

    result = git_fixture.poller().poll_once()

    assert result.new_candidate_count == 2
    assert {row["control_commit_sha"] for row in result.candidates} == {first_sha, second_sha}


def test_modified_dispatch_path_is_anomaly(git_fixture: GitFixture) -> None:
    path = dispatch_path()
    git_fixture.commit_file(path, '{"v": 1}')
    git_fixture.poller().poll_once()
    git_fixture.commit_file(path, '{"v": 2}')

    result = git_fixture.poller().poll_once()

    assert result.new_candidate_count == 1
    assert result.candidates[0]["discovery_state"] == "PATH_MODIFIED"


def test_deleted_dispatch_path_is_anomaly(git_fixture: GitFixture) -> None:
    path = dispatch_path()
    git_fixture.commit_file(path, "{}")
    git_fixture.poller().poll_once()
    (git_fixture.working / Path(*path.split("/"))).unlink()
    run_git(git_fixture.working, "add", "-A")
    run_git(git_fixture.working, "commit", "-m", "delete dispatch")
    deleted_commit = run_git(git_fixture.working, "rev-parse", "HEAD")
    run_git(git_fixture.working, "push", "origin", f"HEAD:{CONTROL_BRANCH}")

    result = git_fixture.poller().poll_once()

    deleted = [row for row in result.candidates if row["control_commit_sha"] == deleted_commit]
    assert len(deleted) == 1
    assert deleted[0]["discovery_state"] == "PATH_DELETED"
    assert deleted[0]["dispatch_blob_sha"] is None


def test_non_fast_forward_history_is_not_accepted(git_fixture: GitFixture) -> None:
    original = git_fixture.poller().poll_once().observed_remote_sha
    orphan = "rewritten-control"
    run_git(git_fixture.working, "checkout", "--orphan", orphan)
    run_git(git_fixture.working, "rm", "-rf", "--ignore-unmatch", ".")
    seed = git_fixture.working / "rewritten.txt"
    seed.write_text("new root\n", encoding="utf-8")
    run_git(git_fixture.working, "add", "rewritten.txt")
    run_git(git_fixture.working, "commit", "-m", "rewrite control history")
    rewritten = run_git(git_fixture.working, "rev-parse", "HEAD")
    run_git(
        git_fixture.working,
        "push",
        "--force",
        "origin",
        f"HEAD:{CONTROL_BRANCH}",
    )

    result = git_fixture.poller().poll_once()

    assert original != rewritten
    assert result.status == "CONTROL_HISTORY_DIVERGED"
    assert result.previous_cursor == original
    assert result.observed_remote_sha == rewritten
    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) == original


def test_failed_fetch_does_not_advance_cursor(git_fixture: GitFixture, monkeypatch) -> None:
    class FailedFetch(GitTransport):
        def fetch_control(self, branch: str, expected_sha: str) -> str:
            raise TransportFailure("fixture fetch interrupted")

    broken = FailedFetch(
        git_executable=git_fixture.transport.git_executable,
        store_path=git_fixture.transport.store_path,
        remote_url=str(git_fixture.remote),
        allow_local_remote=True,
    )
    poller = DispatchPoller(
        git_fixture.config,
        git_fixture.ledger,
        transport=broken,
    )

    result = poller.poll_once()

    assert result.status == "POLL_FAILED"
    assert "interrupted" in (result.error or "")
    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) is None


def test_cursor_survives_poller_restart(git_fixture: GitFixture) -> None:
    expected = git_fixture.poller().poll_once().observed_remote_sha
    restarted = git_fixture.poller()

    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) == expected
    assert restarted.poll_once().status == "NO_CHANGE"


def test_failed_discovery_transaction_rolls_back_cursor(git_fixture: GitFixture) -> None:
    with pytest.raises(DatabaseError):
        git_fixture.ledger.record_poll_success(
            repository=REPOSITORY,
            control_branch=CONTROL_BRANCH,
            previous_cursor=None,
            observed_remote_sha="a" * 40,
            status="INITIALIZED",
            candidates=[
                {
                    "control_commit_sha": "a" * 40,
                    "dispatch_path": dispatch_path(),
                    "dispatch_blob_sha": None,
                    "discovery_state": "NOT_A_VALID_STATE",
                }
            ],
            observed_at_utc="2026-10-13T00:00:00+00:00",
        )

    assert git_fixture.ledger.get_control_cursor(REPOSITORY, CONTROL_BRANCH) is None
    assert git_fixture.ledger.list_candidate_discoveries(REPOSITORY, CONTROL_BRANCH) == ()


def test_git_command_failure_is_poll_failed(git_fixture: GitFixture) -> None:
    class FailedQuery(GitTransport):
        def query_control_sha(self, branch: str) -> str | None:
            raise TransportFailure("fixture DNS failure")

    transport = FailedQuery(
        git_executable=git_fixture.transport.git_executable,
        store_path=git_fixture.transport.store_path,
        remote_url=str(git_fixture.remote),
        allow_local_remote=True,
    )
    result = DispatchPoller(
        git_fixture.config,
        git_fixture.ledger,
        transport=transport,
    ).poll_once()

    assert result.status == "POLL_FAILED"
    assert "DNS failure" in (result.error or "")
    with git_fixture.ledger.connect() as connection:
        row = connection.execute(
            "SELECT cursor_advanced FROM poll_observations WHERE status = 'POLL_FAILED'"
        ).fetchone()
    assert row["cursor_advanced"] == 0


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/dunglt2505/FOX2.git",
        "https://github.com/dunglt2505/FOX2",
        "git@github.com:dunglt2505/FOX2.git",
        "ssh://git@github.com/dunglt2505/FOX2.git",
    ],
)
def test_equivalent_expected_repository_urls_are_accepted(url: str) -> None:
    assert canonical_repository_url(url) == CANONICAL_REMOTE_URL


def _synthetic_credentialed_remote() -> str:
    return (
        "https://"
        + "fixture-user"
        + ":"
        + "synthetic-value"
        + "@github.com/dunglt2505/FOX2.git"
    )


@pytest.mark.parametrize(
    "url",
    [
        "https://attacker/FOX2.git",
        "https://someoneelse/FOX2.git",
        "https://github.com/other/FOX2.git",
        _synthetic_credentialed_remote(),
        "https://user:secret@github.com/dunglt2505/FOX2.git",
        "https://github.com/dunglt2505/FOX2.git?token=synthetic-fixture",
    ],
)
def test_wrong_or_credential_bearing_remote_is_rejected(url: str) -> None:
    with pytest.raises(TransportFailure) as exc:
        canonical_repository_url(url)
    assert exc.value.status == "TRANSPORT_BLOCKED"
    assert exc.value.reason == "REPOSITORY_MISMATCH"
    assert "synthetic-fixture" not in exc.value.message


def test_wrong_repository_is_blocked_before_git_commands(git_fixture: GitFixture) -> None:
    transport = GitTransport(
        git_executable=git_fixture.transport.git_executable,
        store_path=git_fixture.transport.store_path,
        remote_url="https://github.com/else/FOX2.git",
    )

    with pytest.raises(TransportFailure) as exc:
        transport.initialize()

    assert exc.value.reason == "REPOSITORY_MISMATCH"


def test_blob_identity_and_full_commit_sha_are_captured(git_fixture: GitFixture) -> None:
    git_fixture.commit_file(dispatch_path(), "{}")

    result = git_fixture.poller().poll_once()
    candidate = result.candidates[0]

    assert len(candidate["control_commit_sha"] or "") in {40, 64}
    assert len(candidate["dispatch_blob_sha"] or "") in {40, 64}


def test_owner_fox2_workspace_is_not_mutated(git_fixture: GitFixture) -> None:
    repo = Path(r"C:\Projects\FOX2")
    before_status = run_git(repo, "status", "--porcelain")
    before_head = run_git(repo, "rev-parse", "HEAD")
    before_attributes = (repo / ".gitattributes").read_bytes()

    git_fixture.poller().poll_once()

    assert run_git(repo, "status", "--porcelain") == before_status
    assert run_git(repo, "rev-parse", "HEAD") == before_head
    assert (repo / ".gitattributes").read_bytes() == before_attributes


def test_poller_never_invokes_agent_or_remote_push(git_fixture: GitFixture, monkeypatch) -> None:
    calls: list[list[str]] = []
    original = subprocess.run

    def capture(args, *positional, **kwargs):
        calls.append([str(part) for part in args])
        return original(args, *positional, **kwargs)

    monkeypatch.setattr("fox2_agent_bridge.dispatch_poller.subprocess.run", capture)
    git_fixture.poller().poll_once()

    command_text = "\n".join(" ".join(call).lower() for call in calls)
    assert "push" not in command_text
    assert "codex exec" not in command_text
    assert "copilot -p" not in command_text
    assert calls
    assert all(
        (
            "--git-dir" in call
            and call[call.index("--git-dir") + 1] == str(git_fixture.transport.store_path)
        )
        or (
            "init" in call
            and "--bare" in call
            and str(git_fixture.transport.store_path) in call
        )
        for call in calls
    )


def test_git_error_tokens_are_redacted_from_result_and_logs(
    git_fixture: GitFixture, tmp_path: Path
) -> None:
    secret = "gho_" + ("A" * 30)
    logger = configure_logging(tmp_path)

    class SecretFailure(GitTransport):
        def query_control_sha(self, branch: str) -> str | None:
            raise TransportFailure(f"Git error contains {secret}")

    transport = SecretFailure(
        git_executable=git_fixture.transport.git_executable,
        store_path=git_fixture.transport.store_path,
        remote_url=str(git_fixture.remote),
        allow_local_remote=True,
    )
    result = DispatchPoller(
        git_fixture.config,
        git_fixture.ledger,
        logger=logger,
        transport=transport,
    ).poll_once()
    for handler in logger.handlers:
        handler.flush()
    log_text = (tmp_path / "bridge.log").read_text(encoding="utf-8")

    assert secret not in (result.error or "")
    assert secret not in log_text


def test_poll_once_cli_returns_machine_readable_json(
    bridge_config, monkeypatch, capsys
) -> None:
    fake = BridgeApp(bridge_config)
    result = PollResult(
        "NO_CHANGE",
        REPOSITORY,
        CONTROL_BRANCH,
        "a" * 40,
        "a" * 40,
        0,
        0,
        (),
    )
    monkeypatch.setattr(
        BridgeApp,
        "from_file",
        classmethod(lambda cls, config_path=None: fake),
    )
    monkeypatch.setattr(BridgeApp, "poll_once", lambda self: result)

    exit_code = main(["poll-once"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["status"] == "NO_CHANGE"
    assert payload["repository"] == REPOSITORY
    assert payload["control_branch"] == CONTROL_BRANCH
    assert payload["trusted_for_execution"] is False
