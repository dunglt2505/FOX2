#requires -Version 7.0
# FOX2 Bridge Git Delivery: physical Windows read-only intake.
# No Bridge imports, no CLI agent launch, no SQLite initialization,
# no fetch/push/commit, no supervisor/process/Windows policy mutation.
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
if (-not $IsWindows) { throw 'STOP: Owner-selected physical Windows required' }

$Repo = 'C:\Projects\FOX2'
$Root = Join-Path $env:LOCALAPPDATA 'FOX2\AgentBridge'
$Db = Join-Path $Root 'data\bridge.db'
$Check = [ordered]@{
    schema = 'FOX2_BRIDGE_GIT_DELIVERY_HOST_READONLY_V1'
    target = 'OWNER_SELECTED_PHYSICAL_WINDOWS'
    observed_utc = [DateTime]::UtcNow.ToString('o')
    repo = [ordered]@{
        exists = $false
        origin_matches = $false
        branch = 'NOT_VERIFIED'
        sha = 'NOT_VERIFIED'
        dirty = 'NOT_VERIFIED'
    }
    installed = [ordered]@{
        root_exists = $false
        pointer_status = 'NOT_FOUND'
        package_sha256 = $null
        package_source_commit = $null
        receipt_identity = 'NOT_VERIFIED'
        venv_python_present = $false
        config_present = $false
    }
    ledger = [ordered]@{
        database_present = $false
        observation = 'NOT_RUN'
        schema_version = $null
        dispatch_state_counts = $null
        execution_state_counts = $null
        worker_paused = $null
        runtime_writer_quiescence = 'NOT_ATTESTED'
    }
    tools = [ordered]@{
        git_present = $false
        codex_in_path = $false
        copilot_in_path = $false
        pwsh_present = $true
    }
    git_push_rights = 'NOT_VERIFIED_NO_WRITE_TEST'
    test_plan_verifier_bound = 'NOT_ATTESTED'
    recovery_ref_authority = 'NOT_ATTESTED'
    exclusive_writer_lease = 'NOT_ATTESTED'
    wip_process_tree_quiescence = 'NOT_ATTESTED'
    dispatch_replay = 'NONE'
    git_mutation = 'NONE'
    host_mutation = 'NONE'
    installed_runtime_git_delivery_e2e = 'NOT_RUN'
    internal_ready = 'NOT_ATTESTED'
}

$GitCmd = Get-Command git -ErrorAction SilentlyContinue
$Check.tools.git_present = ($null -ne $GitCmd)
$Check.tools.codex_in_path = ($null -ne (Get-Command codex -ErrorAction SilentlyContinue))
$Check.tools.copilot_in_path = ($null -ne (Get-Command copilot -ErrorAction SilentlyContinue))

if ((Test-Path -LiteralPath $Repo -PathType Container) -and
    (Test-Path -LiteralPath (Join-Path $Repo '.git')) -and $GitCmd) {
    $Check.repo.exists = $true
    try {
        $GitExe = $GitCmd.Source
        $ShaOut = @(& $GitExe -C $Repo rev-parse --verify HEAD 2>$null)
        if ($LASTEXITCODE -eq 0 -and $ShaOut.Count -eq 1 -and
            $ShaOut[0] -match '^[0-9a-f]{40}$') {
            $Check.repo.sha = $ShaOut[0]
        }
        $BranchOut = @(& $GitExe -C $Repo branch --show-current 2>$null)
        if ($LASTEXITCODE -eq 0 -and $BranchOut.Count -le 1) {
            $Check.repo.branch = if ($BranchOut.Count) { [string]$BranchOut[0] } else { 'DETACHED' }
        }
        $Origin = @(& $GitExe -C $Repo remote get-url origin 2>$null)
        if ($LASTEXITCODE -eq 0 -and $Origin.Count -eq 1) {
            $Check.repo.origin_matches = [bool](
                $Origin[0] -match '(?i)(^|[:/])dunglt2505/FOX2(\.git)?/?$'
            )
        }
        $Dirty = @(& $GitExe --no-optional-locks -C $Repo status --porcelain=v1 --untracked-files=all 2>$null)
        if ($LASTEXITCODE -eq 0) {
            $Check.repo.dirty = ($Dirty.Count -gt 0)
        }
    } catch {
        # No raw Git errors/URLs/paths in the redacted report.
        $Check.repo.dirty = 'QUERY_INCOMPLETE'
    }
}

$Check.installed.root_exists = Test-Path -LiteralPath $Root -PathType Container
$Check.installed.config_present = Test-Path -LiteralPath (
    Join-Path $Root 'config\bridge.toml') -PathType Leaf
$RuntimePython = $null
$Pointer = Join-Path $Root 'current.json'
# StrictMode: the installed pointer may not exist. Keep a defined, nullable
# interpreter identity before the optional receipt lookup.
$RuntimePython = $null
if (Test-Path -LiteralPath $Pointer -PathType Leaf) {
    try {
        $Current = Get-Content -LiteralPath $Pointer -Raw -ErrorAction Stop |
            ConvertFrom-Json -ErrorAction Stop
        $Id = [string]$Current.package_sha256
        if ($Id -notmatch '^[0-9a-f]{64}$') {
            throw 'Invalid installed SHA'
        }
        $Check.installed.pointer_status = 'WELL_FORMED_POINTER_OBSERVED'
        $Check.installed.package_sha256 = $Id
        $Version = Join-Path $Root ('versions\' + $Id)
        $Receipt = Join-Path $Version 'receipt.json'
        $RuntimePython = Join-Path $Version 'runtime\Scripts\python.exe'
        $Check.installed.venv_python_present = Test-Path -LiteralPath $RuntimePython -PathType Leaf
        if (Test-Path -LiteralPath $Receipt -PathType Leaf) {
            $R = Get-Content -LiteralPath $Receipt -Raw -ErrorAction Stop |
                ConvertFrom-Json -ErrorAction Stop
            if ([string]$R.package_sha256 -ceq $Id) {
                $Check.installed.receipt_identity = 'POINTER_RECEIPT_SHA_FIELD_MATCH_NOT_ARCHIVE_VERIFIED'
                $Source = [string]$R.manifest.source_git_commit
                if ($Source -match '^[0-9a-f]{40}$') {
                    $Check.installed.package_source_commit = $Source
                }
            } else {
                $Check.installed.receipt_identity = 'MISMATCH'
            }
        } else {
            $Check.installed.receipt_identity = 'RECEIPT_MISSING'
        }
    } catch {
        $Check.installed.pointer_status = 'INVALID_OR_UNREADABLE'
        $Check.installed.receipt_identity = 'NOT_VERIFIED'
    }
}

$Check.ledger.database_present = Test-Path -LiteralPath $Db -PathType Leaf
if ($Check.ledger.database_present) {
    $DbPython = $null
    if ($null -ne $RuntimePython -and
        (Test-Path -LiteralPath $RuntimePython -PathType Leaf)) {
        $DbPython = $RuntimePython
    }
    if ($null -ne $DbPython) {
        # Python -B, sqlite mode=ro/query_only, a single consistent DB read
        # transaction; never call Bridge initialize_runtime (it migrates DB).
        $ReadCode = @'
import json, sqlite3, sys, urllib.parse
path = sys.argv[1]
uri = "file:" + urllib.parse.quote(path.replace("\\", "/"), safe=":/") + "?mode=ro"
con = sqlite3.connect(uri, uri=True, timeout=2)
con.execute("PRAGMA query_only=ON")
con.execute("BEGIN")
out = {"observation":"READONLY_TRANSACTION_NOT_QUIESCENCE",
       "schema_version":None,"dispatch_state_counts":None,
       "execution_state_counts":None,"worker_paused":None}
try:
    row = con.execute("SELECT value FROM bridge_meta WHERE key='schema_version'").fetchone()
    out["schema_version"] = str(row[0]) if row else "UNKNOWN"
    for table, name in (("dispatches","dispatch_state_counts"),
                        ("executions","execution_state_counts")):
        rows = con.execute("SELECT state, COUNT(*) FROM " + table + " GROUP BY state").fetchall()
        out[name] = {str(state): int(n) for state,n in rows}
    row = con.execute("SELECT payload FROM worker_state WHERE id=1").fetchone()
    if row:
        state = json.loads(row[0])
        if isinstance(state,dict) and isinstance(state.get("paused"),bool):
            out["worker_paused"] = state["paused"]
except (sqlite3.Error, ValueError, TypeError):
    out["observation"] = "READONLY_QUERY_INCOMPLETE"
finally:
    con.rollback()
    con.close()
print(json.dumps(out,sort_keys=True))
'@
        try {
            $Raw = @(& $DbPython -I -S -B -c $ReadCode $Db 2>$null)
            if ($LASTEXITCODE -eq 0 -and $Raw.Count -eq 1) {
                $Status = $Raw[0] | ConvertFrom-Json -ErrorAction Stop
                $Check.ledger.observation = [string]$Status.observation
                $Check.ledger.schema_version = $Status.schema_version
                $Check.ledger.dispatch_state_counts = $Status.dispatch_state_counts
                $Check.ledger.execution_state_counts = $Status.execution_state_counts
                $Check.ledger.worker_paused = $Status.worker_paused
            } else {
                $Check.ledger.observation = 'READONLY_QUERY_UNAVAILABLE'
            }
        } catch {
            $Check.ledger.observation = 'READONLY_QUERY_UNAVAILABLE'
        }
    } else {
        $Check.ledger.observation = 'INSTALLED_PYTHON_NOT_FOUND_NO_DATABASE_OPEN'
    }
}
Write-Output 'FOX2_BRIDGE_GIT_DELIVERY_READONLY=COMPLETE'
$Check | ConvertTo-Json -Depth 7
Write-Output 'FOX2_BRIDGE_HOST_MUTATION=NONE'
