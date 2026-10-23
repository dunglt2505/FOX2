param(
    [int]$TimeoutSeconds = 180
)

$ErrorActionPreference = "Stop"

$RepoWorktree = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Python = "D:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe"
$BridgeSrc = Join-Path $RepoWorktree "agent_bridge\src"
$DispatchPath = "docs/agent_handoff/FOX2-BRIDGE-E2E-CANARY-003/dispatch/FOX2-BRIDGE-E2E-CANARY-003.json"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Bridge runtime Python not found: $Python"
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoWorktree ".git"))) {
    throw "Bridge source worktree is not a Git worktree: $RepoWorktree"
}

$env:PYTHONPATH = $BridgeSrc

Write-Host "FOX2 Bridge E2E canary 003"
Write-Host "Bridge source: $RepoWorktree"
Write-Host "Dispatch:      $DispatchPath"

& $Python -m fox2_agent_bridge e2e-once `
    --dispatch-path $DispatchPath `
    --timeout $TimeoutSeconds

exit $LASTEXITCODE
