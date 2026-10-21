#requires -Version 7.0
<# Owner-authorized PreExec publication only. No implementation/host-policy execution.
   Source lock stays 600f8ceb; recovery is a script-only child of the pinned publication.
   Run in a child pwsh -File; no exit command can close the Owner's shell.
   Existing receipts/WIP are never deleted, reset, stashed or replayed.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][ValidatePattern('^[0-9a-f]{40}$')][string]$PublicationHead,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021'
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$SourceHead = '600f8ceb6943d1f1ecf341ff06072bf31c1babe0'
$PreviousPublication = 'f3a0e86515c5285715730ff86781eb71c62c7ab0'
$Branch = 'work/FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021'
$TaskId = 'FOX2-BRIDGE-RC1-SAMEHOST-BUILD-A01'
$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/samehost_build_a01_preexec.ps1'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/task.md'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/samehost/prompt.md'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/samehost_build_a01.json'
$SchemaPath = 'docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json'
$Caps = [ordered]@{}
$Blockers = [Collections.Generic.List[object]]::new()
$Lock = $null

function Run-Tool {
    param([string]$File, [string[]]$ToolArgs, [int]$Timeout = 30, [string]$RawArguments = '')
    $si = [Diagnostics.ProcessStartInfo]::new()
    $si.FileName = $File
    $si.WorkingDirectory = $Worktree
    $si.UseShellExecute = $false
    $si.CreateNoWindow = $true
    $si.RedirectStandardOutput = $true
    $si.RedirectStandardError = $true
    if ($RawArguments) { $si.Arguments = $RawArguments }
    else { foreach ($item in $ToolArgs) { $si.ArgumentList.Add($item) } }
    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $si
    try {
        if (-not $p.Start()) { throw 'TOOL_START_FAILED' }
        $stdout = $p.StandardOutput.ReadToEndAsync()
        $stderr = $p.StandardError.ReadToEndAsync()
        if (-not $p.WaitForExit($Timeout * 1000)) {
            $p.Kill($true)
            $p.WaitForExit()
            throw 'TOOL_TIMEOUT'
        }
        return @{ Code = $p.ExitCode; Text = $stdout.GetAwaiter().GetResult().Trim(); ErrorText = $stderr.GetAwaiter().GetResult().Trim() }
    } finally { $p.Dispose() }
}
function Git {
    param([string[]]$GitArgs)
    $r = Run-Tool $GitExe (@('-C', $Worktree) + $GitArgs)
    if ($r.Code -ne 0) { throw ('GIT_FAILED: ' + $GitArgs[0]) }
    return $r.Text
}
function Require {
    param([bool]$Condition, [string]$Code)
    if (-not $Condition) { throw $Code }
}
function Observe {
    param([string]$Name, [bool]$Ok, [string]$Evidence, [string]$Class = 'CAPABILITY')
    $Caps[$Name] = @{ status = $(if ($Ok) { 'PASS' } else { 'FAIL' }); material = $true; evidence = $Evidence }
    if (-not $Ok) { $Blockers.Add(@{ code = $Name.ToUpperInvariant(); class = $Class; material = $true; sanitized_detail = $Evidence }) }
}
function Remote-Head {
    $line = Git @('ls-remote', '--refs', 'origin', ('refs/heads/' + $Branch))
    Require ($line -match '^[0-9a-f]{40}\s+refs/heads/') 'REMOTE_UNREADABLE'
    return ($line -split '\s+')[0]
}
function Assert-Writers {
    $owners = @((Git @('worktree', 'list', '--porcelain')) -split '\r?\n' | Where-Object { $_ -eq ('branch refs/heads/' + $Branch) })
    Require ($owners.Count -eq 1) 'COMPETING_WORKTREE'
    # Process enumeration must succeed. Opaque user/session CODEX or wrappers block.
    $processes = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    $markers = @($Worktree, $Worktree.Replace('\','/'), $TaskId, $Branch, 'FOX2-BRIDGE-F1-SAME-HOST-POLICY-BUILD-20261021', $TaskPath, $PromptPath)
    foreach ($proc in $processes) {
        $name = [string]$proc.Name
        $line = [string]$proc.CommandLine
        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $wrapperName = $name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$'
        $opaque = [string]::IsNullOrWhiteSpace($line)
        # This process is the PreExec host, not a competing Agent wrapper.
        if ($wrapperName -and $proc.ProcessId -eq $PID) { continue }
        $isWrapper = $wrapperName
        if (-not ($isCodex -or $isWrapper)) { continue }
        # Even infrastructure must not carry a task marker when its line is readable.
        foreach ($marker in $markers) {
            Require ($line.IndexOf($marker, [StringComparison]::OrdinalIgnoreCase) -lt 0) 'TASK_SCOPED_CODEX_WRITER_PRESENT'
        }
        # Narrow SCM infrastructure identity; never exempt the codex-* family.
        $scmInfrastructure = $false
        if ($name -ieq 'codex-windows-sandbox-service.exe' -and $proc.SessionId -eq 0) {
            $parents = @($processes | Where-Object {
                $_.ProcessId -eq $proc.ParentProcessId -and
                $_.Name -ieq 'services.exe' -and $_.SessionId -eq 0
            })
            if ($parents.Count -eq 1) {
                # Optional read-only SCM corroboration. Access denial does not require elevation.
                $servicesReadable = $false
                $services = @()
                try {
                    $services = @(Get-CimInstance Win32_Service -ErrorAction Stop)
                    $servicesReadable = $true
                } catch { }
                if ($servicesReadable) {
                    $serviceRows = @($services | Where-Object { $_.ProcessId -eq $proc.ProcessId })
                    Require ($serviceRows.Count -gt 0) 'CODEX_SANDBOX_SERVICE_ATTRIBUTION_MISMATCH'
                }
                $scmInfrastructure = $true
                Write-Output ('FOX2_CODEX_INFRASTRUCTURE=SCM_SANDBOX; PROCESS_ID=' + $proc.ProcessId + '; SCM_CORROBORATED=' + $servicesReadable)
            }
        }
        if ($scmInfrastructure) { continue }
        Require (-not $opaque) 'CODEX_PROCESS_ATTRIBUTION_UNKNOWN'
    }
}
function Codex-Info {
    param([string[]]$InfoArgs)
    # Only fixed metadata/help calls below reach this function. Never exec/resume/run.
    if ($CodexExe.EndsWith('.ps1', [StringComparison]::OrdinalIgnoreCase)) {
        return Run-Tool (Join-Path $PSHOME 'pwsh.exe') (@('-NoProfile','-NonInteractive','-File',$CodexExe) + $InfoArgs)
    }
    if ($CodexExe.EndsWith('.cmd', [StringComparison]::OrdinalIgnoreCase)) {
        Require ($CodexExe -notmatch '["%!&|<>^\r\n]') 'UNSUPPORTED_CODEX_SHIM_PATH'
        return Run-Tool -File $env:ComSpec -ToolArgs @() -RawArguments ('/d /s /c ""' + $CodexExe + '" ' + ($InfoArgs -join ' ') + '"')
    }
    return Run-Tool $CodexExe $InfoArgs
}

try {
    Require ($IsWindows) 'WINDOWS_REQUIRED'
    $Worktree = (Resolve-Path -LiteralPath $Worktree).Path
    $GitExe = (Get-Command git -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    Require ((Git @('rev-parse','--show-toplevel')).Replace('/','\') -eq $Worktree.TrimEnd('\')) 'WORKTREE_ROOT_MISMATCH'
    Require ((Git @('branch','--show-current')) -ceq $Branch) 'BRANCH_MISMATCH'
    $initialHead = Git @('rev-parse','HEAD')
    Require ($initialHead -in @($SourceHead, $PreviousPublication, $PublicationHead)) 'HEAD_MISMATCH'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'DIRTY_WORKTREE'
    $origin = Git @('remote','get-url','origin')
    Require ($origin -match '^(https://github\.com/|git@github\.com:|ssh://git@github\.com/)dunglt2505/FOX2(?:\.git)?$') 'ORIGIN_MISMATCH'
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_HEAD_MISMATCH'
    Require ((Git @('rev-list','--parents','-n','1',$PreviousPublication)) -ceq ($PreviousPublication + ' ' + $SourceHead)) 'PREVIOUS_PUBLICATION_PARENT_MISMATCH'
    Require ((Git @('diff-tree','--no-commit-id','--name-status','-r',$SourceHead,$PreviousPublication)) -ceq ("A`t" + $ScriptPath)) 'PREVIOUS_PUBLICATION_NOT_SCRIPT_ONLY'
    Require ((Git @('rev-list','--parents','-n','1',$PublicationHead)) -ceq ($PublicationHead + ' ' + $PreviousPublication)) 'PUBLICATION_PARENT_MISMATCH'
    Require ((Git @('diff-tree','--no-commit-id','--name-status','-r',$SourceHead,$PublicationHead)) -ceq ("A`t" + $ScriptPath)) 'PUBLICATION_NOT_SCRIPT_ONLY'
    Require ((Git @('diff-tree','--no-commit-id','--name-status','-r',$PreviousPublication,$PublicationHead)) -ceq ("M`t" + $ScriptPath)) 'RECOVERY_NOT_SCRIPT_ONLY'
    $scriptBlob = Git @('rev-parse', ($PublicationHead + ':' + $ScriptPath))
    Require ((Git @('hash-object','--no-filters',$PSCommandPath)) -eq $scriptBlob) 'RUNNING_SCRIPT_MISMATCH'
    Assert-Writers
    # Git metadata lock only; never erase a stale lock or another writer's files.
    $lockFile = Git @('rev-parse','--git-path','fox2-samehost-preexec.lock')
    if (-not [IO.Path]::IsPathRooted($lockFile)) { $lockFile = Join-Path $Worktree $lockFile }
    $Lock = [IO.File]::Open($lockFile, [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None)
    $PythonExe = (Get-Command python -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
    $pythonCheck = Run-Tool $PythonExe @('-c','import sys,jsonschema; print(sys.version.split()[0])')
    Require ($pythonCheck.Code -eq 0) 'PYTHON_OR_JSONSCHEMA_UNAVAILABLE'
    Observe 'python_jsonschema' $true 'Python and jsonschema import succeeded.'
    $Caps.python_jsonschema.version = $pythonCheck.Text
    # Hash raw Git bytes in Python; never hash PowerShell-decoded/re-encoded blob text.
    $verify = @'
import hashlib,subprocess,sys
root,head,task,prompt,schema=sys.argv[1:]
for path,blob,digest in [(task,"8b69f093b8e625fd4404d07d3922658a9bc84a0d","71c4e1c0401c429878fabb95859f64c568c43dbe02f2ffab7b8c0de41b0837fa"),(prompt,"f9a60988fd5e13158cd898492910e92dfbbed253","2b67241b343989b2da6dd17c6927fc5ace6c75678f28efbfa4934e717875f5d9")]:
    actual=subprocess.check_output(["git","-C",root,"rev-parse",head+":"+path]).decode().strip()
    raw=subprocess.check_output(["git","-C",root,"cat-file","blob",actual])
    if actual!=blob or hashlib.sha256(raw).hexdigest()!=digest: raise SystemExit(21)
actual=subprocess.check_output(["git","-C",root,"rev-parse",head+":"+schema]).decode().strip()
if actual!="25fe465f82a16edf29ebf773a220969192f546e8": raise SystemExit(22)
'@
    $rawCheck = Run-Tool $PythonExe @('-c',$verify,$Worktree,$SourceHead,$TaskPath,$PromptPath,$SchemaPath)
    Require ($rawCheck.Code -eq 0) 'SOURCE_BLOB_HASH_MISMATCH'
    Observe 'task_prompt_raw_identity' $true 'Task/prompt Git SHA-1 and raw blob SHA-256 match immutable source lock.' 'SOURCE'
    if ($initialHead -ne $PublicationHead) { $null = Git @('-c','core.hooksPath=NUL','merge','--ff-only',$PublicationHead) }
    Require ((Git @('rev-parse','HEAD')) -eq $PublicationHead) 'PREEXEC_HEAD_MISMATCH'
    Observe 'exact_branch_head' $true ('Publication head=' + $PublicationHead + '; source lock=' + $SourceHead) 'SOURCE'
    Observe 'clean_worktree' ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'Worktree and index checked before receipt.' 'WORKTREE'
    Observe 'one_writer' $true 'One worktree owns branch; no task-scoped CODEX command line observed; exclusive PreExec lock held.' 'WORKTREE'
    Observe 'pwsh' $true ('PowerShell ' + $PSVersionTable.PSVersion.ToString())
    try {
        $CodexExe = (Get-Command codex -ErrorAction Stop | Select-Object -First 1).Source
        Require (-not [string]::IsNullOrWhiteSpace($CodexExe)) 'CODEX_NOT_A_FILE'
        $v = Codex-Info @('--version')
        $version = [regex]::Match(($v.Text + ' ' + $v.ErrorText), 'codex(?:-cli)?\s+(\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?)')
        Observe 'codex_version' ($v.Code -eq 0 -and $version.Success) 'CODEX version command completed and version marker checked.'
        if ($version.Success) { $Caps.codex_version.version = $version.Groups[1].Value }
        $login = Codex-Info @('login','status')
        Observe 'codex_login' ($login.Code -eq 0 -and ($login.Text + "`n" + $login.ErrorText) -match '(?im)^\s*Logged in(?:\s|$)') 'CODEX login status exit and authenticated marker checked; raw output discarded.' 'AUTH'
        $help = Codex-Info @('--help')
        $execHelp = Codex-Info @('exec','--help')
        $flags = $help.Code -eq 0 -and $execHelp.Code -eq 0
        foreach ($flag in @('--model','--config','--sandbox','--cd','--dangerously-bypass-approvals-and-sandbox')) {
            $flags = $flags -and (($help.Text + ' ' + $execHelp.Text).Contains($flag))
        }
        Observe 'codex_help_flags' $flags 'Help checked model/config/sandbox/cd/full-access flags; no agent execution.'
    } catch { Observe 'codex_metadata_probe' $false 'CODEX metadata probe unavailable or timed out; no raw output retained.' }
    # No live Agent probe permitted by Owner. No model/quota/runtime readiness claim.
    $Caps.agent_live_probe = @{ status='NOT_RUN'; material=$false; evidence='Owner scope permits metadata only; model availability, quota and execution readiness unverified.' }
    Assert-Writers
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_DRIFT_BEFORE_RECEIPT'
    Require ((Git @('rev-parse','HEAD')) -eq $PublicationHead) 'LOCAL_DRIFT_BEFORE_RECEIPT'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_BEFORE_RECEIPT'
    $receiptFull = Join-Path $Worktree $ReceiptPath
    Require (-not (Test-Path -LiteralPath $receiptFull)) 'RECEIPT_ALREADY_EXISTS_NO_REPLAY'
    $statusValue = if ($Blockers.Count -eq 0) { 'PASS' } else { 'BLOCKED' }
    $receipt = [ordered]@{
        schema_version='1.0'; receipt_type='FOX2_PREEXEC_RECEIPT'; project='FOX2'; wp_id='FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
        checked_at=[DateTime]::UtcNow.ToString('o'); task_branch=$Branch; source_head=$PublicationHead; receipt_path=$ReceiptPath
        task_source=@{ git_path=$TaskPath; git_commit_sha=$SourceHead; sha256='71c4e1c0401c429878fabb95859f64c568c43dbe02f2ffab7b8c0de41b0837fa' }
        status=$statusValue; capabilities=$Caps; blockers=@($Blockers.ToArray())
        worktree=@{ status='PASS'; path=$Worktree; competing_writer='NONE_OBSERVED'; stale_receipt_cleanup='NOT_NEEDED' }
        candidate_route=@{ product='CODEX'; model_policy='PINNED'; model='gpt-6.1-sol'; reasoning_effort='high'; permission_profile='FULL_ACCESS' }
        dispatch_state=@{ executable_dispatch_published=$false; dispatch_consumed=$false }; agent_execution_started=$false
        notes=@("Task=$TaskId; metadata-only PreExec; PASS means scoped checks only, not PASS_TO_ASSIGN.", "Original source lock=$SourceHead; publication lineage adds/patches only this PreExec script.", 'No Agent implementation, AppLocker/service/ACL mutation, install, deploy or replay performed.', 'Historical BLOCKED/FAIL/NOT_RUN retained. CHAT remote intake required; no model/quota/live execution proof.')
    }
    $json = (($receipt | ConvertTo-Json -Depth 12) -replace '\r\n', "`n").TrimEnd() + "`n"
    $null = New-Item -ItemType Directory -Force -Path (Split-Path -Parent $receiptFull)
    [IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))
    $validate = @'
import json,subprocess,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
root,head,path,receipt=sys.argv[1:]
schema=json.loads(subprocess.check_output(["git","-C",root,"show",head+":"+path]))
Draft202012Validator.check_schema(schema)
Draft202012Validator(schema,format_checker=FormatChecker()).validate(json.loads(Path(receipt).read_bytes()))
'@
    $validation = Run-Tool $PythonExe @('-c',$validate,$Worktree,$SourceHead,$SchemaPath,$receiptFull)
    Require ($validation.Code -eq 0) 'RECEIPT_SCHEMA_VALIDATION_FAILED'
    Assert-Writers
    Require ((Git @('rev-parse','HEAD')) -eq $PublicationHead) 'LOCAL_DRIFT_BEFORE_COMMIT'
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_DRIFT_BEFORE_COMMIT'
    Require ((Git @('status','--porcelain=v1','--untracked-files=all')) -ceq ('?? ' + $ReceiptPath)) 'UNRELATED_WIP_BEFORE_COMMIT'
    $null = Git @('add','--',$ReceiptPath)
    $null = Git @('diff','--cached','--check')
    Require ((Git @('diff','--cached','--name-only')) -ceq $ReceiptPath) 'STAGED_PATH_OUTSIDE_RECEIPT'
    $receiptBlob = Git @('rev-parse', (':' + $ReceiptPath))
    $null = Git @('-c','core.hooksPath=NUL','-c','commit.gpgsign=false','-c','user.name=FOX2 PreExec','-c','user.email=fox2-preexec@local.invalid','commit','-m','preexec(fox2): record samehost BUILD A01 metadata checks')
    $commit = Git @('rev-parse','HEAD')
    Require ((Git @('rev-list','--parents','-n','1',$commit)) -ceq ($commit + ' ' + $PublicationHead)) 'RECEIPT_PARENT_MISMATCH'
    Require ((Git @('diff-tree','--no-commit-id','--name-only','-r',$commit)) -ceq $ReceiptPath) 'COMMIT_NOT_RECEIPT_ONLY'
    Require ([string]::IsNullOrWhiteSpace((Git @('status','--porcelain=v1','--untracked-files=all')))) 'WIP_AFTER_COMMIT'
    Require ((Remote-Head) -eq $PublicationHead) 'REMOTE_DRIFT_BEFORE_PUSH'
    $null = Git @('-c','core.hooksPath=NUL','push','origin', ($commit + ':refs/heads/' + $Branch))
    Require ((Remote-Head) -eq $commit) 'REMOTE_RECEIPT_HEAD_MISMATCH'
    $null = Git @('fetch','--no-tags','origin', ('refs/heads/' + $Branch))
    Require ((Git @('rev-parse','FETCH_HEAD')) -eq $commit) 'REMOTE_FETCH_MISMATCH'
    Require ((Git @('rev-parse', ('FETCH_HEAD:' + $ReceiptPath))) -eq $receiptBlob) 'REMOTE_RECEIPT_BLOB_MISMATCH'
    $remoteValidation = Run-Tool $PythonExe @('-c',$validate,$Worktree,'FETCH_HEAD',$SchemaPath,$receiptFull)
    Require ($remoteValidation.Code -eq 0) 'REMOTE_SCHEMA_READBACK_FAILED'
    Write-Output ('FOX2_PREEXEC_STATUS=' + $statusValue)
    Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $commit)
    Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
    Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
    Write-Output 'FOX2_AGENT_EXECUTION_STARTED=FALSE; HOST_POLICY_MUTATION=FALSE; NEXT=CHAT_INTAKE'
    if ($statusValue -eq 'BLOCKED') { exit 20 }
} catch {
    # Preserve local evidence/commits after failure. Never force-push, retry or clean WIP.
    Write-Output 'FOX2_PREEXEC_STATUS=BLOCKED'
    Write-Output ('FOX2_PREEXEC_STOP=' + $_.Exception.Message.Split("`n")[0])
    Write-Output 'FOX2_PREEXEC_DELIVERY=NOT_VERIFIED; NEXT=RECONCILE_EXISTING_STATE_NO_REPLAY'
    exit 20
} finally { if ($null -ne $Lock) { $Lock.Dispose() } }
