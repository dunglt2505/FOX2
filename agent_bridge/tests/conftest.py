from __future__ import annotations

import sys
import shutil
import uuid
import os
import stat
import gc
import logging
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fox2_agent_bridge.config import BridgeConfig, TOOL_NAMES


@pytest.fixture
def tmp_path():
    # Windows sandbox identities cannot traverse pytest's mode=0700 directories.
    path = Path(__file__).parent / ".sandbox-tmp" / uuid.uuid4().hex
    path.mkdir(parents=True)
    try:
        yield path.resolve()
    finally:
        logger = logging.getLogger("fox2_agent_bridge")
        for handler in tuple(logger.handlers):
            filename = getattr(handler, "baseFilename", None)
            if filename and Path(filename).is_relative_to(path.resolve()):
                logger.removeHandler(handler)
                handler.close()
        gc.collect()
        def writable_retry(function, target, error):
            os.chmod(target, stat.S_IWRITE)
            function(target)
        shutil.rmtree(path, onexc=writable_retry)


@pytest.fixture
def bridge_config(tmp_path: Path, monkeypatch) -> BridgeConfig:
    monkeypatch.setattr("fox2_agent_bridge.config.WORKTREE_ROOT", tmp_path / "worktrees")
    config = BridgeConfig(
        bridge_root=tmp_path / "bridge",
        worktree_root=tmp_path / "worktrees",
        tool_paths={name: Path(sys.executable) for name in TOOL_NAMES},
    )
    return config
