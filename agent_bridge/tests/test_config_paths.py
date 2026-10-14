from __future__ import annotations

import json
from pathlib import Path

import pytest

from fox2_agent_bridge.config import BridgeConfig, load_config
from fox2_agent_bridge.errors import ConfigInvalid, PathInvalid
from fox2_agent_bridge.paths import BRIDGE_ROOT, PROJECT_ROOT, WORKTREE_ROOT


def test_default_configuration_loads_fixed_fox2_identity() -> None:
    config = BridgeConfig()
    local_app_data = Path.home() / "AppData" / "Local"

    assert config.project_id == "FOX2"
    assert config.repository == "dunglt2505/FOX2"
    assert config.local_repo == PROJECT_ROOT
    assert config.bridge_root == BRIDGE_ROOT
    assert config.worktree_root == WORKTREE_ROOT
    assert config.max_active_executions == 1
    assert config.control_branch == "work/FOX2-LOCAL-DISPATCH-chat"
    assert config.tool_paths["codex"] == (
        local_app_data / "Programs" / "OpenAI" / "Codex" / "bin" / "codex.exe"
    )
    assert config.tool_paths["copilot"] == (
        local_app_data
        / "Microsoft"
        / "WinGet"
        / "Packages"
        / "GitHub.Copilot_Microsoft.Winget.Source_8wekyb3d8bbwe"
        / "copilot.exe"
    )
    assert config.tool_paths["pwsh"] == Path(r'C:\Program Files\PowerShell\7\pwsh.exe')


@pytest.mark.parametrize("project_id", ["FOX", "MANTIS", "fox2"])
def test_non_fox2_project_is_rejected(project_id: str) -> None:
    with pytest.raises(ConfigInvalid, match="project_id"):
        BridgeConfig(project_id=project_id)


@pytest.mark.parametrize("repository", ["someone/FOX2", "dunglt2505/other"])
def test_invalid_repository_is_rejected(repository: str) -> None:
    with pytest.raises(ConfigInvalid, match="repository"):
        BridgeConfig(repository=repository)


def test_database_path_traversal_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(PathInvalid, match="database_path"):
        BridgeConfig(
            bridge_root=tmp_path / "bridge",
            database_path=tmp_path / "outside" / "bridge.db",
        )


def test_log_path_traversal_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(PathInvalid, match="log_directory"):
        BridgeConfig(
            bridge_root=tmp_path / "bridge",
            log_directory=tmp_path / "outside",
        )


def test_config_file_rejects_unknown_keys(tmp_path: Path) -> None:
    config_path = tmp_path / "bridge.toml"
    config_path.write_text("multi_project = true\n", encoding="utf-8")

    with pytest.raises(ConfigInvalid, match="unknown configuration"):
        load_config(config_path)


def test_config_file_rejects_alternate_bridge_root(tmp_path: Path) -> None:
    config_path = tmp_path / "bridge.toml"
    config_path.write_text(
        f"bridge_root = {json.dumps(str(tmp_path / 'alternate'))}\n",
        encoding="utf-8",
    )

    with pytest.raises(PathInvalid, match="fixed FOX2 Bridge path"):
        load_config(config_path)


def test_config_file_loads_fixed_fox2_values(tmp_path: Path) -> None:
    config_path = tmp_path / "bridge.toml"
    config_path.write_text(
        'project_id = "FOX2"\nrepository = "dunglt2505/FOX2"\n',
        encoding="utf-8",
    )

    config = load_config(config_path)

    assert config.project_id == "FOX2"
    assert config.repository == "dunglt2505/FOX2"
