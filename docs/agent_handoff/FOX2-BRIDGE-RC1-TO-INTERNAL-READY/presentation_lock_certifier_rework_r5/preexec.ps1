param(
    [Parameter(Mandatory=$true)][string]$PublicationHead,
    [Parameter(Mandatory=$true)][string]$ExpectedScriptBlob,
    [Parameter(Mandatory=$true)][string]$Worktree
)

#requires -Version 7.0
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Project = 'FOX2'
$WpId = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
$TaskId = 'FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5'
$Branch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022'
$StatusBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$ControlBranch = 'work/FOX2-DISPATCH-chat'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'

$AcceptedProductSource = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$SalvageBase = 'd997756b5f4cfaa7e442dfc5d929093782b7a90f'
$R4ReviewCommit = '07ce66987345859f978c06fbb4abbdeeaa0ff04c'
$R4ConsumedDispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001.json'

$TaskCommit = '8fb7d23217067474488203aceef094b838e828ab'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r5/task.md'
$TaskBlob = 'cbc546dcad97c9dcab02d6e82b68eef163d2b17d'
$TaskSha256 = 'd7054edbb574661df9cbba08dcdf282cf175d2cd5496a5dc7b2c2af6cdaa7062'

$PromptCommit = 'b33d0610649cbfb466bb5febd1e295f91f35e53d'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r5/prompt.md'
$PromptBlob = '10b95e130289752701c790beb41b2d0cde9af017'
$PromptSha256 = 'ffeaccd6a60eb4b56da907bf1092bb3889b38a80a8cd957ca5d8a90860e79fba'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r5/preexec.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r5.json'
$FutureDispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-CODEX-001.json'

$CertifierPath = 'agent_bridge/scripts/certify_user_lifecycle.py'
$CertifierBlob = 'cc469b9e29301db488605d621c8cbb37d9c442e0'
$TestPath = 'agent_bridge/tests/test_lifecycle_wpf_contract.py'
$TestBlob = 'e2d6551ca119e72a8cb59f38f50bded09a276731'

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
    if ($v.Length -gt 800) { $v = $v.Substring(0,800) }
    return $v.Trim()
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

    foreach ($a in $ToolArgs) { [void]$psi.ArgumentList.Add([string]$a) }

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
if ($null -eq $GitCommand) { $GitCommand = Get-Command git -ErrorAction Stop }
$Git = $GitCommand.Source

$CodexCommand = Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1
$Codex = $CodexCommand.Source

function G {
    param([string[]]$GitArgs)

    $r = Run-Native -File $Git -ToolArgs (@('-C',$Worktree) + $GitArgs) -TimeoutSeconds 90
    Require ($r.Code -eq 0) ('GIT_FAILED: ' + ($GitArgs -join ' ') + ' :: ' + (SafeText ($r.Err + ' ' + $r.Out)))
    return ([string]$r.Out).Trim()
}

function Get-RemoteHead {
    param([Parameter(Mandatory)][string]$BranchName)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,'ls-remote','--refs','origin',('refs/heads/' + $BranchName)
    ) -TimeoutSeconds 60

    Require ($r.Code -eq 0) ('REMOTE_READ_FAILED: ' + $BranchName)
    $text = ([string]$r.Out).Trim()
    Require (-not [string]::IsNullOrWhiteSpace($text)) ('REMOTE_BRANCH_MISSING: ' + $BranchName)
    return (($text -split '\s+')[0]).Trim()
}

function Fetch-BranchHead {
    param([Parameter(Mandatory)][string]$BranchName)

    $expected = Get-RemoteHead $BranchName
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        $r = Run-Native -File $Git -ToolArgs @(
            '-C',$Worktree,'fetch','--no-tags','origin',('refs/heads/' + $BranchName)
        ) -TimeoutSeconds 90

        if ($r.Code -eq 0) {
            $observed = G @('rev-parse','FETCH_HEAD')
            Require ($observed -ceq $expected) ('FETCH_HEAD_MISMATCH: ' + $BranchName)
            return $observed
        }

        if ($attempt -lt 2) { Start-Sleep -Seconds 2 }
    }

    throw ('FETCH_FAILED_AFTER_BOUNDED_RETRY: ' + $BranchName)
}

function Assert-Ancestor {
    param([string]$Ancestor,[string]$Descendant,[string]$Message)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,'merge-base','--is-ancestor',$Ancestor,$Descendant
    ) -TimeoutSeconds 30
    Require ($r.Code -eq 0) $Message
}

function Get-Sha256 {
    param([Parameter(Mandatory)][string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Assert-NoTaskWriter {
    foreach ($process in @(Get-CimInstance Win32_Process -ErrorAction Stop)) {
        $name = [string]$process.Name
        $line = [string]$process.CommandLine
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        if ($name -ieq 'codex-windows-sandbox-service.exe') { continue }

        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper =
            ($name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$') -and
            ($line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)')

        if (-not ($isCodex -or $isWrapper)) { continue }

        foreach ($marker in @($Worktree,$Branch,$TaskId,'PRESENTATION-LOCK-CERTIFIER-REWORK-R5')) {
            Require (
                $line.IndexOf($marker,[StringComparison]::OrdinalIgnoreCase) -lt 0
            ) 'COMPETING_R5_TASK_WRITER'
        }
    }
}

Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R5 PREEXEC ==='
Write-Output ('FOX2_TASK_ID=' + $TaskId)
Write-Output ('FOX2_ACCEPTED_PRODUCT_SOURCE=' + $AcceptedProductSource)
Write-Output ('FOX2_SALVAGE_BASE=' + $SalvageBase)
Write-Output ('FOX2_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=EASY'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_SAFETY_OVERRIDE=NO'
Write-Output 'FOX2_SELECTED_ACTOR=CODEX'
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_R4_RESULT=CHAT_REWORK_NO_REPLAY'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'

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
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY'
Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_HEAD_MISMATCH'

Assert-Ancestor $SalvageBase $PublicationHead 'SALVAGE_BASE_NOT_ANCESTOR'
Assert-Ancestor $AcceptedProductSource $SalvageBase 'ACCEPTED_PRODUCT_LINEAGE_MISSING'

$observedSetup = @(
    (G @('diff','--name-only',($SalvageBase + '..' + $PublicationHead),'--')) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_.Trim().Replace('\','/') } |
    Sort-Object
)

$expectedSetup = @($TaskPath,$PromptPath,$ScriptPath) | Sort-Object

Require (
    ($observedSetup -join [char]10) -ceq
    ($expectedSetup -join [char]10)
) 'SETUP_PATH_DRIFT'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @('diff','--name-only',($SalvageBase + '..' + $PublicationHead),'--','agent_bridge'))
    )
) 'PRODUCT_DRIFT_BEFORE_R5_CODING'

$taskFull = Join-Path $Worktree ($TaskPath -replace '/', '\')
$promptFull = Join-Path $Worktree ($PromptPath -replace '/', '\')
$scriptFull = Join-Path $Worktree ($ScriptPath -replace '/', '\')

Require ((G @('hash-object','--no-filters',$taskFull)) -ceq $TaskBlob) 'TASK_BLOB_MISMATCH'
Require ((Get-Sha256 $taskFull) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((G @('hash-object','--no-filters',$promptFull)) -ceq $PromptBlob) 'PROMPT_BLOB_MISMATCH'
Require ((Get-Sha256 $promptFull) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'
Require ((G @('hash-object','--no-filters',$scriptFull)) -ceq $ExpectedScriptBlob) 'PREEXEC_BLOB_MISMATCH'

Require ((G @('rev-parse',($SalvageBase + ':' + $CertifierPath))) -ceq $CertifierBlob) 'CERTIFIER_SALVAGE_BLOB_DRIFT'
Require ((G @('rev-parse',($SalvageBase + ':' + $TestPath))) -ceq $TestBlob) 'TEST_SALVAGE_BLOB_DRIFT'

$statusHead = Fetch-BranchHead $StatusBranch
$controlHead = Fetch-BranchHead $ControlBranch
$govHead = Fetch-BranchHead $GovernanceBranch

Assert-Ancestor $R4ReviewCommit $statusHead 'R4_CHAT_REVIEW_NOT_CURRENT'

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
        (G @('rev-parse',($govHead + ':' + $pair[0]))) -ceq $pair[1]
    ) ('GOVERNANCE_BLOB_MISMATCH: ' + $pair[0])
}

$r4DispatchProbe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,'cat-file','-e',($controlHead + ':' + $R4ConsumedDispatchPath)
) -TimeoutSeconds 30
Require ($r4DispatchProbe.Code -eq 0) 'R4_CONSUMED_DISPATCH_HISTORY_MISSING'

$r5DispatchProbe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,'cat-file','-e',($controlHead + ':' + $FutureDispatchPath)
) -TimeoutSeconds 30
Require ($r5DispatchProbe.Code -ne 0) 'FRESH_R5_DISPATCH_ALREADY_EXISTS'

Assert-NoTaskWriter

$pyCode = @'
import importlib.metadata as m
import sys
import pytest
import jsonschema
print(f"{sys.version_info.major}.{sys.version_info.minor}|{pytest.__version__}|{m.version('jsonschema')}")
'@

$py = Run-Native -File $TestPython -ToolArgs @('-I','-B','-c',$pyCode) -TimeoutSeconds 30
Require ($py.Code -eq 0) ('TEST_PYTHON_PROBE_FAILED: ' + (SafeText ($py.Err + ' ' + $py.Out)))
$parts = ([string]$py.Out).Trim() -split '\|'
Require ($parts.Count -eq 3) 'TEST_PYTHON_PROBE_SHAPE'
Require ($parts[0] -ceq '3.13') 'TEST_PYTHON_VERSION_DRIFT'
Require ($parts[1] -ceq '8.3.5') 'PYTEST_VERSION_DRIFT'
Require ($parts[2] -ceq '4.26.0') 'JSONSCHEMA_VERSION_DRIFT'

$cv = Run-Native -File $Codex -ToolArgs @('--version') -TimeoutSeconds 30
Require ($cv.Code -eq 0) 'CODEX_VERSION_FAILED'
$codexVersion = ([string]$cv.Out).Trim()
Require ($codexVersion -ceq $ExpectedCodexVersion) 'CODEX_VERSION_DRIFT'

$login = Run-Native -File $Codex -ToolArgs @('login','status') -TimeoutSeconds 60
Require ($login.Code -eq 0) 'CODEX_AUTH_NOT_READY'

$probeDir = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-r5-medium-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($probeDir) | Out-Null
$last = Join-Path $probeDir 'last.txt'
$marker = 'FOX2_CERTIFIER_R5_MEDIUM_CAPACITY_OK'

try {
    $probeText =
        'FOX2 selected-route capacity probe only. Do not inspect files or execute tools. Reply exactly ' +
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
    Require (([IO.File]::ReadAllText($last).Trim()) -ceq $marker) 'CODEX_MEDIUM_CAPACITY_MARKER_MISMATCH'
}
finally {
    try {
        if ([IO.Directory]::Exists($probeDir)) { [IO.Directory]::Delete($probeDir,$true) }
    }
    catch {}
}

$dry = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,'push','--dry-run','origin',('HEAD:refs/heads/' + $Branch)
) -TimeoutSeconds 90
Require ($dry.Code -eq 0) ('GIT_PUSH_DRY_RUN_FAILED: ' + (SafeText ($dry.Err + ' ' + $dry.Out)))

Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_RECEIPT'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_MOVED_BEFORE_RECEIPT'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_BEFORE_RECEIPT'
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
            evidence=('accepted_product=' + $AcceptedProductSource + '; unaccepted_salvage_base=' + $SalvageBase)
        }
        r4_result_review_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('CHAT_REWORK=' + $R4ReviewCommit + '; R4 Dispatch remains consumed/no-replay')
        }
        route_assessment_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence='COMPLEXITY=EASY; EXECUTION_RISK=MEDIUM; SAFETY_OVERRIDE=NO; selected CODEX/gpt-6.1-sol/medium'
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
            version=('Python ' + $parts[0] + '; pytest ' + $parts[1] + '; jsonschema ' + $parts[2])
            executable=$TestPythonAlias
            evidence='Current existing test runner capability PASS; no install/upgrade'
        }
        salvage_source_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('certifier_blob=' + $CertifierBlob + '; test_blob=' + $TestBlob)
        }
        task_prompt_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('task_sha256=' + $TaskSha256 + '; prompt_sha256=' + $PromptSha256)
        }
        governance_source = [ordered]@{
            status='PASS'
            material=$true
            evidence='Current Registry/Resolution/Dictionary/Policy/Routing/Protocol/ReceiptSchema/DispatchSchema blobs verified'
        }
        worktree_clean = [ordered]@{
            status='PASS'
            material=$true
            evidence='Dedicated R5 worktree clean; no agent_bridge drift relative to R4 salvage base before coding'
        }
        one_writer = [ordered]@{
            status='PASS'
            material=$true
            evidence='No R5 task-scoped CODEX writer observed'
        }
        git_push_permission = [ordered]@{
            status='PASS'
            material=$true
            executable=$Git
            evidence='R5 branch push dry-run PASS'
        }
        no_replay = [ordered]@{
            status='PASS'
            material=$true
            evidence='R4 Dispatch remains consumed; fresh R5 Dispatch absent'
        }
        host_lifecycle_isolation = [ordered]@{
            status='PASS'
            material=$true
            evidence='R5 is two-file certifier correction only; no package/host lifecycle/A05/G3/G4/Canary'
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
        'R5 is a fresh bounded attempt after R4 CHAT_REWORK; R4 Dispatch is no-replay.',
        'R4 result SHA is unaccepted salvage input, not accepted product source.',
        'Only new-attempt/time-dependent gates were rechecked.',
        'Receipt is validated against current Receipt Schema v1 before publication.',
        'PASS permits CHAT intake and one fresh R5 coding Dispatch only.'
    )
}

[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($receiptFull)) | Out-Null
$json = ($receipt | ConvertTo-Json -Depth 30).TrimEnd()
$json = $json -replace [char]13,''
$json = $json + [char]10
[IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))
$receiptSha256 = Get-Sha256 $receiptFull

$schemaText = G @('show',($govHead + ':' + $ReceiptSchemaPath))
$schemaTemp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-r5-receipt-schema-' + [Guid]::NewGuid().ToString('N') + '.json')

try {
    [IO.File]::WriteAllText($schemaTemp,$schemaText + [char]10,[Text.UTF8Encoding]::new($false))

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
validator = jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker())
errors = sorted(validator.iter_errors(receipt),key=lambda e:list(e.absolute_path))
if errors:
    for error in errors:
        print("/".join(str(i) for i in error.absolute_path) + ": " + error.message,file=sys.stderr)
    raise SystemExit(3)
print("FOX2_RECEIPT_SCHEMA_VALID")
'@

    $schemaCheck = Run-Native -File $TestPython -ToolArgs @(
        '-I','-B','-c',$validateCode,$schemaTemp,$receiptFull
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

& $Git -C $Worktree commit -m 'preexec(fox2): PASS certifier rework R5' -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_COMMIT_FAILED'

$receiptCommit = G @('rev-parse','HEAD')
$receiptBlob = G @('rev-parse',($receiptCommit + ':' + $ReceiptPath))

& $Git -C $Worktree push origin ('HEAD:refs/heads/' + $Branch)
Require ($LASTEXITCODE -eq 0) 'RECEIPT_PUSH_FAILED'
Require ((Get-RemoteHead $Branch) -ceq $receiptCommit) 'RECEIPT_REMOTE_HEAD_MISMATCH'

Write-Output ''
Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R5 PREEXEC RESULT ==='
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_RECEIPT_SHA256=' + $receiptSha256)
Write-Output ('FOX2_TEST_PYTHON_ALIAS=' + $TestPythonAlias)
Write-Output ('FOX2_TEST_PYTHON_VERSION=' + $parts[0])
Write-Output ('FOX2_PYTEST_VERSION=' + $parts[1])
Write-Output ('FOX2_JSONSCHEMA_VERSION=' + $parts[2])
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=EASY'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_SELECTED_ACTOR=CODEX'
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_SELECTED_ROUTE_VERIFICATION=PASS'
Write-Output 'FOX2_R4_RESULT=CHAT_REWORK_NO_REPLAY'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_PASS_TO_ASSIGN_THEN_FRESH_R5_DISPATCH'
