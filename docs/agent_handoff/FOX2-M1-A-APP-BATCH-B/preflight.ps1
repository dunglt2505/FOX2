param(
    [Parameter(Mandatory=$true)][string]$SourceHead,
    [string]$EngineRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../..")).Path,
    [string]$Worktree = "C:\Projects\FOX2-worktrees\FOX2-M1-A-APP-BATCH-B",
    [ValidateSet("CODEX","COPILOT")][string]$PinnedAgent,
    [switch]$CleanupStaleReceipt
)
$ErrorActionPreference = "Stop"
$arguments = @((Join-Path $EngineRoot "agent_bridge/scripts/preexec.py"), "--profile", "app",
    "--worktree", $Worktree, "--source-head", $SourceHead, "--publish")
if ($PinnedAgent) { $arguments += @("--pinned-agent", $PinnedAgent) }
if ($CleanupStaleReceipt) { $arguments += "--cleanup-stale-receipt" }
& python @arguments
exit $LASTEXITCODE
