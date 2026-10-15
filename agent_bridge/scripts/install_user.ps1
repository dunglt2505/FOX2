param(
    [Parameter(Mandatory)][string]$Package,
    [Parameter(Mandatory)][ValidatePattern('^[0-9A-Fa-f]{64}$')][string]$Sha256,
    [string]$Python = 'python'
)
$ErrorActionPreference = 'Stop'
# Existing Python 3.13 is a declared prerequisite; no elevated/host installs.
if ((Get-FileHash -LiteralPath $Package -Algorithm SHA256).Hash -ne $Sha256) { throw 'Package integrity mismatch' }
$Bootstrap = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-install-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $Bootstrap | Out-Null
try {
    Expand-Archive -LiteralPath $Package -DestinationPath $Bootstrap
    $Wheel = @(Get-ChildItem -LiteralPath (Join-Path $Bootstrap 'wheels') -Filter 'fox2_agent_bridge-*.whl')
    if ($Wheel.Count -ne 1) { throw 'Expected one Bridge wheel' }
    # Import the installer directly from the verified wheel. Runtime installation is offline.
    $env:FOX2_INSTALL_WHEEL = $Wheel[0].FullName
    $env:FOX2_INSTALL_PACKAGE = (Resolve-Path -LiteralPath $Package).Path
    $env:FOX2_INSTALL_SHA = $Sha256
    & $Python -I -c 'import os,sys; sys.path.insert(0,os.environ["FOX2_INSTALL_WHEEL"]); from pathlib import Path; from fox2_agent_bridge.installation import install; print(install(Path(os.environ["FOX2_INSTALL_PACKAGE"]),os.environ["FOX2_INSTALL_SHA"]))'
    if ($LASTEXITCODE -ne 0) { throw 'Bridge installation stopped' }
} finally {
    Remove-Item Env:FOX2_INSTALL_WHEEL,Env:FOX2_INSTALL_PACKAGE,Env:FOX2_INSTALL_SHA -ErrorAction SilentlyContinue
    $Resolved = [IO.Path]::GetFullPath($Bootstrap)
    $TempRoot = [IO.Path]::GetFullPath([IO.Path]::GetTempPath())
    if (-not $Resolved.StartsWith($TempRoot, [StringComparison]::OrdinalIgnoreCase)) { throw 'Unsafe cleanup path' }
    Remove-Item -LiteralPath $Resolved -Recurse -Force
}
