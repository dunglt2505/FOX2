#requires -Version 7.0
& {
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
function Need([bool]$Condition,[string]$Reason) {
    if (!$Condition) { throw ('STOP: ' + $Reason) }
}
Need (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)) 'Use non-elevated Owner session'
$All = @(Get-CimInstance Win32_Process -ErrorAction Stop)
$Services = @(Get-CimInstance Win32_Service -Filter "Name='CodexSandboxService.OpenAI.Codex'" -ErrorAction Stop)
$Unknown = @($All | Where-Object {
    ([string]$_.Name) -match '(?i)^(python|pythonw|pwsh|powershell|codex|FOX2)' -and
    [string]::IsNullOrWhiteSpace([string]$_.CommandLine)
})
foreach ($Process in $Unknown) {
    $Sandbox = @($Services | Where-Object {
        $_.ProcessId -eq $Process.ProcessId -and $_.State -eq 'Running'
    })
    Need (([string]$Process.Name -ieq 'codex-windows-sandbox-service.exe') -and
        $Sandbox.Count -eq 1) 'Unattributed relevant process; no mutation'
}
$Workers = @($All | Where-Object {
    ([string]$_.CommandLine) -match '(?i)fox2_agent_bridge\s+worker|fox2_agent_bridge\.f1_service|desktop_tray\.ps1|FOX2F1Authority'
})
$Writers = @($All | Where-Object {
    ([string]$_.Name) -match '(?i)^codex([.-].*)?\.exe$' -and
    ([string]$_.CommandLine).IndexOf('FOX2-BRIDGE-',[StringComparison]::OrdinalIgnoreCase) -ge 0
})
$Wpf = @($All | Where-Object { ([string]$_.Name) -ieq 'FOX2.Bridge.Desktop.exe' })
Need ($Workers.Count -eq 0 -and $Writers.Count -eq 0 -and $Wpf.Count -eq 0) 'Bridge process or writer present'
$Python = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python313\python.exe'
Need (Test-Path -LiteralPath $Python -PathType Leaf) 'Owner Python unavailable'
$Code = @'
import hashlib, importlib.util, io, json, sqlite3, subprocess, sys, tempfile, zipfile
from contextlib import closing
from pathlib import Path
def need(ok):
    if not ok:
        raise RuntimeError("RECONCILE")
def main():
    root=Path.home()/"AppData/Local/FOX2/AgentBridge"
    package=Path("C:/Projects/FOX2-artifacts/host_lifecycle_cert_a04/FOX2-Bridge-085cc830-A04.zip")
    expected="f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee"
    claim=Path("C:/Projects/FOX2/.git/fox2-attempts/FOX2-BRIDGE-INTERNAL-VALIDATION-001.claim.json")
    output=Path("C:/Projects/FOX2-artifacts/bridge_internal_validation/attempt_001")
    for path in (claim,output):
        try:
            path.stat()
        except FileNotFoundError:
            continue
        raise RuntimeError("EXISTING_ATTEMPT")
    raw=package.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==expected)
    pointer=json.loads((root/"current.json").read_text(encoding="utf-8-sig"))
    need(pointer["package_sha256"]==expected)
    need(pointer["source_sha256"]=="6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73")
    version=root/"versions"/expected
    installed=version/"runtime/Lib/site-packages"
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        with zipfile.ZipFile(io.BytesIO(z.read("wheels/fox2_agent_bridge-0.1.0-py3-none-any.whl"))) as w:
            modules=[n for n in w.namelist() if n.startswith("fox2_agent_bridge/") and n.endswith(".py")]
            need(len(modules)>30)
            for name in modules:
                need(hashlib.sha256((installed/name).read_bytes()).digest()
                     ==hashlib.sha256(w.read(name)).digest())
    reader=Path(sys.argv[1]).resolve()
    spec=importlib.util.spec_from_file_location("readonly_control",reader)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    # Local transient copies only; live SQLite is opened only by standard pause.
    tempfile.tempdir=str(reader.parent)
    before=mod.inspect(root)
    need(before["safe"] or before["failed"]==["paused"])
    def protected():
        return [(root/p).read_bytes() for p in ("config/bridge.toml","data/manual_consumption.json")]
    identity=protected()
    if before["safe"]:
        action="ALREADY_PAUSED"
    else:
        result=subprocess.run(
            [str(version/"runtime/Scripts/python.exe"),"-I","-B","-m",
             "fox2_agent_bridge","control","pause"],
            capture_output=True,timeout=30)
        need(result.returncode==0)
        state=json.loads(result.stdout)
        need(state.get("paused") is True)
        action="PAUSE_RESTORED"
    after=mod.inspect(root)
    need(after["safe"] and identity==protected())
    need(not claim.exists() and not output.exists())
    print(json.dumps({"schema":"FOX2_PAUSE_RECOVERY_V1","action":action,
        "safe":True,"failed":[],"source_modules_verified":len(modules),
        "config_manual_bytes_unchanged":True,"internal_claim":"ABSENT",
        "internal_output":"ABSENT","validator_run":False,
        "worker_f1_legacy_count":0,"bridge_writer_count":0,
        "sandbox_service_exclusion":"EXACT_NAME_AND_SERVICE_PID",
        "lifecycle":"NOT_RUN","no_replay":True},sort_keys=True))
try:
    main()
except Exception:
    print('{"schema":"FOX2_PAUSE_RECOVERY_V1","status":"NEEDS_RECONCILIATION","validator_run":false}')
    sys.exit(2)
'@
$Reader = Join-Path $PSScriptRoot 'control_reader.py'
Need (Test-Path -LiteralPath $Reader -PathType Leaf) 'Read-only reader unavailable'
$Lines = @(& $Python -I -B -c $Code $Reader 2>$null)
$RecoveryExit = $LASTEXITCODE
Write-Output ($Lines -join [Environment]::NewLine)
Need ($RecoveryExit -eq 0) 'Pause recovery requires reconciliation; do not rerun blindly'
}

