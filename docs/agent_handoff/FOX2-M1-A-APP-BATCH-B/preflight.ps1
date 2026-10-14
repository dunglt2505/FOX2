$ErrorActionPreference = "Stop"
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
    if ($dirty) { throw ("worktree is not clean before preflight:" + [Environment]::NewLine + ($dirty | Out-String)) }
    Invoke-Git -Args @("-C",$Worktree,"pull","--ff-only","origin",$Branch) | Out-Null
    return (& git -C $Worktree rev-parse HEAD).Trim()
}

function Require-Command {
    param([string]$Name)
    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $cmd) { throw "required command missing: $Name" }
    return $cmd.Source
}

function Write-Receipt {
    param([object]$Receipt,[string]$Path)
    $parent = Split-Path -Parent $Path
    New-Item -ItemType Directory -Force -Path $parent | Out-Null
    $json = $Receipt | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($Path, $json + [Environment]::NewLine, [Text.UTF8Encoding]::new($false))
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
$Branch = "work/FOX2-M1-A-APP-BATCH-B"
$Worktree = "C:\Projects\FOX2-worktrees\FOX2-M1-A-APP-BATCH-B"
$ReceiptRel = "reports/FOX2-M1-A-APP-BATCH-B/preexec/local_preflight.json"

if (-not (Test-Path $Repo)) { throw "FOX2 repo missing: $Repo" }
Require-Command "git" | Out-Null
$head = Ensure-TaskWorktree -Repo $Repo -Branch $Branch -Worktree $Worktree

$node = Require-Command "node"
$npm = Require-Command "npm"
$npx = Require-Command "npx"
$nodeVersion = (& $node --version).Trim()
$npmVersion = (& $npm --version).Trim()
$npxVersion = (& $npx --version).Trim()
$npmPingOutput = (& $npm ping --silent 2>&1 | Out-String)
$npmRegistry = if ($LASTEXITCODE -eq 0) { "PASS" } else { "FAIL" }
if ($npmRegistry -ne "PASS") { throw "npm registry/package-resolution preflight failed: $npmPingOutput" }

$probePrompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
$copilot = Get-Command copilot -ErrorAction SilentlyContinue
$codex = Get-Command codex -ErrorAction SilentlyContinue
$copilotResult = [ordered]@{ status="NOT_RUN"; version=$null; output_marker=$false }
$codexResult = [ordered]@{ status="NOT_RUN"; version=$null; output_marker=$false }
$selected = $null
$route = $null

if ($copilot) {
    $copilotResult.version = ((& $copilot.Source --version 2>&1 | Out-String).Trim())
    $copilotArgs = @("-C",$Worktree,"--prompt",$probePrompt,"--allow-all-tools","--allow-all-paths","--allow-all-urls","--model","auto","--no-ask-user","--output-format","json","--auto-tier","balance")
    $out = (& $copilot.Source @copilotArgs 2>&1 | Out-String)
    $ok = ($LASTEXITCODE -eq 0 -and $out -match "FOX2_PREFLIGHT_OK")
    $copilotResult.status = if ($ok) { "PASS" } else { "FAIL" }
    $copilotResult.output_marker = $ok
    if ($ok) {
        $selected = "COPILOT"
        $route = [ordered]@{ model_policy="NATIVE_AUTO"; auto_tier="balance"; model="auto"; reasoning_effort=$null; permission_profile="FULL_ACCESS" }
    }
}

if (-not $selected -and $codex) {
    $codexResult.version = ((& $codex.Source --version 2>&1 | Out-String).Trim())
    $codexArgs = @("--ask-for-approval","never","exec","--sandbox","danger-full-access","--json","--model","gpt-6.1-sol","-c","model_reasoning_effort=`"low`"","-")
    $out = ($probePrompt | & $codex.Source @codexArgs 2>&1 | Out-String)
    $ok = ($LASTEXITCODE -eq 0 -and $out -match "FOX2_PREFLIGHT_OK")
    $codexResult.status = if ($ok) { "PASS" } else { "FAIL" }
    $codexResult.output_marker = $ok
    if ($ok) {
        $selected = "CODEX"
        $route = [ordered]@{ model_policy="PINNED"; auto_tier=$null; model="gpt-6.1-sol"; reasoning_effort="medium"; permission_profile="FULL_ACCESS" }
    }
}

if (-not $selected) { throw "no eligible Agent demonstrated current execution capacity; Copilot=$($copilotResult.status), Codex=$($codexResult.status)" }

$receipt = [ordered]@{
    schema_version = "1.0"
    project = "FOX2"
    wp_id = "FOX2-M1-A-APP-BATCH-B"
    checked_at = [DateTimeOffset]::Now.ToString("o")
    branch = $Branch
    worktree = $Worktree
    source_head = $head
    r3_material_capability = [ordered]@{
        node = [ordered]@{ status="PASS"; executable=$node; version=$nodeVersion }
        npm = [ordered]@{ status="PASS"; executable=$npm; version=$npmVersion; registry=$npmRegistry }
        npx = [ordered]@{ status="PASS"; executable=$npx; version=$npxVersion }
        copilot = $copilotResult
        codex = $codexResult
        selected_agent = $selected
        selected_route = $route
    }
    r5_worktree = [ordered]@{ status="PASS"; branch=$Branch; clean_before_probe=$true; competing_writer="NONE_OBSERVED" }
    execution_authorized = "NO_FROM_PREFLIGHT"
    note = "Preflight evidence only. CHAT must publish the canonical Dispatch v3 before implementation."
}

$receiptPath = Join-Path $Worktree $ReceiptRel
Write-Receipt -Receipt $receipt -Path $receiptPath
$published = Publish-Receipt -Worktree $Worktree -Branch $Branch -RelativePath $ReceiptRel -Message "preflight: record APP Batch B local readiness"
Write-Host "FOX2_APP_BATCH_B_PREFLIGHT_PUSHED"
Write-Host "REMOTE_SHA=$published"
Write-Host "SELECTED_AGENT=$selected"
