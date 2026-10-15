$ErrorActionPreference = "Stop"

$Repo          = "C:\Projects\FOX2"
$WT            = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$TaskBranch    = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$ControlBranch = "work/FOX2-DISPATCH-chat"
$CanaryBranch  = "work/FOX2-BRIDGE-FINAL-CANARY-009"

$ControllerSource = "4a00621b6a736d612cdf99506da01d0e4b3c6417"
$CertifiedCode    = "501822a33ef08c7365154913bbc677544856eee5"

$ControlCommit = "786cfec6b6fbd641a8bde90ccb0e66ac44f98941"
$DispatchId    = "FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-012"
$DispatchPath  = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-012.json"

$PromptCommit = "df7fcbc7af38ca8df3c72eb4ff3e38a0556c26f2"
$PromptPath   = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-FINAL-CERTIFICATION-012.md"
$PromptBlob   = "f1c73cc59e759211938ec3ff2958f1f6398b0116"
$PromptSha256 = "d61ab521f2a96b06340d13ee9ea5b0e52633db887446b4e978324b3d2b383042"

$ObserverCommit = "928e8279ac6ca45d9421d5fa3773dd44943008ef"
$ObserverPath   = "docs/agent_handoff/RECOVERY/FOX2-BRIDGE-CERT-PROCESS-OBSERVER-011.ps1"
$ObserverBlob   = "000dc032777cec198f59ddb7d6af049a9d23f1fc"
$ObserverSha256 = "75325a05b79cc97e20811d724bde9f0642376b2b359de68d5d6439b5f97d5792"
$ObserverBytes  = 2768

$BundleCommit       = "cd2a1bd0d2a4e851a79c17f538f70734277d5ad5"
$V3FixturePath      = "docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-FINAL-CERT-V3-009.json"
$V3FixtureBlob      = "964dceb19c74235b9dbf0d219c77046c1b2e9a4e"
$CanaryDispatchPath = "docs/agent_handoff/FOX2-BRIDGE-FINAL-CANARY-009/dispatch/FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001.json"
$CanaryDispatchBlob = "7bba347537d48d4d7b499841efeafc06ea3e597f"

$CanaryPromptCommit = "530cc64feedbab463cefb0f5baed4e9919f25f15"
$CanaryPromptPath   = "docs/agent_handoff/BRIDGE/FOX2_BRIDGE_FINAL_CANARY_009_PROMPT.md"
$CanaryPromptBlob   = "a3eec972f19d84866b2915edd4bca7a4a02af335"
$CanaryPromptSha256 = "dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0"
$CanaryResultPath   = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/canary/agent_result.json"

$ClaimPath = Join-Path $WT "reports\BRIDGE-DESKTOP-BATCH-B\evidence\final012\controller_claim.json"
$FinalPath = "reports/BRIDGE-DESKTOP-BATCH-B/evidence/final012/final_certification.json"

$ObserverRun = Join-Path $env:LOCALAPPDATA "FOX2\runner-cache\FOX2-BRIDGE-CERT-PROCESS-OBSERVER-012.ps1"

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
repo, spec = sys.argv[1], sys.argv[2]
data = subprocess.check_output(["git", "-C", repo, "cat-file", "blob", spec])
print(hashlib.sha256(data).hexdigest())
'@
    $Value = & python -c $Py $WT $Spec
    if ($LASTEXITCODE -ne 0) { throw "STOP: cannot hash git blob: $Spec" }
    return ($Value | Out-String).Trim()
}

function Materialize-GitBlobRaw {
    param([string]$Spec,[string]$Target,[string]$ExpectedSha256,[int]$ExpectedBytes)
    $Parent = Split-Path $Target
    New-Item -ItemType Directory -Force -Path $Parent | Out-Null

    $Py = @'
import hashlib, pathlib, subprocess, sys
repo, spec, target, expected_sha, expected_bytes = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
data = subprocess.check_output(["git", "-C", repo, "cat-file", "blob", spec])
sha = hashlib.sha256(data).hexdigest()
crlf = data.count(b"\r\n")
if len(data) != expected_bytes:
    raise SystemExit(f"RAW_BYTE_LENGTH_MISMATCH:{len(data)}")
if sha != expected_sha:
    raise SystemExit(f"RAW_SHA256_MISMATCH:{sha}")
if crlf != 0:
    raise SystemExit(f"RAW_CRLF_COUNT_NONZERO:{crlf}")
pathlib.Path(target).write_bytes(data)
written = pathlib.Path(target).read_bytes()
if written != data:
    raise SystemExit("RAW_WRITE_READBACK_MISMATCH")
print(f"{len(written)}|{hashlib.sha256(written).hexdigest()}|{written.count(b'chr(13)+chr(10)')}")
'@
    # The final printed CRLF expression is not trusted; verification below is authoritative.
    & python -c $Py $WT $Spec $Target $ExpectedSha256 $ExpectedBytes | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "STOP: binary-safe observer materialization failed" }

    $VerifyPy = @'
import hashlib, pathlib, sys
p = pathlib.Path(sys.argv[1])
data = p.read_bytes()
print(f"{len(data)}|{hashlib.sha256(data).hexdigest()}|{data.count(bytes([13,10]))}")
'@
    $Raw = (& python -c $VerifyPy $Target | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw "STOP: observer materialization readback failed" }
    $Parts = $Raw.Split("|")
    if ([int]$Parts[0] -ne $ExpectedBytes) { throw "STOP: materialized observer byte length mismatch: $($Parts[0])" }
    if ($Parts[1] -ne $ExpectedSha256) { throw "STOP: materialized observer SHA-256 mismatch: $($Parts[1])" }
    if ([int]$Parts[2] -ne 0) { throw "STOP: materialized observer CRLF count is nonzero: $($Parts[2])" }

    return [ordered]@{
        path = $Target
        bytes = [int]$Parts[0]
        sha256 = $Parts[1]
        crlf_count = [int]$Parts[2]
        status = "PASS_EXACT_RAW_GIT_BLOB"
    }
}

Write-Host "FOX2 Bridge Final Certification 012 launcher" -ForegroundColor Cyan

$TaskRefspec    = "+refs/heads/" + $TaskBranch + ":refs/remotes/origin/" + $TaskBranch
$ControlRefspec = "+refs/heads/" + $ControlBranch + ":refs/remotes/origin/" + $ControlBranch
$CanaryRefspec  = "+refs/heads/" + $CanaryBranch + ":refs/remotes/origin/" + $CanaryBranch

Fetch-Ref $TaskRefspec
Fetch-Ref $ControlRefspec
Fetch-Ref $CanaryRefspec

Require-GitObject ($ControlCommit + "^{commit}") "Controller 012 control commit"
Require-GitObject ($PromptCommit + "^{commit}") "Controller 012 prompt commit"
Require-GitObject ($ObserverCommit + "^{commit}") "observer helper commit"
Require-GitObject ($BundleCommit + "^{commit}") "canary bundle commit"
Require-GitObject ($CanaryPromptCommit + "^{commit}") "canary prompt commit"

$Status = @(& git -C $WT status --porcelain=v1 --untracked-files=all)
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot read Bridge worktree status" }
if ($Status.Count -gt 0) { throw "STOP: Bridge worktree is dirty before Controller 012 claim" }

$LocalBranch = (& git -C $WT branch --show-current).Trim()
if ($LocalBranch -ne $TaskBranch) { throw "STOP: wrong Bridge task branch: $LocalBranch" }

$LocalHead = (& git -C $WT rev-parse HEAD).Trim()
$RemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
if ($LocalHead -ne $ControllerSource -or $RemoteHead -ne $ControllerSource) {
    throw "STOP: Controller 012 source mismatch; local=$LocalHead remote=$RemoteHead"
}

$LineagePaths = @(& git -C $WT diff --name-only ($CertifiedCode + ".." + $ControllerSource))
if ($LASTEXITCODE -ne 0) { throw "STOP: cannot inspect certification lineage" }
$BadLineage = @($LineagePaths | Where-Object {
    if (-not $_) { return $false }
    $N = $_.Replace("\","/")
    return -not (
        $N.StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/") -or
        $N.StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final010/") -or
        $N.StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final011/")
    )
})
if ($BadLineage.Count -gt 0) {
    $BadLineage | ForEach-Object { Write-Host "Unexpected lineage: $_" -ForegroundColor Red }
    throw "STOP: certified product lineage contains non-certification change"
}

$CanaryRemoteHead = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()
if ($CanaryRemoteHead -ne $CertifiedCode) { throw "STOP: canary branch changed before claim: $CanaryRemoteHead" }

$DispatchSpec = $ControlCommit + ":" + $DispatchPath
$DispatchRaw = (& git -C $WT show $DispatchSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($DispatchRaw)) { throw "STOP: cannot read Controller 012 Dispatch" }
try { $Dispatch = $DispatchRaw | ConvertFrom-Json } catch { throw "STOP: Controller 012 Dispatch JSON parse failed" }

if ($Dispatch.dispatch_id -ne $DispatchId) { throw "STOP: controller identity mismatch" }
if ($Dispatch.source.commit_sha -ne $ControllerSource) { throw "STOP: controller source mismatch" }
if ($Dispatch.runtime_contract.base_sha -ne $ControllerSource) { throw "STOP: controller runtime base mismatch" }
if ($Dispatch.routing.model -ne "gpt-6.1-sol") { throw "STOP: controller model mismatch" }
if ($Dispatch.routing.reasoning_effort -ne "high") { throw "STOP: controller reasoning mismatch" }
if ($Dispatch.routing.permission_profile -ne "FULL_ACCESS") { throw "STOP: controller permission mismatch" }
if ([int]$Dispatch.max_runs -ne 1) { throw "STOP: controller max_runs mismatch" }
if (@($Dispatch.runtime_contract.allowed_code_paths).Count -ne 0) { throw "STOP: product code paths unexpectedly authorized" }

$PromptSpec = $PromptCommit + ":" + $PromptPath
$ActualPromptBlob = (& git -C $WT rev-parse $PromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualPromptBlob -ne $PromptBlob) { throw "STOP: Controller 012 prompt blob mismatch" }
$ActualPromptSha = Get-GitBlobSha256 $PromptSpec
if ($ActualPromptSha -ne $PromptSha256 -or $Dispatch.prompt.sha256 -ne $ActualPromptSha) {
    throw "STOP: Controller 012 prompt SHA-256 binding mismatch"
}

$ObserverSpec = $ObserverCommit + ":" + $ObserverPath
$ActualObserverBlob = (& git -C $WT rev-parse $ObserverSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualObserverBlob -ne $ObserverBlob) { throw "STOP: observer Git blob mismatch" }
$ActualObserverSha = Get-GitBlobSha256 $ObserverSpec
if ($ActualObserverSha -ne $ObserverSha256) { throw "STOP: observer Git SHA-256 mismatch" }

$ActualV3Blob = (& git -C $WT rev-parse ($BundleCommit + ":" + $V3FixturePath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualV3Blob -ne $V3FixtureBlob) { throw "STOP: v3 fixture blob mismatch" }

$ActualCanaryBlob = (& git -C $WT rev-parse ($BundleCommit + ":" + $CanaryDispatchPath)).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualCanaryBlob -ne $CanaryDispatchBlob) { throw "STOP: canary Dispatch blob mismatch" }

$CanaryPromptSpec = $CanaryPromptCommit + ":" + $CanaryPromptPath
$ActualCanaryPromptBlob = (& git -C $WT rev-parse $CanaryPromptSpec).Trim()
if ($LASTEXITCODE -ne 0 -or $ActualCanaryPromptBlob -ne $CanaryPromptBlob) { throw "STOP: canary prompt blob mismatch" }
$ActualCanaryPromptSha = Get-GitBlobSha256 $CanaryPromptSpec
if ($ActualCanaryPromptSha -ne $CanaryPromptSha256) { throw "STOP: canary prompt SHA-256 mismatch" }

if (Test-Path -LiteralPath $ClaimPath) { throw "STOP: Controller 012 already claimed; never replay" }
& git -C $WT show ("refs/remotes/origin/" + $CanaryBranch + ":" + $CanaryResultPath) *> $null
if ($LASTEXITCODE -eq 0) { throw "STOP: canary result already exists; do not claim Controller 012" }

# Binary-safe materialization: no PowerShell text pipeline touches observer bytes.
$Materialization = Materialize-GitBlobRaw $ObserverSpec $ObserverRun $ObserverSha256 $ObserverBytes

$BridgeRoot = Join-Path $env:LOCALAPPDATA "FOX2\AgentBridge"
$CurrentPath = Join-Path $BridgeRoot "current.json"
if (-not (Test-Path -LiteralPath $CurrentPath -PathType Leaf)) { throw "STOP: installed Bridge current.json missing" }
$Current = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
$PackageId = [string]$Current.package_sha256
if ($PackageId -notmatch '^[0-9a-f]{64}$') { throw "STOP: installed Bridge package identity invalid" }
$VersionRoot = Join-Path $BridgeRoot ("versions\" + $PackageId)
$TrayScript = Join-Path $VersionRoot "payload\scripts\desktop_tray.ps1"
$WorkerPython = Join-Path $VersionRoot "runtime\Scripts\python.exe"
$Pwsh = "C:\Program Files\PowerShell\7\pwsh.exe"

foreach ($Required in @($TrayScript,$WorkerPython,$Pwsh)) {
    if (-not (Test-Path -LiteralPath $Required -PathType Leaf)) { throw "STOP: observer target missing: $Required" }
}

$env:FOX2_CERT_TRAY_SCRIPT = $TrayScript
$env:FOX2_CERT_WORKER_PYTHON = $WorkerPython
$env:FOX2_CERT_PWSH = $Pwsh

$ObserverRaw = & $Pwsh -NoLogo -NoProfile -NonInteractive -File $ObserverRun
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($ObserverRaw | Out-String))) { throw "STOP: observer smoke test failed" }
try { $Observer = ($ObserverRaw | Out-String) | ConvertFrom-Json } catch { throw "STOP: observer returned invalid JSON" }

if ($Observer.schema -ne "FOX2_CERT_PROCESS_OBSERVER_1") { throw "STOP: observer schema mismatch" }
if ([int]$Observer.tray_count -ne 0 -or [int]$Observer.worker_count -ne 0) {
    throw "STOP: Bridge not idle before claim; tray=$($Observer.tray_count) worker=$($Observer.worker_count)"
}
foreach ($Match in @($Observer.matches)) {
    if ([int]$Match.pid -eq [int]$Observer.observer_pid) { throw "STOP: observer self-match before claim" }
}

$Prompt = (& git -C $WT show $PromptSpec | Out-String)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Prompt)) { throw "STOP: cannot read Controller 012 prompt" }

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
    observer_materialization = $Materialization
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
Execute exactly FOX2 raw-byte-safe final certification controller:
$DispatchId

Before runtime mutation, independently read and validate:
git show $($ControlCommit):$DispatchPath

The launcher already verified:
- exact Controller 012 source $ControllerSource;
- report-only final009/final010/final011 lineage from certified product source $CertifiedCode;
- Controller prompt raw SHA-256 $PromptSha256;
- exact observer Git blob and SHA-256;
- observer materialized with raw git-cat-file bytes using Python Path.write_bytes;
- materialized observer bytes=$ObserverBytes / SHA-256=$ObserverSha256 / CRLF count=0;
- observer smoke test returned Tray=0 / Worker=0 / no self-match;
- exact v3 fixture and existing unclaimed Canary 009;
- canary branch exact base $CertifiedCode.

The exact already-verified observer file is:
$ObserverRun

DO NOT materialize the observer again.
DO NOT pass observer source through any PowerShell text pipeline.

The launcher then created ONLY:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/final012/controller_claim.json

Controller 012 is now CONSUMED and MUST NOT be replayed even if this turn stops.
Dispatches 001-011 are consumed and MUST NOT be replayed.
Do not modify agent_bridge/** or any product source.
Do not create another canary identity.
Follow the exact immutable certification prompt below.

$Prompt
"@

Write-Host "PRELAUNCH PASS: Controller 012 raw-byte observer + Canary 009 verified." -ForegroundColor Green
Write-Host "OBSERVER RAW MATERIALIZATION PASS: bytes=2768 SHA-256 exact CRLF=0." -ForegroundColor Green
Write-Host "OBSERVER SMOKE PASS: Tray=0 Worker=0 no self-match." -ForegroundColor Green
Write-Host "CONTROLLER 012 CLAIMED: never rerun after this point." -ForegroundColor Yellow

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
Write-Host "Controller 012 remains CONSUMED regardless of CLI exit."

Fetch-Ref $TaskRefspec
Fetch-Ref $CanaryRefspec

$RemoteAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $TaskBranch)).Trim()
$CanaryAfter = (& git -C $WT rev-parse ("refs/remotes/origin/" + $CanaryBranch)).Trim()

Write-Host "Bridge remote head: $RemoteAfter"
Write-Host "Canary remote head: $CanaryAfter"

if ($RemoteAfter -ne $ControllerSource) {
    $Changed = @(& git -C $WT diff --name-only ($ControllerSource + ".." + $RemoteAfter))
    $Bad = @($Changed | Where-Object {
        $_ -and -not ($_.Replace("\","/").StartsWith("reports/BRIDGE-DESKTOP-BATCH-B/evidence/final012/"))
    })
    if ($Bad.Count -gt 0) {
        Write-Host "ALERT: Controller 012 changed unauthorized task-branch path(s):" -ForegroundColor Red
        $Bad | ForEach-Object { Write-Host "  $_" }
    }
}

& git -C $WT show ("refs/remotes/origin/" + $TaskBranch + ":" + $FinalPath) *> $null
$FinalExists = ($LASTEXITCODE -eq 0)

Write-Host "Remote final012/final_certification.json exists: $FinalExists"
Write-Host "RESULT: CHAT INTAKE REQUIRED. Do NOT rerun Controller 012." -ForegroundColor Cyan
exit 0
