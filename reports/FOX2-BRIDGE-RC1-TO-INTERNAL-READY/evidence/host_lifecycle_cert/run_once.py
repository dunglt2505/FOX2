"""Task-scoped one-shot orchestrator. No product changes and no lifecycle/uninstall retries."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import traceback
import observe

AREA=Path(__file__).resolve().parent
ROOT=observe.ROOT
STAGE=Path(r'C:\Projects\FOX2-builds\HLC-A01-353ca164')
PACKAGE=STAGE/'accepted-package.zip'
RAW=STAGE/'lifecycle-raw.json'
CHECKS=json.loads((AREA/'package_verification.json').read_text())
SHA=CHECKS['package_sha256']
record=dict(started_at_utc=observe.now(),package_sha256=SHA,install_attempts=0,lifecycle_attempts=0,
            stable_uninstall_attempts=0,recovery_attempts=0,status='STARTING',first_failure=None)

def clean(value):
    if isinstance(value,dict): return {k:clean(v) for k,v in value.items()}
    if isinstance(value,list): return [clean(v) for v in value]
    if not isinstance(value,str): return value
    pairs=[(str(observe.BRIDGE),'BridgeRoot'),(str(STAGE),'BUILD_ROOT'),(str(ROOT),'WORKTREE'),(os.environ['USERPROFILE'],'USERPROFILE')]
    for source,target in pairs:
        value=re.sub(re.escape(source),lambda _:target,value,flags=re.I)
        value=re.sub(re.escape(source.replace('\\','/')),lambda _:target,value,flags=re.I)
    value=re.sub(r'(?i)(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,})','<REDACTED>',value)
    value=re.sub(r'(?i)https?://[^\s/]+:[^\s/]+@','<REDACTED_URL>@',value)
    return value

def checkpoint():
    observe.save('execution.json',clean(record))

def command(args,timeout):
    proc=subprocess.run(list(map(str,args)),capture_output=True,text=True,errors='replace',timeout=timeout,
        env={k:v for k,v in os.environ.items() if k.upper() not in {'PYTHONPATH','PYTHONHOME'}},
        creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    return dict(exit_code=proc.returncode,stdout=clean(proc.stdout)[-8192:],stderr=clean(proc.stderr)[-8192:])

def install():
    assert hashlib.sha256(PACKAGE.read_bytes()).hexdigest()==SHA
    return command([observe.PWSH,'-NoProfile','-NonInteractive','-File',ROOT/'agent_bridge/scripts/install_user.ps1',
        '-Package',PACKAGE,'-Sha256',SHA,'-Python',sys.executable],300)

def persist_raw():
    if RAW.is_file():
        raw=RAW.read_bytes()
        data=json.loads(raw)
        observe.save('lifecycle.json',clean(data))
        record['raw_lifecycle_sha256']=hashlib.sha256(raw).hexdigest()
        record['evidence_normalization']='Recursive replacement of BridgeRoot, build/worktree and user-profile paths; credential patterns redacted. Raw evidence retained outside Git.'
        record['stable_uninstall_attempts']=1 if 'uninstall' in data else 0
        return data
    return None

def verify_installed(snapshot):
    assert snapshot['current']['package_sha256']==SHA
    assert snapshot['installed_source_git_commit']==observe.BASE
    assert snapshot['control']['paused'] and snapshot['control']['setup_complete']
    assert snapshot['control']['state']=='STOPPED' and snapshot['active_runtime_processes']==0
    assert not snapshot['control']['active_dispatch_present']

assert not (AREA/'execution.json').exists(), 'One-shot execution marker exists; no replay'
assert not RAW.exists()
assert observe.git('rev-parse','HEAD')==observe.START
assert not observe.git('diff','--name-only',observe.BASE,'HEAD','--','agent_bridge')
assert hashlib.sha256(PACKAGE.read_bytes()).hexdigest()==SHA
pre=observe.snapshot(); baseline=json.loads((AREA/'pre_install_state.json').read_text())
assert pre['hashes']==baseline['hashes'] and pre['current']==baseline['current']
assert pre['control']['state']=='STOPPED' and pre['control']['paused'] and pre['control']['setup_complete']
assert not pre['control']['active_dispatch_present'] and pre['active_runtime_processes']==0
record['status']='INSTALL_STARTED'; record['install_attempts']=1; checkpoint()
try:
    record['install']=install(); checkpoint()
    assert record['install']['exit_code']==0, 'supported per-user install failed'
    installed=observe.snapshot(); observe.save('post_install_state.json',installed)
    verify_installed(installed)
    assert installed['hashes']['config/bridge.toml']==baseline['hashes']['config/bridge.toml']
    assert installed['hashes']['data/manual_consumption.json']==baseline['hashes']['data/manual_consumption.json']
    record['status']='LIFECYCLE_STARTED'; record['lifecycle_attempts']=1; checkpoint()
    result=command([sys.executable,'-B',ROOT/'agent_bridge/scripts/certify_user_lifecycle.py',
        '--package',PACKAGE,'--sha256',SHA,'--evidence',RAW],600)
    record['lifecycle_process']=result
    lifecycle=persist_raw(); checkpoint()
    assert result['exit_code']==0, 'corrected lifecycle failed; no retry'
    assert lifecycle and lifecycle['uninstall']['status']=='UNINSTALLED'
    assert lifecycle['uninstall']['exit_code']==0
    assert all(lifecycle['uninstall']['post_uninstall'].values())
    assert lifecycle['reinstall']['package_sha256']==SHA
    assert lifecycle['reinstalled_setup']['status']=='SETUP_COMPLETE'
    assert lifecycle['configuration_preserved']
    final=observe.snapshot(); observe.save('final_state.json',final)
    verify_installed(final)
    assert final['database_quick_check']=='ok'
    assert final['dispatch_identity_state_digest']==baseline['dispatch_identity_state_digest']
    assert final['historical_consumed_states']==baseline['historical_consumed_states']
    assert final['hashes']['config/bridge.toml']==baseline['hashes']['config/bridge.toml']
    assert final['hashes']['data/manual_consumption.json']==baseline['hashes']['data/manual_consumption.json']
    record['status']='PASS'
except Exception as error:
    record['status']='FAIL'
    record['first_failure']=dict(type=type(error).__name__,message=clean(str(error))[:4096],observed_at_utc=observe.now(),
        traceback=clean(traceback.format_exc())[-8192:])
    persist_raw(); checkpoint()
    current=observe.BRIDGE/'current.json'
    unavailable=not current.is_file()
    if current.is_file():
        pointer=json.loads(current.read_text())
        unavailable=not (observe.BRIDGE/'versions'/pointer['package_sha256']/'runtime/Scripts/python.exe').is_file()
    if record['lifecycle_attempts']==1 and unavailable:
        record['recovery_attempts']=1; checkpoint()
        record['recovery']=install(); checkpoint()
    # Recovery never alters the first lifecycle verdict.
    try: observe.save('final_state.json',observe.snapshot())
    except Exception as observation_error:
        record['final_observation_error']=clean(str(observation_error))[:1000]
finally:
    record['finished_at_utc']=observe.now(); checkpoint()
print('HOST_LIFECYCLE='+record['status'])
print('INSTALL_ATTEMPTS='+str(record['install_attempts'])+'; LIFECYCLE_ATTEMPTS='+str(record['lifecycle_attempts'])+'; STABLE_UNINSTALL_ATTEMPTS='+str(record['stable_uninstall_attempts'])+'; RECOVERY_ATTEMPTS='+str(record['recovery_attempts']))
