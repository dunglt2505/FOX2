param()
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$Identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$Mutex = [System.Threading.Mutex]::new($false, ('Local\FOX2BridgeTray-' + $Identity.User.Value))
$Owned = $false
try { $Owned = $Mutex.WaitOne(0) } catch [System.Threading.AbandonedMutexException] { $Owned = $true }
if (-not $Owned) { $Mutex.Dispose(); exit 0 }
$Python = 'C:\Projects\FOX2-AgentBridge\.venv\Scripts\python.exe'
$env:PYTHONPATH = (Resolve-Path (Join-Path $PSScriptRoot '..\src')).Path
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
    # Small fixed control responses, no arbitrary shell or prompt input.
    $Output = $Process.StandardOutput.ReadToEnd()
    $ErrorOutput = $Process.StandardError.ReadToEnd()
    $Process.WaitForExit()
    if ($Process.ExitCode -ne 0) { throw 'Bridge control failed' }
    $Process.Dispose()
    return ($Output | ConvertFrom-Json)
}
$Icon = [System.Windows.Forms.NotifyIcon]::new()
$Timer = [System.Windows.Forms.Timer]::new()
try {
    if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) { throw 'Existing Bridge Python missing' }
    $WorkerInfo = [System.Diagnostics.ProcessStartInfo]::new($Python)
    $WorkerInfo.UseShellExecute = $false; $WorkerInfo.CreateNoWindow = $true
    foreach ($Arg in @('-m','fox2_agent_bridge','worker')) { $WorkerInfo.ArgumentList.Add($Arg) }
    $Worker = [System.Diagnostics.Process]::Start($WorkerInfo)
    $Icon.Icon = [System.Drawing.SystemIcons]::Application
    $Menu = [System.Windows.Forms.ContextMenuStrip]::new()
    $Status = $Menu.Items.Add('Starting'); $Status.Enabled = $false
    $Task = $Menu.Items.Add('Task: none'); $Task.Enabled = $false
    $Last = $Menu.Items.Add('Last result: none'); $Last.Enabled = $false
    $Pause = $Menu.Items.Add('Pause new tasks'); $Pause.add_Click({ try { Invoke-BridgeControl pause | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Resume = $Menu.Items.Add('Resume'); $Resume.add_Click({ try { Invoke-BridgeControl resume | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Check = $Menu.Items.Add('Check now'); $Check.add_Click({ try { Invoke-BridgeControl check-now | Out-Null } catch { $Status.Text = 'Error: control failed' } })
    $Logs = $Menu.Items.Add('Open logs'); $Logs.add_Click({ try { Invoke-BridgeControl open-logs | Out-Null } catch { $Status.Text = 'Error: control failed' } })
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
            $Display = switch ($State.state) {
                'PAUSED' { 'Paused' }
                'DEGRADED' { 'Degraded' }
                'ERROR' { 'Error' }
                'STOPPED' { 'Stopped' }
                'STOPPING' { 'Stopping' }
                default { 'Running' }
            }
            if ($State.heartbeat -and ([DateTimeOffset]::UtcNow - [DateTimeOffset]::Parse($State.heartbeat)).TotalSeconds -gt 60) { $Display = 'Error: stale heartbeat' }
            $Status.Text = $Display + ' / ' + $State.state
            $Icon.Text = ('FOX2 Bridge: ' + $Display)
            $Task.Text = 'Task: ' + $State.current_dispatch
            $Last.Text = 'Last result: ' + $State.last_result.status
            $Startup.Checked = $State.start_with_windows -eq $true
            if ($State.stop_requested -and $State.state -eq 'STOPPED') { [System.Windows.Forms.Application]::Exit() }
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
