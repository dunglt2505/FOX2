
param(
    [Parameter(Mandatory=$true)][string]$PublicationHead,
    [Parameter(Mandatory=$true)][string]$ExpectedScriptBlob,
    [Parameter(Mandatory=$true)][string]$Worktree
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Project = 'FOX2'
$WpId = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
$TaskId = 'FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01'
$Branch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01-20261022'
$ControlBranch = 'work/FOX2-DISPATCH-chat'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'

$SourceBase = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$TaskCommit = 'ce72a539cbdc53a100a9c8b78d2bffe29726c15d'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_cert_rework_a01/task.md'
$TaskBlob = '8c54daf0b25f5322c92d1207831c7f5fac172e2a'
$TaskSha256 = '05b8e571f1ba6557fb3898c14a9e23abf412f479adafa9e5f1bfd625a9e46b6f'

$PromptCommit = 'cddde72f8166dc81742a6f0c693adfff69b1bd00'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_cert_rework_a01/prompt.md'
$PromptBlob = '9265ab80d228bc3ab20217a5d946b8b1c6033cd2'
$PromptSha256 = '7967ff645188717812d46ef84815de2ac784c3d24a822c2204ab125074b69ace'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_cert_rework_a01/preexec.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_cert_rework_a01.json'
$FutureDispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERT-REWORK-A01-CODEX-001.json'
$HistoricalA04DispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001.json'

$LifecycleScriptPath = 'agent_bridge/scripts/certify_user_lifecycle.py'
$LifecycleScriptBlob = '7e62103ea4876833f67794a927a2a54622a59ea5'
$LifecycleTestPath = 'agent_bridge/tests/test_lifecycle_wpf_contract.py'
$LifecycleTestBlob = 'f80e50d59b1f1bb9ec9d553e84bbe7948971cb66'

$RegistryPath = 'docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json'
$RegistryBlob = '1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35'
$ResolutionPath = 'docs/governance/releases/FOX2_CURRENT_SOURCE_RESOLUTION_20261019.json'
$ResolutionBlob = '186fdbc72dc1b22e97330895142d68600591ac21'
$DictionaryPath = 'docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json'
$DictionaryBlob = '6c8f30e2e6b07f2e65e45c14faab99672d036083'
$PolicyPath = 'docs/governance/FOX2_POLICY_V2.0.0.md'
$PolicyBlob = '2d373f374f906bf7959062050bbeae5350b0c482'
$RoutingPath = 'docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md'
$RoutingBlob = '14d2e95e419cc67c3e0cf851cc806a96cf885b7e'
$ProtocolPath = 'docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md'
$ProtocolBlob = 'd34a022f2bda39a167a404c8530e57b30f337cb9'

$BuildPython = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B\agent_bridge\.build-venv\Scripts\python.exe'
$BuildPythonAlias = 'WORKTREES/FOX2-BRIDGE-DESKTOP-BATCH-B/agent_bridge/.build-venv/Scripts/python.exe'
$Model = 'gpt-6.1-sol'
$Reasoning = 'high'
$ExpectedCodexVersion = 'codex-cli 0.162.1'

function Require([bool]$Condition,[string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Safe([AllowNull()][object]$Value) {
    if ($null -eq $Value) { return '' }
    $v = [string]$Value
    $v = $v -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'
    $v = $v.Trim()
    if ($v.Length -gt 500) { $v = $v.Substring(0,500) }
    return $v
}

function Run {
    param(
        [Parameter(Mandatory=$true)][string]$File,
        [string[]]$ToolArgs = @(),
        [int]$Timeout = 60,
        [string]$Cwd = $Worktree,
        [AllowNull()][object]$InputText = $null
    )
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $File
    $psi.WorkingDirectory = $Cwd
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = ($null -ne $InputText)
    $psi.CreateNoWindow = $true
    foreach ($a in $ToolArgs) { [void]$psi.ArgumentList.Add([string]$a) }
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi
    try {
        Require ($p.Start()) ('TOOL_START_FAILED:' + $File)
        $outTask = $p.StandardOutput.ReadToEndAsync()
        $errTask = $p.StandardError.ReadToEndAsync()
        if ($null -ne $InputText) {
            $p.StandardInput.Write([string]$InputText)
            $p.StandardInput.Close()
        }
        if (-not $p.WaitForExit($Timeout * 1000)) {
            try { $p.Kill($true) } catch {}
            try { $p.WaitForExit() } catch {}
            throw ('TOOL_TIMEOUT:' + $File)
        }
        return [pscustomobject]@{
            Code = [int]$p.ExitCode
            Out = [string]$outTask.GetAwaiter().GetResult()
            Err = [string]$errTask.GetAwaiter().GetResult()
        }
    } finally {
        $p.Dispose()
    }
}

$GitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if ($null -eq $GitCommand) { $GitCommand = Get-Command git -ErrorAction Stop }
$Git = $GitCommand.Source
$CodexCommand = Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1
$Codex = $CodexCommand.Source

function G([string[]]$GitArgs) {
    $r = Run -File $Git -ToolArgs (@('-C',$Worktree) + $GitArgs) -Timeout 90
    Require ($r.Code -eq 0) ('GIT_FAILED:' + ($GitArgs -join ' ') + ':' + (Safe ($r.Err + ' ' + $r.Out)))
    return ([string]$r.Out).Trim()
}

function Get-RemoteHead([string]$BranchName) {
    $r = Run -File $Git -ToolArgs @('-C',$Worktree,'ls-remote','--refs','origin',('refs/heads/' + $BranchName)) -Timeout 60
    Require ($r.Code -eq 0) ('REMOTE_READ_FAILED:' + (Safe ($r.Err + ' ' + $r.Out)))
    $t = ([string]$r.Out).Trim()
    Require (-not [string]::IsNullOrWhiteSpace($t)) ('REMOTE_BRANCH_MISSING:' + $BranchName)
    return (($t -split '\s+')[0]).Trim()
}

function Get-Sha256([string]$Path) {
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Assert-NoTaskWriter {
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    foreach ($p in $processes) {
        $name = [string]$p.Name
        $line = [string]$p.CommandLine
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($name -ieq 'codex-windows-sandbox-service.exe') { continue }
        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper = ($name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$') -and ($line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)')
        if (-not ($isCodex -or $isWrapper)) { continue }
        foreach ($m in @($Worktree,$Branch,$TaskId,'PRESENTATION-LOCK-CERT-REWORK-A01')) {
            Require ($line.IndexOf($m,[StringComparison]::OrdinalIgnoreCase) -lt 0) 'COMPETING_TASK_WRITER'
        }
    }
}

Write-Output '=== FOX2 PRESENTATION LOCK CERT REWORK A01 PREEXEC ==='
Write-Output ('FOX2_TASK_ID=' + $TaskId)
Write-Output ('FOX2_SOURCE=' + $SourceBase)
Write-Output ('FOX2_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_AGENT_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'

Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'
Require (Test-Path -LiteralPath $Worktree -PathType Container) 'WORKTREE_MISSING'

$top = G @('rev-parse','--show-toplevel')
Require ([IO.Path]::GetFullPath($top).TrimEnd('\').Equals(
    [IO.Path]::GetFullPath($Worktree).TrimEnd('\'),
    [StringComparison]::OrdinalIgnoreCase
)) 'WORKTREE_IDENTITY_MISMATCH'
Require ((G @('branch','--show-current')) -ceq $Branch) 'WRONG_BRANCH'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_HEAD_MISMATCH'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY'
Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_HEAD_MISMATCH'

foreach ($fetchBranch in @($Branch,$ControlBranch,$GovernanceBranch)) {
    $refspec = '+refs/heads/' + $fetchBranch + ':refs/remotes/origin/' + $fetchBranch
    $fr = Run -File $Git -ToolArgs @('-C',$Worktree,'fetch','--no-tags','origin',$refspec) -Timeout 90
    Require ($fr.Code -eq 0) ('FETCH_FAILED:' + $fetchBranch)
}
Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_MOVED_DURING_FETCH'

$r = Run -File $Git -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$SourceBase,$PublicationHead) -Timeout 30
Require ($r.Code -eq 0) 'SOURCE_NOT_ANCESTOR'

$observedSetup = @((G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--')) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_.Trim().Replace('\','/') } | Sort-Object)
$expectedSetup = @($TaskPath,$PromptPath,$ScriptPath) | Sort-Object
Require (($observedSetup -join [char]10) -ceq ($expectedSetup -join [char]10)) 'SETUP_PATH_DRIFT'

$taskSpec = $TaskCommit + ':' + $TaskPath
$promptSpec = $PromptCommit + ':' + $PromptPath
Require ((G @('rev-parse',$taskSpec)) -ceq $TaskBlob) 'TASK_BLOB_MISMATCH'
Require ((G @('rev-parse',$promptSpec)) -ceq $PromptBlob) 'PROMPT_BLOB_MISMATCH'

$taskFull = Join-Path $Worktree ($TaskPath -replace '/', [IO.Path]::DirectorySeparatorChar)
$promptFull = Join-Path $Worktree ($PromptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
$scriptFull = Join-Path $Worktree ($ScriptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require ((Get-Sha256 $taskFull) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((Get-Sha256 $promptFull) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'
Require ((G @('hash-object','--no-filters',$scriptFull)) -ceq $ExpectedScriptBlob) 'PREEXEC_BLOB_MISMATCH'

$lifecycleScriptSpec = $SourceBase + ':' + $LifecycleScriptPath
$lifecycleTestSpec = $SourceBase + ':' + $LifecycleTestPath
Require ((G @('rev-parse',$lifecycleScriptSpec)) -ceq $LifecycleScriptBlob) 'LIFECYCLE_SCRIPT_SOURCE_DRIFT'
Require ((G @('rev-parse',$lifecycleTestSpec)) -ceq $LifecycleTestBlob) 'LIFECYCLE_TEST_SOURCE_DRIFT'
Require ([string]::IsNullOrWhiteSpace((G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--','agent_bridge')))) 'PRODUCT_DRIFT_BEFORE_CODING'

$govRef = 'refs/remotes/origin/' + $GovernanceBranch
foreach ($pair in @(
    @($RegistryPath,$RegistryBlob),
    @($ResolutionPath,$ResolutionBlob),
    @($DictionaryPath,$DictionaryBlob),
    @($PolicyPath,$PolicyBlob),
    @($RoutingPath,$RoutingBlob),
    @($ProtocolPath,$ProtocolBlob)
)) {
    $spec = $govRef + ':' + $pair[0]
    Require ((G @('rev-parse',$spec)) -ceq $pair[1]) ('GOVERNANCE_BLOB_MISMATCH:' + $pair[0])
}

$dispatchSpec = 'refs/remotes/origin/' + $ControlBranch + ':' + $FutureDispatchPath
$probe = Run -File $Git -ToolArgs @('-C',$Worktree,'cat-file','-e',$dispatchSpec) -Timeout 30
Require ($probe.Code -ne 0) 'FRESH_DISPATCH_ALREADY_EXISTS'

$historicalSpec = 'refs/remotes/origin/' + $ControlBranch + ':' + $HistoricalA04DispatchPath
$hist = Run -File $Git -ToolArgs @('-C',$Worktree,'cat-file','-e',$historicalSpec) -Timeout 30
Require ($hist.Code -eq 0) 'HISTORICAL_A04_DISPATCH_IDENTITY_MISSING'

Assert-NoTaskWriter

Require (Test-Path -LiteralPath $BuildPython -PathType Leaf) 'BUILD_PYTHON_MISSING'
$py = Run -File $BuildPython -ToolArgs @('-I','-B','-c','import sys,pytest; print(f"{sys.version_info.major}.{sys.version_info.minor}|{pytest.__version__}")') -Timeout 30
Require ($py.Code -eq 0) ('BUILD_PYTHON_PROBE_FAILED:' + (Safe ($py.Err + ' ' + $py.Out)))
$pyParts = ([string]$py.Out).Trim() -split '\|'
Require ($pyParts[0] -ceq '3.13') 'BUILD_PYTHON_VERSION_DRIFT'
$pytestVersion = if ($pyParts.Count -gt 1) { $pyParts[1] } else { $null }

$cv = Run -File $Codex -ToolArgs @('--version') -Timeout 30
Require ($cv.Code -eq 0) 'CODEX_VERSION_FAILED'
$codexVersion = ([string]$cv.Out).Trim()
Require ($codexVersion -ceq $ExpectedCodexVersion) 'CODEX_VERSION_DRIFT'

$login = Run -File $Codex -ToolArgs @('login','status') -Timeout 60
Require ($login.Code -eq 0) 'CODEX_AUTH_NOT_READY'

$probeDir = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-lock-rework-capacity-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($probeDir) | Out-Null
$last = Join-Path $probeDir 'last.txt'
$marker = 'FOX2_LOCK_REWORK_CAPACITY_OK'
try {
    $probeText = 'FOX2 coding-route capacity probe only. Do not inspect files or execute tools. Reply exactly ' + $marker + ' and nothing else.' + [Environment]::NewLine
    $cap = Run -File $Codex -ToolArgs @(
        'exec','--model',$Model,'--sandbox','read-only',
        '--config','approval_policy="never"',
        '--config','model_reasoning_effort="high"',
        '--skip-git-repo-check','--cd',$probeDir,
        '--output-last-message',$last,'-'
    ) -Timeout 240 -Cwd $probeDir -InputText $probeText
    Require ($cap.Code -eq 0) ('CODEX_CAPACITY_FAILED:' + (Safe ($cap.Err + ' ' + $cap.Out)))
    Require (([IO.File]::ReadAllText($last).Trim()) -ceq $marker) 'CODEX_CAPACITY_MARKER_MISMATCH'
} finally {
    try { if ([IO.Directory]::Exists($probeDir)) { [IO.Directory]::Delete($probeDir,$true) } } catch {}
}

$dryRef = 'HEAD:refs/heads/' + $Branch
$dry = Run -File $Git -ToolArgs @('-C',$Worktree,'push','--dry-run','origin',$dryRef) -Timeout 90
Require ($dry.Code -eq 0) ('GIT_PUSH_DRY_RUN_FAILED:' + (Safe ($dry.Err + ' ' + $dry.Out)))

Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_RECEIPT'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_MOVED_BEFORE_RECEIPT'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_BEFORE_RECEIPT'
Assert-NoTaskWriter

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require (-not (Test-Path -LiteralPath $receiptFull)) 'PREEXEC_RECEIPT_ALREADY_EXISTS'

$receipt = [ordered]@{
    schema_version = '1.0'
    receipt_type = 'FOX2_PREEXEC_RECEIPT'
    project = $Project
    wp_id = $WpId
    checked_at = [DateTime]::UtcNow.ToString('o')
    task_branch = $Branch
    receipt_path = $ReceiptPath
    source_head = $PublicationHead
    task_source = [ordered]@{
        git_path = $TaskPath
        git_commit_sha = $TaskCommit
        sha256 = $TaskSha256
    }
    status = 'PASS'
    capabilities = [ordered]@{
        source_binding = [ordered]@{ status='PASS'; material=$true; evidence=('accepted=' + $SourceBase + '; publication=' + $PublicationHead) }
        target_source_binding = [ordered]@{ status='PASS'; material=$true; evidence=('script_blob=' + $LifecycleScriptBlob + '; test_blob=' + $LifecycleTestBlob) }
        task_prompt_binding = [ordered]@{ status='PASS'; material=$true; evidence=('task=' + $TaskSha256 + '; prompt=' + $PromptSha256) }
        governance_source = [ordered]@{ status='PASS'; material=$true; evidence='Current Registry/Resolution/Dictionary/Policy/Routing/Protocol blobs verified' }
        worktree_clean = [ordered]@{ status='PASS'; material=$true; evidence='Dedicated rework worktree clean; no agent_bridge drift before coding' }
        one_writer = [ordered]@{ status='PASS'; material=$true; evidence='No task-scoped CODEX writer observed' }
        isolated_test_python = [ordered]@{ status='PASS'; material=$true; version=('3.13 / pytest ' + $pytestVersion); executable=$BuildPythonAlias; evidence='Existing compatible Python/pytest verified; no installation' }
        codex_cli = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; evidence='Pinned CODEX CLI verified' }
        codex_auth_capacity = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; exit_code=0; evidence='Authenticated read-only capacity probe PASS' }
        eligible_agent_route = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; exit_code=0; evidence='CODEX gpt-6.1-sol/high/FULL_ACCESS route ready' }
        git_push_permission = [ordered]@{ status='PASS'; material=$true; executable=$Git; evidence='Authorized branch push dry-run PASS' }
        fresh_attempt_dispatch_absent = [ordered]@{ status='PASS'; material=$true; evidence='Fresh rework Dispatch absent; historical consumed A04 Dispatch preserved/no-replay' }
    }
    blockers = @()
    worktree = [ordered]@{
        status = 'PASS'
        path = $Worktree
        competing_writer = 'NONE_OBSERVED'
        stale_receipt_cleanup = 'NOT_NEEDED'
    }
    candidate_route = [ordered]@{
        product = 'CODEX'
        model_policy = 'PINNED'
        model = $Model
        reasoning_effort = $Reasoning
        permission_profile = 'FULL_ACCESS'
    }
    dispatch_state = [ordered]@{
        executable_dispatch_published = $false
        dispatch_consumed = $false
    }
    agent_execution_started = $false
    notes = @(
        'BUILD rework only: presentation-lock certification semantics; no host lifecycle execution.',
        'Allowed code/test paths are exactly certify_user_lifecycle.py and test_lifecycle_wpf_contract.py.',
        'Historical A04 remains FAIL/consumed/no-replay; stable uninstall and reinstall remain NOT_RUN.',
        'No G3/G4/Canary/main/merge/provider/broker/LIVE authority.',
        'PASS permits CHAT intake and fresh assignment only; it does not mean code was changed or tests passed.'
    )
}

[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($receiptFull)) | Out-Null
$json = ($receipt | ConvertTo-Json -Depth 30).TrimEnd()
$json = $json -replace [char]13,''
$json = $json + [char]10
[IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))
$receiptSha256 = Get-Sha256 $receiptFull

& $Git -C $Worktree add -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_GIT_ADD_FAILED'

$staged = @((G @('diff','--cached','--name-only','--')) -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($staged.Count -eq 1 -and $staged[0].Replace('\','/') -ceq $ReceiptPath) 'RECEIPT_STAGED_PATH_DRIFT'

& $Git -C $Worktree diff --cached --check
Require ($LASTEXITCODE -eq 0) 'RECEIPT_DIFF_CHECK_FAILED'

& $Git -C $Worktree commit -m 'preexec(fox2): PASS presentation lock certification rework A01' -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_COMMIT_FAILED'

$receiptCommit = G @('rev-parse','HEAD')
$receiptSpec = $receiptCommit + ':' + $ReceiptPath
$receiptBlob = G @('rev-parse',$receiptSpec)

$pushRef = 'HEAD:refs/heads/' + $Branch
& $Git -C $Worktree push origin $pushRef
Require ($LASTEXITCODE -eq 0) 'RECEIPT_PUSH_FAILED'

$remote = Get-RemoteHead $Branch
Require ($remote -ceq $receiptCommit) 'RECEIPT_REMOTE_HEAD_MISMATCH'

$readbackRefspec = '+refs/heads/' + $Branch + ':refs/remotes/origin/' + $Branch
$fetch = Run -File $Git -ToolArgs @('-C',$Worktree,'fetch','--no-tags','origin',$readbackRefspec) -Timeout 90
Require ($fetch.Code -eq 0) 'RECEIPT_READBACK_FETCH_FAILED'
$remoteReceiptSpec = 'refs/remotes/origin/' + $Branch + ':' + $ReceiptPath
Require ((G @('rev-parse',$remoteReceiptSpec)) -ceq $receiptBlob) 'RECEIPT_REMOTE_BLOB_MISMATCH'

Write-Output ''
Write-Output '=== FOX2 PRESENTATION LOCK CERT REWORK A01 PREEXEC RESULT ==='
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_RECEIPT_SHA256=' + $receiptSha256)
Write-Output ('FOX2_SOURCE_SCRIPT_BLOB=' + $LifecycleScriptBlob)
Write-Output ('FOX2_SOURCE_TEST_BLOB=' + $LifecycleTestBlob)
Write-Output 'FOX2_TEST_PYTHON=3.13'
Write-Output ('FOX2_PYTEST_VERSION=' + $pytestVersion)
Write-Output ('FOX2_CODEX_VERSION=' + $codexVersion)
Write-Output 'FOX2_CODEX_ROUTE=PASS'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_PASS_TO_ASSIGN_THEN_FRESH_CODING_DISPATCH'
