from __future__ import annotations

from pathlib import Path

import pytest

from fox2_agent_bridge.codex_adapter import CodexAdapter


class CaptureStdin:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.closed = False

    def write(self, value: str) -> int:
        self.parts.append(value)
        return len(value)

    def close(self) -> None:
        self.closed = True

    @property
    def value(self) -> str:
        return "".join(self.parts)


class FakeStream:
    def __init__(self, text: str) -> None:
        self._lines = iter(text.splitlines(keepends=True))

    def readline(self) -> str:
        return next(self._lines, "")


class FakeProcess:
    def __init__(self, *, stdout: str, stderr: str, returncode: int = 0) -> None:
        self.stdin = CaptureStdin()
        self.stdout = FakeStream(stdout)
        self.stderr = FakeStream(stderr)
        self.returncode = returncode
        self.pid = 4242

    def poll(self):
        return self.returncode

    def wait(self, timeout=None):
        return self.returncode

    def kill(self):
        self.returncode = -9


def _configured_adapter(bridge_config, tmp_path: Path):
    executable = tmp_path / "codex.exe"
    executable.write_text("", encoding="utf-8")
    tool_paths = dict(bridge_config.tool_paths or {})
    tool_paths["codex"] = executable
    config = type(bridge_config)(
        bridge_root=bridge_config.bridge_root,
        tool_paths=tool_paths,
    )
    return CodexAdapter(config), executable


def test_codex_exec_uses_workspace_write_and_never_approval(
    monkeypatch: pytest.MonkeyPatch, bridge_config, tmp_path: Path
):
    worktree = bridge_config.worktree_root / "CODEX-E2E"
    worktree.mkdir(parents=True, exist_ok=True)
    (worktree / ".git").write_text("gitdir: test", encoding="utf-8")

    adapter, executable = _configured_adapter(bridge_config, tmp_path)
    observed: dict[str, object] = {}

    def fake_popen(command, **kwargs):
        process = FakeProcess(stdout="CODEX_OK\n", stderr="")
        observed["command"] = command
        observed["cwd"] = kwargs["cwd"]
        observed["env"] = kwargs["env"]
        observed["process"] = process
        return process

    monkeypatch.setattr(
        "fox2_agent_bridge.codex_adapter.subprocess.Popen",
        fake_popen,
    )

    result = adapter.run_prompt(
        worktree=worktree,
        prompt="Return CODEX_OK.",
        timeout_seconds=30,
    )

    assert result.status == "CODEX_EXITED"
    assert result.exit_code == 0
    assert result.stdout.strip() == "CODEX_OK"
    assert observed["cwd"] == worktree.resolve()
    command = observed["command"]
    assert command == [
        str(executable.resolve()),
        "-c",
        'windows.sandbox="unelevated"',
        "--ask-for-approval",
        "never",
        "exec",
        "--sandbox",
        "workspace-write",
        "-",
    ]
    process = observed["process"]
    assert process.stdin.value == "Return CODEX_OK.\n"
    assert process.stdin.closed is True
    env = observed["env"]
    assert str(Path(__import__("sys").executable).resolve().parent) == env["PATH"].split(
        __import__("os").pathsep, 1
    )[0]
