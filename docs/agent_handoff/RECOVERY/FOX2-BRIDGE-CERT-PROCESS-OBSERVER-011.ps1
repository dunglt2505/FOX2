$ErrorActionPreference = "Stop"

function Normalize-PathText {
    param([Parameter(Mandatory)][string]$Value)
    try {
        return [System.IO.Path]::GetFullPath($Value).TrimEnd('\')
    } catch {
        return $Value.Trim().Trim('"').TrimEnd('\')
    }
}

$TrayScript = $env:FOX2_CERT_TRAY_SCRIPT
$WorkerPython = $env:FOX2_CERT_WORKER_PYTHON
$PwshPath = $env:FOX2_CERT_PWSH

if ([string]::IsNullOrWhiteSpace($TrayScript)) {
    throw "FOX2_CERT_TRAY_SCRIPT is required"
}
if ([string]::IsNullOrWhiteSpace($WorkerPython)) {
    throw "FOX2_CERT_WORKER_PYTHON is required"
}
if ([string]::IsNullOrWhiteSpace($PwshPath)) {
    $PwshPath = (Get-Process -Id $PID).Path
}

$TrayScript = Normalize-PathText $TrayScript
$WorkerPython = Normalize-PathText $WorkerPython
$PwshPath = Normalize-PathText $PwshPath

$Matches = @()

foreach ($Process in @(Get-CimInstance Win32_Process)) {
    $ProcessId = [int]$Process.ProcessId

    # Never classify this observer itself as Tray/Worker.
    if ($ProcessId -eq $PID) {
        continue
    }

    $Executable = [string]$Process.ExecutablePath
    $CommandLine = [string]$Process.CommandLine

    if ([string]::IsNullOrWhiteSpace($Executable) -or
        [string]::IsNullOrWhiteSpace($CommandLine)) {
        continue
    }

    $Executable = Normalize-PathText $Executable
    $Kind = $null

    # Tray must be the expected pwsh binary AND explicitly execute the exact
    # installed desktop_tray.ps1. Target values come from environment variables,
    # so the observer's own command line never contains the target literal.
    if ($Executable.Equals($PwshPath, [StringComparison]::OrdinalIgnoreCase) -and
        $CommandLine.IndexOf($TrayScript, [StringComparison]::OrdinalIgnoreCase) -ge 0) {
        $Kind = "TRAY"
    }

    # Worker must be the exact installed Python AND run the Bridge worker module.
    if ($Executable.Equals($WorkerPython, [StringComparison]::OrdinalIgnoreCase) -and
        $CommandLine -match '(?i)(^|\s)-m(\s+|=)fox2_agent_bridge(\s+|$).*?(\s|^)worker(\s|$)') {
        $Kind = "WORKER"
    }

    if ($null -ne $Kind) {
        $Matches += [ordered]@{
            kind = $Kind
            pid = $ProcessId
            parent_pid = [int]$Process.ParentProcessId
            executable = $Executable
        }
    }
}

$Tray = @($Matches | Where-Object { $_.kind -eq "TRAY" })
$Worker = @($Matches | Where-Object { $_.kind -eq "WORKER" })

$Result = [ordered]@{
    schema = "FOX2_CERT_PROCESS_OBSERVER_1"
    observer_pid = $PID
    tray_count = $Tray.Count
    worker_count = $Worker.Count
    matches = @($Matches)
    target = [ordered]@{
        tray_script = $TrayScript
        worker_python = $WorkerPython
        pwsh = $PwshPath
    }
}

$Result | ConvertTo-Json -Depth 6 -Compress
