"""Windows host certification of an already installed, paused Bridge.

Uses the installed interpreter for control and the stable external PowerShell 7
supervisor for uninstall. Keeps durable data, then reinstalls the exact package.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from fox2_agent_bridge.artifacts import write_json
from fox2_agent_bridge.installation import install, installed_version, BRIDGE_ROOT
from fox2_agent_bridge.logging_config import redact_context


UNINSTALL_OUTPUT_LIMIT = 4096


def _uninstall_output(value):
    """Redact before truncation so a boundary cannot expose a partial secret."""
    if isinstance(value, bytes):
        value = value.decode('utf-8', errors='replace')
    value = redact_context(value or '')
    value = re.sub(r'(?i)https?://[^\s/]+:[^\s/]+@', '<REDACTED_URL>@', value)
    value = re.sub(
        r'''(?i)["']?(?:authorization|(?:access[_-]?|api[_-]?)?token|api[_-]?key|password|secret)["']?\s*[:=]\s*(?:"[^"\r\n]*"|'[^'\r\n]*'|[^\s,;}]+)''',
        '<REDACTED_FIELD>', value)
    value = ''.join(c for c in value if c in '\n\t' or ord(c) >= 32)
    return value[:UNINSTALL_OUTPUT_LIMIT]


def certify_uninstall(root, pwsh, config_before, results, evidence):
    """One synchronous attempt; checkpoint sanitized evidence before any reinstall."""
    supervisor = root / 'uninstall.ps1'
    versions = (root / 'versions').resolve()
    if (supervisor.resolve() != root.resolve() / 'uninstall.ps1' or
            Path(pwsh).resolve().is_relative_to(versions) or
            Path(sys.executable).resolve().is_relative_to(versions)):
        raise ValueError('lifecycle uninstall requires stable external supervisors')
    consumption = root / 'data/manual_consumption.json'
    consumption_before = consumption.read_bytes() if consumption.exists() else None
    result = {
        'supervisor': {'kind': 'STABLE_EXTERNAL_POWERSHELL7',
                       'path': 'BridgeRoot/uninstall.ps1', 'cwd': 'BridgeRoot',
                       'sha256': hashlib.sha256(supervisor.read_bytes()).hexdigest()},
        'exit_code': None, 'stdout': '', 'stderr': '', 'status': 'SUPERVISOR_FAILED',
    }
    try:
        process = subprocess.run(
            [str(pwsh), '-NoProfile', '-NonInteractive', '-File', str(supervisor)],
            cwd=root, capture_output=True, text=True, errors='replace', timeout=90,
            env={k: v for k, v in os.environ.items()
                 if k.upper() not in {'PYTHONPATH', 'PYTHONHOME'}},
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        result.update(exit_code=process.returncode,
                      stdout=_uninstall_output(process.stdout),
                      stderr=_uninstall_output(process.stderr))
    except subprocess.TimeoutExpired as error:
        result.update(status='SUPERVISOR_TIMEOUT', stdout=_uninstall_output(error.stdout),
                      stderr=_uninstall_output(error.stderr))
    except OSError:
        result['status'] = 'SUPERVISOR_START_FAILED'
    try:
        result['post_uninstall'] = {
            'current_pointer_absent': not (root / 'current.json').exists(),
            'versions_absent': not (root / 'versions').exists() or not any((root / 'versions').iterdir()),
            'configuration_preserved': (root / 'config/bridge.toml').read_bytes() == config_before,
            'database_preserved': (root / 'data/bridge.db').is_file(),
            'consumption_file_preserved': consumption_before is None or (
                consumption.is_file() and consumption.read_bytes() == consumption_before),
        }
    except OSError:
        result['post_uninstall'] = {'checks_unavailable': True}
    if result['exit_code'] == 0:
        checks = result['post_uninstall']
        result['status'] = ('UNINSTALLED' if 'checks_unavailable' not in checks and all(checks.values())
                            else 'POSTCONDITION_FAILED')
    results['uninstall'] = result
    write_json(evidence, results)
    if result['status'] != 'UNINSTALLED':
        raise RuntimeError('stable external uninstall failed; evidence persisted; no retry')
    return result


def main(package,sha,evidence):
    root=BRIDGE_ROOT
    current=installed_version(root)
    assert current and current['package_sha256']==sha
    python=root/'versions'/sha/'runtime/Scripts/python.exe'
    pwsh=r'C:\Program Files\PowerShell\7\pwsh.exe'
    results={}
    def cli(*args):
        r=subprocess.run([str(python),'-I','-m','fox2_agent_bridge',*args],capture_output=True,text=True,timeout=90)
        if r.returncode: raise RuntimeError('installed command failed: '+args[0]+' exit '+str(r.returncode))
        return json.loads(r.stdout)
    config_before=(root/'config/bridge.toml').read_bytes()
    state=cli('control','status')
    assert state['paused'] is True
    results['setup']=cli('setup')
    results['startup']=cli('control','set-start-with-windows','--enabled','true')
    inspect=r'''$Identity=[Security.Principal.WindowsIdentity]::GetCurrent();
    $Task=Get-ScheduledTask -TaskName ('FOX2Bridge-'+$Identity.User.Value);
    @{run_level=[string]$Task.Principal.RunLevel;logon_type=[string]$Task.Principal.LogonType;action=$Task.Actions.Arguments;instances=[string]$Task.Settings.MultipleInstances}|ConvertTo-Json -Compress'''
    r=subprocess.run([pwsh,'-NoProfile','-Command',inspect],capture_output=True,text=True,timeout=30)
    assert r.returncode==0
    task=json.loads(r.stdout); assert task['run_level']=='Limited' and task['logon_type']=='Interactive'
    assert 'launch.ps1' in task['action'] and task['instances']=='IgnoreNew'
    results['task_scheduler']={k:v for k,v in task.items() if k!='action'}
    tray=root/'versions'/sha/'payload/scripts/desktop_tray.ps1'
    launcher=tray.with_name('desktop_launcher.ps1')
    env={**os.environ,'FOX2_CERT_TRAY':str(tray)}
    def tray_count():
        r=subprocess.run([pwsh,'-NoProfile','-Command',
            "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pwsh.exe' -and $_.CommandLine -and $_.CommandLine.Contains($env:FOX2_CERT_TRAY) }).Count"],
            capture_output=True,text=True,timeout=15,env=env)
        assert r.returncode==0
        return int(r.stdout.strip())
    try:
        for _ in range(2):
            subprocess.run([pwsh,'-NoProfile','-NonInteractive','-WindowStyle','Hidden','-STA','-File',str(launcher)],
                capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW,check=True)
        deadline=time.monotonic()+45
        while time.monotonic()<deadline:
            state=cli('control','status')
            if state.get('state')=='PAUSED' and state.get('heartbeat') and tray_count()==1: break
            time.sleep(1)
        else: raise RuntimeError('installed tray/worker did not become healthy')
        results['installed_tray_worker']={'state':state['state'],'heartbeat':state['heartbeat'],
            'tray_processes':tray_count(),'two_launches':True,'source_pythonpath':'UNSET_BY_TRAY'}
        r=subprocess.run([str(python),'-I','-m','fox2_agent_bridge','worker'],capture_output=True,text=True,timeout=30)
        assert r.returncode!=0 and 'LOCK_HELD' in r.stderr
        results['single_instance']={'second_worker_exit':r.returncode,'second_worker':'LOCK_HELD'}
    finally:
        cli('control','request-exit')
        exit_started=time.monotonic()
        deadline=time.monotonic()+30
        while time.monotonic()<deadline and tray_count(): time.sleep(1)
        if tray_count(): raise RuntimeError('tray did not finish graceful exit')
        state=cli('control','status')
        assert state['state']=='STOPPED' and state['stop_requested'] is True
        from fox2_agent_bridge.process_lock import ProcessLock
        with ProcessLock(root/'data/bridge.lock'):
            results['graceful_exit']={'state':state['state'],'stop_requested':True,
                'tray_processes':0,'worker_lock_released':True,
                'elapsed_seconds':round(time.monotonic()-exit_started,3)}
    support=root/'reports/support-certification.zip'
    results['diagnostics']=cli('diagnostics','--output',str(support))
    results['startup_disabled']=cli('control','set-start-with-windows','--enabled','false')
    ids=['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+i for i in ('001','002','003','004')]
    before={i:cli('status','--dispatch-id',i)['dispatch']['dispatch_state'] for i in ids}
    certify_uninstall(root,pwsh,config_before,results,evidence)
    results['reinstall']=install(package,sha)
    results['reinstalled_setup']=cli('setup')
    after={i:cli('status','--dispatch-id',i)['dispatch']['dispatch_state'] for i in ids}
    assert before==after and all(s=='NEEDS_RECONCILIATION' for s in after.values())
    assert (root/'config/bridge.toml').read_bytes()==config_before
    results['durable_consumption']=after
    results['configuration_preserved']=True
    results['runtime']='PER_USER_OFFLINE_VENV'
    write_json(evidence,results)
    print('USER_LIFECYCLE=PASS')


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--package',type=Path,required=True)
    p.add_argument('--sha256',required=True); p.add_argument('--evidence',type=Path,required=True)
    a=p.parse_args(); main(a.package,a.sha256,a.evidence)
