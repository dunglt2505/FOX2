"""Single-use ownership-proven real recovery after the complete disposable PASS."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
STAGE = 'REAL_OWNERSHIP_VALIDATION'
MUTATED = False
PW = shutil.which('pwsh')
IDS = ['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+f'{i:03}' for i in range(1, 9)]


def save(name, value):
    (EV/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8')


def stage(value):
    global STAGE
    STAGE = value
    save('real_progress.json', dict(stage=value, real_root_mutated=MUTATED))
    print(value, flush=True)


def run(args, env, timeout=90):
    r = subprocess.run([str(a) for a in args], cwd=ROOT, env=env, capture_output=True,
        text=True, encoding='utf-8', errors='replace', timeout=timeout,
        creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode:
        save('real_command_failure.json', dict(stage=STAGE, exit_code=r.returncode,
            stdout_sha256=hashlib.sha256(r.stdout.encode()).hexdigest(),
            stderr_sha256=hashlib.sha256(r.stderr.encode()).hexdigest()))
        raise RuntimeError('bounded real recovery command failed')
    return r.stdout


def main():
    global MUTATED
    isolated = json.loads((EV/'isolated_summary.json').read_text())
    assert isolated['status'] == 'PASS' and isolated['all_required_isolated_gates_pass']
    audit = json.loads((EV/'real_readonly_inventory.json').read_text())
    task = json.loads((EV/'real_readonly_task_process.json').read_text())
    real = Path.home()/'AppData/Local/FOX2/AgentBridge'
    assert real.resolve() == Path(audit['root']).resolve()
    assert not task['processes'] and not task['exists'], 'quarantine ownership state changed or requires separate reconciliation'
    assert audit['worker']['paused'] is True and audit['worker']['state'] == 'STOPPED'
    assert audit['all_paths_without_links']
    for p in (real, *real.parents, *real.rglob('*')):
        assert not p.is_symlink() and not p.is_junction()
    package_evidence = json.loads((EV/'package.json').read_text())
    package = Path(package_evidence['package_path'])
    sha = package_evidence['first']['sha256']
    assert hashlib.sha256(package.read_bytes()).hexdigest() == sha
    temp = package.parent
    wheel = temp/'real-installer.whl'
    with zipfile.ZipFile(package) as z:
        member = next(n for n in z.namelist() if n.startswith('wheels/fox2_agent_bridge-'))
        wheel.write_bytes(z.read(member))
    # Materialize certified resources outside versions so the startup script is
    # a real filesystem path even while reconciling a partial old runtime.
    external = temp/'real-external-installer'
    external.mkdir()
    with zipfile.ZipFile(wheel) as archive:
        for entry in archive.infolist():
            path = external/entry.filename
            assert path.resolve().is_relative_to(external.resolve())
            if not entry.is_dir():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(archive.read(entry.filename))
    sys.path.insert(0, str(external))
    from fox2_agent_bridge import installation as m
    from fox2_agent_bridge.artifacts import write_json
    assert m.safe_root(real) == real
    historical = json.loads((EV.parent/'dispatch_004_package.json').read_text())
    known = {historical['sha256'], historical['initial_baseline_install']}
    assert audit['current']['package_sha256'] in known
    assert set(p.name for p in (real/'versions').iterdir()) == {v['name'] for v in audit['versions']}
    ownership = []
    for version in audit['versions']:
        identity = version['name']
        target = m._version_path(real, identity)
        receipt = version['receipt']
        assert identity in known and receipt and receipt['package_sha256'] == identity
        assert target.resolve().parent == (real/'versions').resolve()
        assert receipt['manifest']['format'] == 'FOX2_USER_PACKAGE_1'
        assert receipt['manifest']['dictionary_sha256'] == m.registry.SOURCE_SHA256
        assert json.loads((target/'receipt.json').read_text()) == receipt
        for name, digest in version['files'].items():
            assert hashlib.sha256((real/name).read_bytes()).hexdigest() == digest
        for name, digest in receipt['manifest']['files'].items():
            p = target/'payload'/name
            if p.exists():
                assert hashlib.sha256(p.read_bytes()).hexdigest() == digest
        ownership.append(dict(identity=identity, historical_dispatch_004_package_binding=True,
            receipt_identity_and_manifest=True, contained_without_links=True,
            file_count=len(version['files']), partial=len(version['files']) == 5))
    assert (real/'launch.ps1').read_text() == m.LAUNCHER
    assert m.installed_version(real) == audit['current']
    # Recheck the exact shared scheduler identity immediately before mutation.
    env = {k:v for k,v in os.environ.items() if k.upper() not in ('PYTHONPATH','PYTHONHOME')}
    assert run([PW,'-NoProfile','-Command',
        "$i=[Security.Principal.WindowsIdentity]::GetCurrent(); if(Get-ScheduledTask -TaskName ('FOX2Bridge-'+$i.User.Value) -ErrorAction SilentlyContinue){exit 17}; 'ABSENT'"], env).strip() == 'ABSENT'
    save('real_ownership.json', dict(status='PASS', versions=ownership,
         current_and_launcher_owned=True, task_name=task['name'], sid=task['sid'],
         exact_startup_task_absent=True, no_version_executable_processes=True))
    with (EV/'real_recovery_claim.json').open('x', encoding='utf-8') as f:
        json.dump(dict(single_use=True, disposable_pass_required=True, retry_allowed=False), f)
    stage('REAL_DURABLE_PRESERVATION')
    backup = temp/'real-preservation'
    backup.mkdir()
    # Private local backup only. Raw configuration/ledger never enters Git evidence.
    for directory in ('config','logs','reports'):
        shutil.copytree(real/directory, backup/directory)
    (backup/'data').mkdir()
    for p in (real/'data').iterdir():
        if p.is_file() and p.name not in ('bridge.db','bridge.db-wal','bridge.db-shm') and p.suffix != '.lock':
            shutil.copy2(p, backup/'data'/p.name)
    with sqlite3.connect((real/'data/bridge.db').as_uri()+'?mode=ro', uri=True) as source:
        with sqlite3.connect(backup/'data/bridge.db') as destination:
            source.backup(destination)
        prior_rows = list(source.execute('SELECT dispatch_id,state,payload_hash,created_at_utc,updated_at_utc FROM dispatches ORDER BY dispatch_id'))
    stable = {name:digest for directory in ('config','logs','reports') for name,digest in audit['durable'][directory].items()}
    assert all(hashlib.sha256((real/name).read_bytes()).hexdigest() == digest for name,digest in stable.items())
    assert all(hashlib.sha256((backup/name).read_bytes()).hexdigest() == digest for name,digest in stable.items())
    manual = audit['manual_consumption']
    assert json.loads((real/'data/manual_consumption.json').read_text()) == manual
    # Preserve all original fields and identities; append the consumed 005-008.
    manual = {**manual, 'dispatch_ids': list(dict.fromkeys([*manual['dispatch_ids'], *IDS])),
              'additional_authority_control_commit_008': '737e9851b2367f5e2aeb6597d0445b6df0ffcc71'}
    MUTATED = True
    write_json(real/'data/manual_consumption.json', manual)
    stage('REAL_OWNED_PARTIAL_RECONCILIATION')
    removed = m.uninstall(root=real)  # external base process; never the partial interpreter
    assert removed['status'] == 'UNINSTALLED'
    assert not any((real/'versions').iterdir())
    assert not (real/'current.json').exists() and not (real/'launch.ps1').exists()
    assert all(hashlib.sha256((real/name).read_bytes()).hexdigest() == digest for name,digest in stable.items())
    save('real_reconciliation.json', dict(status='PASS', uninstall=removed,
        removed_owned_versions=[v['identity'] for v in ownership], versions_empty=True,
        current_and_launcher_removed=True, durable_original_hashes_preserved=True,
        private_local_backup=str(backup), manual_original_fields_preserved=True,
        manual_consumed_identities=manual['dispatch_ids']))
    stage('REAL_EXACT_CERTIFIED_INSTALL')
    installed = m.install(package, sha, root=real)
    assert installed['status'] == 'INSTALLED'
    ip = real/'versions'/sha/'runtime/Scripts/python.exe'
    def cli(*args):
        return json.loads(run([ip,'-I','-B','-m','fox2_agent_bridge',*args], env))
    setup = cli('setup')
    assert setup['paused'] is True
    assert cli('setup')['paused'] is True
    assert all(hashlib.sha256((real/name).read_bytes()).hexdigest() == digest for name,digest in stable.items())
    with sqlite3.connect((real/'data/bridge.db').as_uri()+'?mode=ro', uri=True) as db:
        rows = list(db.execute('SELECT dispatch_id,state,payload_hash,created_at_utc,updated_at_utc FROM dispatches ORDER BY dispatch_id'))
        assert set(prior_rows) <= set(rows)
    def no_replay():
        code = '''import json
from fox2_agent_bridge.config import load_config
from fox2_agent_bridge.desktop import initialize_runtime
from fox2_agent_bridge.ledger import utc_now
l=initialize_runtime(load_config())
ids=IDENTITIES
assert all(not l.claim_dispatch(dispatch_id=i,payload_hash='a'*64,execution_id='must-not-execute',observed_at_utc=utc_now()) for i in ids)
assert l.pending_executions()==()
assert l.worker_state()['paused'] is True
print(json.dumps({'blocked':ids,'pending_executions':0,'paused':True}))'''.replace('IDENTITIES', repr(IDS))
        return json.loads(run([ip,'-I','-B','-c',code], env))
    blocked = [no_replay(), no_replay()]
    save('real_install_setup.json', dict(install=installed, setup=setup,
        repeated_setup_idempotent=True, original_durable_hashes_preserved=True,
        all_original_dispatch_rows_byte_value_preserved=True, fresh_process_no_replay=blocked))
    stage('REAL_STARTUP_TASK_OWNERSHIP')
    # Absence was proved above; create only this user's exact named limited task.
    startup = cli('control','set-start-with-windows','--enabled','true')
    task_code = r'''$ErrorActionPreference='Stop'; $i=[Security.Principal.WindowsIdentity]::GetCurrent();
$t=Get-ScheduledTask -TaskName ('FOX2Bridge-'+$i.User.Value); $u=$t.Principal.UserId;
if($u -notlike 'S-1-*'){$u=([Security.Principal.NTAccount]::new($u)).Translate([Security.Principal.SecurityIdentifier]).Value};
@{sid=$i.User.Value;principal_sid=$u;name=$t.TaskName;run_level=[string]$t.Principal.RunLevel;logon_type=[string]$t.Principal.LogonType;
instances=[string]$t.Settings.MultipleInstances;actions=@($t.Actions|ForEach-Object{@{execute=$_.Execute;arguments=$_.Arguments}})}|ConvertTo-Json -Depth 5 -Compress'''
    def task_check():
        t = json.loads(run([PW,'-NoProfile','-Command',task_code], env))
        assert t['sid'] == t['principal_sid'] == task['sid'] and t['name'] == task['name']
        assert t['run_level'] == 'Limited' and t['logon_type'] == 'Interactive' and t['instances'] == 'IgnoreNew'
        assert t['actions'] == [dict(execute=PW, arguments='-NoProfile -NonInteractive -WindowStyle Hidden -STA -File "'+str(real/'launch.ps1')+'"')]
        return t
    registered = task_check()
    cli('control','set-start-with-windows','--enabled','true')
    assert task_check() == registered
    save('real_startup.json', dict(status='PASS', startup=startup, task=registered, repeated_enable_idempotent=True))
    tray = real/'versions'/sha/'payload/scripts/desktop_tray.ps1'
    process_env = {**env, 'FOX2_CORE008_TRAY':str(tray)}
    def count():
        return int(run([PW,'-NoProfile','-Command',
            "@(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pwsh.exe' -and $_.CommandLine -and $_.CommandLine.Contains($env:FOX2_CORE008_TRAY) }).Count"], process_env).strip())
    def cycle(label, keep=False):
        stage(label)
        assert count() == 0
        success = False
        try:
            for _ in range(2):
                run([PW,'-NoProfile','-NonInteractive','-WindowStyle','Hidden','-STA','-File',real/'launch.ps1'], env, timeout=20)
            deadline = time.monotonic()+45
            while time.monotonic() < deadline:
                state = cli('control','status')
                if state.get('state') == 'PAUSED' and state.get('heartbeat') and count() == 1:
                    break
                time.sleep(1)
            else:
                raise RuntimeError('real Tray/Worker health failed')
            duplicate = subprocess.run([str(ip),'-I','-m','fox2_agent_bridge','worker'],env=env,
                capture_output=True,text=True,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
            assert duplicate.returncode != 0 and 'LOCK_HELD' in duplicate.stderr
            result = dict(state='PAUSED', heartbeat=state['heartbeat'], tray_count=1,
                launches=2, duplicate_worker='LOCK_HELD', no_replay=no_replay())
            success = True
        finally:
            if not keep or not success:
                cli('control','request-exit')
                deadline = time.monotonic()+40
                while time.monotonic() < deadline and count():
                    time.sleep(1)
                assert count() == 0
                assert cli('control','status')['state'] == 'STOPPED'
                from fox2_agent_bridge.process_lock import ProcessLock
                with ProcessLock(real/'data/bridge.lock'):
                    pass
        result.update(left_running_paused=keep, graceful_exit_and_lock_release=not keep)
        save(label.lower()+'.json', result)
    cycle('REAL_INSTALLED_TRAY_WORKER')
    cycle('REAL_RESTART_NO_REPLAY', keep=True)
    stage('REAL_SANITIZED_DIAGNOSTICS')
    support = temp/'real-support.zip'
    diagnostic = cli('diagnostics','--output',support)
    with zipfile.ZipFile(support) as z:
        assert z.namelist() == ['support.json']
        summary = json.loads(z.read('support.json'))
    save('real_diagnostics.json', dict(result=diagnostic, whitelist_payload=summary))
    assert all(hashlib.sha256((real/name).read_bytes()).hexdigest() == digest for name,digest in stable.items())
    save('real_summary.json', dict(status='PASS', real_recovery_complete=True, package_sha256=sha,
        owned_partial_reconciled=True, durable_originals_preserved=True, all_prior_consumption_preserved=True,
        blocked_consumed_identities=IDS, state='PAUSED', tray_count=count(), startup_task_owned=True,
        complete_disposable_pass_before_any_real_mutation=True))
    stage('REAL_RECOVERY_PASS')


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        save('real_stop.json', dict(status='STOPPED_NEEDS_RECONCILIATION', stage=STAGE,
            error_type=type(error).__name__, real_root_mutated=MUTATED, no_retry=True,
            detail=str(error) if isinstance(error, (AssertionError, RuntimeError)) else 'bounded recovery failure'))
        print('STOPPED_NEEDS_RECONCILIATION: '+STAGE, flush=True)
        sys.exit(1)
