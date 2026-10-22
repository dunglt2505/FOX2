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


def require_safe_control(state, *, stopped=False):
    if (state.get('paused') is not True or state.get('setup_complete') is not True or
            'current_dispatch' not in state or state['current_dispatch'] is not None or
            (stopped and state.get('state') != 'STOPPED')):
        raise RuntimeError('Phase-2 requires paused/setup_complete/no current dispatch')


def certify_presentation(root, sha, pwsh, cli, results, evidence):
    """Observe only WPF presentation; protected Worker/F1 belongs to G3/G4."""
    env = {k: v for k, v in os.environ.items()
           if k.upper() not in {'PYTHONPATH', 'PYTHONHOME'}}
    expected = root / 'versions' / sha / 'payload/desktop/FOX2.Bridge.Desktop.exe'
    lock = root.parent / 'BridgeDesktop/desktop.lock'
    results['worker_f1_health'] = 'NOT_APPLICABLE_PRE_G3'

    def ps(*args, timeout=30):
        process = subprocess.run([str(pwsh), '-NoProfile', '-NonInteractive', *args],
            capture_output=True, text=True, timeout=timeout, env=env,
            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        if process.returncode:
            raise RuntimeError('WPF presentation certification command failed')
        return process.stdout.strip()

    def presentations():
        observed = json.loads(ps('-Command',
            "$ErrorActionPreference='Stop'; "
            "ConvertTo-Json -Compress -InputObject @(Get-CimInstance Win32_Process "
            "-Filter \"Name='FOX2.Bridge.Desktop.exe'\" | "
            "Select-Object ProcessId,ExecutablePath)"))
        if not isinstance(observed, list):
            raise RuntimeError('WPF process observation must be an explicit array')
        return observed

    def exact_presentation():
        observed = presentations()
        if len(observed) != 1:
            return None
        record = observed[0]
        if (not record.get('ExecutablePath') or
                Path(record['ExecutablePath']).resolve() != expected.resolve() or
                not expected.is_file() or installed_version(root)['package_sha256'] != sha):
            raise RuntimeError('WPF presentation is not the exact current package')
        return record

    def wait_for(predicate, label, seconds=45):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            value = predicate()
            if value:
                return value
            time.sleep(0.5)
        raise RuntimeError(label)

    def ui(action):
        return ps('-File', str(Path(__file__).with_name('certify_rc1_ui.ps1')),
                  '-Action', action)

    try:
        require_safe_control(cli('control', 'status'))
        for _ in range(2):
            ps('-WindowStyle', 'Hidden', '-File', str(root / 'launch.ps1'), timeout=120)
        live = wait_for(exact_presentation, 'Expected exactly one current WPF presentation')
        # WPF opens this existing file with FileShare.None. Never alter its bytes.
        if not lock.is_file():
            raise RuntimeError('Live WPF presentation lock is missing')
        try:
            with lock.open('r+b'):
                pass
        except OSError as error:
            if getattr(error, 'winerror', None) != 32:
                raise
            results['live_presentation_lock_held'] = True
        else:
            raise RuntimeError('Live WPF presentation lock is not held')
        screens = json.loads(ui('inspect'))
        if (screens.get('screens') != ['Dashboard', 'Activity', 'Agents', 'Diagnostics', 'Artifacts', 'Settings'] or
                screens.get('process_id') != live['ProcessId'] or
                screens.get('check_now_enabled') is not False):
            raise RuntimeError('Current WPF navigation/paused control proof failed')
        if ui('check') != 'PAUSED_CHECK_DISABLED':
            raise RuntimeError('Paused Check Now proof failed')
        require_safe_control(cli('control', 'status'))
        if exact_presentation() != live:
            raise RuntimeError('WPF presentation changed before explicit exit')
        results['presentation'] = {'two_launches': True, 'count': 1,
            'package_sha256': sha, 'process_id': live['ProcessId'],
            'executable': str(expected), 'screens': screens['screens'],
            'paused_check_now': 'DISABLED'}
        write_json(evidence, results)
        exit_started = time.monotonic()
        if ui('exit') != 'EXIT_INVOKED':
            raise RuntimeError('Explicit WPF exit was not invoked')
        wait_for(lambda: not presentations(), 'WPF did not finish graceful exit', seconds=30)
        with lock.open('r+b'):
            results['presentation_lock_released'] = True
        state = cli('control', 'status')
        require_safe_control(state, stopped=True)
        results['graceful_exit'] = {'state': state['state'], 'paused': True,
            'setup_complete': True, 'current_dispatch': None, 'presentation_count': 0,
            'explicit_ui_exit': True, 'elapsed_seconds': round(time.monotonic() - exit_started, 3)}
        write_json(evidence, results)
    except Exception:
        results['presentation_status'] = 'FAILED_BEFORE_UNINSTALL'
        write_json(evidence, results)
        raise


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
    require_safe_control(state)
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
    certify_presentation(root,sha,pwsh,cli,results,evidence)
    support=root/'reports/support-certification.zip'
    results['diagnostics']=cli('diagnostics','--output',str(support))
    results['startup_disabled']=cli('control','set-start-with-windows','--enabled','false')
    ids=['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+i for i in ('001','002','003','004')]
    before={i:cli('status','--dispatch-id',i)['dispatch']['dispatch_state'] for i in ids}
    certify_uninstall(root,pwsh,config_before,results,evidence)
    results['reinstall']=install(package,sha)
    results['reinstalled_setup']=cli('setup')
    assert installed_version(root)['package_sha256']==sha
    require_safe_control(cli('control','status'), stopped=True)
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
