param()
$ErrorActionPreference = 'Stop'
$Pwsh = 'C:\Program Files\PowerShell\7\pwsh.exe'
$Tray = Join-Path $PSScriptRoot 'desktop_tray.ps1'
# Background normal entry point. All child processes use hidden windows.
Start-Process -FilePath $Pwsh -ArgumentList @('-NoProfile','-NonInteractive','-WindowStyle','Hidden','-STA','-File',('"' + $Tray + '"')) -WindowStyle Hidden | Out-Null
