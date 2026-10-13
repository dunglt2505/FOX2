from __future__ import annotations

from io import StringIO
from pathlib import Path

import pytest

from fox2_agent_bridge.copilot_adapter import CopilotAdapter
from fox2_agent_bridge.errors import PathInvalid, ToolExecFailed


class FakeProcess:
    def __init__(self, *, stdout: str, stderr: str, returncode: int = 0) -> None:
        self.stdout = StringIO(stdout)
        self.stderr = StringIO(stderr)
        self.returncode = returncode
        self.pid = 4242

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode

    def kill(self):
        self.returncode = -9


def _configured_adapter(bridge_config, tmp_path: Path):
    executable = tmp_path / "copilot.exe"
    executable.write_text("", encoding="utf-8")
    tool_paths = dict(bridge_config.tool_paths or {})
    tool_paths["copilot"] = executable
    config = type(bridge_config)(
        bridge_root=bridge_config.bridge_root,
        tool_paths=tool_paths,
    )
    return CopilotAdapter(config), executable


def test_copilot_smoke_builds_cli_command(
    monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "COPILOT-SMOKE"
    worktree.mkdir(parents=True, exist_ok=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    adapter, executable = _configured_adapter(bridge_config, tmp_path)
    observed: dict[str, object] = {}

    def fake_popen(command, **kwargs):
        observed["command"] = command
        observed["cwd"] = kwargs["cwd"]
        return FakeProcess(stdout="FOX2_BRIDGE_COPILOT_SMOKE_OK\n", stderr="")

    monkeypatch.setattr(
        "fox2_agent_bridge.copilot_adapter.subprocess.Popen",
        fake_popen,
    )

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


def test_copilot_e2e_adds_documented_programmatic_permissions(
    monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "COPILOT-E2E"
    worktree.mkdir(parents=True, exist_ok=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    adapter, _executable = _configured_adapter(bridge_config, tmp_path)
    observed: dict[str, object] = {}

    def fake_popen(command, **kwargs):
        observed["command"] = command
        return FakeProcess(stdout="OK\n", stderr="")

    monkeypatch.setattr(
        "fox2_agent_bridge.copilot_adapter.subprocess.Popen",
        fake_popen,
    )

    adapter.run_prompt(
        worktree=worktree,
        prompt="E2E",
        allow_write=True,
        allow_git=True,
        allow_github_url=False,
        silent=True,
        no_ask_user=True,
    )

    command = observed["command"]
    assert "-s" in command
    assert "--no-ask-user" in command
    assert "--allow-tool=write" in command
    assert "--allow-tool=shell(git:*)" in command
    assert "--allow-url=github.com" not in command


def test_copilot_e2e_adds_bounded_pytest_permission(
    monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "COPILOT-PYTEST"
    worktree.mkdir(parents=True, exist_ok=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    adapter, _executable = _configured_adapter(bridge_config, tmp_path)
    observed: dict[str, object] = {}

    def fake_popen(command, **kwargs):
        observed["command"] = command
        observed["env"] = kwargs["env"]
        return FakeProcess(stdout="PYTEST_OK\n", stderr="")

    monkeypatch.setattr(
        "fox2_agent_bridge.copilot_adapter.subprocess.Popen",
        fake_popen,
    )

    adapter.run_prompt(
        worktree=worktree,
        prompt="Run python -m pytest --version.",
        allow_write=True,
        allow_git=True,
        allowed_shell_tools=(
            "shell(python -m pytest --version)",
            "shell(python -m pytest -q)",
            "shell(python -m pytest tests/m1_p2_01 -q)",
        ),
        silent=True,
        no_ask_user=True,
    )

    command = observed["command"]
    assert "--allow-tool=shell(python -m pytest --version)" in command
    assert "--allow-tool=shell(python -m pytest -q)" in command
    assert "--allow-tool=shell(python -m pytest tests/m1_p2_01 -q)" in command
    env = observed["env"]
    assert str(Path(__import__("sys").executable).resolve().parent) == env["PATH"].split(
        __import__("os").pathsep, 1
    )[0]


def test_copilot_rejects_shell_permission_outside_safe_catalog(
    bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "COPILOT-UNSAFE"
    worktree.mkdir(parents=True, exist_ok=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    adapter, _executable = _configured_adapter(bridge_config, tmp_path)

    with pytest.raises(ToolExecFailed, match="outside the Bridge safe catalog"):
        adapter.run_prompt(
            worktree=worktree,
            prompt="unsafe",
            allowed_shell_tools=("shell(powershell:*)",),
        )
