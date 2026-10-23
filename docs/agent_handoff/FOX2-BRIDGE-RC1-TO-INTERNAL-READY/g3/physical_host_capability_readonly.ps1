#requires -Version 7.0
# FOX2 G3 physical Windows host capability — READ ONLY, no policy/service mutation.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Os = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
$Machine = Get-CimInstance Win32_ComputerSystem -ErrorAction Stop
$CurrentPrincipal = [Security.Principal.WindowsPrincipal]::new(
    [Security.Principal.WindowsIdentity]::GetCurrent())
$IsAdmin = $CurrentPrincipal.IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
$OsSupported = [bool](([int]$Os.BuildNumber -ge 22000) -and
    ([string]$Os.Caption -match '(?i)windows 11') -and
    ([string]$Os.Caption -match '(?i)pro|enterprise|education'))

$AppId = Get-Service -Name AppIDSvc -ErrorAction SilentlyContinue
$F1Service = Get-Service -Name FOX2F1Authority -ErrorAction SilentlyContinue
$F1Root = Join-Path $env:ProgramData 'FOX2\F1Authority'
$NativePS = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$ModuleStatus = 'NOT_VERIFIED'
$PolicyStatus = 'NOT_VERIFIED'
$EffectiveHash = $null
$LocalHash = $null

if (Test-Path -LiteralPath $NativePS -PathType Leaf) {
    $NativeCode = @'
$ErrorActionPreference = 'Stop'
$r = [ordered]@{
    module_loaded = $false
    group_policy_query = $false
    effective_sha256 = $null
    local_sha256 = $null
}
try {
    Import-Module AppLocker -ErrorAction Stop
    $null = Get-Command Get-AppLockerPolicy -ErrorAction Stop
    $r.module_loaded = $true
    try {
        $effective = [string](Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop)
        $local = [string](Get-AppLockerPolicy -Local -Xml -ErrorAction Stop)
        if (-not [string]::IsNullOrWhiteSpace($effective) -and
            -not [string]::IsNullOrWhiteSpace($local)) {
            $hash = [Security.Cryptography.SHA256]::Create()
            try {
                $r.effective_sha256 = [BitConverter]::ToString(
                    $hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($effective))
                ).Replace('-','').ToLowerInvariant()
                $r.local_sha256 = [BitConverter]::ToString(
                    $hash.ComputeHash([Text.Encoding]::UTF8.GetBytes($local))
                ).Replace('-','').ToLowerInvariant()
                $r.group_policy_query = $true
            } finally { $hash.Dispose() }
        }
    } catch { }
} catch { }
$r | ConvertTo-Json -Compress
'@
    $Encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($NativeCode))
    try {
        $Raw = @(& $NativePS -NoProfile -NonInteractive -EncodedCommand $Encoded 2>$null)
        if ($LASTEXITCODE -eq 0 -and $Raw.Count -ge 1) {
            $Value = ($Raw -join [Environment]::NewLine) | ConvertFrom-Json -ErrorAction Stop
            $ModuleStatus = if ($Value.module_loaded -eq $true) {
                'AVAILABLE_NATIVE_WINDOWS_PS'
            } else { 'UNAVAILABLE_OR_IMPORT_FAILED' }
            $PolicyStatus = if ($Value.group_policy_query -eq $true) {
                'GP_POLICY_QUERY_PASS'
            } else { 'GP_POLICY_QUERY_FAILED_OR_EMPTY' }
            $EffectiveHash = $Value.effective_sha256
            $LocalHash = $Value.local_sha256
        } else {
            $ModuleStatus = 'NATIVE_POWERSHELL_QUERY_FAILED'
            $PolicyStatus = 'NOT_VERIFIED'
        }
    } catch {
        $ModuleStatus = 'NATIVE_POWERSHELL_QUERY_FAILED'
        $PolicyStatus = 'NOT_VERIFIED'
    }
}

$Gaps = @()
if (-not $OsSupported) { $Gaps += 'WINDOWS_11_EDITION_NOT_CONFIRMED' }
if (-not $IsAdmin) { $Gaps += 'ADMIN_REQUIRED_FOR_FUTURE_G3_PRIVILEGED_TEST' }
if ($ModuleStatus -ne 'AVAILABLE_NATIVE_WINDOWS_PS') { $Gaps += 'APPLOCKER_MODULE_NOT_AVAILABLE' }
if ($PolicyStatus -ne 'GP_POLICY_QUERY_PASS') { $Gaps += 'APPLOCKER_GP_POLICY_QUERY_NOT_CONFIRMED' }
if ($null -eq $AppId) { $Gaps += 'APPIDSVC_NOT_PRESENT' }
if ($null -ne $F1Service) { $Gaps += 'EXISTING_F1_SERVICE_REQUIRES_RECONCILIATION' }
if (Test-Path -LiteralPath $F1Root) { $Gaps += 'EXISTING_F1_ROOT_REQUIRES_RECONCILIATION' }

$Result = [ordered]@{
    schema = 'FOX2_G3_PHYSICAL_READONLY_V3'
    target = 'OWNER_SELECTED_PHYSICAL_WINDOWS'
    captured_utc = [DateTime]::UtcNow.ToString('o')
    scan = 'COMPLETED_READONLY'
    windows_11_edition_candidate = $OsSupported
    administrator_token_observed = [bool]$IsAdmin
    domain_joined = [bool]$Machine.PartOfDomain
    native_windows_powershell_present = (Test-Path -LiteralPath $NativePS -PathType Leaf)
    applocker_module = $ModuleStatus
    applocker_gp_policy_query = $PolicyStatus
    applocker_policy_channel_coverage = 'GROUP_POLICY_ONLY_CSP_NOT_VERIFIED'
    effective_gp_policy_sha256 = $EffectiveHash
    local_gp_policy_sha256 = $LocalHash
    appidsvc_present = ($null -ne $AppId)
    appidsvc_status = if ($null -eq $AppId) { 'MISSING' } else { [string]$AppId.Status }
    f1_service_present = ($null -ne $F1Service)
    f1_authority_root_present = (Test-Path -LiteralPath $F1Root)
    capability_gaps = @($Gaps)
    policy_export_and_restore = 'NOT_VERIFIED'
    privileged_g3_host_mutation = 'NOT_RUN_NOT_AUTHORIZED_BY_THIS_SCAN'
    g3_test = 'NOT_RUN'
    g4_install = 'NOT_RUN'
    internal_ready = 'NOT_ATTESTED'
}
Write-Output 'FOX2_G3_PHYSICAL_READONLY=COMPLETE'
$Result | ConvertTo-Json -Depth 5
