"""First-run initializes paused; repeat setup preserves explicit user choices."""
import json
import subprocess
import pytest
from fox2_agent_bridge import installation
from fox2_agent_bridge.desktop import initialize_runtime


def prepare(bridge_config, monkeypatch):
    root = bridge_config.bridge_root
    monkeypatch.setattr(installation, 'BRIDGE_ROOT', root)
    root.mkdir(parents=True)
    (root / 'current.json').write_text(json.dumps({'package_sha256': 'a' * 64}))
    python = root / 'versions' / ('a' * 64) / 'runtime/Scripts/python.exe'
    python.parent.mkdir(parents=True); python.write_bytes(b'owned-runtime-fixture')
    monkeypatch.setattr('fox2_agent_bridge.config.default_tool_paths', lambda _: dict(bridge_config.tool_paths))
    monkeypatch.setattr('fox2_agent_bridge.config.load_config', lambda _: bridge_config)
    monkeypatch.setattr('fox2_agent_bridge.preexec.probes.resolve_tool', lambda _: None)
    project = root / 'fixture-repository'; project.mkdir()
    worktrees = root / 'fixture-worktrees'; worktrees.mkdir()
    monkeypatch.setattr('fox2_agent_bridge.paths.PROJECT_ROOT', project)
    monkeypatch.setattr('fox2_agent_bridge.paths.WORKTREE_ROOT', worktrees)
    monkeypatch.setattr(installation.subprocess, 'run', lambda args, **kwargs:
                        subprocess.CompletedProcess(args, 0, '', ''))
    monkeypatch.setattr(installation, '_run', lambda args, **kwargs:
                        subprocess.CompletedProcess(args, 0, 'b' * 40 + '\trefs/heads/control\n', ''))
    return root


def test_fresh_setup_paused_and_repeat_preserves_config_and_user_resume(bridge_config, monkeypatch):
    root = prepare(bridge_config, monkeypatch)
    result = installation.first_run(root=root)
    assert result['status'] == 'SETUP_COMPLETE' and result['paused'] is True
    config = (root / 'config/bridge.toml').read_bytes()
    assert b'python =' not in config
    ledger = initialize_runtime(bridge_config)
    assert ledger.worker_state()['setup_complete'] is True
    ledger.control('resume')
    repeated = installation.first_run(root=root)
    assert repeated['paused'] is False
    assert (root / 'config/bridge.toml').read_bytes() == config


def test_missing_first_run_tool_does_not_write_config_or_claim_setup(bridge_config, monkeypatch):
    root = prepare(bridge_config, monkeypatch)
    monkeypatch.setattr('fox2_agent_bridge.config.default_tool_paths', lambda _: {'git': None})
    with pytest.raises(ValueError, match='setup requires tool: git'):
        installation.first_run(root=root)
    assert not (root / 'config/bridge.toml').exists()
    assert not bridge_config.database_path.exists()
