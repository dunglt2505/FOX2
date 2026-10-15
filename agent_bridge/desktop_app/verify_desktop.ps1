param(
    [string]$InstalledDirectory = (Join-Path $env:LOCALAPPDATA 'FOX2\BridgeDesktop\app')
)

$ErrorActionPreference = 'Stop'
$Exe = Join-Path $InstalledDirectory 'FOX2.Bridge.Desktop.exe'
if (-not (Test-Path -LiteralPath $Exe -PathType Leaf)) {
    throw 'Installed FOX2.Bridge.Desktop.exe missing'
}

$BridgeRoot = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$CurrentPath = Join-Path $BridgeRoot 'current.json'
if (-not (Test-Path -LiteralPath $CurrentPath -PathType Leaf)) {
    throw 'Bridge current.json missing'
}

$Current = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
$Python = Join-Path $BridgeRoot "versions\$($Current.package_sha256)\runtime\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw 'Installed Bridge Python missing'
}

$Before = (& $Python -m fox2_agent_bridge control status | Out-String) | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
    throw 'Cannot read Bridge status before Desktop launch'
}

$Process = Start-Process -FilePath $Exe -PassThru
try {
    Start-Sleep -Seconds 4
    if ($Process.HasExited) {
        throw "Desktop App exited during smoke launch with code $($Process.ExitCode)"
    }

    $After = (& $Python -m fox2_agent_bridge control status | Out-String) | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0) {
        throw 'Cannot read Bridge status after Desktop launch'
    }

    foreach ($Field in @('paused','stop_requested','check_generation')) {
        if ($Before.$Field -ne $After.$Field) {
            throw "Desktop launch unexpectedly changed Bridge control field: $Field"
        }
    }

    Write-Host 'FOX2 BRIDGE DESKTOP RUNTIME SMOKE = PASS' -ForegroundColor Green
    Write-Host "Worker state = $($After.state)" -ForegroundColor Green
    Write-Host "Paused = $($After.paused)" -ForegroundColor Green
}
finally {
    if (-not $Process.HasExited) {
        Stop-Process -Id $Process.Id -Force -ErrorAction SilentlyContinue
    }
}
