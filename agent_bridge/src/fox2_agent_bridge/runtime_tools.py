"""Harmless executable discovery and factual capability probes."""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from .config import TOOL_NAMES, BridgeConfig
from .errors import ToolExecFailed, ToolNotFound
from .models import AuthStatus, Status, ToolCapability, ToolRecord

_CAPABILITY_FLAGS = {
    "codex": {
        "non_interactive_prompt": r"\bcodex exec\b",
        "model_selection": r"--model",
        "reasoning_effort_selection": r"--reasoning-effort",
        "working_directory_selection": r"--cd",
        "machine_readable_output": r"--json",
    },
    "copilot": {
        "non_interactive_prompt": r"--prompt",
        "model_selection": r"--model",
        "reasoning_effort_selection": r"--reasoning-effort",
        "auto_mode_selection": r"--auto-tier|--allow-all-tools",
        "working_directory_selection": r"-C\s+<directory>",
        "machine_readable_output": r"--output-format",
    },
}


def _run(
    executable: Path,
    arguments: tuple[str, ...],
    *,
    timeout: float = 12.0,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            [str(executable), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ToolExecFailed(f"tool invocation failed: {type(exc).__name__}") from exc


def _find_executable(name: str, configured: Path | None) -> tuple[Path | None, str | None]:
    candidates: list[Path] = []
    if configured is not None:
        if not configured.is_absolute():
            return None, "configured executable path is not absolute"
        candidates.append(configured)
    path_candidate = shutil.which(name)
    if path_candidate:
        resolved = Path(path_candidate).resolve()
        if resolved not in candidates:
            candidates.append(resolved)
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve(), None
    if configured is not None:
        return None, "configured executable not found; PATH fallback also unavailable"
    return None, "executable not found on PATH"


def _auth_status(name: str, executable: Path) -> AuthStatus:
    if name == "gh":
        result = _run(executable, ("auth", "status"))
        return AuthStatus.AUTHENTICATED if result.returncode == 0 else AuthStatus.NOT_AUTHENTICATED
    if name == "codex":
        result = _run(executable, ("login", "status"))
        combined = f"{result.stdout}\n{result.stderr}".lower()
        if result.returncode == 0 and "logged in" in combined:
            return AuthStatus.AUTHENTICATED
        return AuthStatus.NOT_AUTHENTICATED
    return AuthStatus.UNVERIFIED


def _capabilities(name: str, executable: Path) -> tuple[ToolCapability, ...]:
    flags = _CAPABILITY_FLAGS.get(name)
    if flags is None:
        return ()
    help_arguments = ("exec", "--help") if name == "codex" else ("--help",)
    try:
        result = _run(executable, help_arguments)
    except ToolExecFailed:
        return tuple(
            ToolCapability(capability, Status.UNVERIFIED, "help invocation failed")
            for capability in flags
        )
    if result.returncode != 0:
        return tuple(
            ToolCapability(capability, Status.UNVERIFIED, "help invocation returned non-zero")
            for capability in flags
        )
    output = f"{result.stdout}\n{result.stderr}"
    return tuple(
        ToolCapability(
            capability,
            Status.READY if re.search(pattern, output, re.IGNORECASE) else Status.UNVERIFIED,
            (
                "observed in relevant --help"
                if re.search(pattern, output, re.IGNORECASE)
                else "not exposed in relevant --help"
            ),
        )
        for capability, pattern in flags.items()
    ) + (
        ToolCapability(
            "prompt_execution_exit_code",
            Status.UNVERIFIED,
            "prompt execution was intentionally not run in BRG-010",
        ),
    )


def discover_tool(name: str, configured_path: Path | None) -> ToolRecord:
    if name not in TOOL_NAMES:
        raise ValueError(f"unsupported runtime tool: {name}")
    observed_at = datetime.now(UTC)
    executable, error = _find_executable(name, configured_path)
    if executable is None:
        return ToolRecord(
            tool_name=name,
            configured_path=configured_path,
            executable_path=None,
            version=None,
            available=False,
            version_exit_code=None,
            version_stdout_available=False,
            version_stderr_available=False,
            auth_status=AuthStatus.UNVERIFIED,
            capabilities=(),
            observed_at=observed_at,
            error=error,
        )
    try:
        result = _run(executable, ("--version",))
    except ToolExecFailed as exc:
        return ToolRecord(
            tool_name=name,
            configured_path=configured_path,
            executable_path=executable,
            version=None,
            available=False,
            version_exit_code=None,
            version_stdout_available=False,
            version_stderr_available=False,
            auth_status=AuthStatus.UNVERIFIED,
            capabilities=(),
            observed_at=observed_at,
            error=exc.message,
        )
    version_output = result.stdout.strip() or result.stderr.strip()
    if result.returncode != 0:
        return ToolRecord(
            tool_name=name,
            configured_path=configured_path,
            executable_path=executable,
            version=version_output.splitlines()[0] if version_output else None,
            available=False,
            version_exit_code=result.returncode,
            version_stdout_available=bool(result.stdout),
            version_stderr_available=bool(result.stderr),
            auth_status=AuthStatus.UNVERIFIED,
            capabilities=(),
            observed_at=observed_at,
            error=f"--version returned exit code {result.returncode}",
        )
    version = version_output.splitlines()[0] if version_output else "version output empty"
    try:
        auth = _auth_status(name, executable)
    except ToolExecFailed:
        auth = AuthStatus.UNVERIFIED
    return ToolRecord(
        tool_name=name,
        configured_path=configured_path,
        executable_path=executable,
        version=version,
        available=True,
        version_exit_code=result.returncode,
        version_stdout_available=bool(result.stdout),
        version_stderr_available=bool(result.stderr),
        auth_status=auth,
        capabilities=_capabilities(name, executable),
        observed_at=observed_at,
    )


def discover_all(config: BridgeConfig) -> tuple[ToolRecord, ...]:
    paths = config.tool_paths or {}
    return tuple(discover_tool(name, paths.get(name)) for name in TOOL_NAMES)
