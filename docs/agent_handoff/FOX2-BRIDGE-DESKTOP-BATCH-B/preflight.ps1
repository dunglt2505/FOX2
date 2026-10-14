$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest
function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    $output = & git @Args 2>&1
    if ($LASTEXITCODE -ne 0) { throw ("git failed: git " + ($Args -join " ") + [Environment]::NewLine + ($output | Out-String)) }
    return $output
}

function Get-BranchWorktree {
    param([string]$Repo,[string]$Branch)
    $lines = & git -C $Repo worktree list --porcelain
    $path = $null
    foreach ($line in $lines) {
        if ($line -like "worktree *") { $path = $line.Substring(9) }
        elseif ($line -eq "branch refs/heads/$Branch") { return $path }
    }
    return $null
}

function Ensure-TaskWorktree {
    param([string]$Repo,[string]$Branch,[string]$Worktree)
    Invoke-Git -Args @("-C",$Repo,"fetch","origin",("refs/heads/" + $Branch + ":refs/remotes/origin/" + $Branch)) | Out-Null
    $bound = Get-BranchWorktree -Repo $Repo -Branch $Branch
    if ($bound -and ([IO.Path]::GetFullPath($bound) -ne [IO.Path]::GetFullPath($Worktree))) { throw "writer/worktree collision: $Branch is already checked out at $bound" }
    if (-not (Test-Path $Worktree)) {
        & git -C $Repo show-ref --verify --quiet ("refs/heads/" + $Branch)
        if ($LASTEXITCODE -eq 0) { Invoke-Git -Args @("-C",$Repo,"worktree","add",$Worktree,$Branch) | Out-Null }
        else { Invoke-Git -Args @("-C",$Repo,"worktree","add","-b",$Branch,$Worktree,("origin/" + $Branch)) | Out-Null }
    }
    $actual = (& git -C $Worktree branch --show-current).Trim()
    if ($actual -ne $Branch) { throw "wrong worktree branch: $actual" }
    $dirty = & git -C $Worktree status --porcelain
    $receiptDirty = @(& git -C $Worktree status --porcelain --untracked-files=all -- $ReceiptRel)
    if ($dirty) {
        if ($receiptDirty.Count -eq 0 -or ((@($dirty) -join "`n") -ne ($receiptDirty -join "`n"))) { throw ("worktree has non-preflight WIP:" + "`n" + ($dirty | Out-String)) }
        & git -C $Worktree reset --quiet HEAD -- $ReceiptRel 2>$null
        $stale = Join-Path $Worktree $ReceiptRel
        if (Test-Path $stale) { Remove-Item -Force $stale }
    }
    Invoke-Git -Args @("-C",$Worktree,"pull","--ff-only","origin",$Branch) | Out-Null
    return (& git -C $Worktree rev-parse HEAD).Trim()
}

function Require-Command {
    param([string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $cmd) { throw "required command missing: $Name" }
    return $cmd.Source
}

function Classify-AgentFailure {
    param([string]$Text,[int]$ExitCode,[bool]$Marker)
    $t = $Text.ToLowerInvariant()
    if ($t -match "auth|login|unauthorized|forbidden") { return "AUTH_REQUIRED" }
    if ($t -match "quota|rate.?limit|capacity|exhaust|insufficient") { return "CAPACITY_OR_QUOTA" }
    if ($t -match "unknown model|unsupported model|invalid.*model|model_reasoning") { return "MODEL_OR_CONFIG_UNSUPPORTED" }
    if ($t -match "sandbox|approval|allow-all|permission|unknown option|unrecognized option") { return "PERMISSION_OR_CLI_ARGS" }
    if ($ExitCode -eq 0 -and -not $Marker) { return "RESPONSE_MARKER_MISSING" }
    return "CLI_NONZERO"
}

function Write-Receipt {
    param([object]$Receipt,[string]$Path)
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    $json = ($Receipt | ConvertTo-Json -Depth 12) -replace "`r`n","`n"
    $json = ($json -replace "`r","`n").TrimEnd() + "`n"
    [IO.File]::WriteAllText($Path, $json, [Text.UTF8Encoding]::new($false))
}

function Publish-Receipt {
    param([string]$Worktree,[string]$Branch,[string]$RelativePath,[string]$Message)
    Invoke-Git -Args @("-C",$Worktree,"add","--",$RelativePath) | Out-Null
    Invoke-Git -Args @("-C",$Worktree,"diff","--cached","--check") | Out-Null
    $staged = @(& git -C $Worktree diff --cached --name-only)
    $normalized = $RelativePath.Replace("\\","/")
    if ($staged.Count -ne 1 -or $staged[0].Trim() -ne $normalized) { throw ("preflight publication scope mismatch: " + ($staged -join ",")) }
    Invoke-Git -Args @("-C",$Worktree,"commit","-m",$Message) | Out-Null
    Invoke-Git -Args @("-C",$Worktree,"push","origin",("HEAD:refs/heads/" + $Branch)) | Out-Null
    $local = (& git -C $Worktree rev-parse HEAD).Trim()
    $remoteLine = (& git -C $Worktree ls-remote --refs origin ("refs/heads/" + $Branch)).Trim()
    $remote = ($remoteLine -split "\s+")[0]
    if ($remote -ne $local) { throw "remote readback mismatch: local=$local remote=$remote" }
    return $local
}

$Repo = "C:\Projects\FOX2"
$Branch = "work/FOX2-BRIDGE-DESKTOP-BATCH-B"
$Worktree = "C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B"
$ReceiptRel = "reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json"

if (-not (Test-Path $Repo)) { throw "FOX2 repo missing: $Repo" }
Require-Command "git" | Out-Null
$head = Ensure-TaskWorktree -Repo $Repo -Branch $Branch -Worktree $Worktree

$python = Require-Command "python"
$pwsh = Require-Command "pwsh"
$schtasks = Require-Command "schtasks.exe"
$pythonVersion = (& $python --version 2>&1 | Out-String).Trim()
$pwshVersion = (& $pwsh -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' | Out-String).Trim()
if (-not $env:LOCALAPPDATA) { throw "LOCALAPPDATA is not available" }
$probeDir = Join-Path $env:LOCALAPPDATA "AgentBridge-preflight"
New-Item -ItemType Directory -Force -Path $probeDir | Out-Null
$probeFile = Join-Path $probeDir "write-test.tmp"
[IO.File]::WriteAllText($probeFile, "FOX2" + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
Remove-Item -Force $probeFile

$probePrompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
$codex = Get-Command codex -ErrorAction SilentlyContinue
$copilot = Get-Command copilot -ErrorAction SilentlyContinue
$codexResult = [ordered]@{ status="NOT_RUN"; version=$null; output_marker=$false }
$copilotResult = [ordered]@{ status="NOT_RUN"; version=$null; output_marker=$false }
$selected = $null
$route = $null

if ($codex) {
    $codexResult.version = ((& $codex.Source --version 2>&1 | Out-String).Trim())
    $codexArgs = @("--ask-for-approval","never","exec","--sandbox","danger-full-access","--json","--model","gpt-6.1-sol","-c","model_reasoning_effort=`"low`"","-")
    $out = ($probePrompt | & $codex.Source @codexArgs 2>&1 | Out-String)
    $codexExit = $LASTEXITCODE
    $ok = ($codexExit -eq 0 -and $out -match "FOX2_PREFLIGHT_OK")
    $codexResult.status = if ($ok) { "PASS" } else { "FAIL" }
    $codexResult.output_marker = $ok
    $codexResult.exit_code = $codexExit
    $codexResult.failure_class = if ($ok) { $null } else { Classify-AgentFailure -Text $out -ExitCode $codexExit -Marker $ok }
    if ($ok) {
        $selected = "CODEX"
        $route = [ordered]@{ model_policy="PINNED"; auto_tier=$null; model="gpt-6.1-sol"; reasoning_effort="medium"; permission_profile="FULL_ACCESS" }
    }
}

if (-not $selected -and $copilot) {
    $copilotResult.version = ((& $copilot.Source --version 2>&1 | Out-String).Trim())
    $copilotArgs = @("-C",$Worktree,"--prompt",$probePrompt,"--allow-all-tools","--allow-all-paths","--allow-all-urls","--model","auto","--no-ask-user","--output-format","json","--auto-tier","balance")
    $out = (& $copilot.Source @copilotArgs 2>&1 | Out-String)
    $copilotExit = $LASTEXITCODE
    $ok = ($copilotExit -eq 0 -and $out -match "FOX2_PREFLIGHT_OK")
    $copilotResult.status = if ($ok) { "PASS" } else { "FAIL" }
    $copilotResult.output_marker = $ok
    $copilotResult.exit_code = $copilotExit
    $copilotResult.failure_class = if ($ok) { $null } else { Classify-AgentFailure -Text $out -ExitCode $copilotExit -Marker $ok }
    if ($ok) {
        $selected = "COPILOT"
        $route = [ordered]@{ model_policy="NATIVE_AUTO"; auto_tier="balance"; model="auto"; reasoning_effort=$null; permission_profile="FULL_ACCESS" }
    }
}

$blocked = -not $selected

$receipt = [ordered]@{
    schema_version = "1.0"
    project = "FOX2"
    wp_id = "FOX2-BRIDGE-DESKTOP-BATCH-B"
    checked_at = [DateTimeOffset]::Now.ToString("o")
    branch = $Branch
    worktree = $Worktree
    source_head = $head
    r3_material_capability = [ordered]@{
        python = [ordered]@{ status="PASS"; executable=$python; version=$pythonVersion }
        powershell7 = [ordered]@{ status="PASS"; executable=$pwsh; version=$pwshVersion }
        task_scheduler = [ordered]@{ status="PASS"; executable=$schtasks }
        local_appdata_per_user_write = "PASS"
        codex = $codexResult
        copilot = $copilotResult
        selected_agent = $selected
        selected_route = $route
    }
    r5_worktree = [ordered]@{ status="PASS"; branch=$Branch; clean_before_probe=$true; competing_writer="NONE_OBSERVED" }
    status = $(if ($blocked) { "BLOCKED" } else { "PASS" })
    blockers = $(if ($blocked) { @("NO_AGENT_CURRENT_EXECUTION_PROOF") } else { @() })
    execution_authorized = "NO_FROM_PREFLIGHT"
    note = "Preflight evidence only. CHAT must publish the canonical Dispatch v3 before implementation."
}

$receiptPath = Join-Path $Worktree $ReceiptRel
Write-Receipt -Receipt $receipt -Path $receiptPath
$published = Publish-Receipt -Worktree $Worktree -Branch $Branch -RelativePath $ReceiptRel -Message "preflight: record Bridge Batch B local readiness"
Write-Host "FOX2_BRIDGE_BATCH_B_PREFLIGHT_RECEIPT_PUSHED"
Write-Host "REMOTE_SHA=$published"
Write-Host ("STATUS=" + $receipt.status)
Write-Host "SELECTED_AGENT=$selected"
if ($blocked) { exit 20 }
