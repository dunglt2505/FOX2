"""Single-use 007 disposable lifecycle. Never operates on the real Bridge root."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
STAGE = 'PACKAGE'
REAL = Path.home() / 'AppData/Local/FOX2/AgentBridge'
PW = shutil.which('pwsh')
IDS = ['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-' + f'{i:03}' for i in range(1, 8)]


def save(name, value):
    (EV/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8', newline='\n')


def stage(name):
    global STAGE
    STAGE = name
    save('progress.json', dict(stage=name, real_runtime_touched=False))
    print(name, flush=True)


def run(args, *, env, timeout=180):
    try:
        r = subprocess.run([str(a) for a in args], cwd=ROOT, env=env, capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=timeout,
                           creationflags=subprocess.CREATE_NO_WINDOW)
    except subprocess.TimeoutExpired:
        save('command_failure.json', dict(stage=STAGE, classification='TIMEOUT', timeout=timeout))
        raise RuntimeError('bounded command timeout') from None
    if r.returncode:
        save('command_failure.json', dict(stage=STAGE, exit_code=r.returncode,
             stdout_sha256=hashlib.sha256(r.stdout.encode()).hexdigest(),
             stderr_sha256=hashlib.sha256(r.stderr.encode()).hexdigest(),
             module_not_found='ModuleNotFoundError' in r.stderr,
             sanitized_install_failure='installation subprocess failed' in r.stderr,
             classification='COMMAND_NONZERO'))
        raise RuntimeError('bounded command failed: exit ' + str(r.returncode))
    return r.stdout


def main():
    assert (EV/'claim.json').is_file()
    tests = json.loads((EV/'tests.json').read_text())
    assert tests['full_exit'] == tests['focused_exit'] == 0
    with (EV/'lifecycle_claim.json').open('x', encoding='utf-8') as f:
        json.dump(dict(single_use=True, retry_allowed=False), f)
    temp = Path(tempfile.mkdtemp(prefix='fox2-core007-', dir='C:/Temp'))
    profile = temp/'user'
    isolated = profile/'AppData/Local/FOX2/AgentBridge'
    assert not isolated.resolve().is_relative_to(REAL.resolve())
    assert not REAL.resolve().is_relative_to(isolated.resolve())
    assert not any(p.is_symlink() or p.is_junction() for p in (temp, *temp.parents))
    profile.mkdir()
    (profile/'AppData/Local').mkdir(parents=True)
    (temp/'tmp').mkdir()
    old = json.loads((EV.parent/'core006/build_environment.json').read_text())
    bp = Path(old['venv'])/'Scripts/python.exe'
    assert bp.is_file()
    clean = {k: v for k, v in os.environ.items() if k.upper() not in ('PYTHONPATH', 'PYTHONHOME')}
    clean['PYTHONDONTWRITEBYTECODE'] = '1'
    # Reuse the provisioned build interpreter read-only; installation stays offline.
    save('build_environment.json', dict(provisioned_interpreter=str(bp),
         versions=old['versions'], host_environment_modified=False, existing_build_venv_modified=False))
    for n in (1, 2):
        run([bp, '-B', ROOT/'agent_bridge/scripts/build_user_package.py', '--output', temp/f'package{n}.zip',
             '--build-python', bp], env=clean, timeout=240)
    first = json.loads((temp/'package1.json').read_text())
    second = json.loads((temp/'package2.json').read_text())
    assert first['sha256'] == second['sha256']
    assert (temp/'package1.zip').read_bytes() == (temp/'package2.zip').read_bytes()
    save('package.json', dict(first=first, second_sha256=second['sha256'], byte_identical=True,
         package_path=str(temp/'package1.zip')))
    env = {**clean, 'USERPROFILE': str(profile), 'HOME': str(profile),
           'LOCALAPPDATA': str(profile/'AppData/Local'), 'APPDATA': str(profile/'AppData/Roaming'),
           'TEMP': str(temp/'tmp'), 'TMP': str(temp/'tmp'),
           'CODEX_HOME': os.environ.get('CODEX_HOME', str(Path.home()/'.codex')),
           'PYTHONPATH': str(ROOT/'agent_bridge/src'), 'PYTHONHOME': sys.base_prefix,
           'FOX2_INSTALL_SENTINEL': 'core007-non-python-environment'}
    save('isolation.json', dict(disposable_profile=str(profile), disposable_runtime=str(isolated),
         real_runtime_touched=False, roots_disjoint=True, contaminated_parent=dict(
             PYTHONPATH=env['PYTHONPATH'], PYTHONHOME=env['PYTHONHOME']),
         contamination='source path plus explicit base interpreter home; retained for entire lifecycle'))
    package = temp/'package1.zip'
    sha = first['sha256']

    def install_from_package(path, identity):
        # The production installer is imported from the verified package's wheel.
        # Observe its real subprocess boundary without replacing any execution.
        code = '''import hashlib,io,json,os,subprocess,sys,zipfile
from pathlib import Path
p=Path(PACKAGE); identity=IDENTITY
assert hashlib.sha256(p.read_bytes()).hexdigest()==identity
with zipfile.ZipFile(p) as z:
    wheel=next(n for n in z.namelist() if n.startswith('wheels/fox2_agent_bridge-'))
    w=Path(WHEEL); w.write_bytes(z.read(wheel))
sys.path.insert(0,str(w))
from fox2_agent_bridge import installation as m
assert m.BRIDGE_ROOT.resolve()==Path(ISOLATED).resolve()
assert os.environ['PYTHONPATH'] and os.environ['PYTHONHOME']
original=subprocess.run; calls=[]
def observed(args,**kwargs):
    e=kwargs['env']
    assert not {'PYTHONPATH','PYTHONHOME'} & {k.upper() for k in e}
    assert e['FOX2_INSTALL_SENTINEL']=='core007-non-python-environment'
    r=original(args,**kwargs)
    calls.append({'arguments':args,'exit_code':r.returncode,'python_paths_absent':True,'ordinary_environment_preserved':True})
    return r
subprocess.run=observed
result=m.install(p,identity)
assert len(calls)==3 and calls[0]['arguments'][1:3]==['-m','venv']
assert '--no-index' in calls[1]['arguments'] and '--isolated' in calls[1]['arguments']
assert calls[2]['arguments'][1:3]==['-I','-c']
print(json.dumps({'result':result,'subprocesses':calls}))
'''.replace('PACKAGE', repr(str(path))).replace('IDENTITY', repr(identity)).replace('WHEEL', repr(str(temp/'installer.whl'))).replace('ISOLATED', repr(str(isolated)))
        return json.loads(run([sys.executable, '-I', '-B', '-c', code], env=env))

    stage('PER_USER_INSTALL')
    initial = install_from_package(package, sha)
    assert initial['result']['status'] == 'INSTALLED'
    ip = isolated/'versions'/sha/'runtime/Scripts/python.exe'
    # Initialize only the new disposable ledger, preventing any legacy migration.
    (isolated/'data/manual_consumption.json').write_text(json.dumps(dict(
        format='FOX2_MANUAL_CONSUMPTION_1', dispatch_ids=IDS)), encoding='utf-8')
    run([ip, '-I', '-c', 'from fox2_agent_bridge.ledger import SQLiteLedger; '
         'from fox2_agent_bridge.paths import BRIDGE_ROOT; SQLiteLedger(BRIDGE_ROOT/"data/bridge.db").initialize()'], env=env)

    def cli(*args):
        return json.loads(run([ip, '-I', '-m', 'fox2_agent_bridge', *args], env=env, timeout=90))

    stage('FIRST_RUN_SETUP')
    setup = cli('setup')
    assert setup['paused'] is True
    config = (isolated/'config/bridge.toml').read_bytes()
    assert cli('setup')['paused'] is True
    assert (isolated/'config/bridge.toml').read_bytes() == config
    save('install_setup.json', dict(install=initial, setup=setup, repeated_setup_preserved_config=True))
    stage('UPDATE_PATH')
    update = temp/'update.zip'
    with zipfile.ZipFile(package) as src, zipfile.ZipFile(update, 'w', compression=zipfile.ZIP_STORED) as dst:
        for item in src.infolist():
            dst.writestr(item.filename, src.read(item.filename))
    updated_sha = hashlib.sha256(update.read_bytes()).hexdigest()
    updated = install_from_package(update, updated_sha)
    assert updated['result']['status'] == 'UPDATED'
    ip = isolated/'versions'/updated_sha/'runtime/Scripts/python.exe'
    assert cli('setup')['paused'] is True
    assert (isolated/'config/bridge.toml').read_bytes() == config
    save('update.json', dict(update=updated, variant='identical verified payload in byte-distinct ZIP_STORED archive',
         previous_version_retained=(isolated/'versions'/sha).is_dir(), config_preserved=True))

    def no_replay():
        code = '''import json
from fox2_agent_bridge.config import load_config
from fox2_agent_bridge.desktop import initialize_runtime
from fox2_agent_bridge.ledger import utc_now
l=initialize_runtime(load_config())
ids=IDS
assert all(not l.claim_dispatch(dispatch_id=i,payload_hash='a'*64,execution_id='must-not-execute',observed_at_utc=utc_now()) for i in ids)
assert l.pending_executions()==()
print(json.dumps({'blocked':ids,'pending_executions':0}))'''.replace('IDS', repr(IDS))
        return json.loads(run([ip, '-I', '-c', code], env=env))

    def tray_cycle(label):
        stage(label)
        tray = ip.parents[2]/'payload/scripts/desktop_tray.ps1'
        launcher = tray.with_name('desktop_launcher.ps1')
        count_env = {**env, 'FOX2_CORE007_TRAY': str(tray)}
        def count():
            return int(run([PW, '-NoProfile', '-Command',
                "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pwsh.exe' -and $_.CommandLine -and $_.CommandLine.Contains($env:FOX2_CORE007_TRAY) }).Count"], env=count_env).strip())
        assert count() == 0
        try:
            for _ in range(2):
                run([PW, '-NoProfile', '-NonInteractive', '-WindowStyle', 'Hidden', '-STA', '-File', launcher], env=env, timeout=20)
            deadline = time.monotonic()+45
            while time.monotonic() < deadline:
                state = cli('control', 'status')
                if state.get('state') == 'PAUSED' and state.get('heartbeat') and count() == 1:
                    break
                time.sleep(1)
            else:
                raise RuntimeError('disposable Tray/Worker health failed')
            duplicate = subprocess.run([str(ip), '-I', '-m', 'fox2_agent_bridge', 'worker'], env=env,
                capture_output=True, text=True, timeout=20, creationflags=subprocess.CREATE_NO_WINDOW)
            assert duplicate.returncode != 0 and 'LOCK_HELD' in duplicate.stderr
            result = dict(state=state['state'], heartbeat=state['heartbeat'], tray_count=1,
                 launches=2, duplicate_worker='LOCK_HELD', startup_entrypoint='installed desktop_launcher.ps1',
                 login_task_registration='not changed in disposable profile; host SID namespace is shared')
        finally:
            cli('control', 'request-exit')
            deadline = time.monotonic()+40
            while time.monotonic() < deadline and count():
                time.sleep(1)
            assert count() == 0, 'disposable tray did not exit'
        assert cli('control', 'status')['state'] == 'STOPPED'
        run([ip, '-I', '-c', 'from fox2_agent_bridge.process_lock import ProcessLock; '
             'from fox2_agent_bridge.paths import BRIDGE_ROOT;\nwith ProcessLock(BRIDGE_ROOT/"data/bridge.lock"): print("LOCK_RELEASED")'], env=env)
        result.update(graceful_exit=True, worker_lock_released=True)
        save(label.lower()+'.json', result)

    tray_cycle('STARTUP_SINGLE_INSTANCE_TRAY_WORKER')
    stage('SANITIZED_DIAGNOSTICS_BUNDLE')
    support_path = temp/'support.zip'
    diagnostic = cli('diagnostics', '--output', str(support_path))
    with zipfile.ZipFile(support_path) as z:
        assert z.namelist() == ['support.json']
        support = json.loads(z.read('support.json'))
    save('diagnostics.json', dict(result=diagnostic, whitelist_payload=support))
    no_replay()
    # The startup disable called by uninstall must have no host task to remove.
    absent = run([PW, '-NoProfile', '-Command',
        "$i=[Security.Principal.WindowsIdentity]::GetCurrent(); if (Get-ScheduledTask -TaskName ('FOX2Bridge-'+$i.User.Value) -ErrorAction SilentlyContinue) { exit 17 }; 'ABSENT'"], env=env)
    assert absent.strip() == 'ABSENT'
    durable = {'config/bridge.toml': config, 'data/manual_consumption.json': (isolated/'data/manual_consumption.json').read_bytes()}
    for name in ('data/core007-preserve.txt', 'logs/core007-preserve.txt', 'reports/core007-preserve.txt'):
        p = isolated/name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b'core007 durable preservation fixture\n')
        durable[name] = p.read_bytes()
    stage('UNINSTALL_PATH')
    removed = cli('uninstall')
    assert removed['status'] == 'UNINSTALLED'
    assert not (isolated/'current.json').exists()
    assert not any((isolated/'versions').iterdir())
    assert all((isolated/p).read_bytes() == raw for p, raw in durable.items())
    assert (isolated/'data/bridge.db').is_file()
    save('uninstall.json', dict(result=removed, no_deferred_uninstall=True, versions_empty=True,
         durable_files_preserved=True, host_startup_task_absent_before_uninstall=True))
    stage('REINSTALL_DURABLE_PRESERVATION')
    reinstalled = install_from_package(package, sha)
    ip = isolated/'versions'/sha/'runtime/Scripts/python.exe'
    assert cli('setup')['paused'] is True
    assert all((isolated/p).read_bytes() == raw for p, raw in durable.items())
    for _ in range(2):
        blocked = no_replay()
    save('reinstall.json', dict(install=reinstalled, durable_files_preserved=True, restart_no_replay=blocked, fresh_processes=2))
    tray_cycle('RESTART_NO_REPLAY')
    blocked = no_replay()
    save('isolated_summary.json', dict(status='PASS', all_required_isolated_gates_pass=True,
         package_sha256=sha, disposable_root=str(isolated),
         contaminated_parent_retained_for_entire_lifecycle=True,
         no_replay=blocked, real_runtime_touched=False,
         startup_scope='normal installed entrypoint and single-instance; actual host logon task deferred to conditional real certification'))
    stage('ISOLATED_LIFECYCLE_PASS')


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        save('stop.json', dict(status='STOPPED_NEEDS_RECONCILIATION', stage=STAGE,
             error_type=type(exc).__name__, detail=str(exc) if isinstance(exc, (RuntimeError, AssertionError)) else 'bounded lifecycle error',
             dispatch_consumed=True, no_retry=True, real_runtime_touched=False))
        print('STOPPED_NEEDS_RECONCILIATION: ' + STAGE, flush=True)
        sys.exit(1)
