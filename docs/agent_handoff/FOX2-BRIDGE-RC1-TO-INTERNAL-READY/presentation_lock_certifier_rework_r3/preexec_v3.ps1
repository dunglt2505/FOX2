param(
    [Parameter(Mandatory=$true)][string]$PublicationHead,
    [Parameter(Mandatory=$true)][string]$ExpectedScriptBlob,
    [Parameter(Mandatory=$true)][string]$Worktree
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Project = 'FOX2'
$WpId = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
$TaskId = 'FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3'
$Branch = 'work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-20261022'
$StatusBranch = 'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021'
$ControlBranch = 'work/FOX2-DISPATCH-chat'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'

$SourceBase = '085cc8302e824dbccf9cbef80422ed48894b9cb4'

$TaskCommit = 'c5b8ccef94fc222bc2626209c74c074b827269f3'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/task.md'
$TaskBlob = 'e66f8fc39add4024de3b242771d171e9b6b5bec3'
$TaskSha256 = '4dde2215f4095f26caa00bb6c0254cfb421d3d5d21086e5c1b6769b197acec5e'

$PromptCommit = 'aed565cd230ccea9f7b8353ed72820c616985fd9'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/prompt.md'
$PromptBlob = 'aee25625c67abf1a4ec5b8aa1cda22e517214a8e'
$PromptSha256 = '44f0138cf10ae96de0392d84f11b5151ad85496fa93d64aa056a3316ad42d75c'

$PreExecV1Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/preexec.ps1'
$PreExecV1Commit = 'ba9b8eda7de3c2aa53cf0e7aeee3249f60780b13'
$PreExecV1Blob = '8cbb498ea806b1601c5eb8cb99732510272132b4'
$PreExecV1State = 'BLOCKED_TEST_PYTHON_BINDING_DEFECT_DO_NOT_RERUN'

$PreExecV2Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/preexec_v2.ps1'
$PreExecV2Commit = '5319554547aeb03b9a3faf8970794f21c9f97cb7'
$PreExecV2Blob = '98231e03937a55b91ef9f769bb371d9354c77627'
$PreExecV2ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r3_v2.json'
$PreExecV2ReceiptBlob = 'b2de022ea3f65f9062d7c24e0a7535bf8f958ed6'
$PreExecV2ReceiptSha256 = '154d82f91c0f2d5b0f5f609ad42a449f7b8ab0be2bf99ec52a4a239af6a050eb'
$PreExecV2State = 'SCHEMA_INVALID_DO_NOT_USE_FOR_PASS_TO_ASSIGN'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/presentation_lock_certifier_rework_r3/preexec_v3.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/presentation_lock_certifier_rework_r3_v3.json'
$FutureDispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R3-CODEX-001.json'
$SupersededR2DispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R2-CODEX-001.json'
$A04DispatchPath = 'docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001.json'

$LifecycleScriptPath = 'agent_bridge/scripts/certify_user_lifecycle.py'
$LifecycleScriptBlob = '7e62103ea4876833f67794a927a2a54622a59ea5'
$LifecycleTestPath = 'agent_bridge/tests/test_lifecycle_wpf_contract.py'
$LifecycleTestBlob = 'f80e50d59b1f1bb9ec9d553e84bbe7948971cb66'

$MasterPlanPath = 'docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md'
$MasterPlanCommit = 'ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56'
$MasterPlanBlob = '6068b0e664d43afc87468e52785806dafc70b59f'

$ReusePlanPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_A04_A05_REUSE_PLAN_20261022.md'
$ReusePlanCommit = 'da6fd27d78380db42fce155d634044c94a661229'
$ReusePlanBlob = '65f5a8359c18588be61ca42122acd894a8a80d99'

$V037ReviewPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/BRIDGE_FEATURE_REASSESSMENT_V037_20261022.md'
$V037ReviewCommit = '7cee0933ffd241deaa8e748bfeb626c56fab0cd0'
$V037ReviewBlob = '74864a7520bcaaedcb885c4581a7f679fd5d1a43'

$RecoveryPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PRESENTATION_LOCK_CERTIFIER_R3_PREEXEC_V1_RECOVERY_20261022.md'
$RecoveryCommit = '03ba2e7961307a6ce29b424765b05a337da8c200'
$SchemaRecoveryPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/PRESENTATION_LOCK_CERTIFIER_R3_PREEXEC_V3_SCHEMA_RECOVERY_20261022.md'
$SchemaRecoveryCommit = '2b6ecc56fad6deca2f85c3f2fd7651a3bd4ce7ff'

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

$SelectedActor = 'CODEX'
$SelectedModel = 'gpt-6.1-sol'
$SelectedReasoning = 'medium'
$ExpectedCodexVersion = 'codex-cli 0.162.1'

function Require {
    param([bool]$Condition,[string]$Message)
    if (-not $Condition) { throw $Message }
}

function Safe {
    param([AllowNull()][object]$Value)
    if ($null -eq $Value) { return '' }
    $v = [string]$Value
    $v = $v -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'
    $v = $v.Trim()
    if ($v.Length -gt 600) { $v = $v.Substring(0,600) }
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
        (Safe ($r.Err + ' ' + $r.Out))
    )

    return ([string]$r.Out).Trim()
}

function Get-RemoteHead {
    param([string]$BranchName)

    $r = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,
        'ls-remote','--refs','origin',
        ('refs/heads/' + $BranchName)
    ) -TimeoutSeconds 60

    Require ($r.Code -eq 0) ('REMOTE_READ_FAILED: ' + $BranchName)

    $text = ([string]$r.Out).Trim()

    Require (-not [string]::IsNullOrWhiteSpace($text)) (
        'REMOTE_BRANCH_MISSING: ' + $BranchName
    )

    return (($text -split '\s+')[0]).Trim()
}

function Get-Sha256 {
    param([string]$Path)

    return (
        Get-FileHash -LiteralPath $Path -Algorithm SHA256
    ).Hash.ToLowerInvariant()
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
            'PRESENTATION-LOCK-CERTIFIER-REWORK-R3'
        )) {
            Require (
                $line.IndexOf(
                    $marker,
                    [StringComparison]::OrdinalIgnoreCase
                ) -lt 0
            ) 'COMPETING_TASK_WRITER'
        }
    }
}

function Add-PythonCandidate {
    param(
        [System.Collections.Generic.List[string]]$List,
        [System.Collections.Generic.HashSet[string]]$Seen,
        [AllowNull()][string]$Path
    )

    if ([string]::IsNullOrWhiteSpace($Path)) { return }

    $candidate = [Environment]::ExpandEnvironmentVariables($Path.Trim().Trim('"'))

    if (-not [IO.Path]::IsPathFullyQualified($candidate)) { return }
    if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { return }

    try {
        $full = [IO.Path]::GetFullPath($candidate)
    }
    catch {
        return
    }

    if ($Seen.Add($full)) {
        [void]$List.Add($full)
    }
}

function Resolve-TestPython {
    $list = [System.Collections.Generic.List[string]]::new()
    $seen = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)

    Add-PythonCandidate -List $list -Seen $seen -Path (
        Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
    )

    foreach ($name in @('python.exe','python')) {
        $cmd = Get-Command $name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($null -ne $cmd) {
            Add-PythonCandidate -List $list -Seen $seen -Path $cmd.Source
        }
    }

    $pyLauncher = Get-Command py.exe -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1

    if ($null -ne $pyLauncher) {
        $probe = Run-Native -File $pyLauncher.Source -ToolArgs @('-0p') -TimeoutSeconds 30

        if ($probe.Code -eq 0) {
            foreach ($line in (([string]$probe.Out) -split '\r?\n')) {
                $trimmed = $line.Trim()

                if ($trimmed -match '([A-Za-z]:\\.*?python(?:\.exe)?)\s*$') {
                    Add-PythonCandidate -List $list -Seen $seen -Path $Matches[1]
                }
            }
        }
    }

    $probeCode = @'
import importlib.metadata as m
import sys
import pytest
import jsonschema
print(f"{sys.version_info.major}.{sys.version_info.minor}|{pytest.__version__}|{m.version('jsonschema')}")
'@

    foreach ($candidate in $list) {
        $probe = Run-Native -File $candidate -ToolArgs @('-I','-B','-c',$probeCode) -TimeoutSeconds 30

        if ($probe.Code -ne 0) { continue }

        $parts = ([string]$probe.Out).Trim() -split '\|'

        if ($parts.Count -ne 3) { continue }
        if ($parts[0] -cne '3.13') { continue }

        try {
            $pytestVersion = [version]$parts[1]
        }
        catch {
            continue
        }

        if ($pytestVersion.Major -ne 8 -or $pytestVersion.Minor -lt 3) {
            continue
        }

        $alias =
            if ($candidate.StartsWith(
                [IO.Path]::GetFullPath($env:LOCALAPPDATA),
                [StringComparison]::OrdinalIgnoreCase
            )) {
                'USERLOCAL/' +
                [IO.Path]::GetRelativePath(
                    [IO.Path]::GetFullPath($env:LOCALAPPDATA),
                    $candidate
                ).Replace('\','/')
            }
            else {
                'EXISTING_HOST_PYTHON313'
            }

        return [pscustomobject]@{
            Path = $candidate
            Alias = $alias
            Python = $parts[0]
            Pytest = $parts[1]
            Jsonschema = $parts[2]
        }
    }

    throw 'COMPATIBLE_EXISTING_TEST_PYTHON_NOT_FOUND'
}

Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R3 PREEXEC V3 ==='
Write-Output ('FOX2_TASK_ID=' + $TaskId)
Write-Output ('FOX2_SOURCE=' + $SourceBase)
Write-Output ('FOX2_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output 'FOX2_PREEXEC_V1_STATE=BLOCKED_DO_NOT_RERUN'
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_SAFETY_OVERRIDE=NO'
Write-Output ('FOX2_SELECTED_ACTOR=' + $SelectedActor)
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_AGENT_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'

Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'
Require (Test-Path -LiteralPath $Worktree -PathType Container) 'WORKTREE_MISSING'

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

foreach ($fetchBranch in @(
    $Branch,
    $StatusBranch,
    $ControlBranch,
    $GovernanceBranch
)) {
    $refspec =
        '+refs/heads/' +
        $fetchBranch +
        ':refs/remotes/origin/' +
        $fetchBranch

    $fr = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,
        'fetch','--no-tags','origin',
        $refspec
    ) -TimeoutSeconds 90

    Require ($fr.Code -eq 0) ('FETCH_FAILED: ' + $fetchBranch)
}

Require ((Get-RemoteHead $Branch) -ceq $PublicationHead) 'REMOTE_MOVED_DURING_FETCH'

$ancestor = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'merge-base','--is-ancestor',
    $SourceBase,$PublicationHead
) -TimeoutSeconds 30

Require ($ancestor.Code -eq 0) 'SOURCE_NOT_ANCESTOR'

$observedSetup = @(
    (G @(
        'diff','--name-only',
        ($SourceBase + '..' + $PublicationHead),
        '--'
    )) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
    ForEach-Object { $_.Trim().Replace('\','/') } |
    Sort-Object
)

$expectedSetup = @(
    $TaskPath,
    $PromptPath,
    $PreExecV1Path,
    $PreExecV2Path,
    $ScriptPath
) | Sort-Object

Require (
    ($observedSetup -join [char]10) -ceq
    ($expectedSetup -join [char]10)
) 'SETUP_PATH_DRIFT'

Require (
    (G @('rev-parse',($TaskCommit + ':' + $TaskPath))) -ceq
    $TaskBlob
) 'TASK_BLOB_MISMATCH'

Require (
    (G @('rev-parse',($PromptCommit + ':' + $PromptPath))) -ceq
    $PromptBlob
) 'PROMPT_BLOB_MISMATCH'

Require (
    (G @('rev-parse',($PreExecV1Commit + ':' + $PreExecV1Path))) -ceq
    $PreExecV1Blob
) 'PREEXEC_V1_HISTORY_MISMATCH'

Require (
    (G @('rev-parse',($PreExecV2Commit + ':' + $PreExecV2Path))) -ceq
    $PreExecV2Blob
) 'PREEXEC_V2_HISTORY_MISMATCH'

Require (
    (G @('rev-parse',($PreExecV2Commit + ':' + $PreExecV2ReceiptPath))) -ceq
    $PreExecV2ReceiptBlob
) 'PREEXEC_V2_RECEIPT_HISTORY_MISMATCH'

$taskFull = Join-Path $Worktree ($TaskPath -replace '/', '\')
$promptFull = Join-Path $Worktree ($PromptPath -replace '/', '\')
$scriptFull = Join-Path $Worktree ($ScriptPath -replace '/', '\')

Require ((Get-Sha256 $taskFull) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((Get-Sha256 $promptFull) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'

Require (
    (G @('hash-object','--no-filters',$scriptFull)) -ceq
    $ExpectedScriptBlob
) 'PREEXEC_V3_BLOB_MISMATCH'

Require (
    (G @('rev-parse',($SourceBase + ':' + $LifecycleScriptPath))) -ceq
    $LifecycleScriptBlob
) 'LIFECYCLE_SCRIPT_SOURCE_DRIFT'

Require (
    (G @('rev-parse',($SourceBase + ':' + $LifecycleTestPath))) -ceq
    $LifecycleTestBlob
) 'LIFECYCLE_TEST_SOURCE_DRIFT'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @(
            'diff','--name-only',
            ($SourceBase + '..' + $PublicationHead),
            '--','agent_bridge'
        ))
    )
) 'PRODUCT_DRIFT_BEFORE_CODING'

$statusRef = 'refs/remotes/origin/' + $StatusBranch

foreach ($pair in @(
    @($MasterPlanCommit,$MasterPlanPath,$MasterPlanBlob,'MASTER_PLAN'),
    @($ReusePlanCommit,$ReusePlanPath,$ReusePlanBlob,'REUSE_PLAN'),
    @($V037ReviewCommit,$V037ReviewPath,$V037ReviewBlob,'V037_REVIEW'),
    @($RecoveryCommit,$RecoveryPath,$null,'RECOVERY'),
    @($SchemaRecoveryCommit,$SchemaRecoveryPath,$null,'SCHEMA_RECOVERY')
)) {
    if ($null -ne $pair[2]) {
        Require (
            (G @('rev-parse',($pair[0] + ':' + $pair[1]))) -ceq
            $pair[2]
        ) ($pair[3] + '_BLOB_MISMATCH')
    }
    else {
        $exists = Run-Native -File $Git -ToolArgs @(
            '-C',$Worktree,
            'cat-file','-e',
            ($pair[0] + ':' + $pair[1])
        ) -TimeoutSeconds 30

        Require ($exists.Code -eq 0) ($pair[3] + '_MISSING')
    }

    $lineage = Run-Native -File $Git -ToolArgs @(
        '-C',$Worktree,
        'merge-base','--is-ancestor',
        $pair[0],$statusRef
    ) -TimeoutSeconds 30

    Require ($lineage.Code -eq 0) ($pair[3] + '_NOT_ON_STATUS_LINEAGE')
}

$govRef = 'refs/remotes/origin/' + $GovernanceBranch

foreach ($pair in @(
    @($RegistryPath,$RegistryBlob),
    @($ResolutionPath,$ResolutionBlob),
    @($DictionaryPath,$DictionaryBlob),
    @($PolicyPath,$PolicyBlob),
    @($RoutingPath,$RoutingBlob),
    @($ProtocolPath,$ProtocolBlob)
)) {
    Require (
        (G @('rev-parse',($govRef + ':' + $pair[0]))) -ceq
        $pair[1]
    ) ('GOVERNANCE_BLOB_MISMATCH: ' + $pair[0])
}

$futureDispatchSpec =
    'refs/remotes/origin/' +
    $ControlBranch +
    ':' +
    $FutureDispatchPath

$dispatchProbe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'cat-file','-e',
    $futureDispatchSpec
) -TimeoutSeconds 30

Require ($dispatchProbe.Code -ne 0) 'FRESH_R3_DISPATCH_ALREADY_EXISTS'

$r2DispatchSpec =
    'refs/remotes/origin/' +
    $ControlBranch +
    ':' +
    $SupersededR2DispatchPath

$r2Probe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'cat-file','-e',
    $r2DispatchSpec
) -TimeoutSeconds 30

Require ($r2Probe.Code -ne 0) 'SUPERSEDED_R2_DISPATCH_UNEXPECTEDLY_EXISTS'

$a04DispatchSpec =
    'refs/remotes/origin/' +
    $ControlBranch +
    ':' +
    $A04DispatchPath

$a04Probe = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'cat-file','-e',
    $a04DispatchSpec
) -TimeoutSeconds 30

Require ($a04Probe.Code -eq 0) 'A04_DISPATCH_HISTORY_MISSING'

Assert-NoTaskWriter

$testPython = Resolve-TestPython

Write-Output ('FOX2_TEST_PYTHON_ALIAS=' + $testPython.Alias)
Write-Output ('FOX2_TEST_PYTHON_VERSION=' + $testPython.Python)
Write-Output ('FOX2_PYTEST_VERSION=' + $testPython.Pytest)
Write-Output ('FOX2_JSONSCHEMA_VERSION=' + $testPython.Jsonschema)
Write-Output 'FOX2_TEST_PYTHON_CAPABILITY=PASS'

$cv = Run-Native -File $Codex -ToolArgs @('--version') -TimeoutSeconds 30
Require ($cv.Code -eq 0) 'CODEX_VERSION_FAILED'

$codexVersion = ([string]$cv.Out).Trim()
Require ($codexVersion -ceq $ExpectedCodexVersion) 'CODEX_VERSION_DRIFT'

$login = Run-Native -File $Codex -ToolArgs @('login','status') -TimeoutSeconds 60
Require ($login.Code -eq 0) 'CODEX_AUTH_NOT_READY'

$probeDir = Join-Path (
    [IO.Path]::GetTempPath()
) ('FOX2-certifier-r3-v2-medium-' + [Guid]::NewGuid().ToString('N'))

[IO.Directory]::CreateDirectory($probeDir) | Out-Null

$last = Join-Path $probeDir 'last.txt'
$marker = 'FOX2_CERTIFIER_R3_V3_MEDIUM_CAPACITY_OK'

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

    Require ($cap.Code -eq 0) (
        'CODEX_MEDIUM_CAPACITY_FAILED: ' +
        (Safe ($cap.Err + ' ' + $cap.Out))
    )

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

$dryRef = 'HEAD:refs/heads/' + $Branch

$dry = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'push','--dry-run',
    'origin',$dryRef
) -TimeoutSeconds 90

Require ($dry.Code -eq 0) (
    'GIT_PUSH_DRY_RUN_FAILED: ' +
    (Safe ($dry.Err + ' ' + $dry.Out))
)

Require (
    (Get-RemoteHead $Branch) -ceq
    $PublicationHead
) 'REMOTE_MOVED_BEFORE_RECEIPT'

Require (
    (G @('rev-parse','HEAD')) -ceq
    $PublicationHead
) 'LOCAL_MOVED_BEFORE_RECEIPT'

Require (
    [string]::IsNullOrWhiteSpace(
        (G @('status','--porcelain=v1','--untracked-files=all'))
    )
) 'WIP_BEFORE_RECEIPT'

Assert-NoTaskWriter

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', '\')

Require (
    -not (Test-Path -LiteralPath $receiptFull)
) 'PREEXEC_RECEIPT_ALREADY_EXISTS'

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
            evidence='Fresh gpt-6.1-sol/medium read-only capacity probe PASS; no effort substitution'
        }
        test_python = [ordered]@{
            status='PASS'
            material=$true
            version=('Python ' + $testPython.Python + '; pytest ' + $testPython.Pytest + '; jsonschema ' + $testPython.Jsonschema)
            executable=$testPython.Alias
            evidence='Fresh bounded discovery found an existing compatible Python 3.13 pytest environment; no installation'
        }
        certifier_source_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('certifier_blob=' + $LifecycleScriptBlob + '; test_blob=' + $LifecycleTestBlob)
        }
        task_prompt_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('task_sha256=' + $TaskSha256 + '; prompt_sha256=' + $PromptSha256)
        }
        recovery_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('preexec_v1=' + $PreExecV1Commit + ':' + $PreExecV1State + '; preexec_v2=' + $PreExecV2Commit + ':' + $PreExecV2State + '; recovery_v1=' + $RecoveryCommit + '; recovery_v2=' + $SchemaRecoveryCommit)
        }
        reuse_plan_binding = [ordered]@{
            status='PASS'
            material=$true
            evidence=('master_plan=' + $MasterPlanCommit + '; reuse_plan=' + $ReusePlanCommit + '; v037_review=' + $V037ReviewCommit)
        }
        governance_source = [ordered]@{
            status='PASS'
            material=$true
            evidence='Current Registry/Resolution/Dictionary/Policy/Routing/Protocol blobs verified'
        }
        worktree_clean = [ordered]@{
            status='PASS'
            material=$true
            evidence='Dedicated R3 worktree clean; zero agent_bridge drift before coding'
        }
        one_writer = [ordered]@{
            status='PASS'
            material=$true
            evidence='No task-scoped CODEX writer observed'
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
            evidence='Authorized R3 branch push dry-run PASS'
        }
        no_replay = [ordered]@{
            status='PASS'
            material=$true
            evidence='A04 historical Dispatch present; R2 Dispatch absent; R3 Dispatch absent'
        }
        host_lifecycle_isolation = [ordered]@{
            status='PASS'
            material=$true
            evidence='R3 is certifier-only correction; package build/install/host lifecycle/G3 forbidden'
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
        product = $SelectedActor
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
        'PreExec v1 BLOCKED because package-build venv was incorrectly assumed to provide pytest.',
        'PreExec v2 host probes PASS but receipt is schema-invalid and cannot authorize assignment.',
        'PreExec v3 performs bounded current test-runner discovery and installs nothing.',
        'Receipt candidate_route.model_policy uses schema-supported PINNED; route-assessment semantics remain in evidence/notes.'
        'FOX2 Skills v0.3.7 route assessment selected Medium before PreExec.',
        'PreExec verifies selected Medium route; it does not classify complexity.',
        'R3 corrects only external certifier + focused regression test.',
        'A04 reusable PASS remains preserved; no package rebuild or replay.',
        'No package build/install/host lifecycle mutation/G3/G4/Canary authority.',
        'PASS permits CHAT intake and fresh R3 coding assignment only.'
    )
}

[IO.Directory]::CreateDirectory(
    [IO.Path]::GetDirectoryName($receiptFull)
) | Out-Null

$json = ($receipt | ConvertTo-Json -Depth 30).TrimEnd()
$json = $json -replace [char]13,''
$json = $json + [char]10

[IO.File]::WriteAllText(
    $receiptFull,
    $json,
    [Text.UTF8Encoding]::new($false)
)

$receiptSha256 = Get-Sha256 $receiptFull

& $Git -C $Worktree add -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_GIT_ADD_FAILED'

$staged = @(
    (G @('diff','--cached','--name-only','--')) -split '\r?\n' |
    Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
)

Require (
    $staged.Count -eq 1 -and
    $staged[0].Replace('\','/') -ceq
    $ReceiptPath
) 'RECEIPT_STAGED_PATH_DRIFT'

& $Git -C $Worktree diff --cached --check
Require ($LASTEXITCODE -eq 0) 'RECEIPT_DIFF_CHECK_FAILED'

& $Git -C $Worktree commit -m 'preexec(fox2): PASS R3 Medium certifier v2' -- $ReceiptPath
Require ($LASTEXITCODE -eq 0) 'RECEIPT_COMMIT_FAILED'

$receiptCommit = G @('rev-parse','HEAD')
$receiptBlob = G @('rev-parse',($receiptCommit + ':' + $ReceiptPath))

& $Git -C $Worktree push origin ('HEAD:refs/heads/' + $Branch)
Require ($LASTEXITCODE -eq 0) 'RECEIPT_PUSH_FAILED'

$remote = Get-RemoteHead $Branch
Require ($remote -ceq $receiptCommit) 'RECEIPT_REMOTE_HEAD_MISMATCH'

$readbackRefspec =
    '+refs/heads/' +
    $Branch +
    ':refs/remotes/origin/' +
    $Branch

$fetch = Run-Native -File $Git -ToolArgs @(
    '-C',$Worktree,
    'fetch','--no-tags','origin',
    $readbackRefspec
) -TimeoutSeconds 90

Require ($fetch.Code -eq 0) 'RECEIPT_READBACK_FETCH_FAILED'

$remoteReceiptSpec =
    'refs/remotes/origin/' +
    $Branch +
    ':' +
    $ReceiptPath

Require (
    (G @('rev-parse',$remoteReceiptSpec)) -ceq
    $receiptBlob
) 'RECEIPT_REMOTE_BLOB_MISMATCH'

Write-Output ''
Write-Output '=== FOX2 PRESENTATION LOCK CERTIFIER REWORK R3 PREEXEC V3 RESULT ==='
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_RECEIPT_SHA256=' + $receiptSha256)
Write-Output ('FOX2_TEST_PYTHON_ALIAS=' + $testPython.Alias)
Write-Output ('FOX2_TEST_PYTHON_VERSION=' + $testPython.Python)
Write-Output ('FOX2_PYTEST_VERSION=' + $testPython.Pytest)
Write-Output ('FOX2_JSONSCHEMA_VERSION=' + $testPython.Jsonschema)
Write-Output 'FOX2_TASK_ROUTE_COMPLEXITY=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_EXECUTION_RISK=MEDIUM'
Write-Output 'FOX2_TASK_ROUTE_SAFETY_OVERRIDE=NO'
Write-Output ('FOX2_SELECTED_ACTOR=' + $SelectedActor)
Write-Output ('FOX2_SELECTED_MODEL=' + $SelectedModel)
Write-Output ('FOX2_SELECTED_REASONING=' + $SelectedReasoning)
Write-Output 'FOX2_SELECTED_ROUTE_VERIFICATION=PASS'
Write-Output 'FOX2_CODE_EDIT_STARTED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_PASS_TO_ASSIGN_THEN_FRESH_R3_CODING_DISPATCH'
