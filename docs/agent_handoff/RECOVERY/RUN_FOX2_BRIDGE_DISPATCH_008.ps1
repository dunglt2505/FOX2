$ErrorActionPreference = "Stop"

$Repo          = "C:\Projects\FOX2"
$WT            = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$TaskBranch    = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$ControlBranch = "work/FOX2-DISPATCH-chat"

$ExpectedHead  = "0c739db91553ab8dd39a30b221f079b9538b0836"
$ControlCommit = "737e9851b2367f5e2aeb6597d0445b6df0ffcc71"
$DispatchId    = "FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-008"
$DispatchPath  = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-008.json"
$PromptCommit  = "e4b32ace0d03f67d4dba28e05f3dd9b24ccfab7f"
$PromptPath    = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-BATCH-B-UNINSTALL-ROOT-FIX-008.md"
$PromptBlob    = "1357c4574da175f444408eb29eaf6d33eb364a6f"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    & git -C $WT @Args
    if ($LASTEXITCODE -ne 0) {
        throw "STOP: git failed: $($Args -join ' ')"
    }
}

Write-Host "FOX2 Bridge Dispatch 008 launcher" -ForegroundColor Cyan

$TaskRefspec = "+refs/heads/" + $TaskBranch + ":refs/remotes/origin/" + $TaskBranch
$ControlRefspec = "+refs/heads/" + $ControlBranch + ":refs/remotes/origin/" + $ControlBranch

Invoke-Git fetch origin $TaskRefspec
Invoke-Git fetch origin $ControlRefspec

& git -C $WT cat-file -e ($ControlCommit + "^{commit}")
if ($LASTEXITCODE -ne 0) { throw "STOP: pinned control commit unavailable after fetch" }

& git -C $WT cat-file -e ($PromptCommit + "^{commit}")
if ($LASTEXITCODE -ne 0) { throw "STOP: pinned prompt commit unavailable after fetch" }

$Status = @(& git -C $WT status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot read worktree status" }
if ($Status.Count -gt 0) { throw "STOP: Bridge worktree is dirty" }

$RemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot resolve remote task head" }
if ($RemoteHead -ne $ExpectedHead) { throw "STOP: remote task head changed: $RemoteHead" }

$LocalBranch = (& git -C $WT branch --show-current).Trim()
if ($LocalBranch -ne $TaskBranch) { throw "STOP: wrong task branch: $LocalBranch" }

$LocalHead = (& git -C $WT rev-parse HEAD).Trim()
if ($LocalHead -ne $ExpectedHead) {
    Invoke-Git merge --ff-only ("refs/remotes/origin/" + $TaskBranch)
    $LocalHead = (& git -C $WT rev-parse HEAD).Trim()
}
if ($LocalHead -ne $ExpectedHead) { throw "STOP: local HEAD mismatch after fast-forward: $LocalHead" }

$DispatchSpec = $ControlCommit + ":" + $DispatchPath
$DispatchRaw = (& git -C $WT show $DispatchSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($DispatchRaw)) {
    throw "STOP: cannot read exact Dispatch 008"
}
try { $Dispatch = $DispatchRaw | ConvertFrom-Json }
catch { throw "STOP: Dispatch 008 JSON parse failed" }

if ($Dispatch.dispatch_id -ne $DispatchId) { throw "STOP: dispatch identity mismatch" }
if ($Dispatch.source.commit_sha -ne $ExpectedHead) { throw "STOP: dispatch source mismatch" }
if ($Dispatch.runtime_contract.base_sha -ne $ExpectedHead) { throw "STOP: runtime base mismatch" }
if ($Dispatch.routing.model -ne "gpt-6.1-sol") { throw "STOP: model mismatch" }
if ($Dispatch.routing.reasoning_effort -ne "high") { throw "STOP: reasoning mismatch" }
if ($Dispatch.routing.permission_profile -ne "FULL_ACCESS") { throw "STOP: permission mismatch" }
if ([int]$Dispatch.max_runs -ne 1) { throw "STOP: max_runs mismatch" }

$PromptSpec = $PromptCommit + ":" + $PromptPath
$Prompt = (& git -C $WT show $PromptSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Prompt)) {
    throw "STOP: cannot read bound prompt"
}
$ActualPromptBlob = (& git -C $WT rev-parse $PromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualPromptBlob -ne $PromptBlob) {
    throw "STOP: prompt blob mismatch"
}

$Claim = Join-Path $WT "reports\BRIDGE-DESKTOP-BATCH-B\evidence\core008\claim.json"
if (Test-Path -LiteralPath $Claim) {
    throw "STOP: Dispatch 008 already has a local claim; never replay"
}

$AgentInput = @"
Execute exactly FOX2 Dispatch:
$DispatchId

Before any mutation, independently read and validate:
git show $($ControlCommit):$DispatchPath

Dispatches 001-007 are consumed and MUST NOT be replayed.
Preserve the successful 007 installer environment fix.
Do not touch the real per-user Bridge until the complete disposable lifecycle including uninstall/reinstall has passed.
Follow the exact bound prompt below.

$Prompt
"@

Write-Host "PRELAUNCH PASS: exact Dispatch/prompt/source bindings verified." -ForegroundColor Green
Write-Host "Launching single-use Codex route..." -ForegroundColor Cyan

$CodexArgs = @(
    "exec",
    "-C", $WT,
    "--ephemeral",
    "--sandbox", "danger-full-access",
    "-c", 'approval_policy="never"',
    "--json",
    "--model", "gpt-6.1-sol",
    "-c", 'model_reasoning_effort="high"',
    "-"
)

$AgentInput | & codex @CodexArgs
$CodexExit = $LASTEXITCODE

Write-Host ""
Write-Host "CODEX CLI EXIT = $CodexExit"

$ClaimExists = Test-Path -LiteralPath $Claim

& git -C $WT fetch origin $TaskRefspec | Out-Null
$RemoteAfter = if ($LASTEXITCODE -eq 0) {
    (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
} else {
    "FETCH_FAILED"
}

if (-not $ClaimExists -and $RemoteAfter -eq $ExpectedHead) {
    Write-Host "RESULT: 008 NOT CONSUMED / NO REMOTE RESULT OBSERVED." -ForegroundColor Yellow
    Write-Host "Do not infer success from CODEX CLI EXIT. Return this output to CHAT."
    exit 20
}

Write-Host "RESULT: execution produced local and/or remote state that requires CHAT intake." -ForegroundColor Cyan
Write-Host "Local claim exists: $ClaimExists"
Write-Host "Remote task head: $RemoteAfter"
Write-Host "Do NOT rerun Dispatch 008. Ask CHAT to check status."
exit 0
