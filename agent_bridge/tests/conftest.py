from __future__ import annotations

import sys
import uuid
from pathlib import Path

import pytest

from fox2_agent_bridge.config import BridgeConfig, TOOL_NAMES


@pytest.fixture
def tmp_path() -> Path:
    # pytest's mode=0700 temporary directories are inaccessible to the managed
    # Windows sandbox token. Inherit workspace ACLs without altering permissions.
    path = Path(__file__).resolve().parents[1] / 'test_artifacts' / uuid.uuid4().hex
    path.mkdir(parents=True)
    return path


@pytest.fixture
def bridge_config(tmp_path: Path, monkeypatch) -> BridgeConfig:
    monkeypatch.setattr('fox2_agent_bridge.config.WORKTREE_ROOT', tmp_path / 'worktrees')
    return BridgeConfig(
        bridge_root=tmp_path / "bridge",
        worktree_root=tmp_path / 'worktrees',
        tool_paths={name: Path(sys.executable) for name in TOOL_NAMES},
    )
