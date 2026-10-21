"""StrictMode regression on synthetic tasks; never inspect the real host."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "f1_host_discovery_readonly.ps1"
PWSH = shutil.which("pwsh")
pytestmark = pytest.mark.skipif(
    os.name != "nt" or PWSH is None, reason="Windows PowerShell 7 required"
)

HARNESS = r"""
param([string]$DiscoveryScript, [string]$FixturePath)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$global:FOX2TestFixture = Get-Content -LiteralPath $FixturePath -Raw | ConvertFrom-Json
# Every host-facing command used by discovery is replaced before execution.
function Test-Path { return $false }
function Get-CimInstance { return @() }
function Get-ItemProperty { throw 'synthetic registry unavailable' }
function Get-ChildItem { throw 'unexpected startup enumeration' }
function Get-Command { return $null }
function Get-ScheduledTask {
    if ($global:FOX2TestFixture.raise_error) { throw 'synthetic task access denied' }
    return $global:FOX2TestFixture.tasks
}
& $DiscoveryScript
"""

CASES = [
    pytest.param([{}, {"ClassId": "opaque"}], False, id="non-exec-actions"),
    pytest.param([None, {}], False, id="null-and-empty-actions"),
    pytest.param([{"Arguments": "--unrelated"}], False, id="missing-execute"),
    pytest.param([{"Execute": "unrelated.exe"}], False, id="missing-arguments"),
    pytest.param([{"Execute": "C:/FOX2/bridge.exe"}], True, id="execute-only-match"),
    pytest.param([{"Arguments": "C:/agent_bridge/worker.py"}], True, id="arguments-only-match"),
    pytest.param([{"Execute": None, "Arguments": None}], False, id="null-values"),
    pytest.param([None, {}, {"ClassId": "opaque"},
                  {"Execute": "C:/FOX2/bridge.exe", "Arguments": "--private-secret"}],
                 True, id="mixed-actions"),
    pytest.param([], False, id="empty-actions"),
]


def run_discovery(tmp_path: Path, tasks: list[dict], *, raise_error: bool = False) -> tuple[dict, str]:
    fixture = tmp_path / "tasks.json"
    fixture.write_text(json.dumps({"tasks": tasks, "raise_error": raise_error}), encoding="utf-8")
    harness = tmp_path / "discovery_harness.ps1"
    harness.write_text(HARNESS, encoding="utf-8")
    result = subprocess.run(
        [PWSH, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(harness),
         "-DiscoveryScript", str(SCRIPT), "-FixturePath", str(fixture)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr, result.stderr
    output = json.loads(result.stdout)
    assert output["schema"] == "FOX2_F1_HOST_DISCOVERY_READ_ONLY_V1"
    assert output["positive_claim_authority"] == "DENY"
    assert output["canary"] == "HOLD"
    for key in ("all_legacy_entrypoints_enumerated",
                "durable_legacy_retirement_verified", "privileged_broker_verified"):
        assert output[key] is False
    assert "--private-secret" not in result.stdout
    assert "Arguments" not in result.stdout and "Execute" not in result.stdout
    return output, result.stdout


@pytest.mark.parametrize("actions,expected_match", CASES)
def test_optional_action_properties_do_not_erase_task_inventory(
    tmp_path: Path, actions: list, expected_match: bool,
) -> None:
    # Always follow the malformed action with a valid matching task. The old
    # outer Probe swallowed StrictMode errors and lost the complete inventory.
    tasks = [
        {"TaskName": "unrelated-first", "State": "Ready", "Actions": actions},
        {"TaskName": "unrelated-later", "State": "Disabled",
         "Actions": [{"Execute": "C:/FOX2/later.exe", "Arguments": "--private-secret"}]},
        {"TaskName": "FOX2-name-match", "State": "Ready", "Actions": [None, {}]},
        {"TaskName": "unrelated-last", "State": "Ready",
         "Actions": [{"Execute": "other.exe", "Arguments": "--other"}]},
    ]
    output, _ = run_discovery(tmp_path, tasks)
    names = [task["name"] for task in output["task_candidates"]]
    expected = (["unrelated-first"] if expected_match else []) + [
        "unrelated-later", "FOX2-name-match"]
    assert names == expected
    assert output["task_candidates"][-2:] == [
        {"name": "unrelated-later", "state": "Disabled"},
        {"name": "FOX2-name-match", "state": "Ready"},
    ]


def test_task_access_failure_cannot_grant_authority(tmp_path: Path) -> None:
    output, _ = run_discovery(tmp_path, [], raise_error=True)
    assert not any(output["task_candidates"])


def test_discovery_ast_contains_only_read_only_commands(tmp_path: Path) -> None:
    # Parse, never execute, the production script. Reject new dynamic commands
    # or unreviewed host-writing cmdlets even when a mock could hide them.
    parser = r"""
param([string]$Source)
$tokens = $null
$errors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile(
    $Source, [ref]$tokens, [ref]$errors)
if (@($errors).Count) { throw 'parse error' }
@($ast.FindAll({
    param($node)
    $node -is [System.Management.Automation.Language.CommandAst]
}, $true) | ForEach-Object {
    $name = $_.GetCommandName()
    if ($name) { $name } else { 'DYNAMIC' }
} | Sort-Object -Unique) | ConvertTo-Json
"""
    harness = tmp_path / "parse_discovery.ps1"
    harness.write_text(parser, encoding="utf-8")
    result = subprocess.run(
        [PWSH, "-NoLogo", "-NoProfile", "-NonInteractive", "-File",
         str(harness), "-Source", str(SCRIPT)],
        capture_output=True, text=True, timeout=30, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr, result.stderr
    assert set(json.loads(result.stdout)) <= {
        "Set-StrictMode", "Probe", "DYNAMIC", "git", "Test-Path", "Join-Path",
        "Get-CimInstance", "Where-Object", "ForEach-Object", "Get-ScheduledTask",
        "Get-ItemProperty", "Get-ChildItem", "Select-Object", "Get-Command",
        "Get-AppLockerPolicy", "ConvertTo-Json",
    }
    # Probe has the script's sole dynamic invocation: its supplied read action.
    source = SCRIPT.read_text(encoding="utf-8")
    assert source.count("& $Action") == 1
    assert source.count("& ") == 4  # Probe plus three literal git read commands.
