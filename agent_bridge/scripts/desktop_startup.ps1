param([Parameter(Mandatory)][ValidateSet('true','false')][string]$Enabled)
$ErrorActionPreference = 'Stop'
$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$TaskName = 'FOX2Bridge-' + $Identity.User.Value
$Existing = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($Enabled -eq 'false') {
    if ($Existing) { Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false }
    exit 0
}
$Pwsh = 'C:\Program Files\PowerShell\7\pwsh.exe'
$Launcher = Join-Path $PSScriptRoot 'desktop_launcher.ps1'
$InstalledLauncher = Join-Path $env:LOCALAPPDATA 'FOX2/AgentBridge/launch.ps1'
if (Test-Path -LiteralPath $InstalledLauncher) { $Launcher = $InstalledLauncher }
$Arguments = '-NoProfile -NonInteractive -WindowStyle Hidden -STA -File "' + $Launcher + '"'
$Action = New-ScheduledTaskAction -Execute $Pwsh -Argument $Arguments
$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $Identity.Name
$Principal = New-ScheduledTaskPrincipal -UserId $Identity.Name -LogonType Interactive -RunLevel Limited
$Settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
# Register -Force replaces only our SID-qualified named task, making enable idempotent.
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force | Out-Null
