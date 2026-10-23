#requires -Version 7.0
# FOX2 G3 physical Windows: scoped READ ONLY host/ACL and F1 receipt inventory.
# No AppLocker rule generation, installation, service changes or claim consumption.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not $IsWindows) { throw 'STOP: physical Windows host required.' }

$BaselineHash = '635222d6f1ee0a7561e6c04e8894e688a5d19a3ce7549294f4c821a11f807e15'
$SnapshotDir = Join-Path $env:LOCALAPPDATA 'FOX2\G3PolicySnapshots\20261023T041424Z'
foreach ($Scope in @('local', 'effective')) {
    $File = Join-Path $SnapshotDir "applocker_$Scope.xml"
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) {
        throw "STOP: private $Scope policy backup not found."
    }
    if ((Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash.ToLowerInvariant() -ne $BaselineHash) {
        throw "STOP: private $Scope policy backup hash drift."
    }
    [xml]$Xml = Get-Content -LiteralPath $File -Raw
    if ($Xml.DocumentElement.LocalName -ne 'AppLockerPolicy' -or
        @($Xml.SelectNodes('/AppLockerPolicy/RuleCollection')).Count -ne 0) {
        throw "STOP: $Scope policy backup is no longer the observed empty baseline."
    }
}

$Untrusted = @('S-1-1-0', 'S-1-5-11', 'S-1-5-32-545')
$WriteMask = [int64]([Security.AccessControl.FileSystemRights]::WriteData -bor
    [Security.AccessControl.FileSystemRights]::AppendData -bor
    [Security.AccessControl.FileSystemRights]::CreateDirectories -bor
    [Security.AccessControl.FileSystemRights]::Delete -bor
    [Security.AccessControl.FileSystemRights]::ChangePermissions -bor
    [Security.AccessControl.FileSystemRights]::TakeOwnership -bor
    [Security.AccessControl.FileSystemRights]::WriteAttributes)

function Get-PathReview([string]$ItemPath, [string]$Kind) {
    $Exists = Test-Path -LiteralPath $ItemPath -PathType $Kind
    if (-not $Exists) {
        return [ordered]@{exists=$false; acl_observation='NOT_PRESENT'; risk_aces=0}
    }
    $Current = (Get-Item -LiteralPath $ItemPath -Force -ErrorAction Stop).FullName
    $Issues = 0
    $Examined = 0
    $ErrorFound = $false
    while ($Current -and $Examined -lt 20) {
        $Examined++
        try {
            $Item = Get-Item -LiteralPath $Current -Force -ErrorAction Stop
            if ($Item.Attributes -band [IO.FileAttributes]::ReparsePoint) { $Issues++ }
            $Acl = Get-Acl -LiteralPath $Current -ErrorAction Stop
            foreach ($Ace in @($Acl.Access)) {
                if ($Ace.AccessControlType -ne 'Allow' -or
                    (([int64]$Ace.FileSystemRights -band $WriteMask) -eq 0)) {
                    continue
                }
                try {
                    $Sid = $Ace.IdentityReference.Translate(
                        [Security.Principal.SecurityIdentifier]).Value
                } catch {
                    $Sid = 'UNRESOLVED'
                }
                if ($Sid -in $Untrusted -or $Sid -eq 'UNRESOLVED' -or
                    $Sid -match '^S-1-5-21-') { $Issues++ }
            }
        } catch {
            $ErrorFound = $true
            break
        }
        $Root = [IO.Path]::GetPathRoot($Current)
        if ($Current.TrimEnd('\') -ieq $Root.TrimEnd('\')) { break }
        $Next = Split-Path -Path $Current -Parent
        if (-not $Next -or $Next -ieq $Current) { break }
        $Current = $Next
    }
    $State = if ($ErrorFound) { 'ACL_QUERY_INCOMPLETE' }
        elseif ($Issues -gt 0) { 'POTENTIAL_LOW_TRUST_WRITE_REVIEW_REQUIRED' }
        else { 'NO_OBVIOUS_LOW_TRUST_WRITE_ACE_NOT_ATTESTED' }
    return [ordered]@{exists=$true; acl_observation=$State;
        risk_aces=$Issues; ancestor_nodes_checked=$Examined}
}

$Candidates = @(
    [ordered]@{ collection='Exe'; rule='%WINDIR%\System32\cmd.exe';
        target=(Join-Path $env:WINDIR 'System32\cmd.exe'); kind='Leaf' },
    [ordered]@{ collection='Exe'; rule='%WINDIR%\System32\WindowsPowerShell\v1.0\powershell.exe';
        target=(Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'); kind='Leaf' },
    [ordered]@{ collection='Exe'; rule='%PROGRAMFILES%\PowerShell\7\pwsh.exe';
        target=(Join-Path $env:ProgramFiles 'PowerShell\7\pwsh.exe'); kind='Leaf' },
    [ordered]@{ collection='Script'; rule='%WINDIR%\System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Management\*';
        target=(Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\Modules\Microsoft.PowerShell.Management'); kind='Container' },
    [ordered]@{ collection='Script'; rule='%PROGRAMFILES%\PowerShell\7\Modules\Microsoft.PowerShell.Archive\*';
        target=(Join-Path $env:ProgramFiles 'PowerShell\7\Modules\Microsoft.PowerShell.Archive'); kind='Container' }
)
$Observed = @()
foreach ($Candidate in $Candidates) {
    $Check = Get-PathReview -ItemPath $Candidate.target -Kind $Candidate.kind
    $Observed += [ordered]@{
        collection=$Candidate.collection
        candidate_rule_path=$Candidate.rule
        present=$Check.exists
        acl_observation=$Check.acl_observation
        suspicious_ace_count=$Check.risk_aces
        # A protected-looking ACL alone never constitutes an approved rule.
        approved_allow_rule=$false
    }
}

$PackageReceipts = @()
$Root = 'C:\Projects\FOX2'
$KnownRoots = @(
    (Join-Path $Root 'dist'),
    (Join-Path $Root 'artifacts'),
    (Join-Path $Root 'agent_bridge\dist'),
    (Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge')
)
foreach ($Dir in $KnownRoots) {
    if (-not (Test-Path -LiteralPath $Dir -PathType Container)) { continue }
    foreach ($Receipt in @(Get-ChildItem -LiteralPath $Dir -Filter '*.json' -File -ErrorAction SilentlyContinue)) {
        try {
            $Entry = Get-Content -LiteralPath $Receipt.FullName -Raw | ConvertFrom-Json -ErrorAction Stop
            if ($Entry.manifest.format -cne 'FOX2_USER_PACKAGE_1' -or
                [string]$Entry.sha256 -notmatch '^[0-9a-fA-F]{64}$') { continue }
            $Name = [string]$Entry.package
            if (-not $Name -or [IO.Path]::GetFileName($Name) -cne $Name) { continue }
            $Archive = Join-Path $Dir $Name
            $Valid = (Test-Path -LiteralPath $Archive -PathType Leaf) -and
                ((Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash.ToLowerInvariant() -ceq
                ([string]$Entry.sha256).ToLowerInvariant())
            $PackageReceipts += [ordered]@{
                archive_sha256=([string]$Entry.sha256).ToLowerInvariant()
                hash_verified=[bool]$Valid
                source_git_commit=[string]$Entry.manifest.source_git_commit
                f1_activation=[string]$Entry.manifest.f1_support.activation
                # Receipt search is limited to known roots, not all user files.
                host_installed_or_adopted='NOT_ATTESTED'
            }
        } catch { continue }
    }
}

$Result = [ordered]@{
    schema='FOX2_G3_PHYSICAL_ALLOW_PACKAGE_READONLY_V1'
    baseline_snapshot='PRIVATE_LOCAL_AND_EFFECTIVE_SHA256_MATCH'
    observed_utc=[DateTime]::UtcNow.ToString('o')
    allow_rule_candidates=@($Observed)
    allow_rules_reviewed_and_approved=0
    allow_manifest_generated=$false
    acl_review_completeness='NOT_ATTESTED_BY_AUTOMATED_ACE_SCAN'
    package_receipts_in_known_roots=@($PackageReceipts)
    final_f1_installed_package_identity='NOT_ATTESTED'
    other_install_locations_searched=$false
    csp_policy_coverage='NOT_VERIFIED'
    rollback_restore_execution='NOT_RUN'
    applocker_or_service_mutation='NONE'
    g3_host_enforcement='NOT_RUN'
    g4_adoption='NOT_RUN'
    internal_ready='NOT_ATTESTED'
}
Write-Output 'FOX2_G3_ALLOW_PACKAGE_READONLY=COMPLETE'
$Result | ConvertTo-Json -Depth 7
Write-Output 'FOX2_G3_HOST_MUTATION=NONE'
