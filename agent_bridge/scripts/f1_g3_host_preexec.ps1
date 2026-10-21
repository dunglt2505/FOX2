# FOX2 G3 isolated-host PreExec. Read-only host checks plus durable Git receipt.
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$Worktree,
    [Parameter(Mandatory=$true)][string]$ExpectedBranch,
    [Parameter(Mandatory=$true)][string]$ExpectedSourceHead,
    [Parameter(Mandatory=$true)][string]$TaskPath,
    [Parameter(Mandatory=$true)][string]$ExpectedTaskSha256,
    [Parameter(Mandatory=$true)][string]$ReceiptPath
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Sha256TextFile([string]$Path) {
    (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}
function Obs([string]$Status,[bool]$Material,[string]$Evidence,[int]$ExitCode=0,[string]$FailureClass=$null) {
    [ordered]@{status=$Status;material=$Material;exit_code=$ExitCode;failure_class=$FailureClass;evidence=$Evidence}
}
function Add-Blocker($List,[string]$Code,[string]$Class,[string]$Detail) {
    $List.Add([ordered]@{code=$Code;class=$Class;material=$true;sanitized_detail=$Detail})
}
function Invoke-Git([string[]]$Args,[bool]$AllowFail=$false) {
    $out=@(& git -C $Worktree @Args 2>&1)
    $code=$LASTEXITCODE
    if(-not $AllowFail -and $code -ne 0){throw "git failed ($code): $($Args -join ' ')"}
    [pscustomobject]@{Code=$code;Text=(($out|ForEach-Object{"$_"}) -join [Environment]::NewLine).Trim()}
}

if($PSVersionTable.PSVersion.Major -lt 7){throw 'PowerShell 7+ required.'}
if(-not(Test-Path -LiteralPath $Worktree -PathType Container)){throw "Missing worktree: $Worktree"}
if($null -eq (Get-Command git -ErrorAction SilentlyContinue)){throw 'git unavailable.'}

$cap=[ordered]@{}
$blockers=[System.Collections.Generic.List[object]]::new()
$branch=(Invoke-Git @('branch','--show-current')).Text
$head=(Invoke-Git @('rev-parse','HEAD')).Text
$status=(Invoke-Git @('status','--porcelain=v1','--untracked-files=all')).Text

if($branch -eq $ExpectedBranch){$cap.git_branch=Obs 'PASS' $true 'Exact G3 task branch observed.'}
else{Add-Blocker $blockers 'G3_BRANCH_MISMATCH' 'SOURCE' 'Current branch differs from bound G3 branch.';$cap.git_branch=Obs 'FAIL' $true 'G3 branch mismatch.' 1 'G3_BRANCH_MISMATCH'}

if($head -eq $ExpectedSourceHead){$cap.source_head=Obs 'PASS' $true 'Exact G3 source head observed.'}
else{Add-Blocker $blockers 'G3_SOURCE_HEAD_MISMATCH' 'SOURCE' 'Local HEAD differs from bound G3 source.';$cap.source_head=Obs 'FAIL' $true 'G3 source head mismatch.' 1 'G3_SOURCE_HEAD_MISMATCH'}

if([string]::IsNullOrWhiteSpace($status)){$cap.clean_worktree=Obs 'PASS' $true 'No local WIP observed before PreExec.'}
else{Add-Blocker $blockers 'G3_WORKTREE_DIRTY' 'WORKTREE' 'Unrelated WIP exists before host PreExec.';$cap.clean_worktree=Obs 'FAIL' $true 'Worktree is not clean.' 1 'G3_WORKTREE_DIRTY'}

$taskFull=Join-Path $Worktree ($TaskPath -replace '/', [IO.Path]::DirectorySeparatorChar)
if(-not(Test-Path -LiteralPath $taskFull -PathType Leaf)){Add-Blocker $blockers 'G3_TASK_MISSING' 'SOURCE' 'Bound G3 task file is missing.';$cap.task_identity=Obs 'MISSING' $true 'Bound task file missing.' 1 'G3_TASK_MISSING'}
else{$taskHash=Sha256TextFile $taskFull;if($taskHash -eq $ExpectedTaskSha256){$cap.task_identity=Obs 'PASS' $true 'Task SHA-256 matches bound task.'}else{Add-Blocker $blockers 'G3_TASK_HASH_MISMATCH' 'SOURCE' 'Task SHA-256 does not match.';$cap.task_identity=Obs 'FAIL' $true 'Task SHA-256 mismatch.' 1 'G3_TASK_HASH_MISMATCH'}}

$remote=Invoke-Git @('ls-remote','--refs','origin',('refs/heads/'+$ExpectedBranch)) $true
if($remote.Code -ne 0 -or [string]::IsNullOrWhiteSpace($remote.Text)){Add-Blocker $blockers 'G3_REMOTE_UNREADABLE' 'GIT' 'Cannot read exact remote G3 branch.';$cap.remote_source=Obs 'FAIL' $true 'Remote G3 branch unreadable.' $remote.Code 'G3_REMOTE_UNREADABLE'}
else{$remoteHead=($remote.Text -split '\s+')[0];if($remoteHead -eq $ExpectedSourceHead){$cap.remote_source=Obs 'PASS' $true 'Remote G3 branch equals bound source head.'}else{Add-Blocker $blockers 'G3_REMOTE_DRIFT' 'GIT' 'Remote G3 branch differs from bound source.';$cap.remote_source=Obs 'FAIL' $true 'Remote branch drift.' 1 'G3_REMOTE_DRIFT'}}

$wtList=[regex]::Split((Invoke-Git @('worktree','list','--porcelain')).Text,'\r?\n')
$branchMarker='branch refs/heads/'+$ExpectedBranch
$owners=@($wtList|Where-Object{$_ -eq $branchMarker})
if($owners.Count -eq 1){$cap.one_writer=Obs 'PASS' $true 'Exactly one Git worktree owns the G3 branch.'}
else{Add-Blocker $blockers 'G3_COMPETING_WORKTREE' 'SERIALIZATION' 'G3 branch has zero or multiple worktree owners.';$cap.one_writer=Obs 'FAIL' $true 'Unexpected G3 worktree ownership.' 1 'G3_COMPETING_WORKTREE'}

$principal=[Security.Principal.WindowsPrincipal]::new([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin=$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if($isAdmin){$cap.elevated_admin=Obs 'PASS' $true 'Elevated Administrator token observed.'}
else{Add-Blocker $blockers 'G3_ADMIN_REQUIRED' 'PERMISSION' 'Elevated Administrator token required on isolated G3 target.';$cap.elevated_admin=Obs 'FAIL' $true 'Current token is not elevated Administrator.' 1 'G3_ADMIN_REQUIRED'}

$cap.pwsh=Obs 'PASS' $true ('PowerShell '+$PSVersionTable.PSVersion.ToString())
$gitVersion=(Invoke-Git @('--version')).Text
$cap.git_tool=Obs 'PASS' $true $gitVersion

$os=Get-CimInstance Win32_OperatingSystem
$cs=Get-CimInstance Win32_ComputerSystem
$caption=[string]$os.Caption
$buildNumber=[int]$os.BuildNumber
$osOk=($buildNumber -ge 22000) -and ($caption -match 'Pro|Enterprise|Education')
if($osOk){$cap.windows_applocker_edition=Obs 'PASS' $true ('Supported Windows edition/build observed: '+$caption+' / '+$os.BuildNumber)}
else{Add-Blocker $blockers 'G3_WINDOWS_EDITION_UNSUPPORTED' 'CAPABILITY' 'Windows 11-class build with Pro/Enterprise/Education edition required.';$cap.windows_applocker_edition=Obs 'FAIL' $true 'Unsupported Windows edition for this G3 contract.' 1 'G3_WINDOWS_EDITION_UNSUPPORTED'}

$vmText=[string]($cs.Manufacturer+' '+$cs.Model)
$isVirtual=$vmText -match '(?i)(virtual|vmware|virtualbox|kvm|qemu|parallels|hyper-v)'
if($isVirtual -and -not $cs.PartOfDomain){$cap.isolated_virtual_target=Obs 'PASS' $true ('Virtual non-domain target observed: '+$cs.Manufacturer+' / '+$cs.Model)}
else{Add-Blocker $blockers 'G3_ISOLATED_TARGET_UNPROVEN' 'PERMISSION' 'G3 requires a virtual isolated non-domain test target.';$cap.isolated_virtual_target=Obs 'FAIL' $true 'Isolated virtual target not proven.' 1 'G3_ISOLATED_TARGET_UNPROVEN'}

$appLocker=Get-Module -ListAvailable AppLocker|Select-Object -First 1
if($null -ne $appLocker){$cap.applocker_module=Obs 'PASS' $true ('AppLocker module available: '+$appLocker.Version)}
else{Add-Blocker $blockers 'G3_APPLOCKER_MODULE_MISSING' 'CAPABILITY' 'AppLocker module unavailable.';$cap.applocker_module=Obs 'MISSING' $true 'AppLocker module unavailable.' 1 'G3_APPLOCKER_MODULE_MISSING'}

$effectiveXml=$null;$localXml=$null
try{Import-Module AppLocker -ErrorAction Stop;$effectiveXml=Get-AppLockerPolicy -Effective -Xml -ErrorAction Stop;$localXml=Get-AppLockerPolicy -Local -Xml -ErrorAction Stop;$cap.applocker_policy_query=Obs 'PASS' $true 'Effective and local AppLocker policy are readable.'}
catch{Add-Blocker $blockers 'G3_APPLOCKER_QUERY_FAILED' 'CAPABILITY' 'Cannot read effective/local AppLocker policy.';$cap.applocker_policy_query=Obs 'FAIL' $true 'AppLocker policy query failed.' 1 'G3_APPLOCKER_QUERY_FAILED'}

$appId=Get-Service -Name AppIDSvc -ErrorAction SilentlyContinue
if($null -ne $appId){$cap.appidsvc_present=Obs 'PASS' $true ('AppIDSvc observed; current state='+$appId.Status)}
else{Add-Blocker $blockers 'G3_APPIDSVC_MISSING' 'CAPABILITY' 'Application Identity service is missing.';$cap.appidsvc_present=Obs 'MISSING' $true 'AppIDSvc missing.' 1 'G3_APPIDSVC_MISSING'}

$existingService=Get-Service -Name FOX2F1Authority -ErrorAction SilentlyContinue
if($null -eq $existingService){$cap.f1_service_collision=Obs 'PASS' $true 'No existing FOX2F1Authority service observed.'}
else{Add-Blocker $blockers 'G3_EXISTING_F1_SERVICE' 'OTHER' 'Existing FOX2F1Authority service requires separate reconciliation.';$cap.f1_service_collision=Obs 'FAIL' $true 'Existing F1 service collision.' 1 'G3_EXISTING_F1_SERVICE'}

$programData=[Environment]::GetFolderPath('CommonApplicationData')
$authorityRoot=Join-Path $programData 'FOX2\F1Authority'
if(-not(Test-Path -LiteralPath $authorityRoot)){$cap.authority_root_collision=Obs 'PASS' $true 'No pre-existing F1 authority root observed.'}
else{Add-Blocker $blockers 'G3_EXISTING_AUTHORITY_ROOT' 'OTHER' 'Existing protected authority root requires separate reconciliation.';$cap.authority_root_collision=Obs 'FAIL' $true 'Existing F1 authority root collision.' 1 'G3_EXISTING_AUTHORITY_ROOT'}

if($null -ne $effectiveXml -and $null -ne $localXml){
    $effectiveHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$effectiveXml))).ToLowerInvariant()
    $localHash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes([string]$localXml))).ToLowerInvariant()
    $cap.rollback_policy_snapshot=Obs 'PASS' $true ('Pre-change AppLocker query hashes captured: effective='+$effectiveHash+'; local='+$localHash)
}else{Add-Blocker $blockers 'G3_POLICY_ROLLBACK_SNAPSHOT_UNAVAILABLE' 'CAPABILITY' 'Pre-change policy snapshot cannot be established.';$cap.rollback_policy_snapshot=Obs 'FAIL' $true 'Policy rollback snapshot unavailable.' 1 'G3_POLICY_ROLLBACK_SNAPSHOT_UNAVAILABLE'}

$statusValue=if($blockers.Count -eq 0){'PASS'}else{'BLOCKED'}
$receiptFull=Join-Path $Worktree ($ReceiptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $receiptFull)|Out-Null
$receipt=[ordered]@{
    schema_version='1.0';receipt_type='FOX2_PREEXEC_RECEIPT';project='FOX2';wp_id='FOX2-BRIDGE-RC1-TO-INTERNAL-READY';
    checked_at=(Get-Date).ToUniversalTime().ToString('o');task_branch=$ExpectedBranch;receipt_path=$ReceiptPath;source_head=$ExpectedSourceHead;
    task_source=[ordered]@{git_path=$TaskPath;git_commit_sha=$ExpectedSourceHead;sha256=$ExpectedTaskSha256};
    status=$statusValue;capabilities=$cap;blockers=@($blockers);
    worktree=[ordered]@{status=if([string]::IsNullOrWhiteSpace($status)){'PASS'}else{'BLOCKED'};path=$Worktree;competing_writer=if($owners.Count -eq 1){'NONE_OBSERVED'}else{'PRESENT'};stale_receipt_cleanup='NOT_NEEDED'};
    dispatch_state=[ordered]@{executable_dispatch_published=$false;dispatch_consumed=$false};agent_execution_started=$false;
    notes=@('OWNER_MANUAL_HOST G3 preflight; no Agent route selected.','No AppLocker/service/AppIDSvc/ACL mutation performed by this PreExec.','PASS authorizes CHAT intake only; host mutation waits for PASS_TO_EXECUTE.')
}
$json=$receipt|ConvertTo-Json -Depth 12
$json=($json -replace '\r\n',[string][char]10).TrimEnd()+[char]10
[IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))

$python=Get-Command python -ErrorAction SilentlyContinue
if($null -eq $python){throw 'Python required for receipt schema validation.'}
$schemaPath=Join-Path $Worktree 'docs\agent_handoff\FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json'
$validation=@'
import json,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
schema=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
value=json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
Draft202012Validator(schema,format_checker=FormatChecker()).validate(value)
'@
$tmp=Join-Path ([IO.Path]::GetTempPath()) ('fox2_g3_preexec_validate_'+[guid]::NewGuid().ToString('N')+'.py')
try{[IO.File]::WriteAllText($tmp,$validation,[Text.UTF8Encoding]::new($false));& $python.Source $tmp $schemaPath $receiptFull;if($LASTEXITCODE -ne 0){throw 'PreExec receipt schema validation failed.'}}
finally{Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue}

& git -C $Worktree add -- $ReceiptPath
if($LASTEXITCODE -ne 0){throw 'Failed to stage G3 receipt.'}
& git -C $Worktree -c 'core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol' diff --cached --check
if($LASTEXITCODE -ne 0){throw 'G3 receipt diff check failed.'}
$staged=(Invoke-Git @('diff','--cached','--name-only')).Text
if($staged.Trim() -ne $ReceiptPath){throw "STOP: staged path outside receipt: $staged"}

& git -C $Worktree -c 'user.name=FOX2 G3 Host PreExec' -c 'user.email=fox2-g3-preexec@local.invalid' commit -m 'preexec(fox2): record G3 isolated-host readiness'
if($LASTEXITCODE -ne 0){throw 'G3 receipt commit failed.'}
$receiptCommit=(Invoke-Git @('rev-parse','HEAD')).Text
$receiptBase64=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($json))
$pushSpec=$receiptCommit+':refs/heads/'+$ExpectedBranch
& git -C $Worktree push origin $pushSpec
$pushExit=$LASTEXITCODE
$remoteAfter=Invoke-Git @('ls-remote','--refs','origin',('refs/heads/'+$ExpectedBranch)) $true
$remoteSha=if($remoteAfter.Code -eq 0 -and -not[string]::IsNullOrWhiteSpace($remoteAfter.Text)){($remoteAfter.Text -split '\s+')[0]}else{$null}

Write-Output ('FOX2_G3_PREEXEC_STATUS='+$statusValue)
Write-Output ('FOX2_G3_PREEXEC_LOCAL_RECEIPT_SHA='+$receiptCommit)
Write-Output ('FOX2_G3_PREEXEC_PUSH_EXIT='+$pushExit)
Write-Output ('FOX2_G3_PREEXEC_REMOTE_SHA='+$remoteSha)
Write-Output ('FOX2_G3_PREEXEC_RECEIPT_BASE64='+$receiptBase64)
Write-Output 'FOX2_G3_HOST_MUTATION_STARTED=FALSE'
if($remoteSha -eq $receiptCommit){Write-Output 'FOX2_G3_PREEXEC_DELIVERY=REMOTE_READBACK_PASS';Write-Output 'FOX2_G3_NEXT=RETURN_OUTPUT_TO_CHAT_FOR_INTAKE'}
else{Write-Output 'FOX2_G3_PREEXEC_DELIVERY=REMOTE_READBACK_UNKNOWN';Write-Output 'FOX2_G3_NEXT=CHAT_REMOTE_READBACK_REQUIRED'}
if($statusValue -eq 'PASS'){exit 0}else{exit 20}
