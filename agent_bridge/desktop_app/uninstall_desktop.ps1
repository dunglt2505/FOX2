param(
    [switch]$RemoveSettings
)

$ErrorActionPreference = 'Stop'
$Root = Join-Path $env:LOCALAPPDATA 'FOX2\BridgeDesktop'
$Programs = [Environment]::GetFolderPath('Programs')
$Shortcut = Join-Path $Programs 'FOX2 Bridge.lnk'

Get-Process -Name 'FOX2.Bridge.Desktop' -ErrorAction SilentlyContinue |
    Stop-Process -Force -ErrorAction SilentlyContinue

if (Test-Path -LiteralPath $Shortcut) {
    Remove-Item -LiteralPath $Shortcut -Force
}

$App = Join-Path $Root 'app'
if (Test-Path -LiteralPath $App) {
    Remove-Item -LiteralPath $App -Recurse -Force
}

if ($RemoveSettings -and (Test-Path -LiteralPath $Root)) {
    Remove-Item -LiteralPath $Root -Recurse -Force
}

Write-Host 'FOX2 BRIDGE DESKTOP UNINSTALL = PASS' -ForegroundColor Green
Write-Host 'Python Bridge runtime/data were not modified.' -ForegroundColor Green
