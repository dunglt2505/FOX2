param(
    [int]$TimeoutSeconds = 120
)

$ErrorActionPreference = "Stop"

$RepoWorktree = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Python = "D:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe"
$BridgeSrc = Join-Path $RepoWorktree "agent_bridge\src"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Bridge runtime Python not found: $Python"
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoWorktree ".git"))) {
    throw "Target is not a Git worktree: $RepoWorktree"
}

$env:PYTHONPATH = $BridgeSrc

Write-Host "FOX2 Bridge -> Copilot CLI smoke"
Write-Host "Worktree: $RepoWorktree"
Write-Host "Python:   $Python"

& $Python -m fox2_agent_bridge copilot-smoke `
    --worktree $RepoWorktree `
    --timeout $TimeoutSeconds

exit $LASTEXITCODE
