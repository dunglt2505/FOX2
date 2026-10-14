$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false
Set-StrictMode -Version Latest

$Repo = "C:\Projects\FOX2"
$Branch = "work/FOX2-M1-A-APP-BATCH-B"
$Worktree = "C:\Projects\FOX2-worktrees\FOX2-M1-A-APP-BATCH-B"
$ReceiptRel = "reports/FOX2-M1-A-APP-BATCH-B/preexec/local_preflight.json"
$receipt = [ordered]@{ schema_version="1.1"; project="FOX2"; wp_id="FOX2-M1-A-APP-BATCH-B"; checked_at=[DateTimeOffset]::Now.ToString("o"); status="BLOCKED"; branch=$Branch; worktree=$Worktree; source_head=$null; blockers=@(); capabilities=[ordered]@{}; execution_authorized="NO_FROM_PREFLIGHT" }
$publishable = $false
$exitCode = 20

function Get-WorktreeForBranch([string]$repo,[string]$branch) {
  $path = $null
  foreach ($line in @(& git -C $repo worktree list --porcelain)) {
    if ($line -like "worktree *") { $path = $line.Substring(9) }
    elseif ($line -eq ("branch refs/heads/" + $branch)) { return $path }
  }
  return $null
}

function Resolve-AppTool([string]$name) {
  $cmd = Get-Command $name -ErrorAction SilentlyContinue
  if ($cmd) { return $cmd.Source }

  $nodeHome = Join-Path $env:ProgramFiles "nodejs"
  $fallback = switch ($name) {
    "node" { Join-Path $nodeHome "node.exe" }
    "npm"  { Join-Path $nodeHome "npm.cmd" }
    "npx"  { Join-Path $nodeHome "npx.cmd" }
    default { $null }
  }
  if ($fallback -and (Test-Path $fallback)) { return $fallback }
  return $null
}

function Classify-AgentFailure([string]$text,[int]$code,[bool]$marker) {
  $t = $text.ToLowerInvariant()
  if ($t -match "auth|login|unauthorized|forbidden") { return "AUTH_REQUIRED" }
  if ($t -match "quota|rate.?limit|capacity|exhaust|insufficient") { return "CAPACITY_OR_QUOTA" }
  if ($t -match "unknown model|unsupported model|invalid.*model|model_reasoning") { return "MODEL_OR_CONFIG_UNSUPPORTED" }
  if ($t -match "sandbox|approval|allow-all|permission|unknown option|unrecognized option") { return "PERMISSION_OR_CLI_ARGS" }
  if ($code -eq 0 -and -not $marker) { return "RESPONSE_MARKER_MISSING" }
  return "CLI_NONZERO"
}

function Probe-Copilot([string]$worktree) {
  $cmd = Get-Command copilot -ErrorAction SilentlyContinue
  if (-not $cmd) { return [ordered]@{status="MISSING";version=$null;exit_code=$null;failure_class="TOOL_MISSING"} }
  $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim())
  $prompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
  $args = @("-C",$worktree,"--prompt",$prompt,"--allow-all-tools","--allow-all-paths","--allow-all-urls","--model","auto","--no-ask-user","--output-format","json","--auto-tier","balance")
  $out = (& $cmd.Source @args 2>&1 | Out-String)
  $code = $LASTEXITCODE
  $marker = ($out -match "FOX2_PREFLIGHT_OK")
  if ($code -eq 0 -and $marker) { return [ordered]@{status="PASS";version=$version;exit_code=0;failure_class=$null} }
  return [ordered]@{status="FAIL";version=$version;exit_code=$code;failure_class=(Classify-AgentFailure $out $code $marker)}
}

function Probe-Codex([string]$worktree) {
  $cmd = Get-Command codex -ErrorAction SilentlyContinue
  if (-not $cmd) { return [ordered]@{status="MISSING";version=$null;exit_code=$null;failure_class="TOOL_MISSING"} }
  $version = ((& $cmd.Source --version 2>&1 | Out-String).Trim())
  $prompt = "Reply exactly FOX2_PREFLIGHT_OK. Do not read or write files. Do not run tools."
  $args = @("--ask-for-approval","never","exec","--sandbox","danger-full-access","--json","--model","gpt-6.1-sol","-c","model_reasoning_effort=`"low`"","-")
  $out = ($prompt | & $cmd.Source @args 2>&1 | Out-String)
  $code = $LASTEXITCODE
  $marker = ($out -match "FOX2_PREFLIGHT_OK")
  if ($code -eq 0 -and $marker) { return [ordered]@{status="PASS";version=$version;exit_code=0;failure_class=$null} }
  return [ordered]@{status="FAIL";version=$version;exit_code=$code;failure_class=(Classify-AgentFailure $out $code $marker)}
}

try {
  if (-not (Test-Path $Repo)) { throw "FOX2 repo missing" }
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "git missing" }
  & git -C $Repo fetch origin ("refs/heads/" + $Branch + ":refs/remotes/origin/" + $Branch)
  if ($LASTEXITCODE -ne 0) { throw "git fetch failed" }
  $bound = Get-WorktreeForBranch $Repo $Branch
  if ($bound -and ([IO.Path]::GetFullPath($bound) -ne [IO.Path]::GetFullPath($Worktree))) { throw ("writer/worktree collision at " + $bound) }
  if (-not (Test-Path $Worktree)) {
    & git -C $Repo show-ref --verify --quiet ("refs/heads/" + $Branch)
    if ($LASTEXITCODE -eq 0) { & git -C $Repo worktree add $Worktree $Branch } else { & git -C $Repo worktree add -b $Branch $Worktree ("origin/" + $Branch) }
    if ($LASTEXITCODE -ne 0) { throw "worktree create failed" }
  }
  $allDirty = @(& git -C $Worktree status --porcelain --untracked-files=all)
  if ($allDirty.Count -gt 0) {
    $receiptDirty = @(& git -C $Worktree status --porcelain --untracked-files=all -- $ReceiptRel)
    if ($receiptDirty.Count -eq 0 -or (($allDirty -join "`n") -ne ($receiptDirty -join "`n"))) { throw ("non-preflight WIP exists: " + ($allDirty -join " | ")) }
    & git -C $Worktree reset --quiet HEAD -- $ReceiptRel 2>$null
    $stale = Join-Path $Worktree $ReceiptRel
    if (Test-Path $stale) { Remove-Item -Force $stale }
  }
  & git -C $Worktree pull --ff-only origin $Branch
  if ($LASTEXITCODE -ne 0) { throw "git pull --ff-only failed" }
  $receipt.source_head = (& git -C $Worktree rev-parse HEAD).Trim()
  $receipt.r5_worktree = [ordered]@{status="PASS";competing_writer="NONE_OBSERVED";stale_receipt_cleanup="SAFE_ONLY"}
  $publishable = $true

  foreach ($name in @("node","npm","npx")) {
    $toolPath = Resolve-AppTool $name
    if ($toolPath) {
      $ver = ((& $toolPath --version 2>&1 | Out-String).Trim())
      $receipt.capabilities[$name] = [ordered]@{status="PASS";executable=$toolPath;version=$ver}
    } else {
      $receipt.capabilities[$name] = [ordered]@{status="MISSING";executable=$null;version=$null}
      $receipt.blockers += ("MISSING_" + $name.ToUpperInvariant())
    }
  }
  if ($receipt.capabilities["npm"].status -eq "PASS") {
    $npmPath = $receipt.capabilities["npm"].executable
    $null = (& $npmPath ping --silent 2>&1 | Out-String)
    $npmCode = $LASTEXITCODE
    $receipt.capabilities["npm_registry"] = [ordered]@{status=($(if($npmCode -eq 0){"PASS"}else{"FAIL"}));exit_code=$npmCode}
    if ($npmCode -ne 0) { $receipt.blockers += "NPM_REGISTRY_UNAVAILABLE" }
  } else { $receipt.capabilities["npm_registry"] = [ordered]@{status="NOT_RUN";exit_code=$null} }

  $copilot = Probe-Copilot $Worktree
  $codex = Probe-Codex $Worktree
  $receipt.capabilities["copilot"] = $copilot
  $receipt.capabilities["codex"] = $codex
  if ($copilot.status -eq "PASS") {
    $receipt.selected_agent="COPILOT"; $receipt.selected_route=[ordered]@{model_policy="NATIVE_AUTO";auto_tier="balance";model="auto";reasoning_effort=$null;permission_profile="FULL_ACCESS"}
  } elseif ($codex.status -eq "PASS") {
    $receipt.selected_agent="CODEX"; $receipt.selected_route=[ordered]@{model_policy="PINNED";auto_tier=$null;model="gpt-6.1-sol";reasoning_effort="medium";permission_profile="FULL_ACCESS"}
  } else { $receipt.blockers += "NO_AGENT_CURRENT_EXECUTION_PROOF" }
  if ($receipt.blockers.Count -eq 0) { $receipt.status="PASS"; $exitCode=0 }
} catch { $receipt.blockers += ("PREFLIGHT_EXCEPTION:" + $_.Exception.Message) }

if (-not $publishable) { Write-Error ("preflight could not safely publish receipt: " + ($receipt.blockers -join ",")); exit 31 }
$receipt.checked_at=[DateTimeOffset]::Now.ToString("o")
$receiptPath = Join-Path $Worktree $ReceiptRel
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $receiptPath) | Out-Null
$json = ($receipt | ConvertTo-Json -Depth 16) -replace "`r`n","`n"
$json = ($json -replace "`r","`n").TrimEnd() + "`n"
[IO.File]::WriteAllText($receiptPath,$json,[Text.UTF8Encoding]::new($false))
& git -C $Worktree add -- $ReceiptRel
& git -C $Worktree diff --cached --check
if ($LASTEXITCODE -ne 0) { Write-Error "canonical receipt hygiene failed"; exit 30 }
$staged = @(& git -C $Worktree diff --cached --name-only)
if ($staged.Count -ne 1 -or $staged[0].Trim() -ne $ReceiptRel) { Write-Error ("unexpected staged scope: " + ($staged -join ",")); exit 30 }
& git -C $Worktree commit -m ("preflight: record APP Batch B " + $receipt.status.ToLowerInvariant())
if ($LASTEXITCODE -ne 0) { Write-Error "preflight receipt commit failed"; exit 30 }
& git -C $Worktree push origin ("HEAD:refs/heads/" + $Branch)
if ($LASTEXITCODE -ne 0) { Write-Error "preflight receipt push failed"; exit 30 }
$local = (& git -C $Worktree rev-parse HEAD).Trim()
$remote = ((& git -C $Worktree ls-remote --refs origin ("refs/heads/" + $Branch)).Trim() -split "\s+")[0]
if ($local -ne $remote) { Write-Error "remote readback mismatch"; exit 30 }
Write-Host ("APP_PREFLIGHT_RECEIPT_PUSHED=" + $local)
Write-Host ("APP_PREFLIGHT_STATUS=" + $receipt.status)
if ($receipt.blockers.Count -gt 0) { Write-Host ("APP_PREFLIGHT_BLOCKERS=" + ($receipt.blockers -join ",")) }
exit $exitCode
