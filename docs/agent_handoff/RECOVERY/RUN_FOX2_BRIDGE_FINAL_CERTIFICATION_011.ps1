$ErrorActionPreference = "Stop"

$Repo          = "C:\Projects\FOX2"
$WT            = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$TaskBranch    = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$ControlBranch = "work/FOX2-DISPATCH-chat"
$CanaryBranch  = "work/FOX2-BRIDGE-FINAL-CANARY-009"

$ControllerSource = "92bd9c82385f05893d9379c00f964760e9fe06dc"
$CertifiedCode    = "501822a33ef08c7365154913bbc677544856eee5"

$ControlCommit = "4eae4eec694acb70e472e0e14d23861cee9c214c"
$DispatchId    = "FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-011"
$DispatchPath  = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-011.json"

$PromptCommit = "ebb841afd47a1f41dcb03a4f5c7a114e203cdb1a"
$PromptPath   = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-FINAL-CERTIFICATION-011.md"
$PromptBlob   = "e1e892f30ab36c77ff7b9e7305a68d91dbc7b554"
$PromptSha256 = "2ad27316f2d049baf4dec12161d186adaef6f428ac02f36dbb6dd6a6f61a197d"

$ObserverCommit = "928e8279ac6ca45d9421d5fa3773dd44943008ef"
$ObserverPath   = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1"
$ObserverBlob   = "000dc032777cec198f59ddb7d6af049a9d23f1fc"
$ObserverSha256 = "75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792"

$BundleCommit      = "cd2a1bd0d2a4e851a79c17f538f70734277d5ad5"
$V3FixturePath     = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json"
$V3FixtureBlob     = "964dceb19c74235b9dbf0d219c77046c1b2e9a4e"
$CanaryDispatchPath = "docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json"
$CanaryDispatchBlob = "7bba347537d48d4d7b499841efeafc06ea3e597f"

$CanaryPromptCommit = "530cc64feedbab463cefb0f5baed4e9919f25f15"
$CanaryPromptPath   = "docs/agent_handoff/BRIDGE/FOX2_BRIDGE_FINAL_CANARY_009_PROMPT.md"
$CanaryPromptBlob   = "a3eec972f19d84866b2915edd4bca7a4a02af335"
$CanaryPromptSha256 = "dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0"
$CanaryResultPath   = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json"

$ClaimPath = Join-Path $WT "reports\BRIDGE-DESKTOP-BATCH-B\evidence\final011\controller_claim.json"
$FinalPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/final_certification.json"

$ObserverRun = Join-Path $env:LOCALAPPDATA "FOX2\runner-cache\FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1"

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

function Materialize-GitBlob {
    param([string]$Spec,[string]$Target)
    $Parent = Split-Path $Target
    New-Item -ItemType Directory -Force -Path $Parent | Out-Null
    $Content = & git -C $WT show $Spec | Out-String
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Content)) {
        throw "STOP: cannot materialize $Spec"
    }
    [IO.File]::WriteAllText($Target, $Content, [Text.UTF8Encoding]::new($false))
}

Write-Host "FOX2 Bridge Final Certification 011 launcher" -ForegroundColor Cyan

$TaskRefspec    = "+refs/heads/" + $TaskBranch + ":refs/remotes/origin/" + $TaskBranch
$ControlRefspec = "+refs/heads/" + $ControlBranch + ":refs/remotes/origin/" + $ControlBranch
$CanaryRefspec  = "+refs/heads/" + $CanaryBranch + ":refs/remotes/origin/" + $CanaryBranch

Fetch-Ref $TaskRefspec
Fetch-Ref $ControlRefspec
Fetch-Ref $CanaryRefspec

Require-GitObject ($ControlCommit + "^{commit}") "Controller 011 control commit"
Require-GitObject ($PromptCommit + "^{commit}") "Controller 011 prompt commit"
Require-GitObject ($ObserverCommit + "^{commit}") "observer helper commit"
Require-GitObject ($BundleCommit + "^{commit}") "canary bundle commit"
Require-GitObject ($CanaryPromptCommit + "^{commit}") "canary prompt commit"

$Status = @(& git -C $WT status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot read Bridge worktree status" }
if ($Status.Count -gt 0) { throw "STOP: Bridge worktree is dirty before Controller 011 claim" }

$LocalBranch = (& git -C $WT branch --show-current).Trim()
if ($LocalBranch -ne $TaskBranch) { throw "STOP: wrong Bridge task branch: $LocalBranch" }

$LocalHead = (& git -C $WT rev-parse HEAD).Trim()
$RemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
if ($LocalHead -ne $ControllerSource -or $RemoteHead -ne $ControllerSource) {
    throw "STOP: Controller 011 source mismatch; local=$LocalHead remote=$RemoteHead"
}

# Certified product source -> current task head may contain only final009/final010 evidence.
$LineagePaths = @(& git -C $WT diff --name-only ($CertifiedCode + ".." + $ControllerSource))
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot inspect certification lineage" }
$BadLineage = @($LineagePaths | Where-Object {
    if (-not $_) { return $false }
    $N = $_.Replace("\","/")
    return -not (
        $N.StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/") -or
        $N.StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/")
    )
})
if ($BadLineage.Count -gt 0) {
    Write-Host "Unexpected lineage path(s):" -ForegroundColor Red
    $BadLineage | ForEach-Object { Write-Host "  $_" }
    throw "STOP: certified product lineage is not report-only final009/final010"
}

$CanaryRemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()
if ($CanaryRemoteHead -ne $CertifiedCode) {
    throw "STOP: canary branch changed before claim: $CanaryRemoteHead"
}

$DispatchSpec = $ControlCommit + ":" + $DispatchPath
$DispatchRaw = (& git -C $WT show $DispatchSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($DispatchRaw)) {
    throw "STOP: cannot read Controller 011 Dispatch"
}
try { $Dispatch = $DispatchRaw | ConvertFrom-Json }
catch { throw "STOP: Controller 011 Dispatch JSON parse failed" }

if ($Dispatch.dispatch_id -ne $DispatchId) { throw "STOP: controller identity mismatch" }
if ($Dispatch.source.commit_sha -ne $ControllerSource) { throw "STOP: controller source mismatch" }
if ($Dispatch.runtime_contract.base_sha -ne $ControllerSource) { throw "STOP: controller runtime base mismatch" }
if ($Dispatch.routing.model -ne "gpt-6.1-sol") { throw "STOP: controller model mismatch" }
if ($Dispatch.routing.reasoning_effort -ne "high") { throw "STOP: controller reasoning mismatch" }
if ($Dispatch.routing.permission_profile -ne "FULL_ACCESS") { throw "STOP: controller permission mismatch" }
if ([int]$Dispatch.max_runs -ne 1) { throw "STOP: controller max_runs mismatch" }
if (@($Dispatch.runtime_contract.allowed_code_paths).Count -ne 0) {
    throw "STOP: Controller 011 unexpectedly authorizes product code paths"
}

$PromptSpec = $PromptCommit + ":" + $PromptPath
$ActualPromptBlob = (& git -C $WT rev-parse $PromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualPromptBlob -ne $PromptBlob) {
    throw "STOP: Controller 011 prompt blob mismatch"
}
$ActualPromptSha = Get-GitBlobSha256 $PromptSpec
if ($ActualPromptSha -ne $PromptSha256 -or $Dispatch.prompt.sha256 -ne $ActualPromptSha) {
    throw "STOP: Controller 011 prompt raw SHA-256 binding mismatch"
}

$ObserverSpec = $ObserverCommit + ":" + $ObserverPath
$ActualObserverBlob = (& git -C $WT rev-parse $ObserverSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualObserverBlob -ne $ObserverBlob) {
    throw "STOP: observer helper blob mismatch"
}
$ActualObserverSha = Get-GitBlobSha256 $ObserverSpec
if ($ActualObserverSha -ne $ObserverSha256) {
    throw "STOP: observer helper raw SHA-256 mismatch"
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
    throw "STOP: legacy canary prompt SHA-256 mismatch"
}

if (Test-Path -LiteralPath $ClaimPath) {
    throw "STOP: Controller 011 already has a local claim; never replay"
}
& git -C $WT show ("refs/remotes/origin/" + $CanaryBranch + ":" + $CanaryResultPath) *> $null
if ($LASTEXITCODE -eq 0) {
    throw "STOP: legacy canary result already exists; do not claim Controller 011"
}

# Materialize exact observer outside the repository and smoke-test before claim.
Materialize-GitBlob $ObserverSpec $ObserverRun

$BridgeRoot = Join-Path $env:LOCALAPPDATA "FOX2\AgentBridge"
$CurrentPath = Join-Path $BridgeRoot "current.json"
if (-not (Test-Path -LiteralPath $CurrentPath -PathType Leaf)) {
    throw "STOP: installed Bridge current.json missing"
}
$Current = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
$PackageId = [string]$Current.package_sha256
if ($PackageId -notmatch '^[0-9a-f]{64}$') {
    throw "STOP: installed Bridge package identity invalid"
}
$VersionRoot = Join-Path $BridgeRoot ("versions\" + $PackageId)
$TrayScript = Join-Path $VersionRoot "payload\scripts\desktop_tray.ps1"
$WorkerPython = Join-Path $VersionRoot "runtime\Scripts\python.exe"
$Pwsh = "C:\Program Files\PowerShell\7\pwsh.exe"

foreach ($Required in @($TrayScript,$WorkerPython,$Pwsh)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) {
        throw "STOP: observer target missing: $Required"
    }
}

$env:FOX2_CERT_TRAY_SCRIPT = $TrayScript
$env:FOX2_CERT_WORKER_PYTHON = $WorkerPython
$env:FOX2_CERT_PWSH = $Pwsh

$ObserverRaw = & $Pwsh -NoLogo -NoProfile -NonInteractive -File $ObserverRun
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($ObserverRaw | Out-String))) {
    throw "STOP: observer helper smoke test failed"
}
try { $Observer = ($ObserverRaw | Out-String) | ConvertFrom-Json }
catch { throw "STOP: observer helper returned invalid JSON" }

if ($Observer.schema -ne "FOX2_CERT_PROCESS_OBSERVER_1") {
    throw "STOP: observer schema mismatch"
}
if ([int]$Observer.tray_count -ne 0 -or [int]$Observer.worker_count -ne 0) {
    throw "STOP: Bridge is not idle before Controller 011 claim; tray=$($Observer.tray_count) worker=$($Observer.worker_count)"
}
foreach ($Match in @($Observer.matches)) {
    if ([int]$Match.pid -eq [int]$Observer.observer_pid) {
        throw "STOP: observer self-match regression detected before claim"
    }
}

$Prompt = (& git -C $WT show $PromptSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Prompt)) {
    throw "STOP: cannot read Controller 011 prompt"
}

# All immutable + observer checks passed. From this point Controller 011 is consumed.
New-Item -ItemType Directory -Force -Path (Split-Path $ClaimPath) | Out-Null
$Claim = [ordered]@{
    dispatch_id = $DispatchId
    control_commit = $ControlCommit
    source_head = $ControllerSource
    certified_product_source = $CertifiedCode
    prompt_sha256 = $ActualPromptSha
    observer_commit = $ObserverCommit
    observer_blob_sha1 = $ActualObserverBlob
    observer_sha256 = $ActualObserverSha
    observer_preclaim = [ordered]@{
        tray_count = [int]$Observer.tray_count
        worker_count = [int]$Observer.worker_count
        observer_pid = [int]$Observer.observer_pid
        status = "PASS_ZERO_ZERO_NO_SELF_MATCH"
    }
    canary_dispatch_id = "FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001"
    canary_bundle_commit = $BundleCommit
    canary_branch = $CanaryBranch
    canary_base = $CertifiedCode
    canary_prompt_sha256 = $ActualCanaryPromptSha
    consumed = $true
    max_runs = 1
    claimed_at = (Get-Date).ToUniversalTime().ToString("o")
}
$ClaimJson = ($Claim | ConvertTo-Json -Depth 10) + [char]10
[IO.File]::WriteAllText($ClaimPath, $ClaimJson, [Text.UTF8Encoding]::new($false))

$AgentInput = @"
Execute exactly FOX2 observer-corrected final certification controller:
$DispatchId

Before runtime mutation, independently read and validate:
git show $($ControlCommit):$DispatchPath

The launcher already verified:
- exact Controller 011 source $ControllerSource;
- report-only final009/final010 lineage from certified product source $CertifiedCode;
- Controller 011 prompt raw SHA-256 $PromptSha256;
- exact observer helper commit/blob/SHA-256 $ObserverCommit / $ObserverBlob / $ObserverSha256;
- exact v3 fixture and existing unclaimed canary blobs;
- canary prompt raw SHA-256 $CanaryPromptSha256;
- canary branch exact base $CertifiedCode;
- observer preclaim smoke test returned tray_count=0 / worker_count=0 / no self-match.

The exact observer helper is materialized at:
$ObserverRun

The launcher then created ONLY this authorized consumption artifact:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/controller_claim.json

Treat it as Controller-owned claim evidence, not unrelated WIP.

Controller 011 is now CONSUMED and MUST NOT be replayed even if this turn stops.
Dispatches 001-010 are consumed and MUST NOT be replayed.
Do not modify agent_bridge/** or any product source.
Do not create another canary identity.
Use the pinned observer helper; do not recreate the failing inline process query.
Follow the exact immutable certification prompt below.

$Prompt
"@

Write-Host "PRELAUNCH PASS: Controller 011 + observer + Canary 009 verified." -ForegroundColor Green
Write-Host "OBSERVER SMOKE TEST PASS: Tray=0 Worker=0 no self-match." -ForegroundColor Green
Write-Host "CONTROLLER 011 CLAIMED: never rerun after this point." -ForegroundColor Yellow
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
Write-Host "Controller 011 remains CONSUMED regardless of CLI exit."

Fetch-Ref $TaskRefspec
Fetch-Ref $CanaryRefspec

$RemoteAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
$CanaryAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()

Write-Host "Bridge remote head: $RemoteAfter"
Write-Host "Canary remote head: $CanaryAfter"

if ($RemoteAfter -ne $ControllerSource) {
    $Changed = @(& git -C $WT diff --name-only ($ControllerSource + ".." + $RemoteAfter))
    $Bad = @($Changed | Where-Object {
        $_ -and -not ($_.Replace("\","/").StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/"))
    })
    if ($Bad.Count -gt 0) {
        Write-Host "ALERT: Controller 011 changed unauthorized task-branch path(s):" -ForegroundColor Red
        $Bad | ForEach-Object { Write-Host "  $_" }
    }
}

& git -C $WT show ("refs/remotes/origin/" + $TaskBranch + ":" + $FinalPath) *> $null
$FinalExists = ($LASTEXITCODE -eq 0)

Write-Host "Remote final011/final_certification.json exists: $FinalExists"
Write-Host "RESULT: CHAT INTAKE REQUIRED. Do NOT rerun Controller 011." -ForegroundColor Cyan

exit 0
