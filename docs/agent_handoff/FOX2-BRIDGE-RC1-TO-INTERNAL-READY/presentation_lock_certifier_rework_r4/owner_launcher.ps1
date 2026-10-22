param()

#requires -Version 7.0
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# FOX2 immutable Owner launcher.
# Execute through the verified bootstrap only.
# Do not paste this file body line-by-line into an interactive shell.

$Repo = 'C:\Projects\FOX2'
$WT = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-20261022'

$TaskBranch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-20261022'
$StatusBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$ControlBranch = 'work/FOX2-DISPATCH-chat'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'

$AcceptedSource = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$RuntimeBase = '35aa18ccabcc6f7d4b889ed213c075fc314d45d0'

$TaskCommit = '6b6cc697ca35b35ade1ccdf363782a1f912a8936'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/task.md'
$TaskBlob = '90e6c18192cb594f408c9fd99b23da772e37c87f'
$TaskSha256 = '54c2075c0cce6faa90c4f23292ebe43f90e28c356089f4cbbe1e245b9a257456'

$PromptCommit = '2df8bd66f325a7a5eaee854e59f24db1ccfabf46'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r4/prompt.md'
$PromptBlob = '16d40d6c22175dedd944c75e4fb8844f41ac489c'
$PromptSha256 = 'bc10a5f348fbe8a5348db9159f93820841b8044bd5e4eb644093b892ea79b253'

$ReceiptCommit = '35aa18ccabcc6f7d4b889ed213c075fc314d45d0'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r4.json'
$ReceiptBlob = '13163c5a14812b71253e094d7dc8341bc0bbacf8'
$ReceiptSha256 = 'e183bfef170fc98d826fbe48fe4eb8cef58648d4b979b211c6ab02546e8aa6b8'

$PassCommit = 'ab04ab51a06dfd712d5031d8e90e7bcd46f142c6'
$PassPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PRESENTATION_LOCK_CERTIFIER_R4_PASS_TO_ASSIGN_20261022.md'
$PassBlob = '0d85e82e45611e4188ee942730fd80a94305a5a6'
$PassSha256 = '684825dd82b2ad07cbc2ec2351623086bb6c06d0feb75a6e574ad5a451303c66'

$TransportRecoveryCommit = '48ee3101697463adbebf78d877cab25f8ee2a707'

$DispatchId = 'FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001'
$DispatchCommit = '4655d1c2505ab4feb425efc9a09ceb0820631d3c'
$DispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4-CODEX-001.json'
$DispatchBlob = '514294c290c2cc9235fd2b616a948e9e1bf46fe9'
$DispatchSha256 = '33014d81c55fb3c98f710cfddf5ba659ea271c624b81960e30c7f1f6a0121009'

$ConsumedR3DispatchId = 'FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001'
$R3FinalRecovery = '3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71'

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

$CertifierPath = 'agent_bridge/scripts/certify_user_lifecycle.py'
$CertifierBlob = '7e62103ea4876833f67794a927a2a54622a59ea5'
$TestPath = 'agent_bridge/tests/test_lifecycle_wpf_contract.py'
$TestBlob = 'f80e50d59b1f1bb9ec9d553e84bbe7948971cb66'

$ReportPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md'
$ManifestPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json'
$EvidencePrefix = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/presentation_lock_certifier_rework_r4/'

$TestPython = 'C:\Users\Fox Le\AppData\Local\Programs\Python\Python313\python.exe'
$ExpectedCodexVersion = 'codex-cli 0.162.1'
$Model = 'gpt-6.1-sol'
$Reasoning = 'medium'

function Require {
    param([bool]$Condition,[string]$Message)
    if (-not $Condition) { throw $Message }
}

function Run-Native {
    param(
        [Parameter(Mandatory)][string]$File,
        [string[]]$ToolArgs = @(),
        [int]$TimeoutSeconds = 60,
        [string]$WorkingDirectory = $WT,
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

    foreach ($item in $ToolArgs) {
        [void]$psi.ArgumentList.Add([string]$item)
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

function Run-CodexImplementation {
    param(
        [Parameter(Mandatory)][string]$CodexExe,
        [Parameter(Mandatory)][string]$PromptText,
        [Parameter(Mandatory)][string]$LastMessagePath
    )

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $CodexExe
    $psi.WorkingDirectory = $WT
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $false
    $psi.RedirectStandardError = $false
    $psi.RedirectStandardInput = $true

    foreach ($item in @(
        'exec',
        '--model',$Model,
        '--sandbox','danger-full-access',
        '--config','approval_policy="never"',
        '--config','model_reasoning_effort="medium"',
        '--cd',$WT,
        '--output-last-message',$LastMessagePath,
        '-'
    )) {
        [void]$psi.ArgumentList.Add([string]$item)
    }

    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi

    try {
        Require ($p.Start()) 'CODEX_IMPLEMENTATION_START_FAILED'
        $p.StandardInput.Write($PromptText)
        $p.StandardInput.Close()
        $p.WaitForExit()
        return [int]$p.ExitCode
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

$PwshCommand = Get-Command pwsh.exe -ErrorAction SilentlyContinue
if ($null -eq $PwshCommand) {
    $PwshCommand = Get-Command pwsh -ErrorAction Stop
}
$Pwsh = $PwshCommand.Source

$CodexCommand = Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1
$Codex = $CodexCommand.Source

function G {
    param([string[]]$GitArgs)

    $r = Run-Native -File $Git -ToolArgs (@('-C',$WT) + $GitArgs) -TimeoutSeconds 90

    Require ($r.Code -eq 0) (
        'GIT_FAILED: ' +
        ($GitArgs -join ' ') +
        ' :: ' +
        ([string]$r.Err).Trim()
    )

    return ([string]$r.Out).Trim()
}

function Get-RemoteHead {
    param([Parameter(Mandatory)][string]$BranchName)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$WT,
        'ls-remote','--refs','origin',
        ('refs/heads/' + $BranchName)
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
            '-C',$WT,
            'fetch','--no-tags','origin',
            ('refs/heads/' + $BranchName)
        ) -TimeoutSeconds 90

        if ($r.Code -eq 0) {
            $observed = G @('rev-parse','FETCH_HEAD')
            Require ($observed -ceq $expected) ('FETCH_HEAD_MISMATCH: ' + $BranchName)
            return $observed
        }

        if ($attempt -lt 2) {
            Start-Sleep -Seconds 2
        }
    }

    throw ('FETCH_FAILED_AFTER_BOUNDED_RETRY: ' + $BranchName)
}

function Assert-Ancestor {
    param([string]$Ancestor,[string]$Descendant,[string]$Message)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$WT,
        'merge-base','--is-ancestor',
        $Ancestor,$Descendant
    ) -TimeoutSeconds 30

    Require ($r.Code -eq 0) $Message
}

function Assert-Blob {
    param([string]$Commit,[string]$Path,[string]$Expected,[string]$Label)

    $observed = G @('rev-parse',($Commit + ':' + $Path))
    Require ($observed -ceq $Expected) ($Label + '_BLOB_MISMATCH')
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

        foreach ($marker in @($WT,$TaskBranch,$DispatchId,'PRESENTATION-LOCK-CERTIFIER-REWORK-R4')) {
            Require (
                $line.IndexOf($marker,[StringComparison]::OrdinalIgnoreCase) -lt 0
            ) ('COMPETING_R4_TASK_WRITER: ' + $name)
        }
    }
}

function Is-AllowedResultPath {
    param([string]$Path)

    $p = $Path.Replace('\','/')

    return (
        ($p -ceq $CertifierPath) -or
        ($p -ceq $TestPath) -or
        ($p -ceq $ReportPath) -or
        ($p -ceq $ManifestPath) -or
        $p.StartsWith($EvidencePrefix,[StringComparison]::Ordinal)
    )
}

Write-Output '=== FOX2 R4 IMMUTABLE OWNER LAUNCHER ==='
Write-Output ('FOX2_DISPATCH_ID=' + $DispatchId)
Write-Output 'FOX2_PRIOR_TRANSPORT_FAILURE=RECOVERED'
Write-Output 'FOX2_R3_A01=CONSUMED_NO_RESULT_NO_REPLAY'
Write-Output 'FOX2_R4_CONSUMED=FALSE'

Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'
Require (Test-Path -LiteralPath $Repo -PathType Container) 'REPO_MISSING'
Require (Test-Path -LiteralPath $WT -PathType Container) 'R4_WORKTREE_MISSING'
Require (Test-Path -LiteralPath $TestPython -PathType Leaf) 'TEST_PYTHON_MISSING'

$pwshVersion = Run-Native -File $Pwsh -ToolArgs @(
    '-NoProfile','-Command','$PSVersionTable.PSVersion.Major'
) -TimeoutSeconds 30

Require ($pwshVersion.Code -eq 0) 'PWSH_VERSION_PROBE_FAILED'
Require (([string]$pwshVersion.Out).Trim() -eq '7') 'PWSH7_NOT_VERIFIED'

$top = G @('rev-parse','--show-toplevel')
Require (
    [IO.Path]::GetFullPath($top).TrimEnd('\').Equals(
        [IO.Path]::GetFullPath($WT).TrimEnd('\'),
        [StringComparison]::OrdinalIgnoreCase
    )
) 'WORKTREE_IDENTITY_MISMATCH'

Require ((G @('branch','--show-current')) -ceq $TaskBranch) 'WRONG_R4_BRANCH'
Require ((G @('rev-parse','HEAD')) -ceq $RuntimeBase) 'LOCAL_R4_HEAD_NOT_RUNTIME_BASE'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'R4_WORKTREE_DIRTY'
Require ((Get-RemoteHead $TaskBranch) -ceq $RuntimeBase) 'R4_REMOTE_MOVED_BEFORE_START'

$statusHead = Fetch-BranchHead $StatusBranch
$controlHead = Fetch-BranchHead $ControlBranch
$govHead = Fetch-BranchHead $GovernanceBranch

Assert-Ancestor $PassCommit $statusHead 'R4_PASS_TO_ASSIGN_NOT_CURRENT'
Assert-Ancestor $TransportRecoveryCommit $statusHead 'R4_TRANSPORT_RECOVERY_NOT_CURRENT'
Assert-Ancestor $R3FinalRecovery $statusHead 'R3_FINAL_RECOVERY_NOT_CURRENT'
Assert-Ancestor $DispatchCommit $controlHead 'R4_DISPATCH_NOT_CURRENT'

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
    Assert-Blob $govHead $pair[0] $pair[1] ('GOV_' + $pair[0])
}

Assert-Blob $TaskCommit $TaskPath $TaskBlob 'TASK'
Assert-Blob $PromptCommit $PromptPath $PromptBlob 'PROMPT'
Assert-Blob $ReceiptCommit $ReceiptPath $ReceiptBlob 'RECEIPT'
Assert-Blob $PassCommit $PassPath $PassBlob 'PASS_TO_ASSIGN'
Assert-Blob $DispatchCommit $DispatchPath $DispatchBlob 'DISPATCH'
Assert-Blob $statusHead $PassPath $PassBlob 'CURRENT_PASS_TO_ASSIGN'
Assert-Blob $controlHead $DispatchPath $DispatchBlob 'CURRENT_DISPATCH'

Assert-Ancestor $AcceptedSource $RuntimeBase 'ACCEPTED_SOURCE_NOT_ANCESTOR'
Require (
    [string]::IsNullOrWhiteSpace(
        (G @('diff','--name-only',($AcceptedSource + '..' + $RuntimeBase),'--','agent_bridge'))
    )
) 'PRODUCT_DRIFT_BEFORE_R4_AGENT'

Assert-Blob $AcceptedSource $CertifierPath $CertifierBlob 'CERTIFIER_SOURCE'
Assert-Blob $AcceptedSource $TestPath $TestBlob 'TEST_SOURCE'

$verifyCode = @'
import hashlib
import json
import subprocess
import sys
import jsonschema

(
    wt,
    gov,
    receipt_schema_path,
    dispatch_schema_path,
    task_commit, task_path, task_sha,
    prompt_commit, prompt_path, prompt_sha,
    receipt_commit, receipt_path, receipt_sha,
    pass_commit, pass_path, pass_sha,
    dispatch_commit, dispatch_path, dispatch_sha,
    dispatch_id, retry_of, runtime_base, source,
) = sys.argv[1:24]

def raw(commit, path):
    return subprocess.check_output(
        ["git","-C",wt,"show",f"{commit}:{path}"]
    )

for commit, path, expected in (
    (task_commit, task_path, task_sha),
    (prompt_commit, prompt_path, prompt_sha),
    (receipt_commit, receipt_path, receipt_sha),
    (pass_commit, pass_path, pass_sha),
    (dispatch_commit, dispatch_path, dispatch_sha),
):
    actual = hashlib.sha256(raw(commit, path)).hexdigest()
    assert actual == expected, (path, actual, expected)

receipt_schema = json.loads(raw(gov, receipt_schema_path))
dispatch_schema = json.loads(raw(gov, dispatch_schema_path))
receipt = json.loads(raw(receipt_commit, receipt_path))
dispatch = json.loads(raw(dispatch_commit, dispatch_path))

jsonschema.Draft202012Validator(
    receipt_schema,
    format_checker=jsonschema.FormatChecker(),
).validate(receipt)

jsonschema.Draft202012Validator(
    dispatch_schema,
    format_checker=jsonschema.FormatChecker(),
).validate(dispatch)

assert receipt["status"] == "PASS"
assert receipt["blockers"] == []
assert receipt["candidate_route"]["model"] == "gpt-6.1-sol"
assert receipt["candidate_route"]["reasoning_effort"] == "medium"

assert dispatch["dispatch_id"] == dispatch_id
assert dispatch["max_runs"] == 1
assert dispatch["retry_of_dispatch_id"] == retry_of
assert dispatch["runtime_contract"]["base_sha"] == runtime_base
assert dispatch["source"]["commit_sha"] == source
assert dispatch["routing"]["model"] == "gpt-6.1-sol"
assert dispatch["routing"]["reasoning_effort"] == "medium"
assert dispatch["routing"]["permission_profile"] == "FULL_ACCESS"

assert set(dispatch["runtime_contract"]["allowed_code_paths"]) == {
    "agent_bridge/scripts/certify_user_lifecycle.py",
    "agent_bridge/tests/test_lifecycle_wpf_contract.py",
}

assert dispatch["permissions"]["pr_create"] is False
assert dispatch["permissions"]["merge_allowed"] is False
assert dispatch["permissions"]["production_provider"] is False
assert dispatch["permissions"]["broker_write"] is False
assert dispatch["permissions"]["live"] is False

print("PASS")
'@

$verify = Run-Native -File $TestPython -ToolArgs @(
    '-I','-B','-c',
    $verifyCode,
    $WT,
    $govHead,
    $ReceiptSchemaPath,
    $DispatchSchemaPath,
    $TaskCommit,$TaskPath,$TaskSha256,
    $PromptCommit,$PromptPath,$PromptSha256,
    $ReceiptCommit,$ReceiptPath,$ReceiptSha256,
    $PassCommit,$PassPath,$PassSha256,
    $DispatchCommit,$DispatchPath,$DispatchSha256,
    $DispatchId,$ConsumedR3DispatchId,$RuntimeBase,$AcceptedSource
) -TimeoutSeconds 60

Require ($verify.Code -eq 0) ('IMMUTABLE_BINDING_OR_SCHEMA_FAILED: ' + ([string]$verify.Err).Trim())
Require (([string]$verify.Out).Trim() -ceq 'PASS') 'IMMUTABLE_BINDING_OR_SCHEMA_MARKER_FAILED'

Write-Output 'FOX2_IMMUTABLE_BINDINGS=PASS'
Write-Output 'FOX2_RECEIPT_SCHEMA=PASS'
Write-Output 'FOX2_DISPATCH_SCHEMA=PASS'

$pyProbe = Run-Native -File $TestPython -ToolArgs @(
    '-I','-B','-c',
    'import importlib.metadata as m,sys,pytest,jsonschema; print(f"{sys.version_info.major}.{sys.version_info.minor}|{pytest.__version__}|{m.version(''jsonschema'')}")'
) -TimeoutSeconds 30

Require ($pyProbe.Code -eq 0) 'TEST_PYTHON_CAPABILITY_FAILED'
Require (([string]$pyProbe.Out).Trim() -ceq '3.13|8.3.5|4.26.0') 'TEST_PYTHON_CAPABILITY_DRIFT'

$codexVersion = Run-Native -File $Codex -ToolArgs @('--version') -TimeoutSeconds 30
Require ($codexVersion.Code -eq 0) 'CODEX_VERSION_PROBE_FAILED'
Require (([string]$codexVersion.Out).Trim() -ceq $ExpectedCodexVersion) 'CODEX_VERSION_DRIFT'

$login = Run-Native -File $Codex -ToolArgs @('login','status') -TimeoutSeconds 60
Require ($login.Code -eq 0) 'CODEX_AUTH_NOT_READY'

Assert-NoTaskWriter

$probeDir = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-r4-fullaccess-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($probeDir) | Out-Null
$probeLast = Join-Path $probeDir 'last.txt'
$probeMarker = 'FOX2_R4_FULLACCESS_MEDIUM_OK'

try {
    $probePrompt =
        'FOX2 capability probe only. Do not inspect or modify external files. Reply exactly ' +
        $probeMarker +
        ' and nothing else.' +
        [Environment]::NewLine

    $probe = Run-Native -File $Codex -ToolArgs @(
        'exec',
        '--model',$Model,
        '--sandbox','danger-full-access',
        '--config','approval_policy="never"',
        '--config','model_reasoning_effort="medium"',
        '--skip-git-repo-check',
        '--cd',$probeDir,
        '--output-last-message',$probeLast,
        '-'
    ) -TimeoutSeconds 240 -WorkingDirectory $probeDir -StandardInput $probePrompt

    Require ($probe.Code -eq 0) ('FULLACCESS_MEDIUM_PROBE_FAILED: ' + ([string]$probe.Err).Trim())
    Require (Test-Path -LiteralPath $probeLast -PathType Leaf) 'FULLACCESS_MEDIUM_LAST_MESSAGE_MISSING'
    Require (([IO.File]::ReadAllText($probeLast)).Trim() -ceq $probeMarker) 'FULLACCESS_MEDIUM_MARKER_MISMATCH'
}
finally {
    try {
        if ([IO.Directory]::Exists($probeDir)) {
            [IO.Directory]::Delete($probeDir,$true)
        }
    }
    catch {}
}

Write-Output 'FOX2_FULLACCESS_MEDIUM_CAPABILITY=PASS'

Require ((Get-RemoteHead $TaskBranch) -ceq $RuntimeBase) 'R4_REMOTE_MOVED_PRECONSUME'
Require ((G @('rev-parse','HEAD')) -ceq $RuntimeBase) 'R4_LOCAL_MOVED_PRECONSUME'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'R4_WIP_PRECONSUME'
Assert-NoTaskWriter

$gitCommonRaw = G @('rev-parse','--git-common-dir')
$gitCommon =
    if ([IO.Path]::IsPathFullyQualified($gitCommonRaw)) {
        [IO.Path]::GetFullPath($gitCommonRaw)
    }
    else {
        [IO.Path]::GetFullPath((Join-Path $WT $gitCommonRaw))
    }

$attemptDir = Join-Path $gitCommon 'fox2-attempts'
[IO.Directory]::CreateDirectory($attemptDir) | Out-Null
$claimPath = Join-Path $attemptDir ($DispatchId + '.claim.json')

if (Test-Path -LiteralPath $claimPath -PathType Leaf) {
    Write-Output 'FOX2_EXISTING_DURABLE_CLAIM=TRUE'
    Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
    Write-Output 'FOX2_NO_REPLAY_STOP=TRUE'
    throw 'R4_DURABLE_CLAIM_ALREADY_EXISTS_NO_REPLAY'
}

Write-Output 'FOX2_PRIOR_MALFORMED_PASTE_CLASSIFICATION=LAUNCH_TRANSPORT_NOT_STARTED'
Write-Output 'FOX2_EXISTING_DURABLE_CLAIM=FALSE'

$claim = [ordered]@{
    schema = 'FOX2_LOCAL_ATTEMPT_CLAIM_V1'
    dispatch_id = $DispatchId
    retry_of_dispatch_id = $ConsumedR3DispatchId
    dispatch_commit = $DispatchCommit
    runtime_base = $RuntimeBase
    task_branch = $TaskBranch
    selected_model = $Model
    selected_reasoning = $Reasoning
    consumed = $true
    state = 'CONSUMED_BEFORE_CODEX_SPAWN'
    claimed_at = [DateTime]::UtcNow.ToString('o')
    no_replay = $true
}

$claimJson = ($claim | ConvertTo-Json -Depth 10).TrimEnd() + [char]10
$claimBytes = [Text.UTF8Encoding]::new($false).GetBytes($claimJson)

$claimStream = [IO.File]::Open(
    $claimPath,
    [IO.FileMode]::CreateNew,
    [IO.FileAccess]::Write,
    [IO.FileShare]::None
)

try {
    $claimStream.Write($claimBytes,0,$claimBytes.Length)
    $claimStream.Flush($true)
}
finally {
    $claimStream.Dispose()
}

Require (Test-Path -LiteralPath $claimPath -PathType Leaf) 'DURABLE_CLAIM_DID_NOT_PERSIST'

$claimReadback = Get-Content -LiteralPath $claimPath -Raw | ConvertFrom-Json

Require ($claimReadback.dispatch_id -ceq $DispatchId) 'CLAIM_DISPATCH_MISMATCH'
Require ($claimReadback.dispatch_commit -ceq $DispatchCommit) 'CLAIM_COMMIT_MISMATCH'
Require ($claimReadback.runtime_base -ceq $RuntimeBase) 'CLAIM_RUNTIME_BASE_MISMATCH'
Require ($claimReadback.consumed -eq $true) 'CLAIM_CONSUMED_FALSE'
Require ($claimReadback.no_replay -eq $true) 'CLAIM_NO_REPLAY_FALSE'

Write-Output ''
Write-Output '=== FOX2 R4 DISPATCH CONSUMED ==='
Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
Write-Output 'FOX2_DURABLE_CLAIM_READBACK=PASS'
Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
Write-Output 'FOX2_NO_REPLAY=TRUE'

$env:FOX2_PROJECT = 'FOX2'
$env:FOX2_WP_ID = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
$env:FOX2_TASK_ID = 'FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4'
$env:FOX2_DISPATCH_ID = $DispatchId
$env:FOX2_DISPATCH_COMMIT = $DispatchCommit
$env:FOX2_DISPATCH_SHA256 = $DispatchSha256
$env:FOX2_RETRY_OF_DISPATCH_ID = $ConsumedR3DispatchId
$env:FOX2_PASS_TO_ASSIGN_COMMIT = $PassCommit
$env:FOX2_PREEXEC_RECEIPT_COMMIT = $ReceiptCommit
$env:FOX2_RUNTIME_BASE = $RuntimeBase
$env:FOX2_ACCEPTED_SOURCE = $AcceptedSource
$env:FOX2_SELECTED_MODEL = $Model
$env:FOX2_SELECTED_REASONING = $Reasoning
$env:FOX2_DISPATCH_CONSUMED = 'TRUE'
$env:FOX2_NO_REPLAY = 'TRUE'
$env:FOX2_TEST_PYTHON = $TestPython
$env:FOX2_PACKAGE_BUILD_ALLOWED = 'FALSE'
$env:FOX2_HOST_LIFECYCLE_MUTATION = 'FALSE'
$env:FOX2_A05_ALLOWED = 'FALSE'
$env:FOX2_G3_ALLOWED = 'FALSE'
$env:FOX2_G4_ALLOWED = 'FALSE'
$env:FOX2_CANARY_ALLOWED = 'FALSE'
$env:PATH = (Split-Path -Parent $TestPython) + ';' + $env:PATH

$promptFull = Join-Path $WT ($PromptPath -replace '/', '\')
Require (Test-Path -LiteralPath $promptFull -PathType Leaf) 'POST_CONSUME_PROMPT_MISSING'

$promptText = [IO.File]::ReadAllText($promptFull)
$lastMessage = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-R4-CODEX-LAST-' + [Guid]::NewGuid().ToString('N') + '.txt')

Write-Output ''
Write-Output '=== START CODEX R4 MEDIUM ==='

$codexExit = Run-CodexImplementation -CodexExe $Codex -PromptText $promptText -LastMessagePath $lastMessage

try {
    $claimAfter = Get-Content -LiteralPath $claimPath -Raw | ConvertFrom-Json
    $claimAfter.state = 'CODEX_EXITED'
    $claimAfter | Add-Member -NotePropertyName codex_exit_code -NotePropertyValue $codexExit -Force
    $claimAfter | Add-Member -NotePropertyName codex_exited_at -NotePropertyValue ([DateTime]::UtcNow.ToString('o')) -Force
    $claimAfterJson = ($claimAfter | ConvertTo-Json -Depth 10).TrimEnd() + [char]10
    [IO.File]::WriteAllText($claimPath,$claimAfterJson,[Text.UTF8Encoding]::new($false))
}
catch {
    Write-Output 'FOX2_CLAIM_TERMINAL_UPDATE=FAILED_NONFATAL'
}

Write-Output ''
Write-Output '=== CODEX R4 EXITED ==='
Write-Output ('FOX2_CODEX_EXIT=' + $codexExit)
Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
Write-Output 'FOX2_NO_REPLAY=TRUE'

if (Test-Path -LiteralPath $lastMessage -PathType Leaf) {
    Write-Output '--- CODEX R4 LAST MESSAGE BEGIN ---'
    Get-Content -LiteralPath $lastMessage -Tail 200
    Write-Output '--- CODEX R4 LAST MESSAGE END ---'
}

try {
    $localAfter = G @('rev-parse','HEAD')
    $wipAfter = @(& $Git -C $WT status --porcelain=v1 --untracked-files=all)
    $remoteAfter = Get-RemoteHead $TaskBranch

    Write-Output ''
    Write-Output '=== FOX2 R4 POST-CONSUME STATE ==='
    Write-Output ('FOX2_LOCAL_HEAD_AFTER=' + $localAfter)
    Write-Output ('FOX2_REMOTE_HEAD_AFTER=' + $remoteAfter)
    Write-Output ('FOX2_LOCAL_WIP_AFTER=' + ($wipAfter.Count -gt 0))

    if ($remoteAfter -ceq $RuntimeBase) {
        if (($localAfter -cne $RuntimeBase) -or ($wipAfter.Count -gt 0)) {
            Write-Output '=== FOX2 R4 EXECUTION RECOVERY REQUIRED ==='
            Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
            Write-Output 'FOX2_RESULT_DELIVERY=LOCAL_RESULT_OR_WIP_NO_REMOTE_PUSH'
            Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
            Write-Output 'FOX2_NEXT=CHAT_EXECUTION_RECOVERY'
            Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
            exit 0
        }

        Write-Output '=== FOX2 R4 EXECUTION RECOVERY REQUIRED ==='
        Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
        Write-Output 'FOX2_RESULT_DELIVERY=CONSUMED_NO_LOCAL_OR_REMOTE_RESULT'
        Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
        Write-Output 'FOX2_NEXT=CHAT_EXECUTION_RECOVERY'
        Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
        exit 0
    }

    $fetch = Run-Native -File $Git -ToolArgs @(
        '-C',$WT,
        'fetch','--no-tags','origin',
        ('refs/heads/' + $TaskBranch)
    ) -TimeoutSeconds 90

    Require ($fetch.Code -eq 0) 'REMOTE_RESULT_FETCH_FAILED'

    $fetchedResult = G @('rev-parse','FETCH_HEAD')
    Require ($fetchedResult -ceq $remoteAfter) 'REMOTE_RESULT_FETCH_SHA_MISMATCH'
    Assert-Ancestor $RuntimeBase $remoteAfter 'REMOTE_RESULT_NOT_DESCENDANT_OF_RUNTIME_BASE'

    $changedPaths = @(
        & $Git -C $WT diff --name-only "$RuntimeBase..$remoteAfter" --
    ) |
    ForEach-Object { "$_".Trim().Replace('\','/') } |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }

    $changedPaths = @($changedPaths)

    $unauthorized = @(
        foreach ($p in $changedPaths) {
            if (-not (Is-AllowedResultPath $p)) {
                $p
            }
        }
    )

    $reportChanged = $changedPaths -contains $ReportPath
    $manifestChanged = $changedPaths -contains $ManifestPath
    $evidenceChanged = @(
        $changedPaths |
        Where-Object {
            $_.StartsWith($EvidencePrefix,[StringComparison]::Ordinal)
        }
    ).Count -gt 0

    Write-Output ('FOX2_CHANGED_PATH_COUNT=' + $changedPaths.Count)
    Write-Output ('FOX2_UNAUTHORIZED_PATH_COUNT=' + $unauthorized.Count)
    Write-Output ('FOX2_RESULT_REPORT_CHANGED=' + $reportChanged)
    Write-Output ('FOX2_RESULT_MANIFEST_CHANGED=' + $manifestChanged)
    Write-Output ('FOX2_RESULT_EVIDENCE_CHANGED=' + $evidenceChanged)

    if ($unauthorized.Count -gt 0) {
        foreach ($p in $unauthorized) {
            Write-Output ('FOX2_UNAUTHORIZED_PATH=' + $p)
        }

        Write-Output '=== FOX2 R4 EXECUTION RECOVERY REQUIRED ==='
        Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
        Write-Output 'FOX2_RESULT_DELIVERY=REMOTE_RESULT_UNAUTHORIZED_PATH'
        Write-Output ('FOX2_RESULT_SHA=' + $remoteAfter)
        Write-Output 'FOX2_NEXT=CHAT_RESULT_RECOVERY'
        Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
        exit 0
    }

    if (-not $reportChanged -or -not $manifestChanged -or -not $evidenceChanged) {
        Write-Output '=== FOX2 R4 EXECUTION RECOVERY REQUIRED ==='
        Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
        Write-Output 'FOX2_RESULT_DELIVERY=REMOTE_RESULT_CONTRACT_INCOMPLETE'
        Write-Output ('FOX2_RESULT_SHA=' + $remoteAfter)
        Write-Output 'FOX2_NEXT=CHAT_RESULT_RECOVERY'
        Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
        exit 0
    }

    $manifestCheckCode = @'
import json
import subprocess
import sys

wt, commit, path = sys.argv[1:4]
raw = subprocess.check_output(
    ["git","-C",wt,"show",f"{commit}:{path}"]
)
json.loads(raw)
print("PASS")
'@

    $manifestCheck = Run-Native -File $TestPython -ToolArgs @(
        '-I','-B','-c',
        $manifestCheckCode,
        $WT,$remoteAfter,$ManifestPath
    ) -TimeoutSeconds 30

    Require ($manifestCheck.Code -eq 0) 'REMOTE_RESULT_MANIFEST_INVALID'
    Require (([string]$manifestCheck.Out).Trim() -ceq 'PASS') 'REMOTE_RESULT_MANIFEST_MARKER_INVALID'

    if ($wipAfter.Count -gt 0) {
        Write-Output '=== FOX2 R4 EXECUTION RECOVERY REQUIRED ==='
        Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
        Write-Output 'FOX2_RESULT_DELIVERY=PUSHED_WITH_LOCAL_WIP'
        Write-Output ('FOX2_RESULT_SHA=' + $remoteAfter)
        Write-Output 'FOX2_NEXT=CHAT_RESULT_RECOVERY'
        Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
        exit 0
    }

    Write-Output ''
    Write-Output '=== FOX2 R4 EXECUTION RESULT ==='
    Write-Output ('FOX2_CODEX_EXIT=' + $codexExit)
    Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
    Write-Output 'FOX2_NO_REPLAY=TRUE'
    Write-Output ('FOX2_RUNTIME_BASE=' + $RuntimeBase)
    Write-Output ('FOX2_RESULT_SHA=' + $remoteAfter)
    Write-Output 'FOX2_REMOTE_DESCENDANT_OF_RUNTIME_BASE=TRUE'
    Write-Output 'FOX2_WORKTREE_DIRTY_AFTER=FALSE'
    Write-Output ('FOX2_CHANGED_PATH_COUNT=' + $changedPaths.Count)
    Write-Output 'FOX2_UNAUTHORIZED_PATH_COUNT=0'
    Write-Output ('FOX2_RESULT_REPORT_CHANGED=' + $reportChanged)
    Write-Output ('FOX2_RESULT_MANIFEST_CHANGED=' + $manifestChanged)
    Write-Output ('FOX2_RESULT_EVIDENCE_CHANGED=' + $evidenceChanged)
    Write-Output 'FOX2_RESULT_DELIVERY=PUSHED_UNREVIEWED'
    Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
    Write-Output 'FOX2_PACKAGE_BUILD_ALLOWED=FALSE'
    Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
    Write-Output 'FOX2_A05_ALLOWED=FALSE'
    Write-Output 'FOX2_G3_ALLOWED=FALSE'
    Write-Output 'FOX2_G4_ALLOWED=FALSE'
    Write-Output 'FOX2_CANARY_ALLOWED=FALSE'
    Write-Output 'FOX2_NEXT=CHAT_RESULT_REVIEW'
    Write-Output 'FOX2_STOP_HERE=TRUE'
    Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
}
catch {
    $failureMessage = [string]$_.Exception.Message
    $failureMessage = $failureMessage -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'

    if ($failureMessage.Length -gt 1000) {
        $failureMessage = $failureMessage.Substring(0,1000)
    }

    Write-Output ''
    Write-Output '=== FOX2 R4 POST-CONSUME FAILURE ==='
    Write-Output 'FOX2_DISPATCH_CONSUMED=TRUE'
    Write-Output 'FOX2_NO_REPLAY=TRUE'
    Write-Output ('FOX2_FAILURE=' + $failureMessage)
    Write-Output ('FOX2_DURABLE_CLAIM=' + $claimPath)
    Write-Output 'FOX2_NEXT=CHAT_EXECUTION_RECOVERY'
    Write-Output 'FOX2_DO_NOT_RERUN_THIS_DISPATCH=TRUE'
}
