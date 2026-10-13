"""Minimal GitHub Copilot CLI relay used by the Bridge smoke pilot."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from .config import BridgeConfig
from .errors import PathInvalid, ToolExecFailed, ToolNotFound
from .paths import validate_path


@dataclass(frozen=True)
class CopilotRunResult:
    status: str
    exit_code: int
    stdout: str
    stderr: str
    executable: str
    worktree: str

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "executable": self.executable,
            "worktree": self.worktree,
        }


class CopilotAdapter:
    """Launch the installed Copilot CLI in one exact FOX2 worktree."""

    def __init__(self, config: BridgeConfig) -> None:
        self.config = config

    def _resolve_executable(self) -> Path:
        configured = (self.config.tool_paths or {}).get("copilot")
        candidates: list[Path] = []
        if configured is not None:
            candidates.append(configured)
        discovered = shutil.which("copilot")
        if discovered:
            path = Path(discovered)
            if path not in candidates:
                candidates.append(path)

        for candidate in candidates:
            try:
                if candidate.is_file():
                    return candidate.resolve()
            except OSError:
                continue
        raise ToolNotFound("GitHub Copilot CLI executable was not found")

    def _resolve_worktree(self, worktree: Path) -> Path:
        resolved = validate_path(
            worktree,
            allowed_roots=(self.config.worktree_root,),
            label="copilot_worktree",
        )
        if not resolved.exists() or not resolved.is_dir():
            raise PathInvalid("copilot_worktree does not exist")
        git_marker = resolved / ".git"
        if not git_marker.exists():
            raise PathInvalid("copilot_worktree is not a Git worktree")
        return resolved

    def run_prompt(
        self,
        *,
        worktree: Path,
        prompt: str,
        timeout_seconds: int = 120,
        allow_write: bool = False,
        allow_git: bool = False,
        allow_github_url: bool = False,
        silent: bool = False,
        no_ask_user: bool = False,
    ) -> CopilotRunResult:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ToolExecFailed("Copilot prompt must be non-empty")
        if timeout_seconds < 1 or timeout_seconds > 900:
            raise ToolExecFailed("Copilot timeout must be between 1 and 900 seconds")

        executable = self._resolve_executable()
        resolved_worktree = self._resolve_worktree(worktree)

        command = [
            str(executable),
            "-C",
            str(resolved_worktree),
            "--prompt",
            prompt,
        ]
        if silent:
            command.append("-s")
        if no_ask_user:
            command.append("--no-ask-user")
        if allow_write:
            command.append("--allow-tool=write")
        if allow_git:
            command.append("--allow-tool=shell(git:*)")
        if allow_github_url:
            command.append("--allow-url=github.com")
        environment = {
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
        }

        try:
            result = subprocess.run(
                command,
                cwd=resolved_worktree,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                check=False,
                env=environment,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ToolExecFailed(
                f"Copilot CLI failed to start or timed out: {type(exc).__name__}"
            ) from exc

        status = "COPILOT_EXITED" if result.returncode == 0 else "COPILOT_FAILED"
        return CopilotRunResult(
            status=status,
            exit_code=result.returncode,
            stdout=result.stdout[-12000:],
            stderr=result.stderr[-12000:],
            executable=str(executable),
            worktree=str(resolved_worktree),
        )
