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


FAKE_CLI_HELP = ('--model --config --no-ask-user --output-format --auto-tier --max-ai-credits '
                 '--sandbox danger-full-access --ask-for-approval never --json --prompt -C '
                 '--allow-all-tools --allow-all-paths --allow-all-urls')


@pytest.fixture(autouse=True)
def fake_adapter_capability_probe(monkeypatch):
    """Adapters under test use deterministic fake CLI contracts, never paid Agents."""
    for product in ('codex', 'copilot'):
        module = f'fox2_agent_bridge.{product}_adapter'
        monkeypatch.setattr(module + '.help_text', lambda *_: FAKE_CLI_HELP)
        monkeypatch.setattr(module + '.version_text', lambda *_: 'fixture-cli 2.0')
