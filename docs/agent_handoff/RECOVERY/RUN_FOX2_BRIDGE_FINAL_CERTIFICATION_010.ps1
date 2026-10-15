$ErrorActionPreference = "Stop"

$Repo          = "C:\Projects\FOX2"
$WT            = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$TaskBranch    = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$ControlBranch = "work/FOX2-DISPATCH-chat"
$CanaryBranch  = "work/FOX2-BRIDGE-FINAL-CANARY-009"

$ControllerSource = "3e8f47a28bc66a78442059f0b0d1d3ccd4663a06"
$CertifiedCode    = "501822a33ef08c7365154913bbc677544856eee5"
$ControlCommit    = "376dbc9f82e2a931cf6d9191754ef3d62a5c6094"
$BundleCommit     = "cd2a1bd0d2a4e851a79c17f538f70734277d5ad5"

$DispatchId       = "FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-010"
$DispatchPath     = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-010.json"

$PromptCommit     = "d161710832de15e1acd6f75cc99ab15b48885a1d"
$PromptPath       = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-FINAL-CERTIFICATION-010.md"
$PromptBlob       = "ced663bbbfb4f2a5e4695747ee8c3de51a9a8b47"
$PromptSha256     = "c7c44dc400017b057debbfa1c9c74475faa6218405750ee2924b6d0abe35383e"

$V3FixturePath    = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json"
$V3FixtureBlob    = "964dceb19c74235b9dbf0d219c77046c1b2e9a4e"

$CanaryDispatchPath = "docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json"
$CanaryDispatchBlob = "7bba347537d48d4d7b499841efeafc06ea3e597f"

$CanaryPromptCommit = "530cc64feedbab463cefb0f5baed4e9919f25f15"
$CanaryPromptPath   = "docs/agent_handoff/BRIDGE/FOX2_BRIDGE_FINAL_CANARY_009_PROMPT.md"
$CanaryPromptBlob   = "a3eec972f19d84866b2915edd4bca7a4a02af335"
$CanaryPromptSha256 = "dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0"

$CanaryResultPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json"

$ClaimPath = Join-Path $WT "reports\BRIDGE-DESKTOP-BATCH-B\evidence\final010\controller_claim.json"
$FinalPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/final_certification.json"

function Fetch-Ref {
    param([string]$Refspec)
    for ($i=1; $i -le 3; $i++) {
        & git -C $WT fetch --no-tags origin $Refspec
        if ($LASTEXITCODE -eq 0) { return }
        if ($i -lt 3) { Start-Sleep -Seconds 3 }
    }
    throw "STOP: git fetch failed after 3 attempts: $Refspec"
}

function Require-GitObject {
    param([string]$Spec,[string]$Label)
    & git -C $WT cat-file -e $Spec
    if ($LASTEXITCODE -ne 0) { throw "STOP: missing $Label ($Spec)" }
}

function Get-GitBlobSha256 {
    param([string]$Spec)
    $Py = @'
import hashlib, subprocess, sys
repo = sys.argv[1]
spec = sys.argv[2]
data = subprocess.check_output(["git", "-C", repo, "cat-file", "blob", spec])
print(hashlib.sha256(data).hexdigest())
'@
    $Value = & python -c $Py $WT $Spec
    if ($LASTEXITCODE -ne 0) { throw "STOP: cannot hash git blob: $Spec" }
    return ($Value | Out-String).Trim()
}

Write-Host "FOX2 Bridge Final Certification 010 launcher" -ForegroundColor Cyan

$TaskRefspec    = "+refs/heads/" + $TaskBranch + ":refs/remotes/origin/" + $TaskBranch
$ControlRefspec = "+refs/heads/" + $ControlBranch + ":refs/remotes/origin/" + $ControlBranch
$CanaryRefspec  = "+refs/heads/" + $CanaryBranch + ":refs/remotes/origin/" + $CanaryBranch

Fetch-Ref $TaskRefspec
Fetch-Ref $ControlRefspec
Fetch-Ref $CanaryRefspec

Require-GitObject ($ControlCommit + "^{commit}") "Controller 010 control commit"
Require-GitObject ($PromptCommit + "^{commit}") "Controller 010 prompt commit"
Require-GitObject ($BundleCommit + "^{commit}") "009 canary bundle commit"
Require-GitObject ($CanaryPromptCommit + "^{commit}") "009 canary prompt commit"

$Status = @(& git -C $WT status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot read Bridge worktree status" }
if ($Status.Count -gt 0) { throw "STOP: Bridge worktree is dirty before Controller 010 claim" }

$LocalBranch = (& git -C $WT branch --show-current).Trim()
if ($LocalBranch -ne $TaskBranch) { throw "STOP: wrong Bridge task branch: $LocalBranch" }

$LocalHead = (& git -C $WT rev-parse HEAD).Trim()
$RemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
if ($LocalHead -ne $ControllerSource -or $RemoteHead -ne $ControllerSource) {
    throw "STOP: Controller 010 source mismatch; local=$LocalHead remote=$RemoteHead"
}

# Prove the task branch advanced from certified product source only by 009 evidence.
$LineagePaths = @(& git -C $WT diff --name-only ($CertifiedCode + ".." + $ControllerSource))
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot inspect report-only lineage" }
$BadLineage = @($LineagePaths | Where-Object {
    $_ -and -not ($_.Replace("\","/").StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/"))
})
if ($BadLineage.Count -gt 0) {
    Write-Host "Unexpected lineage path(s):" -ForegroundColor Red
    $BadLineage | ForEach-Object { Write-Host "  $_" }
    throw "STOP: 501822a..3e8f47a is not report-only final009 lineage"
}

$CanaryRemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()
if ($CanaryRemoteHead -ne $CertifiedCode) {
    throw "STOP: canary branch changed before claim: $CanaryRemoteHead"
}

$DispatchSpec = $ControlCommit + ":" + $DispatchPath
$DispatchRaw = (& git -C $WT show $DispatchSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($DispatchRaw)) {
    throw "STOP: cannot read Controller 010 Dispatch"
}
try { $Dispatch = $DispatchRaw | ConvertFrom-Json }
catch { throw "STOP: Controller 010 Dispatch JSON parse failed" }

if ($Dispatch.dispatch_id -ne $DispatchId) { throw "STOP: controller identity mismatch" }
if ($Dispatch.source.commit_sha -ne $ControllerSource) { throw "STOP: controller source mismatch" }
if ($Dispatch.runtime_contract.base_sha -ne $ControllerSource) { throw "STOP: controller runtime base mismatch" }
if ($Dispatch.routing.model -ne "gpt-6.1-sol") { throw "STOP: controller model mismatch" }
if ($Dispatch.routing.reasoning_effort -ne "high") { throw "STOP: controller reasoning mismatch" }
if ($Dispatch.routing.permission_profile -ne "FULL_ACCESS") { throw "STOP: controller permission mismatch" }
if ([int]$Dispatch.max_runs -ne 1) { throw "STOP: controller max_runs mismatch" }
if (@($Dispatch.runtime_contract.allowed_code_paths).Count -ne 0) {
    throw "STOP: Controller 010 unexpectedly authorizes product code paths"
}

$PromptSpec = $PromptCommit + ":" + $PromptPath
$ActualPromptBlob = (& git -C $WT rev-parse $PromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualPromptBlob -ne $PromptBlob) {
    throw "STOP: Controller 010 prompt blob mismatch"
}
$ActualPromptSha = Get-GitBlobSha256 $PromptSpec
if ($ActualPromptSha -ne $PromptSha256) {
    throw "STOP: Controller 010 prompt raw SHA-256 mismatch: $ActualPromptSha"
}
if ($Dispatch.prompt.sha256 -ne $ActualPromptSha) {
    throw "STOP: Controller 010 Dispatch prompt SHA-256 binding mismatch"
}

$ActualV3Blob = (& git -C $WT rev-parse ($BundleCommit + ":" + $V3FixturePath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualV3Blob -ne $V3FixtureBlob) {
    throw "STOP: v3 fixture blob mismatch"
}

$ActualCanaryBlob = (& git -C $WT rev-parse ($BundleCommit + ":" + $CanaryDispatchPath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualCanaryBlob -ne $CanaryDispatchBlob) {
    throw "STOP: legacy canary Dispatch blob mismatch"
}

$CanaryPromptSpec = $CanaryPromptCommit + ":" + $CanaryPromptPath
$ActualCanaryPromptBlob = (& git -C $WT rev-parse $CanaryPromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualCanaryPromptBlob -ne $CanaryPromptBlob) {
    throw "STOP: legacy canary prompt blob mismatch"
}
$ActualCanaryPromptSha = Get-GitBlobSha256 $CanaryPromptSpec
if ($ActualCanaryPromptSha -ne $CanaryPromptSha256) {
    throw "STOP: legacy canary prompt SHA-256 mismatch: $ActualCanaryPromptSha"
}

if (Test-Path -LiteralPath $ClaimPath) {
    throw "STOP: Controller 010 already has a local claim; never replay"
}

& git -C $WT show ("refs/remotes/origin/" + $CanaryBranch + ":" + $CanaryResultPath) *> $null
if ($LASTEXITCODE -eq 0) {
    throw "STOP: legacy canary result already exists; do not claim Controller 010"
}

$Prompt = (& git -C $WT show $PromptSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Prompt)) {
    throw "STOP: cannot read Controller 010 prompt"
}

# All immutable checks have passed. From this exact point Controller 010 is consumed.
New-Item -ItemType Directory -Force -Path (Split-Path $ClaimPath) | Out-Null
$Claim = [ordered]@{
    dispatch_id = $DispatchId
    control_commit = $ControlCommit
    source_head = $ControllerSource
    certified_product_source = $CertifiedCode
    prompt_sha256 = $ActualPromptSha
    canary_dispatch_id = "FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001"
    canary_bundle_commit = $BundleCommit
    canary_branch = $CanaryBranch
    canary_base = $CertifiedCode
    canary_prompt_sha256 = $ActualCanaryPromptSha
    consumed = $true
    max_runs = 1
    claimed_at = (Get-Date).ToUniversalTime().ToString("o")
}
$ClaimJson = ($Claim | ConvertTo-Json -Depth 8) + [char]10
[IO.File]::WriteAllText($ClaimPath, $ClaimJson, [Text.UTF8Encoding]::new($false))

$AgentInput = @"
Execute exactly FOX2 replacement certification controller:
$DispatchId

Before any runtime mutation, independently read and validate:
git show $($ControlCommit):$DispatchPath

The launcher has already verified:
- exact Controller 010 source $ControllerSource;
- report-only lineage from certified product source $CertifiedCode;
- raw-byte Controller 010 prompt SHA-256 $PromptSha256;
- exact v3 fixture and existing unclaimed legacy canary blobs;
- raw-byte legacy canary prompt SHA-256 $CanaryPromptSha256;
- canary branch exact base $CertifiedCode.

The launcher then created ONLY this authorized consumption artifact:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/controller_claim.json

Treat it as Controller-owned claim evidence, not unrelated WIP.

Controller 010 is now CONSUMED and MUST NOT be replayed even if this turn stops.
Dispatches 001-009 are also consumed and MUST NOT be replayed.
Do not modify agent_bridge/** or any product source.
Do not create another canary identity.
Follow the exact immutable certification prompt below.

$Prompt
"@

Write-Host "PRELAUNCH PASS: Controller 010 + existing Canary 009 bindings verified." -ForegroundColor Green
Write-Host "CONTROLLER 010 CLAIMED: never rerun after this point." -ForegroundColor Yellow
Write-Host "Launching final certification controller..." -ForegroundColor Cyan

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
Write-Host "Controller 010 remains CONSUMED regardless of CLI exit."

Fetch-Ref $TaskRefspec
Fetch-Ref $CanaryRefspec

$RemoteAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
$CanaryAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()

Write-Host "Bridge remote head: $RemoteAfter"
Write-Host "Canary remote head: $CanaryAfter"

if ($RemoteAfter -ne $ControllerSource) {
    $Changed = @(& git -C $WT diff --name-only ($ControllerSource + ".." + $RemoteAfter))
    $Bad = @($Changed | Where-Object {
        $_ -and -not ($_.Replace("\","/").StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/"))
    })
    if ($Bad.Count -gt 0) {
        Write-Host "ALERT: Controller 010 changed unauthorized task-branch path(s):" -ForegroundColor Red
        $Bad | ForEach-Object { Write-Host "  $_" }
    }
}

& git -C $WT show ("refs/remotes/origin/" + $TaskBranch + ":" + $FinalPath) *> $null
$FinalExists = ($LASTEXITCODE -eq 0)

Write-Host "Remote final010/final_certification.json exists: $FinalExists"
Write-Host "RESULT: CHAT INTAKE REQUIRED. Do NOT rerun Controller 010." -ForegroundColor Cyan

exit 0
