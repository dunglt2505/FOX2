#requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$PublicationHead,
    [Parameter(Mandatory)][string]$ExpectedScriptBlob,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Branch = 'work/FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-FIX-20261021'
$TaskId = 'FOX2-BRIDGE-RC1-PACKAGE-LIFECYCLE-A03'
$TaskCommit = 'ac12501e1b3c94a0e75b72adc7dc78743d18e660'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix_attempt03/task.md'
$TaskBlob = '264c1bb54e985d8cd3a73df21072b04271b79d6c'
$TaskSha256 = 'b6bbe42d781939a1b05b1dd2aa3fd985677d970b783ab8c2a30b11e9ada85c7e'

$PromptCommit = '39d6a8f36dd573a4fb9e61a5d4102a15e9b3a80f'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix_attempt03/prompt.md'
$PromptBlob = '23e562253b1d61f413ed6378a218ba903f87d92e'
$PromptSha256 = '25ff86531e9841a9cc8cde6259f0fc9512fe8949c98a57457d689c61bcabce77'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/package_lifecycle_fix_attempt03/package_lifecycle_a03_preexec.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/package_lifecycle_a03.json'

$Model = 'gpt-6.1-sol'
$ReasoningEffort = 'high'
$Marker = 'FOX2_PACKAGE_LIFECYCLE_A03_ADMISSION_OK'

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

Write-Output '=== FOX2 PACKAGE LIFECYCLE A03 PREEXEC ==='
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

$ancestor = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$PromptCommit,$PublicationHead) -TimeoutSeconds 30
Require ($ancestor.Code -eq 0) 'PREEXEC_PUBLICATION_NOT_DESCENDANT_OF_PROMPT'
$lineageOut = Git @('rev-list',($PromptCommit + '..' + $PublicationHead))
$lineage = @($lineageOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($lineage.Count -ge 1) 'PREEXEC_PUBLICATION_LINEAGE_EMPTY'
$paths = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($commit in $lineage) {
    $pOut = Git @('diff-tree','--no-commit-id','--name-only','-r',$commit)
    foreach ($p in @($pOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
        $null = $paths.Add($p)
    }
}
Require ($paths.Count -eq 1 -and $paths.Contains($ScriptPath)) 'PREEXEC_PUBLICATION_NOT_SCRIPT_ONLY'

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
            'FOX2-package-lifecycle-preexec-',
            [StringComparison]::OrdinalIgnoreCase
        ) -ge 0
    }
)
Require ($lingeringProbe.Count -eq 0) 'LINGERING_PREEXEC_CODEX_PROBE_PROCESS'

$login = Run-Tool -File $CodexExe -ToolArgs @('login','status') -TimeoutSeconds 60 -Stage 'CODEX_LOGIN_STATUS'
Require ($login.Code -eq 0) 'CODEX_LOGIN_NOT_READY'

$help = Run-Tool -File $CodexExe -ToolArgs @('exec','--help') -TimeoutSeconds 60 -Stage 'CODEX_EXEC_HELP'
Require ($help.Code -eq 0) 'CODEX_EXEC_HELP_FAILED'
$helpText = [string]$help.Out + [string]$help.Err
foreach ($flag in @('--model','--sandbox','--config','--skip-git-repo-check','--cd','--output-last-message')) {
    Require ($helpText.Contains($flag)) ('CODEX_FLAG_MISSING:' + $flag)
}

$temp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-package-lifecycle-preexec-' + [Guid]::NewGuid().ToString('N'))
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
    source_code_base = 'b065a468279cbf63ae4bbfad7a0efaad1e6046e4'
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
        clean_worktree='PASS'; live_route_admission='PASS'
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
    host_lifecycle_mutation = $false
    notes = @(
        'PreExec only; no product code changed.',
        'Live probe verifies pinned CODEX route reachability only.',
        'Real install/update/uninstall/reinstall remains NOT_RUN.',
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
    'commit','-m','preexec(fox2): package lifecycle A03 route PASS'
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
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_DISPATCH'
