"""Read-only Git transport for FOX2 dispatch candidate discovery."""

from __future__ import annotations

import re
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from .config import REPOSITORY, BridgeConfig
from .errors import DatabaseError, TransportFailure
from .ledger import SQLiteLedger, utc_now
from .logging_config import log_event, redact_context

CONTROL_REF = "refs/bridge/control"
OBSERVED_REF_PREFIX = "refs/bridge/observed"
FULL_SHA_PATTERN = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
CANDIDATE_PATH_PATTERN = re.compile(
    rb"^docs/agent_handoff/([A-Za-z0-9][A-Za-z0-9._-]*)/dispatch/"
    rb"([A-Za-z0-9][A-Za-z0-9._-]*\.json)$"
)
CANONICAL_REMOTE_URL = "https://github.com/dunglt2505/FOX2.git"


def canonical_repository_url(url: str) -> str:
    value = url.strip()
    if not value or "\x00" in value:
        raise TransportFailure(
            "configured remote is invalid",
            status="TRANSPORT_BLOCKED",
            reason="REPOSITORY_MISMATCH",
        )

    if value.startswith("git@github.com:"):
        path = value.removeprefix("git@github.com:")
        host = "github.com"
    else:
        parsed = urlparse(value)
        if parsed.scheme not in {"https", "ssh"} or parsed.hostname is None:
            raise TransportFailure(
                "configured remote is not an accepted GitHub URL",
                status="TRANSPORT_BLOCKED",
                reason="REPOSITORY_MISMATCH",
            )
        if parsed.username not in (None, "git") or parsed.password is not None:
            raise TransportFailure(
                "credentials are not permitted in the configured remote URL",
                status="TRANSPORT_BLOCKED",
                reason="REPOSITORY_MISMATCH",
            )
        if parsed.query or parsed.fragment:
            raise TransportFailure(
                "query and fragment components are not permitted in the remote URL",
                status="TRANSPORT_BLOCKED",
                reason="REPOSITORY_MISMATCH",
            )
        host = parsed.hostname.lower()
        path = unquote(parsed.path).lstrip("/")

    if host != "github.com":
        raise TransportFailure(
            "configured remote host does not match github.com",
            status="TRANSPORT_BLOCKED",
            reason="REPOSITORY_MISMATCH",
        )
    if path.endswith(".git"):
        path = path[:-4]
    if path.casefold() != REPOSITORY.casefold():
        raise TransportFailure(
            "configured remote repository does not match dunglt2505/FOX2",
            status="TRANSPORT_BLOCKED",
            reason="REPOSITORY_MISMATCH",
        )
    return CANONICAL_REMOTE_URL


def _safe_error_text(value: str) -> str:
    safe = str(redact_context(value, "details"))
    safe = re.sub(r"https?://[^/\s:@]+:[^@\s/]+@", "https://<REDACTED>@", safe)
    safe = re.sub(r"(?i)(authorization:\s*)\S+", r"\1<REDACTED>", safe)
    return safe[:2000]


def _decode_git_path(value: bytes) -> str:
    try:
        return value.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise TransportFailure("Git returned a non-UTF-8 candidate path") from exc


def _candidate_path(path: bytes) -> bool:
    return CANDIDATE_PATH_PATTERN.fullmatch(path) is not None


def _parse_tree_listing(output: bytes, commit_sha: str) -> list[dict[str, str | None]]:
    candidates: list[dict[str, str | None]] = []
    for record in output.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path = record.split(b"\t", 1)
            _mode, object_type, blob_sha = metadata.split(b" ", 2)
        except ValueError as exc:
            raise TransportFailure("Git returned a malformed tree entry") from exc
        if object_type != b"blob" or not _candidate_path(path):
            continue
        candidates.append(
            {
                "control_commit_sha": commit_sha,
                "dispatch_path": _decode_git_path(path),
                "dispatch_blob_sha": blob_sha.decode("ascii"),
                "discovery_state": "DISCOVERED",
            }
        )
    return candidates


def _parse_name_status(output: bytes) -> list[tuple[str, bytes]]:
    fields = output.split(b"\0")
    changes: list[tuple[str, bytes]] = []
    index = 0
    while index < len(fields):
        status_field = fields[index]
        index += 1
        if not status_field:
            continue
        if status_field[:1] in (b"R", b"C"):
            raise TransportFailure("unexpected rename/copy record from no-renames diff")
        if index >= len(fields):
            raise TransportFailure("Git returned an incomplete name-status record")
        path = fields[index]
        index += 1
        try:
            status = status_field.decode("ascii")
        except UnicodeDecodeError as exc:
            raise TransportFailure("Git returned an invalid name-status code") from exc
        changes.append((status, path))
    return changes


class GitTransport:
    """A Git command boundary restricted to a Bridge-owned bare object store."""

    def __init__(
        self,
        *,
        git_executable: Path,
        store_path: Path,
        remote_url: str = CANONICAL_REMOTE_URL,
        allow_local_remote: bool = False,
    ) -> None:
        self.git_executable = str(git_executable)
        self.store_path = store_path.resolve()
        self.remote_url = remote_url
        self.allow_local_remote = allow_local_remote
        self._canonical_url: str | None = None

    def _validate_store(self) -> None:
        if not self.allow_local_remote:
            self._canonical_url = canonical_repository_url(self.remote_url)
        bridge_data = (Path(r"C:\Projects\FOX2-AgentBridge") / "data").resolve()
        if not self.allow_local_remote:
            try:
                self.store_path.relative_to(bridge_data)
            except ValueError as exc:
                raise TransportFailure(
                    "Git object store must be under Bridge data",
                    status="TRANSPORT_BLOCKED",
                    reason="STORE_PATH_INVALID",
                ) from exc
        if self.allow_local_remote:
            if not self.remote_url:
                raise TransportFailure("local test remote is empty")
            return

    def _run(
        self,
        arguments: list[str],
        *,
        check: bool = True,
        binary: bool = False,
    ) -> subprocess.CompletedProcess[Any]:
        environment = {
            **__import__("os").environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
        }
        command = [self.git_executable, "--git-dir", str(self.store_path), *arguments]
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=not binary,
                encoding=None if binary else "utf-8",
                errors=None if binary else "replace",
                timeout=60,
                check=False,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise TransportFailure(
                f"Git transport command failed to start or timed out: {type(exc).__name__}"
            ) from exc
        if check and result.returncode != 0:
            detail = _safe_error_text(result.stderr.decode("utf-8", "replace") if binary else result.stderr)
            raise TransportFailure(
                f"Git transport command failed with exit code {result.returncode}"
                + (f": {detail}" if detail else "")
            )
        return result

    def initialize(self) -> None:
        self._validate_store()
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            init = subprocess.run(
                [self.git_executable, "init", "--bare", str(self.store_path)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=60,
                check=False,
                env={
                    **__import__("os").environ,
                    "GIT_TERMINAL_PROMPT": "0",
                    "GCM_INTERACTIVE": "Never",
                },
            )
            if init.returncode:
                raise TransportFailure(
                    "cannot initialize Bridge-owned bare Git store: "
                    + _safe_error_text(init.stderr)
                )
        bare = self._run(["rev-parse", "--is-bare-repository"])
        if bare.stdout.strip() != "true":
            raise TransportFailure(
                "control.git exists but is not a bare repository",
                status="TRANSPORT_BLOCKED",
                reason="STORE_PATH_INVALID",
            )

        existing = self._run(["remote", "get-url", "origin"], check=False)
        if existing.returncode == 0:
            existing_url = existing.stdout.strip()
            if self.allow_local_remote:
                if Path(existing_url).resolve() != Path(self.remote_url).resolve():
                    raise TransportFailure("existing control.git remote differs from test remote")
            else:
                resolved_existing = canonical_repository_url(existing_url)
                if resolved_existing != self._canonical_url:
                    raise TransportFailure(
                        "control.git origin does not match configured FOX2 repository",
                        status="TRANSPORT_BLOCKED",
                        reason="REPOSITORY_MISMATCH",
                    )
        else:
            local_url = self.remote_url if self.allow_local_remote else self._canonical_url
            self._run(["remote", "add", "origin", str(local_url)])

    def query_control_sha(self, branch: str) -> str | None:
        result = self._run(
            ["ls-remote", "--refs", "origin", f"refs/heads/{branch}"],
            check=False,
        )
        if result.returncode != 0:
            detail = _safe_error_text(result.stderr)
            raise TransportFailure(
                f"cannot query remote control branch (exit {result.returncode})"
                + (f": {detail}" if detail else "")
            )
        lines = [line for line in result.stdout.splitlines() if line]
        if not lines:
            return None
        if len(lines) != 1:
            raise TransportFailure("remote returned multiple values for the control ref")
        parts = lines[0].split("\t", 1)
        if len(parts) != 2 or parts[1] != f"refs/heads/{branch}" or not FULL_SHA_PATTERN.fullmatch(parts[0]):
            raise TransportFailure("remote returned an invalid full commit SHA for control ref")
        return parts[0]

    def fetch_control(self, branch: str, expected_sha: str) -> str:
        if not FULL_SHA_PATTERN.fullmatch(expected_sha):
            raise TransportFailure("control ref is not a full immutable commit SHA")
        self._run(
            [
                "fetch",
                "--no-tags",
                "--no-write-fetch-head",
                "origin",
                f"+refs/heads/{branch}:{CONTROL_REF}",
            ]
        )
        actual = self._run(["rev-parse", "--verify", f"{CONTROL_REF}^{{commit}}"]).stdout.strip()
        if actual != expected_sha:
            raise TransportFailure("fetched control ref does not match observed remote SHA")
        self._run(
            [
                "update-ref",
                f"{OBSERVED_REF_PREFIX}/{expected_sha}",
                expected_sha,
            ]
        )
        return actual

    def is_ancestor(self, ancestor_sha: str, descendant_sha: str) -> bool:
        result = self._run(
            ["merge-base", "--is-ancestor", ancestor_sha, descendant_sha],
            check=False,
        )
        if result.returncode == 0:
            return True
        if result.returncode == 1:
            return False
        detail = _safe_error_text(result.stderr)
        raise TransportFailure(
            "cannot verify control history ancestry"
            + (f": {detail}" if detail else "")
        )

    def commits_between(self, old_sha: str, new_sha: str) -> tuple[str, ...]:
        result = self._run(["rev-list", "--reverse", f"{old_sha}..{new_sha}"])
        commits = tuple(line.strip() for line in result.stdout.splitlines() if line.strip())
        if any(not FULL_SHA_PATTERN.fullmatch(sha) for sha in commits):
            raise TransportFailure("Git returned an invalid commit id in control history")
        return commits

    def tree_candidates(self, commit_sha: str) -> list[dict[str, str | None]]:
        result = self._run(
            ["ls-tree", "-r", "-z", "--full-tree", commit_sha],
            binary=True,
        )
        return _parse_tree_listing(result.stdout, commit_sha)

    def changed_candidates(self, commit_sha: str) -> list[dict[str, str | None]]:
        result = self._run(
            [
                "diff-tree",
                "--no-commit-id",
                "--name-status",
                "--root",
                "-r",
                "--no-renames",
                "-z",
                commit_sha,
            ],
            binary=True,
        )
        candidates: list[dict[str, str | None]] = []
        for status, raw_path in _parse_name_status(result.stdout):
            if status not in {"A", "M", "D"} or not _candidate_path(raw_path):
                continue
            path = _decode_git_path(raw_path)
            blob_sha = None
            state = {"A": "DISCOVERED", "M": "PATH_MODIFIED", "D": "PATH_DELETED"}[status]
            if status != "D":
                result = self._run(["rev-parse", "--verify", f"{commit_sha}:{path}"])
                blob_sha = result.stdout.strip()
                if not FULL_SHA_PATTERN.fullmatch(blob_sha):
                    raise TransportFailure("Git returned an invalid dispatch blob identity")
            candidates.append(
                {
                    "control_commit_sha": commit_sha,
                    "dispatch_path": path,
                    "dispatch_blob_sha": blob_sha,
                    "discovery_state": state,
                }
            )
        return candidates


    def read_dispatch_blob(self, commit_sha: str, dispatch_path: str) -> tuple[bytes, str]:
        """Read one immutable dispatch blob from the fetched control commit."""
        if not FULL_SHA_PATTERN.fullmatch(commit_sha):
            raise TransportFailure("dispatch control commit is not a full immutable SHA")
        try:
            raw_path = dispatch_path.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise TransportFailure("dispatch path is not valid UTF-8") from exc
        if not _candidate_path(raw_path):
            raise TransportFailure("dispatch path is outside the FOX2 dispatch namespace")

        identity = self._run(
            ["rev-parse", "--verify", f"{commit_sha}:{dispatch_path}"]
        ).stdout.strip()
        if not FULL_SHA_PATTERN.fullmatch(identity):
            raise TransportFailure("Git returned an invalid dispatch blob identity")
        content = self._run(
            ["show", f"{commit_sha}:{dispatch_path}"],
            binary=True,
        ).stdout
        return content, identity


@dataclass(frozen=True)
class PollResult:
    status: str
    repository: str
    control_branch: str
    previous_cursor: str | None
    observed_remote_sha: str | None
    new_candidate_count: int
    already_seen_count: int
    candidates: tuple[dict[str, str | None], ...]
    error: str | None = None
    reason: str | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "repository": self.repository,
            "control_branch": self.control_branch,
            "previous_cursor": self.previous_cursor,
            "observed_remote_sha": self.observed_remote_sha,
            "new_candidate_count": self.new_candidate_count,
            "already_seen_count": self.already_seen_count,
            "candidates": list(self.candidates),
            "error": self.error,
            "reason": self.reason,
            "trusted_for_execution": False,
        }


class DispatchPoller:
    def __init__(
        self,
        config: BridgeConfig,
        ledger: SQLiteLedger,
        *,
        logger: Any = None,
        transport: GitTransport | None = None,
    ) -> None:
        self.config = config
        self.ledger = ledger
        self.logger = logger
        self.transport = transport or GitTransport(
            git_executable=(config.tool_paths or {})["git"] or Path("git"),
            store_path=config.bridge_root / "data" / "control.git",
        )

    def _log(self, event: str, context: dict[str, object]) -> None:
        if self.logger is not None:
            log_event(
                self.logger,
                component="dispatch_poller",
                event=event,
                context=context,
            )

    def _failure(
        self,
        *,
        started: float,
        previous_cursor: str | None,
        observed_sha: str | None,
        status: str,
        reason: str | None,
        error: str | None,
    ) -> PollResult:
        safe_error = _safe_error_text(error) if error else None
        now = utc_now()
        self.ledger.record_poll_failure(
            repository=self.config.repository,
            control_branch=self.config.control_branch,
            previous_cursor=previous_cursor,
            observed_remote_sha=observed_sha,
            status=status,
            reason=reason,
            error=safe_error,
            observed_at_utc=now,
        )
        self._log(
            "POLL_FAILED",
            {
                "branch": self.config.control_branch,
                "previous_sha": previous_cursor,
                "observed_sha": observed_sha,
                "status": status,
                "reason": reason,
                "error": safe_error,
                "duration_seconds": round(time.monotonic() - started, 3),
            },
        )
        return PollResult(
            status=status,
            repository=self.config.repository,
            control_branch=self.config.control_branch,
            previous_cursor=previous_cursor,
            observed_remote_sha=observed_sha,
            new_candidate_count=0,
            already_seen_count=0,
            candidates=(),
            error=safe_error,
            reason=reason,
        )

    def poll_once(self) -> PollResult:
        started = time.monotonic()
        previous_cursor = self.ledger.get_control_cursor(
            self.config.repository,
            self.config.control_branch,
        )
        observed_sha: str | None = None
        self._log(
            "POLL_STARTED",
            {
                "repository": self.config.repository,
                "branch": self.config.control_branch,
                "previous_sha": previous_cursor,
            },
        )
        try:
            self.transport.initialize()
            observed_sha = self.transport.query_control_sha(self.config.control_branch)
            if observed_sha is None:
                return self._failure(
                    started=started,
                    previous_cursor=previous_cursor,
                    observed_sha=None,
                    status="CONTROL_BRANCH_UNAVAILABLE",
                    reason="CONTROL_BRANCH_UNAVAILABLE",
                    error="configured control branch does not exist on the expected remote",
                )
            self._log(
                "REMOTE_REF_OBSERVED",
                {
                    "branch": self.config.control_branch,
                    "control_commit_sha": observed_sha,
                },
            )
            if observed_sha == previous_cursor:
                now = utc_now()
                self.ledger.record_poll_success(
                    repository=self.config.repository,
                    control_branch=self.config.control_branch,
                    previous_cursor=previous_cursor,
                    observed_remote_sha=observed_sha,
                    status="NO_CHANGE",
                    candidates=(),
                    observed_at_utc=now,
                    cursor_advanced=False,
                )
                self._log(
                    "NO_CHANGE",
                    {
                        "branch": self.config.control_branch,
                        "control_commit_sha": observed_sha,
                        "duration_seconds": round(time.monotonic() - started, 3),
                    },
                )
                self._log(
                    "POLL_COMPLETED",
                    {"status": "NO_CHANGE", "duration_seconds": round(time.monotonic() - started, 3)},
                )
                return PollResult(
                    "NO_CHANGE",
                    self.config.repository,
                    self.config.control_branch,
                    previous_cursor,
                    observed_sha,
                    0,
                    0,
                    (),
                )

            self._log(
                "FETCH_STARTED",
                {"branch": self.config.control_branch, "control_commit_sha": observed_sha},
            )
            fetched_sha = self.transport.fetch_control(self.config.control_branch, observed_sha)
            self._log(
                "FETCH_COMPLETED",
                {"branch": self.config.control_branch, "control_commit_sha": fetched_sha},
            )

            if previous_cursor is None:
                candidates = self.transport.tree_candidates(fetched_sha)
                status = "INITIALIZED"
            else:
                if not self.transport.is_ancestor(previous_cursor, fetched_sha):
                    return self._failure(
                        started=started,
                        previous_cursor=previous_cursor,
                        observed_sha=observed_sha,
                        status="CONTROL_HISTORY_DIVERGED",
                        reason="CONTROL_HISTORY_DIVERGED",
                        error="previous cursor is not an ancestor of the observed remote commit",
                    )
                commits = self.transport.commits_between(previous_cursor, fetched_sha)
                candidates = [
                    candidate
                    for commit_sha in commits
                    for candidate in self.transport.changed_candidates(commit_sha)
                ]
                status = "ADVANCED"

            for candidate in candidates:
                self._log(
                    "CANDIDATE_DISCOVERED",
                    {
                        "branch": self.config.control_branch,
                        "control_commit_sha": candidate["control_commit_sha"],
                        "dispatch_path": candidate["dispatch_path"],
                        "dispatch_blob_sha": candidate["dispatch_blob_sha"],
                        "discovery_state": candidate["discovery_state"],
                        "trust_state": "UNVALIDATED_CANDIDATE",
                    },
                )
            inserted, already_seen = self.ledger.record_poll_success(
                repository=self.config.repository,
                control_branch=self.config.control_branch,
                previous_cursor=previous_cursor,
                observed_remote_sha=fetched_sha,
                status=status,
                candidates=candidates,
                observed_at_utc=utc_now(),
            )
            result_status = (
                "CANDIDATES_DISCOVERED"
                if inserted and candidates
                else ("ALREADY_SEEN" if already_seen and candidates else status)
            )
            if already_seen:
                self._log(
                    "CANDIDATE_ALREADY_SEEN",
                    {
                        "branch": self.config.control_branch,
                        "control_commit_sha": fetched_sha,
                        "count": already_seen,
                    },
                )
            duration = round(time.monotonic() - started, 3)
            self._log(
                "POLL_COMPLETED",
                {
                    "status": result_status,
                    "control_commit_sha": fetched_sha,
                    "new_candidate_count": inserted,
                    "already_seen_count": already_seen,
                    "duration_seconds": duration,
                },
            )
            return PollResult(
                result_status,
                self.config.repository,
                self.config.control_branch,
                previous_cursor,
                fetched_sha,
                inserted,
                already_seen,
                tuple(candidates),
            )
        except TransportFailure as exc:
            return self._failure(
                started=started,
                previous_cursor=previous_cursor,
                observed_sha=observed_sha,
                status=exc.status,
                reason=exc.reason,
                error=exc.message,
            )
        except DatabaseError:
            raise
