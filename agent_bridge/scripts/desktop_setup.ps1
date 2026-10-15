param([Parameter(Mandatory)][string]$Python)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$Form = [System.Windows.Forms.Form]::new()
$Form.Text = 'Set up FOX2 Bridge'; $Form.Size = [Drawing.Size]::new(600,460)
$Form.StartPosition = 'CenterScreen'
$Text = [System.Windows.Forms.Label]::new()
$Text.Location = [Drawing.Point]::new(24,24); $Text.Size = [Drawing.Size]::new(540,260)
$Text.Text = @"
Confirm these locations and prerequisites:

Runtime: $env:LOCALAPPDATA\FOX2\AgentBridge
Repository: C:\Projects\FOX2
Worktrees: C:\Projects\FOX2-worktrees

Setup checks Git access, Codex sign-in, the FOX2 dispatch branch and
runtime health. Copilot is optional for this Codex route.
Use the official Codex login command if sign-in is needed.

Bridge starts paused. Use Resume in the tray when ready.
Your repositories and worktrees remain outside installer ownership.
"@
$Form.Controls.Add($Text)
$Startup = [System.Windows.Forms.CheckBox]::new()
$Startup.Text = 'Start FOX2 Bridge when I sign in to Windows'
$Startup.Location = [Drawing.Point]::new(24,290); $Startup.Width = 520
$Form.Controls.Add($Startup)
$Finish = [System.Windows.Forms.Button]::new()
$Finish.Text = 'Validate and finish'; $Finish.Width = 180
$Finish.Location = [Drawing.Point]::new(24,340)
$Cancel = [System.Windows.Forms.Button]::new()
$Cancel.Text = 'Cancel'; $Cancel.Location = [Drawing.Point]::new(240,340)
$Form.Controls.AddRange(@($Finish,$Cancel))
$script:Done = $false
$Cancel.add_Click({ $Form.Close() })
$Finish.add_Click({
    try {
        $Finish.Enabled = $false
        $Info = [Diagnostics.ProcessStartInfo]::new($Python)
        $Info.UseShellExecute = $false; $Info.CreateNoWindow = $true
        $Info.RedirectStandardOutput = $true; $Info.RedirectStandardError = $true
        foreach ($Arg in @('-m','fox2_agent_bridge','setup')) { $Info.ArgumentList.Add($Arg) }
        $Process = [Diagnostics.Process]::Start($Info)
        $Output = $Process.StandardOutput.ReadToEnd(); $null = $Process.StandardError.ReadToEnd()
        $Process.WaitForExit()
        if ($Process.ExitCode -ne 0) { throw 'Check Git/PowerShell/Codex availability, Codex sign-in and FOX2 repository access, then retry.' }
        $Result = $Output | ConvertFrom-Json
        if ($Result.status -ne 'SETUP_COMPLETE') { throw 'Setup did not complete.' }
        if ($Startup.Checked) {
            & $Python -m fox2_agent_bridge control set-start-with-windows --enabled true
            if ($LASTEXITCODE -ne 0) { throw 'Startup registration failed. Setup is saved; retry or leave startup disabled.' }
        }
        $Process.Dispose(); $script:Done = $true; $Form.Close()
    } catch {
        [Windows.Forms.MessageBox]::Show($_.Exception.Message,'FOX2 Bridge setup') | Out-Null
        $Finish.Enabled = $true
    }
})
$null = $Form.ShowDialog(); $Form.Dispose()
if (-not $script:Done) { exit 1 }
exit 0
