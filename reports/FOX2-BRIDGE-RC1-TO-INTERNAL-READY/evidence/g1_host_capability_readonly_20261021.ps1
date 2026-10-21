#Requires -Version 7.0
<#
FOX2 F1 G1 narrow Windows capability probe.
READ ONLY. Prints redacted JSON to stdout only.
Does NOT install/change AppLocker/App Control, services, tasks, ACLs, registry,
Bridge runtime, SQLite, processes or files. No usernames/SIDs/rule bodies/command lines.
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not $IsWindows) { throw 'STOP: Windows host required' }

$failed = [System.Collections.Generic.List[string]]::new()
function Probe([string]$Name, [scriptblock]$Action) {
    try { return & $Action }
    catch { $failed.Add($Name) | Out-Null; return $null }
}

$os = Probe 'os' {
    $x = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
    [ordered]@{
        caption = [string]$x.Caption
        version = [string]$x.Version
        build_number = [string]$x.BuildNumber
        architecture = [string]$x.OSArchitecture
        product_type = [int]$x.ProductType
    }
}

$currentVersion = Probe 'current_version' {
    $x = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion' -ErrorAction Stop
    [ordered]@{
        product_name = [string]$x.ProductName
        edition_id = [string]$x.EditionID
        display_version = [string]$x.DisplayVersion
        current_build = [string]$x.CurrentBuildNumber
        ubr = if ($null -ne $x.UBR) { [int]$x.UBR } else { $null }
    }
}

$currentTokenIsAdmin = Probe 'admin_boolean' {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($id)
    [bool]$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

$secureBoot = Probe 'secure_boot' {
    [bool](Confirm-SecureBootUEFI -ErrorAction Stop)
}

$scmReadable = Probe 'scm_read' {
    $null = Get-CimInstance -ClassName Win32_Service -Filter "Name='AppIDSvc'" -ErrorAction Stop
    $true
}
if ($null -eq $scmReadable) { $scmReadable = $false }

$appIdSvc = Probe 'appid_service' {
    $s = Get-CimInstance -ClassName Win32_Service -Filter "Name='AppIDSvc'" -ErrorAction Stop
    if ($null -eq $s) {
        [ordered]@{ present = $false; state = $null; start_mode = $null }
    } else {
        [ordered]@{ present = $true; state = [string]$s.State; start_mode = [string]$s.StartMode }
    }
}

$deviceGuard = Probe 'device_guard' {
    $x = Get-CimInstance -Namespace 'root\Microsoft\Windows\DeviceGuard' -ClassName Win32_DeviceGuard -ErrorAction Stop
    [ordered]@{
        code_integrity_enforcement = if ($null -ne $x.CodeIntegrityPolicyEnforcementStatus) { [int]$x.CodeIntegrityPolicyEnforcementStatus } else { $null }
        user_mode_code_integrity_enforcement = if ($null -ne $x.UsermodeCodeIntegrityPolicyEnforcementStatus) { [int]$x.UsermodeCodeIntegrityPolicyEnforcementStatus } else { $null }
        virtualization_based_security_status = if ($null -ne $x.VirtualizationBasedSecurityStatus) { [int]$x.VirtualizationBasedSecurityStatus } else { $null }
    }
}

$appLockerCommand = Get-Command Get-AppLockerPolicy -ErrorAction SilentlyContinue
$appLocker = [ordered]@{
    cmdlet_available = [bool]($null -ne $appLockerCommand)
    effective_policy_returned = $false
    collections = @()
}
if ($null -ne $appLockerCommand) {
    $policy = Probe 'applocker_effective' { Get-AppLockerPolicy -Effective -ErrorAction Stop }
    if ($null -ne $policy) {
        $appLocker.effective_policy_returned = $true
        $collections = @()
        foreach ($c in @($policy.RuleCollections)) {
            if ($null -eq $c) { continue }
            $collectionType = $c.PSObject.Properties['CollectionType']
            $enforcementMode = $c.PSObject.Properties['EnforcementMode']
            $collections += [ordered]@{
                collection_type = if ($null -ne $collectionType) { [string]$collectionType.Value } else { 'UNKNOWN' }
                enforcement_mode = if ($null -ne $enforcementMode) { [string]$enforcementMode.Value } else { 'UNKNOWN' }
            }
        }
        $appLocker.collections = $collections
    }
}

$ciTool = Get-Command CiTool.exe -ErrorAction SilentlyContinue
$ciToolAvailable = [bool]($null -ne $ciTool)

$out = [ordered]@{
    schema = 'FOX2_F1_G1_HOST_CAPABILITY_READ_ONLY_V1'
    design_source_sha = 'f15f8efba214d0f5a3ca51304ff5127d293356cc'
    mode = 'READ_ONLY_NO_BRIDGE_EXECUTION_NO_POLICY_CHANGE'
    os = $os
    windows_current_version = $currentVersion
    current_token_is_admin = $currentTokenIsAdmin
    scm_readable = [bool]$scmReadable
    secure_boot = $secureBoot
    device_guard = $deviceGuard
    app_locker = $appLocker
    application_identity_service = $appIdSvc
    citool_available = $ciToolAvailable
    policy_issuer_independence = 'NOT_ATTESTED_BY_LOCAL_READONLY_PROBE'
    durable_legacy_retirement_verified = $false
    privileged_f1_service_verified = $false
    positive_claim_authority = 'DENY'
    canary = 'HOLD'
    failed_probes = @($failed)
}
$out | ConvertTo-Json -Depth 8
