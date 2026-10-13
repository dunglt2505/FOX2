from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from fox2_agent_bridge.copilot_adapter import CopilotAdapter
from fox2_agent_bridge.errors import PathInvalid


def test_copilot_smoke_builds_cli_command(monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path):
    worktree = bridge_config.worktree_root / "COPILOT-SMOKE"
    worktree.mkdir(parents=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    executable = tmp_path / "copilot.exe"
    executable.write_text("", encoding="utf-8")

    tool_paths = dict(bridge_config.tool_paths or {})
    tool_paths["copilot"] = executable
    config = type(bridge_config)(
        bridge_root=bridge_config.bridge_root,
        tool_paths=tool_paths,
    )
    adapter = CopilotAdapter(config)

    observed: dict[str, object] = {}

    def fake_run(command, **kwargs):
        observed["command"] = command
        observed["cwd"] = kwargs["cwd"]
        return SimpleNamespace(returncode=0, stdout="FOX2_BRIDGE_COPILOT_SMOKE_OK\n", stderr="")

    monkeypatch.setattr("fox2_agent_bridge.copilot_adapter.subprocess.run", fake_run)

    result = adapter.run_prompt(
        worktree=worktree,
        prompt="Return exactly FOX2_BRIDGE_COPILOT_SMOKE_OK.",
        timeout_seconds=30,
    )

    assert result.status == "COPILOT_EXITED"
    assert result.exit_code == 0
    assert result.stdout.strip() == "FOX2_BRIDGE_COPILOT_SMOKE_OK"
    assert observed["cwd"] == worktree.resolve()
    command = observed["command"]
    assert command[0] == str(executable.resolve())
    assert command[1:4] == ["-C", str(worktree.resolve()), "--prompt"]


def test_copilot_smoke_rejects_non_worktree(bridge_config):
    adapter = CopilotAdapter(bridge_config)
    with pytest.raises(PathInvalid):
        adapter.run_prompt(
            worktree=bridge_config.worktree_root / "DOES-NOT-EXIST",
            prompt="smoke",
        )


def test_copilot_e2e_adds_bounded_programmatic_permissions(
    monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "COPILOT-E2E"
    worktree.mkdir(parents=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    executable = tmp_path / "copilot.exe"
    executable.write_text("", encoding="utf-8")

    tool_paths = dict(bridge_config.tool_paths or {})
    tool_paths["copilot"] = executable
    config = type(bridge_config)(
        bridge_root=bridge_config.bridge_root,
        tool_paths=tool_paths,
    )
    observed: dict[str, object] = {}

    def fake_run(command, **kwargs):
        observed["command"] = command
        return SimpleNamespace(returncode=0, stdout="OK\n", stderr="")

    monkeypatch.setattr("fox2_agent_bridge.copilot_adapter.subprocess.run", fake_run)

    CopilotAdapter(config).run_prompt(
        worktree=worktree,
        prompt="E2E",
        allow_write=True,
        allow_git=True,
        allow_github_url=True,
        silent=True,
        no_ask_user=True,
    )

    command = observed["command"]
    assert "-s" in command
    assert "--no-ask-user" in command
    assert "--allow-tool=read,write,shell(git:*)" in command
    assert "--allow-url=github.com" in command
