"""Single-use Core 006 harness. Never invoke uninstall or the real runtime."""
import datetime, hashlib, json, os, shutil, subprocess, sys, tempfile, time, zipfile
from pathlib import Path

ROOT = Path(r'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B')
OUT = ROOT / 'reports/BRIDGE-DESKTOP-BATCH-B'
EV = OUT / 'evidence/core006'
BASE = '28550c49f07075c80cd730da9be80c72e5bc5e76'
CONTROL = 'fa262cebc3965a1c32042aceb4742326a4533ed7'
BRANCH = 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
ID = 'FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-006'
sys.path.insert(0, str(ROOT / 'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import writer_lock, competing_writer
from fox2_agent_bridge.preexec.probes import agent_probe, tool_probe
from jsonschema import Draft202012Validator, FormatChecker

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def save(name, value):
    EV.mkdir(parents=True, exist_ok=True)
    (EV/name).write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8', newline='\n')

def run(args, *, env=None, timeout=180, cwd=ROOT):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, encoding='utf-8', errors='replace', env=env, timeout=timeout, cwd=cwd, creationflags=subprocess.CREATE_NO_WINDOW)
    if r.returncode:
        raise RuntimeError('command failed: '+str(args[0])+' '+str(args[1:3])+' exit '+str(r.returncode))
    return r.stdout

def main():
    with writer_lock(ROOT):
        assert git('rev-parse','HEAD').decode().strip() == BASE
        assert git('branch','--show-current').decode().strip() == BRANCH
        assert not git('status','--porcelain=v1','--untracked-files=all').strip()
        assert not competing_writer(ROOT), 'competing material writer'
        assert git('ls-remote','--refs','origin','refs/heads/'+BRANCH).decode().split()[0] == BASE
        assert not (EV/'claim.json').exists(), '006 already claimed'
        raw=git('show', CONTROL+':docs/agent_handoff/DISPATCH/'+ID+'.json')
        dispatch=json.loads(raw)
        schema=json.loads(git('show',BASE+':docs/agent_handoff/FOX2_LOCAL_AGENT_DISPATCH_SCHEMA_v3.json'))
        Draft202012Validator(schema,format_checker=FormatChecker()).validate(dispatch)
        bindings={}
        for key,ck,pk in [('dictionary','git_commit_sha','git_path'),('policy','git_commit_sha','git_path'),('task','commit_sha','path'),('prompt','git_commit','path')]:
            b=dispatch[key]; data=git('show',b[ck]+':'+b[pk]); actual=hashlib.sha256(data).hexdigest()
            assert actual==b['sha256'], key
            bindings[key]={'commit':b[ck], 'path':b[pk], 'sha256':actual, 'verified':True}
        assert git('rev-parse',dispatch['prompt']['git_commit']+':'+dispatch['prompt']['path']).decode().strip()==dispatch['prompt']['git_blob_sha1']
        receipt=json.loads(git('show',BASE+':reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json'))
        assert receipt['status']=='PASS' and receipt['source_head']==git('rev-parse',BASE+'^').decode().strip()
        assert git('diff',BASE+'^',BASE,'--name-only').decode().strip()=='reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json'
        tools={n:tool_probe(n, ROOT) for n in ('git','python','pwsh','schtasks.exe')}
        assert all(t['status']=='PASS' for t in tools.values())
        route={'product':'CODEX',**dispatch['routing']}
        probe=agent_probe(route, ROOT)
        assert probe['status']=='PASS', 'current pinned auth/capacity probe failed'
        real=(Path.home()/'AppData/Local/FOX2/AgentBridge').resolve()
        temp=Path(tempfile.mkdtemp(prefix='fox2-core006-',dir='C:/Temp'))
        profile=temp/'user'; isolated=profile/'AppData/Local/FOX2/AgentBridge'
        assert not isolated.resolve().is_relative_to(real) and not real.is_relative_to(isolated.resolve())
        assert not any(p.is_symlink() or p.is_junction() for p in (temp,*temp.parents))
        profile.mkdir(); (profile/'AppData/Local').mkdir(parents=True)
        env={**os.environ, 'USERPROFILE':str(profile),'HOME':str(profile),'LOCALAPPDATA':str(profile/'AppData/Local'), 'APPDATA':str(profile/'AppData/Roaming'), 'CODEX_HOME':os.environ.get('CODEX_HOME', str(Path.home()/'.codex')), 'PYTHONDONTWRITEBYTECODE':'1'}
        env.pop('PYTHONPATH',None)
        env['TEMP']=env['TMP']=str(temp/'tmp'); (temp/'tmp').mkdir()
        prior={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.rglob('*') if p.is_file()}
        EV.mkdir(parents=True)
        with (EV/'claim.json').open('x',encoding='utf-8',newline='\n') as f:
            json.dump({'dispatch_id':ID,'control_commit':CONTROL,'source_head':BASE,'claimed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'max_runs':1,'dispatch_consumed':True,'no_retry':True,'prior_dispatches_replayed':False},f,indent=2); f.write('\n')
        save('launch.json',{'status':'PASS','bindings':bindings,'dispatch_sha256':hashlib.sha256(raw).hexdigest(),'schema_validation':'PASS','initial_worktree_clean':True,'branch':BRANCH,'source_head':BASE,'exclusive_os_lock':'fox2-preexec.lock held across launch and integrated tests','competing_writer':'NONE_OBSERVED','tools':tools,'current_pinned_route_probe':probe,'route':route,'permission':'danger-full-access / approval never','preexec_receipt':{'publication_commit':BASE,'receipt_source':receipt['source_head'],'receipt_only_parent_relation_verified':True},'quarantined_root':str(real),'disposable_profile':str(profile),'disposable_runtime_root':str(isolated),'root_overlap':False,'real_runtime_read_or_write':False,'prior_evidence_hashes':prior})
        shutil.copyfile(__file__,EV/'harness.py')
        save('progress.json',{'stage':'BUILD_ENVIRONMENT','disposable_root':str(temp)})
        print('LAUNCH_PASS; DISPATCH_006_CLAIMED; DISPOSABLE='+str(temp),flush=True)
        build=temp/'build'
        run([sys.executable,'-m','venv',build],env=env)
        bp=build/'Scripts/python.exe'
        run([bp,'-m','pip','--isolated','install','--disable-pip-version-check','setuptools>=80,<90','wheel','build','jsonschema>=4.25,<5','pytest>=8.3,<9'],env=env,timeout=240)
        packages=json.loads(run([bp,'-I','-c','import importlib.metadata as m,json; print(json.dumps({n:m.version(n) for n in ["setuptools","wheel","build","jsonschema","pytest","attrs","referencing","rpds-py","jsonschema-specifications"]}))'],env=env))
        save('build_environment.json',{'versions':packages,'venv':str(build),'host_modified':False})
        benv={**env,'PYTHONPATH':str(ROOT/'agent_bridge/src')}
        for n in (1,2):
            run([bp,ROOT/'agent_bridge/scripts/build_user_package.py','--output',temp/f'package{n}.zip','--build-python',bp],env=benv,timeout=240)
        first=json.loads((temp/'package1.json').read_text()); second=json.loads((temp/'package2.json').read_text())
        assert first['sha256']==second['sha256'],'package not deterministic'
        save('package.json',{'first':first,'second_sha256':second['sha256'],'byte_identical':True})
        def source(code): return json.loads(run([bp,'-c',code],env=benv))
        proof=source('import json; from pathlib import Path; from fox2_agent_bridge.paths import BRIDGE_ROOT; print(json.dumps({"root":str(BRIDGE_ROOT),"home":str(Path.home())}))')
        assert Path(proof['root']).resolve()==isolated.resolve()
        install=source('import json; from pathlib import Path; from fox2_agent_bridge.installation import install; print(json.dumps(install(Path('+repr(str(temp/'package1.zip'))+'),'+repr(first['sha256'])+')))')
        ip=isolated/'versions'/first['sha256']/'runtime/Scripts/python.exe'
        # Seed only disposable claims before setup; prevents legacy ledger migration.
        ids=['FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-'+f'{i:03}' for i in range(1,7)]
        isolated.joinpath('data/manual_consumption.json').write_text(json.dumps({'format':'FOX2_MANUAL_CONSUMPTION_1','dispatch_ids':ids}),encoding='utf-8')
        run([ip,'-I','-c','from fox2_agent_bridge.ledger import SQLiteLedger; from fox2_agent_bridge.paths import BRIDGE_ROOT; SQLiteLedger(BRIDGE_ROOT/"data/bridge.db").initialize()'],env=env)
        def cli(*args): return json.loads(run([ip,'-I','-m','fox2_agent_bridge',*args],env=env,timeout=90))
        setup=cli('setup'); assert setup['paused'] is True
        config=(isolated/'config/bridge.toml').read_bytes()
        assert cli('setup')['paused'] is True and config==(isolated/'config/bridge.toml').read_bytes()
        save('install_setup.json',{'root_proof':proof,'install':install,'setup':setup,'repeat_setup_preserves_config':True,'interpreter':str(ip)})
        print('PACKAGE_DETERMINISTIC; ISOLATED_INSTALL_SETUP_PASS',flush=True)
        # A byte-distinct archive of identical verified payload exercises real update
        # without inventing source changes or modifying the accepted source.
        update=temp/'update.zip'
        with zipfile.ZipFile(temp/'package1.zip') as src, zipfile.ZipFile(update,'w',compression=zipfile.ZIP_STORED) as dest:
            for item in src.infolist(): dest.writestr(item.filename,src.read(item.filename))
        update_sha=hashlib.sha256(update.read_bytes()).hexdigest()
        upgraded=source('import json; from pathlib import Path; from fox2_agent_bridge.installation import install; print(json.dumps(install(Path('+repr(str(update))+'),'+repr(update_sha)+')))')
        assert upgraded['status']=='UPDATED' and config==(isolated/'config/bridge.toml').read_bytes()
        ip=isolated/'versions'/update_sha/'runtime/Scripts/python.exe'
        assert cli('setup')['paused'] is True
        save('update.json',{'result':upgraded,'variant':'same verified payload, ZIP_STORED archive; packaging identity update, no code version change','configuration_preserved':True,'previous_version_retained':(isolated/'versions'/first['sha256']).is_dir()})
        tray=isolated/'versions'/update_sha/'payload/scripts/desktop_launcher.ps1'
        pwsh=shutil.which('pwsh')
        def count():
            script="$needle=$env:FOX2_CORE006_TRAY; @(Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'pwsh.exe' -and $_.CommandLine -and $_.CommandLine.Contains($needle) }).Count"
            return int(run([pwsh,'-NoProfile','-Command',script],env={**env,'FOX2_CORE006_TRAY':str(tray.with_name('desktop_tray.ps1'))}).strip())
        try:
            for _ in range(2): run([pwsh,'-NoProfile','-NonInteractive','-WindowStyle','Hidden','-STA','-File',tray],env=env,timeout=20)
            deadline=time.monotonic()+60
            while time.monotonic()<deadline:
                state=cli('control','status')
                if state.get('state')=='PAUSED' and state.get('heartbeat') and count()==1: break
                time.sleep(1)
            else: raise RuntimeError('isolated Tray/Worker unhealthy')
            r=subprocess.run([str(ip),'-I','-m','fox2_agent_bridge','worker'],capture_output=True,text=True,env=env,timeout=20,creationflags=subprocess.CREATE_NO_WINDOW)
            assert r.returncode!=0 and 'LOCK_HELD' in r.stderr
            runtime={'state':state['state'],'heartbeat':state['heartbeat'],'tray_count':count(),'launches':2,'duplicate_worker_exit':r.returncode,'duplicate_worker':'LOCK_HELD','startup_registration':'NOT_RUN: fixed current-user SID task belongs to host user; do not alter it'}
        finally:
            cli('control','request-exit')
            deadline=time.monotonic()+40
            while time.monotonic()<deadline and count(): time.sleep(1)
            assert count()==0,'isolated tray did not exit'
        state=cli('control','status'); assert state['state']=='STOPPED'
        lockproof=run([ip,'-I','-c','from fox2_agent_bridge.process_lock import ProcessLock; from fox2_agent_bridge.paths import BRIDGE_ROOT;\nwith ProcessLock(BRIDGE_ROOT/"data/bridge.lock"): print("LOCK_RELEASED")'],env=env)
        assert lockproof.strip()=='LOCK_RELEASED'
        runtime.update(graceful_exit='PASS',worker_lock_released=True,final_state=state['state'])
        save('tray_worker.json',runtime)
        bundle=temp/'support.zip'; diagnostics=cli('diagnostics','--output',str(bundle))
        with zipfile.ZipFile(bundle) as z:
            assert z.namelist()==['support.json']; support=json.loads(z.read('support.json'))
        save('diagnostics.json',{'result':diagnostics,'whitelist_payload':support,'raw_config_database_logs_excluded':True})
        # Genuine installed adapter execution, bounded response only; no nested DEV.
        code='''import json
from pathlib import Path
from fox2_agent_bridge.config import load_config
from fox2_agent_bridge.codex_adapter import CodexAdapter
from fox2_agent_bridge.preexec.probes import PROMPT,proof_marker
from fox2_agent_bridge.agent_policy import configuration_mismatch
r=CodexAdapter(load_config()).run_prompt(worktree=Path(ROOT_VALUE),prompt=PROMPT,selection=ROUTE_VALUE,timeout_seconds=90)
assert r.exit_code==0 and proof_marker('CODEX',r.stdout) and not configuration_mismatch(r.metadata)
print(json.dumps({'status':'PASS','execution_class':'installed adapter bounded no-write readiness fixture; not full dispatch/result E2E','exit_code':r.exit_code,'metadata':r.metadata}))
'''.replace('ROOT_VALUE',repr(str(ROOT))).replace('ROUTE_VALUE',repr(route))
        fixture=json.loads(run([ip,'-I','-c',code],env=env,timeout=120))
        save('installed_adapter.json',fixture)
        # Check all consumed identities in isolated ledger twice across process restarts.
        no_replay='''import json
from fox2_agent_bridge.config import load_config
from fox2_agent_bridge.desktop import initialize_runtime
from fox2_agent_bridge.ledger import utc_now
l=initialize_runtime(load_config())
ids=IDS_VALUE
assert all(not l.claim_dispatch(dispatch_id=i,payload_hash='a'*64,execution_id='must-not-execute',observed_at_utc=utc_now()) for i in ids)
assert l.pending_executions()==()
print(json.dumps({'blocked':ids,'pending_executions':0}))
'''.replace('IDS_VALUE',repr(ids))
        for _ in range(2): restart=json.loads(run([ip,'-I','-c',no_replay],env=env))
        save('restart_no_replay.json',{'status':'PASS','proof':restart,'fresh_processes':2,'scope':'isolated manual-consumption ledger only; historical live ledger untouched'})
        print('ISOLATED_TRAY_WORKER_EXIT_ADAPTER_RESTART_PASS; FULL_PYTEST_START_ONCE',flush=True)
        save('progress.json',{'stage':'FULL_PYTEST_ONCE','disposable_root':str(temp)})
        result=subprocess.run([str(bp),'-m','pytest',str(ROOT/'agent_bridge/tests'),'-q','--junitxml='+str(EV/'pytest.xml')],cwd=ROOT/'agent_bridge',env=benv,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600,creationflags=subprocess.CREATE_NO_WINDOW)
        (EV/'pytest.txt').write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
        save('pytest_result.json',{'exit_code':result.returncode,'invocations':1,'scope':'full Bridge suite, including existing mocked uninstall regressions; no lifecycle uninstall invoked'})
        assert result.returncode==0,'full Bridge tests failed'
        assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in prior.items()),'prior evidence modified'
        save('progress.json',{'stage':'CORE_TESTS_COMPLETED','disposable_root':str(temp),'prior_reports_preserved':True,'source_changes':False,'uninstall_lifecycle':'DEFERRED_OWNER_PRIORITY'})
        print('CORE_TESTS_COMPLETED',flush=True)

if __name__=='__main__':
    try: main()
    except Exception as exc:
        if (EV/'claim.json').exists(): save('stop.json',{'status':'STOPPED_NEEDS_RECONCILIATION','error_type':type(exc).__name__,'detail':str(exc),'dispatch_consumed':True,'no_retry':True})
        print(type(exc).__name__+': '+str(exc),flush=True)
        raise
