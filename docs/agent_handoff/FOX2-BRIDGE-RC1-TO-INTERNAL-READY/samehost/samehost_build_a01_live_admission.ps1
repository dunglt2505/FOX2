#requires -Version 7.0
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$PublicationHead,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false

$Branch = 'work/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021'
$MetadataReceiptCommit = 'f60ab169baaf8c3e0f644adbf850021cea9ebf7d'
$MetadataReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/samehost_build_a01.json'
$MetadataReceiptBlob = '340ea3401d8ea94b86ae85bd8f067d17ddb44bb8'
$TaskSourceHead = '600f8ceb6943d1f1ecf341ff06072bf31c1babe0'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/task.md'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/prompt.md'
$TaskBlob = '8b69f093b8e625fd4404d07d3922658a9bc84a0d'
$PromptBlob = 'f9a60988fd5e13158cd898492910e92dfbbed253'
$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/samehost_build_a01_live_admission.ps1'
$EvidencePath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/samehost/samehost_build_a01_live_admission.json'
$Model = 'gpt-6.1-sol'
$ReasoningEffort = 'high'
$Marker = 'FOX2_ADMISSION_OK'
$Lock = $null
$TempProbeDir = $null

function Run-Tool {
    param(
        [Parameter(Mandatory)][string]$File,
        [string[]]$ToolArgs = @(),
        [int]$TimeoutSeconds = 60,
        [string]$WorkingDirectory = $Worktree,
        [string]$StandardInput = ''
    )
    $si = [Diagnostics.ProcessStartInfo]::new()
    $si.FileName = $File
    $si.WorkingDirectory = $WorkingDirectory
    $si.UseShellExecute = $false
    $si.CreateNoWindow = $true
    $si.RedirectStandardOutput = $true
    $si.RedirectStandardError = $true
    $si.RedirectStandardInput = $true
    foreach ($item in $ToolArgs) { $si.ArgumentList.Add($item) }
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $si
    try {
        if (-not $p.Start()) { throw 'TOOL_START_FAILED' }
        if (-not [string]::IsNullOrEmpty($StandardInput)) { $p.StandardInput.Write($StandardInput) }
        $p.StandardInput.Close()
        $stdoutTask = $p.StandardOutput.ReadToEndAsync()
        $stderrTask = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
            $p.Kill($true)
            $p.WaitForExit()
            throw 'TOOL_TIMEOUT'
        }
        return [ordered]@{
            Code = $p.ExitCode
            Text = $stdoutTask.GetAwaiter().GetResult().Trim()
            ErrorText = $stderrTask.GetAwaiter().GetResult().Trim()
        }
    }
    finally {
        $p.Dispose()
    }
}

function Git {
    param([Parameter(Mandatory)][string[]]$GitArgs)
    $r = Run-Tool -File $GitExe -ToolArgs (@('-C', $Worktree) + $GitArgs) -TimeoutSeconds 60 -WorkingDirectory $Worktree
    if ($r.Code -ne 0) { throw ('GIT_FAILED:' + $GitArgs[0]) }
    return [string]$r.Text
}

function Require {
    param([bool]$Condition, [string]$Code)
    if (-not $Condition) { throw $Code }
}

function Remote-Head {
    $line = Git @('ls-remote','--refs','origin',('refs/heads/' + $Branch))
    Require ($line -match '^[0-9a-f]{40}\s+refs/heads/') 'REMOTE_UNREADABLE'
    return ($line -split '\s+')[0]
}

function Assert-NoTaskWriter {
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    $services = @(Get-CimInstance Win32_Service -ErrorAction Stop)
    $markers = @(
        $Worktree,
        $Worktree.Replace('\','/'),
        'FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01',
        $Branch,
        'FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021',
        $TaskPath,
        $PromptPath
    )

    foreach ($record in $processes) {
        $name = [string]$record.Name
        $line = [string]$record.CommandLine
        $session = [int]$record.SessionId
        $processIdValue = [int]$record.ProcessId
        $parentProcessIdValue = [int]$record.ParentProcessId
        $parent = $processes | Where-Object { [int]$_.ProcessId -eq $parentProcessIdValue } | Select-Object -First 1
        $parentName = if ($null -ne $parent) { [string]$parent.Name } else { '' }

        if ($name -ieq 'codex-windows-sandbox-service.exe') {
            $matchingService = @($services | Where-Object { [int]$_.ProcessId -eq $processIdValue })
            $scmInfrastructure = ($session -eq 0 -and $parentName -ieq 'services.exe' -and $matchingService.Count -ge 1)
            Require $scmInfrastructure 'CODEX_SANDBOX_SERVICE_IDENTITY_UNVERIFIED'
            continue
        }

        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper = (($name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$') -and (-not [string]::IsNullOrWhiteSpace($line)) -and ($line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)'))
        if (-not ($isCodex -or $isWrapper)) { continue }

        Require (-not [string]::IsNullOrWhiteSpace($line)) 'CODEX_PROCESS_ATTRIBUTION_UNKNOWN'
        foreach ($markerValue in $markers) {
            Require ($line.IndexOf($markerValue,[StringComparison]::OrdinalIgnoreCase) -lt 0) 'TASK_SCOPED_CODEX_WRITER_PRESENT'
        }
    }
}

function Classify-ProbeFailure {
    param([string]$Text)
    if ($Text -match '(?i)(quota|usage limit|rate limit|too many requests|\b429\b)') { return 'CODEX_QUOTA_UNAVAILABLE' }
    if ($Text -match '(?i)(model.+not.+available|unknown model|model.+not found|unsupported model|does not have access to model)') { return 'CODEX_MODEL_UNAVAILABLE' }
    if ($Text -match '(?i)(authentication|unauthorized|forbidden|not logged in|\b401\b|\b403\b)') { return 'CODEX_AUTH_RUNTIME_FAILED' }
    return 'CODEX_LIVE_RUNTIME_PROBE_FAILED'
}

try {
    Require $IsWindows 'WINDOWS_REQUIRED'
    Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL7_REQUIRED'

    $Worktree = (Resolve-Path -LiteralPath $Worktree).Path
    $GitExe = (Get-Command git -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source

    Require ((Git @('rev-parse','--show-toplevel')).Replace('/','\') -eq $Worktree.TrimEnd('\')) 'WORKTREE_ROOT_MISMATCH'
    Require ((Git @('branch','--show-current')) -ceq $Branch) 'BRANCH_MISMATCH'

    $initialHead = Git @('rev-parse','HEAD')
    Require ($initialHead -in @($MetadataReceiptCommit,$PublicationHead)) 'HEAD_MISMATCH'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'DIRTY_WORKTREE'
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_HEAD_MISMATCH'
    Require ((Git @('rev-list','--parents','-n','1',$PublicationHead)) -ceq ($PublicationHead + ' ' + $MetadataReceiptCommit)) 'PUBLICATION_PARENT_MISMATCH'

    $changedLine = Git @('diff-tree','--no-commit-id','--name-status','-r',$MetadataReceiptCommit,$PublicationHead)
    Require ($changedLine -ceq ('A' + [char]9 + $ScriptPath)) 'PUBLICATION_NOT_SCRIPT_ONLY'

    $scriptBlob = Git @('rev-parse',($PublicationHead + ':' + $ScriptPath))
    Require ((Git @('hash-object','--no-filters',$PSCommandPath)) -eq $scriptBlob) 'RUNNING_SCRIPT_MISMATCH'
    Require ((Git @('rev-parse',($MetadataReceiptCommit + ':' + $MetadataReceiptPath))) -eq $MetadataReceiptBlob) 'METADATA_RECEIPT_BLOB_MISMATCH'
    Require ((Git @('rev-parse',($TaskSourceHead + ':' + $TaskPath))) -eq $TaskBlob) 'TASK_BLOB_MISMATCH'
    Require ((Git @('rev-parse',($TaskSourceHead + ':' + $PromptPath))) -eq $PromptBlob) 'PROMPT_BLOB_MISMATCH'

    Assert-NoTaskWriter

    $lockFile = Git @('rev-parse','--git-path','fox2-samehost-live-admission.lock')
    if (-not [IO.Path]::IsPathRooted($lockFile)) { $lockFile = Join-Path $Worktree $lockFile }
    $Lock = [IO.File]::Open($lockFile,[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)

    if ($initialHead -eq $MetadataReceiptCommit) {
        $null = Git @('-c','core.hooksPath=NUL','merge','--ff-only',$PublicationHead)
    }

    Require ((Git @('rev-parse','HEAD')) -eq $PublicationHead) 'ADMISSION_HEAD_MISMATCH'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_BEFORE_PROBE'
    Require (-not (Test-Path -LiteralPath (Join-Path $Worktree $EvidencePath))) 'ADMISSION_EVIDENCE_ALREADY_EXISTS_NO_REPLAY'

    $CodexExe = (Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    Require (-not [string]::IsNullOrWhiteSpace($CodexExe)) 'CODEX_EXE_UNAVAILABLE'

    $help = Run-Tool -File $CodexExe -ToolArgs @('exec','--help') -TimeoutSeconds 30
    Require ($help.Code -eq 0) 'CODEX_EXEC_HELP_FAILED'
    $helpText = $help.Text + [Environment]::NewLine + $help.ErrorText

    foreach ($requiredFlag in @('--model','--sandbox','--config','--skip-git-repo-check','--cd','--output-last-message')) {
        Require ($helpText.Contains($requiredFlag)) ('CODEX_FLAG_MISSING:' + $requiredFlag)
    }

    Assert-NoTaskWriter

    $TempProbeDir = Join-Path ([IO.Path]::GetTempPath()) ('fox2_samehost_live_admission_' + [guid]::NewGuid().ToString('N'))
    $null = New-Item -ItemType Directory -Path $TempProbeDir -Force
    $LastMessagePath = Join-Path $TempProbeDir 'last_message.txt'

    $probePrompt = 'FOX2 route-admission probe only. Do not inspect files, do not use tools, do not execute commands, and do not modify anything. Reply with exactly ' + $Marker + ' and nothing else.'
    $probeArgs = @(
        'exec',
        '--model',$Model,
        '--sandbox','read-only',
        '--config','approval_policy="never"',
        '--config',('model_reasoning_effort=' + $ReasoningEffort),
        '--skip-git-repo-check',
        '--cd',$TempProbeDir,
        '--output-last-message',$LastMessagePath,
        '-'
    )

    $startedAt = [DateTime]::UtcNow
    $probe = Run-Tool -File $CodexExe -ToolArgs $probeArgs -TimeoutSeconds 180 -WorkingDirectory $TempProbeDir -StandardInput ($probePrompt + [Environment]::NewLine)
    $finishedAt = [DateTime]::UtcNow

    $markerObserved = $false
    if (Test-Path -LiteralPath $LastMessagePath -PathType Leaf) {
        $lastMessage = [IO.File]::ReadAllText($LastMessagePath,[Text.Encoding]::UTF8).Trim()
        $markerObserved = ($lastMessage -ceq $Marker)
    }

    $statusValue = 'BLOCKED'
    $failureClass = $null

    if ($probe.Code -eq 0 -and $markerObserved) {
        $statusValue = 'PASS'
    }
    else {
        $failureClass = Classify-ProbeFailure -Text ($probe.Text + [Environment]::NewLine + $probe.ErrorText)
    }

    Assert-NoTaskWriter
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_DRIFT_AFTER_PROBE'
    Require ((Git @('rev-parse','HEAD')) -eq $PublicationHead) 'LOCAL_DRIFT_AFTER_PROBE'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'PROJECT_WIP_AFTER_PROBE'

    $evidenceFull = Join-Path $Worktree $EvidencePath
    $null = New-Item -ItemType Directory -Force -Path (Split-Path -Parent $evidenceFull)

    $evidence = [ordered]@{
        schema_version = '1.0'
        evidence_type = 'FOX2_CODEX_LIVE_ADMISSION_PROBE'
        project = 'FOX2'
        wp_id = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
        task_id = 'FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01'
        checked_at = $finishedAt.ToString('o')
        task_branch = $Branch
        metadata_preexec_commit = $MetadataReceiptCommit
        admission_tool_commit = $PublicationHead
        task_source_commit = $TaskSourceHead
        model = $Model
        reasoning_effort = $ReasoningEffort
        sandbox = 'read-only'
        approval_policy = 'never_via_config_override'
        status = $statusValue
        probe_agent_execution_started = $true
        task_agent_execution_started = $false
        dispatch_consumed = $false
        host_policy_mutation = $false
        project_files_accessed_by_probe = $false
        probe_working_directory_kind = 'EMPTY_TEMP_DIRECTORY'
        probe_exit_code = [int]$probe.Code
        marker_expected = $Marker
        marker_match = [bool]$markerObserved
        failure_class = $failureClass
        duration_seconds = [Math]::Round(($finishedAt - $startedAt).TotalSeconds,3)
        notes = @(
            'This evidence proves only pinned CODEX model/quota/runtime route reachability at observation time.',
            'The implementation task was not started or consumed.',
            'The probe used an empty temporary directory and read-only sandbox.',
            'CODEX CLI 0.162.1 admission uses --config approval_policy="never" because codex exec --help does not expose --ask-for-approval.',
            'Raw CODEX stdout/stderr are not persisted in Git.'
        )
    }

    $json = (($evidence | ConvertTo-Json -Depth 10) -replace [char]13 + [char]10,[string][char]10).TrimEnd() + [char]10
    [IO.File]::WriteAllText($evidenceFull,$json,[Text.UTF8Encoding]::new($false))

    Require ((Git @('status','--porcelain=v1','--untracked-files=all')) -ceq ('?? ' + $EvidencePath)) 'UNRELATED_WIP_BEFORE_EVIDENCE_COMMIT'
    $null = Git @('add','--',$EvidencePath)
    $null = Git @('diff','--cached','--check')
    Require ((Git @('diff','--cached','--name-only')) -ceq $EvidencePath) 'STAGED_PATH_OUTSIDE_ADMISSION_EVIDENCE'

    $evidenceBlob = Git @('rev-parse',(':' + $EvidencePath))

    $null = Git @(
        '-c','core.hooksPath=NUL',
        '-c','commit.gpgsign=false',
        '-c','user.name=FOX2 Admission',
        '-c','user.email=fox2-admission@local.invalid',
        'commit','-m','preexec(fox2): record samehost BUILD A01 live route admission'
    )

    $evidenceCommit = Git @('rev-parse','HEAD')
    Require ((Git @('rev-list','--parents','-n','1',$evidenceCommit)) -ceq ($evidenceCommit + ' ' + $PublicationHead)) 'ADMISSION_EVIDENCE_PARENT_MISMATCH'
    Require ((Git @('diff-tree','--no-commit-id','--name-only','-r',$evidenceCommit)) -ceq $EvidencePath) 'ADMISSION_COMMIT_NOT_EVIDENCE_ONLY'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_AFTER_ADMISSION_COMMIT'
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_DRIFT_BEFORE_ADMISSION_PUSH'

    $null = Git @('-c','core.hooksPath=NUL','push','origin',($evidenceCommit + ':refs/heads/' + $Branch))
    Require ((Remote-Head) -eq $evidenceCommit) 'REMOTE_ADMISSION_EVIDENCE_MISMATCH'

    $null = Git @('fetch','--no-tags','origin',('refs/heads/' + $Branch))
    Require ((Git @('rev-parse','FETCH_HEAD')) -eq $evidenceCommit) 'REMOTE_ADMISSION_FETCH_MISMATCH'
    Require ((Git @('rev-parse',('FETCH_HEAD:' + $EvidencePath))) -eq $evidenceBlob) 'REMOTE_ADMISSION_BLOB_MISMATCH'

    Write-Output ('FOX2_ADMISSION_STATUS=' + $statusValue)
    Write-Output ('FOX2_ADMISSION_REMOTE_COMMIT=' + $evidenceCommit)
    Write-Output ('FOX2_ADMISSION_EVIDENCE_BLOB=' + $evidenceBlob)
    Write-Output ('FOX2_ADMISSION_MODEL=' + $Model)
    Write-Output ('FOX2_ADMISSION_REASONING=' + $ReasoningEffort)
    Write-Output ('FOX2_ADMISSION_PROBE_EXIT=' + $probe.Code)
    Write-Output ('FOX2_ADMISSION_MARKER_MATCH=' + $markerObserved)
    Write-Output ('FOX2_ADMISSION_FAILURE_CLASS=' + $(if ($null -eq $failureClass) { 'NONE' } else { $failureClass }))
    Write-Output 'FOX2_TASK_AGENT_EXECUTION_STARTED=FALSE'
    Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
    Write-Output 'FOX2_HOST_POLICY_MUTATION=FALSE'
    Write-Output 'FOX2_ADMISSION_DELIVERY=REMOTE_READBACK_PASS'
    Write-Output 'FOX2_NEXT=CHAT_INTAKE'

    if ($statusValue -eq 'BLOCKED') { exit 20 }
}
catch {
    Write-Output 'FOX2_ADMISSION_STATUS=BLOCKED'
    Write-Output ('FOX2_ADMISSION_STOP=' + $_.Exception.Message.Split([Environment]::NewLine)[0])
    Write-Output 'FOX2_TASK_AGENT_EXECUTION_STARTED=FALSE'
    Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
    Write-Output 'FOX2_HOST_POLICY_MUTATION=FALSE'
    Write-Output 'FOX2_ADMISSION_DELIVERY=NOT_VERIFIED'
    Write-Output 'FOX2_NEXT=RECONCILE_EXISTING_STATE_NO_REPLAY'
    exit 20
}
finally {
    if ($null -ne $Lock) { $Lock.Dispose() }
    if ($null -ne $TempProbeDir -and (Test-Path -LiteralPath $TempProbeDir)) {
        Remove-Item -LiteralPath $TempProbeDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
