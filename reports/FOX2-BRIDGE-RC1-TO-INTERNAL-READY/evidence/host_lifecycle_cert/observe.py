"""Read-only bounded host/source observer for this certification; never executes lifecycle."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[4]
AREA = Path(__file__).resolve().parent
BRIDGE = Path(os.environ['FOX2_BRIDGE_ROOT'])
BASE = '2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb'
START = os.environ['FOX2_EXECUTION_START_HEAD']
PWSH = r'C:\Program Files\PowerShell\7\pwsh.exe'

def now():
    return datetime.now(timezone.utc).isoformat()

def run(args, **kwargs):
    return subprocess.check_output(list(map(str, args)), text=True, timeout=60, **kwargs).strip()

def git(*args):
    return run(['git', '-C', ROOT, *args])

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None

def save(name, data):
    (AREA/name).write_text(json.dumps(data, indent=2, sort_keys=True)+'\n', encoding='utf-8', newline='\n')

def ps(code):
    return json.loads(run([PWSH, '-NoProfile', '-NonInteractive', '-Command', code]))

def snapshot():
    current = json.loads((BRIDGE/'current.json').read_text()) if (BRIDGE/'current.json').is_file() else None
    receipt = None
    state = None
    if current:
        version = BRIDGE/'versions'/current['package_sha256']
        receipt = json.loads((version/'receipt.json').read_text())
        raw = json.loads(run([version/'runtime/Scripts/python.exe', '-I', '-m', 'fox2_agent_bridge', 'control', 'status']))
        state = {k: raw.get(k) for k in ('state','paused','setup_complete','start_with_windows','stop_requested','active_dispatch_id')}
        state['active_dispatch_present'] = bool(state.pop('active_dispatch_id'))
    hashes = {p: sha(BRIDGE/p) for p in ('current.json','config/bridge.toml','data/bridge.db','data/manual_consumption.json','uninstall.ps1')}
    db = BRIDGE/'data/bridge.db'
    ledger = []
    integrity = None
    if db.is_file():
        with sqlite3.connect(db.as_uri()+'?mode=ro', uri=True) as conn:
            ledger = [dict(dispatch_id=d, state=s, payload_hash=h) for d,s,h in conn.execute('SELECT dispatch_id,state,payload_hash FROM dispatches ORDER BY dispatch_id')]
            integrity = conn.execute('PRAGMA quick_check').fetchone()[0]
    # Persist only aggregate counts and an identity digest; no private dispatch payloads.
    ledger_hash = hashlib.sha256(json.dumps(ledger,sort_keys=True).encode()).hexdigest()
    consumed = {x['dispatch_id']:x['state'] for x in ledger if x['dispatch_id'] in [
        'FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+n for n in ('001','002','003','004')]}
    observation = ps(r'''
    $root=$env:FOX2_BRIDGE_ROOT; $records=@(Get-CimInstance Win32_Process);
    $active=@($records | Where-Object {$l=[string]$_.CommandLine; $l.Contains($root) -and ($l -match 'fox2_agent_bridge\s+worker|desktop_(tray|launcher)\.ps1|install_user\.ps1|certify_user_lifecycle\.py')});
    $sid=[Security.Principal.WindowsIdentity]::GetCurrent().User.Value;
    $task=Get-ScheduledTask -TaskName ('FOX2Bridge-'+$sid) -ErrorAction SilentlyContinue;
    @{active_runtime_processes=$active.Count; startup_task_present=($null -ne $task);
      startup_task_state=if($task){[string]$task.State}else{$null};
      run_level=if($task){[string]$task.Principal.RunLevel}else{$null};
      logon_type=if($task){[string]$task.Principal.LogonType}else{$null}}|ConvertTo-Json -Compress
    ''')
    return dict(observed_at_utc=now(), bridge_root_alias='LOCALAPPDATA/FOX2/AgentBridge', current=current,
                installed_source_git_commit=receipt['manifest'].get('source_git_commit') if receipt else None,
                installed_manifest_sha256=hashlib.sha256(json.dumps(receipt['manifest'],sort_keys=True).encode()).hexdigest() if receipt else None,
                receipt_sha256=sha(BRIDGE/'versions'/current['package_sha256']/'receipt.json') if current else None,
                control=state, hashes=hashes, database_size=db.stat().st_size if db.is_file() else None,
                database_quick_check=integrity, dispatch_identity_state_digest=ledger_hash,
                dispatch_count=len(ledger), historical_consumed_states=consumed,
                owned_versions=sorted(p.name for p in (BRIDGE/'versions').iterdir()) if (BRIDGE/'versions').exists() else [],
                **observation)

def preflight():
    assert git('branch','--show-current') == 'work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021'
    assert git('rev-parse','HEAD') == START
    git('merge-base','--is-ancestor',BASE,START)
    assert not git('diff','--name-only',BASE,START,'--','agent_bridge')
    changed = git('diff','--name-only',BASE,START).splitlines()
    assert all('/host_lifecycle_cert/' in p or p.endswith('/preexec/host_lifecycle_cert_a01.json') for p in changed)
    assert git('status','--porcelain=v1','--untracked-files=all').splitlines() == ['?? '+(AREA/'observe.py').relative_to(ROOT).as_posix()]
    did = os.environ['FOX2_EXECUTABLE_DISPATCH_ID']
    dc = os.environ['FOX2_EXECUTABLE_DISPATCH_COMMIT']
    dp = 'docs/agent_handoff/DISPATCH/'+did+'.json'
    assert git('rev-parse',dc+':'+dp) == os.environ['FOX2_EXECUTABLE_DISPATCH_BLOB']
    assert git('rev-parse','FETCH_HEAD') == dc
    dispatch_raw = subprocess.check_output(['git','-C',str(ROOT),'show',dc+':'+dp])
    dispatch = json.loads(dispatch_raw)
    assert dispatch['runtime_contract']['base_sha'] == START and dispatch['max_runs']==1
    assert dispatch['source']['commit_sha'] == BASE and not dispatch['permissions']['code_allowed']
    assert git('ls-remote','--refs','origin','refs/heads/'+dispatch['runtime_contract']['branch']).split()[0] == START
    identities = {}
    for key, ckey in [('task','commit_sha'),('prompt','git_commit'),('policy','git_commit_sha'),('dictionary','git_commit_sha')]:
        entry=dispatch[key]; path=entry.get('path',entry.get('git_path')); commit=entry[ckey]
        raw=subprocess.check_output(['git','-C',str(ROOT),'show',commit+':'+path])
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], key
        if key in ('task','prompt'):
            assert (ROOT/path).read_bytes().replace(b'\r\n',b'\n') == raw
        identities[key] = dict(commit=commit,path=path,blob=git('rev-parse',commit+':'+path),sha256=hashlib.sha256(raw).hexdigest())
    prepath='reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a01.json'
    pre=json.loads((ROOT/prepath).read_text())
    assert pre['status']=='PASS' and pre['task_id']==os.environ['FOX2_TASK_ID'] and pre['source_code_base']==BASE
    assert git('rev-parse',START+':'+prepath)=='08056cb73333934a148cef2b4f1f3da11f6b9b3e'
    route = ps(r'''
    $procs=@(Get-CimInstance Win32_Process); $matching=@($procs | Where-Object {$_.Name -eq 'codex.exe' -and ([string]$_.CommandLine).Contains($env:FOX2_TASK_ID.Replace('-A01','').Replace('FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT','FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021'))});
    $writers=@($procs|Where-Object{$_.Name -eq 'codex.exe' -and ([string]$_.CommandLine).Contains(' exec ') -and ([string]$_.CommandLine).Contains('FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021')});
    $foreign=@($procs|Where-Object{$_.Name -eq 'codex.exe' -and ([string]$_.CommandLine).Contains(' exec ') -and ([string]$_.CommandLine -match 'G3-HOST|G4|CANARY')});
    $w=$writers|Select-Object -First 1;
    @{task_writer_count=$writers.Count; task_writer_pid=if($w){$w.ProcessId}else{$null};
      model_high_full_access=if($w){[bool]($w.CommandLine -match '--model gpt-6.1-sol' -and $w.CommandLine -match 'model_reasoning_effort=high' -and $w.CommandLine -match '--sandbox danger-full-access')}else{$false};
      active_g3_g4_canary_writers=$foreign.Count}|ConvertTo-Json -Compress
    ''')
    assert route['task_writer_count']==1 and route['model_high_full_access'] and route['active_g3_g4_canary_writers']==0
    bpython=Path(os.environ['FOX2_BOUND_BUILD_PYTHON'])
    spec=importlib.util.spec_from_file_location('accepted_builder',ROOT/'agent_bridge/scripts/build_user_package.py')
    builder=importlib.util.module_from_spec(spec); spec.loader.exec_module(builder)
    env=builder.inspect_build_environment(bpython)
    versions=json.loads(run([bpython,'-I','-c','import sys,importlib.metadata as m,json; print(json.dumps(dict(version=sys.version.split()[0],pip=m.version("pip"),build=m.version("build"))))']))
    assert env['python']=='3.13' and env['setuptools']=='84.0.0' and env['wheel']=='0.48.0'
    assert versions['pip']=='26.2.1' and versions['build']=='1.6.1'
    assert run(['dotnet','--version'])=='8.0.426'
    capabilities=dict(build_python_alias='WORKTREES/FOX2-BRIDGE-DESKTOP-BATCH-B/agent_bridge/.build-venv/Scripts/python.exe',build_environment=env,build_tools=versions,
        git=run(['git','--version']),python=run([sys.executable,'--version']),codex=run(['codex','--version']),dotnet=run(['dotnet','--version']),pwsh=run([PWSH,'-NoProfile','-Command','$PSVersionTable.PSVersion.ToString()']))
    before=snapshot()
    assert before['control']['state']=='STOPPED' and before['control']['paused'] and before['control']['setup_complete']
    assert not before['control']['active_dispatch_present'] and before['active_runtime_processes']==0
    assert before['database_quick_check']=='ok'
    for version in before['owned_versions']:
        assert len(version)==64 and (BRIDGE/'versions'/version/'receipt.json').is_file()
    # Admission marker is exclusive and is not a Bridge/package mutation.
    marker=Path(os.environ['TEMP'])/(did+'.consumed')
    with marker.open('x',encoding='utf-8') as stream:
        stream.write(now()+'\n')
    save('pre_state.json',before)
    save('source_binding.json',dict(observed_at_utc=now(),status='PASS',accepted_source=BASE,start_head=START,
        dispatch_id=did,dispatch_commit=dc,dispatch_blob=os.environ['FOX2_EXECUTABLE_DISPATCH_BLOB'],dispatch_sha256=hashlib.sha256(dispatch_raw).hexdigest(),
        remote_readback='fetch exact dispatch commit and ls-remote exact task branch before build',identities=identities,
        preexec_blob=git('rev-parse',START+':'+prepath),preexec_checked_at=pre['checked_at'],route=route,capabilities=capabilities,
        clean_before_evidence=True,only_observer_added_after_initial_clean_check=True,prestart_paths=changed,
        source_bytes_verified=True,authority='Owner task plus exact Dispatch and task-specific CHAT PASS_TO_ASSIGN 185f4cdcdfb6a7487f8bbc0f256c304fb1d9f263; scoped TEST only',
        global_release_effective='NOT_CLAIMED',dispatch_consumed=True,old_dispatch_replay=False,host_mutation_performed=False))
    print('SOURCE/REMOTE/DISPATCH/PREEXEC/ONE_WRITER/CAPABILITIES/HOST_PRESTATE=PASS')

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='preflight':
        preflight()
    else:
        save(sys.argv[1] if len(sys.argv)>1 else 'final_state.json', snapshot())
        print('BOUNDED_HOST_SNAPSHOT=RECORDED')
