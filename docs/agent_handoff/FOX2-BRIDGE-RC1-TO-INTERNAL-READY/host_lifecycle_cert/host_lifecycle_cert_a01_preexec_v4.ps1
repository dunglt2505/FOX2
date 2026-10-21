#requires -Version 7.0
param(
    [Parameter(Mandatory)][string]$PublicationHead,
    [Parameter(Mandatory)][string]$ExpectedScriptBlob,
    [string]$Worktree = 'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Branch = 'work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021'
$SourceBase = '2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb'
$TaskId = 'FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01'
$TaskCommit = 'd95f08ceed2f5a25ad288b9630ffc87b698f329c'
$TaskPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/task.md'
$TaskBlob = '86e0afaec6f6e47c9d15b51564a38bf5167a892b'
$TaskSha256 = '95d64b3cb3999c55700ded2a6451cd9ffa23872fb87fd00c97df7edbb8c06221'

$PromptCommit = '250c8ab15bdfd8339e6332dc105a559dbd5b3151'
$PromptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/prompt.md'
$PromptBlob = '2fd33dbef3fc327ca71844b1e05670b312eefc7d'
$PromptSha256 = '4a3cab3096b9eca8a65938e5b36d658ceaca5e684def26524ce44cedebe1a689'

$ScriptPath = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec_v4.ps1'
$InvalidV3Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec_v3.ps1'
$InvalidV3Blob = 'bd246b96709c918d4b7576e763525930d656c56e'
$InvalidV1Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec.ps1'
$InvalidV1Blob = 'd13a6688b65f68c671ed4ea1eb3409b4fa2da203'
$InvalidV2Path = 'docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/host_lifecycle_cert_a01_preexec_v2.ps1'
$InvalidV2Blob = 'ee7b22338e4ce2e67e987587e8bb29f3dedc1075'
$ReceiptPath = 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a01.json'

$Model = 'gpt-6.1-sol'
$ReasoningEffort = 'high'
$Marker = 'FOX2_HOST_LIFECYCLE_CERT_A01_ADMISSION_OK'

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

Write-Output '=== FOX2 HOST LIFECYCLE CERT A01 PREEXEC V4 ==='
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
Require ($sourceAncestor.Code -eq 0) 'SOURCE_BASE_NOT_ANCESTOR'
$productDrift = Git @('diff','--name-only',($SourceBase + '..' + $PublicationHead),'--','agent_bridge')
Require ([string]::IsNullOrWhiteSpace($productDrift)) 'PREEXEC_PRODUCT_CODE_DRIFT'

$ancestor = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'merge-base','--is-ancestor',$PromptCommit,$PublicationHead) -TimeoutSeconds 30
Require ($ancestor.Code -eq 0) 'PREEXEC_PUBLICATION_NOT_DESCENDANT_OF_PROMPT'
$lineageOut = Git @('rev-list',($PromptCommit + '..' + $PublicationHead))
$lineage = @($lineageOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
Require ($lineage.Count -ge 4) 'PREEXEC_PUBLICATION_LINEAGE_TOO_SHORT'
$paths = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::Ordinal)
foreach ($commit in $lineage) {
    $pOut = Git @('diff-tree','--no-commit-id','--name-only','-r',$commit)
    foreach ($p in @($pOut -split '\r?\n' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
        $null = $paths.Add($p)
    }
}
$allowedPublicationPaths = @($InvalidV1Path,$InvalidV2Path,$InvalidV3Path,$ScriptPath)
foreach ($p in $paths) {
    Require ($p -in $allowedPublicationPaths) ('PREEXEC_PUBLICATION_UNEXPECTED_PATH:' + $p)
}
Require ($paths.Count -eq 4) 'PREEXEC_PUBLICATION_PATH_COUNT_MISMATCH'
Require ($paths.Contains($InvalidV1Path)) 'PREEXEC_V1_HISTORY_MISSING'
Require ($paths.Contains($InvalidV2Path)) 'PREEXEC_V2_HISTORY_MISSING'
Require ($paths.Contains($InvalidV3Path)) 'PREEXEC_V3_HISTORY_MISSING'
Require ($paths.Contains($ScriptPath)) 'PREEXEC_V4_PUBLICATION_MISSING'
Require ((Git @('rev-parse',('c1772c9f51f03425c865198329b2740921b6df51:' + $InvalidV1Path))) -ceq $InvalidV1Blob) 'PREEXEC_V1_BLOB_MISMATCH'
Require ((Git @('rev-parse',('69bc6fb7b61d4405d6db296a5b8211bddb6c13b2:' + $InvalidV2Path))) -ceq $InvalidV2Blob) 'PREEXEC_V2_BLOB_MISMATCH'
Require ((Git @('rev-parse',('45afc00b621f579202633fe705e2ec6f5ba4b5ed:' + $InvalidV3Path))) -ceq $InvalidV3Blob) 'PREEXEC_V3_BLOB_MISMATCH'

$receiptFull = Join-Path $Worktree ($ReceiptPath -replace '/', [IO.Path]::DirectorySeparatorChar)
Require (-not (Test-Path -LiteralPath $receiptFull)) 'PREEXEC_RECEIPT_ALREADY_EXISTS'
$receiptInGit = Run-Tool -File $GitExe -ToolArgs @('-C',$Worktree,'cat-file','-e',($PublicationHead + ':' + $ReceiptPath)) -TimeoutSeconds 30
Require ($receiptInGit.Code -ne 0) 'PREEXEC_RECEIPT_ALREADY_COMMITTED'

Assert-NoTaskWriter

# Read-only host/build readiness. No package or Bridge mutation occurs here.
$BridgeRoot = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$CurrentPath = Join-Path $BridgeRoot 'current.json'
$VersionsPath = Join-Path $BridgeRoot 'versions'
$HostInstalled = $false
$HostCurrentSha = $null
$HostSourceSha = $null
$HostControlState = 'NOT_INSTALLED'
$HostPaused = $null
$HostSetupComplete = $null
$StableUninstallSha256 = $null
$ConfigSha256 = $null
$DatabaseSha256 = $null
$ConsumptionSha256 = $null
$OwnedVersions = @()

if (Test-Path -LiteralPath $CurrentPath -PathType Leaf) {
    $HostInstalled = $true
    $current = Get-Content -LiteralPath $CurrentPath -Raw | ConvertFrom-Json
    $HostCurrentSha = [string]$current.package_sha256
    $HostSourceSha = [string]$current.source_sha256
    Require ($HostCurrentSha -match '^[0-9a-f]{64}$') 'HOST_CURRENT_POINTER_INVALID'
    $InstalledPython = Join-Path $VersionsPath ($HostCurrentSha + '\runtime\Scripts\python.exe')
    Require (Test-Path -LiteralPath $InstalledPython -PathType Leaf) 'HOST_CURRENT_RUNTIME_MISSING'
    $status = Run-Tool -File $InstalledPython -ToolArgs @('-I','-m','fox2_agent_bridge','control','status') -TimeoutSeconds 30 -Stage 'HOST_CONTROL_STATUS'
    Require ($status.Code -eq 0) 'HOST_CONTROL_STATUS_FAILED'
    $state = ([string]$status.Out).Trim() | ConvertFrom-Json
    $HostControlState = [string]$state.state
    $HostPaused = [bool]$state.paused
    $HostSetupComplete = [bool]$state.setup_complete
    Require ($HostPaused -eq $true) 'HOST_NOT_PAUSED'
}
elseif (Test-Path -LiteralPath $VersionsPath -PathType Container) {
    $orphaned = @(Get-ChildItem -LiteralPath $VersionsPath -Force -ErrorAction Stop)
    Require ($orphaned.Count -eq 0) 'HOST_ORPHANED_VERSIONS_WITHOUT_POINTER'
}

if (Test-Path -LiteralPath $VersionsPath -PathType Container) {
    $OwnedVersions = @(
        Get-ChildItem -LiteralPath $VersionsPath -Directory -Force -ErrorAction Stop |
        ForEach-Object { $_.Name } |
        Sort-Object
    )
    foreach ($identity in $OwnedVersions) {
        Require ($identity -match '^[0-9a-f]{64}$') 'HOST_VERSION_IDENTITY_INVALID'
        Require (Test-Path -LiteralPath (Join-Path (Join-Path $VersionsPath $identity) 'receipt.json') -PathType Leaf) 'HOST_UNOWNED_VERSION_PRESENT'
    }
}

$UninstallPath = Join-Path $BridgeRoot 'uninstall.ps1'
if (Test-Path -LiteralPath $UninstallPath -PathType Leaf) {
    $StableUninstallSha256 = (Get-FileHash -LiteralPath $UninstallPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
$ConfigPath = Join-Path $BridgeRoot 'config\bridge.toml'
$DatabasePath = Join-Path $BridgeRoot 'data\bridge.db'
$ConsumptionPath = Join-Path $BridgeRoot 'data\manual_consumption.json'
if (Test-Path -LiteralPath $ConfigPath -PathType Leaf) {
    $ConfigSha256 = (Get-FileHash -LiteralPath $ConfigPath -Algorithm SHA256).Hash.ToLowerInvariant()
}
if (Test-Path -LiteralPath $DatabasePath -PathType Leaf) {
    $DatabaseSha256 = (Get-FileHash -LiteralPath $DatabasePath -Algorithm SHA256).Hash.ToLowerInvariant()
}
if (Test-Path -LiteralPath $ConsumptionPath -PathType Leaf) {
    $ConsumptionSha256 = (Get-FileHash -LiteralPath $ConsumptionPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

$bridgeRootSlash = ($BridgeRoot -replace '\\','/')
$activeRuntime = @(
    Get-CimInstance Win32_Process -ErrorAction Stop |
    Where-Object {
        $line = [string]$_.CommandLine
        -not [string]::IsNullOrWhiteSpace($line) -and
        (
            $line.IndexOf($BridgeRoot,[StringComparison]::OrdinalIgnoreCase) -ge 0 -or
            $line.IndexOf($bridgeRootSlash,[StringComparison]::OrdinalIgnoreCase) -ge 0
        ) -and
        (
            $line -match '(?i)fox2_agent_bridge\s+worker' -or
            $line -match '(?i)desktop_(tray|launcher)\.ps1'
        )
    }
)
Require ($activeRuntime.Count -eq 0) 'HOST_ACTIVE_BRIDGE_RUNTIME_PRESENT'

$BuildRoots = @(
    (Join-Path $Worktree 'agent_bridge'),
    'C:\Projects\FOX2\agent_bridge'
) | Where-Object { Test-Path -LiteralPath $_ -PathType Container } | Select-Object -Unique

$BuildPython = $null
$BuildEnvironment = $null
$inspectBuild = @'
import importlib.metadata as m, json, sys
names=("jsonschema","attrs","referencing","rpds-py","jsonschema-specifications")
try:
    data=dict(
        isolated=sys.prefix!=sys.base_prefix,
        python=f"{sys.version_info.major}.{sys.version_info.minor}",
        platform=sys.platform,
        setuptools=m.version("setuptools"),
        wheel=m.version("wheel"),
        build=m.version("build"),
        dependencies={name:m.version(name) for name in names},
    )
    print(json.dumps(data))
except Exception:
    raise SystemExit(7)
'@

foreach ($root in $BuildRoots) {
    foreach ($candidate in @(Get-ChildItem -LiteralPath $root -Filter python.exe -File -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.FullName -match '(?i)\\Scripts\\python\.exe$' })) {
        $buildProbe = Run-Tool -File $candidate.FullName -ToolArgs @('-I','-c',$inspectBuild) -TimeoutSeconds 30
        if ($buildProbe.Code -ne 0) { continue }
        try { $envInfo = ([string]$buildProbe.Out).Trim() | ConvertFrom-Json } catch { continue }
        $major = 0
        try { $major = [int](([string]$envInfo.setuptools -split '\.')[0]) } catch { continue }
        $deps = $envInfo.dependencies
        $depsOk = $null -ne $deps -and
            -not [string]::IsNullOrWhiteSpace([string]$deps.jsonschema) -and
            -not [string]::IsNullOrWhiteSpace([string]$deps.attrs) -and
            -not [string]::IsNullOrWhiteSpace([string]$deps.referencing) -and
            -not [string]::IsNullOrWhiteSpace([string]$deps.'rpds-py') -and
            -not [string]::IsNullOrWhiteSpace([string]$deps.'jsonschema-specifications')
        if ($envInfo.isolated -eq $true -and
            [string]$envInfo.platform -eq 'win32' -and
            $major -ge 80 -and $major -lt 90 -and
            $depsOk -and
            -not [string]::IsNullOrWhiteSpace([string]$envInfo.wheel) -and
            -not [string]::IsNullOrWhiteSpace([string]$envInfo.build)) {
            $BuildPython = $candidate.FullName
            $BuildEnvironment = $envInfo
            break
        }
    }
    if ($null -ne $BuildPython) { break }
}
Require ($null -ne $BuildPython) 'COMPATIBLE_ISOLATED_BUILD_PYTHON_NOT_FOUND'

$BuildPythonAlias = if ($BuildPython.StartsWith($Worktree,[StringComparison]::OrdinalIgnoreCase)) {
    'WORKTREE/' + $BuildPython.Substring($Worktree.Length).TrimStart('\').Replace('\','/')
} elseif ($BuildPython.StartsWith('C:\Projects\FOX2',[StringComparison]::OrdinalIgnoreCase)) {
    'PROJECT/' + $BuildPython.Substring('C:\Projects\FOX2'.Length).TrimStart('\').Replace('\','/')
} else {
    'EXTERNAL_BUILD_PYTHON'
}

$dotnet = Run-Tool -File $DotnetExe -ToolArgs @('--version') -TimeoutSeconds 30 -Stage 'DOTNET_VERSION'
Require ($dotnet.Code -eq 0) 'DOTNET_NOT_READY'
$DotnetVersion = ([string]$dotnet.Out).Trim()
Require (-not [string]::IsNullOrWhiteSpace($DotnetVersion)) 'DOTNET_VERSION_EMPTY'

$lingeringProbe = @(
    Get-CimInstance Win32_Process -ErrorAction Stop |
    Where-Object {
        -not [string]::IsNullOrWhiteSpace([string]$_.CommandLine) -and
        ([string]$_.CommandLine).IndexOf(
            'FOX2-host-lifecycle-preexec-',
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

$temp = Join-Path ([IO.Path]::GetTempPath()) ('FOX2-host-lifecycle-preexec-' + [Guid]::NewGuid().ToString('N'))
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
    source_code_base = '2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb'
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
        dotnet='PASS'; isolated_build_python='PASS'; host_read_only_state='PASS'
    }
    host_readiness = [ordered]@{
        bridge_root_alias='LOCALAPPDATA/FOX2/AgentBridge'
        installed=$HostInstalled
        current_package_sha256=$HostCurrentSha
        current_source_sha256=$HostSourceSha
        control_state=$HostControlState
        paused=$HostPaused
        setup_complete=$HostSetupComplete
        owned_versions=$OwnedVersions
        active_runtime_processes=0
        stable_uninstall_sha256=$StableUninstallSha256
        config_sha256=$ConfigSha256
        database_sha256=$DatabaseSha256
        manual_consumption_sha256=$ConsumptionSha256
        build_python_alias=$BuildPythonAlias
        build_python_version=[string]$BuildEnvironment.python
        build_setuptools=[string]$BuildEnvironment.setuptools
        build_wheel=[string]$BuildEnvironment.wheel
        build_module=[string]$BuildEnvironment.build
        dotnet_version=$DotnetVersion
        host_mutation_performed=$false
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
        'PreExec v1, v2 and v3 were rejected before execution and are not executable.',
        'PreExec v4 is read-only with respect to the Bridge package lifecycle.',
        'No package build/install/update/uninstall/reinstall occurred during PreExec.',
        'Final host mutation requires CHAT remote intake and a fresh executable Dispatch.'
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
    'commit','-m','preexec(fox2): host lifecycle cert A01 route PASS'
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
