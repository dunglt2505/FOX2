import os,sys,json,time,subprocess,hashlib,sqlite3,re
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd();out=repo/'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04';art=Path(r'C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04');package=art/'FOX2-Bridge-085cc830-A04.zip';raw=art/'lifecycle_raw.json';root=Path(os.environ['LOCALAPPDATA'])/'FOX2/AgentBridge';path=out/'lifecycle_attempt.json';assert not path.exists() and not raw.exists(),'lifecycle already attempted'
v=json.loads((out/'package_verification.json').read_text());s=json.loads((out/'installed_before_lifecycle.json').read_text());assert s['current']['package_sha256']==v['package_sha256'] and s['installed_receipt']['manifest']['source_git_commit']==os.environ['FOX2_ACCEPTED_SOURCE'];assert s['processes']['wpf']==[] and s['control']['paused'] is True and s['control']['setup_complete'] is True and s['control']['current_dispatch'] is None
assert hashlib.sha256(package.read_bytes()).hexdigest()==v['package_sha256'];assert subprocess.check_output(['git','diff',os.environ['FOX2_ACCEPTED_SOURCE'],'--','agent_bridge/scripts/certify_user_lifecycle.py']).strip()==b''
record={'attempts':1,'started_at_utc':datetime.now(timezone.utc).isoformat(),'package_sha256':v['package_sha256'],'entrypoint':'agent_bridge/scripts/certify_user_lifecycle.py','external_supervisor':True,'reruns':0};path.write_text(json.dumps(record,indent=2)+'\n')
def sanitize(value):
 if isinstance(value,dict):return {k:sanitize(v) for k,v in value.items()}
 if isinstance(value,list):return [sanitize(v) for v in value]
 if isinstance(value,str):return value.replace(str(root),'BridgeRoot').replace(str(art),'ARTIFACTS/host_lifecycle_cert_a04').replace(os.environ['USERPROFILE'],'UserProfile')
 return value
def checkpoint():
 if not raw.exists():return
 try:d=json.loads(raw.read_text())
 except (OSError,ValueError):return
 (out/'lifecycle.json').write_text(json.dumps(sanitize(d),indent=2)+'\n')
 if d.get('uninstall',{}).get('status')=='UNINSTALLED' and not (out/'post_uninstall_durable_checkpoint.json').exists():
  c={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'source':'read-only watcher after harness immediate uninstall checkpoint; same-package reinstall may have begun','harness_postconditions':d['uninstall']['post_uninstall'],'hashes':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ('config/bridge.toml','data/bridge.db','data/manual_consumption.json')}}
  conn=sqlite3.connect((root/'data/bridge.db').as_uri()+'?mode=ro',uri=True);conn.execute('PRAGMA query_only=ON');c['quick_check']=conn.execute('PRAGMA quick_check').fetchall();c['tables']={}
  for (table,) in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
   assert re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',table);rows=conn.execute('SELECT * FROM '+table).fetchall();normalized=sorted(json.dumps(row,sort_keys=True,default=lambda x:{'bytes_sha256':hashlib.sha256(x).hexdigest()}) for row in rows);c['tables'][table]={'rows':len(rows),'logical_sha256':hashlib.sha256(json.dumps(normalized).encode()).hexdigest()}
  conn.close();(out/'post_uninstall_durable_checkpoint.json').write_text(json.dumps(c,indent=2)+'\n')
with (art/'lifecycle_stdout.txt').open('w') as stdout,(art/'lifecycle_stderr.txt').open('w') as stderr:
 p=subprocess.Popen([sys.executable,'-I','-B',str(repo/'agent_bridge/scripts/certify_user_lifecycle.py'),'--package',str(package),'--sha256',v['package_sha256'],'--evidence',str(raw)],cwd=repo,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW)
 while p.poll() is None:
  checkpoint();time.sleep(.1)
 checkpoint();record.update(exit_code=p.returncode,finished_at_utc=datetime.now(timezone.utc).isoformat(),status='PASS' if p.returncode==0 else 'FAIL');path.write_text(json.dumps(record,indent=2)+'\n')
text=(art/'lifecycle_stdout.txt').read_text()+'\n'+(art/'lifecycle_stderr.txt').read_text();(out/'lifecycle.log').write_text(sanitize(text));print(json.dumps(record));print(sanitize(text));sys.exit(p.returncode)