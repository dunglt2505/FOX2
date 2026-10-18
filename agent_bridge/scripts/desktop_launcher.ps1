param()
$ErrorActionPreference = 'Stop'
$Root = Join-Path $env:LOCALAPPDATA 'FOX2/AgentBridge'
$Current = Get-Content -LiteralPath (Join-Path $Root 'current.json') -Raw | ConvertFrom-Json
if ($Current.package_sha256 -cnotmatch '^[0-9a-f]{64}$') { throw 'Invalid Bridge installation' }
$Version = Join-Path $Root ('versions/' + $Current.package_sha256)
$Python = Join-Path $Version 'runtime/Scripts/python.exe'
$Desktop = Join-Path $Version 'payload/desktop/FOX2.Bridge.Desktop.exe'
foreach ($Path in @($Root, $Version, $Python)) {
    $Item = Get-Item -LiteralPath $Path -ErrorAction Stop
    while ($Item) {
        if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked Bridge installation is not supported' }
        $Item = if ($Item -is [IO.FileInfo]) { $Item.Directory } else { $Item.Parent }
    }
}
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
# Existing configured installations start offline; first-run alone validates auth/remote.
$NeedsSetup = $true
if (Test-Path -LiteralPath (Join-Path $Root 'config/bridge.toml')) {
    $StatusInfo = [Diagnostics.ProcessStartInfo]::new($Python)
    $StatusInfo.UseShellExecute = $false; $StatusInfo.CreateNoWindow = $true
    $StatusInfo.RedirectStandardOutput = $true; $StatusInfo.RedirectStandardError = $true
    foreach ($Argument in @('-I','-m','fox2_agent_bridge','control','status')) { $StatusInfo.ArgumentList.Add($Argument) }
    $Status = [Diagnostics.Process]::Start($StatusInfo)
    try {
        $Out = $Status.StandardOutput.ReadToEndAsync(); $Err = $Status.StandardError.ReadToEndAsync()
        if (-not $Status.WaitForExit(15000)) { $Status.Kill($true); throw 'Bridge status timed out' }
        $Value = $Out.GetAwaiter().GetResult(); $null = $Err.GetAwaiter().GetResult()
        if ($Status.ExitCode -eq 0) { $NeedsSetup = -not ($Value | ConvertFrom-Json).setup_complete }
    } finally { $Status.Dispose() }
}
if ($NeedsSetup) {
    # Setup is bounded and owned by the launcher, never the presentation process.
    $SetupInfo = [Diagnostics.ProcessStartInfo]::new($Python)
    $SetupInfo.UseShellExecute = $false; $SetupInfo.CreateNoWindow = $true
    $SetupInfo.RedirectStandardOutput = $true; $SetupInfo.RedirectStandardError = $true
    foreach ($Argument in @('-I','-m','fox2_agent_bridge','setup')) { $SetupInfo.ArgumentList.Add($Argument) }
    $Setup = [Diagnostics.Process]::Start($SetupInfo)
    try {
        $Out = $Setup.StandardOutput.ReadToEndAsync(); $Err = $Setup.StandardError.ReadToEndAsync()
        if (-not $Setup.WaitForExit(90000)) { $Setup.Kill($true); throw 'Bridge setup timed out' }
        $null = $Out.GetAwaiter().GetResult(); $null = $Err.GetAwaiter().GetResult()
        if ($Setup.ExitCode -ne 0) { throw 'Bridge setup needs configured tools and Codex sign-in' }
    } finally { $Setup.Dispose() }
}
# The fixed helper starts siblings with DEVNULL handles, avoiding inherited caller pipes.
$LaunchInfo = [Diagnostics.ProcessStartInfo]::new($Python)
$LaunchInfo.UseShellExecute = $false; $LaunchInfo.CreateNoWindow = $true
$LaunchInfo.RedirectStandardOutput = $true; $LaunchInfo.RedirectStandardError = $true
foreach ($Argument in @('-I','-m','fox2_agent_bridge.launcher')) { $LaunchInfo.ArgumentList.Add($Argument) }
$Launch = [Diagnostics.Process]::Start($LaunchInfo)
try {
    $Out = $Launch.StandardOutput.ReadToEndAsync(); $Err = $Launch.StandardError.ReadToEndAsync()
    if (-not $Launch.WaitForExit(15000)) { $Launch.Kill($true); throw 'Bridge launch timed out' }
    $null = $Out.GetAwaiter().GetResult(); $null = $Err.GetAwaiter().GetResult()
    if ($Launch.ExitCode -ne 0) { throw 'Bridge launcher unavailable' }
} finally { $Launch.Dispose() }
