param(
    [switch]$SkipAuthRecovery
)

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Repo = "C:\Projects\FOX2"
$Branch = "work/FOX2-PREEXEC-ROLLOUT-V1"
$Worktree = "C:\Projects\FOX2-worktrees\FOX2-PREEXEC-ROLLOUT-V1"
$TaskRel = "docs/agent_handoff/FOX2-PREEXEC-ROLLOUT-V1/task.md"
$ReceiptRel = "reports/FOX2-PREEXEC-ROLLOUT-V1/preexec/local_preflight.json"
$DictionaryRel = "docs/governance/FOX2_PROJECT_DICTIONARY_v1.json"

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
    $out = & git @Args 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git failed: git $($Args -join ' ')"
    }
    return $out
}

function Get-BranchWorktree {
    param([string]$RepoPath,[string]$BranchName)
    $current = $null
    foreach ($line in @(& git -C $RepoPath worktree list --porcelain)) {
        if ($line -like "worktree *") { $current = $line.Substring(9) }
        elseif ($line -eq ("branch refs/heads/" + $BranchName)) { return $current }
    }
    return $null
}

function Ensure-Worktree {
    Invoke-Git -Args @("-C",$Repo,"fetch","origin",("refs/heads/" + $Branch + ":refs/remotes/origin/" + $Branch)) | Out-Null
    $bound = Get-BranchWorktree -RepoPath $Repo -BranchName $Branch
    if ($bound -and ([IO.Path]::GetFullPath($bound) -ne [IO.Path]::GetFullPath($Worktree))) {
        throw "rollout branch already has another worktree: $bound"
    }
    if (-not (Test-Path $Worktree)) {
        & git -C $Repo show-ref --verify --quiet ("refs/heads/" + $Branch)
        if ($LASTEXITCODE -eq 0) {
            Invoke-Git -Args @("-C",$Repo,"worktree","add",$Worktree,$Branch) | Out-Null
        } else {
            Invoke-Git -Args @("-C",$Repo,"worktree","add","-b",$Branch,$Worktree,("origin/" + $Branch)) | Out-Null
        }
    }

    $actual = (& git -C $Worktree branch --show-current).Trim()
    if ($actual -ne $Branch) { throw "wrong rollout worktree branch: $actual" }

    $allDirty = @(& git -C $Worktree status --porcelain --untracked-files=all)
    if ($allDirty.Count -gt 0) {
        $receiptDirty = @(& git -C $Worktree status --porcelain --untracked-files=all -- $ReceiptRel)
        if ($receiptDirty.Count -eq 0 -or (($allDirty -join "`n") -ne ($receiptDirty -join "`n"))) {
            throw ("rollout worktree has unrelated WIP: " + ($allDirty -join " | "))
        }
        & git -C $Worktree reset --quiet HEAD -- $ReceiptRel 2>$null
        $stale = Join-Path $Worktree $ReceiptRel
        if (Test-Path $stale) { [IO.File]::Delete($stale) }
    }

    Invoke-Git -Args @("-C",$Worktree,"pull","--ff-only","origin",$Branch) | Out-Null
}

function Classify-AgentFailure {
    param([string]$Text,[int]$ExitCode,[bool]$Marker)
    $t = $Text.ToLowerInvariant()
    if ($t -match "auth|login|sign in|sign-in|unauthorized|forbidden|credential") { return "AUTH_REQUIRED" }
    if ($t -match "quota|rate.?limit|capacity|exhaust|insufficient|credit") { return "CAPACITY_OR_QUOTA" }
    if ($t -match "unknown model|unsupported model|invalid.*model|model_reasoning|reasoning_effort") { return "MODEL_OR_CONFIG_UNSUPPORTED" }
    if ($t -match "sandbox|approval|allow-all|permission|unknown option|unrecognized option|unexpected argument") { return "PERMISSION_OR_CLI_ARGS" }
    if ($ExitCode -eq 0 -and -not $Marker) { return "RESPONSE_MARKER_MISSING" }
    return "CLI_NONZERO"
}

function New-Capability {
    param(
        [string]$Status,
        [bool]$Material,
        [AllowNull()][string]$Version,
        [AllowNull()][string]$Executable,
        [AllowNull()][Nullable[int]]$ExitCode,
        [AllowNull()][string]$FailureClass,
        [AllowNull()][string]$Evidence
    )
    return [ordered]@{
        status = $Status
        material = $Material
        version = $Version
        executable = $Executable
        exit_code = $ExitCode
        failure_class = $FailureClass
        evidence = $Evidence
    }
}

function Probe-Copilot {
    $cmd = Get-Command copilot -ErrorAction SilentlyContinue
    if (-not $cmd) {
        return [ordered]@{
            capability = (New-Capability -Status "MISSING" -Material $true -Version $null -Executable $null -ExitCode $null -FailureClass "TOOL_MISSING" -Evidence "copilot executable not found")
            raw_class = "TOOL_MISSING"
        }
    }

    $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim())
    $prompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
    $args = @(
        "-C",$Worktree,
        "--prompt",$prompt,
        "--allow-all",
        "--model","auto",
        "--auto-tier","balance",
        "--no-ask-user",
        "--no-auto-update",
        "--output-format","json"
    )
    $out = (& $cmd.Source @args 2>&1 | Out-String)
    $code = $LASTEXITCODE
    $marker = ($out -match "FOX2_PREFLIGHT_OK")
    if ($code -eq 0 -and $marker) {
        return [ordered]@{
            capability = (New-Capability -Status "PASS" -Material $true -Version $version -Executable $cmd.Source -ExitCode 0 -FailureClass $null -Evidence "minimal no-write FULL_ACCESS probe returned expected marker")
            raw_class = $null
        }
    }

    $class = Classify-AgentFailure -Text $out -ExitCode $code -Marker $marker
    return [ordered]@{
        capability = (New-Capability -Status "FAIL" -Material $true -Version $version -Executable $cmd.Source -ExitCode $code -FailureClass $class -Evidence "minimal no-write FULL_ACCESS probe failed; raw output not persisted")
        raw_class = $class
    }
}

function Probe-Codex {
    $cmd = Get-Command codex -ErrorAction SilentlyContinue
    if (-not $cmd) {
        return [ordered]@{
            capability = (New-Capability -Status "MISSING" -Material $true -Version $null -Executable $null -ExitCode $null -FailureClass "TOOL_MISSING" -Evidence "codex executable not found")
            raw_class = "TOOL_MISSING"
        }
    }

    $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim())
    $prompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
    $args = @(
        "exec",
        "-C",$Worktree,
        "--ephemeral",
        "--sandbox","danger-full-access",
        "-c",'approval_policy="never"',
        "--json",
        "--model","gpt-6.1-sol",
        "-c",'model_reasoning_effort="low"',
        "-"
    )
    $out = ($prompt | & $cmd.Source @args 2>&1 | Out-String)
    $code = $LASTEXITCODE
    $marker = ($out -match "FOX2_PREFLIGHT_OK")
    if ($code -eq 0 -and $marker) {
        return [ordered]@{
            capability = (New-Capability -Status "PASS" -Material $true -Version $version -Executable $cmd.Source -ExitCode 0 -FailureClass $null -Evidence "minimal no-write PINNED/FULL_ACCESS probe returned expected marker")
            raw_class = $null
        }
    }

    $class = Classify-AgentFailure -Text $out -ExitCode $code -Marker $marker
    return [ordered]@{
        capability = (New-Capability -Status "FAIL" -Material $true -Version $version -Executable $cmd.Source -ExitCode $code -FailureClass $class -Evidence "minimal no-write PINNED/FULL_ACCESS probe failed; raw output not persisted")
        raw_class = $class
    }
}

function Recover-CopilotAuth {
    $cmd = Get-Command copilot -ErrorAction SilentlyContinue
    if (-not $cmd) { return $false }
    Write-Host ""
    Write-Host "Copilot authentication is required. Opening official login flow..." -ForegroundColor Yellow
    & $cmd.Source login --web-flow
    return ($LASTEXITCODE -eq 0)
}

function Recover-CodexAuth {
    $cmd = Get-Command codex -ErrorAction SilentlyContinue
    if (-not $cmd) { return $false }
    Write-Host ""
    Write-Host "Codex authentication is required. Opening official login flow..." -ForegroundColor Yellow
    & $cmd.Source --login
    return ($LASTEXITCODE -eq 0)
}

function Publish-Receipt {
    param([object]$Receipt)
    $full = Join-Path $Worktree $ReceiptRel
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $full) | Out-Null
    $json = ($Receipt | ConvertTo-Json -Depth 20)
    $json = ($json -replace "`r`n","`n" -replace "`r","`n").TrimEnd() + "`n"
    [IO.File]::WriteAllText($full,$json,[Text.UTF8Encoding]::new($false))

    Invoke-Git -Args @("-C",$Worktree,"add","--",$ReceiptRel) | Out-Null
    Invoke-Git -Args @("-C",$Worktree,"diff","--cached","--check") | Out-Null

    $staged = @(& git -C $Worktree diff --cached --name-only)
    if ($staged.Count -ne 1 -or $staged[0].Trim() -ne $ReceiptRel) {
        throw ("unexpected staged scope: " + ($staged -join ","))
    }

    Invoke-Git -Args @("-C",$Worktree,"commit","-m",("preflight: record FOX2 PreExec rollout " + $Receipt.status.ToLowerInvariant())) | Out-Null
    Invoke-Git -Args @("-C",$Worktree,"push","origin",("HEAD:refs/heads/" + $Branch)) | Out-Null

    $local = (& git -C $Worktree rev-parse HEAD).Trim()
    $remote = ((& git -C $Worktree ls-remote --refs origin ("refs/heads/" + $Branch)).Trim() -split "\s+")[0]
    if ($local -ne $remote) { throw "remote readback mismatch" }

    Write-Host ("FOX2_PREEXEC_ROLLOUT_RECEIPT_PUSHED=" + $local) -ForegroundColor Green
    return $local
}

if (-not (Test-Path $Repo)) { throw "FOX2 repo missing: $Repo" }
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git missing" }

Ensure-Worktree

$sourceHead = (& git -C $Worktree rev-parse HEAD).Trim()
$taskPath = Join-Path $Worktree $TaskRel
$dictionaryPath = Join-Path $Worktree $DictionaryRel
if (-not (Test-Path $taskPath)) { throw "rollout task missing" }
if (-not (Test-Path $dictionaryPath)) { throw "Project Dictionary missing" }

$dictionary = Get-Content -Raw -Encoding UTF8 $dictionaryPath | ConvertFrom-Json
if ($dictionary.dictionary_version -ne "1.1") { throw "Dictionary v1.1 required" }
if ($dictionary.current.policy.version -ne "1.8.8") { throw "Policy V1.8.8 required" }
if ($dictionary.current.routing_index.version -ne "1.2.9") { throw "Routing V1.2.9 required" }
if ($dictionary.current.git_first_protocol.version -ne "11") { throw "Protocol v11 required" }
if ($dictionary.current.preflight_receipt_schema.version -ne "1") { throw "Preflight Receipt Schema v1 required" }

$capabilities = [ordered]@{}
$blockers = New-Object System.Collections.Generic.List[object]

foreach ($name in @("git","python","pwsh")) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) {
        $version = $null
        try {
            if ($name -eq "git") { $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim()) }
            elseif ($name -eq "python") { $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim()) }
            else { $version = ((& $cmd.Source -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()' | Out-String).Trim()) }
        } catch {}
        $capabilities[$name] = New-Capability -Status "PASS" -Material $true -Version $version -Executable $cmd.Source -ExitCode 0 -FailureClass $null -Evidence "required rollout host tool available"
    } else {
        $capabilities[$name] = New-Capability -Status "MISSING" -Material $true -Version $null -Executable $null -ExitCode $null -FailureClass "TOOL_MISSING" -Evidence "required rollout host tool missing"
        $blockers.Add([ordered]@{code=("MISSING_" + $name.ToUpperInvariant());class="CAPABILITY";material=$true;sanitized_detail="$name is required for rollout preflight/implementation"})
    }
}

$copilot = Probe-Copilot
if ($copilot.raw_class -eq "AUTH_REQUIRED" -and -not $SkipAuthRecovery) {
    if (Recover-CopilotAuth) { $copilot = Probe-Copilot }
}
$capabilities["copilot"] = $copilot.capability

$codex = Probe-Codex
if ($codex.raw_class -eq "AUTH_REQUIRED" -and -not $SkipAuthRecovery) {
    if (Recover-CodexAuth) { $codex = Probe-Codex }
}
if ($codex.capability.status -eq "FAIL" -and $codex.raw_class -eq "CLI_NONZERO") {
    $doctor = Get-Command codex -ErrorAction SilentlyContinue
    if ($doctor) {
        & $doctor.Source doctor *> $null
        $capabilities["codex_doctor"] = New-Capability -Status ($(if($LASTEXITCODE -eq 0){"PASS"}else{"FAIL"})) -Material $false -Version $null -Executable $doctor.Source -ExitCode $LASTEXITCODE -FailureClass ($(if($LASTEXITCODE -eq 0){$null}else{"CLI_NONZERO"})) -Evidence "codex doctor exit status only; output not persisted"
    }
}
$capabilities["codex"] = $codex.capability

$candidate = $null
if ($copilot.capability.status -eq "PASS") {
    $candidate = [ordered]@{
        product = "COPILOT"
        model_policy = "NATIVE_AUTO"
        model = "auto"
        auto_tier = "balance"
        reasoning_effort = $null
        permission_profile = "FULL_ACCESS"
    }
} elseif ($codex.capability.status -eq "PASS") {
    $candidate = [ordered]@{
        product = "CODEX"
        model_policy = "PINNED"
        model = "gpt-6.1-sol"
        auto_tier = $null
        reasoning_effort = "medium"
        permission_profile = "FULL_ACCESS"
    }
}

if (-not $candidate) {
    if ($copilot.capability.status -ne "PASS") {
        $blockers.Add([ordered]@{code="COPILOT_EXECUTION_NOT_PROVEN";class=$(if($copilot.capability.failure_class -eq "AUTH_REQUIRED"){"AUTH"}elseif($copilot.capability.failure_class -eq "CAPACITY_OR_QUOTA"){"CAPACITY"}else{"TOOLING"});material=$true;sanitized_detail=$copilot.capability.failure_class})
    }
    if ($codex.capability.status -ne "PASS") {
        $blockers.Add([ordered]@{code="CODEX_EXECUTION_NOT_PROVEN";class=$(if($codex.capability.failure_class -eq "AUTH_REQUIRED"){"AUTH"}elseif($codex.capability.failure_class -eq "CAPACITY_OR_QUOTA"){"CAPACITY"}else{"TOOLING"});material=$true;sanitized_detail=$codex.capability.failure_class})
    }
}

$hostMaterialFailed = $false
foreach ($k in @("git","python","pwsh")) {
    if ($capabilities[$k].status -ne "PASS") { $hostMaterialFailed = $true }
}

$status = if (-not $hostMaterialFailed -and $candidate) { "PASS" } else { "BLOCKED" }

$taskHash = (Get-FileHash -Algorithm SHA256 $taskPath).Hash.ToLowerInvariant()
$receipt = [ordered]@{
    schema_version = "1.0"
    receipt_type = "FOX2_PREEXEC_RECEIPT"
    project = "FOX2"
    wp_id = "FOX2-PREEXEC-ROLLOUT-V1"
    checked_at = [DateTimeOffset]::Now.ToString("o")
    task_branch = $Branch
    receipt_path = $ReceiptRel
    source_head = $sourceHead
    task_source = [ordered]@{
        git_path = $TaskRel
        git_commit_sha = $sourceHead
        sha256 = $taskHash
    }
    status = $status
    capabilities = $capabilities
    blockers = @($blockers)
    worktree = [ordered]@{
        status = "PASS"
        path = $Worktree
        competing_writer = "NONE_OBSERVED"
        stale_receipt_cleanup = "SAFE_ONLY"
    }
    candidate_route = $candidate
    dispatch_state = [ordered]@{
        executable_dispatch_published = $false
        dispatch_consumed = $false
    }
    agent_execution_started = $false
    notes = @(
        "Preflight only; no implementation Agent was started.",
        "Candidate route is advisory evidence until CHAT remote intake.",
        "Raw Agent probe output is intentionally not persisted."
    )
}

$published = Publish-Receipt -Receipt $receipt
Write-Host ("FOX2_PREEXEC_ROLLOUT_STATUS=" + $status)
if ($candidate) { Write-Host ("FOX2_PREEXEC_ROLLOUT_CANDIDATE=" + $candidate.product) }

if ($status -eq "PASS") { exit 0 }
exit 20
