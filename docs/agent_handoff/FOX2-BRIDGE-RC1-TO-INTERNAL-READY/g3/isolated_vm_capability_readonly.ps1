#requires -Version 7.0
# FOX2 G3 — READ-ONLY disposable-VM capability inventory.
# Do not run G3 mutations based solely on this result.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$OS = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
$Machine = Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction Stop
$Principal = [Security.Principal.WindowsPrincipal]::new(
    [Security.Principal.WindowsIdentity]::GetCurrent())
$Admin = $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$VmName = ([string]$Machine.Manufacturer + ' ' + [string]$Machine.Model)
$VmIndicator = $VmName -match '(?i)(virtual machine|vmware|virtualbox|kvm|qemu|parallels|hyper-v|hypervisor|xen)'
$NonDomain = -not [bool]$Machine.PartOfDomain
$OsCandidate = ([int]$OS.BuildNumber -ge 22000) -and
    ([string]$OS.Caption -match '(?i)windows 11') -and
    ([string]$OS.Caption -match '(?i)pro|enterprise|education')
$AppId = Get-Service -Name AppIDSvc -ErrorAction SilentlyContinue
$Existing = Get-Service -Name FOX2F1Authority -ErrorAction SilentlyContinue
$NativePS = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$AppLocker = 'NOT_VERIFIED'
$PolicyRead = 'NOT_VERIFIED'
if (Test-Path -LiteralPath $NativePS -PathType Leaf) {
    $Code = @'
$ErrorActionPreference = 'Stop'
Import-Module AppLocker -ErrorAction Stop
$null = Get-Command Get-AppLockerPolicy -ErrorAction Stop
Write-Output 'MODULE_OK'
$effective = Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop
$local = Get-AppLockerPolicy -Local -Xml -ErrorAction Stop
if ([string]::IsNullOrWhiteSpace($effective) -or
    [string]::IsNullOrWhiteSpace($local)) {
    throw 'Policy query returned empty result'
}
Write-Output 'POLICY_QUERY_OK'
'@
    $Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($Code))
    $Messages = @(& $NativePS -NoProfile -NonInteractive -EncodedCommand $Encoded 2>$null)
    $Exit = $LASTEXITCODE
    if ($Messages -contains 'MODULE_OK') { $AppLocker = 'AVAILABLE_NATIVE_5_1' }
    if ($Exit -eq 0 -and $Messages -contains 'POLICY_QUERY_OK') {
        $PolicyRead = 'PASS_READONLY'
    } else {
        $PolicyRead = 'FAILED_OR_UNAVAILABLE'
    }
}
$Blockers = @()
if (-not $VmIndicator) { $Blockers += 'VM_NOT_OBSERVED' }
if (-not $NonDomain) { $Blockers += 'DOMAIN_JOINED' }
if (-not $Admin) { $Blockers += 'ELEVATED_ADMIN_NOT_OBSERVED' }
if (-not $OsCandidate) { $Blockers += 'WINDOWS_OS_EDITION_NOT_CONFIRMED' }
if ($AppLocker -ne 'AVAILABLE_NATIVE_5_1') { $Blockers += 'APPLOCKER_MODULE_NOT_VERIFIED' }
if ($PolicyRead -ne 'PASS_READONLY') { $Blockers += 'APPLOCKER_POLICY_QUERY_NOT_VERIFIED' }
if ($null -eq $AppId) { $Blockers += 'APPIDSVC_NOT_PRESENT' }
if ($null -ne $Existing) { $Blockers += 'EXISTING_F1_SERVICE_RECONCILE' }

[ordered]@{
    schema = 'FOX2_G3_VM_CAPABILITY_READONLY_V1'
    read_only = $true
    g3_execution_authorized_by_this_probe = $false
    observed_utc = [DateTime]::UtcNow.ToString('o')
    vm_hardware_indicator = [bool]$VmIndicator
    non_domain = [bool]$NonDomain
    disposable_vm_isolation_attested = $false
    elevated_admin = [bool]$Admin
    os_candidate = [bool]$OsCandidate
    native_windows_powershell_5_1 = (Test-Path -LiteralPath $NativePS -PathType Leaf)
    applocker_module = $AppLocker
    applocker_policy_query = $PolicyRead
    appidsvc_present = ($null -ne $AppId)
    existing_f1_service = ($null -ne $Existing)
    technical_capability_blockers = $Blockers
    g3_preexec_status = 'NOT_RUN_ON_THIS_TARGET'
    f1_positive_runtime = 'NOT_RUN'
    g4_daily_host_adoption = 'NOT_AUTHORIZED'
} | ConvertTo-Json -Depth 4
