$ErrorActionPreference = "Stop"

$Repo          = "C:\Projects\FOX2"
$WT            = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$TaskBranch    = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$ControlBranch = "work/FOX2-DISPATCH-chat"
$CanaryBranch  = "work/FOX2-BRIDGE-FINAL-CANARY-009"

$ExpectedHead  = "501822a33ef08c7365154913bbc677544856eee5"
$ControlCommit = "72290d52585c3c6e09030c1c7a840583e61af637"
$BundleCommit  = "cd2a1bd0d2a4e851a79c17f538f70734277d5ad5"

$DispatchId    = "FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-009"
$DispatchPath  = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-009.json"
$PromptCommit  = "5a527dd71e2217baef42a4a5c29b81e1533a5a5b"
$PromptPath    = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-FINAL-CERTIFICATION-009.md"
$PromptBlob    = "fb0822e6ab27e9721eaaf6bdcbf3566d1904329b"

$V3FixturePath = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json"
$V3FixtureBlob = "964dceb19c74235b9dbf0d219c77046c1b2e9a4e"

$CanaryDispatchPath = "docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json"
$CanaryDispatchBlob = "7bba347537d48d4d7b499841efeafc06ea3e597f"
$CanaryResultPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json"

$ClaimPath = Join-Path $WT "reports\BRIDGE-DESKTOP-BATCH-B\evidence\final009\controller_claim.json"
$FinalPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/final_certification.json"

function Fetch-Ref {
    param([string]$Refspec)
    for ($i = 1; $i -le 3; $i++) {
        & git -C $WT fetch --no-tags origin $Refspec
        if ($LASTEXITCODE -eq 0) { return }
        if ($i -lt 3) { Start-Sleep -Seconds 3 }
    }
    throw "STOP: git fetch failed after 3 attempts: $Refspec"
}

function Require-GitObject {
    param([string]$Spec, [string]$Label)
    & git -C $WT cat-file -e $Spec
    if ($LASTEXITCODE -ne 0) { throw "STOP: missing $Label ($Spec)" }
}

Write-Host "FOX2 Bridge Final Certification 009 launcher" -ForegroundColor Cyan

$TaskRefspec    = "+refs/heads/" + $TaskBranch + ":refs/remotes/origin/" + $TaskBranch
$ControlRefspec = "+refs/heads/" + $ControlBranch + ":refs/remotes/origin/" + $ControlBranch
$CanaryRefspec  = "+refs/heads/" + $CanaryBranch + ":refs/remotes/origin/" + $CanaryBranch

Fetch-Ref $TaskRefspec
Fetch-Ref $ControlRefspec
Fetch-Ref $CanaryRefspec

Require-GitObject ($ControlCommit + "^{commit}") "controller control commit"
Require-GitObject ($BundleCommit + "^{commit}") "canary bundle commit"
Require-GitObject ($PromptCommit + "^{commit}") "controller prompt commit"

$Status = @(& git -C $WT status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot read Bridge worktree status" }
if ($Status.Count -gt 0) { throw "STOP: Bridge worktree is dirty before 009 claim" }

$LocalBranch = (& git -C $WT branch --show-current).Trim()
if ($LocalBranch -ne $TaskBranch) { throw "STOP: wrong Bridge task branch: $LocalBranch" }

$LocalHead = (& git -C $WT rev-parse HEAD).Trim()
$RemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
if ($LocalHead -ne $ExpectedHead -or $RemoteHead -ne $ExpectedHead) {
    throw "STOP: Bridge source head mismatch; local=$LocalHead remote=$RemoteHead"
}

$CanaryRemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()
if ($CanaryRemoteHead -ne $ExpectedHead) {
    throw "STOP: canary branch already advanced or changed: $CanaryRemoteHead"
}

$DispatchSpec = $ControlCommit + ":" + $DispatchPath
$DispatchRaw = (& git -C $WT show $DispatchSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($DispatchRaw)) {
    throw "STOP: cannot read controller Dispatch 009"
}
try { $Dispatch = $DispatchRaw | ConvertFrom-Json }
catch { throw "STOP: controller Dispatch 009 JSON parse failed" }

if ($Dispatch.dispatch_id -ne $DispatchId) { throw "STOP: controller dispatch identity mismatch" }
if ($Dispatch.source.commit_sha -ne $ExpectedHead) { throw "STOP: controller source mismatch" }
if ($Dispatch.runtime_contract.base_sha -ne $ExpectedHead) { throw "STOP: controller runtime base mismatch" }
if ($Dispatch.routing.model -ne "gpt-6.1-sol") { throw "STOP: controller model mismatch" }
if ($Dispatch.routing.reasoning_effort -ne "high") { throw "STOP: controller reasoning mismatch" }
if ($Dispatch.routing.permission_profile -ne "FULL_ACCESS") { throw "STOP: controller permission mismatch" }
if ([int]$Dispatch.max_runs -ne 1) { throw "STOP: controller max_runs mismatch" }
if (@($Dispatch.runtime_contract.allowed_code_paths).Count -ne 0) {
    throw "STOP: controller unexpectedly authorizes product code paths"
}

$PromptSpec = $PromptCommit + ":" + $PromptPath
$Prompt = (& git -C $WT show $PromptSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Prompt)) {
    throw "STOP: cannot read bound controller prompt"
}
$ActualPromptBlob = (& git -C $WT rev-parse $PromptSpec).Trim()
if ($ActualPromptBlob -ne $PromptBlob) { throw "STOP: controller prompt blob mismatch" }

$ActualV3Blob = (& git -C $WT rev-parse ($BundleCommit + ":" + $V3FixturePath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualV3Blob -ne $V3FixtureBlob) {
    throw "STOP: v3 fixture blob mismatch"
}

$ActualCanaryBlob = (& git -C $WT rev-parse ($BundleCommit + ":" + $CanaryDispatchPath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualCanaryBlob -ne $CanaryDispatchBlob) {
    throw "STOP: legacy canary blob mismatch"
}

if (Test-Path -LiteralPath $ClaimPath) {
    throw "STOP: controller 009 already has a local claim; never replay"
}

& git -C $WT show ("refs/remotes/origin/" + $CanaryBranch + ":" + $CanaryResultPath) *> $null
if ($LASTEXITCODE -eq 0) {
    throw "STOP: final009 canary result already exists; never replay"
}

New-Item -ItemType Directory -Force -Path (Split-Path $ClaimPath) | Out-Null
$Claim = [ordered]@{
    dispatch_id = $DispatchId
    control_commit = $ControlCommit
    source_head = $ExpectedHead
    canary_bundle_commit = $BundleCommit
    canary_branch = $CanaryBranch
    canary_base = $ExpectedHead
    consumed = $true
    max_runs = 1
    claimed_at = (Get-Date).ToUniversalTime().ToString("o")
}
$ClaimJson = ($Claim | ConvertTo-Json -Depth 6) + [char]10
[IO.File]::WriteAllText($ClaimPath, $ClaimJson, [Text.UTF8Encoding]::new($false))

$AgentInput = @"
Execute exactly FOX2 controller Dispatch:
$DispatchId

Before real runtime mutation, independently read and validate:
git show $($ControlCommit):$DispatchPath

The launcher already proved the Bridge worktree clean at exact source $ExpectedHead and then created ONLY this authorized consumption evidence:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/controller_claim.json

Treat that file as controller-owned claim evidence, not unrelated WIP.
Dispatch 009 is now CONSUMED and MUST NOT be replayed even if this turn later stops.

Dispatches 001-008 are also consumed and MUST NOT be replayed.
Do not modify agent_bridge/** or any product source.
Follow the exact immutable certification prompt below.

$Prompt
"@

Write-Host "PRELAUNCH PASS: source/control/v3/canary bindings verified." -ForegroundColor Green
Write-Host "DISPATCH 009 CLAIMED: do not rerun after this point." -ForegroundColor Yellow
Write-Host "Launching certification controller..." -ForegroundColor Cyan

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
Write-Host "Dispatch 009 remains CONSUMED regardless of CLI exit."

Fetch-Ref $TaskRefspec
Fetch-Ref $CanaryRefspec

$RemoteAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
$CanaryAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()

Write-Host "Bridge remote head: $RemoteAfter"
Write-Host "Canary remote head: $CanaryAfter"

if ($RemoteAfter -ne $ExpectedHead) {
    $Changed = @(& git -C $WT diff --name-only ($ExpectedHead + ".." + $RemoteAfter))
    $Bad = @($Changed | Where-Object {
        $_ -and -not ($_.Replace("\","/").StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/"))
    })
    if ($Bad.Count -gt 0) {
        Write-Host "ALERT: 009 remote result changed unauthorized path(s):" -ForegroundColor Red
        $Bad | ForEach-Object { Write-Host "  $_" }
    }
}

& git -C $WT show ("refs/remotes/origin/" + $TaskBranch + ":" + $FinalPath) *> $null
$FinalExists = ($LASTEXITCODE -eq 0)

Write-Host "Remote final_certification.json exists: $FinalExists"
Write-Host "RESULT: CHAT INTAKE REQUIRED. Do NOT rerun Dispatch 009." -ForegroundColor Cyan

exit 0
