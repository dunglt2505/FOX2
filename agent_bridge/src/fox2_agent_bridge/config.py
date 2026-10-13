"""Typed, FOX2-specific TOML configuration."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import BridgeError, ConfigInvalid, PathInvalid
from .paths import BRIDGE_ROOT, PROJECT_ROOT, WORKTREE_ROOT, canonical, validate_path

PROJECT_ID = "FOX2"
REPOSITORY = "dunglt2505/FOX2"
CONTROL_BRANCH = "work/FOX2-LOCAL-DISPATCH-chat"
REVIEW_EVENT_BRANCH = "work/FOX2-REVIEW-EVENTS-bridge"
REVIEW_BRANCH = "work/FOX2-CHAT-REVIEWS"
MAX_ACTIVE_EXECUTIONS = 1
TOOL_NAMES = ("git", "gh", "codex", "copilot", "pwsh", "python")


def default_tool_paths(bridge_root: Path) -> dict[str, Path]:
    local_app_data = Path.home() / "AppData" / "Local"
    return {
        "git": Path(r"C:\Program Files\Git\cmd\git.exe"),
        "gh": Path(r"C:\Program Files\GitHub CLI\gh.exe"),
        "codex": (
            local_app_data
            / "Programs"
            / "OpenAI"
            / "Codex"
            / "bin"
            / "codex.exe"
        ),
        "copilot": (
            local_app_data
            / "Microsoft"
            / "WinGet"
            / "Packages"
            / "GitHub.Copilot_Microsoft.Winget.Source_8wekyb3d8bbwe"
            / "copilot.exe"
        ),
        "pwsh": local_app_data / "Microsoft" / "WindowsApps" / "pwsh.exe",
        "python": bridge_root / ".venv" / "Scripts" / "python.exe",
    }


@dataclass(frozen=True)
class BridgeConfig:
    project_id: str = PROJECT_ID
    repository: str = REPOSITORY
    local_repo: Path = PROJECT_ROOT
    bridge_root: Path = BRIDGE_ROOT
    worktree_root: Path = WORKTREE_ROOT
    control_branch: str = CONTROL_BRANCH
    review_event_branch: str = REVIEW_EVENT_BRANCH
    review_branch: str = REVIEW_BRANCH
    poll_interval_seconds: int = 30
    database_path: Path | None = None
    log_directory: Path | None = None
    max_active_executions: int = MAX_ACTIVE_EXECUTIONS
    tool_paths: dict[str, Path | None] | None = None

    def __post_init__(self) -> None:
        root = canonical(self.bridge_root)
        object.__setattr__(self, "bridge_root", root)
        object.__setattr__(self, "local_repo", canonical(self.local_repo))
        object.__setattr__(self, "worktree_root", canonical(self.worktree_root))
        object.__setattr__(
            self,
            "database_path",
            canonical(self.database_path or root / "data" / "bridge.db"),
        )
        object.__setattr__(
            self,
            "log_directory",
            canonical(self.log_directory or root / "logs"),
        )

        if self.project_id != PROJECT_ID:
            raise ConfigInvalid(f"project_id must be {PROJECT_ID}")
        if self.repository != REPOSITORY:
            raise ConfigInvalid(f"repository must be {REPOSITORY}")
        if self.control_branch != CONTROL_BRANCH:
            raise ConfigInvalid(f"control_branch must be {CONTROL_BRANCH}")
        if (
            isinstance(self.poll_interval_seconds, bool)
            or not isinstance(self.poll_interval_seconds, int)
            or self.poll_interval_seconds < 1
        ):
            raise ConfigInvalid("poll_interval_seconds must be a positive integer")
        if (
            isinstance(self.max_active_executions, bool)
            or not isinstance(self.max_active_executions, int)
        ):
            raise ConfigInvalid("max_active_executions must be an integer")
        if self.local_repo != canonical(PROJECT_ROOT):
            raise ConfigInvalid("local_repo must be the fixed FOX2 repository path")
        if self.worktree_root != canonical(WORKTREE_ROOT):
            raise ConfigInvalid("worktree_root must be the fixed FOX2 worktree path")
        if self.max_active_executions != MAX_ACTIVE_EXECUTIONS:
            raise ConfigInvalid("max_active_executions must remain 1 in BRG-010")

        tool_paths = self.tool_paths or default_tool_paths(root)
        unknown_tools = set(tool_paths) - set(TOOL_NAMES)
        if unknown_tools:
            raise ConfigInvalid(f"unknown tool path(s): {', '.join(sorted(unknown_tools))}")
        normalized_tools: dict[str, Path | None] = {}
        for name in TOOL_NAMES:
            tool_path = tool_paths.get(name)
            if tool_path is not None and not tool_path.is_absolute():
                raise PathInvalid(f"configured path for {name} must be absolute")
            normalized_tools[name] = tool_path.expanduser() if tool_path else None
        object.__setattr__(self, "tool_paths", normalized_tools)

        validate_path(
            self.database_path,
            allowed_roots=(self.bridge_root,),
            label="database_path",
        )
        validate_path(
            self.log_directory,
            allowed_roots=(self.bridge_root,),
            label="log_directory",
        )


def _path_value(value: Any, name: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ConfigInvalid(f"{name} must be a non-empty path string")
    return Path(value)


def load_config(config_path: Path | None = None) -> BridgeConfig:
    if config_path is None:
        return BridgeConfig()
    if not config_path.exists():
        raise ConfigInvalid(f"configuration file does not exist: {config_path}")
    try:
        with config_path.open("rb") as stream:
            raw = tomllib.load(stream)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigInvalid(f"cannot read configuration: {exc}") from exc

    allowed = {
        "project_id",
        "repository",
        "local_repo",
        "bridge_root",
        "worktree_root",
        "control_branch",
        "review_event_branch",
        "review_branch",
        "poll_interval_seconds",
        "database_path",
        "log_directory",
        "max_active_executions",
        "tools",
    }
    unknown = set(raw) - allowed
    if unknown:
        raise ConfigInvalid(f"unknown configuration key(s): {', '.join(sorted(unknown))}")

    base = BridgeConfig()
    values: dict[str, Any] = dict(raw)
    for key in ("local_repo", "bridge_root", "worktree_root", "database_path", "log_directory"):
        if key in values:
            values[key] = _path_value(values[key], key)
    tools = values.pop("tools", {})
    if not isinstance(tools, dict):
        raise ConfigInvalid("tools must be a table")
    configured_tools: dict[str, Path | None] = dict(base.tool_paths or {})
    for name, value in tools.items():
        if name not in TOOL_NAMES:
            raise ConfigInvalid(f"unknown tool path: {name}")
        if value is not None:
            configured_tools[name] = _path_value(value, f"tools.{name}")
        else:
            configured_tools[name] = None
    values["tool_paths"] = configured_tools
    try:
        config = BridgeConfig(**values)
        if config.bridge_root != canonical(BRIDGE_ROOT):
            raise PathInvalid("bridge_root must be the fixed FOX2 Bridge path")
        return config
    except BridgeError:
        raise
    except TypeError as exc:
        raise ConfigInvalid(f"invalid configuration value: {exc}") from exc
