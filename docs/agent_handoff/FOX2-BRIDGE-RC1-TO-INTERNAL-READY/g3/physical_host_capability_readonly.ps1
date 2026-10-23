#requires -Version 7.0
# FOX2 G3 — PHYSICAL WINDOWS HOST: read-only capability inventory.
# This does NOT authorize G3 AppLocker/SCM/Service changes or F1 positive claims.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Os = Get-CimInstance -ClassName Win32_OperatingSystem -ErrorAction Stop
$Computer = Get-CimInstance -ClassName Win32_ComputerSystem -ErrorAction Stop
$Identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$Principal = [Security.Principal.WindowsPrincipal]::new($Identity)
$Elevated = $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

$Hardware = ([string]$Computer.Manufacturer + ' ' + [string]$Computer.Model)
$LooksVirtual = [bool]($Hardware -match '(?i)(virtual machine|vmware|virtualbox|kvm|qemu|parallels|hyper-v|hypervisor|xen)')
$OsCandidate = [bool](([int]$Os.BuildNumber -ge 22000) -and
    ([string]$Os.Caption -match '(?i)Windows 11') -and
    ([string]$Os.Caption -match '(?i)Pro|Enterprise|Education'))

$AppId = Get-Service -Name AppIDSvc -ErrorAction SilentlyContinue
$F1 = Get-Service -Name FOX2F1Authority -ErrorAction SilentlyContinue
$AuthorityRoot = Join-Path $env:ProgramData 'FOX2\F1Authority'
$NativePS = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$Module = 'NOT_VERIFIED'
$PolicyQuery = 'NOT_VERIFIED'
$EffectiveDigest = $null
$LocalDigest = $null

if (Test-Path -LiteralPath $NativePS -PathType Leaf) {
    $NativeCode = @'
$ErrorActionPreference='Stop'
try {
    Import-Module AppLocker -ErrorAction Stop
    $moduleOk = $null -ne (Get-Command Get-AppLockerPolicy -ErrorAction Stop)
    $effective = [string](Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop)
    $local = [string](Get-AppLockerPolicy -Local -Xml -ErrorAction Stop)
    $available = (-not [string]::IsNullOrWhiteSpace($effective)) -and
                 (-not [string]::IsNullOrWhiteSpace($local))
    $sha = [Security.Cryptography.SHA256]::Create()
    try {
        $effDigest = if ($available) {
            [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($effective))).Replace('-','').ToLowerInvariant()
        } else { $null }
        $localDigest = if ($available) {
            [BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($local))).Replace('-','').ToLowerInvariant()
        } else { $null }
    } finally { $sha.Dispose() }
    @{ module=$moduleOk; policy_query=$available; effective_sha256=$effDigest;
       local_sha256=$localDigest } | ConvertTo-Json -Compress
} catch {
    @{ module=$false; policy_query=$false; effective_sha256=$null;
       local_sha256=$null } | ConvertTo-Json -Compress
}
'@
    $Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($NativeCode))
    try {
        $Raw = @(& $NativePS -NoProfile -NonInteractive -EncodedCommand $Encoded 2>$null)
        if ($LASTEXITCODE -eq 0 -and $Raw.Count -ge 1) {
            $Value = ($Raw -join [Environment]::NewLine) | ConvertFrom-Json
            $Module = if ($Value.module -eq $true) { 'AVAILABLE_NATIVE_PS51' } else { 'FAILED_OR_UNAVAILABLE' }
            $PolicyQuery = if ($Value.policy_query -eq $true) { 'PASS_READONLY' } else { 'FAILED_OR_UNAVAILABLE' }
            $EffectiveDigest = $Value.effective_sha256
            $LocalDigest = $Value.local_sha256
        } else {
            $Module = 'FAILED_OR_UNAVAILABLE'
            $PolicyQuery = 'FAILED_OR_UNAVAILABLE'
        }
    } catch {
        $Module = 'FAILED_OR_UNAVAILABLE'
        $PolicyQuery = 'FAILED_OR_UNAVAILABLE'
    }
}
$Gaps = @()
if ($LooksVirtual) { $Gaps += 'PHYSICAL_HARDWARE_NOT_CONFIRMED' }
if (-not $OsCandidate) { $Gaps += 'WINDOWS_11_EDITION_NOT_CONFIRMED' }
if (-not $Elevated) { $Gaps += 'ADMIN_TOKEN_NOT_PRESENT_FOR_FUTURE_G3' }
if ($Module -ne 'AVAILABLE_NATIVE_PS51') { $Gaps += 'APPLOCKER_MODULE_NOT_AVAILABLE' }
if ($PolicyQuery -ne 'PASS_READONLY') { $Gaps += 'APPLOCKER_POLICY_QUERY_NOT_AVAILABLE' }
if ($null -eq $AppId) { $Gaps += 'APPIDSVC_MISSING' }
if ($null -ne $F1) { $Gaps += 'EXISTING_F1_SERVICE_REQUIRES_RECONCILIATION' }
if (Test-Path -LiteralPath $AuthorityRoot) { $Gaps += 'EXISTING_F1_AUTHORITY_ROOT_REQUIRES_RECONCILIATION' }

[ordered]@{
    schema = 'FOX2_G3_PHYSICAL_HOST_READONLY_V1'
    owner_target = 'PHYSICAL_WINDOWS'
    read_only = $true
    observed_utc = [DateTime]::UtcNow.ToString('o')
    physical_hardware_candidate = (-not $LooksVirtual)
    physical_host_execution_authorized = $false
    daily_use_host_protection = 'NOT_ATTESTED'
    recovery_and_rollback_proven = $false
    admin_token_elevated = [bool]$Elevated
    domain_joined = [bool]$Computer.PartOfDomain
    windows_11_edition_candidate = $OsCandidate
    native_windows_powershell_present = (Test-Path -LiteralPath $NativePS -PathType Leaf)
    applocker_module = $Module
    policy_query = $PolicyQuery
    effective_policy_sha256 = $EffectiveDigest
    local_policy_sha256 = $LocalDigest
    appidsvc_present = ($null -ne $AppId)
    appidsvc_status = if ($null -eq $AppId) { 'MISSING' } else { [string]$AppId.Status }
    existing_f1_service = ($null -ne $F1)
    existing_f1_authority_root = (Test-Path -LiteralPath $AuthorityRoot)
    capability_gaps = @($Gaps)
    old_vm_bound_preexec_usable_for_physical = $false
    g3_host_preexec = 'NOT_RUN'
    g3_privileged_operations = 'NOT_AUTHORIZED_BY_THIS_PROBE'
    g4_owner_host_adoption = 'NOT_RUN'
    internal_ready = 'NOT_ATTESTED'
} | ConvertTo-Json -Depth 5
