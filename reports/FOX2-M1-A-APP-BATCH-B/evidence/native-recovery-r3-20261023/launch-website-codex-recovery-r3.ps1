# Immutable recovery R3, same Whole-WP and assignment; original preserved.
& {
Set-StrictMode -Version Latest
$PSNativeCommandUseErrorActionPreference = $false
$OriginalLauncher = 'C:\Users\Fox Le\.codex\.chatgpt-projects\g-p-6abcbc976b948191a760dbb0c316a64d\work\website_codex_20261023\current\launch-website-codex.ps1'
if ((Get-FileHash -LiteralPath $OriginalLauncher -Algorithm SHA256).Hash -ne '1916309D9DC96F8F2A93D834EBF797BFE4B66A8FC2F96F4BC7DBCA6D1817580D') { throw 'Original launcher changed; reconcile.' }
$ErrorActionPreference = 'Stop'
$Base = '92191f1d9701a9886ed886e6653e39d604b8b617'
$Assignment = 'e7c4d83a13c9bcf8d39d67ea9112b1727fe7fdde'
$Gov = '0da03b052c6a63d560e830c7956a2625c0bfe843'
$Branch = 'work/FOX2-M1-A-APP-BATCH-B'
$AssignBranch = 'work/FOX2-M1-A-APP-BATCH-B-CODEX-CONTINUE-20261023'
$Task = 'FOX2-M1-A-APP-BATCH-B'
$Prefix = "docs/agent_handoff/$Task/native-codex-continue-20261023"
$Url = 'https://github.com/dunglt2505/FOX2.git'
$RunRoot = 'C:\Users\Fox Le\AppData\Local\FOX2\APP-BATCH-B-CODEX-CONTINUE-20261023'
$RepoDir = Join-Path $RunRoot 'repo'
$InputDir = Join-Path $RunRoot 'assignment'
$Utf8 = New-Object System.Text.UTF8Encoding($false)
$NL = [Environment]::NewLine
function G {
    $out = & $GitPath -C $RepoDir @args
    if ($LASTEXITCODE -ne 0) { throw "Git failed (exit $LASTEXITCODE): $($args -join ' ')" }
    return $out
}
function Save-Text([string]$Path, [string]$Text) {
    [IO.File]::WriteAllText($Path, $Text, $Utf8)
}
function Assert-Paths([string[]]$Paths) {
    foreach ($p in $Paths) {
        if ($p -notmatch '^(frontend/|tests/app_batch_b/|reports/FOX2-M1-A-APP-BATCH-B/)' -or
            $p -match '(^|/)\.\.(/|$)' -or
            $p -match '^reports/FOX2-M1-A-APP-BATCH-B/preexec/') {
            throw "Out-of-scope path: $p"
        }
    }
}
function Remote-Head([string]$Ref) {
    $rows = @(G ls-remote --exit-code origin "refs/heads/$Ref")
    if ($rows.Count -ne 1) { throw "Ambiguous remote ref: $Ref" }
    return ($rows[0] -split '\s+')[0]
}
if ($PSVersionTable.PSVersion.Major -lt 7) { throw 'Open PowerShell 7 (pwsh) and paste again.' }
$OutputEncoding = $Utf8
[Console]::OutputEncoding = $Utf8
if ($env:OS -ne 'Windows_NT') { throw 'Windows host required.' }
$GitPath = (Get-Command git -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
$CodexPath = (Get-Command codex -CommandType Application -ErrorAction Stop | Select-Object -First 1).Source
$null = Get-Command node,npm,python -ErrorAction Stop
$cliVersion = (& $CodexPath --version | Out-String).Trim()
if ($LASTEXITCODE -ne 0 -or $cliVersion -ne 'codex-cli 0.162.1') {
    throw "CLI differs from verified version: $cliVersion"
}
$helpText = (& $CodexPath exec --help | Out-String)
if ($LASTEXITCODE -ne 0) { throw 'Cannot inspect Codex exec.' }
foreach ($flag in @('--sandbox','--model','--config','--cd','--output-last-message')) {
    if (-not $helpText.Contains($flag)) { throw "CLI capability missing: $flag" }
}
$authText = (& $CodexPath login status 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $authText -notmatch 'Logged in') { throw 'Codex not authenticated.' }
$nodeMajor = [int]((& node -p 'process.versions.node.split(".")[0]') | Select-Object -Last 1)
if ($LASTEXITCODE -ne 0 -or $nodeMajor -lt 20) { throw 'Node 20+ required.' }
& npm --version
if ($LASTEXITCODE -ne 0) { throw 'npm unavailable.' }
& python -c 'import sys; assert sys.version_info >= (3,11); print(sys.version.split()[0])'
if ($LASTEXITCODE -ne 0) { throw 'Python 3.11+ required.' }
$CodexDir = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE '.codex' }
$models = Get-Content -Raw -LiteralPath (Join-Path $CodexDir 'models_cache.json') | ConvertFrom-Json
$chosen = @($models.models | Where-Object { $_.slug -eq 'gpt-6.1-sol' })
if ($chosen.Count -ne 1 -or 'medium' -notin @($chosen[0].supported_reasoning_levels.effort)) {
    throw 'Pinned gpt-6.1-sol/medium not observed; no model fallback.'
}
if (-not (Test-Path -LiteralPath $RepoDir -PathType Container)) { throw 'Original checkout missing.' }
function Assert-Unused {
    if ((Get-FileHash -LiteralPath (Join-Path $RunRoot 'recovery-r2-claim.json') -Algorithm SHA256).Hash -ne '3E0E1DFB7F3BA2416D5BF6D0F3F379701B7518615C49EB24397B8E6D2A2EE689') { throw 'Prior claim changed; reconcile.' }
    $unexpected = @(Get-ChildItem -LiteralPath $RunRoot -Force | Where-Object { $_.Name -notin @('repo','assignment','recovery-r2-claim.json') })
    if ($unexpected.Count) { throw "Run has markers/unexpected artifacts: $($unexpected.Name -join ', '); reconcile, never replay." }
    if ((G rev-parse HEAD) -ne $Base -or (G branch --show-current) -ne $Branch) { throw 'Original checkout changed.' }
    if (@(G status --porcelain --untracked-files=all).Count) { throw 'Dirty checkout; reconcile.' }
    if (@(G ls-files --others --ignored --exclude-standard).Count) { throw 'Ignored artifacts; reconcile.' }
    if ((G remote get-url origin) -ne $Url -or (G remote get-url --push origin) -ne $Url) { throw 'Wrong remote.' }
}
$mutex = New-Object System.Threading.Mutex($false, 'Local\FOX2_APP_BATCH_B_CODEX_20261023')
$held = $false
try {
    $held = $mutex.WaitOne(0)
    if (-not $held) { throw 'Another local launcher owns this task.' }
    Assert-Unused
    if ((G remote get-url origin) -ne $Url) { throw 'Wrong repository.' }
    if ((Remote-Head $Branch) -ne $Base) { throw 'APP source advanced; review required.' }
    if ((G rev-parse HEAD) -ne $Base -or (G branch --show-current) -ne $Branch) { throw 'Wrong source/branch.' }
    if (@(G status --porcelain).Count -ne 0) { throw 'Worktree not clean.' }
    G fetch --no-tags origin "refs/heads/$($AssignBranch):refs/remotes/origin/$AssignBranch"
    if ((G rev-parse "refs/remotes/origin/$AssignBranch") -ne $Assignment) { throw 'Assignment head mismatch.' }
    G fetch --no-tags origin $Gov
    G fetch --no-tags origin 'refs/heads/main:refs/remotes/origin/main'
    $blobs = @{
        'task.md' = '90db231affb2e4dd052eaad1914fae25692aba16'
        'prompt.md' = '035395325c16db77c09f073e4b18e191dce84efc'
        'source-lock.json' = 'f4dbb76af89fe86044b0c3ae8321f6031bdac334'
    }
    foreach ($name in $blobs.Keys) {
        $spec = "$($Assignment):$Prefix/$name"
        if ((G rev-parse $spec) -ne $blobs[$name]) { throw "Input mismatch: $name" }
        Save-Text (Join-Path $InputDir $name) ((G show $spec) -join $NL)
    }
    $lock = Get-Content -Raw -LiteralPath (Join-Path $InputDir 'source-lock.json') | ConvertFrom-Json
    if ($lock.base_sha -ne $Base -or $lock.governance_sha -ne $Gov -or $lock.task_id -ne $Task) { throw 'Source-lock mismatch.' }
    foreach ($s in @($lock.product_sources) + @($lock.current_increment_evidence)) {
        if ((G rev-parse "$($Base):$($s.path)") -ne $s.blob_sha1) { throw "Product source mismatch: $($s.path)" }
    }
    $govDir = Join-Path $InputDir 'governance'
    $null = New-Item -ItemType Directory -Path $govDir -Force
    foreach ($s in $lock.governance_sources) {
        if ((G rev-parse "$($Gov):$($s.path)") -ne $s.blob_sha1 -or
            (G rev-parse "refs/remotes/origin/main:$($s.path)") -ne $s.blob_sha1) {
            throw "Governance changed/mismatch: $($s.path)"
        }
        Save-Text (Join-Path $govDir ([IO.Path]::GetFileName($s.path))) ((G show "$($Gov):$($s.path)") -join $NL)
    }
    $reg = Get-Content -Raw -LiteralPath (Join-Path $govDir 'FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json') | ConvertFrom-Json
    if ($reg.status -ne 'GOVERNANCE_EFFECTIVE_OWNER_AUTHORIZED_IN_SCOPE') { throw 'Governance not effective.' }
    # Owner-supplied identity, repository local only.
    G config --local user.name 'dunglt2505'
    G config --local user.email '339199063+dunglt2505@users.noreply.github.com'
    if ((G config --local --get user.name) -ne 'dunglt2505' -or
        (G config --local --get user.email) -ne '339199063+dunglt2505@users.noreply.github.com') { throw 'Local identity verification failed.' }
    G push --dry-run origin "HEAD:refs/heads/$Branch"
    $ignore = @('', '/frontend/node_modules/', '/frontend/dist/', '/frontend/.venv/', '/tests/app_batch_b/.venv/', '**/__pycache__/', '**/.pytest_cache/', '')
    [IO.File]::AppendAllText((Join-Path $RepoDir '.git/info/exclude'), ($ignore -join $NL), $Utf8)
    # Exclusive durable claim under the original task mutex; never retry this attempt.
    $claimPath = Join-Path $RunRoot 'recovery-r3-claim.json'
    $claim = [IO.File]::Open($claimPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try {
        $bytes = $Utf8.GetBytes((@{task_id=$Task; attempt='native-recovery-r3'; prior_state='NOT_STARTED'; source=$Base; assignment=$Assignment; pid=$PID; claimed_utc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json))
        $claim.Write($bytes,0,$bytes.Length)
        $claim.Flush($true)
    } finally { $claim.Dispose() }
    Save-Text (Join-Path $RunRoot 'started.json') (@{
        task_id=$Task; source=$Base; assignment=$Assignment; model='gpt-6.1-sol'
        effort='medium'; attempt='native-recovery-r3'; pid=$PID; started_utc=[DateTime]::UtcNow.ToString('o'); status='STARTING_NOT_ACCEPTED'
    } | ConvertTo-Json)
    $promptText = Get-Content -Raw -LiteralPath (Join-Path $InputDir 'prompt.md')
    $promptText += $NL + "Runner inputs: $InputDir" + $NL + "Use task_id=$Task in evidence_manifest.json. Do not commit/push; runner publishes candidate."
    $codexArgs = @('exec','--model','gpt-6.1-sol',
        '--config','model_reasoning_effort="medium"',
        '--config','sandbox_workspace_write.network_access=true',
        '--sandbox','workspace-write','--cd',$RepoDir,
        '--output-last-message',(Join-Path $RunRoot 'codex-final.txt'),'-')
    # Actual invocation checks current capacity. Never retry automatically.
    $promptText | & $CodexPath @codexArgs 2>&1 | Tee-Object -FilePath (Join-Path $RunRoot 'codex-transcript.txt')
    $agentExit = $LASTEXITCODE
    Save-Text (Join-Path $RunRoot 'agent-exit.txt') ([string]$agentExit)
    if ($agentExit -ne 0) { throw "Codex exited $agentExit; preserve evidence, no replay/push." }
    if ((G rev-parse HEAD) -ne $Base -or (G branch --show-current) -ne $Branch) { throw 'Agent changed branch/commit.' }
    $raw = ((G -c core.quotepath=false diff --name-only --no-renames -z HEAD) -join $NL) +
           ((G -c core.quotepath=false ls-files --others --exclude-standard -z) -join $NL)
    Assert-Paths @($raw -split ([char]0) | Where-Object { $_ })
    foreach ($name in @('report.md','evidence_manifest.json')) {
        if (-not (Test-Path -LiteralPath (Join-Path $RepoDir "reports/$Task/$name") -PathType Leaf)) { throw "Missing result: $name" }
    }
    $manifest = Get-Content -Raw -LiteralPath (Join-Path $RepoDir "reports/$Task/evidence_manifest.json") | ConvertFrom-Json
    if ($manifest.task_id -ne $Task) { throw 'Result task_id mismatch.' }
    G diff --check HEAD
    if ((Remote-Head $Branch) -ne $Base) { throw 'Remote writer advanced APP branch; do not overwrite.' }
    G add -A -- frontend tests/app_batch_b "reports/$Task"
    $staged = ((G -c core.quotepath=false diff --cached --name-only --no-renames -z) -join $NL) -split ([char]0)
    Assert-Paths @($staged | Where-Object { $_ })
    G diff --cached --check
    G commit -m 'APP-BATCH-B: Codex Website completion candidate and actual evidence'
    $resultSha = G rev-parse HEAD
    G push origin "HEAD:refs/heads/$Branch"
    if ((Remote-Head $Branch) -ne $resultSha) { throw 'Remote SHA readback failed.' }
    G fetch --no-tags origin "refs/heads/$($Branch):refs/remotes/origin/$Branch"
    foreach ($name in @('report.md','evidence_manifest.json')) {
        $p = "reports/$Task/$name"
        if ((G rev-parse "$($resultSha):$p") -ne (G rev-parse "refs/remotes/origin/$($Branch):$p")) { throw "Remote blob mismatch: $name" }
    }
    Save-Text (Join-Path $RunRoot 'remote-result-sha.txt') $resultSha
    Write-Host "REMOTE_RESULT_SHA=$resultSha"
    Write-Host "PUSHED_UNREVIEWED; CHAT acceptance pending. Result: $RunRoot"
}
finally {
    if ($held) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}
}

