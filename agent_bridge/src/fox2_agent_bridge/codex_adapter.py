"""OpenAI Codex CLI relay used by FOX2 Bridge."""

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
from .errors import AgentNotStarted, PathInvalid, ToolExecFailed, ToolNotFound
from .paths import validate_path
from .agent_policy import help_text, policy_arguments, observe_metadata, permission_arguments, require_capabilities, version_text, tool_compatibility
from .logging_config import redact_context


@dataclass(frozen=True)
class CodexRunResult:
    status: str
    exit_code: int
    stdout: str
    stderr: str
    executable: str
    worktree: str
    metadata: dict[str, object] | None = None

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "executable": self.executable,
            "worktree": self.worktree,
            "metadata": self.metadata,
        }


class CodexAdapter:
    """Launch Codex CLI non-interactively in one exact FOX2 worktree."""

    def __init__(self, config: BridgeConfig) -> None:
        self.config = config

    def _resolve_executable(self) -> Path:
        configured = (self.config.tool_paths or {}).get("codex")
        candidates: list[Path] = []
        if configured is not None:
            candidates.append(configured)
        discovered = shutil.which("codex")
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
        raise ToolNotFound("Codex CLI executable was not found")

    def _resolve_worktree(self, worktree: Path) -> Path:
        resolved = validate_path(
            worktree,
            allowed_roots=(self.config.worktree_root,),
            label="codex_worktree",
        )
        if not resolved.exists() or not resolved.is_dir():
            raise PathInvalid("codex_worktree does not exist")
        if not (resolved / ".git").exists():
            raise PathInvalid("codex_worktree is not a Git worktree")
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
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
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
        timeout_seconds: int = 300,
        progress: Callable[[str, str], None] | None = None,
        heartbeat_seconds: int = 10,
        selection: dict[str, object] | None = None,
        configuration: Callable[[dict[str, object]], None] | None = None,
    ) -> CodexRunResult:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ToolExecFailed("Codex prompt must be non-empty")
        if timeout_seconds < 1 or timeout_seconds > 1800:
            raise ToolExecFailed("Codex timeout must be between 1 and 1800 seconds")
        if heartbeat_seconds < 1:
            raise ToolExecFailed("heartbeat_seconds must be positive")

        executable = self._resolve_executable()
        resolved_worktree = self._resolve_worktree(worktree)
        selection = selection or {'product': 'CODEX'}
        if selection.get('product') != 'CODEX':
            raise AgentNotStarted('Codex adapter cannot substitute for another Agent')
        exec_help = help_text(executable, 'exec')
        permission, applied = permission_arguments(selection, exec_help + '\n' + help_text(executable))
        require_capabilities(exec_help, ('--json',))
        extra, metadata = policy_arguments(selection, exec_help)
        metadata.update(applied_permission=applied, executable=str(executable))
        metadata['tool_compatibility'] = tool_compatibility(version_text(executable),
            selection.get('expected_cli_version'), exec_help, ('--sandbox', '--json'))
        command = [str(executable), *permission, 'exec', '--sandbox', 'danger-full-access', '--json', *extra, '-']
        if configuration:
            configuration(metadata)

        runtime_scripts = str(Path(sys.executable).resolve().parent)
        powershell_msi = Path(r"C:\Program Files\PowerShell\7")
        path_parts = [runtime_scripts]
        if (powershell_msi / "pwsh.exe").is_file():
            path_parts.append(str(powershell_msi))
        original_path = os.environ.get("PATH", "")
        if original_path:
            path_parts.append(original_path)
        environment = {
            **os.environ,
            "PATH": os.pathsep.join(path_parts),
            "GIT_TERMINAL_PROMPT": "0",
            "GCM_INTERACTIVE": "Never",
        }

        try:
            process = subprocess.Popen(
                command,
                cwd=resolved_worktree,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=environment,
            )
        except OSError as exc:
            raise AgentNotStarted(
                f"Codex CLI failed to start: {type(exc).__name__}"
            ) from exc

        assert process.stdin is not None
        assert process.stdout is not None
        assert process.stderr is not None

        try:
            process.stdin.write(prompt)
            if not prompt.endswith("\n"):
                process.stdin.write("\n")
            process.stdin.close()
        except OSError as exc:
            self._kill_process_tree(process)
            raise ToolExecFailed("Codex prompt could not be sent") from exc

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
                        f"Codex CLI timed out after {timeout_seconds}s"
                    )

                if progress is not None and now >= next_heartbeat:
                    progress("heartbeat", f"Codex CLI RUNNING {int(elapsed)}s")
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
                        observe_metadata(metadata, line)
                        if configuration:
                            configuration(metadata)
                    else:
                        stderr_parts.append(line)
                    if progress is not None:
                        progress(stream_name, redact_context(line.rstrip("\r\n")))

                if process.poll() is not None and len(closed_streams) == 2:
                    break
        except BaseException:
            self._kill_process_tree(process)
            raise
        finally:
            for thread in threads:
                thread.join(timeout=2)

        return_code = process.wait(timeout=5)
        stdout = "".join(stdout_parts)[-20000:]
        stderr = "".join(stderr_parts)[-20000:]
        status = "CODEX_EXITED" if return_code == 0 else "CODEX_FAILED"
        return CodexRunResult(
            status=status,
            exit_code=return_code,
            stdout=redact_context(stdout),
            stderr=redact_context(stderr),
            executable=str(executable),
            worktree=str(resolved_worktree),
            metadata=observe_metadata(metadata, stdout) if metadata else None,
        )
