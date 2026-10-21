"""FOX2 dispatch -> worktree -> selected local Agent CLI -> pushed-result E2E runner."""

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
from .codex_adapter import CodexAdapter
from .copilot_adapter import DEV_SHELL_CAPABILITIES, CopilotAdapter
from .dispatch_poller import (
    FULL_SHA_PATTERN,
    DispatchPoller,
    GitTransport,
    _safe_error_text,
)
from .errors import (
    BridgeError,
    AgentNotStarted,
    ToolNotFound,
    AuthUnavailable,
    DatabaseError,
    DispatchInvalid,
    ReplayBlocked,
    ToolExecFailed,
    TransportFailure,
    WorkspaceBlocked,
)
from .ledger import SQLiteLedger, utc_now
from .paths import validate_path
from .result_store import write_execution_report
from .agent_policy import validate_selection, ADAPTER_REGISTRY, ExecutionTuple, configuration_mismatch
from .logging_config import redact_context
from .dispatch_normalizer import normalize_dispatch
from .project_dictionary import PROJECT_ID, IDENTIFIERS, PROTECTED_AUTHORITY_DEFAULTS

_BRANCH_PATTERN = re.compile(r"^work/[A-Za-z0-9._/-]+$")
_AGENT_INTERFACES = {product: route[0] for product, route in ADAPTER_REGISTRY.items()}
_AGENT_EXECUTION_PATHS = {product: route[1] for product, route in ADAPTER_REGISTRY.items()}
_ADAPTERS = {"CODEX": CodexAdapter, "COPILOT": CopilotAdapter}


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
    agent_product: str
    agent_exit_code: int
    agent_stdout: str
    agent_stderr: str
    agent_metadata: dict[str, object] | None = None
    execution_tuple: dict[str, object] | None = None

    def as_dict(self) -> dict[str, object]:
        result: dict[str, object] = {
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
            "agent_product": self.agent_product,
            "agent_exit_code": self.agent_exit_code,
            "agent_stdout": self.agent_stdout,
            "agent_stderr": self.agent_stderr,
            "agent_metadata": self.agent_metadata,
            "execution_tuple": self.execution_tuple,
        }
        prefix = self.agent_product.lower()
        result[f"{prefix}_exit_code"] = self.agent_exit_code
        result[f"{prefix}_stdout"] = self.agent_stdout
        result[f"{prefix}_stderr"] = self.agent_stderr
        return result


class BridgeE2ERunner:
    """Execute one immutable, single-use FOX2 Agent dispatch."""

    def __init__(
        self,
        config: BridgeConfig,
        ledger: SQLiteLedger,
        *,
        logger: Any = None,
        transport: GitTransport | None = None,
        progress: Callable[[str], None] | None = None,
        can_claim: Callable[[], bool] | None = None,
    ) -> None:
        self.config = config
        self.ledger = ledger
        self.logger = logger
        self.transport = transport or GitTransport(
            git_executable=(config.tool_paths or {})["git"] or Path("git"),
            store_path=config.bridge_root / "data" / "control.git",
        )
        self.progress = progress
        self.can_claim = can_claim or (lambda: True)

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
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
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

    @staticmethod
    def _resolve_dev_shell_tools(payload: dict[str, object]) -> tuple[str, ...]:
        runtime = payload.get("runtime_contract")
        if runtime is None:
            return ()
        if not isinstance(runtime, dict):
            raise DispatchInvalid("runtime_contract must be an object when present")

        capabilities = runtime.get("dev_shell_capabilities", [])
        if not isinstance(capabilities, list) or not all(
            isinstance(item, str) and item for item in capabilities
        ):
            raise DispatchInvalid(
                "runtime_contract.dev_shell_capabilities must be a string list"
            )
        if len(capabilities) != len(set(capabilities)):
            raise DispatchInvalid(
                "runtime_contract.dev_shell_capabilities must not contain duplicates"
            )

        unknown = [
            capability
            for capability in capabilities
            if capability not in DEV_SHELL_CAPABILITIES
        ]
        if unknown:
            raise DispatchInvalid(
                "unsupported runtime_contract.dev_shell_capabilities: "
                + ", ".join(unknown)
            )

        tools: list[str] = []
        for capability in capabilities:
            tools.extend(DEV_SHELL_CAPABILITIES[capability])
        return tuple(dict.fromkeys(tools))

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

        payload = normalize_dispatch(payload, self.config.control_branch)
        return self._validate_normalized_dispatch(payload, raw=raw,
            dispatch_path=dispatch_path, observed_blob_sha=observed_blob_sha)

    def _validate_normalized_dispatch(self, payload, *, raw, dispatch_path, observed_blob_sha):
        if payload.get("project") != PROJECT_ID:
            raise DispatchInvalid("project must be FOX2")
        if payload.get("type") != "NORMAL_AGENT_DISPATCH":
            raise DispatchInvalid("unsupported dispatch type")
        if payload.get("repository") != REPOSITORY:
            raise DispatchInvalid("dispatch repository mismatch")
        expected_control = f"refs/heads/{self.config.control_branch}"
        if payload.get("control_ref") != expected_control:
            raise DispatchInvalid("control_ref mismatch")
        if type(payload.get("max_runs")) is not int or payload.get("max_runs") != 1:
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
        agent_product = self._required_string(agent, "product")
        expected_interface = _AGENT_INTERFACES.get(agent_product)
        if expected_interface is None:
            raise DispatchInvalid("agent.product must be COPILOT or CODEX")
        if agent.get("interface") != expected_interface:
            raise DispatchInvalid(
                f"agent.interface must be {expected_interface} for {agent_product}"
            )
        expected_execution_path = _AGENT_EXECUTION_PATHS[agent_product]
        payload['agent'] = validate_selection(agent)
        if payload.get("execution_path") != expected_execution_path:
            raise DispatchInvalid(
                f"execution_path must be {expected_execution_path} for {agent_product}"
            )

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

        delivery_owner = payload.get('delivery_owner', 'BRIDGE')
        if not isinstance(delivery_owner, str) or delivery_owner not in IDENTIFIERS['delivery_owners']:
            raise DispatchInvalid('delivery_owner must be AGENT or BRIDGE')
        payload['delivery_owner'] = delivery_owner
        profile = payload.get('permission_profile', payload['agent']['permission_profile'])
        if profile != payload['agent']['permission_profile']:
            raise DispatchInvalid('dispatch/Agent permission profile mismatch')
        payload['permission_profile'] = profile
        permissions = self._required_mapping(payload, "permissions")
        if permissions.get('permission_profile', profile) != profile:
            raise DispatchInvalid('permissions/Agent permission profile mismatch')
        required_true = (
            "code_allowed",
            "git_code_push",
            "git_report_write",
            "git_report_push",
        )
        for key in required_true:
            if not self._required_bool(permissions, key):
                raise DispatchInvalid(f"permissions.{key} must be true")
        forbidden_true = PROTECTED_AUTHORITY_DEFAULTS
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

        copilot_shell_tools = self._resolve_dev_shell_tools(payload)
        if agent_product == "CODEX" and copilot_shell_tools:
            raise DispatchInvalid(
                "CODEX dispatch must not request Copilot dev_shell_capabilities"
            )
        payload["_agent_product"] = agent_product
        payload["_copilot_shell_tools"] = (
            list(copilot_shell_tools) if agent_product == "COPILOT" else []
        )
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

    @staticmethod
    def _allowed_patterns(payload: dict[str, object]) -> tuple[str, ...]:
        return tuple(
            str(item)
            for item in (
                list(payload.get("allowed_code_paths", []))
                + list(payload.get("allowed_report_paths", []))
            )
        )

    def _verify_changed_paths(
        self,
        *,
        payload: dict[str, object],
        changed: tuple[str, ...],
    ) -> None:
        if not changed:
            raise WorkspaceBlocked("Agent did not create any result file changes")
        allowed_patterns = self._allowed_patterns(payload)
        unexpected = [
            path for path in changed if not self._path_allowed(path, allowed_patterns)
        ]
        if unexpected:
            raise WorkspaceBlocked(
                "result changed path(s) outside dispatch scope: " + ", ".join(unexpected)
            )

    @staticmethod
    def _verify_acceptance(
        *,
        payload: dict[str, object],
        worktree: Path,
        agent_stdout: str,
        agent_label: str,
    ) -> None:
        acceptance = payload.get("acceptance")
        if acceptance is None:
            return
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
            if stdout_contains not in agent_stdout:
                raise WorkspaceBlocked(
                    f"{agent_label} stdout did not contain the required E2E marker"
                )

    def _dirty_changed_paths(self, worktree: Path) -> tuple[str, ...]:
        paths: set[str] = set()
        commands = (
            ["diff", "--name-only"],
            ["diff", "--cached", "--name-only"],
            ["ls-files", "--others", "--exclude-standard"],
        )
        for command in commands:
            result = self._git(["-C", str(worktree), *command])
            for line in result.stdout.splitlines():
                value = line.strip().replace("\\", "/")
                if value:
                    paths.add(value)
        return tuple(sorted(paths))

    def _commit_and_push_codex_result(
        self,
        *,
        payload: dict[str, object],
        worktree: Path,
        before_head: str,
        agent_stdout: str,
    ) -> tuple[str, tuple[str, ...]]:
        if payload.get('delivery_owner', 'BRIDGE') != 'BRIDGE':
            raise WorkspaceBlocked('Bridge publication forbidden for Agent-owned delivery')
        current_branch = self._git(['-C', str(worktree), 'branch', '--show-current']).stdout.strip()
        if current_branch != payload['branch']:
            raise WorkspaceBlocked('publication worktree no longer matches exact task branch')
        local_head = self._git(
            ["-C", str(worktree), "rev-parse", "HEAD"]
        ).stdout.strip()
        if local_head != before_head:
            raise WorkspaceBlocked(
                "Agent changed Git history; dispatch assigns commit/push to Bridge"
            )
        remote_head = self._remote_branch_head(str(payload["branch"]))
        if remote_head != before_head:
            raise WorkspaceBlocked(
                "task branch changed remotely during Codex execution"
            )

        changed = self._dirty_changed_paths(worktree)
        self._verify_changed_paths(payload=payload, changed=changed)
        self._verify_acceptance(
            payload=payload,
            worktree=worktree,
            agent_stdout=agent_stdout,
            agent_label="Codex",
        )

        self._git(["-C", str(worktree), "diff", "--check"])
        self._git(["-C", str(worktree), "add", "-A", "--", *changed])
        self._git(["-C", str(worktree), "diff", "--cached", "--check"])
        dispatch_id = str(payload["dispatch_id"])
        self._git(
            [
                "-C",
                str(worktree),
                "-c",
                "user.name=FOX2 Bridge",
                "-c",
                "user.email=fox2-bridge@local.invalid",
                "commit",
                "-m",
                f"FOX2 Bridge result: {dispatch_id}",
            ]
        )
        after_head = self._git(
            ["-C", str(worktree), "rev-parse", "HEAD"]
        ).stdout.strip()
        execution_id = payload.get('_execution_id')
        if execution_id:
            row = next(row for row in self.ledger.pending_executions()
                       if row['execution_id'] == execution_id)
            context = json.loads(row['checkpoint_json'])
            context['expected_result_sha'] = after_head
            self.ledger.checkpoint(str(execution_id), 'PUBLISHING', context)
        self._git(
            [
                "-C",
                str(worktree),
                "push",
                "origin",
                f"HEAD:refs/heads/{payload['branch']}",
            ]
        )

        return self._verify_result(
            payload=payload,
            worktree=worktree,
            before_head=before_head,
            agent_stdout=agent_stdout,
            agent_label="Codex",
        )

    def _verify_result(
        self,
        *,
        payload: dict[str, object],
        worktree: Path,
        before_head: str,
        agent_stdout: str,
        agent_label: str,
    ) -> tuple[str, tuple[str, ...]]:
        current_branch = self._git(['-C', str(worktree), 'branch', '--show-current']).stdout.strip()
        if current_branch != payload['branch']:
            raise WorkspaceBlocked('result worktree no longer matches exact task branch')
        if self._git(
            ["-C", str(worktree), "status", "--porcelain"]
        ).stdout.strip():
            raise WorkspaceBlocked(f"{agent_label} result left a dirty worktree")

        after_head = self._git(
            ["-C", str(worktree), "rev-parse", "HEAD"]
        ).stdout.strip()
        if after_head == before_head:
            raise WorkspaceBlocked(f"{agent_label} did not create a result commit")
        self._git(['-C', str(worktree), 'merge-base', '--is-ancestor', before_head, after_head])

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
        self._verify_changed_paths(payload=payload, changed=changed)
        self._verify_acceptance(
            payload=payload,
            worktree=worktree,
            agent_stdout=agent_stdout,
            agent_label=agent_label,
        )
        return after_head, changed

    def _write_runtime_report_best_effort(
        self,
        *,
        dispatch_id: str,
        payload: dict[str, object],
    ) -> None:
        try:
            path = write_execution_report(
                bridge_root=self.config.bridge_root,
                dispatch_id=dispatch_id,
                payload=payload,
            )
            self._progress(f"runtime report: {path}")
        except DatabaseError as exc:
            self._progress(f"runtime report warning: {exc.message}")

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
        if not self.can_claim():
            raise ReplayBlocked('new claims paused or graceful stop requested')
        self._progress(f"claim dispatch {dispatch_id}")
        claimed = self.ledger.claim_dispatch(
            dispatch_id=dispatch_id,
            payload_hash=str(payload["_payload_sha256"]),
            execution_id=execution_id,
            observed_at_utc=utc_now(),
            honor_controls=True,
        )
        if not claimed:
            existing = self.ledger.dispatch_state(dispatch_id)
            raise ReplayBlocked(
                f"dispatch {dispatch_id} was already claimed: {existing}"
            )

        agent_result = None
        payload['_execution_id'] = execution_id
        agent_product = str(payload["_agent_product"])
        execution_tuple = ExecutionTuple(dispatch_id, str(payload['branch']), str(worktree),
                                         str(payload.get('prompt', {}).get('sha256', 'NOT_EXPOSED')),
                                         json.dumps(payload['agent'], sort_keys=True),
                                         str(payload.get('delivery_owner', 'BRIDGE')))
        checkpoint = {'payload': payload, 'before_head': before_head,
                      'execution_tuple': execution_tuple.as_dict()}
        self.ledger.update_worker(execution_display={'dispatch_id': dispatch_id,
            'requested': payload['agent'], 'metadata': None,
            'delivery_owner': payload.get('delivery_owner', 'BRIDGE')})
        self.ledger.checkpoint(execution_id, 'CLAIMED', checkpoint)
        try:
            self._progress("prepare authorized result parent directories")
            self._prepare_required_parents(payload=payload, worktree=worktree)
            self.ledger.checkpoint(execution_id, 'RUNNING', checkpoint)

            def persist_configuration(metadata):
                checkpoint['agent_metadata'] = metadata
                self.ledger.checkpoint(execution_id, 'RUNNING', checkpoint)
                self.ledger.update_worker(execution_display={
                    'dispatch_id': dispatch_id, 'requested': payload['agent'],
                    'metadata': metadata, 'delivery_owner': payload.get('delivery_owner', 'BRIDGE')})

            options = {}
            if agent_product == 'COPILOT':
                options = dict(allow_write=True, allow_git=payload.get('delivery_owner', 'BRIDGE') == 'AGENT',
                               allow_github_url=payload.get('delivery_owner', 'BRIDGE') == 'AGENT',
                               allowed_shell_tools=tuple(payload.get('_copilot_shell_tools', [])),
                               silent=False, no_ask_user=True)
            owner = payload.get('delivery_owner', 'BRIDGE')
            delivery_instruction = ('Commit and push only the exact authorized task branch; verify remote SHA.'
                                    if owner == 'AGENT' else
                                    'Leave commit and push to Bridge. Do not change Git history or publish.')
            # F1 hard host retirement/lease remains NOT_IMPLEMENTED. This
            # additional local gate prevents a PAUSE/STOP received after the
            # durable claim from reaching the paid Agent spawn checkpoint.
            # Preserve consumed identity even if launch is now denied.
            if not self.can_claim() or not self.ledger.spawn_permitted():
                raise AgentNotStarted(
                    'local PAUSE/STOP or invalid worker controls before Agent spawn'
                )
            self._progress(f'launch {agent_product} CLI')
            agent_result = _ADAPTERS[agent_product](self.config).run_prompt(
                worktree=worktree, prompt=prompt_text + '\n\nDispatch delivery owner: ' + owner +
                '\n' + delivery_instruction + '\nNo PR/main/merge/deploy/provider/broker/LIVE authority.',
                timeout_seconds=timeout_seconds, progress=lambda stream, line: self._progress(
                    f'{agent_product.lower()}[{stream}]: {line}'), heartbeat_seconds=10,
                selection=payload['agent'], configuration=persist_configuration, **options)
            checkpoint.update(agent_stdout=agent_result.stdout, agent_stderr=agent_result.stderr,
                              agent_exit_code=agent_result.exit_code,
                              agent_metadata=getattr(agent_result, 'metadata', None))
            self.ledger.checkpoint(execution_id, 'AGENT_EXITED', checkpoint)
            metadata = getattr(agent_result, 'metadata', None)
            if agent_result.exit_code != 0 or (metadata and (
                    metadata.get('post_start_failure') or configuration_mismatch(metadata))):
                raise ToolExecFailed(f'{agent_product} post-start failure/configuration mismatch: '
                                     f'exit={agent_result.exit_code}: {_safe_error_text(agent_result.stderr)}')
            if owner == 'BRIDGE':
                self._progress(f'Bridge verifies, commits, and pushes {agent_product} result')
                self.ledger.checkpoint(execution_id, 'PUBLISHING', checkpoint)
                after_head, changed_paths = self._commit_and_push_codex_result(
                    payload=payload, worktree=worktree, before_head=before_head,
                    agent_stdout=agent_result.stdout)
            else:
                self._progress('verify pushed result owned by Agent')
                after_head, changed_paths = self._verify_result(
                    payload=payload, worktree=worktree, before_head=before_head,
                    agent_stdout=agent_result.stdout, agent_label=agent_product)

            self._progress(f"result verified: {after_head}")
            result = E2EResult(
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
                agent_product=agent_product,
                agent_exit_code=agent_result.exit_code,
                agent_stdout=agent_result.stdout,
                agent_stderr=agent_result.stderr,
                agent_metadata=getattr(agent_result, 'metadata', None),
                execution_tuple=execution_tuple.as_dict(),
            )
            self.ledger.finish_execution(
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                dispatch_state="PUSHED_UNREVIEWED",
                execution_state="PUSHED_UNREVIEWED",
                finished_at_utc=utc_now(),
                result=result.as_dict(),
            )
            self._write_runtime_report_best_effort(
                dispatch_id=dispatch_id,
                payload={"status": "PUSHED_UNREVIEWED", "result": result.as_dict()},
            )
            self._progress("E2E state = PUSHED_UNREVIEWED")
            return result
        except KeyboardInterrupt:
            finished = utc_now()
            self.ledger.finish_execution(
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                dispatch_state="NEEDS_RECONCILIATION",
                execution_state="RUNNING",
                finished_at_utc=finished,
                error_code="USER_INTERRUPT",
                error_message="Execution interrupted by local user",
            )
            self._write_runtime_report_best_effort(
                dispatch_id=dispatch_id,
                payload={
                    "status": "NEEDS_RECONCILIATION",
                    "dispatch_id": dispatch_id,
                    "execution_id": execution_id,
                    "error": {
                        "code": "USER_INTERRUPT",
                        "message": "Execution interrupted by local user",
                    },
                    "finished_at_utc": finished,
                },
            )
            raise
        except Exception as exc:
            finished = utc_now()
            if isinstance(exc, BridgeError):
                error_code = exc.code
                error_message = exc.message
            else:
                error_code = "UNEXPECTED_ERROR"
                error_message = f"{type(exc).__name__}: {exc}"
            failure_result: dict[str, object] = {
                "dispatch_id": dispatch_id,
                "execution_id": execution_id,
                "branch": str(payload["branch"]),
                "worktree": str(worktree),
                "before_head": before_head,
                "execution_tuple": execution_tuple.as_dict(),
                "agent_metadata": checkpoint.get("agent_metadata"),
            }
            if agent_result is not None:
                failure_result["agent_product"] = agent_product
                failure_result[agent_product.lower()] = agent_result.as_dict()

            pending = self.ledger.pending_executions()
            stage = next((row['stage'] for row in pending if row['execution_id'] == execution_id), 'UNKNOWN')
            metadata = getattr(agent_result, 'metadata', None)
            nonzero_after_start = agent_result is not None and (agent_result.exit_code != 0 or
                bool(metadata and (metadata.get('post_start_failure') or configuration_mismatch(metadata))))
            uncertain = agent_result is not None or stage == 'PUBLISHING' or (agent_result is None and not isinstance(exc, (AgentNotStarted, ToolNotFound, AuthUnavailable)))
            self.ledger.finish_execution(
                dispatch_id=dispatch_id,
                execution_id=execution_id,
                dispatch_state="NEEDS_RECONCILIATION" if uncertain else "FAILED",
                execution_state=("NEEDS_RECONCILIATION" if nonzero_after_start
                                 else "RUNNING" if uncertain else "FAILED"),
                finished_at_utc=finished,
                result=failure_result,
                error_code=error_code,
                error_message=redact_context(error_message[:4000]),
            )
            self._write_runtime_report_best_effort(
                dispatch_id=dispatch_id,
                payload={
                    "status": "NEEDS_RECONCILIATION" if uncertain else "FAILED",
                    "dispatch_id": dispatch_id,
                    "execution_id": execution_id,
                    "result": failure_result,
                    "error": {
                        "code": error_code,
                        "message": error_message[:4000],
                    },
                    "finished_at_utc": finished,
                },
            )
            raise
