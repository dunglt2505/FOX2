#requires -Version 7.0
param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# FOX2 Bridge Whole-WP, restart-only continuation AFTER consumed integrated validation 001.
# NO lifecycle repeat, uninstall, reinstall, package build, Agent Dispatch, Worker/F1,
# privileged G3/G4, provider/broker, Canary or LIVE actions.
$Repo = 'C:\Projects\FOX2'
$WT = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022'
$SourceBranch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022'
$ReviewBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$R5Source = '10326dd116ccbfa90a70db4f4c8ec27487ee4fbf'
$R5Review = '1ef5506d592cc7da9c93e61d86a158c12b9b27b3'
$R5CertifierBlob = '0ef54968bb750fdfec22fd5c77bf09b0b6c74603'
$A04PackageHash = 'f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee'
$A04Source = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$A04Inventory = '6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73'
$A04DictHash = '7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7'
$Archive = 'C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip'
$Root = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$DesktopRoot = Join-Path $env:LOCALAPPDATA 'FOX2\BridgeDesktop'
$Python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
$UI = Join-Path $WT 'agent_bridge\scripts\certify_rc1_ui.ps1'
$OldAttemptId = 'FOX2-BRIDGE-INTERNAL-VALIDATION-001'
$NewAttemptId = 'FOX2-BRIDGE-RESTART-CONTINUATION-001'
$OldOut = 'C:\Projects\FOX2-artifacts\bridge_internal_validation\attempt_001'
$NewOut = 'C:\Projects\FOX2-artifacts\bridge_internal_validation\restart_continuation_001'
$Git = (Get-Command git.exe -ErrorAction Stop).Source
$Pwsh = (Get-Command pwsh.exe -ErrorAction Stop).Source

function Need([bool]$Ok,[string]$Code) {
    if (-not $Ok) { throw ('STOP: ' + $Code) }
}
function GitRead([string[]]$Arguments) {
    $Rows = @(& $Git -C $WT @Arguments)
    Need ($LASTEXITCODE -eq 0) 'GIT_READ_FAILED'
    return ($Rows -join [Environment]::NewLine).Trim()
}
function RemoteHead([string]$Branch) {
    $Rows = @(& $Git -C $WT ls-remote --refs origin ('refs/heads/' + $Branch))
    Need ($LASTEXITCODE -eq 0 -and $Rows.Count -eq 1) 'REMOTE_SOURCE_UNAVAILABLE'
    return (($Rows[0] -split '\s+')[0])
}
function WpfProcesses {
    return @(Get-CimInstance Win32_Process -Filter "Name='FOX2.Bridge.Desktop.exe'" -ErrorAction Stop |
        Select-Object ProcessId,ExecutablePath,SessionId)
}
function AssertWpf([object[]]$Processes) {
    Need ($Processes.Count -le 1) 'DUPLICATE_WPF'
    if ($Processes.Count -eq 1) {
        $Expected = Join-Path $Root ('versions\' + $A04PackageHash + '\payload\desktop\FOX2.Bridge.Desktop.exe')
        Need (Test-Path -LiteralPath $Expected -PathType Leaf) 'EXACT_WPF_BINARY_MISSING'
        Need (-not [string]::IsNullOrWhiteSpace([string]$Processes[0].ExecutablePath)) 'WPF_IMAGE_UNKNOWN'
        Need ([IO.Path]::GetFullPath([string]$Processes[0].ExecutablePath).Equals(
            [IO.Path]::GetFullPath($Expected),[StringComparison]::OrdinalIgnoreCase)) 'WRONG_WPF_IMAGE'
        Need ([int]$Processes[0].ProcessId -gt 0) 'WPF_PID_INVALID'
        $CurrentSession = (Get-Process -Id $PID -ErrorAction Stop).SessionId
        Need ([int]$Processes[0].SessionId -eq [int]$CurrentSession) 'WPF_OTHER_SESSION'
    }
}
function NoBridgeWorker {
    $Processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    $Workers = @($Processes | Where-Object {
        ([string]$_.CommandLine) -match '(?i)fox2_agent_bridge\s+worker|fox2_agent_bridge\.f1_service|desktop_tray\.ps1|FOX2F1Authority'
    })
    Need ($Workers.Count -eq 0) 'WORKER_F1_OR_LEGACY_PRESENT'
    $Writers = @($Processes | Where-Object {
        ([string]$_.Name) -match '(?i)^codex([.-].*)?\.exe$' -and
        ([string]$_.CommandLine).IndexOf('FOX2-BRIDGE-',[StringComparison]::OrdinalIgnoreCase) -ge 0
    })
    Need ($Writers.Count -eq 0) 'COMPETING_BRIDGE_WRITER'
}
function Installed {
    $PointerPath = Join-Path $Root 'current.json'
    $ReceiptPath = Join-Path $Root ('versions\' + $A04PackageHash + '\receipt.json')
    Need (Test-Path -LiteralPath $PointerPath -PathType Leaf) 'CURRENT_POINTER_MISSING'
    Need (Test-Path -LiteralPath $ReceiptPath -PathType Leaf) 'INSTALLED_RECEIPT_MISSING'
    $Pointer = Get-Content -LiteralPath $PointerPath -Raw | ConvertFrom-Json
    $Receipt = Get-Content -LiteralPath $ReceiptPath -Raw | ConvertFrom-Json
    Need ($Pointer.package_sha256 -ceq $A04PackageHash) 'PACKAGE_IDENTITY_DRIFT'
    Need ($Pointer.source_sha256 -ceq $A04Inventory) 'SOURCE_INVENTORY_DRIFT'
    Need ($Receipt.package_sha256 -ceq $A04PackageHash) 'RECEIPT_PACKAGE_DRIFT'
    Need ($Receipt.manifest.source_git_commit -ceq $A04Source) 'SOURCE_COMMIT_DRIFT'
    Need ($Receipt.manifest.dictionary_sha256 -ceq $A04DictHash) 'INSTALLED_DICTIONARY_DRIFT'
}
$StateCode = @'
import hashlib, json, re, sqlite3, sys, tempfile
from contextlib import closing
from pathlib import Path
root=Path(sys.argv[1]).resolve()
cfg=root/'config/bridge.toml'; db=root/'data/bridge.db'
manual=root/'data/manual_consumption.json'
wal=db.with_name(db.name+'-wal'); journal=db.with_name(db.name+'-journal')
def capture():
    return (cfg.read_bytes(),db.read_bytes(),wal.read_bytes() if wal.exists() else None,
            journal.read_bytes() if journal.exists() else None,manual.read_bytes())
a=capture()
if a[3]:
    raise RuntimeError('JOURNAL_PRESENT')
with tempfile.TemporaryDirectory(prefix='FOX2-restart-state-') as temp:
    snap=Path(temp)/'bridge.db';snap.write_bytes(a[1])
    if a[2] is not None:
        snap.with_name('bridge.db-wal').write_bytes(a[2])
    with closing(sqlite3.connect(str(snap),timeout=5)) as con:
        con.execute('PRAGMA query_only=ON')
        assert con.execute('PRAGMA quick_check').fetchall()==[('ok',)]
        value=con.execute('SELECT payload FROM worker_state WHERE id=1').fetchone()
        assert value is not None
        s=json.loads(value[0]); assert isinstance(s,dict)
        rows=con.execute('SELECT * FROM dispatches ORDER BY dispatch_id').fetchall()
        def norm(v):
            return {'binary_sha256':hashlib.sha256(v).hexdigest()} if isinstance(v,bytes) else v
        normalized=[json.dumps([norm(x) for x in row],sort_keys=True,default=str)
                    for row in rows]
        dhash=hashlib.sha256(json.dumps(normalized,sort_keys=True).encode()).hexdigest()
if a != capture():
    raise RuntimeError('SOURCE_CHANGED')
safe=(s.get('state')=='STOPPED' and s.get('paused') is True and
      s.get('setup_complete') is True and 'current_dispatch' in s and
      s['current_dispatch'] is None)
print(json.dumps({'safe':safe,'state':s.get('state') if s.get('state') in
 ('STOPPED','PAUSED','IDLE','ERROR','DEGRADED') else 'OTHER',
 'paused':s.get('paused') is True,
 'setup_complete':s.get('setup_complete') is True,
 'current_dispatch_absent': 'current_dispatch' in s and s['current_dispatch'] is None,
 'config_sha256':hashlib.sha256(a[0]).hexdigest(),
 'consumption_sha256':hashlib.sha256(a[4]).hexdigest(),
 'dispatch_table_sha256':dhash,'dispatch_count':len(rows)},sort_keys=True))
'@
function ReadState {
    $Rows = @(& $Python -I -B -c $StateCode $Root 2>$null)
    Need ($LASTEXITCODE -eq 0 -and $Rows.Count -ge 1) 'READONLY_STATE_FAILED'
    $State = ($Rows -join [Environment]::NewLine) | ConvertFrom-Json
    Need ($State.safe -eq $true) 'UNSAFE_CONTROL'
    return $State
}
function WaitWpf([int]$Count,[int]$TimeoutSeconds) {
    $Deadline = [DateTime]::UtcNow.AddSeconds($TimeoutSeconds)
    do {
        $List = @(WpfProcesses)
        AssertWpf $List
        if ($List.Count -eq $Count) { return $List }
        Start-Sleep -Milliseconds 500
    } while ([DateTime]::UtcNow -lt $Deadline)
    throw 'STOP: WPF_WAIT_TIMEOUT'
}
function InvokeLaunch {
    & $Pwsh -NoProfile -NonInteractive -WindowStyle Hidden -File (Join-Path $Root 'launch.ps1') 2>$null | Out-Null
    Need ($LASTEXITCODE -eq 0) 'LAUNCH_ENTRYPOINT_NONZERO'
}
function UiAction([string]$Action) {
    $Rows = @(& $Pwsh -NoProfile -NonInteractive -File $UI -Action $Action 2>$null)
    Need ($LASTEXITCODE -eq 0) ('UI_' + $Action.ToUpperInvariant() + '_FAILED')
    return ($Rows -join [Environment]::NewLine).Trim()
}

# The following are PRE-CONSUME checks. They make NO WPF changes.
Need ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'
Need (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)) 'NON_ELEVATED_OWNER_REQUIRED'
foreach ($Path in @($Repo,$WT,$Archive,$Python,$UI)) {
    Need (Test-Path -LiteralPath $Path) 'PREREQUISITE_PATH_MISSING'
}
Need ((GitRead @('branch','--show-current')) -ceq $SourceBranch) 'WRONG_SOURCE_BRANCH'
Need ((GitRead @('rev-parse','HEAD')) -ceq $R5Source) 'R5_WORKTREE_HEAD_DRIFT'
Need ([string]::IsNullOrWhiteSpace((GitRead @('status','--porcelain=v1','--untracked-files=all')))) 'SOURCE_WORKTREE_DIRTY'
Need ((RemoteHead $SourceBranch) -ceq $R5Source) 'R5_REMOTE_SOURCE_DRIFT'
Need ((GitRead @('rev-parse',($R5Source+':agent_bridge/scripts/certify_user_lifecycle.py'))) -ceq $R5CertifierBlob) 'CERTIFIER_SOURCE_DRIFT'
$ReviewRemote = RemoteHead $ReviewBranch
[void](& $Git -C $WT fetch --no-tags origin ('refs/heads/' + $ReviewBranch))
Need ($LASTEXITCODE -eq 0) 'REVIEW_FETCH_FAILED'
Need ((GitRead @('rev-parse','FETCH_HEAD')) -ceq $ReviewRemote) 'REVIEW_READBACK_DRIFT'
[void](& $Git -C $WT merge-base --is-ancestor $R5Review $ReviewRemote)
Need ($LASTEXITCODE -eq 0) 'R5_REVIEW_NOT_APPLICABLE'
Need ((Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash.ToLowerInvariant() -ceq $A04PackageHash) 'A04_ARCHIVE_HASH_MISMATCH'
Installed
$OldSummary = Join-Path $OldOut 'summary_sanitized.json'
$OldEvidence = Join-Path $OldOut 'lifecycle_local.json'
Need (Test-Path -LiteralPath $OldSummary -PathType Leaf) 'PRIOR_SUMMARY_MISSING'
Need (Test-Path -LiteralPath $OldEvidence -PathType Leaf) 'PRIOR_LIFECYCLE_EVIDENCE_MISSING'
$Prior = Get-Content -LiteralPath $OldSummary -Raw | ConvertFrom-Json
$Proof = Get-Content -LiteralPath $OldEvidence -Raw | ConvertFrom-Json
Need ($Prior.attempt_id -ceq $OldAttemptId) 'PRIOR_ATTEMPT_ID_MISMATCH'
Need ($Prior.attempt_consumed -eq $true -and $Prior.no_replay -eq $true) 'PRIOR_ATTEMPT_NOT_CONSUMED'
Need ($Prior.lifecycle -ceq 'PASS') 'PRIOR_LIFECYCLE_NOT_PASSED'
Need ($Prior.presentation_restart -ceq 'NOT_RUN' -and $Prior.stage -ceq 'RESTART_PRESENTATION_TRIAL') 'PRIOR_RESTART_SUBJECT_MISMATCH'
Need ($Prior.package_sha256 -ceq $A04PackageHash -and $Prior.r5_source -ceq $R5Source) 'PRIOR_SOURCE_PACKAGE_MISMATCH'
Need ($Proof.presentation_lock_status -ceq 'PRESENTATION_LOCK_HELD' -and
    $Proof.presentation_lock_released -eq $true) 'LIFECYCLE_PRESENTATION_PROOF_MISSING'
Need ($Proof.uninstall.status -ceq 'UNINSTALLED') 'LIFECYCLE_UNINSTALL_PROOF_MISSING'
Need ($Proof.reinstall.package_sha256 -ceq $A04PackageHash) 'LIFECYCLE_REINSTALL_PROOF_MISSING'

$Common = GitRead @('rev-parse','--git-common-dir')
if (-not [IO.Path]::IsPathFullyQualified($Common)) {
    $Common = [IO.Path]::GetFullPath((Join-Path $WT $Common))
}
$Claims = Join-Path $Common 'fox2-attempts'
Need (Test-Path -LiteralPath $Claims -PathType Container) 'CLAIM_DIRECTORY_MISSING'
$OldClaimPath = Join-Path $Claims ($OldAttemptId + '.claim.json')
$NewClaimPath = Join-Path $Claims ($NewAttemptId + '.claim.json')
Need (Test-Path -LiteralPath $OldClaimPath -PathType Leaf) 'PRIOR_DURABLE_CLAIM_MISSING'
$OldClaim = Get-Content -LiteralPath $OldClaimPath -Raw | ConvertFrom-Json
Need ($OldClaim.consumed -eq $true -and $OldClaim.no_replay -eq $true) 'PRIOR_CLAIM_NOT_CONSUMED'
Need ($OldClaim.r5_result -ceq $R5Source) 'PRIOR_CLAIM_SOURCE_DRIFT'
Need (!(Test-Path -LiteralPath $NewClaimPath)) 'RESTART_ATTEMPT_CONSUMED_NO_REPLAY'
Need (!(Test-Path -LiteralPath $NewOut)) 'RESTART_EVIDENCE_ALREADY_EXISTS'

NoBridgeWorker
$Before = ReadState
$Existing = @(WpfProcesses)
AssertWpf $Existing
$AtEntry = $Existing.Count
if ($AtEntry -eq 0) {
    $Lock = Join-Path $DesktopRoot 'desktop.lock'
    if (Test-Path -LiteralPath $Lock -PathType Leaf) {
        try {
            $LockStream = [IO.File]::Open($Lock,[IO.FileMode]::Open,
                [IO.FileAccess]::ReadWrite,[IO.FileShare]::ReadWrite)
            $LockStream.Dispose()
        } catch {
            throw 'STOP: ORPHAN_LOCK_NOT_OPENABLE'
        }
    }
}
Write-Output 'FOX2_RESTART_ONLY_PRECONSUME=PASS'
Write-Output ('FOX2_RESTART_ENTRY_WPF_COUNT=' + $AtEntry)
Write-Output 'FOX2_LIFECYCLE_PASS_REUSED=TRUE'
Write-Output 'FOX2_PRIOR_ATTEMPT_NO_REPLAY=TRUE'

# This is a genuinely fresh bounded restart continuation attempt, not replay 001.
$Claim = [ordered]@{
    schema='FOX2_NATIVE_RESTART_CONTINUATION_V1'
    attempt_id=$NewAttemptId
    whole_wp='FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
    prior_consumed_attempt=$OldAttemptId
    prior_lifecycle='PASS_REUSED'
    r5_source=$R5Source
    package_sha256=$A04PackageHash
    consumed=$true
    no_replay=$true
    created_utc=[DateTime]::UtcNow.ToString('o')
}
$RawClaim = [Text.UTF8Encoding]::new($false).GetBytes(
    (($Claim | ConvertTo-Json -Compress -Depth 6) + [char]10))
$Fd = [IO.File]::Open($NewClaimPath,[IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write,[IO.FileShare]::None)
try { $Fd.Write($RawClaim,0,$RawClaim.Length);$Fd.Flush($true) }
finally { $Fd.Dispose() }
Need (Test-Path -LiteralPath $NewClaimPath -PathType Leaf) 'CLAIM_READBACK_FAILED'

$Step = 'CREATE_OUTPUT'
$ErrorCode = $null
$Restart = 'FAILED_IN_PROGRESS'
$InitialPid = if ($AtEntry -eq 1) { [int]$Existing[0].ProcessId } else { $null }
$VerifiedPid = $null
$ScreensVerified = 0
$ExplicitExit = $false
$NoWorkerVerified = $false
$PreservedDispatches = $false
try {
    [void][IO.Directory]::CreateDirectory((Split-Path -Parent $NewOut))
    New-Item -Path $NewOut -ItemType Directory -ErrorAction Stop | Out-Null
    $Step = 'ESTABLISH_EXACT_WPF'
    Write-Output 'FOX2_RESTART_ONLY_ATTEMPT_CONSUMED=TRUE'
    if ($AtEntry -eq 0) {
        InvokeLaunch
        $First = @(WaitWpf 1 45)
        Need ($First.Count -eq 1) 'FIRST_WPF_NOT_SINGLETON'
        $InitialPid = [int]$First[0].ProcessId
    }
    $Step = 'RELAUNCH_SINGLETON'
    InvokeLaunch
    $Second = @(WaitWpf 1 45)
    Need ($Second.Count -eq 1) 'SECOND_WPF_NOT_SINGLETON'
    $VerifiedPid = [int]$Second[0].ProcessId
    Need ($VerifiedPid -eq $InitialPid) 'SINGLETON_PID_CHANGED'
    $Step = 'UI_INSPECT'
    $Info = (UiAction 'inspect') | ConvertFrom-Json
    Need ([int]$Info.process_id -eq $VerifiedPid) 'UI_PID_CHANGED'
    $Names = @('Dashboard','Activity','Agents','Diagnostics','Artifacts','Settings')
    Need ((@($Info.screens).Count -eq $Names.Count) -and
        (($Info.screens -join '|') -ceq ($Names -join '|'))) 'UI_NAVIGATION_MISMATCH'
    Need ($Info.check_now_enabled -eq $false) 'PAUSED_UI_CHECK_ENABLED'
    $ScreensVerified = 6
    $Step = 'UI_CHECK'
    Need ((UiAction 'check') -ceq 'PAUSED_CHECK_DISABLED') 'PAUSED_CHECK_COMMAND_MISMATCH'
    $Step = 'GRACEFUL_EXIT'
    Need ((UiAction 'exit') -ceq 'EXIT_INVOKED') 'EXIT_ACTION_MISMATCH'
    $ExplicitExit = $true
    $Step = 'WAIT_ZERO_WPF'
    [void](WaitWpf 0 30)
    $Step = 'LOCK_RELEASE'
    $Lock = Join-Path $DesktopRoot 'desktop.lock'
    Need (Test-Path -LiteralPath $Lock -PathType Leaf) 'DESKTOP_LOCK_MISSING'
    $LockStream = [IO.File]::Open($Lock,[IO.FileMode]::Open,
        [IO.FileAccess]::ReadWrite,[IO.FileShare]::ReadWrite)
    $LockStream.Dispose()
    $Step = 'FINAL_SAFE_STATE'
    Installed
    NoBridgeWorker
    $After = ReadState
    Need ($Before.config_sha256 -ceq $After.config_sha256) 'CONFIGURATION_HASH_DRIFT'
    Need ($Before.consumption_sha256 -ceq $After.consumption_sha256) 'CONSUMPTION_HASH_DRIFT'
    Need ($Before.dispatch_table_sha256 -ceq $After.dispatch_table_sha256) 'DISPATCH_TABLE_HASH_DRIFT'
    Need ($Before.dispatch_count -eq $After.dispatch_count) 'DISPATCH_COUNT_DRIFT'
    $NoWorkerVerified = $true
    $PreservedDispatches = $true
    $Restart = 'PASS'
    $Step = 'COMPLETE'
    Write-Output 'FOX2_RESTART_ONLY_SINGLETON_UI_EXIT=PASS'
}
catch {
    if ($_.Exception.Message -match '^STOP: ([A-Z0-9_]+)$') {
        $ErrorCode = $Matches[1]
    } else {
        $ErrorCode = 'UNEXPECTED_EXCEPTION'
    }
    Write-Output ('FOX2_RESTART_ONLY_STOP_STEP=' + $Step)
    Write-Output ('FOX2_RESTART_ONLY_ERROR_CODE=' + $ErrorCode)
}
finally {
    $RemainingWpf = $null
    try { $RemainingWpf = @(WpfProcesses).Count } catch { }
    $Report = [ordered]@{
        schema='FOX2_RESTART_CONTINUATION_RESULT_V1'
        whole_wp='FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
        attempt_id=$NewAttemptId
        consumed=$true
        prior_attempt=$OldAttemptId
        previous_lifecycle='PASS_REUSED'
        package_sha256=$A04PackageHash
        r5_source=$R5Source
        restart=$Restart
        stage=$Step
        error_code=$ErrorCode
        entry_wpf_count=$AtEntry
        exit_wpf_count=$RemainingWpf
        same_singleton_pid=($null -ne $VerifiedPid -and $VerifiedPid -eq $InitialPid)
        screens_verified=$ScreensVerified
        explicit_graceful_exit=$ExplicitExit
        no_worker_after=$NoWorkerVerified
        durable_dispatches_preserved=$PreservedDispatches
        g3_isolated_host='NOT_RUN'
        g4_privileged_adoption='NOT_RUN'
        f1_worker_runtime='NOT_RUN'
        internal_ready='NOT_ATTESTED'
        no_replay=$true
        completed_utc=[DateTime]::UtcNow.ToString('o')
    }
    $SummaryJson = $Report | ConvertTo-Json -Depth 5
    if (Test-Path -LiteralPath $NewOut -PathType Container) {
        $SummaryJson | Set-Content -LiteralPath (Join-Path $NewOut 'summary_sanitized.json') -Encoding utf8
    }
    Write-Output '=== FOX2 RESTART CONTINUATION SANITIZED SUMMARY ==='
    Write-Output ($Report | ConvertTo-Json -Depth 5 -Compress)
    Write-Output 'FOX2_RESTART_CONTINUATION_NO_REPLAY=TRUE'
}
if ($Restart -cne 'PASS') {
    throw ('STOP: restart continuation consumed; step=' + $Step + '; code=' + $ErrorCode)
}
