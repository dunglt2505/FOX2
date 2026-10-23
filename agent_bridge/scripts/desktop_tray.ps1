param()
$ErrorActionPreference = 'Stop'
# Installed RC1's authoritative WPF surface replaces this legacy primary UI.
if (Test-Path -LiteralPath (Join-Path $PSScriptRoot '../desktop/FOX2.Bridge.Desktop.exe')) {
    & (Join-Path $PSScriptRoot 'desktop_launcher.ps1')
    exit
}
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$Mutex = [System.Threading.Mutex]::new($false, ('Local\FOX2BridgeTray-' + $Identity.User.Value))
$Owned = $false
try { $Owned = $Mutex.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $Owned = $true }
if (-not $Owned) { $Mutex.Dispose(); exit 0 }
$InstalledPython = Join-Path $PSScriptRoot '../../runtime/Scripts/python.exe'
if (Test-Path -LiteralPath $InstalledPython) {
    $Python = (Resolve-Path -LiteralPath $InstalledPython).Path
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
} else {
    $Python = 'D:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe'
    $env:PYTHONPATH = (Resolve-Path (Join-Path $PSScriptRoot '..\src')).Path
}
function Invoke-BridgeControl {
    param([ValidateSet('status','pause','resume','check-now','request-exit','open-logs','set-start-with-windows')][string]$Action,
          [ValidateSet('true','false')][string]$Enabled)
    $Info = [System.Diagnostics.ProcessStartInfo]::new($Python)
    $Info.UseShellExecute = $false
    $Info.CreateNoWindow = $true
    $Info.RedirectStandardOutput = $true
    $Info.RedirectStandardError = $true
    foreach ($Arg in @('-m','fox2_agent_bridge','control',$Action)) { $Info.ArgumentList.Add($Arg) }
    if ($Action -eq 'set-start-with-windows') {
        $Info.ArgumentList.Add('--enabled'); $Info.ArgumentList.Add($Enabled)
    }
    $Process = [System.Diagnostics.Process]::Start($Info)
    try {
        # Drain both pipes concurrently; a stalled control must not freeze the UI.
        $Output = $Process.StandardOutput.ReadToEndAsync()
        $ErrorOutput = $Process.StandardError.ReadToEndAsync()
        if (-not $Process.WaitForExit(10000)) {
            # Only this fixed, short-lived control subprocess is owned here.
            $Process.Kill()
            $Process.WaitForExit(2000) | Out-Null
            throw 'Bridge control timed out'
        }
        if ($Process.ExitCode -ne 0) { throw 'Bridge control failed' }
        return ($Output.GetAwaiter().GetResult() | ConvertFrom-Json)
    } finally { $Process.Dispose() }
}
function Get-BridgeHeartbeatAge {
    param($Heartbeat)
    # ConvertFrom-Json may return DateTime on PowerShell 7. Never reparse its
    # culture-dependent ToString() representation (for example on vi-VN).
    if ($Heartbeat -is [DateTime]) {
        $Stamp = [DateTimeOffset]::new($Heartbeat.ToUniversalTime())
    } elseif ($Heartbeat -is [DateTimeOffset]) {
        $Stamp = $Heartbeat
    } else {
        $Stamp = [DateTimeOffset]::MinValue
        if (-not [DateTimeOffset]::TryParse([string]$Heartbeat,
                [Globalization.CultureInfo]::InvariantCulture,
                [Globalization.DateTimeStyles]::RoundtripKind, [ref]$Stamp)) { return $null }
    }
    return ([DateTimeOffset]::UtcNow - $Stamp).TotalSeconds
}
$Icon = [System.Windows.Forms.NotifyIcon]::new()
$Timer = [System.Windows.Forms.Timer]::new()
try {
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'Existing Bridge Python missing' }
    if ((Test-Path -LiteralPath $InstalledPython) -and -not (Test-Path -LiteralPath (Join-Path $env:LOCALAPPDATA 'FOX2/AgentBridge/config/bridge.toml'))) {
        & (Join-Path $PSScriptRoot 'desktop_setup.ps1') -Python $Python
        if ($LASTEXITCODE -ne 0) { throw 'Setup cancelled or incomplete' }
    }
    if (Test-Path -LiteralPath $InstalledPython) {
        $SetupInfo = [System.Diagnostics.ProcessStartInfo]::new($Python)
        $SetupInfo.UseShellExecute = $false; $SetupInfo.CreateNoWindow = $true
        foreach ($Arg in @('-m','fox2_agent_bridge','setup')) { $SetupInfo.ArgumentList.Add($Arg) }
        $Setup = [System.Diagnostics.Process]::Start($SetupInfo)
        $Setup.WaitForExit()
        if ($Setup.ExitCode -ne 0) {
            [System.Windows.Forms.MessageBox]::Show('Setup needs Git, PowerShell 7, Python and Codex CLI. Configure these tools and sign in to Codex, then reopen FOX2 Bridge.', 'FOX2 Bridge setup') | Out-Null
            throw 'First-run setup failed'
        }
        $Setup.Dispose()
    }
    $WorkerInfo = [System.Diagnostics.ProcessStartInfo]::new($Python)
    $WorkerInfo.UseShellExecute = $false; $WorkerInfo.CreateNoWindow = $true
    foreach ($Arg in @('-m','fox2_agent_bridge','worker')) { $WorkerInfo.ArgumentList.Add($Arg) }
    $Worker = [System.Diagnostics.Process]::Start($WorkerInfo)
    $Icon.Icon = [System.Drawing.SystemIcons]::Application
    $Menu = [System.Windows.Forms.ContextMenuStrip]::new()
    $Status = $Menu.Items.Add('Starting'); $Status.Enabled = $false
    $Task = $Menu.Items.Add('Task: none'); $Task.Enabled = $false
    $Last = $Menu.Items.Add('Last result: none'); $Last.Enabled = $false
    $Model = $Menu.Items.Add('Requested / observed model: unavailable'); $Model.Enabled = $false
    $Permission = $Menu.Items.Add('Permission: unavailable'); $Permission.Enabled = $false
    $Usage = $Menu.Items.Add('Usage: NOT_EXPOSED'); $Usage.Enabled = $false
    $Capacity = $Menu.Items.Add('Capacity: NOT_EXPOSED'); $Capacity.Enabled = $false
    $Pause = $Menu.Items.Add('Pause new tasks'); $Pause.add_Click({ try { Invoke-BridgeControl pause | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Resume = $Menu.Items.Add('Resume'); $Resume.add_Click({ try { Invoke-BridgeControl resume | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Check = $Menu.Items.Add('Check now'); $Check.add_Click({ try { Invoke-BridgeControl check-now | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Logs = $Menu.Items.Add('Open logs'); $Logs.add_Click({ try { Invoke-BridgeControl open-logs | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Support = $Menu.Items.Add('Save support bundle')
    $Support.add_Click({
        $Dialog = [System.Windows.Forms.SaveFileDialog]::new()
        $Dialog.Filter = 'ZIP archive (*.zip)|*.zip'; $Dialog.FileName = 'FOX2-support.zip'
        try {
            if ($Dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
                $Info = [System.Diagnostics.ProcessStartInfo]::new($Python)
                $Info.UseShellExecute = $false; $Info.CreateNoWindow = $true
                foreach ($Arg in @('-m','fox2_agent_bridge','diagnostics','--output',$Dialog.FileName)) { $Info.ArgumentList.Add($Arg) }
                $Process = [System.Diagnostics.Process]::Start($Info); $Process.WaitForExit()
                if ($Process.ExitCode -ne 0) { throw 'Support export failed' }
                $Process.Dispose()
            }
        } catch { $Status.Text = 'Error: support export failed' }
        finally { $Dialog.Dispose() }
    })
    $Startup = $Menu.Items.Add('Start with Windows'); $Startup.CheckOnClick = $false
    $Startup.add_Click({
        try {
            $Desired = if ($Startup.Checked) { 'false' } else { 'true' }
            Invoke-BridgeControl set-start-with-windows -Enabled $Desired | Out-Null
            $Startup.Checked = $Desired -eq 'true'
        } catch { $Status.Text = 'Error: startup registration failed' }
    })
    $Exit = $Menu.Items.Add('Exit (finish current task)')
    $Exit.add_Click({
        try { Invoke-BridgeControl request-exit | Out-Null; $Exit.Enabled = $false; $Status.Text = 'Stopping after current task' }
        catch { $Status.Text = 'Error: exit request failed' }
    })
    $Icon.ContextMenuStrip = $Menu; $Icon.Visible = $true
    $Timer.Interval = 2000
    $Timer.add_Tick({
        try {
            $State = Invoke-BridgeControl status
            # Lifecycle completion must not depend on optional display fields.
            # STOPPED is published before the worker releases its runtime lock;
            # wait for the owned worker process to finish before closing Tray.
            if ($State.stop_requested -and $State.state -eq 'STOPPED' -and $Worker.HasExited) {
                $Timer.Stop()
                [System.Windows.Forms.Application]::ExitThread()
                return
            }
            $Display = switch ($State.state) {
                'PAUSED' { 'Paused' }
                'DEGRADED' { 'Degraded' }
                'ERROR' { 'Error' }
                'STOPPED' { 'Stopped' }
                'STOPPING' { 'Stopping' }
                default { 'Running' }
            }
            if ($State.heartbeat) {
                $Age = Get-BridgeHeartbeatAge $State.heartbeat
                if ($null -eq $Age) { $Display = 'Error: invalid heartbeat' }
                elseif ($Age -gt 60) { $Display = 'Error: stale heartbeat' }
            }
            $Status.Text = $Display + ' / ' + $State.state
            $Icon.Text = ('FOX2 Bridge: ' + $Display)
            $Task.Text = 'Task: ' + $State.current_dispatch
            $Last.Text = 'Last result: ' + $State.last_result.status
            $Execution = $State.execution_display
            $Observed = if ($Execution.metadata.observed_model) { $Execution.metadata.observed_model } else { 'NOT_EXPOSED' }
            $Model.Text = 'Requested / observed model: ' + $Execution.requested.product + ' ' + $Execution.requested.model + ' / ' + $Observed + ' / tier: ' + $Execution.requested.auto_tier + ' / reasoning: ' + $Execution.requested.reasoning_effort
            $Permission.Text = 'Permission requested / applied / observed: ' + $Execution.requested.permission_profile + ' / ' + $Execution.metadata.applied_permission.profile + ' / ' + $Execution.metadata.observed_permission_profile
            $Usage.Text = 'Usage: ' + $(if ($null -ne $Execution.metadata.usage) { $Execution.metadata.usage | ConvertTo-Json -Compress } else { 'NOT_EXPOSED' })
            $Capacity.Text = 'Capacity: ' + $(if ($null -ne $Execution.metadata.capacity) { $Execution.metadata.capacity | ConvertTo-Json -Compress } else { 'NOT_EXPOSED' })
            $Startup.Checked = $State.start_with_windows -eq $true
        } catch { $Status.Text = 'Error: status unavailable'; $Icon.Text = 'FOX2 Bridge: Error' }
    })
    $Timer.Start()
    [System.Windows.Forms.Application]::Run()
} finally {
    $Timer.Stop(); $Timer.Dispose(); $Icon.Visible = $false; $Icon.Dispose()
    if ($Worker) { $Worker.Dispose() }
    if ($Owned) { $Mutex.ReleaseMutex() }
    $Mutex.Dispose()
}
