#requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$PublicationHead,
    [Parameter(Mandatory)][string]$ExpectedScriptBlob,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-20261022'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Branch = 'work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-20261022'
$GovernanceBranch = 'work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019'
$SourceBase = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
$TaskId = 'FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02'

$TaskCommit = 'd0b070e42d25a1581fee8a8731f393206ec5ef5b'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a02/task.md'
$TaskBlob = 'fb6ecc9ebf097c58809123f04d61b5802e920e77'
$TaskSha256 = 'cd3a08ebcbdd4d02e3b3a98a59de6eb6631cccbf9e94ae0d203ff9dc496c82ce'

$PromptCommit = '40bf70cbf0a46be0cfafbf9965704e68eb48fa5e'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a02/prompt.md'
$PromptBlob = '50a96f461bfe48dfa5514ac0d537e48c7a2d6540'
$PromptSha256 = 'c99584faa1b165b5e766579188afefa86532a8833fe9c966e1a8979c6352f8c5'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a02/host_lifecycle_cert_a02_preexec.ps1'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a02.json'

$PolicyPath = 'docs/governance/FOX2_POLICY_V2.0.0.md'
$PolicyBlob = '2d373f374f906bf7959062050bbeae5350b0c482'
$DictionaryPath = 'docs/governance/FOX2_PROJECT_DICTIONARY_v1.3.json'
$DictionaryBlob = '6c8f30e2e6b07f2e65e45c14faab99672d036083'
$RoutingPath = 'docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_4_0_OWNER_OVERRIDE_ROUTING_INDEX_20261019.md'
$RoutingBlob = '14d2e95e419cc67c3e0cf851cc806a96cf885b7e'
$ProtocolPath = 'docs/agent_handoff/FOX2_GIT_FIRST_TASK_RESULT_PROTOCOL_v12.md'
$ProtocolBlob = 'd34a022f2bda39a167a404c8530e57b30f337cb9'

$Model = 'gpt-6.1-sol'
$Reasoning = 'high'
$Marker = 'FOX2_HOST_LIFECYCLE_CERT_A02_PREEXEC_OK'

function Require([bool]$Condition,[string]$Message) {
    if (-not $Condition) { throw $Message }
}

function Safe([string]$Value) {
    if ($null -eq $Value) { return '' }
    $v = $Value -replace '(?i)(authorization|bearer|token|password|secret)\s*[:=]\s*\S+', '$1=<redacted>'
    $v = $v.Trim()
    if ($v.Length -gt 400) { $v = $v.Substring(0,400) }
    return $v
}

function Run {
    param(
        [Parameter(Mandatory)][string]$File,
        [string[]]$Args = @(),
        [int]$Timeout = 60,
        [string]$Cwd = $Worktree,
        [AllowNull()][string]$InputText = $null
    )

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $File
    $psi.WorkingDirectory = $Cwd
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.RedirectStandardInput = $null -ne $InputText
    $psi.CreateNoWindow = $true
    foreach ($a in $Args) { $null = $psi.ArgumentList.Add($a) }

    $p = [Diagnostics.Process]::new()
    $p.StartInfo = $psi
    try {
        Require ($p.Start()) ('TOOL_START_FAILED:' + $File)
        $ot = $p.StandardOutput.ReadToEndAsync()
        $et = $p.StandardError.ReadToEndAsync()
        if ($null -ne $InputText) {
            $p.StandardInput.Write($InputText)
            $p.StandardInput.Close()
        }
        if (-not $p.WaitForExit($Timeout * 1000)) {
            try { $p.Kill($true) } catch {}
            try { $p.WaitForExit() } catch {}
            throw ('TOOL_TIMEOUT:' + $File)
        }
        [pscustomobject]@{
            Code = [int]$p.ExitCode
            Out = [string]$ot.GetAwaiter().GetResult()
            Err = [string]$et.GetAwaiter().GetResult()
        }
    }
    finally {
        $p.Dispose()
    }
}

$Git = (Get-Command git.exe -ErrorAction Stop).Source
$Python = (Get-Command python.exe -ErrorAction Stop).Source
$Pwsh = (Get-Command pwsh.exe -ErrorAction Stop).Source
$Codex = (Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
$Dotnet = (Get-Command dotnet -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source

function G([string[]]$Args) {
    $r = Run -File $Git -Args (@('-C',$Worktree) + $Args)
    Require ($r.Code -eq 0) ('GIT_FAILED:' + ($Args -join ' ') + ':' + (Safe ($r.Err + ' ' + $r.Out)))
    ([string]$r.Out).Trim()
}

function RemoteHead([string]$Name = $Branch) {
    $r = Run -File $Git -Args @('-C',$Worktree,'ls-remote','--refs','origin',('refs/heads/' + $Name))
    Require ($r.Code -eq 0) ('REMOTE_READ_FAILED:' + $Name)
    $v = ([string]$r.Out).Trim()
    Require (-not [string]::IsNullOrWhiteSpace($v)) ('REMOTE_BRANCH_MISSING:' + $Name)
    (($v -split '\s+')[0]).Trim()
}

function GitSha256([string]$Spec) {
    $code = 'import hashlib,subprocess,sys; d=subprocess.check_output(["git","-C",sys.argv[1],"show",sys.argv[2]]); print(hashlib.sha256(d).hexdigest())'
    $r = Run -File $Python -Args @('-c',$code,$Worktree,$Spec)
    Require ($r.Code -eq 0) ('SHA256_FAILED:' + $Spec)
    ([string]$r.Out).Trim()
}

function NoTaskWriter {
    $all = @(Get-CimInstance Win32_Process -ErrorAction Stop)
    foreach ($p in $all) {
        $name = [string]$p.Name
        $line = [string]$p.CommandLine
        $isCodex = $name -match '(?i)^codex(?:[.-].*)?(?:\.exe)?$'
        $isWrapper = $name -match '(?i)^(node|cmd|pwsh|powershell)\.exe$' -and
            -not [string]::IsNullOrWhiteSpace($line) -and
            $line -match '(?i)codex(?:\.js|\.cmd|\.ps1|\.exe|\s)'
        if (-not ($isCodex -or $isWrapper)) { continue }
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        foreach ($m in @($Worktree,$Branch,$TaskId,$TaskPath,$PromptPath,$ScriptPath)) {
            Require ($line.IndexOf($m,[StringComparison]::OrdinalIgnoreCase) -lt 0) 'TASK_SCOPED_WRITER_PRESENT'
        }
    }
}

Write-Output '=== FOX2 HOST LIFECYCLE CERT A02 PREEXEC ==='
Write-Output ('FOX2_TASK_ID=' + $TaskId)
Write-Output ('FOX2_SOURCE=' + $SourceBase)
Write-Output ('FOX2_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output 'FOX2_HOST_MUTATION=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'

Require ($PSVersionTable.PSVersion.Major -ge 7) 'POWERSHELL_7_REQUIRED'
Require (Test-Path -LiteralPath $Worktree -PathType Container) 'WORKTREE_MISSING'
Require ((G @('branch','--show-current')) -ceq $Branch) 'WRONG_BRANCH'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'LOCAL_HEAD_MISMATCH'
Require ((RemoteHead) -ceq $PublicationHead) 'REMOTE_HEAD_MISMATCH'
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY'

$scriptFull = Join-Path $Worktree ($ScriptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require ((G @('hash-object','--no-filters',$scriptFull)) -ceq $ExpectedScriptBlob) 'PREEXEC_SCRIPT_BLOB_MISMATCH'

Require ((G @('rev-parse',($TaskCommit + ':' + $TaskPath))) -ceq $TaskBlob) 'TASK_BLOB_MISMATCH'
Require ((G @('rev-parse',($PromptCommit + ':' + $PromptPath))) -ceq $PromptBlob) 'PROMPT_BLOB_MISMATCH'
Require ((GitSha256 ($TaskCommit + ':' + $TaskPath)) -ceq $TaskSha256) 'TASK_SHA256_MISMATCH'
Require ((GitSha256 ($PromptCommit + ':' + $PromptPath)) -ceq $PromptSha256) 'PROMPT_SHA256_MISMATCH'

$anc = Run -File $Git -Args @('-C',$Worktree,'merge-base','--is-ancestor',$SourceBase,$PublicationHead)
Require ($anc.Code -eq 0) 'SOURCE_NOT_ANCESTOR'
Require ([string]::IsNullOrWhiteSpace((G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--','agent_bridge')))) 'PRODUCT_DRIFT'

$expectedSetup = @($TaskPath,$PromptPath,$ScriptPath) | Sort-Object
$setupText = G @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--')
$observedSetup = @($setupText -split '\r?\n' | Where-Object { $_ } | Sort-Object)
Require (($observedSetup -join [char]10) -ceq ($expectedSetup -join [char]10)) 'SETUP_PATH_DRIFT'

$govFetch = Run -File $Git -Args @('-C',$Worktree,'fetch','--no-tags','origin',('+refs/heads/' + $GovernanceBranch + ':refs/remotes/origin/' + $GovernanceBranch)) -Timeout 90
Require ($govFetch.Code -eq 0) 'GOVERNANCE_FETCH_FAILED'
foreach ($x in @(
    @($PolicyPath,$PolicyBlob),
    @($DictionaryPath,$DictionaryBlob),
    @($RoutingPath,$RoutingBlob),
    @($ProtocolPath,$ProtocolBlob)
)) {
    Require ((G @('rev-parse',('refs/remotes/origin/' + $GovernanceBranch + ':' + $x[0]))) -ceq $x[1]) ('GOVERNANCE_DRIFT:' + $x[0])
}

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require (-not (Test-Path -LiteralPath $receiptFull)) 'RECEIPT_ALREADY_EXISTS'
$receiptProbe = Run -File $Git -Args @('-C',$Worktree,'cat-file','-e',($PublicationHead + ':' + $ReceiptPath))
Require ($receiptProbe.Code -ne 0) 'RECEIPT_ALREADY_COMMITTED'

NoTaskWriter

# Read-only installed state.
$BridgeRoot = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$CurrentPath = Join-Path $BridgeRoot 'current.json'
$VersionsPath = Join-Path $BridgeRoot 'versions'
$installed = Test-Path -LiteralPath $CurrentPath -PathType Leaf
$currentSha = $null
$currentSource = $null
$controlState = 'NOT_INSTALLED'
$paused = $null
$setupComplete = $null

if ($installed) {
    $cur = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
    $currentSha = [string]$cur.package_sha256
    $currentSource = [string]$cur.source_sha256
    Require ($currentSha -match '^[0-9a-f]{64}$') 'CURRENT_POINTER_INVALID'
    $installedPython = Join-Path $VersionsPath ($currentSha + '\runtime\Scripts\python.exe')
    Require (Test-Path -LiteralPath $installedPython -PathType Leaf) 'CURRENT_RUNTIME_MISSING'
    $sr = Run -File $installedPython -Args @('-I','-m','fox2_agent_bridge','control','status') -Timeout 30
    Require ($sr.Code -eq 0) 'CONTROL_STATUS_FAILED'
    $state = ([string]$sr.Out).Trim() | ConvertFrom-Json
    $controlState = [string]$state.state
    $paused = [bool]$state.paused
    $setupComplete = [bool]$state.setup_complete
    Require ($paused) 'HOST_NOT_PAUSED'
    Require ($setupComplete) 'HOST_SETUP_INCOMPLETE'
    Require ($state.PSObject.Properties.Name -contains 'current_dispatch') 'CURRENT_DISPATCH_FIELD_MISSING'
    Require ($null -eq $state.current_dispatch) 'CURRENT_DISPATCH_ACTIVE'
}

$allProcesses = @(Get-CimInstance Win32_Process -ErrorAction Stop)
$workerLegacy = @($allProcesses | Where-Object {
    $line = [string]$_.CommandLine
    -not [string]::IsNullOrWhiteSpace($line) -and
    ($line -match '(?i)fox2_agent_bridge\s+worker' -or $line -match '(?i)desktop_(tray|launcher)\.ps1')
})
Require ($workerLegacy.Count -eq 0) 'WORKER_OR_LEGACY_TRAY_ACTIVE'

$wpf = @($allProcesses | Where-Object { [string]$_.Name -ieq 'FOX2.Bridge.Desktop.exe' })
Require ($wpf.Count -le 1) 'MULTIPLE_WPF_PRESENTATIONS'

$wpfExact = $false
$wpfPid = $null
$uiInspect = 'NOT_RUN'

if ($wpf.Count -eq 1) {
    Require ($installed) 'WPF_PRESENT_WITHOUT_CURRENT_INSTALL'
    $wpfPid = [int]$wpf[0].ProcessId
    $wpfPath = [string]$wpf[0].ExecutablePath
    Require (-not [string]::IsNullOrWhiteSpace($wpfPath)) 'WPF_PATH_UNKNOWN'
    $expectedWpf = Join-Path $VersionsPath ($currentSha + '\payload\desktop\FOX2.Bridge.Desktop.exe')
    Require ([IO.Path]::GetFullPath($wpfPath).Equals([IO.Path]::GetFullPath($expectedWpf),[StringComparison]::OrdinalIgnoreCase)) 'WPF_NOT_CURRENT_PACKAGE'
    $ui = Join-Path $Worktree 'agent_bridge\scripts\certify_rc1_ui.ps1'
    $ir = Run -File $Pwsh -Args @('-NoProfile','-NonInteractive','-File',$ui,'-Action','inspect') -Timeout 30
    Require ($ir.Code -eq 0) ('WPF_INSPECT_FAILED:' + (Safe ($ir.Err + ' ' + $ir.Out)))
    $u = ([string]$ir.Out).Trim() | ConvertFrom-Json
    Require ([int]$u.process_id -eq $wpfPid) 'WPF_UI_PID_MISMATCH'
    $wpfExact = $true
    $uiInspect = 'PASS'
}

$configHash = $null
$dbHash = $null
$consumptionHash = $null
$uninstallHash = $null
foreach ($pair in @(
    @('config', (Join-Path $BridgeRoot 'config\bridge.toml')),
    @('db', (Join-Path $BridgeRoot 'data\bridge.db')),
    @('consumption', (Join-Path $BridgeRoot 'data\manual_consumption.json')),
    @('uninstall', (Join-Path $BridgeRoot 'uninstall.ps1'))
)) {
    if (Test-Path -LiteralPath $pair[1] -PathType Leaf) {
        $h = (Get-FileHash -LiteralPath $pair[1] -Algorithm SHA256).Hash.ToLowerInvariant()
        switch ($pair[0]) {
            'config' { $configHash = $h }
            'db' { $dbHash = $h }
            'consumption' { $consumptionHash = $h }
            'uninstall' { $uninstallHash = $h }
        }
    }
}

# Existing build environment previously verified by host lifecycle A01.
$BuildPython = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B\agent_bridge\.build-venv\Scripts\python.exe'
$BuildAlias = 'WORKTREES/FOX2-BRIDGE-DESKTOP-BATCH-B/agent_bridge/.build-venv/Scripts/python.exe'
Require (Test-Path -LiteralPath $BuildPython -PathType Leaf) 'BUILD_PYTHON_MISSING'
$probeCode = 'import importlib.metadata as m,json,sys; print(json.dumps({"isolated":sys.prefix!=sys.base_prefix,"python":f"{sys.version_info.major}.{sys.version_info.minor}","pip":m.version("pip"),"setuptools":m.version("setuptools"),"wheel":m.version("wheel"),"build":m.version("build"),"jsonschema":m.version("jsonschema")},sort_keys=True))'
$br = Run -File $BuildPython -Args @('-I','-c',$probeCode) -Timeout 30
Require ($br.Code -eq 0) 'BUILD_ENV_PROBE_FAILED'
$be = ([string]$br.Out).Trim() | ConvertFrom-Json
Require ($be.isolated -eq $true) 'BUILD_PYTHON_NOT_ISOLATED'
Require ([string]$be.python -ceq '3.13') 'BUILD_PYTHON_VERSION_DRIFT'
Require ([string]$be.pip -ceq '26.2.1') 'BUILD_PIP_DRIFT'
Require ([string]$be.setuptools -ceq '84.0.0') 'BUILD_SETUPTOOLS_DRIFT'
Require ([string]$be.wheel -ceq '0.48.0') 'BUILD_WHEEL_DRIFT'
Require ([string]$be.build -ceq '1.6.1') 'BUILD_MODULE_DRIFT'
Require ([string]$be.jsonschema -ceq '4.26.0') 'BUILD_JSONSCHEMA_DRIFT'

$dn = Run -File $Dotnet -Args @('--version') -Timeout 30
Require ($dn.Code -eq 0) 'DOTNET_FAILED'
$dotnetVersion = ([string]$dn.Out).Trim()
Require ($dotnetVersion -ceq '8.0.426') 'DOTNET_VERSION_DRIFT'

$cv = Run -File $Codex -Args @('--version') -Timeout 30
Require ($cv.Code -eq 0) 'CODEX_VERSION_FAILED'
$codexVersion = ([string]$cv.Out).Trim()
Require ($codexVersion -ceq 'codex-cli 0.162.1') 'CODEX_VERSION_DRIFT'

$login = Run -File $Codex -Args @('login','status') -Timeout 60
Require ($login.Code -eq 0) 'CODEX_LOGIN_NOT_READY'

$help = Run -File $Codex -Args @('exec','--help') -Timeout 60
Require ($help.Code -eq 0) 'CODEX_HELP_FAILED'
$helpText = [string]$help.Out + [string]$help.Err
foreach ($flag in @('--model','--sandbox','--config','--skip-git-repo-check','--cd','--output-last-message')) {
    Require ($helpText.Contains($flag)) ('CODEX_FLAG_MISSING:' + $flag)
}

$temp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-host-a02-preexec-' + [Guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($temp) | Out-Null
$last = Join-Path $temp 'last.txt'
try {
    $probePrompt = 'FOX2 route-admission probe only. Do not inspect files, use tools, execute commands, or modify anything. Reply exactly ' + $Marker
    $cr = Run -File $Codex -Args @(
        'exec','--model',$Model,'--sandbox','read-only',
        '--config','approval_policy="never"',
        '--config',('model_reasoning_effort="' + $Reasoning + '"'),
        '--skip-git-repo-check','--cd',$temp,'--output-last-message',$last,'-'
    ) -Timeout 240 -Cwd $temp -InputText ($probePrompt + [Environment]::NewLine)
    Require ($cr.Code -eq 0) ('CODEX_CAPACITY_FAILED:' + (Safe ($cr.Err + ' ' + $cr.Out)))
    $markerValue = if (Test-Path -LiteralPath $last) { [IO.File]::ReadAllText($last).Trim() } else { '' }
    Require ($markerValue -ceq $Marker) ('CODEX_MARKER_MISMATCH:' + (Safe $markerValue))
}
finally {
    try { if ([IO.Directory]::Exists($temp)) { [IO.Directory]::Delete($temp,$true) } } catch {}
}

NoTaskWriter
Require ([string]::IsNullOrWhiteSpace((G @('status','--porcelain=v1','--untracked-files=all')))) 'WORKTREE_DIRTY_AFTER_PROBE'
Require ((G @('rev-parse','HEAD')) -ceq $PublicationHead) 'HEAD_DRIFT'
Require ((RemoteHead) -ceq $PublicationHead) 'REMOTE_DRIFT'

$dry = Run -File $Git -Args @('-C',$Worktree,'push','--dry-run','origin',($PublicationHead + ':refs/heads/' + $Branch)) -Timeout 60
Require ($dry.Code -eq 0) 'GIT_PUSH_DRY_RUN_FAILED'

$cap = [ordered]@{
    source_binding = [ordered]@{ status='PASS'; material=$true; evidence=('accepted=' + $SourceBase + '; publication=' + $PublicationHead) }
    task_prompt_binding = [ordered]@{ status='PASS'; material=$true; evidence=('task=' + $TaskSha256 + '; prompt=' + $PromptSha256) }
    governance_source = [ordered]@{ status='PASS'; material=$true; evidence='Current Policy/Dictionary/Routing/Protocol bytes verified' }
    worktree_clean = [ordered]@{ status='PASS'; material=$true; evidence='Dedicated host lifecycle A02 worktree clean' }
    one_writer = [ordered]@{ status='PASS'; material=$true; evidence='No task-scoped writer observed' }
    host_safe_control = [ordered]@{ status='PASS'; material=$true; evidence=('installed=' + $installed + '; state=' + $controlState + '; paused=' + $paused + '; setup=' + $setupComplete) }
    host_wpf_state = [ordered]@{ status='PASS'; material=$true; evidence=('count=' + $wpf.Count + '; exact=' + $wpfExact + '; inspect=' + $uiInspect) }
    worker_legacy_absent = [ordered]@{ status='PASS'; material=$true; evidence='Worker/legacy tray-launcher count=0' }
    isolated_build_python = [ordered]@{ status='PASS'; material=$true; version=([string]$be.python); executable=$BuildAlias; evidence='Existing isolated build environment verified' }
    dotnet = [ordered]@{ status='PASS'; material=$true; version=$dotnetVersion; executable=$Dotnet; evidence='Existing dotnet verified' }
    codex_cli = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; evidence='Pinned CODEX CLI verified' }
    codex_auth_capacity = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; exit_code=0; evidence='Current authenticated read-only service probe PASS' }
    eligible_agent_route = [ordered]@{ status='PASS'; material=$true; version=$codexVersion; executable=$Codex; exit_code=0; evidence=('Pinned CODEX ' + $Model + '/' + $Reasoning + ' ready') }
    git_push_permission = [ordered]@{ status='PASS'; material=$true; executable=$Git; evidence='Task branch push dry-run PASS' }
}

$notes = @(
    ('Accepted BUILD result=' + $SourceBase + '; real host lifecycle still NOT_RUN before this PreExec.'),
    ('Installed=' + $installed + '; current_package=' + $currentSha + '; current_source=' + $currentSource + '; state=' + $controlState + '.'),
    ('WPF count=' + $wpf.Count + '; pid=' + $wpfPid + '; exact current package=' + $wpfExact + '; inspect=' + $uiInspect + '.'),
    ('Worker/legacy count=' + $workerLegacy.Count + '; paused=' + $paused + '; setup=' + $setupComplete + '; no current dispatch verified when installed.'),
    ('Durable hashes only: config=' + $configHash + '; database=' + $dbHash + '; manual_consumption=' + $consumptionHash + '; uninstall=' + $uninstallHash + '.'),
    ('Build env=' + $BuildAlias + '; python=' + $be.python + '; pip=' + $be.pip + '; setuptools=' + $be.setuptools + '; wheel=' + $be.wheel + '; build=' + $be.build + '; dotnet=' + $dotnetVersion + '.'),
    'No package build/install/update/uninstall/reinstall, WPF exit, Worker/F1, G3/G4/Canary or Bridge lifecycle mutation occurred during PreExec.',
    'One exact stale current-package WPF may be observed and left untouched; any graceful cleanup belongs only to a future fresh executable TEST Dispatch.',
    'PASS permits CHAT intake only. Dispatch remains unpublished and Agent lifecycle certification has not started.'
)

$receipt = [ordered]@{
    schema_version='1.0'
    receipt_type='FOX2_PREEXEC_RECEIPT'
    project='FOX2'
    wp_id='FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
    checked_at=[DateTime]::UtcNow.ToString('o')
    task_branch=$Branch
    receipt_path=$ReceiptPath
    source_head=$PublicationHead
    task_source=[ordered]@{ git_path=$TaskPath; git_commit_sha=$TaskCommit; sha256=$TaskSha256 }
    status='PASS'
    capabilities=$cap
    blockers=@()
    worktree=[ordered]@{ status='PASS'; path=$Worktree; competing_writer='NONE_OBSERVED'; stale_receipt_cleanup='NOT_NEEDED' }
    candidate_route=[ordered]@{ product='CODEX'; model_policy='PINNED'; model=$Model; reasoning_effort=$Reasoning; permission_profile='FULL_ACCESS' }
    dispatch_state=[ordered]@{ executable_dispatch_published=$false; dispatch_consumed=$false }
    agent_execution_started=$false
    notes=$notes
}

$dir = Split-Path -Parent $receiptFull
[IO.Directory]::CreateDirectory($dir) | Out-Null
$json = ($receipt | ConvertTo-Json -Depth 20).TrimEnd()
$json = $json.Replace(([string][char]13 + [char]10),[string][char]10)
Require (-not $json.Contains([char]13)) 'RECEIPT_LONE_CR'
$json = $json + [char]10
[IO.File]::WriteAllText($receiptFull,$json,[Text.UTF8Encoding]::new($false))

$afterText = G @('status','--porcelain=v1','--untracked-files=all')
$after = @($afterText -split '\r?\n' | Where-Object { $_ })
Require ($after.Count -eq 1 -and $after[0].EndsWith($ReceiptPath)) 'UNEXPECTED_WIP'

G @('add','--',$ReceiptPath) | Out-Null
$stagedText = G @('diff','--cached','--name-only')
$staged = @($stagedText -split '\r?\n' | Where-Object { $_ })
Require ($staged.Count -eq 1 -and $staged[0] -ceq $ReceiptPath) 'STAGED_SCOPE_MISMATCH'

$dc = Run -File $Git -Args @('-C',$Worktree,'diff','--cached','--check')
Require ($dc.Code -eq 0) 'DIFF_CHECK_FAILED'
Require ((RemoteHead) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_COMMIT'

$commit = Run -File $Git -Args @(
    '-C',$Worktree,
    '-c','core.hooksPath=NUL',
    '-c','commit.gpgsign=false',
    '-c','user.name=FOX2 PreExec',
    '-c','user.email=fox2-preexec@local.invalid',
    'commit','-m','preexec(fox2): host lifecycle cert A02 route PASS'
)
Require ($commit.Code -eq 0) ('COMMIT_FAILED:' + (Safe ($commit.Err + ' ' + $commit.Out)))

$receiptCommit = G @('rev-parse','HEAD')
Require ((G @('rev-list','--parents','-n','1',$receiptCommit)) -ceq ($receiptCommit + ' ' + $PublicationHead)) 'RECEIPT_PARENT_MISMATCH'
$cpText = G @('diff-tree','--no-commit-id','--name-only','-r',$receiptCommit)
$cp = @($cpText -split '\r?\n' | Where-Object { $_ })
Require ($cp.Count -eq 1 -and $cp[0] -ceq $ReceiptPath) 'RECEIPT_COMMIT_SCOPE_MISMATCH'

Require ((RemoteHead) -ceq $PublicationHead) 'REMOTE_MOVED_BEFORE_PUSH'
$push = Run -File $Git -Args @('-C',$Worktree,'push','origin',($receiptCommit + ':refs/heads/' + $Branch)) -Timeout 90
Require ($push.Code -eq 0) ('PUSH_FAILED:' + (Safe ($push.Err + ' ' + $push.Out)))
Require ((RemoteHead) -ceq $receiptCommit) 'REMOTE_READBACK_MISMATCH'

$receiptBlob = G @('rev-parse',($receiptCommit + ':' + $ReceiptPath))
$receiptHash = (Get-FileHash -LiteralPath $receiptFull -Algorithm SHA256).Hash.ToLowerInvariant()

Write-Output ''
Write-Output '=== FOX2 HOST LIFECYCLE CERT A02 PREEXEC RESULT ==='
Write-Output 'FOX2_PREEXEC_STATUS=PASS'
Write-Output ('FOX2_PREEXEC_PUBLICATION_HEAD=' + $PublicationHead)
Write-Output ('FOX2_PREEXEC_REMOTE_COMMIT=' + $receiptCommit)
Write-Output ('FOX2_PREEXEC_RECEIPT_BLOB=' + $receiptBlob)
Write-Output ('FOX2_PREEXEC_RECEIPT_SHA256=' + $receiptHash)
Write-Output ('FOX2_HOST_INSTALLED=' + $installed)
Write-Output ('FOX2_HOST_WPF_COUNT=' + $wpf.Count)
Write-Output ('FOX2_HOST_WPF_EXACT_CURRENT=' + $wpfExact)
Write-Output ('FOX2_HOST_WORKER_LEGACY_COUNT=' + $workerLegacy.Count)
Write-Output 'FOX2_IMPLEMENTATION_AGENT_EXECUTION_STARTED=FALSE'
Write-Output 'FOX2_DISPATCH_PUBLISHED=FALSE'
Write-Output 'FOX2_DISPATCH_CONSUMED=FALSE'
Write-Output 'FOX2_HOST_LIFECYCLE_MUTATION=FALSE'
Write-Output 'FOX2_G3_ALLOWED=FALSE'
Write-Output 'FOX2_PREEXEC_DELIVERY=REMOTE_READBACK_PASS'
Write-Output 'FOX2_NEXT=CHAT_INTAKE_THEN_PASS_TO_ASSIGN_THEN_FRESH_DISPATCH'
