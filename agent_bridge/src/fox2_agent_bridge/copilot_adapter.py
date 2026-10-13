"""GitHub Copilot CLI relay used by FOX2 Bridge."""

from __future__ import annotations

import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, TextIO

from .config import BridgeConfig
from .errors import PathInvalid, ToolExecFailed, ToolNotFound
from .paths import validate_path


DEV_SHELL_CAPABILITIES: dict[str, tuple[str, ...]] = {
    "PYTEST": (
        "shell(python -m pytest --version)",
        "shell(python -m pytest -q)",
        "shell(python -m pytest tests/m1_p2_01 -q)",
    ),
}


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
        if not (resolved / ".git").exists():
            raise PathInvalid("copilot_worktree is not a Git worktree")
        return resolved

    @staticmethod
    def _reader(
        stream: TextIO,
        name: str,
        events: queue.Queue[tuple[str, str | None]],
    ) -> None:
        try:
            for line in iter(stream.readline, ""):
                events.put((name, line))
        finally:
            events.put((name, None))

    @staticmethod
    def _kill_process_tree(process: subprocess.Popen[str]) -> None:
        if process.poll() is not None:
            return
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                capture_output=True,
                text=True,
                check=False,
                timeout=15,
            )
        else:
            process.kill()

    def run_prompt(
        self,
        *,
        worktree: Path,
        prompt: str,
        timeout_seconds: int = 120,
        allow_write: bool = False,
        allow_git: bool = False,
        allow_github_url: bool = False,
        allowed_shell_tools: tuple[str, ...] = (),
        silent: bool = False,
        no_ask_user: bool = False,
        progress: Callable[[str, str], None] | None = None,
        heartbeat_seconds: int = 10,
    ) -> CopilotRunResult:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ToolExecFailed("Copilot prompt must be non-empty")
        if timeout_seconds < 1 or timeout_seconds > 900:
            raise ToolExecFailed("Copilot timeout must be between 1 and 900 seconds")
        if heartbeat_seconds < 1:
            raise ToolExecFailed("heartbeat_seconds must be positive")

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
        known_shell_tools = {
            tool
            for tools in DEV_SHELL_CAPABILITIES.values()
            for tool in tools
        }
        unknown_shell_tools = [
            tool for tool in allowed_shell_tools if tool not in known_shell_tools
        ]
        if unknown_shell_tools:
            raise ToolExecFailed(
                "Copilot shell permission is outside the Bridge safe catalog: "
                + ", ".join(unknown_shell_tools)
            )
        for tool in dict.fromkeys(allowed_shell_tools):
            command.append(f"--allow-tool={tool}")

        if allow_github_url:
            command.append("--allow-url=github.com")

        runtime_scripts = str(Path(sys.executable).resolve().parent)
        original_path = os.environ.get("PATH", "")
        environment = {
            **os.environ,
            "PATH": runtime_scripts
            + (os.pathsep + original_path if original_path else ""),
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
        }

        try:
            process = subprocess.Popen(
                command,
                cwd=resolved_worktree,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=environment,
            )
        except OSError as exc:
            raise ToolExecFailed(
                f"Copilot CLI failed to start: {type(exc).__name__}"
            ) from exc

        assert process.stdout is not None
        assert process.stderr is not None

        events: queue.Queue[tuple[str, str | None]] = queue.Queue()
        threads = [
            threading.Thread(
                target=self._reader,
                args=(process.stdout, "stdout", events),
                daemon=True,
            ),
            threading.Thread(
                target=self._reader,
                args=(process.stderr, "stderr", events),
                daemon=True,
            ),
        ]
        for thread in threads:
            thread.start()

        stdout_parts: list[str] = []
        stderr_parts: list[str] = []
        closed_streams: set[str] = set()
        started = time.monotonic()
        next_heartbeat = started + heartbeat_seconds

        try:
            while True:
                now = time.monotonic()
                elapsed = now - started
                if elapsed >= timeout_seconds:
                    self._kill_process_tree(process)
                    raise ToolExecFailed(
                        f"Copilot CLI timed out after {timeout_seconds}s"
                    )

                if progress is not None and now >= next_heartbeat:
                    progress("heartbeat", f"Copilot CLI RUNNING {int(elapsed)}s")
                    next_heartbeat = now + heartbeat_seconds

                try:
                    stream_name, line = events.get(timeout=0.5)
                except queue.Empty:
                    if process.poll() is not None and len(closed_streams) == 2:
                        break
                    continue

                if line is None:
                    closed_streams.add(stream_name)
                else:
                    if stream_name == "stdout":
                        stdout_parts.append(line)
                    else:
                        stderr_parts.append(line)
                    if progress is not None:
                        progress(stream_name, line.rstrip("\r\n"))

                if process.poll() is not None and len(closed_streams) == 2:
                    break
        except BaseException:
            self._kill_process_tree(process)
            raise
        finally:
            for thread in threads:
                thread.join(timeout=2)

        return_code = process.wait(timeout=5)
        stdout = "".join(stdout_parts)[-12000:]
        stderr = "".join(stderr_parts)[-12000:]
        status = "COPILOT_EXITED" if return_code == 0 else "COPILOT_FAILED"
        return CopilotRunResult(
            status=status,
            exit_code=return_code,
            stdout=stdout,
            stderr=stderr,
            executable=str(executable),
            worktree=str(resolved_worktree),
        )
