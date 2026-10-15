$ErrorActionPreference = "Stop"

function Normalize-PathText {
    param([Parameter(Mandatory)][string]$Value)

    try {
        return [IO.Path]::GetFullPath($Value).TrimEnd('\')
    }
    catch {
        return $Value.Trim().Trim('"').TrimEnd('\')
    }
}

$TrayScript   = $env:FOX2_CERT_TRAY_SCRIPT
$WorkerPython = $env:FOX2_CERT_WORKER_PYTHON
$PwshPath     = $env:FOX2_CERT_PWSH

if ([string]::IsNullOrWhiteSpace($TrayScript)) {
    throw "FOX2_CERT_TRAY_SCRIPT required"
}
if ([string]::IsNullOrWhiteSpace($WorkerPython)) {
    throw "FOX2_CERT_WORKER_PYTHON required"
}
if ([string]::IsNullOrWhiteSpace($PwshPath)) {
    $PwshPath = (Get-Process -Id $PID).Path
}

$TrayScript   = Normalize-PathText $TrayScript
$WorkerPython = Normalize-PathText $WorkerPython
$PwshPath     = Normalize-PathText $PwshPath

$Processes = @(Get-CimInstance Win32_Process)

$Trays = @()

foreach ($P in $Processes) {

    if ([int]$P.ProcessId -eq $PID) { continue }

    $Exe = [string]$P.ExecutablePath
    $Cmd = [string]$P.CommandLine

    if ([string]::IsNullOrWhiteSpace($Exe) -or
        [string]::IsNullOrWhiteSpace($Cmd)) {
        continue
    }

    $Exe = Normalize-PathText $Exe

    if (
        $Exe.Equals($PwshPath,[StringComparison]::OrdinalIgnoreCase) -and
        $Cmd.IndexOf($TrayScript,[StringComparison]::OrdinalIgnoreCase) -ge 0
    ) {
        $Trays += [ordered]@{
            kind       = "TRAY"
            pid        = [int]$P.ProcessId
            parent_pid = [int]$P.ParentProcessId
            executable = $Exe
        }
    }
}

$TrayPids = @($Trays | ForEach-Object { [int]$_.pid })

$Workers = @()

foreach ($P in $Processes) {

    if ([int]$P.ProcessId -eq $PID) { continue }

    $Exe = [string]$P.ExecutablePath
    $Cmd = [string]$P.CommandLine

    if ([string]::IsNullOrWhiteSpace($Exe) -or
        [string]::IsNullOrWhiteSpace($Cmd)) {
        continue
    }

    $Exe = Normalize-PathText $Exe

    $ExecutableExact = $Exe.Equals(
        $WorkerPython,
        [StringComparison]::OrdinalIgnoreCase
    )

    $ArgvExact = (
        $Cmd -match
        '(?i)(^|\s)-m(?:\s+|=)fox2_agent_bridge\s+worker(?:\s|$)'
    )

    $ParentIsTray = (
        $TrayPids -contains [int]$P.ParentProcessId
    )

    if ($ExecutableExact -and $ArgvExact -and $ParentIsTray) {

        $Workers += [ordered]@{
            kind             = "WORKER"
            pid              = [int]$P.ProcessId
            parent_pid       = [int]$P.ParentProcessId
            executable       = $Exe
            executable_exact = $true
            argv_exact       = $true
            parent_is_tray   = $true
        }
    }
}

[ordered]@{
    schema       = "FOX2_CERT_PROCESS_OBSERVER_2"
    observer_pid = $PID
    tray_count   = @($Trays).Count
    worker_count = @($Workers).Count
    matches      = @($Trays) + @($Workers)
    target = [ordered]@{
        tray_script   = $TrayScript
        worker_python = $WorkerPython
        pwsh          = $PwshPath
    }
} | ConvertTo-Json -Depth 8 -Compress
