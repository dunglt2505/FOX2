#Requires -Version 7.0
<#
F1 Windows host discovery, READ ONLY. Never an F1 admission/retirement receipt.
No installation, task/service changes, ACL changes, credential reads or files.
Output intentionally excludes command-line arguments and registry values.
An OS administrator must separately validate WDAC/AppLocker coverage, copies,
alternative Python/script entrypoints, service ownership and restart denial.
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not $IsWindows) { throw 'STOP: Windows host required' }

function Probe([scriptblock]$Action) {
    try { return & $Action }
    catch { return $null }
}

$repo = 'C:\Projects\FOX2'
$gitHead = $null
$gitBranch = $null
$gitOriginMatches = $false
$gitDirty = $null
if (Test-Path -LiteralPath (Join-Path $repo '.git')) {
    $gitHead = Probe { (& git -C $repo rev-parse HEAD 2>$null).Trim() }
    $gitBranch = Probe { (& git -C $repo branch --show-current 2>$null).Trim() }
    $origin = Probe { (& git -C $repo remote get-url origin 2>$null).Trim() }
    $gitOriginMatches = [bool]($origin -match '(^|[:/])dunglt2505/FOX2(\.git)?$')
    $gitDirty = Probe { [bool](@(git -C $repo status --porcelain 2>$null).Count) }
}

$services = @(Probe {
    @(Get-CimInstance -ClassName Win32_Service | Where-Object {
        $_.Name -match '(?i)fox2|agentbridge' -or
        $_.DisplayName -match '(?i)fox2|agentbridge' -or
        $_.PathName -match '(?i)fox2|agent_bridge'
    } | ForEach-Object {
        [ordered]@{ name = $_.Name; state = $_.State; start_mode = $_.StartMode }
    })
})
$tasks = @(Probe {
    @(Get-ScheduledTask | Where-Object {
        $task = $_
        $task.TaskName -match '(?i)fox2|agentbridge' -or
        @($task.Actions | Where-Object {
            $_.Execute -match '(?i)fox2|agent_bridge' -or
            $_.Arguments -match '(?i)fox2|agent_bridge'
        }).Count -gt 0
    } | ForEach-Object {
        [ordered]@{ name = $_.TaskName; state = [string]$_.State }
    })
})
$processes = @(Probe {
    @(Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match '(?i)fox2|agentbridge' -or
        $_.ExecutablePath -match '(?i)fox2|agent_bridge'
    } | ForEach-Object {
        [ordered]@{ name = $_.Name; pid = $_.ProcessId }
    })
})
$runKeys = @(
    'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
    'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'
)
$runEntries = @()
foreach ($key in $runKeys) {
    $props = Probe { Get-ItemProperty -LiteralPath $key -ErrorAction Stop }
    if ($null -eq $props) { continue }
    foreach ($name in $props.PSObject.Properties.Name) {
        if ($name -match '^PS') { continue }
        $value = [string]$props.$name
        if ($name -match '(?i)fox2|agentbridge' -or
            $value -match '(?i)fox2|agent_bridge') {
            $runEntries += [ordered]@{ hive = $key.Split(':')[0]; entry_name = $name }
        }
    }
}
$startup = @()
foreach ($folder in @(
    [Environment]::GetFolderPath('Startup'),
    [Environment]::GetFolderPath('CommonStartup')
)) {
    if ($folder -and (Test-Path -LiteralPath $folder)) {
        $startup += @(Get-ChildItem -LiteralPath $folder -File -ErrorAction SilentlyContinue |
            Where-Object Name -Match '(?i)fox2|agentbridge' |
            Select-Object -ExpandProperty Name)
    }
}
$deviceGuard = Probe {
    $x = Get-CimInstance -Namespace 'root\Microsoft\Windows\DeviceGuard' -ClassName Win32_DeviceGuard -ErrorAction Stop
    [ordered]@{
        user_mode_code_integrity_enforcement = $x.UsermodeCodeIntegrityPolicyEnforcementStatus
        code_integrity_enforcement = $x.CodeIntegrityPolicyEnforcementStatus
    }
}
$appLocker = Probe {
    if (Get-Command Get-AppLockerPolicy -ErrorAction SilentlyContinue) {
        $x = Get-AppLockerPolicy -Effective -ErrorAction Stop
        if ($null -ne $x) { return 'POLICY_RETURNED_COVERAGE_NOT_VERIFIED' }
    }
    return 'NOT_VERIFIED'
}
$bridgeRoot = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$out = [ordered]@{
    schema = 'FOX2_F1_HOST_DISCOVERY_READ_ONLY_V1'
    source = 'LOCAL_HOST_DIAGNOSTIC_NOT_TRUST_ANCHOR'
    git = [ordered]@{
        expected_repo = 'dunglt2505/FOX2'
        origin_matches = $gitOriginMatches
        local_head = $gitHead
        local_branch = $gitBranch
        dirty = $gitDirty
    }
    installed_bridge_root_exists = Test-Path -LiteralPath $bridgeRoot
    service_candidates = $services
    task_candidates = $tasks
    process_candidates = $processes
    run_entry_candidates = $runEntries
    startup_name_candidates = $startup
    device_guard_observation = $deviceGuard
    app_locker_observation = $appLocker
    all_legacy_entrypoints_enumerated = $false
    durable_legacy_retirement_verified = $false
    privileged_broker_verified = $false
    positive_claim_authority = 'DENY'
    canary = 'HOLD'
}
$out | ConvertTo-Json -Depth 8
