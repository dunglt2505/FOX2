param(
    [string]$PublishDirectory = (Join-Path $PSScriptRoot 'artifacts\publish'),
    [switch]$Launch
)

$ErrorActionPreference = 'Stop'
$Source = (Resolve-Path -LiteralPath $PublishDirectory).Path
$Exe = Join-Path $Source 'FOX2.Bridge.Desktop.exe'
if (-not (Test-Path -LiteralPath $Exe -PathType Leaf)) {
    throw 'FOX2.Bridge.Desktop.exe missing from publish directory'
}

$Root = Join-Path $env:LOCALAPPDATA 'FOX2\BridgeDesktop'
$Target = Join-Path $Root 'app'
$Stage = Join-Path $Root ('stage-' + [Guid]::NewGuid().ToString('N'))

New-Item -ItemType Directory -Force -Path $Root | Out-Null
New-Item -ItemType Directory -Path $Stage | Out-Null
Copy-Item -Path (Join-Path $Source '*') -Destination $Stage -Recurse -Force

$Old = Join-Path $Root 'app.previous'
if (Test-Path -LiteralPath $Old) {
    Remove-Item -LiteralPath $Old -Recurse -Force
}
if (Test-Path -LiteralPath $Target) {
    Move-Item -LiteralPath $Target -Destination $Old
}
Move-Item -LiteralPath $Stage -Destination $Target
if (Test-Path -LiteralPath $Old) {
    Remove-Item -LiteralPath $Old -Recurse -Force
}

$InstalledExe = Join-Path $Target 'FOX2.Bridge.Desktop.exe'
$Programs = [Environment]::GetFolderPath('Programs')
$Shortcut = Join-Path $Programs 'FOX2 Bridge.lnk'
$Shell = New-Object -ComObject WScript.Shell
$Link = $Shell.CreateShortcut($Shortcut)
$Link.TargetPath = $InstalledExe
$Link.WorkingDirectory = $Target
$Link.Description = 'FOX2 Bridge Desktop'
$Link.Save()

Write-Host 'FOX2 BRIDGE DESKTOP INSTALL = PASS' -ForegroundColor Green
Write-Host "PATH = $InstalledExe" -ForegroundColor Green

if ($Launch) {
    Start-Process -FilePath $InstalledExe
}
