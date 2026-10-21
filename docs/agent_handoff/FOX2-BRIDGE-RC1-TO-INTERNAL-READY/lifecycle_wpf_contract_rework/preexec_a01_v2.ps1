#requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$PublicationHead,
    [Parameter(Mandatory)][string]$ExpectedScriptBlob,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-20261022'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Branch = 'work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-20261022'
$SourceBase = '9dd91becf47d934183baf147d0a4f03f4bf5933d'
$ProductSource = '2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb'
$TaskId = 'FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01'
$TaskCommit = 'aabe81fad8a465ea12a763fd4cccc54670dd707f'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/task.md'
$TaskBlob = 'e6503c2a817450f270ab674ce1cd723019961dce'
$TaskSha256 = '50bf03fc9fdb149dd7b4d0a3edf4bd2acbc26ec0000f39208b17b9d2f7bc2b01'

$PromptCommit = 'de3f6768fa01b1396b6686f3c06c103669bcd24d'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/prompt.md'
$PromptBlob = '5bd037b3536592d31e68b3b5e5929b84fb48d50f'
$PromptSha256 = '88359fad2607aeb7669f3678966390a118c131d9849697c24a8505e3d9932dd9'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/preexec_a01_v2.ps1'
$InvalidV1Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/lifecycle_wpf_contract_rework/preexec_a01.ps1'
$InvalidV1Blob = 'ef329ab0bc5ecf88048734012c0d66e292f84f43'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/lifecycle_wpf_contract_rework_a01.json'

$Model = 'gpt-6.1-sol'
$ReasoningEffort = 'high'
$Marker = 'FOX2_LIFECYCLE_WPF_REWORK_A01_ADMISSION_OK'

function Require([bool]$Condition, [string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Run-Tool {
    param(
        [Parameter(Mandatory)][string]$File,
        [string[]]$ToolArgs = @(),
        [int]$TimeoutSeconds = 60,
        [string]$WorkingDirectory = $Worktree,
        [string]$StandardInput = $null,
        [string]$Stage = ''
    )
    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $File
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $null -ne $StandardInput
    $psi.CreateNoWindow = $true
    foreach ($a in $ToolArgs) { $null = $psi.ArgumentList.Add($a) }
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi
    try {
        if (-not [string]::IsNullOrWhiteSpace($Stage)) { Write-Host ('FOX2_PREEXEC_STAGE=' + $Stage) }
        Require ($p.Start()) ('TOOL_START_FAILED:' + $Stage + ':' + $File)

        $outTask = $p.StandardOutput.ReadToEndAsync()
        $errTask = $p.StandardError.ReadToEndAsync()

        if ($null -ne $StandardInput) {
            $p.StandardInput.Write($StandardInput)
            $p.StandardInput.Close()
        }

        if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
            try {
                $p.Kill($true)
                $p.WaitForExit()
            } catch {}
            $outText = try { $outTask.GetAwaiter().GetResult() } catch { '' }
            $errText = try { $errTask.GetAwaiter().GetResult() } catch { '' }
            throw ('TOOL_TIMEOUT:' + $Stage + ':' + [IO.Path]::GetFileName($File) + ':' + (Safe-Text ($errText + ' ' + $outText)))
        }

        $outText = $outTask.GetAwaiter().GetResult()
        $errText = $errTask.GetAwaiter().GetResult()

        [pscustomobject]@{
            Code = [int]$p.ExitCode
            Out = $outText
            Err = $errText
        }
    }
    finally {
        $p.Dispose()
    }
}

$GitExe = (Get-Command git.exe -ErrorAction Stop).Source
$PythonExe = (Get-Command python.exe -ErrorAction Stop).Source
$CodexExe = (Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
$DotnetExe = (Get-Command dotnet -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source

function Git([string[]]$GitArgs) {
    Require ($null -ne $GitArgs -and $GitArgs.Count -ge 1) 'GIT_ARGUMENTS_EMPTY'
    $r = Run-Tool -File $GitExe -ToolArgs (@('-C',$Worktree) + $GitArgs) -TimeoutSeconds 60
    if ($r.Code -ne 0) {
        $detail = ([string]$r.Err).Trim()
        if ($detail.Length -gt 300) { $detail = $detail.Substring(0,300) }
        throw ('GIT_FAILED:' + $GitArgs[0] + ':' + $detail)
    }
    return ([string]$r.Out).Trim()
}

function Remote-Head {
    $r = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'ls-remote','--refs','origin',('refs/heads/' + $Branch)) -TimeoutSeconds 60
    Require ($r.Code -eq 0) 'REMOTE_READ_FAILED'
    $line = ([string]$r.Out).Trim()
    Require (-not [string]::IsNullOrWhiteSpace($line)) 'REMOTE_BRANCH_MISSING'
    return (($line -split '\s+')[0]).Trim()
}

function Git-Object-Sha256([string]$Spec) {
    $code = 'import hashlib,subprocess,sys; d=subprocess.check_output(["git","-C",sys.argv[1],"show",sys.argv[2]]); print(hashlib.sha256(d).hexdigest())'
    $r = Run-Tool -File $PythonExe -ToolArgs @('-c',$code,$Worktree,$Spec) -TimeoutSeconds 60
    Require ($r.Code -eq 0) ('SHA256_FAILED:' + $Spec)
    return ([string]$r.Out).Trim()
}

function Assert-NoTaskWriter {
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    $services = @(Get-CimInstance Win32_Service -ErrorAction Stop)
    $markers = @($Worktree, ($Worktree -replace '\\','/'), $Branch, $TaskId, $TaskPath, $PromptPath)

    foreach ($record in $processes) {
        $name = [string]$record.Name
        $line = [string]$record.CommandLine
        $pidValue = [int]$record.ProcessId
        $parentPid = [int]$record.ParentProcessId
        $session = [int]$record.SessionId
        $parent = $processes | Where-Object { [int]$_.ProcessId -eq $parentPid } | Select-Object -First 1
        $parentName = if ($null -eq $parent) { '' } else { [string]$parent.Name }

        if ($name -ieq 'codex-windows-sandbox-service.exe') {
            $matching = @($services | Where-Object { [int]$_.ProcessId -eq $pidValue })
            Require ($session -eq 0 -and $parentName -ieq 'services.exe' -and $matching.Count -ge 1) 'CODEX_SANDBOX_SERVICE_IDENTITY_UNVERIFIED'
            continue
        }

        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper = (($name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$') -and
                      (-not [string]::IsNullOrWhiteSpace($line)) -and
                      ($line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)'))
        if (-not ($isCodex -or $isWrapper)) { continue }

        Require (-not [string]::IsNullOrWhiteSpace($line)) 'CODEX_PROCESS_ATTRIBUTION_UNKNOWN'
        foreach ($m in $markers) {
            Require ($line.IndexOf($m,[StringComparison]::OrdinalIgnoreCase) -lt 0) 'TASK_SCOPED_CODEX_WRITER_PRESENT'
        }
    }
}

function Safe-Text([string]$Value, [int]$Max = 500) {
    if ($null -eq $Value) { return '' }
    $v = $Value -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'
    $v = $v.Trim()
    if ($v.Length -gt $Max) { $v = $v.Substring(0,$Max) }
    return $v
}

Write-Output '=== FOX2 LIFECYCLE/WPF CONTRACT REWORK A01 PREEXEC ==='
Write-Output ('FOX2_PREEXEC_BRANCH=' + $Branch)
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)

Require (Test-Path -LiteralPath $Worktree -PathType Container) 'WORKTREE_MISSING'
Require ((Git @('branch','--show-current')) -ceq $Branch) 'WRONG_BRANCH'
Require ((Git @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_HEAD_MISMATCH'
Require ((Remote-Head) -ceq $PublicationHead) 'REMOTE_HEAD_MISMATCH'
Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY'

$observedScriptBlob = Git @('hash-object','--no-filters',(Join-Path $Worktree ($ScriptPath -replace '/', [IO.Path]::DirectorySeparatorChar)))
Require ($observedScriptBlob -ceq $ExpectedScriptBlob) 'PREEXEC_SCRIPT_BLOB_MISMATCH'

Require ((Git @('rev-parse',($TaskCommit + ':' + $TaskPath))) -ceq $TaskBlob) 'TASK_BLOB_MISMATCH'
Require ((Git @('rev-parse',($PromptCommit + ':' + $PromptPath))) -ceq $PromptBlob) 'PROMPT_BLOB_MISMATCH'
Require ((Git-Object-Sha256 ($TaskCommit + ':' + $TaskPath)) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((Git-Object-Sha256 ($PromptCommit + ':' + $PromptPath)) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'

$sourceAncestor = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$SourceBase,$PublicationHead) -TimeoutSeconds 30
Require ($sourceAncestor.Code -eq 0) 'SOURCE_RESULT_BASE_NOT_ANCESTOR'
$productAncestor = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$ProductSource,$SourceBase) -TimeoutSeconds 30
Require ($productAncestor.Code -eq 0) 'PRODUCT_SOURCE_NOT_ANCESTOR_OF_RESULT_BASE'
$productDrift = Git @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--','agent_bridge')
Require ([string]::IsNullOrWhiteSpace($productDrift)) 'PREEXEC_PRODUCT_CODE_DRIFT'

$ancestor = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$PromptCommit,$PublicationHead) -TimeoutSeconds 30
Require ($ancestor.Code -eq 0) 'PREEXEC_PUBLICATION_NOT_DESCENDANT_OF_PROMPT'
$lineageOut = Git @('rev-list',($PromptCommit + '..' + $PublicationHead))
$lineage = @($lineageOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($lineage.Count -eq 2) 'PREEXEC_PUBLICATION_LINEAGE_COUNT_MISMATCH'
$paths = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($commit in $lineage) {
    $pOut = Git @('diff-tree','--no-commit-id','--name-only','-r',$commit)
    foreach ($p in @($pOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
        $null = $paths.Add($p)
    }
}
Require ($paths.Count -eq 2) 'PREEXEC_PUBLICATION_PATH_COUNT_MISMATCH'
Require ($paths.Contains($InvalidV1Path)) 'PREEXEC_V1_HISTORY_MISSING'
Require ($paths.Contains($ScriptPath)) 'PREEXEC_V2_PUBLICATION_MISSING'
Require ((Git @('rev-parse',('544c1a39861966b3d589f692bb8e0b27c6f329c3:' + $InvalidV1Path))) -ceq $InvalidV1Blob) 'PREEXEC_V1_BLOB_MISMATCH'

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require (-not (Test-Path -LiteralPath $receiptFull)) 'PREEXEC_RECEIPT_ALREADY_EXISTS'
$receiptInGit = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'cat-file','-e',($PublicationHead + ':' + $ReceiptPath)) -TimeoutSeconds 30
Require ($receiptInGit.Code -ne 0) 'PREEXEC_RECEIPT_ALREADY_COMMITTED'

Assert-NoTaskWriter

$lingeringProbe = @(
    Get-CimInstance Win32_Process -ErrorAction Stop |
    Where-Object {
        -not [string]::IsNullOrWhiteSpace([string]$_.CommandLine) -and
        ([string]$_.CommandLine).IndexOf(
            'FOX2-lifecycle-wpf-rework-preexec-',
            [StringComparison]::OrdinalIgnoreCase
        ) -ge 0
    }
)
Require ($lingeringProbe.Count -eq 0) 'LINGERING_PREEXEC_CODEX_PROBE_PROCESS'

$pythonVersion = Run-Tool -File $PythonExe -ToolArgs @('-c','import json,sys; print(json.dumps({"major":sys.version_info.major,"minor":sys.version_info.minor,"version":".".join(map(str,sys.version_info[:3]))}))') -TimeoutSeconds 30 -Stage 'PYTHON_VERSION'
Require ($pythonVersion.Code -eq 0) 'PYTHON_NOT_READY'
$pythonInfo = ([string]$pythonVersion.Out).Trim() | ConvertFrom-Json
Require ([int]$pythonInfo.major -eq 3 -and [int]$pythonInfo.minor -ge 13) 'PYTHON_3_13_REQUIRED'

$dotnetVersionProbe = Run-Tool -File $DotnetExe -ToolArgs @('--version') -TimeoutSeconds 30 -Stage 'DOTNET_VERSION'
Require ($dotnetVersionProbe.Code -eq 0) 'DOTNET_NOT_READY'
$dotnetVersion = ([string]$dotnetVersionProbe.Out).Trim()
Require (-not [string]::IsNullOrWhiteSpace($dotnetVersion)) 'DOTNET_VERSION_EMPTY'

$login = Run-Tool -File $CodexExe -ToolArgs @('login','status') -TimeoutSeconds 60 -Stage 'CODEX_LOGIN_STATUS'
Require ($login.Code -eq 0) 'CODEX_LOGIN_NOT_READY'

$help = Run-Tool -File $CodexExe -ToolArgs @('exec','--help') -TimeoutSeconds 60 -Stage 'CODEX_EXEC_HELP'
Require ($help.Code -eq 0) 'CODEX_EXEC_HELP_FAILED'
$helpText = [string]$help.Out + [string]$help.Err
foreach ($flag in @('--model','--sandbox','--config','--skip-git-repo-check','--cd','--output-last-message')) {
    Require ($helpText.Contains($flag)) ('CODEX_FLAG_MISSING:' + $flag)
}

$temp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-lifecycle-wpf-rework-preexec-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($temp) | Out-Null
$lastMessage = Join-Path $temp 'last_message.txt'
$probePrompt = 'FOX2 route-admission probe only. Do not inspect files, do not use tools, do not execute commands, and do not modify anything. Reply with exactly ' + $Marker + ' and nothing else.'
try {
    $probeArgs = @(
        'exec',
        '--model',$Model,
        '--sandbox','read-only',
        '--config','approval_policy="never"',
        '--config',('model_reasoning_effort=' + $ReasoningEffort),
        '--skip-git-repo-check',
        '--cd',$temp,
        '--output-last-message',$lastMessage,
        '-'
    )
    $probe = Run-Tool -File $CodexExe -ToolArgs $probeArgs -TimeoutSeconds 240 -WorkingDirectory $temp -StandardInput ($probePrompt + [Environment]::NewLine) -Stage 'CODEX_LIVE_PROBE'
    $markerValue = if (Test-Path -LiteralPath $lastMessage) { [IO.File]::ReadAllText($lastMessage).Trim() } else { '' }
    Require ($probe.Code -eq 0) ('CODEX_LIVE_PROBE_FAILED:' + (Safe-Text ($probe.Err + ' ' + $probe.Out)))
    Require ($markerValue -ceq $Marker) ('CODEX_LIVE_MARKER_MISMATCH:' + (Safe-Text $markerValue))
}
finally {
    try { if ([IO.Directory]::Exists($temp)) { [IO.Directory]::Delete($temp,$true) } } catch {}
}

Assert-NoTaskWriter
Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY_AFTER_PROBE'
Require ((Git @('rev-parse','HEAD')) -ceq $PublicationHead) 'HEAD_DRIFT_AFTER_PROBE'
Require ((Remote-Head) -ceq $PublicationHead) 'REMOTE_DRIFT_AFTER_PROBE'

$receipt = [ordered]@{
    schema_version = '1.0'
    receipt_type = 'FOX2_PREEXEC_RECEIPT'
    project = 'FOX2'
    wp_id = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
    task_id = $TaskId
    checked_at = [DateTime]::UtcNow.ToString('o')
    status = 'PASS'
    blockers = @()
    task_branch = $Branch
    source_result_base = $SourceBase
    product_source = $ProductSource
    publication_head = $PublicationHead
    task = [ordered]@{ commit=$TaskCommit; path=$TaskPath; blob_sha1=$TaskBlob; sha256=$TaskSha256 }
    prompt = [ordered]@{ commit=$PromptCommit; path=$PromptPath; blob_sha1=$PromptBlob; sha256=$PromptSha256 }
    route = [ordered]@{
        agent='CODEX'; model=$Model; reasoning_effort=$ReasoningEffort
        permission_profile='FULL_ACCESS'; execution_path='MANUAL_LOCAL'
    }
    capabilities = [ordered]@{
        pwsh7='PASS'; python='PASS'; git='PASS'; codex_login='PASS'
        codex_cli_contract='PASS'; one_writer='PASS'; exact_task_prompt='PASS'
        clean_worktree='PASS'; live_route_admission='PASS'; dotnet='PASS'; python_3_13='PASS'
    }
    observed_versions = [ordered]@{
        python=[string]$pythonInfo.version; pwsh=[string]$PSVersionTable.PSVersion; dotnet=$dotnetVersion
    }
    live_probe = [ordered]@{
        status='PASS'; exit_code=0; marker=$Marker
        working_directory_kind='EMPTY_TEMP_DIRECTORY'
        sandbox='read-only'; approval_policy='never_via_config_override'
        project_files_accessed=$false
    }
    implementation_agent_execution_started = $false
    dispatch_published = $false
    dispatch_consumed = $false
    real_host_lifecycle_mutation = $false
    g3_mutation = $false
    notes = @(
        'PreExec v1 was rejected before execution and is historical non-executable evidence.',
        'PreExec v2 is the current Source BUILD rework PreExec; no product code changed.',
        'Live probe verifies pinned CODEX route reachability only.',
        'Real installed Bridge launch/install/update/uninstall/reinstall remains NOT_RUN.',
        'Worker/F1/G3/G4/AppLocker/service/ACL mutation remains NOT_RUN.',
        'Final assignment still requires CHAT remote intake and a fresh executable Dispatch.'
    )
}

$receiptDir = Split-Path -Parent $receiptFull
[IO.Directory]::CreateDirectory($receiptDir) | Out-Null
$json = ($receipt | ConvertTo-Json -Depth 12).TrimEnd()
$json = $json.Replace("`r`n", "`n")
Require (-not $json.Contains("`r")) 'PREEXEC_RECEIPT_LONE_CR'
$json = $json + "`n"
[IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))

$afterOut = Git @('status','--porcelain=v1','--untracked-files=all')
$after = @($afterOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($after.Count -eq 1 -and $after[0].EndsWith($ReceiptPath)) 'PREEXEC_UNEXPECTED_WIP'

Git @('add','--',$ReceiptPath) | Out-Null
$stagedOut = Git @('diff','--cached','--name-only')
$staged = @($stagedOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($staged.Count -eq 1 -and $staged[0] -ceq $ReceiptPath) 'PREEXEC_STAGED_SCOPE_MISMATCH'
$diffCheck = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'diff','--cached','--check') -TimeoutSeconds 30
Require ($diffCheck.Code -eq 0) ('PREEXEC_DIFF_CHECK_FAILED:' + (Safe-Text $diffCheck.Err))

$commit = Run-Tool -File $GitExe -ToolArgs @(
    '-C',$Worktree,
    '-c','core.hooksPath=NUL',
    '-c','commit.gpgsign=false',
    '-c','user.name=FOX2 PreExec',
    '-c','user.email=fox2-preexec@local.invalid',
    'commit','-m','preexec(fox2): lifecycle WPF contract rework A01 PASS'
) -TimeoutSeconds 60
Require ($commit.Code -eq 0) ('PREEXEC_COMMIT_FAILED:' + (Safe-Text ($commit.Err + ' ' + $commit.Out)))

$receiptCommit = Git @('rev-parse','HEAD')
$parents = Git @('rev-list','--parents','-n','1',$receiptCommit)
Require ($parents -ceq ($receiptCommit + ' ' + $PublicationHead)) 'PREEXEC_RECEIPT_PARENT_MISMATCH'
$commitPathsOut = Git @('diff-tree','--no-commit-id','--name-only','-r',$receiptCommit)
$commitPaths = @($commitPathsOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($commitPaths.Count -eq 1 -and $commitPaths[0] -ceq $ReceiptPath) 'PREEXEC_RECEIPT_COMMIT_SCOPE_MISMATCH'

Require ((Remote-Head) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_PREEXEC_PUSH'
$push = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'push','origin',($receiptCommit + ':refs/heads/' + $Branch)) -TimeoutSeconds 90
Require ($push.Code -eq 0) ('PREEXEC_PUSH_FAILED:' + (Safe-Text ($push.Err + ' ' + $push.Out)))
Require ((Remote-Head) -ceq $receiptCommit) 'PREEXEC_REMOTE_READBACK_MISMATCH'

$receiptBlob = Git @('rev-parse',($receiptCommit + ':' + $ReceiptPath))
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_MODEL=' + $Model)
Write-Output ('FOX2_PREEXEC_REASONING=' + $ReasoningEffort)
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
Write-Output 'FOX2_REAL_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_G3_MUTATION=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_DISPATCH'
