param(
    [ValidateSet("run-next", "status", "health", "poll-once")]
    [string]$Command = "status",
    [string]$DispatchId,
    [int]$Limit = 20,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = "Stop"

$SourceWorktree = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Python = "C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe"
$BridgeSrc = Join-Path $SourceWorktree "agent_bridge\src"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Bridge runtime Python not found: $Python"
}
if (-not (Test-Path -LiteralPath (Join-Path $SourceWorktree ".git"))) {
    throw "Bridge source worktree is not a Git worktree: $SourceWorktree"
}

$env:PYTHONPATH = $BridgeSrc

Write-Host "FOX2 Bridge Operational MVP"
Write-Host "Source:  $SourceWorktree"
Write-Host "Command: $Command"

$CliArgs = @("-u", "-m", "fox2_agent_bridge", $Command)

switch ($Command) {
    "run-next" {
        $CliArgs += @("--timeout", "$TimeoutSeconds")
    }
    "status" {
        $CliArgs += @("--limit", "$Limit")
        if ($DispatchId) {
            $CliArgs += @("--dispatch-id", $DispatchId)
        }
    }
}

& $Python @CliArgs
exit $LASTEXITCODE
