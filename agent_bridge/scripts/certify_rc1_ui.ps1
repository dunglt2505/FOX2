param([Parameter(Mandatory)][ValidateSet('inspect','close','exit','check','artifact')][string]$Action, [string]$Artifact)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes
$Condition = [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'FOX2 Bridge RC1')
$Window = [Windows.Automation.AutomationElement]::RootElement.FindFirst([Windows.Automation.TreeScope]::Children, $Condition)
if (-not $Window) { throw 'Installed Desktop window unavailable' }
if ($Action -eq 'close') {
    $Window.GetCurrentPattern([Windows.Automation.WindowPattern]::Pattern).Close()
    'CLOSE_SENT'; exit
}
if ($Action -eq 'artifact') {
    if (-not (Test-Path -LiteralPath $Artifact -PathType Leaf)) { throw 'Explicit test artifact unavailable' }
    $Artifacts = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Artifacts'))
    $Artifacts.GetCurrentPattern([Windows.Automation.SelectionItemPattern]::Pattern).Select()
    $Save = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Save local artifact'))
    $Save.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
    $Deadline = [DateTime]::UtcNow.AddSeconds(10)
    do {
        $Dialog = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Save a local artifact'))
        if (-not $Dialog) { Start-Sleep -Milliseconds 100 }
    } while (-not $Dialog -and [DateTime]::UtcNow -lt $Deadline)
    if (-not $Dialog) { throw 'Explicit file-selection dialog unavailable' }
    $EditCondition = [Windows.Automation.AndCondition]::new(
        [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::ControlTypeProperty, [Windows.Automation.ControlType]::Edit),
        [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'File name:'))
    $Edit = $Dialog.FindFirst([Windows.Automation.TreeScope]::Descendants, $EditCondition)
    if (-not $Edit) { throw 'File selection edit unavailable' }
    # Resolve the chosen directory first. The native picker does not reliably
    # commit a full-path ValuePattern edit and Open in one automation turn.
    $Edit.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue([IO.Path]::GetDirectoryName($Artifact))
    $Open = $Dialog.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::AutomationIdProperty, '1'))
    $Open.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
    Start-Sleep -Milliseconds 400
    $Dialog = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Save a local artifact'))
    if (-not $Dialog) { 'EXPLICIT_ARTIFACT_SELECTED'; exit }
    $Edit = $Dialog.FindFirst([Windows.Automation.TreeScope]::Descendants, $EditCondition)
    $Edit.GetCurrentPattern([Windows.Automation.ValuePattern]::Pattern).SetValue([IO.Path]::GetFileName($Artifact))
    $Open.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
    'EXPLICIT_ARTIFACT_SELECTED'; exit
}
if ($Action -eq 'exit') {
    $Settings = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Settings'))
    $Settings.GetCurrentPattern([Windows.Automation.SelectionItemPattern]::Pattern).Select()
    $Exit = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::AutomationIdProperty, 'GracefulExit'))
    $Exit.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
    'EXIT_INVOKED'; exit
}
$Check = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::AutomationIdProperty, 'CheckNow'))
if (-not $Check) { throw 'Check now automation missing' }
if ($Action -eq 'check') {
    if ($Check.Current.IsEnabled) { throw 'Check now must be disabled while paused' }
    'PAUSED_CHECK_DISABLED'; exit
}
$Names = @('Dashboard','Activity','Agents','Diagnostics','Artifacts','Settings')
$Verified = @()
foreach ($Name in $Names) {
    $Tab = $Window.FindFirst([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, $Name))
    if (-not $Tab) { throw 'Navigation accessibility missing' }
    $Tab.GetCurrentPattern([Windows.Automation.SelectionItemPattern]::Pattern).Select()
    if (-not $Tab.GetCurrentPattern([Windows.Automation.SelectionItemPattern]::Pattern).Current.IsSelected) { throw 'Navigation selection failed' }
    $Verified += $Name
}
@{screens=$Verified;check_now_enabled=$Check.Current.IsEnabled;process_id=$Window.Current.ProcessId}|ConvertTo-Json -Compress
