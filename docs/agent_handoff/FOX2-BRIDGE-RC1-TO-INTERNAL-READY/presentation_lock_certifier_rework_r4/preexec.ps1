param(
    [Parameter(Mandatory=$true)][string]$PublicationHead,
    [Parameter(Mandatory=$true)][string]$ExpectedScriptBlob,
    [Parameter(Mandatory=$true)][string]$Worktree
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Project = 'FOX2'
$WpId = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
$TaskId = 'FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4'
$Branch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-20261022'
$StatusBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$ControlBranch = 'work/FOX2-DISPATCH-chat'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'

$SourceBase = '085cc8302e824dbccf9cbef80422ed48894b9cb4'

$TaskCommit = '6b6cc697ca35b35ade1ccdf363782a1f912a8936'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/task.md'
$TaskBlob = '90e6c18192cb594f408c9fd99b23da772e37c87f'
$TaskSha256 = '54c2075c0cce6faa90c4f23292ebe43f90e28c356089f4cbbe1e245b9a257456'

$PromptCommit = '2df8bd66f325a7a5eaee854e59f24db1ccfabf46'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/prompt.md'
$PromptBlob = '16d40d6c22175dedd944c75e4fb8844f41ac489c'
$PromptSha256 = 'bc10a5f348fbe8a5348db9159f93820841b8044bd5e4eb644093b892ea79b253'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/preexec.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r4.json'

$FutureDispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001.json'
$ConsumedR3DispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001.json'

$CertifierPath = 'agent_bridge/scripts/certify_user_lifecycle.py'
$CertifierBlob = '7e62103ea4876833f67794a927a2a54622a59ea5'
$TestPath = 'agent_bridge/tests/test_lifecycle_wpf_contract.py'
$TestBlob = 'f80e50d59b1f1bb9ec9d553e84bbe7948971cb66'

$MasterPlanCommit = 'ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56'
$ReusePlanCommit = 'da6fd27d78380db42fce155d634044c94a661229'
$V037ReviewCommit = '7cee0933ffd241deaa8e748bfeb626c56fab0cd0'
$R3FinalRecoveryCommit = '3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71'

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
$ReceiptSchemaPath = 'docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json'
$ReceiptSchemaBlob = '25fe465f82a16edf29ebf773a220969192f546e8'
$DispatchSchemaPath = 'docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json'
$DispatchSchemaBlob = '1692061941e2bef498515cd0e96b9b3046119ebb'

$TestPython = 'C:\Users\Fox Le\AppData\Local\Programs\Python\Python313\python.exe'
$TestPythonAlias = 'USERLOCAL/Programs/Python/Python313/python.exe'
$ExpectedCodexVersion = 'codex-cli 0.162.1'
$SelectedModel = 'gpt-6.1-sol'
$SelectedReasoning = 'medium'

function Require {
    param([bool]$Condition,[string]$Message)
    if (-not $Condition) { throw $Message }
}

function SafeText {
    param([AllowNull()][object]$Value)

    if ($null -eq $Value) { return '' }

    $v = [string]$Value
    $v = $v -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'
    $v = $v.Trim()

    if ($v.Length -gt 600) {
        $v = $v.Substring(0,600)
    }

    return $v
}

function Run-Native {
    param(
        [Parameter(Mandatory)][string]$File,
        [string[]]$ToolArgs = @(),
        [int]$TimeoutSeconds = 60,
        [string]$WorkingDirectory = $Worktree,
        [AllowNull()][object]$StandardInput = $null
    )

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $File
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = ($null -ne $StandardInput)
    $psi.CreateNoWindow = $true

    foreach ($a in $ToolArgs) {
        [void]$psi.ArgumentList.Add([string]$a)
    }

    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi

    try {
        Require ($p.Start()) ('TOOL_START_FAILED: ' + $File)

        $outTask = $p.StandardOutput.ReadToEndAsync()
        $errTask = $p.StandardError.ReadToEndAsync()

        if ($null -ne $StandardInput) {
            $p.StandardInput.Write([string]$StandardInput)
            $p.StandardInput.Close()
        }

        if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
            try { $p.Kill($true) } catch {}
            try { $p.WaitForExit() } catch {}
            throw ('TOOL_TIMEOUT: ' + $File)
        }

        return [pscustomobject]@{
            Code = [int]$p.ExitCode
            Out = [string]$outTask.GetAwaiter().GetResult()
            Err = [string]$errTask.GetAwaiter().GetResult()
        }
    }
    finally {
        $p.Dispose()
    }
}

$GitCommand = Get-Command git.exe -ErrorAction SilentlyContinue
if ($null -eq $GitCommand) {
    $GitCommand = Get-Command git -ErrorAction Stop
}
$Git = $GitCommand.Source

$CodexCommand = Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1
$Codex = $CodexCommand.Source

function G {
    param([string[]]$GitArgs)

    $r = Run-Native -File $Git -ToolArgs (@('-C',$Worktree) + $GitArgs) -TimeoutSeconds 90

    Require ($r.Code -eq 0) (
        'GIT_FAILED: ' +
        ($GitArgs -join ' ') +
        ' :: ' +
        (SafeText ($r.Err + ' ' + $r.Out))
    )

    return ([string]$r.Out).Trim()
}

function Get-RemoteHead {
    param([Parameter(Mandatory)][string]$BranchName)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,
        'ls-remote','--refs','origin',
        ('refs/heads/' + $BranchName)
    ) -TimeoutSeconds 60

    Require ($r.Code -eq 0) ('REMOTE_READ_FAILED: ' + $BranchName)

    $text = ([string]$r.Out).Trim()
    Require (-not [string]::IsNullOrWhiteSpace($text)) ('REMOTE_BRANCH_MISSING: ' + $BranchName)

    return (($text -split '\s+')[0]).Trim()
}

function Fetch-BranchHead {
    param(
        [Parameter(Mandatory)][string]$BranchName,
        [int]$MaxAttempts = 2
    )

    $expected = Get-RemoteHead $BranchName
    $detail = ''

    for ($attempt = 1; $attempt -le $MaxAttempts; $attempt++) {
        $r = Run-Native -File $Git -ToolArgs @(
            '-C',$Worktree,
            'fetch','--no-tags','origin',
            ('refs/heads/' + $BranchName)
        ) -TimeoutSeconds 90

        if ($r.Code -eq 0) {
            $observed = G @('rev-parse','FETCH_HEAD')
            Require ($observed -ceq $expected) ('FETCH_HEAD_MISMATCH: ' + $BranchName)
            return $observed
        }

        $detail = SafeText ($r.Err + ' ' + $r.Out)

        if ($attempt -lt $MaxAttempts) {
            Start-Sleep -Seconds 2
        }
    }

    throw ('FETCH_FAILED_AFTER_BOUNDED_RETRY: ' + $BranchName + ' :: ' + $detail)
}

function Get-Sha256 {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Assert-Ancestor {
    param(
        [Parameter(Mandatory)][string]$Ancestor,
        [Parameter(Mandatory)][string]$Descendant,
        [Parameter(Mandatory)][string]$Message
    )

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,
        'merge-base','--is-ancestor',
        $Ancestor,$Descendant
    ) -TimeoutSeconds 30

    Require ($r.Code -eq 0) $Message
}

function Assert-NoTaskWriter {
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)

    foreach ($process in $processes) {
        $name = [string]$process.Name
        $line = [string]$process.CommandLine

        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($name -ieq 'codex-windows-sandbox-service.exe') { continue }

        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper =
            ($name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$') -and
            ($line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)')

        if (-not ($isCodex -or $isWrapper)) { continue }

        foreach ($marker in @(
            $Worktree,
            $Branch,
            $TaskId,
            'PRESENTATION-LOCK-CERTIFIER-REWORK-R4'
        )) {
            Require (
                $line.IndexOf($marker,[StringComparison]::OrdinalIgnoreCase) -lt 0
            ) 'COMPETING_TASK_WRITER'
        }
    }
}

Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R4 PREEXEC ==='
Write-Output ('FOX2_TASK_ID=' + $TaskId)
Write-Output ('FOX2_SOURCE=' + $SourceBase)
Write-Output ('FOX2_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_SAFETY_OVERRIDE=NO'
Write-Output 'FOX2_SELECTED_ACTOR=CODEX'
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_R3_A01=CONSUMED_NO_RESULT_NO_REPLAY'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'

Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'
Require (Test-Path -LiteralPath $Worktree -PathType Container) 'WORKTREE_MISSING'
Require (Test-Path -LiteralPath $TestPython -PathType Leaf) 'TEST_PYTHON_MISSING'

$top = G @('rev-parse','--show-toplevel')

Require (
    [IO.Path]::GetFullPath($top).TrimEnd('\').Equals(
        [IO.Path]::GetFullPath($Worktree).TrimEnd('\'),
        [StringComparison]::OrdinalIgnoreCase
    )
) 'WORKTREE_IDENTITY_MISMATCH'

Require ((G @('branch','--show-current')) -ceq $Branch) 'WRONG_BRANCH'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_HEAD_MISMATCH'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @('status','--porcelain=v1','--untracked-files=all'))
    )
) 'WORKTREE_DIRTY'

Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_HEAD_MISMATCH'

Assert-Ancestor -Ancestor $SourceBase -Descendant $PublicationHead -Message 'SOURCE_NOT_ANCESTOR'

$observedSetup = @(
    (G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--')) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_.Trim().Replace('\','/') } |
    Sort-Object
)

$expectedSetup = @(
    $TaskPath,
    $PromptPath,
    $ScriptPath
) | Sort-Object

Require (
    ($observedSetup -join [char]10) -ceq
    ($expectedSetup -join [char]10)
) 'SETUP_PATH_DRIFT'

$taskFull = Join-Path $Worktree ($TaskPath -replace '/', '\')
$promptFull = Join-Path $Worktree ($PromptPath -replace '/', '\')
$scriptFull = Join-Path $Worktree ($ScriptPath -replace '/', '\')

Require ((G @('hash-object','--no-filters',$taskFull)) -ceq $TaskBlob) 'TASK_BLOB_MISMATCH'
Require ((Get-Sha256 $taskFull) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((G @('hash-object','--no-filters',$promptFull)) -ceq $PromptBlob) 'PROMPT_BLOB_MISMATCH'
Require ((Get-Sha256 $promptFull) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'
Require ((G @('hash-object','--no-filters',$scriptFull)) -ceq $ExpectedScriptBlob) 'PREEXEC_BLOB_MISMATCH'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--','agent_bridge'))
    )
) 'PRODUCT_DRIFT_BEFORE_CODING'

Require ((G @('rev-parse',($SourceBase + ':' + $CertifierPath))) -ceq $CertifierBlob) 'CERTIFIER_SOURCE_DRIFT'
Require ((G @('rev-parse',($SourceBase + ':' + $TestPath))) -ceq $TestBlob) 'TEST_SOURCE_DRIFT'

$statusHead = Fetch-BranchHead -BranchName $StatusBranch
$controlHead = Fetch-BranchHead -BranchName $ControlBranch
$govHead = Fetch-BranchHead -BranchName $GovernanceBranch

foreach ($commit in @(
    $MasterPlanCommit,
    $ReusePlanCommit,
    $V037ReviewCommit,
    $R3FinalRecoveryCommit
)) {
    Assert-Ancestor -Ancestor $commit -Descendant $statusHead -Message ('STATUS_LINEAGE_MISSING: ' + $commit)
}

foreach ($pair in @(
    @($RegistryPath,$RegistryBlob),
    @($ResolutionPath,$ResolutionBlob),
    @($DictionaryPath,$DictionaryBlob),
    @($PolicyPath,$PolicyBlob),
    @($RoutingPath,$RoutingBlob),
    @($ProtocolPath,$ProtocolBlob),
    @($ReceiptSchemaPath,$ReceiptSchemaBlob),
    @($DispatchSchemaPath,$DispatchSchemaBlob)
)) {
    Require (
        (G @('rev-parse',($govHead + ':' + $pair[0]))) -ceq
        $pair[1]
    ) ('GOVERNANCE_BLOB_MISMATCH: ' + $pair[0])
}

$futureDispatchSpec = $controlHead + ':' + $FutureDispatchPath
$futureDispatchProbe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,'cat-file','-e',$futureDispatchSpec
) -TimeoutSeconds 30

Require ($futureDispatchProbe.Code -ne 0) 'FRESH_R4_DISPATCH_ALREADY_EXISTS'

$r3DispatchSpec = $controlHead + ':' + $ConsumedR3DispatchPath
$r3DispatchProbe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,'cat-file','-e',$r3DispatchSpec
) -TimeoutSeconds 30

Require ($r3DispatchProbe.Code -eq 0) 'CONSUMED_R3_DISPATCH_HISTORY_MISSING'

Assert-NoTaskWriter

$pyProbeCode = @'
import importlib.metadata as m
import sys
import pytest
import jsonschema

print(
    f"{sys.version_info.major}.{sys.version_info.minor}"
    f"|{pytest.__version__}"
    f"|{m.version('jsonschema')}"
)
'@

$py = Run-Native -File $TestPython -ToolArgs @(
    '-I','-B','-c',$pyProbeCode
) -TimeoutSeconds 30

Require ($py.Code -eq 0) ('TEST_PYTHON_PROBE_FAILED: ' + (SafeText ($py.Err + ' ' + $py.Out)))

$pyParts = ([string]$py.Out).Trim() -split '\|'

Require ($pyParts.Count -eq 3) 'TEST_PYTHON_PROBE_SHAPE'
Require ($pyParts[0] -ceq '3.13') 'TEST_PYTHON_VERSION_DRIFT'
Require ($pyParts[1] -ceq '8.3.5') 'PYTEST_VERSION_DRIFT'
Require ($pyParts[2] -ceq '4.26.0') 'JSONSCHEMA_VERSION_DRIFT'

$cv = Run-Native -File $Codex -ToolArgs @('--version') -TimeoutSeconds 30
Require ($cv.Code -eq 0) 'CODEX_VERSION_FAILED'

$codexVersion = ([string]$cv.Out).Trim()
Require ($codexVersion -ceq $ExpectedCodexVersion) 'CODEX_VERSION_DRIFT'

$login = Run-Native -File $Codex -ToolArgs @('login','status') -TimeoutSeconds 60
Require ($login.Code -eq 0) 'CODEX_AUTH_NOT_READY'

$probeDir = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-r4-medium-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($probeDir) | Out-Null

$last = Join-Path $probeDir 'last.txt'
$marker = 'FOX2_CERTIFIER_R4_MEDIUM_CAPACITY_OK'

try {
    $probeText =
        'FOX2 selected-route capacity probe only. ' +
        'Do not inspect files or execute tools. ' +
        'Reply exactly ' +
        $marker +
        ' and nothing else.' +
        [Environment]::NewLine

    $cap = Run-Native -File $Codex -ToolArgs @(
        'exec',
        '--model',$SelectedModel,
        '--sandbox','read-only',
        '--config','approval_policy="never"',
        '--config','model_reasoning_effort="medium"',
        '--skip-git-repo-check',
        '--cd',$probeDir,
        '--output-last-message',$last,
        '-'
    ) -TimeoutSeconds 240 -WorkingDirectory $probeDir -StandardInput $probeText

    Require ($cap.Code -eq 0) ('CODEX_MEDIUM_CAPACITY_FAILED: ' + (SafeText ($cap.Err + ' ' + $cap.Out)))

    Require (
        ([IO.File]::ReadAllText($last).Trim()) -ceq
        $marker
    ) 'CODEX_MEDIUM_CAPACITY_MARKER_MISMATCH'
}
finally {
    try {
        if ([IO.Directory]::Exists($probeDir)) {
            [IO.Directory]::Delete($probeDir,$true)
        }
    }
    catch {}
}

$dry = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'push','--dry-run',
    'origin',
    ('HEAD:refs/heads/' + $Branch)
) -TimeoutSeconds 90

Require ($dry.Code -eq 0) ('GIT_PUSH_DRY_RUN_FAILED: ' + (SafeText ($dry.Err + ' ' + $dry.Out)))

Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_RECEIPT'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_MOVED_BEFORE_RECEIPT'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @('status','--porcelain=v1','--untracked-files=all'))
    )
) 'WIP_BEFORE_RECEIPT'

Assert-NoTaskWriter

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', '\')
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
        source_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('accepted_source=' + $SourceBase + '; publication=' + $PublicationHead)
        }
        route_assessment_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence='COMPLEXITY=MEDIUM; EXECUTION_RISK=MEDIUM; SAFETY_OVERRIDE=NO; selected CODEX/gpt-6.1-sol/medium'
        }
        selected_route_verification = [ordered]@{
            status='PASS'
            material=$true
            version=$codexVersion
            executable=$Codex
            exit_code=0
            evidence='Fresh gpt-6.1-sol/medium read-only capacity probe PASS'
        }
        test_python = [ordered]@{
            status='PASS'
            material=$true
            version=('Python ' + $pyParts[0] + '; pytest ' + $pyParts[1] + '; jsonschema ' + $pyParts[2])
            executable=$TestPythonAlias
            evidence='Fresh current existing Python test runner capability PASS; no install/upgrade'
        }
        certifier_source_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('certifier_blob=' + $CertifierBlob + '; test_blob=' + $TestBlob)
        }
        task_prompt_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('task_sha256=' + $TaskSha256 + '; prompt_sha256=' + $PromptSha256)
        }
        recovery_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('R3_A01_CONSUMED_NO_RESULT_NO_REPLAY=' + $R3FinalRecoveryCommit)
        }
        reuse_plan_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('master_plan=' + $MasterPlanCommit + '; reuse_plan=' + $ReusePlanCommit + '; v037_review=' + $V037ReviewCommit)
        }
        governance_source = [ordered]@{
            status='PASS'
            material=$true
            evidence='Current Registry/Resolution/Dictionary/Policy/Routing/Protocol/ReceiptSchema/DispatchSchema blobs verified'
        }
        worktree_clean = [ordered]@{
            status='PASS'
            material=$true
            evidence='Dedicated R4 worktree clean; zero agent_bridge drift before coding'
        }
        one_writer = [ordered]@{
            status='PASS'
            material=$true
            evidence='No R4 task-scoped CODEX writer observed'
        }
        codex_cli = [ordered]@{
            status='PASS'
            material=$true
            version=$codexVersion
            executable=$Codex
            evidence='Pinned CODEX CLI verified'
        }
        git_push_permission = [ordered]@{
            status='PASS'
            material=$true
            executable=$Git
            evidence='Authorized R4 branch push dry-run PASS'
        }
        no_replay = [ordered]@{
            status='PASS'
            material=$true
            evidence='Consumed R3 Dispatch remains historical; fresh R4 Dispatch absent'
        }
        host_lifecycle_isolation = [ordered]@{
            status='PASS'
            material=$true
            evidence='R4 certifier-only correction; no package build/install/host lifecycle/A05/G3/G4/Canary'
        }
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
        model = $SelectedModel
        reasoning_effort = $SelectedReasoning
        permission_profile = 'FULL_ACCESS'
    }
    dispatch_state = [ordered]@{
        executable_dispatch_published = $false
        dispatch_consumed = $false
    }
    agent_execution_started = $false
    notes = @(
        'R4 is a fresh attempt after R3 A01 CONSUMED_NO_RESULT; R3 Dispatch is no-replay.',
        'Unchanged A04/R3 PASS evidence is reused; only new-attempt/time-dependent gates were rechecked.',
        'FOX2 Skills v0.3.7 route assessment selected Medium before PreExec.',
        'PreExec verifies the selected Medium route and does not classify complexity.',
        'No package build/install/host lifecycle/A05/G3/G4/Canary authority.',
        'Receipt is validated against current Receipt Schema v1 before publication.',
        'PASS permits CHAT intake and one fresh R4 coding Dispatch only.'
    )
}

[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($receiptFull)) | Out-Null

$json = ($receipt | ConvertTo-Json -Depth 30).TrimEnd()
$json = $json -replace [char]13,''
$json = $json + [char]10

[IO.File]::WriteAllText(
    $receiptFull,
    $json,
    [Text.UTF8Encoding]::new($false)
)

$receiptSha256 = Get-Sha256 $receiptFull

$schemaText = G @('show',($govHead + ':' + $ReceiptSchemaPath))
$schemaTemp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-r4-preflight-schema-' + [Guid]::NewGuid().ToString('N') + '.json')

try {
    [IO.File]::WriteAllText(
        $schemaTemp,
        $schemaText + [char]10,
        [Text.UTF8Encoding]::new($false)
    )

    $validateCode = @'
import json
import sys
import jsonschema

schema_path, receipt_path = sys.argv[1], sys.argv[2]

with open(schema_path, "r", encoding="utf-8") as f:
    schema = json.load(f)

with open(receipt_path, "r", encoding="utf-8") as f:
    receipt = json.load(f)

jsonschema.Draft202012Validator.check_schema(schema)

validator = jsonschema.Draft202012Validator(
    schema,
    format_checker=jsonschema.FormatChecker(),
)

errors = sorted(
    validator.iter_errors(receipt),
    key=lambda error: list(error.absolute_path),
)

if errors:
    for error in errors:
        print(
            "/".join(str(item) for item in error.absolute_path)
            + ": "
            + error.message,
            file=sys.stderr,
        )
    raise SystemExit(3)

print("FOX2_RECEIPT_SCHEMA_VALID")
'@

    $schemaCheck = Run-Native -File $TestPython -ToolArgs @(
        '-I','-B','-c',
        $validateCode,
        $schemaTemp,
        $receiptFull
    ) -TimeoutSeconds 60

    if (
        $schemaCheck.Code -ne 0 -or
        ([string]$schemaCheck.Out).Trim() -cne 'FOX2_RECEIPT_SCHEMA_VALID'
    ) {
        try { Remove-Item -LiteralPath $receiptFull -Force -ErrorAction SilentlyContinue } catch {}
        throw ('RECEIPT_SCHEMA_VALIDATION_FAILED: ' + (SafeText ($schemaCheck.Err + ' ' + $schemaCheck.Out)))
    }
}
finally {
    try { Remove-Item -LiteralPath $schemaTemp -Force -ErrorAction SilentlyContinue } catch {}
}

Write-Output 'FOX2_RECEIPT_SCHEMA_VALIDATION=PASS'

& $Git -C $Worktree add -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_GIT_ADD_FAILED'

$staged = @(
    (G @('diff','--cached','--name-only','--')) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
)

Require (
    $staged.Count -eq 1 -and
    $staged[0].Replace('\','/') -ceq $ReceiptPath
) 'RECEIPT_STAGED_PATH_DRIFT'

& $Git -C $Worktree diff --cached --check
Require ($LASTEXITCODE -eq 0) 'RECEIPT_DIFF_CHECK_FAILED'

& $Git -C $Worktree commit -m 'preexec(fox2): PASS certifier rework R4' -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_COMMIT_FAILED'

$receiptCommit = G @('rev-parse','HEAD')
$receiptBlob = G @('rev-parse',($receiptCommit + ':' + $ReceiptPath))

& $Git -C $Worktree push origin ('HEAD:refs/heads/' + $Branch)
Require ($LASTEXITCODE -eq 0) 'RECEIPT_PUSH_FAILED'

Require ((Get-RemoteHead $Branch) -ceq $receiptCommit) 'RECEIPT_REMOTE_HEAD_MISMATCH'

$readbackHead = Fetch-BranchHead -BranchName $Branch
Require ($readbackHead -ceq $receiptCommit) 'RECEIPT_READBACK_HEAD_MISMATCH'
Require ((G @('rev-parse',($receiptCommit + ':' + $ReceiptPath))) -ceq $receiptBlob) 'RECEIPT_REMOTE_BLOB_MISMATCH'

Write-Output ''
Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R4 PREEXEC RESULT ==='
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_RECEIPT_SHA256=' + $receiptSha256)
Write-Output ('FOX2_TEST_PYTHON_ALIAS=' + $TestPythonAlias)
Write-Output ('FOX2_TEST_PYTHON_VERSION=' + $pyParts[0])
Write-Output ('FOX2_PYTEST_VERSION=' + $pyParts[1])
Write-Output ('FOX2_JSONSCHEMA_VERSION=' + $pyParts[2])
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_SAFETY_OVERRIDE=NO'
Write-Output 'FOX2_SELECTED_ACTOR=CODEX'
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_SELECTED_ROUTE_VERIFICATION=PASS'
Write-Output 'FOX2_R3_A01=CONSUMED_NO_RESULT_NO_REPLAY'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_PASS_TO_ASSIGN_THEN_FRESH_R4_DISPATCH'
