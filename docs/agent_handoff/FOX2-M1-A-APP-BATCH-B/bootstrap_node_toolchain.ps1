$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

function Resolve-NodeHome {
    $known = Join-Path $env:ProgramFiles "nodejs"
    if (Test-Path (Join-Path $known "node.exe")) { return $known }
    return $null
}

function Test-Toolchain {
    $node = Get-Command node -ErrorAction SilentlyContinue
    $npm = Get-Command npm -ErrorAction SilentlyContinue
    $npx = Get-Command npx -ErrorAction SilentlyContinue
    return ($node -and $npm -and $npx)
}

if (Test-Toolchain) {
    Write-Host "FOX2_NODE_TOOLCHAIN=ALREADY_READY"
    node --version
    npm --version
    npx --version
    exit 0
}

$existingHome = Resolve-NodeHome
if ($existingHome) {
    $env:PATH = $existingHome + [IO.Path]::PathSeparator + $env:PATH
}

if (-not (Test-Toolchain)) {
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "Node/npm/npx missing and winget is unavailable. Install official Node.js LTS, then rerun preflight."
    }

    Write-Host "Installing official Node.js LTS via winget..." -ForegroundColor Cyan
    & $winget.Source install --id OpenJS.NodeJS.LTS --exact --source winget --accept-package-agreements --accept-source-agreements --silent
    $installCode = $LASTEXITCODE

    $nodeHome = Resolve-NodeHome
    if ($nodeHome) {
        $env:PATH = $nodeHome + [IO.Path]::PathSeparator + $env:PATH
    }

    if (-not (Test-Toolchain)) {
        throw "Node.js LTS installation/path refresh failed (winget exit=$installCode). Open a new PowerShell after successful install or repair Node.js LTS."
    }
}

Write-Host "FOX2_NODE_TOOLCHAIN=PASS" -ForegroundColor Green
Write-Host ("NODE=" + ((node --version | Out-String).Trim()))
Write-Host ("NPM=" + ((npm --version | Out-String).Trim()))
Write-Host ("NPX=" + ((npx --version | Out-String).Trim()))
exit 0
