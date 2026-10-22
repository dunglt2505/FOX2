#requires -Version 7.0
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# One native Owner-host attempt inside the existing FOX2 Bridge Whole-WP.
# Only the accepted A04 package and R5 external certifier are used.
# This runner does not activate F1/Worker, G3, G4, broker, provider or LIVE.
$Repo = 'C:\Projects\FOX2'
$WT = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022'
$R5Branch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022'
$ReviewBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$R5Result = '10326dd116ccbfa90a70db4f4c8ec27487ee4fbf'
$R5Review = '1ef5506d592cc7da9c93e61d86a158c12b9b27b3'
$R5RuntimeBase = '59ba8b50136ac5bcee7cf2d2edbf65e360812b78'
$CertifierBlob = '0ef54968bb750fdfec22fd5c77bf09b0b6c74603'
$PackageHash = 'f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee'
$PackageSource = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$SourceInventory = '6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73'
$DictionaryHash = '7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7'
$Package = 'C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip'
$Python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$Out = 'C:\Projects\FOX2-artifacts\bridge_internal_validation\attempt_001'
$Root = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$Desktop = Join-Path $env:LOCALAPPDATA 'FOX2\BridgeDesktop'
$Certifier = Join-Path $WT 'agent_bridge\scripts\certify_user_lifecycle.py'
$UI = Join-Path $WT 'agent_bridge\scripts\certify_rc1_ui.ps1'
$Attempt = 'FOX2-BRIDGE-INTERNAL-VALIDATION-001'
$R5Dispatch = 'FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-CODEX-001'
$Git = (Get-Command git.exe -ErrorAction Stop).Source
$Pwsh = (Get-Command pwsh.exe -ErrorAction Stop).Source
function Need([bool]$Ok,[string]$Reason) { if (-not $Ok) { throw ('STOP: ' + $Reason) } }
function G([string[]]$A) {
    $Lines = @(& $Git -C $WT @A)
    Need ($LASTEXITCODE -eq 0) ('Git error: ' + $A[0])
    return ($Lines -join [Environment]::NewLine).Trim()
}
function Remote([string]$B) {
    $L = @(& $Git -C $WT ls-remote --refs origin ('refs/heads/' + $B))
    Need ($LASTEXITCODE -eq 0 -and $L.Count -eq 1) ('Remote unavailable: ' + $B)
    return (($L[0] -split '\s+')[0])
}
function WPF {
    return @(Get-CimInstance Win32_Process -Filter "Name='FOX2.Bridge.Desktop.exe'" |
        Select-Object ProcessId,ExecutablePath)
}
function WpfIdentity([object[]]$List) {
    Need ($List.Count -le 1) 'Duplicate WPF process'
    if ($List.Count -eq 1) {
        $Expected = Join-Path $Root ('versions\' + $PackageHash + '\payload\desktop\FOX2.Bridge.Desktop.exe')
        Need (Test-Path -LiteralPath $Expected -PathType Leaf) 'Exact WPF missing'
        Need (-not [string]::IsNullOrWhiteSpace([string]$List[0].ExecutablePath)) 'WPF path unavailable'
        Need ([IO.Path]::GetFullPath([string]$List[0].ExecutablePath).Equals(
            [IO.Path]::GetFullPath($Expected),[StringComparison]::OrdinalIgnoreCase)) 'WPF package mismatch'
    }
}
function NoWorker {
    $P = @(Get-CimInstance Win32_Process)
    $Bad = @($P | Where-Object {
        ([string]$_.CommandLine) -match '(?i)fox2_agent_bridge\s+worker|desktop_tray\.ps1|FOX2F1Authority'
    })
    Need ($Bad.Count -eq 0) 'Worker/F1/legacy process present'
    $Writers = @($P | Where-Object {
        ([string]$_.Name) -match '(?i)^codex([.-].*)?\.exe$' -and
        ([string]$_.CommandLine).IndexOf('FOX2-BRIDGE-',[StringComparison]::OrdinalIgnoreCase) -ge 0
    })
    Need ($Writers.Count -eq 0) 'Competing Bridge CODEX writer'
}
function Installed {
    $Pointer = Join-Path $Root 'current.json'
    $Receipt = Join-Path $Root ('versions\' + $PackageHash + '\receipt.json')
    Need (Test-Path -LiteralPath $Pointer -PathType Leaf) 'Installed pointer missing'
    Need (Test-Path -LiteralPath $Receipt -PathType Leaf) 'Installed receipt missing'
    $P = Get-Content -LiteralPath $Pointer -Raw | ConvertFrom-Json
    $R = Get-Content -LiteralPath $Receipt -Raw | ConvertFrom-Json
    Need ($P.package_sha256 -ceq $PackageHash) 'Wrong installed package'
    Need ($P.source_sha256 -ceq $SourceInventory) 'Wrong installed source inventory'
    Need ($R.package_sha256 -ceq $PackageHash) 'Wrong receipt package'
    Need ($R.manifest.source_git_commit -ceq $PackageSource) 'Wrong receipt source commit'
    Need ($R.manifest.dictionary_sha256 -ceq $DictionaryHash) 'Wrong installed Dictionary'
}
function Safe {
    $Runtime = Join-Path $Root ('versions\' + $PackageHash + '\runtime\Scripts\python.exe')
    Need (Test-Path -LiteralPath $Runtime -PathType Leaf) 'Installed runtime Python missing'
    $L = @(& $Runtime -I -m fox2_agent_bridge control status)
    Need ($LASTEXITCODE -eq 0) 'Installed control failed'
    $S = ($L -join [Environment]::NewLine) | ConvertFrom-Json
    Need (($S.state -ceq 'STOPPED') -and ($S.paused -eq $true) -and
        ($S.setup_complete -eq $true) -and ($null -eq $S.current_dispatch)) 'Unsafe control'
}
$SnapshotCode = @'
import hashlib,json,re,sqlite3,sys
from pathlib import Path
root=Path(sys.argv[1]); db=root/'data/bridge.db'
assert db.is_file()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
with sqlite3.connect(db.as_uri()+'?mode=ro',uri=True,timeout=5) as conn:
    conn.execute('PRAGMA query_only=ON')
    assert conn.execute('PRAGMA quick_check').fetchall()==[('ok',)]
    tables={}
    for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
        assert re.fullmatch('[A-Za-z_][A-Za-z0-9_]*',name)
        def clean(v): return {'bytes_sha256':hashlib.sha256(v).hexdigest()} if isinstance(v,bytes) else v
        rows=sorted(json.dumps([clean(v) for v in row],sort_keys=True,default=str)
                    for row in conn.execute('SELECT * FROM "'+name+'"'))
        tables[name]={'rows':len(rows),'hash':hashlib.sha256(json.dumps(rows).encode()).hexdigest()}
print(json.dumps({'config':sha(root/'config/bridge.toml'),
    'manual_consumption':sha(root/'data/manual_consumption.json'),
    'tables':tables},sort_keys=True,separators=(',',':')))
'@
function Snapshot {
    $L = @(& $Python -I -B -c $SnapshotCode $Root)
    Need ($LASTEXITCODE -eq 0 -and $L.Count -gt 0) 'SQLite snapshot failed'
    return ($L -join [Environment]::NewLine).Trim()
}
function WaitWpf([int]$Number,[int]$Seconds) {
    $Deadline = [DateTime]::UtcNow.AddSeconds($Seconds)
    do {
        $P = @(WPF)
        WpfIdentity $P
        if ($P.Count -eq $Number) { return $P }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $Deadline)
    throw ('STOP: WPF count did not become ' + $Number)
}

# All following checks are read-only; no attempt consumed yet.
Need ($PSVersionTable.PSVersion.Major -ge 7) 'PowerShell 7 required'
Need (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)) 'Run non-elevated per-user'
foreach ($P in @($Repo,$WT,$Package,$Python,$Certifier,$UI)) {
    Need (Test-Path -LiteralPath $P) ('Prerequisite absent: ' + $P)
}
Need ((G @('branch','--show-current')) -ceq $R5Branch) 'Wrong source branch'
Need ((G @('rev-parse','HEAD')) -ceq $R5Result) 'R5 HEAD mismatch'
Need ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'R5 WIP detected'
Need ((Remote $R5Branch) -ceq $R5Result) 'R5 result remote moved'
Need ((G @('rev-parse',($R5Result+':agent_bridge/scripts/certify_user_lifecycle.py'))) -ceq $CertifierBlob) 'R5 certifier Git identity mismatch'
Need ((G @('hash-object','--',$Certifier)) -ceq $CertifierBlob) 'R5 local certifier mismatch'
$ReviewRemote = Remote $ReviewBranch
[void](& $Git -C $WT fetch --no-tags origin ('refs/heads/' + $ReviewBranch))
Need ($LASTEXITCODE -eq 0) 'R5 CHAT review fetch failed'
Need ((G @('rev-parse','FETCH_HEAD')) -ceq $ReviewRemote) 'R5 review fetch drift'
[void](& $Git -C $WT merge-base --is-ancestor $R5Review $ReviewRemote)
Need ($LASTEXITCODE -eq 0) 'R5 CHAT acceptance not current'
Need ((Get-FileHash -LiteralPath $Package -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $PackageHash) 'A04 package hash mismatch'
Installed
Safe
NoWorker
$WpfAtEntry = @(WPF)
WpfIdentity $WpfAtEntry
$Before = Snapshot
$BeforeObject = $Before | ConvertFrom-Json
Need ($null -ne $BeforeObject.config -and $null -ne $BeforeObject.manual_consumption) 'Durable baseline incomplete'
$Common = G @('rev-parse','--git-common-dir')
if (![IO.Path]::IsPathFullyQualified($Common)) {
    $Common = [IO.Path]::GetFullPath((Join-Path $WT $Common))
}
$Claims = Join-Path $Common 'fox2-attempts'
Need (Test-Path -LiteralPath $Claims -PathType Container) 'Claims directory missing'
$R5Claim = Join-Path $Claims ($R5Dispatch + '.claim.json')
Need (Test-Path -LiteralPath $R5Claim -PathType Leaf) 'R5 durable claim missing'
$Consumed = Get-Content -LiteralPath $R5Claim -Raw | ConvertFrom-Json
Need (($Consumed.consumed -eq $true) -and ($Consumed.no_replay -eq $true) -and
    ($Consumed.runtime_base -ceq $R5RuntimeBase)) 'R5 claim mismatch'
$Claim = Join-Path $Claims ($Attempt + '.claim.json')
Need (!(Test-Path -LiteralPath $Claim)) 'Validation already consumed: NO REPLAY'
Need (!(Test-Path -LiteralPath $Out)) 'Evidence output exists: reconcile before new attempt'

Write-Output 'FOX2_INTERNAL_VALIDATION_PRECONSUME=PASS'
Write-Output 'FOX2_A04_PACKAGE_REUSE=VERIFIED'
Write-Output ('FOX2_ENTRY_WPF_COUNT=' + $WpfAtEntry.Count)

# Durable no-replay claim is written BEFORE any host mutation.
$ClaimContent = [ordered]@{
    attempt_id=$Attempt;wp_id='FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
    r5_result=$R5Result;r5_chat_accept=$R5Review
    package_sha256=$PackageHash;consumed=$true;no_replay=$true
    created_utc=[DateTime]::UtcNow.ToString('o')
}
$ClaimBytes = [Text.UTF8Encoding]::new($false).GetBytes(
    (($ClaimContent | ConvertTo-Json -Compress) + [char]10))
$File = [IO.File]::Open($Claim,[IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write,[IO.FileShare]::None)
try { $File.Write($ClaimBytes,0,$ClaimBytes.Length);$File.Flush($true) }
finally { $File.Dispose() }
Need (Test-Path -LiteralPath $Claim -PathType Leaf) 'Claim write failed'

$Stage = 'OUTPUT_DIRECTORY';$Lifecycle = 'NOT_RUN';$Trial = 'NOT_RUN'
$Failure = $null
$Evidence = Join-Path $Out 'lifecycle_local.json'
try {
    New-Item -Path $Out -ItemType Directory -ErrorAction Stop | Out-Null
    $Stage = 'A04_LIFECYCLE_CONTINUATION'
    Write-Output 'FOX2_INTERNAL_ATTEMPT_CONSUMED=TRUE'
    # The accepted certifier performs one uninstall and reinstall of SAME A04 package.
    & $Python -I -B $Certifier --package $Package --sha256 $PackageHash --evidence $Evidence --continuation
    Need ($LASTEXITCODE -eq 0) 'R5 external certifier exited nonzero'
    Need (Test-Path -LiteralPath $Evidence -PathType Leaf) 'Lifecycle evidence missing'
    $Proof = Get-Content -LiteralPath $Evidence -Raw | ConvertFrom-Json
    Need ($Proof.presentation_lock_status -ceq 'PRESENTATION_LOCK_HELD') 'Live WPF lock proof missing'
    Need ($Proof.presentation_lock_released -eq $true) 'Lock release proof missing'
    Need ($Proof.uninstall.status -ceq 'UNINSTALLED') 'Uninstall proof missing'
    Need ($Proof.reinstall.package_sha256 -ceq $PackageHash) 'Same-package reinstall not proven'
    Installed;Safe;NoWorker
    Need (@(WPF).Count -eq 0) 'WPF remains after lifecycle'
    # Startup/scheduler bookkeeping can legitimately change in worker_state/bridge_meta.
    # Protect durable identities and all nonvolatile data tables, not volatile controls.
    $AfterObject = (Snapshot) | ConvertFrom-Json
    Need ($AfterObject.config -ceq $BeforeObject.config) 'Configuration changed across uninstall'
    Need ($AfterObject.manual_consumption -ceq $BeforeObject.manual_consumption) 'Consumption identities changed'
    foreach ($Table in @($BeforeObject.tables.PSObject.Properties.Name)) {
        if ($Table -in @('bridge_meta','worker_state','control_cursors','poll_observations')) {
            continue
        }
        $Prior = $BeforeObject.tables.$Table
        $Current = $AfterObject.tables.$Table
        Need ($null -ne $Current) ('Durable SQLite table missing: ' + $Table)
        Need (($Prior.rows -eq $Current.rows) -and ($Prior.hash -ceq $Current.hash)) (
            'Durable SQLite logical table drift: ' + $Table)
    }
    $Lifecycle = 'PASS'
    Write-Output 'FOX2_INTEGRATED_LIFECYCLE=PASS'

    $Stage = 'RESTART_PRESENTATION_TRIAL'
    & $Pwsh -NoProfile -NonInteractive -File (Join-Path $Root 'launch.ps1')
    Need ($LASTEXITCODE -eq 0) 'Presentation launch 1 failed'
    $First = @(WaitWpf 1 45)
    $OriginalPid = [int]$First[0].ProcessId
    & $Pwsh -NoProfile -NonInteractive -File (Join-Path $Root 'launch.ps1')
    Need ($LASTEXITCODE -eq 0) 'Presentation singleton launch failed'
    $Second = @(WaitWpf 1 45)
    Need ([int]$Second[0].ProcessId -eq $OriginalPid) 'Singleton PID changed'
    $Json = @(& $Pwsh -NoProfile -NonInteractive -File $UI -Action inspect)
    Need ($LASTEXITCODE -eq 0) 'UI inspect failed'
    $Screen = ($Json -join [Environment]::NewLine) | ConvertFrom-Json
    Need ($Screen.process_id -eq $OriginalPid -and @($Screen.screens).Count -eq 6 -and
        $Screen.check_now_enabled -eq $false) 'UI PID/navigation/paused check failed'
    $Check = @(& $Pwsh -NoProfile -NonInteractive -File $UI -Action check)
    Need ($LASTEXITCODE -eq 0 -and ($Check -join '').Trim() -ceq 'PAUSED_CHECK_DISABLED') 'Check Now not disabled'
    $Exit = @(& $Pwsh -NoProfile -NonInteractive -File $UI -Action exit)
    Need ($LASTEXITCODE -eq 0 -and ($Exit -join '').Trim() -ceq 'EXIT_INVOKED') 'Graceful exit failed'
    [void](WaitWpf 0 30)
    $Lock = Join-Path $Desktop 'desktop.lock'
    Need (Test-Path -LiteralPath $Lock -PathType Leaf) 'Desktop lock absent after exit'
    $LockStream = [IO.File]::Open($Lock,[IO.FileMode]::Open,
        [IO.FileAccess]::ReadWrite,[IO.FileShare]::ReadWrite)
    $LockStream.Dispose()
    Installed;Safe;NoWorker
    $Trial = 'PASS';$Stage = 'COMPLETE'
    Write-Output 'FOX2_RESTART_SINGLETON_PRESENTATION=PASS'
}
catch {
    $Failure = $_.Exception.GetType().Name
    Write-Output ('FOX2_INTERNAL_VALIDATION_STOP_STAGE=' + $Stage)
    Write-Output 'FOX2_INTERNAL_VALIDATION=NEEDS_RECONCILIATION'
}
finally {
    $Summary = [ordered]@{
        schema='FOX2_INTERNAL_VALIDATION_SANITIZED_V1'
        attempt_id=$Attempt;attempt_consumed=$true
        r5_source=$R5Result;r5_chat_accept=$R5Review
        package_sha256=$PackageHash;package_rebuilt=$false
        lifecycle=$Lifecycle;presentation_restart=$Trial
        g3_isolated_host='NOT_RUN';g4_privileged_adoption='NOT_RUN'
        f1_worker_runtime='NOT_RUN';internal_ready='NOT_ATTESTED'
        stage=$Stage;failure_class=$Failure;no_replay=$true
        finished_utc=[DateTime]::UtcNow.ToString('o')
    }
    $SummaryJson = $Summary | ConvertTo-Json -Depth 5
    if (Test-Path -LiteralPath $Out -PathType Container) {
        $SummaryJson | Set-Content -LiteralPath (Join-Path $Out 'summary_sanitized.json') -Encoding utf8
    }
    Write-Output '=== FOX2 INTERNAL VALIDATION SANITIZED SUMMARY ==='
    Write-Output ($Summary | ConvertTo-Json -Compress -Depth 5)
    Write-Output 'FOX2_DO_NOT_RERUN_THIS_ATTEMPT=TRUE'
}
