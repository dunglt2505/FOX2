#!/usr/bin/env python3
"""FOX2 Bridge C1 current-host inspection. Strictly read-only; no worker/CLI starts.

Invoke on FOXLE-PC with a trusted Python 3 interpreter:
  python -I C1_readonly_host_snapshot_20261019.py

Output: sanitized JSON to stdout ONLY. Never invokes Bridge control commands,
opens an agent, changes worker/startup, fetches/pushes Git, or writes a receipt.
Source: FOX2 Bridge RC1 Whole-WP and 2026-10-19 Owner Bridge-P0 instruction.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys

HISTORICAL_PACKAGE_SHA256 = "a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac"
EXPECTED_BRIDGE_BRANCH_HEAD = "f3d6468fedb553ba6c6192ba5811cb1b26a11ab9"
BRIDGE_BRANCH = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
ROOT = Path(os.environ.get("LOCALAPPDATA") or (Path.home() / "AppData" / "Local")) / "FOX2" / "AgentBridge"
LEGACY = Path("C:/Projects/FOX2-AgentBridge")
SOURCE_WORKTREE = Path("C:/Projects/FOX2-worktrees/FOX2-BRIDGE-DESKTOP-BATCH-B")
ALLOWED_CONTROL_FIELDS = (
    "state", "paused", "stop_requested", "setup_complete", "start_with_windows",
    "current_dispatch", "current_execution",
)
NONTERMINAL = {"CLAIMED", "RUNNING", "EXECUTING", "PUBLISHING", "NEEDS_RECONCILIATION", "STARTING"}


def fail(label: str) -> dict:
    return {"status": "UNKNOWN", "reason": label}


def installed() -> dict:
    pointer = ROOT / "current.json"
    if not pointer.is_file():
        return {"status": "ABSENT", "pointer_exists": False}
    try:
        value = json.loads(pointer.read_text(encoding="utf-8"))
        identity = value.get("package_sha256")
        if not isinstance(identity, str) or not re.fullmatch(r"[0-9a-f]{64}", identity):
            return fail("INVALID_INSTALLED_POINTER")
        version = ROOT / "versions" / identity
        return {
            "status": "OBSERVED", "pointer_exists": True,
            "package_sha256": identity,
            "historical_package_match": identity == HISTORICAL_PACKAGE_SHA256,
            "installed_interpreter_exists": (version / "runtime" / "Scripts" / "python.exe").is_file(),
            "installed_desktop_exists": (version / "payload" / "desktop" / "FOX2.Bridge.Desktop.exe").is_file(),
            "installed_paths_are_symlinks": ROOT.is_symlink() or version.is_symlink(),
        }
    except (OSError, ValueError, TypeError, UnicodeError):
        return fail("INSTALLED_POINTER_READ_FAILED")


def read_ledger(db: Path) -> dict:
    if not db.is_file():
        return {"status": "ABSENT"}
    try:
        # mode=ro and query_only; do not import or call Bridge runtime initialization.
        with sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=1) as conn:
            conn.execute("PRAGMA query_only=ON")
            existing = {row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name IN "
                "('worker_state','dispatches','executions')"
            )}
            result = {"status": "OBSERVED", "tables_present": sorted(existing)}
            if "worker_state" in existing:
                row = conn.execute("SELECT payload FROM worker_state WHERE id=1").fetchone()
                if row:
                    state = json.loads(row[0])
                    result["worker_control"] = {k: state.get(k) for k in ALLOWED_CONTROL_FIELDS}
                else:
                    result["worker_control"] = {"status": "MISSING_ROW"}
            for table in ("dispatches", "executions"):
                if table in existing:
                    counts = conn.execute("SELECT state, COUNT(*) FROM " + table + " GROUP BY state").fetchall()
                    result[table + "_counts"] = {
                        str(s)[:55]: n for s, n in counts if isinstance(s, str)
                    }
                    if table == "executions":
                        result["nonterminal_count"] = sum(
                            n for s, n in counts if isinstance(s, str) and s.upper() in NONTERMINAL
                        )
            return result
    except (sqlite3.Error, OSError, ValueError, TypeError, json.JSONDecodeError):
        return fail("LEDGER_READ_ONLY_OPEN_OR_PARSE_FAILED")


def windows_observation(script: str, reason: str) -> dict:
    shell = shutil.which("pwsh") or shutil.which("powershell.exe") or shutil.which("powershell")
    if not shell:
        return fail("POWERSHELL_NOT_FOUND")
    try:
        response = subprocess.run(
            [shell, "-NoProfile", "-NonInteractive", "-Command", script],
            capture_output=True, text=True, timeout=25, check=False,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if response.returncode:
            return fail(reason)
        value = json.loads(response.stdout.strip())
        return {"status": "OBSERVED", "items": value}
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return fail(reason)


PROCESS_QUERY = r"""
$ErrorActionPreference = 'Stop'
$found = @(
  Get-CimInstance Win32_Process | Where-Object {
    ($_.Name -match '^(python|pythonw|FOX2\.Bridge\.Desktop)\.exe$') -and
    ($_.Name -eq 'FOX2.Bridge.Desktop.exe' -or
     ($_.CommandLine -and $_.CommandLine -match 'fox2_agent_bridge|AgentBridge'))
  } | ForEach-Object {
    $cmd = [string]$_.CommandLine
    $role = if ($_.Name -eq 'FOX2.Bridge.Desktop.exe') { 'DESKTOP' }
            elseif ($cmd -match 'fox2_agent_bridge.*worker') { 'WORKER' }
            else { 'BRIDGE_PYTHON_OTHER' }
    [pscustomobject]@{
      pid = [int]$_.ProcessId
      parent_pid = [int]$_.ParentProcessId
      role = $role
    }
  }
)
ConvertTo-Json -InputObject @($found) -Depth 4 -Compress
"""

STARTUP_QUERY = r"""
$ErrorActionPreference = 'Stop'
$found = @(
  Get-ScheduledTask | Where-Object {
    $_.TaskName -match 'FOX2|Bridge' -or
    ($_.Actions | Where-Object { ($_.Execute + ' ' + $_.Arguments) -match 'FOX2|AgentBridge' })
  } | ForEach-Object {
    [pscustomobject]@{state = [string]$_.State; enabled = [bool]$_.Settings.Enabled}
  }
)
ConvertTo-Json -InputObject @($found) -Depth 4 -Compress
"""


def git_source() -> dict:
    if not SOURCE_WORKTREE.is_dir():
        return {"status": "NOT_FOUND_AT_EXPECTED_PATH"}
    git = shutil.which("git")
    if not git:
        return fail("GIT_NOT_FOUND")
    try:
        def query(*args):
            p = subprocess.run(
                [git, "--no-optional-locks", "-C", str(SOURCE_WORKTREE), *args],
                capture_output=True, text=True, timeout=10, check=False,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            if p.returncode:
                raise ValueError("GIT_QUERY_FAILED")
            return p.stdout.strip()
        head = query("rev-parse", "HEAD")
        branch = query("branch", "--show-current")
        changes = query("status", "--porcelain=v1", "--untracked-files=all")
        return {
            "status": "OBSERVED", "head": head,
            "source_baseline_match": head == EXPECTED_BRIDGE_BRANCH_HEAD,
            "branch_matches": branch == BRIDGE_BRANCH,
            "dirty_entry_count": len(changes.splitlines()) if changes else 0,
        }
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return fail("SOURCE_GIT_READ_FAILED")


def manual_marker() -> dict:
    marker = ROOT / "data" / "manual_consumption.json"
    if not marker.is_file():
        return {"status": "ABSENT"}
    try:
        item = json.loads(marker.read_text(encoding="utf-8"))
        return {
            "status": "OBSERVED",
            "format_valid": item.get("format") == "FOX2_MANUAL_CONSUMPTION_1",
            "record_exists": True,
        }
    except (OSError, ValueError, TypeError):
        return fail("MANUAL_MARKER_READ_FAILED")


def main() -> int:
    now = datetime.now(timezone.utc).isoformat()
    if os.name != "nt":
        print(json.dumps({
            "format": "FOX2_BRIDGE_C1_READ_ONLY_HOST_OBSERVATION_V1",
            "observed_utc": now, "status": "NOT_WINDOWS_HOST",
            "no_bridge_command_executed": True,
        }, indent=2))
        return 2
    result = {
        "format": "FOX2_BRIDGE_C1_READ_ONLY_HOST_OBSERVATION_V1",
        "observed_utc": now,
        "stage": "READ_ONLY_HOST_INVENTORY",
        "no_bridge_command_executed": True,
        "no_dispatch_claim_or_worker_control": True,
        "installed": installed(),
        "current_ledger": read_ledger(ROOT / "data" / "bridge.db"),
        "legacy_ledger": read_ledger(LEGACY / "data" / "bridge.db"),
        "manual_marker": manual_marker(),
        "processes": windows_observation(PROCESS_QUERY, "PROCESS_INVENTORY_FAILED"),
        "startup_tasks": windows_observation(STARTUP_QUERY, "STARTUP_INVENTORY_FAILED"),
        "source_worktree": git_source(),
        "git_control_ref": "CHECKED_SEPARATELY_BY_CHAT_REMOTE",
        "review_verdict": "C1_HOST_SNAPSHOT_PENDING_CHAT_INTAKE",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if all(
        result[k].get("status") == "OBSERVED"
        for k in ("installed", "current_ledger", "processes", "startup_tasks")
    ) else 20


if __name__ == "__main__":
    sys.exit(main())
