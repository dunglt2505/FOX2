param(
    [string]$Configuration = 'Release'
)

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Solution = Join-Path $Root 'FOX2.Bridge.Desktop.sln'
$DesktopProject = Join-Path $Root 'FOX2.Bridge.Desktop\FOX2.Bridge.Desktop.csproj'
$SmokeProject = Join-Path $Root 'FOX2.Bridge.Desktop.Smoke\FOX2.Bridge.Desktop.Smoke.csproj'
$Artifacts = Join-Path $Root 'artifacts'
$Publish = Join-Path $Artifacts 'publish'

Push-Location $Root
try {
    $Sdk = (& dotnet --version).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $Sdk.StartsWith('8.')) {
        throw "FOX2 Desktop requires an available .NET 8 SDK selected by global.json. Observed: $Sdk"
    }

    if (Test-Path -LiteralPath $Artifacts) {
        Remove-Item -LiteralPath $Artifacts -Recurse -Force
    }
    New-Item -ItemType Directory -Path $Artifacts | Out-Null

    & dotnet restore $Solution
    if ($LASTEXITCODE -ne 0) { throw 'dotnet restore failed' }

    & dotnet build $Solution -c $Configuration --no-restore
    if ($LASTEXITCODE -ne 0) { throw 'dotnet build failed' }

    & dotnet run --project $SmokeProject -c $Configuration --no-build
    if ($LASTEXITCODE -ne 0) { throw 'desktop smoke harness failed' }

    & dotnet restore $DesktopProject -r win-x64
    if ($LASTEXITCODE -ne 0) { throw 'win-x64 publish restore failed' }

    & dotnet publish $DesktopProject -c $Configuration -r win-x64 --self-contained false --no-restore -o $Publish
    if ($LASTEXITCODE -ne 0) { throw 'dotnet publish failed' }

    $Exe = Join-Path $Publish 'FOX2.Bridge.Desktop.exe'
    if (-not (Test-Path -LiteralPath $Exe -PathType Leaf)) {
        throw 'published FOX2.Bridge.Desktop.exe missing'
    }

    $Hash = (Get-FileHash -LiteralPath $Exe -Algorithm SHA256).Hash.ToLowerInvariant()

    [ordered]@{
        status = 'PASS'
        sdk = $Sdk
        configuration = $Configuration
        smoke = 'PASS'
        publish_directory = $Publish
        executable = $Exe
        executable_sha256 = $Hash
    } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Artifacts 'build-result.json') -Encoding utf8NoBOM

    Write-Host ''
    Write-Host 'FOX2 BRIDGE DESKTOP BUILD = PASS' -ForegroundColor Green
    Write-Host "SDK = $Sdk" -ForegroundColor Green
    Write-Host "EXE SHA256 = $Hash" -ForegroundColor Green
    Write-Host "PUBLISH = $Publish" -ForegroundColor Green
}
finally {
    Pop-Location
}
