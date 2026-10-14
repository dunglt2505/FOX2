$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Repo = "C:\Projects\FOX2"
if (-not (Test-Path $Repo)) { throw "FOX2 repo missing: $Repo" }

$jobs = @(
    [ordered]@{
        name = "APP_NODE_BOOTSTRAP"
        branch = "work/FOX2-M1-A-APP-BATCH-B"
        path = "docs/agent_handoff/FOX2-M1-A-APP-BATCH-B/bootstrap_node_toolchain.ps1"
        kind = "bootstrap"
    },
    [ordered]@{
        name = "APP_PREFLIGHT"
        branch = "work/FOX2-M1-A-APP-BATCH-B"
        path = "docs/agent_handoff/FOX2-M1-A-APP-BATCH-B/preflight.ps1"
        kind = "preflight"
    },
    [ordered]@{
        name = "BRIDGE_PREFLIGHT"
        branch = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
        path = "docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/preflight.ps1"
        kind = "preflight"
    }
)

$blocked = @()
$infraFailed = @()

foreach ($job in $jobs) {
    Write-Host ""
    Write-Host ("=== " + $job.name + " ===") -ForegroundColor Cyan

    & git -C $Repo fetch origin $job.branch
    if ($LASTEXITCODE -ne 0) {
        $infraFailed += ($job.name + ":FETCH_FAILED")
        continue
    }

    $tmp = Join-Path $env:TEMP ("FOX2-" + $job.name + "-" + [Guid]::NewGuid().ToString("N") + ".ps1")
    try {
        $spec = "origin/" + $job.branch + ":" + $job.path
        $content = (& git -C $Repo show $spec | Out-String)
        if ($LASTEXITCODE -ne 0 -or -not $content) {
            $infraFailed += ($job.name + ":SCRIPT_READ_FAILED")
            continue
        }
        [IO.File]::WriteAllText($tmp,$content,[Text.UTF8Encoding]::new($false))

        & pwsh -NoLogo -NoProfile -File $tmp
        $code = $LASTEXITCODE

        if ($job.kind -eq "preflight" -and $code -eq 20) {
            $blocked += $job.name
            Write-Host ($job.name + " published BLOCKED receipt") -ForegroundColor Yellow
        } elseif ($code -ne 0) {
            $infraFailed += ($job.name + ":EXIT_" + $code)
        }
    }
    finally {
        Remove-Item -Force $tmp -ErrorAction SilentlyContinue
    }
}

Write-Host ""
if ($infraFailed.Count -gt 0) {
    Write-Host ("FOX2_BATCH_B_RECOVERY=INFRA_FAILED " + ($infraFailed -join ",")) -ForegroundColor Red
    exit 30
}
if ($blocked.Count -gt 0) {
    Write-Host ("FOX2_BATCH_B_RECOVERY=BLOCKED_RECEIPTS_PUBLISHED " + ($blocked -join ",")) -ForegroundColor Yellow
    exit 20
}

Write-Host "FOX2_BATCH_B_RECOVERY=PREFLIGHT_PASS" -ForegroundColor Green
exit 0
