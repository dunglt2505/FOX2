import io,json,sys,os,hashlib,zipfile,subprocess,importlib.util
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd();out=repo/'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04';src=Path(os.environ['FOX2_PACKAGE_SOURCE_WORKTREE']);package=Path(r'C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip');checks={}
def sha(b):return hashlib.sha256(b).hexdigest()
def check(n,v):checks[n]=bool(v);assert v,n
try:
 attempt=json.loads((out/'build_attempt.json').read_text());check('one_build_exit_zero',attempt['build_attempts']==1 and attempt['exit_code']==0)
 digest=sha(package.read_bytes());check('package_sha256',digest==attempt['package_sha256'])
 with zipfile.ZipFile(package) as z:
  names=z.namelist();check('unique_safe_members',len(names)==len(set(names)) and all(not n.startswith('/') and '..' not in n.split('/') for n in names));m=json.loads(z.read('manifest.json'))
  check('format',m['format']=='FOX2_USER_PACKAGE_1');check('exact_source_commit',m['source_git_commit']==os.environ['FOX2_ACCEPTED_SOURCE']);check('payload_inventory',set(names)==set(m['files'])|{'manifest.json'})
  check('payload_hashes',all(sha(z.read(n))==h for n,h in m['files'].items()));check('desktop',m['desktop']=='NET8_WPF_SELF_CONTAINED_WIN_X64' and 'desktop/FOX2.Bridge.Desktop.exe' in names)
  for n,h in m['source_files'].items():
   p=src/'agent_bridge'/n
   if n.startswith('src/fox2_agent_bridge/resources/'):
    p=src/'agent_bridge/scripts'/Path(n).name
   check('source_file:'+n,p.is_file() and sha(p.read_bytes())==h)
  check('source_inventory_hash',sha(json.dumps(m['source_files'],sort_keys=True).encode())==m['source_sha256'])
  wheels=[n for n in names if n.startswith('wheels/fox2_agent_bridge-') and n.endswith('.whl')];check('one_bridge_wheel',len(wheels)==1)
  with zipfile.ZipFile(io.BytesIO(z.read(wheels[0]))) as w:
   modules={n for n in w.namelist() if n.startswith('fox2_agent_bridge/') and n.endswith('.py')};check('wheel_module_inventory',modules==set(m['wheel_source_modules']))
   check('wheel_source_module_hashes',all(sha(w.read(n))==h and sha((src/'agent_bridge/src'/n).read_bytes())==h for n,h in m['wheel_source_modules'].items()))
 sys.path.insert(0,str(src/'agent_bridge/src'));from fox2_agent_bridge import project_dictionary as d
 check('dictionary_identity',m['dictionary_version']==d.DICTIONARY_VERSION and m['dictionary_sha256']==d.SOURCE_SHA256)
 check('dictionary_git_bytes',sha(subprocess.check_output(['git','show',d.SOURCE_COMMIT+':'+d.SOURCE_PATH]))==d.SOURCE_SHA256)
 from fox2_agent_bridge.installation import verified_package
 vm,vf=verified_package(package,digest);check('accepted_package_verifier',vm==m and len(vf)==len(m['files']))
 check('source_head_unchanged',subprocess.check_output(['git','-C',str(src),'rev-parse','HEAD']).decode().strip()==os.environ['FOX2_ACCEPTED_SOURCE']);check('source_no_tracked_or_untracked_drift',subprocess.check_output(['git','-C',str(src),'status','--porcelain=v1','--untracked-files=all']).strip()==b'')
 result={'status':'PASS','package_sha256':digest,'manifest_summary':{k:m[k] for k in ['format','source_git_commit','source_sha256','dictionary_version','dictionary_sha256','python','platform','desktop']},'source_files_count':len(m['source_files']),'wheel_module_count':len(m['wheel_source_modules']),'payload_count':len(m['files']),'checks':checks,'observed_at_utc':datetime.now(timezone.utc).isoformat()}
except Exception as e:result={'status':'BLOCKED','first_failure':str(e),'checks':checks,'observed_at_utc':datetime.now(timezone.utc).isoformat()}
(out/'package_verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='checks'}));sys.exit(0 if result['status']=='PASS' else 1)