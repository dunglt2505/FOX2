import os,sys,json,time,subprocess,importlib.util
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd();out=repo/'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04';root=Path(os.environ['LOCALAPPDATA'])/'FOX2/AgentBridge';pwsh=r'C:\Program Files\PowerShell\7\pwsh.exe';ui=repo/'agent_bridge/scripts/certify_rc1_ui.ps1';record={'started_at_utc':datetime.now(timezone.utc).isoformat(),'stable_launch_count':0,'explicit_exit_count':0,'force_kill_count':0}
assert not (out/'stale_wpf_cleanup.json').exists(),'cleanup already attempted'
def save(): (out/'stale_wpf_cleanup.json').write_text(json.dumps(record,indent=2)+'\n')
def ps(*args):return subprocess.run([pwsh,'-NoProfile','-NonInteractive',*map(str,args)],capture_output=True,text=True,timeout=45,creationflags=subprocess.CREATE_NO_WINDOW)
def processes():
 r=ps('-Command',r'''ConvertTo-Json -Compress -InputObject @(Get-CimInstance Win32_Process -Filter "Name='FOX2.Bridge.Desktop.exe'"|Select-Object ProcessId,ExecutablePath)''');assert r.returncode==0;return json.loads(r.stdout)
def safe():
 current=json.loads((root/'current.json').read_text());assert current==original
 r=subprocess.run([str(root/'versions'/current['package_sha256']/'runtime/Scripts/python.exe'),'-I','-m','fox2_agent_bridge','control','status'],capture_output=True,text=True,timeout=30);assert r.returncode==0;s=json.loads(r.stdout);assert s.get('state')=='STOPPED' and s.get('paused') is True and s.get('setup_complete') is True and 'current_dispatch' in s and s['current_dispatch'] is None
 r=ps('-Command',r'''$p=@(Get-CimInstance Win32_Process|Where-Object {([string]$_.CommandLine) -match '(?i)fox2_agent_bridge\s+worker|desktop_(tray|launcher)\.ps1'}); $p.Count''');assert r.returncode==0 and int(r.stdout)==0
 return {k:s[k] for k in ('state','paused','setup_complete','current_dispatch')}
try:
 assert json.loads((out/'package_verification.json').read_text())['status']=='PASS'
 original=json.loads((root/'current.json').read_text());expected=root/'versions'/original['package_sha256']/'payload/desktop/FOX2.Bridge.Desktop.exe';record['initial_safe_control']=safe();observed=processes();assert len(observed)==1 and Path(observed[0]['ExecutablePath'])==expected;pid=observed[0]['ProcessId'];record['pid_before']=pid;record['package_before']=original
 r=ps('-File',ui,'-Action','inspect');record['initial_inspect_exit']=r.returncode
 if r.returncode:
  assert 'Installed Desktop window unavailable' in r.stderr+r.stdout,'unexpected inspect failure';record['initial_inspect']='WINDOW_UNAVAILABLE';safe();assert processes()==observed
  record['stable_launch_count']=1;record['host_mutation_started']=True;save()
  launched=ps('-WindowStyle','Hidden','-File',root/'launch.ps1');record['surface_launch_exit']=launched.returncode;save();assert launched.returncode==0,'surface launch failure'
  deadline=time.monotonic()+30
  while True:
   assert processes()==observed,'WPF singleton PID/path/count drift'
   r=ps('-File',ui,'-Action','inspect')
   if r.returncode==0:break
   assert 'Installed Desktop window unavailable' in r.stderr+r.stdout,'unexpected inspect failure after signal'
   if time.monotonic()>=deadline:raise RuntimeError('UI unavailable after bounded singleton show signal')
   time.sleep(.5)
  record['surface_same_pid_path_count']=True
 else:record['initial_inspect']='PASS'
 inspection=json.loads(r.stdout);assert inspection['process_id']==pid;record['inspection']=inspection;record['safe_before_exit']=safe();assert processes()==observed
 record['explicit_exit_count']=1;record['host_mutation_started']=True;save();r=ps('-File',ui,'-Action','exit');record['explicit_exit_result']=r.stdout.strip();save();assert r.returncode==0 and r.stdout.strip()=='EXIT_INVOKED','graceful exit failed'
 deadline=time.monotonic()+30
 while processes():
  if time.monotonic()>=deadline:raise RuntimeError('presentation remains after explicit exit')
  time.sleep(.5)
 record['final_presentation_count']=0
 lock=root.parent/'BridgeDesktop/desktop.lock'
 if lock.exists():
  with lock.open('r+b'):pass
 record['presentation_lock_released']=True;record['safe_after_exit']=safe();record['status']='PASS'
except Exception as e:record['status']='BLOCKED';record['first_failure']=str(e)
finally:
 record['finished_at_utc']=datetime.now(timezone.utc).isoformat();save();print(json.dumps(record));sys.exit(0 if record['status']=='PASS' else 1)