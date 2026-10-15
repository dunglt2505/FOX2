"""Execute the production PowerShell callbacks with real WinForms and pipes."""
import os
from pathlib import Path
import subprocess
import sys

import pytest


TRAY = Path(__file__).parents[1] / 'scripts/desktop_tray.ps1'
LOAD = r'''
$ErrorActionPreference='Stop'
$Tokens=$null; $Errors=$null
$Ast=[System.Management.Automation.Language.Parser]::ParseFile($env:FOX2_TEST_TRAY,[ref]$Tokens,[ref]$Errors)
if ($Errors.Count) { throw 'Tray parse error' }
foreach ($Function in $Ast.FindAll({param($n) $n -is [System.Management.Automation.Language.FunctionDefinitionAst]},$true)) {
    . ([scriptblock]::Create($Function.Extent.Text))
}
'''


def run_ps(tmp_path, body, **env):
    script = tmp_path / 'harness.ps1'
    script.write_text(LOAD + body, encoding='utf-8')
    return subprocess.run(
        ['pwsh', '-NoProfile', '-NonInteractive', '-STA', '-File', str(script)],
        capture_output=True, text=True, timeout=25,
        env={**os.environ, 'FOX2_TEST_TRAY': str(TRAY), **env},
    )


def test_heartbeat_json_datetime_and_strings_across_cultures(tmp_path):
    result = run_ps(tmp_path, r'''
foreach ($Culture in 'vi-VN','en-US','en-GB') {
    [Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::new($Culture)
    $Now=[DateTimeOffset]::UtcNow
    $Json='{"heartbeat":"'+$Now.ToString('o')+'"}'
    $Values=@(($Json | ConvertFrom-Json).heartbeat, $Now, $Now.UtcDateTime, $Now.ToString('o'))
    foreach ($Value in $Values) {
        $Age=Get-BridgeHeartbeatAge $Value
        if ($null -eq $Age -or [Math]::Abs($Age) -gt 10) { throw 'heartbeat age drift' }
    }
    if ((Get-BridgeHeartbeatAge $Now.AddMinutes(-2)) -lt 60) { throw 'stale not detected' }
    if ($null -ne (Get-BridgeHeartbeatAge 'invalid')) { throw 'invalid accepted' }
}
'HEARTBEAT_PASS'
''')
    assert result.returncode == 0, result.stderr
    assert 'HEARTBEAT_PASS' in result.stdout


def test_timer_waits_for_worker_and_exits_despite_invalid_display(tmp_path):
    result = run_ps(tmp_path, r'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Threading.Thread]::CurrentThread.CurrentCulture=[Globalization.CultureInfo]::new('vi-VN')
$script:Calls=0
$Worker=[pscustomobject]@{HasExited=$false}
function Invoke-BridgeControl {
    $script:Calls++
    $Worker.HasExited=$script:Calls -ge 3
    return [pscustomobject]@{state='STOPPED';stop_requested=$true;heartbeat='invalid'}
}
$Status=[System.Windows.Forms.ToolStripMenuItem]::new()
$Task=[System.Windows.Forms.ToolStripMenuItem]::new()
$Last=[System.Windows.Forms.ToolStripMenuItem]::new()
$Model=[System.Windows.Forms.ToolStripMenuItem]::new()
$Permission=[System.Windows.Forms.ToolStripMenuItem]::new()
$Usage=[System.Windows.Forms.ToolStripMenuItem]::new()
$Capacity=[System.Windows.Forms.ToolStripMenuItem]::new()
$Startup=[System.Windows.Forms.ToolStripMenuItem]::new()
$Icon=[System.Windows.Forms.NotifyIcon]::new()
$Timer=[System.Windows.Forms.Timer]::new(); $Timer.Interval=50
$Tick=$Ast.Find({param($n) $n -is [System.Management.Automation.Language.InvokeMemberExpressionAst] -and $n.Member.Value -eq 'add_Tick'},$true)
$Timer.add_Tick($Tick.Arguments[0].ScriptBlock.GetScriptBlock())
$Guard=[System.Windows.Forms.Timer]::new(); $Guard.Interval=4000
$Guard.add_Tick({$script:TimedOut=$true; [System.Windows.Forms.Application]::ExitThread()})
try {
    $Timer.Start(); $Guard.Start()
    [System.Windows.Forms.Application]::Run()
    if ($script:TimedOut -or $script:Calls -ne 3) { throw 'shutdown missed or exited before worker' }
    'TIMER_PASS'
} finally { $Timer.Dispose(); $Guard.Dispose(); $Icon.Dispose() }
''')
    assert result.returncode == 0, result.stderr
    assert 'TIMER_PASS' in result.stdout


@pytest.mark.parametrize('mode', ['pipes', 'nonzero', 'timeout'])
def test_control_process_drains_bounds_and_disposes(tmp_path, mode):
    package = tmp_path / 'fox2_agent_bridge'
    package.mkdir()
    (package / '__init__.py').write_text('')
    (package / '__main__.py').write_text(
        "import os,sys,time\n"
        "mode=os.environ['FOX2_TEST_MODE']\n"
        "if mode=='timeout': time.sleep(60)\n"
        "elif mode=='nonzero': sys.exit(7)\n"
        "else:\n sys.stderr.write('x'*200000); sys.stderr.flush()\n"
        " sys.stdout.write('{\"state\":\"STOPPED\"}'); sys.stdout.flush()\n"
    )
    result = run_ps(tmp_path, r'''
$Python=$env:FOX2_TEST_PYTHON
$Watch=[Diagnostics.Stopwatch]::StartNew()
try {
    $Value=Invoke-BridgeControl status
    if ($env:FOX2_TEST_MODE -ne 'pipes' -or $Value.state -ne 'STOPPED') { throw 'unexpected result' }
} catch {
    if ($env:FOX2_TEST_MODE -eq 'pipes') { throw }
    $Expected=if ($env:FOX2_TEST_MODE -eq 'timeout') {'Bridge control timed out'} else {'Bridge control failed'}
    if ($_.Exception.Message -ne $Expected) { throw }
}
if ($Watch.Elapsed.TotalSeconds -gt 15) { throw 'control exceeded bound' }
'CONTROL_PASS'
''', FOX2_TEST_PYTHON=sys.executable, FOX2_TEST_MODE=mode, PYTHONPATH=str(tmp_path))
    assert result.returncode == 0, result.stderr
    assert 'CONTROL_PASS' in result.stdout
