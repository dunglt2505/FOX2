"""Minimal FOX2 dispatch -> worktree -> Copilot CLI -> pushed-result E2E runner."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .config import REPOSITORY, BridgeConfig
from .copilot_adapter import CopilotAdapter
from .dispatch_poller import (
    FULL_SHA_PATTERN,
    DispatchPoller,
    GitTransport,
    _safe_error_text,
)
from .errors import (
    DispatchInvalid,
    ReplayBlocked,
    ToolExecFailed,
    TransportFailure,
    WorkspaceBlocked,
)
from .ledger import SQLiteLedger, utc_now
from .paths import validate_path

_BRANCH_PATTERN = re.compile(r"^work/[A-Za-z0-9._/-]+$")
_ALLOWED_EXECUTION_PATH = "BRIDGE_DIRECT_COPILOT_CLI"
_ALLOWED_AGENT_PRODUCT = "COPILOT"
_ALLOWED_AGENT_INTERFACE = "GITHUB_COPILOT_CLI"


@dataclass(frozen=True)
class E2EResult:
    status: str
    dispatch_id: str
    execution_id: str
    poll_status: str
    control_commit_sha: str
    dispatch_blob_sha: str
    worktree: str
    branch: str
    before_head: str
    after_head: str
    changed_paths: tuple[str, ...]
    copilot_exit_code: int
    copilot_stdout: str
    copilot_stderr: str

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "dispatch_id": self.dispatch_id,
            "execution_id": self.execution_id,
            "poll_status": self.poll_status,
            "control_commit_sha": self.control_commit_sha,
            "dispatch_blob_sha": self.dispatch_blob_sha,
            "worktree": self.worktree,
            "branch": self.branch,
            "before_head": self.before_head,
            "after_head": self.after_head,
            "changed_paths": list(self.changed_paths),
            "copilot_exit_code": self.copilot_exit_code,
            "copilot_stdout": self.copilot_stdout,
            "copilot_stderr": self.copilot_stderr,
        }


class BridgeE2ERunner:
    """Execute one immutable, single-use FOX2 Copilot dispatch."""

    def __init__(
        self,
        config: BridgeConfig,
        ledger: SQLiteLedger,
        *,
        logger: Any = None,
        transport: GitTransport | None = None,
        progress: Callable[[str], None] | None = None,
    ) -> None:
        self.config = config
        self.ledger = ledger
        self.logger = logger
        self.transport = transport or GitTransport(
            git_executable=(config.tool_paths or {})["git"] or Path("git"),
            store_path=config.bridge_root / "data" / "control.git",
        )
        self.progress = progress

    def _progress(self, message: str) -> None:
        if self.progress is not None:
            self.progress(message)

    @property
    def git_executable(self) -> str:
        configured = (self.config.tool_paths or {}).get("git")
        return str(configured or "git")

    def _git(
        self,
        arguments: list[str],
        *,
        cwd: Path | None = None,
        check: bool = True,
        binary: bool = False,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[Any]:
        command = [self.git_executable, *arguments]
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=not binary,
                encoding=None if binary else "utf-8",
                errors=None if binary else "replace",
                timeout=timeout,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise WorkspaceBlocked(
                f"Git workspace command failed to start or timed out: {type(exc).__name__}"
            ) from exc
        if check and result.returncode != 0:
            stderr = (
                result.stderr.decode("utf-8", "replace")
                if binary
                else result.stderr
            )
            raise WorkspaceBlocked(
                "Git workspace command failed: " + _safe_error_text(stderr)
            )
        return result

    @staticmethod
    def _required_mapping(payload: dict[str, object], key: str) -> dict[str, object]:
        value = payload.get(key)
        if not isinstance(value, dict):
            raise DispatchInvalid(f"{key} must be an object")
        return value

    @staticmethod
    def _required_string(payload: dict[str, object], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise DispatchInvalid(f"{key} must be a non-empty string")
        return value

    @staticmethod
    def _required_bool(payload: dict[str, object], key: str) -> bool:
        value = payload.get(key)
        if not isinstance(value, bool):
            raise DispatchInvalid(f"{key} must be boolean")
        return value

    def _validate_dispatch(
        self,
        raw: bytes,
        *,
        dispatch_path: str,
        observed_blob_sha: str,
    ) -> dict[str, object]:
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DispatchInvalid("dispatch is not valid UTF-8 JSON") from exc
        if not isinstance(payload, dict):
            raise DispatchInvalid("dispatch root must be an object")

        if payload.get("schema_version") != "0.6":
            raise DispatchInvalid("schema_version must be 0.6")
        if payload.get("project") != "FOX2":
            raise DispatchInvalid("project must be FOX2")
        if payload.get("type") != "NORMAL_AGENT_DISPATCH":
            raise DispatchInvalid("unsupported dispatch type")
        if payload.get("repository") != REPOSITORY:
            raise DispatchInvalid("dispatch repository mismatch")
        expected_control = f"refs/heads/{self.config.control_branch}"
        if payload.get("control_ref") != expected_control:
            raise DispatchInvalid("control_ref mismatch")
        if payload.get("max_runs") != 1:
            raise DispatchInvalid("max_runs must equal 1")

        dispatch_id = self._required_string(payload, "dispatch_id")
        wp_id = self._required_string(payload, "wp_id")
        if not dispatch_path.endswith(f"/{dispatch_id}.json"):
            raise DispatchInvalid("dispatch path must end with dispatch_id.json")
        if not wp_id.startswith("FOX2-"):
            raise DispatchInvalid("wp_id must be FOX2-scoped")

        branch = self._required_string(payload, "branch")
        if (
            not _BRANCH_PATTERN.fullmatch(branch)
            or ".." in branch
            or branch.endswith("/")
            or branch in {"work/main", "work/master"}
        ):
            raise DispatchInvalid("task branch is invalid")

        base_sha = self._required_string(payload, "base_sha")
        if not FULL_SHA_PATTERN.fullmatch(base_sha):
            raise DispatchInvalid("base_sha must be a full immutable SHA")

        agent = self._required_mapping(payload, "agent")
        if agent.get("product") != _ALLOWED_AGENT_PRODUCT:
            raise DispatchInvalid("agent.product must be COPILOT")
        if agent.get("interface") != _ALLOWED_AGENT_INTERFACE:
            raise DispatchInvalid("agent.interface must be GITHUB_COPILOT_CLI")
        if payload.get("execution_path") != _ALLOWED_EXECUTION_PATH:
            raise DispatchInvalid("execution_path must be BRIDGE_DIRECT_COPILOT_CLI")

        prompt = self._required_mapping(payload, "prompt")
        prompt_commit = self._required_string(prompt, "git_commit")
        prompt_path = self._required_string(prompt, "path")
        prompt_blob = self._required_string(prompt, "git_blob_sha1")
        prompt_sha256 = self._required_string(prompt, "sha256")
        if not FULL_SHA_PATTERN.fullmatch(prompt_commit):
            raise DispatchInvalid("prompt.git_commit must be a full immutable SHA")
        if not re.fullmatch(r"[0-9a-f]{40}", prompt_blob):
            raise DispatchInvalid("prompt.git_blob_sha1 must be a 40-char SHA-1")
        if not re.fullmatch(r"[0-9a-f]{64}", prompt_sha256):
            raise DispatchInvalid("prompt.sha256 must be a 64-char SHA-256")
        prompt_parts = Path(prompt_path).parts
        if (
            Path(prompt_path).is_absolute()
            or ".." in prompt_parts
            or not prompt_path.startswith("docs/agent_handoff/")
        ):
            raise DispatchInvalid("prompt.path is outside docs/agent_handoff")

        worktree = Path(self._required_string(payload, "worktree"))
        validate_path(
            worktree,
            allowed_roots=(self.config.worktree_root,),
            label="dispatch.worktree",
        )

        permissions = self._required_mapping(payload, "permissions")
        required_true = (
            "code_allowed",
            "git_code_push",
            "git_report_write",
            "git_report_push",
        )
        for key in required_true:
            if not self._required_bool(permissions, key):
                raise DispatchInvalid(f"permissions.{key} must be true")
        forbidden_true = (
            "pr_create",
            "merge_allowed",
            "production_provider",
            "broker_write",
            "live",
        )
        for key in forbidden_true:
            if self._required_bool(permissions, key):
                raise DispatchInvalid(f"permissions.{key} must be false")

        code_paths = payload.get("allowed_code_paths")
        report_paths = payload.get("allowed_report_paths")
        if not isinstance(code_paths, list) or not all(
            isinstance(item, str) and item for item in code_paths
        ):
            raise DispatchInvalid("allowed_code_paths must be a string list")
        if not isinstance(report_paths, list) or not all(
            isinstance(item, str) and item for item in report_paths
        ):
            raise DispatchInvalid("allowed_report_paths must be a string list")
        if not code_paths and not report_paths:
            raise DispatchInvalid("dispatch must allow at least one write path")

        payload["_observed_dispatch_blob_sha"] = observed_blob_sha
        payload["_payload_sha256"] = hashlib.sha256(raw).hexdigest()
        return payload

    def _remote_branch_head(self, branch: str) -> str:
        result = self._git(
            ["ls-remote", "--refs", "origin", f"refs/heads/{branch}"],
            cwd=self.config.local_repo,
        )
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if len(lines) != 1:
            raise WorkspaceBlocked("task branch is missing or ambiguous on origin")
        sha, ref = lines[0].split("\t", 1)
        if ref != f"refs/heads/{branch}" or not FULL_SHA_PATTERN.fullmatch(sha):
            raise WorkspaceBlocked("origin returned an invalid task branch identity")
        return sha

    def _resolve_worktree(self, payload: dict[str, object]) -> tuple[Path, str]:
        branch = str(payload["branch"])
        base_sha = str(payload["base_sha"])
        worktree = validate_path(
            Path(str(payload["worktree"])),
            allowed_roots=(self.config.worktree_root,),
            label="dispatch.worktree",
        )

        if not self.config.local_repo.exists():
            raise WorkspaceBlocked(
                f"FOX2 local repository does not exist: {self.config.local_repo}"
            )

        remote_head = self._remote_branch_head(branch)
        if remote_head != base_sha:
            raise WorkspaceBlocked(
                f"task branch head {remote_head} does not match dispatch base_sha {base_sha}"
            )

        self._git(
            ["-C", str(self.config.local_repo), "fetch", "--no-tags", "origin", branch]
        )

        if worktree.exists():
            if not (worktree / ".git").exists():
                raise WorkspaceBlocked("target worktree path exists but is not a Git worktree")
            current_branch = self._git(
                ["-C", str(worktree), "branch", "--show-current"]
            ).stdout.strip()
            if current_branch != branch:
                raise WorkspaceBlocked(
                    f"worktree is bound to {current_branch!r}, expected {branch!r}"
                )
            if self._git(
                ["-C", str(worktree), "status", "--porcelain"]
            ).stdout.strip():
                raise WorkspaceBlocked("target worktree is dirty before execution")
            self._git(
                ["-C", str(worktree), "pull", "--ff-only", "origin", branch]
            )
        else:
            worktree.parent.mkdir(parents=True, exist_ok=True)
            local_ref = self._git(
                [
                    "-C",
                    str(self.config.local_repo),
                    "show-ref",
                    "--verify",
                    "--quiet",
                    f"refs/heads/{branch}",
                ],
                check=False,
            )
            if local_ref.returncode == 0:
                self._git(
                    ["-C", str(self.config.local_repo), "worktree", "add", str(worktree), branch]
                )
            else:
                self._git(
                    [
                        "-C",
                        str(self.config.local_repo),
                        "worktree",
                        "add",
                        "--track",
                        "-b",
                        branch,
                        str(worktree),
                        f"origin/{branch}",
                    ]
                )

        head = self._git(["-C", str(worktree), "rev-parse", "HEAD"]).stdout.strip()
        if head != base_sha:
            raise WorkspaceBlocked(
                f"resolved worktree HEAD {head} does not match dispatch base_sha {base_sha}"
            )
        return worktree, head

    def _resolve_prompt(self, payload: dict[str, object]) -> str:
        prompt = self._required_mapping(payload, "prompt")
        commit = str(prompt["git_commit"])
        path = str(prompt["path"])
        expected_blob = str(prompt["git_blob_sha1"])
        expected_sha256 = str(prompt["sha256"])

        self._progress("fetch prompt authority from control branch")
        self._git(
            [
                "-C",
                str(self.config.local_repo),
                "fetch",
                "--no-tags",
                "origin",
                self.config.control_branch,
            ]
        )
        exists = self._git(
            ["-C", str(self.config.local_repo), "cat-file", "-e", f"{commit}^{{commit}}"],
            check=False,
        )
        if exists.returncode != 0:
            raise DispatchInvalid("prompt commit is not available after control-branch fetch")
        blob = self._git(
            ["-C", str(self.config.local_repo), "rev-parse", "--verify", f"{commit}:{path}"]
        ).stdout.strip()
        if blob != expected_blob:
            raise DispatchInvalid(
                f"prompt blob mismatch: observed {blob}, expected {expected_blob}"
            )
        raw = self._git(
            ["-C", str(self.config.local_repo), "show", f"{commit}:{path}"],
            binary=True,
        ).stdout
        observed_sha256 = hashlib.sha256(raw).hexdigest()
        if observed_sha256 != expected_sha256:
            raise DispatchInvalid(
                "prompt SHA-256 mismatch: "
                f"observed {observed_sha256}, expected {expected_sha256}"
            )
        try:
            return raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise DispatchInvalid("prompt is not UTF-8 text") from exc

    @staticmethod
    def _path_allowed(path: str, patterns: tuple[str, ...]) -> bool:
        normalized = path.replace("\\", "/")
        for pattern in patterns:
            candidate = pattern.replace("\\", "/")
            if candidate.endswith("/**"):
                prefix = candidate[:-3].rstrip("/")
                if normalized == prefix or normalized.startswith(prefix + "/"):
                    return True
            if fnmatch.fnmatchcase(normalized, candidate):
                return True
        return False

    def _prepare_required_parents(
        self,
        *,
        payload: dict[str, object],
        worktree: Path,
    ) -> None:
        acceptance = payload.get("acceptance")
        if acceptance is None:
            return
        if not isinstance(acceptance, dict):
            raise DispatchInvalid("acceptance must be an object when present")
        required_paths = acceptance.get("required_paths", [])
        if not isinstance(required_paths, list) or not all(
            isinstance(item, str) and item for item in required_paths
        ):
            raise DispatchInvalid("acceptance.required_paths must be a string list")

        allowed_patterns = tuple(
            str(item)
            for item in (
                list(payload.get("allowed_code_paths", []))
                + list(payload.get("allowed_report_paths", []))
            )
        )
        for required_path in required_paths:
            relative = Path(*required_path.split("/"))
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or not self._path_allowed(required_path, allowed_patterns)
            ):
                raise DispatchInvalid(
                    f"required E2E result path is outside dispatch scope: {required_path}"
                )
            target = (worktree / relative).resolve(strict=False)
            try:
                target.relative_to(worktree.resolve(strict=False))
            except ValueError as exc:
                raise DispatchInvalid(
                    f"required E2E result path escapes worktree: {required_path}"
                ) from exc
            target.parent.mkdir(parents=True, exist_ok=True)

    def _verify_result(
        self,
        *,
        payload: dict[str, object],
        worktree: Path,
        before_head: str,
        copilot_stdout: str,
    ) -> tuple[str, tuple[str, ...]]:
        if self._git(
            ["-C", str(worktree), "status", "--porcelain"]
        ).stdout.strip():
            raise WorkspaceBlocked("Copilot exited with a dirty worktree")

        after_head = self._git(
            ["-C", str(worktree), "rev-parse", "HEAD"]
        ).stdout.strip()
        if after_head == before_head:
            raise WorkspaceBlocked("Copilot did not create a result commit")

        remote_head = self._remote_branch_head(str(payload["branch"]))
        if remote_head != after_head:
            raise WorkspaceBlocked(
                "result commit is not pushed to the authorized task branch"
            )

        changed = tuple(
            line.strip().replace("\\", "/")
            for line in self._git(
                ["-C", str(worktree), "diff", "--name-only", f"{before_head}..{after_head}"]
            ).stdout.splitlines()
            if line.strip()
        )
        allowed_patterns = tuple(
            str(item)
            for item in (
                list(payload.get("allowed_code_paths", []))
                + list(payload.get("allowed_report_paths", []))
            )
        )
        unexpected = [
            path for path in changed if not self._path_allowed(path, allowed_patterns)
        ]
        if unexpected:
            raise WorkspaceBlocked(
                "result changed path(s) outside dispatch scope: " + ", ".join(unexpected)
            )

        acceptance = payload.get("acceptance")
        if acceptance is not None:
            if not isinstance(acceptance, dict):
                raise DispatchInvalid("acceptance must be an object when present")
            required_paths = acceptance.get("required_paths", [])
            if not isinstance(required_paths, list) or not all(
                isinstance(item, str) for item in required_paths
            ):
                raise DispatchInvalid("acceptance.required_paths must be a string list")
            for required_path in required_paths:
                target = worktree / Path(*required_path.split("/"))
                if not target.is_file():
                    raise WorkspaceBlocked(
                        f"required E2E result path is missing: {required_path}"
                    )
            stdout_contains = acceptance.get("stdout_contains")
            if stdout_contains is not None:
                if not isinstance(stdout_contains, str) or not stdout_contains:
                    raise DispatchInvalid(
                        "acceptance.stdout_contains must be a non-empty string"
                    )
                if stdout_contains not in copilot_stdout:
                    raise WorkspaceBlocked(
                        "Copilot stdout did not contain the required E2E marker"
                    )

        return after_head, changed

    def run_once(
        self,
        *,
        dispatch_path: str,
        timeout_seconds: int = 300,
    ) -> E2EResult:
        self._progress("poll control branch")
        poller = DispatchPoller(
            self.config,
            self.ledger,
            logger=self.logger,
            transport=self.transport,
        )
        poll = poller.poll_once()

        self._progress(f"poll complete: {poll.status}")
        self._progress("read immutable dispatch")
        control_sha = self.transport.query_control_sha(self.config.control_branch)
        if control_sha is None:
            raise TransportFailure(
                "configured control branch is unavailable",
                status="CONTROL_BRANCH_UNAVAILABLE",
                reason="CONTROL_BRANCH_UNAVAILABLE",
            )
        self.transport.fetch_control(self.config.control_branch, control_sha)
        raw_dispatch, dispatch_blob_sha = self.transport.read_dispatch_blob(
            control_sha,
            dispatch_path,
        )
        self._progress("validate dispatch")
        payload = self._validate_dispatch(
            raw_dispatch,
            dispatch_path=dispatch_path,
            observed_blob_sha=dispatch_blob_sha,
        )

        self._progress("resolve/create exact worktree")
        worktree, before_head = self._resolve_worktree(payload)
        self._progress(f"worktree ready: {worktree}")
        self._progress("resolve immutable prompt")
        prompt_text = self._resolve_prompt(payload)
        self._progress("prompt verified")

        dispatch_id = str(payload["dispatch_id"])
        execution_id = str(uuid.uuid4())
        self._progress(f"claim dispatch {dispatch_id}")
        claimed = self.ledger.claim_dispatch(
            dispatch_id=dispatch_id,
            payload_hash=str(payload["_payload_sha256"]),
            execution_id=execution_id,
            observed_at_utc=utc_now(),
        )
        if not claimed:
            existing = self.ledger.dispatch_state(dispatch_id)
            raise ReplayBlocked(
                f"dispatch {dispatch_id} was already claimed: {existing}"
            )

        try:
            self._progress("prepare authorized result parent directories")
            self._prepare_required_parents(payload=payload, worktree=worktree)
            self._progress("launch Copilot CLI")
            agent_result = CopilotAdapter(self.config).run_prompt(
                worktree=worktree,
                prompt=prompt_text,
                timeout_seconds=timeout_seconds,
                allow_write=True,
                allow_git=True,
                allow_github_url=False,
                silent=True,
                no_ask_user=True,
                progress=lambda stream, line: self._progress(
                    f"copilot[{stream}]: {line}"
                ),
                heartbeat_seconds=10,
            )
            if agent_result.exit_code != 0:
                raise ToolExecFailed(
                    "Copilot CLI returned non-zero exit code "
                    f"{agent_result.exit_code}: {_safe_error_text(agent_result.stderr)}"
                )

            self._progress(f"Copilot exited: {agent_result.exit_code}")
            self._progress("verify pushed result")
            after_head, changed_paths = self._verify_result(
                payload=payload,
                worktree=worktree,
                before_head=before_head,
                copilot_stdout=agent_result.stdout,
            )
            self._progress(f"result verified: {after_head}")
            self.ledger.finish_execution(
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                dispatch_state="PUSHED_UNREVIEWED",
                execution_state="PUSHED_UNREVIEWED",
                finished_at_utc=utc_now(),
            )
            self._progress("E2E state = PUSHED_UNREVIEWED")
            return E2EResult(
                status="PUSHED_UNREVIEWED",
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                poll_status=poll.status,
                control_commit_sha=control_sha,
                dispatch_blob_sha=dispatch_blob_sha,
                worktree=str(worktree),
                branch=str(payload["branch"]),
                before_head=before_head,
                after_head=after_head,
                changed_paths=changed_paths,
                copilot_exit_code=agent_result.exit_code,
                copilot_stdout=agent_result.stdout,
                copilot_stderr=agent_result.stderr,
            )
        except Exception:
            self.ledger.finish_execution(
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                dispatch_state="FAILED",
                execution_state="FAILED",
                finished_at_utc=utc_now(),
            )
            raise
