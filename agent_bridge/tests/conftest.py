from __future__ import annotations

import sys
from pathlib import Path

import pytest

from fox2_agent_bridge.config import BridgeConfig, TOOL_NAMES


@pytest.fixture
def bridge_config(tmp_path: Path) -> BridgeConfig:
    return BridgeConfig(
        bridge_root=tmp_path / "bridge",
        tool_paths={name: Path(sys.executable) for name in TOOL_NAMES},
    )
