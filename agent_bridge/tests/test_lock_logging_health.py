from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from fox2_agent_bridge.app import BridgeApp
from fox2_agent_bridge.errors import LockHeld
from fox2_agent_bridge.logging_config import configure_logging, log_event
from fox2_agent_bridge.process_lock import ProcessLock


def test_second_process_lock_is_rejected(tmp_path: Path) -> None:
    lock_path = tmp_path / "bridge.lock"
    first = ProcessLock(lock_path)
    second = ProcessLock(lock_path)
    first.acquire()
    try:
        with pytest.raises(LockHeld):
            second.acquire()
    finally:
        first.release()


def test_lock_is_rejected_from_a_second_process(tmp_path: Path) -> None:
    lock_path = tmp_path / "bridge.lock"
    source = """
import sys
from pathlib import Path

from fox2_agent_bridge.errors import LockHeld
from fox2_agent_bridge.process_lock import ProcessLock

lock = ProcessLock(Path(sys.argv[1]))
try:
    lock.acquire()
except LockHeld:
    print("HELD")
else:
    lock.release()
    raise SystemExit(1)
"""
    owner = ProcessLock(lock_path)
    owner.acquire()
    try:
        result = subprocess.run(
            [sys.executable, "-c", source, str(lock_path)],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    finally:
        owner.release()

    assert result.returncode == 0
    assert result.stdout.strip() == "HELD"


def test_stale_lock_metadata_is_recovered(tmp_path: Path) -> None:
    lock_path = tmp_path / "bridge.lock"
    lock_path.write_text('{"pid": 99999999, "acquired_at": "old"}', encoding="utf-8")

    lock = ProcessLock(lock_path)
    lock.acquire()
    try:
        assert lock.stale_owner_detected
        assert lock.owner is not None
        assert lock.owner["pid"] == os.getpid()
    finally:
        lock.release()


def test_normal_shutdown_releases_lock_and_clears_metadata(tmp_path: Path) -> None:
    lock_path = tmp_path / "bridge.lock"
    with ProcessLock(lock_path):
        assert lock_path.stat().st_size > 0

    assert lock_path.read_bytes() == b""
    with ProcessLock(lock_path):
        assert True


def test_structured_logging_redacts_secret_keys_but_not_sha(tmp_path: Path) -> None:
    logger = configure_logging(tmp_path)
    synthetic_oauth_token = "gho_" + ("A" * 30)
    synthetic_private_key = (
        "-----BEGIN "
        + "PRIVATE KEY"
        + "-----fixture-----END "
        + "PRIVATE KEY"
        + "-----"
    )
    log_event(
        logger,
        component="test",
        event="probe",
        context={
            "access_token": "must-not-appear",
            "api_key": "also-secret",
            "details": f"OAuth value {synthetic_oauth_token}",
            "key_material": synthetic_private_key,
            "sha256": "a" * 64,
        },
    )
    for handler in logger.handlers:
        handler.flush()
    line = (tmp_path / "bridge.log").read_text(encoding="utf-8")
    record = json.loads(line)

    assert "must-not-appear" not in line
    assert "also-secret" not in line
    assert synthetic_oauth_token not in line
    assert "fixture" not in line
    assert record["context"]["access_token"] == "<REDACTED>"
    assert record["context"]["api_key"] == "<REDACTED>"
    assert "<REDACTED>" in record["context"]["details"]
    assert record["context"]["key_material"] == "<REDACTED>"
    assert record["context"]["sha256"] == "a" * 64


def test_health_command_runs_without_agent_execution(
    bridge_config, monkeypatch, capsys
) -> None:
    calls: list[list[str]] = []
    original_run = subprocess.run

    def record_run(args, *positional, **kwargs):
        calls.append([str(part) for part in args])
        return original_run(args, *positional, **kwargs)

    monkeypatch.setattr("fox2_agent_bridge.runtime_tools.subprocess.run", record_run)
    app = BridgeApp(bridge_config)
    with app:
        report = app.health_report()
    output = json.dumps(report)
    capsys.readouterr()

    assert report["project_id"] == "FOX2"
    assert report["repository"] == "dunglt2505/FOX2"
    assert report["database"]["schema_version"] == 3
    assert report["status"] == "READY"
    assert "AGENT_READY" not in output
    assert "DISPATCH_READY" not in output
    assert not any(
        "--prompt" in call or ("exec" in call and "--help" not in call)
        for call in calls
    )
    assert all("--version" in call or "--help" in call or "status" in call for call in calls)


def test_health_cli_entrypoint_emits_json(bridge_config, monkeypatch, capsys) -> None:
    from fox2_agent_bridge.__main__ import main

    monkeypatch.setattr(
        BridgeApp,
        "from_file",
        classmethod(lambda cls, config_path=None: BridgeApp(bridge_config)),
    )

    exit_code = main(["health"])
    captured = capsys.readouterr()
    report = json.loads(captured.out)

    assert exit_code == 0
    assert report["status"] == "READY"
    assert "scope" in report


def test_health_does_not_mutate_fox2_source(bridge_config) -> None:
    repo = Path(r"C:\Projects\FOX2")
    before = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    head_before = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    attributes = repo / ".gitattributes"
    attributes_before = attributes.read_bytes()
    with BridgeApp(bridge_config) as app:
        app.health_report()

    after = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    head_after = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    assert after == before
    assert head_after == head_before
    assert attributes.read_bytes() == attributes_before


def test_graceful_app_shutdown_releases_lock(bridge_config) -> None:
    app = BridgeApp(bridge_config)
    app.start()
    lock_path = bridge_config.bridge_root / "data" / "bridge.lock"
    assert lock_path.stat().st_size > 0

    app.shutdown()

    assert lock_path.read_bytes() == b""
    with ProcessLock(lock_path):
        assert True
