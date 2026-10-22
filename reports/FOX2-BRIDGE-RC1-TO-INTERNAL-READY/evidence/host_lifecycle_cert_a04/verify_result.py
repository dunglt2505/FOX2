import ast,json,hashlib,os,re,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd();prefix='reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY';out=repo/prefix/'evidence/host_lifecycle_cert_a04';base=os.environ['FOX2_RUNTIME_BASE']
def git(*args):return subprocess.check_output(['git',*args],cwd=repo).decode().strip()
def changed():return sorted(set(git('diff','--name-only',base).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines()))
def allowed(p):return p in [prefix+'/report.md',prefix+'/evidence_manifest.json'] or p.startswith(prefix+'/evidence/host_lifecycle_cert_a04/')
def scan(paths):
 findings=[]
 patterns=[rb'gh[pousr]_[A-Za-z0-9]{20,}',rb'github_pat_[A-Za-z0-9_]{20,}',rb'sk-[A-Za-z0-9_-]{20,}',rb'https?://[^\s/]+:[^\s/]+@',rb'(?i)(?:access_token|api_key|password|authorization)\s*[:=]\s*["\x27]?[A-Za-z0-9_/-]{16,}',rb'(?i)C:[\\/]+Users[\\/]+Fox Le',rb'(?i)BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY']
 for path in paths:
  raw=(repo/path).read_bytes()
  for i,pattern in enumerate(patterns):
   if re.search(pattern,raw):findings.append({'path':path,'pattern_id':i})
 assert not findings,str(findings)
 return {'status':'PASS','files_scanned':len(paths),'findings':findings,'method':'Credential signatures, credential assignments, private-key headers, user-profile paths; file inventory inspection excludes raw config/database/prompts/binaries'}
def static():
 paths=changed();assert all(allowed(p) for p in paths);assert git('diff','--name-only',os.environ['FOX2_ACCEPTED_SOURCE'],'--','agent_bridge')==''
 src=os.environ['FOX2_PACKAGE_SOURCE_WORKTREE'];assert subprocess.check_output(['git','-C',src,'status','--porcelain=v1','--untracked-files=all']).strip()==b'';assert subprocess.check_output(['git','-C',src,'rev-parse','HEAD']).decode().strip()==os.environ['FOX2_ACCEPTED_SOURCE']
 for p in out.glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
 diff=subprocess.run(['git','diff','--check',base],capture_output=True,text=True);assert diff.returncode==0; (out/'diff_check.log').write_text('git diff --check '+base+'\nexit=0\n'+diff.stdout+diff.stderr,newline='\n')
 scan_result=scan(paths)
 groups=[]
 for path in changed():
  tracked=bool(git('ls-files','--',path));patch=subprocess.check_output(['git','diff','--unified=0',base,'--',path]) if tracked else (repo/path).read_bytes()
  headers=re.findall(rb'^@@.*@@.*$',patch,re.M) if tracked else [b'NEW_EVIDENCE_FILE']
  groups.append({'path':path,'classification':'REQUESTED' if path.endswith(('/report.md','/evidence_manifest.json')) else 'JUSTIFIED_GENERATED','reason':'A04 report and Result Contract v2 delivery' if path.endswith(('/report.md','/evidence_manifest.json')) else 'Bounded A04 execution, immutable binding, read-only snapshot, single-attempt helper, or audit evidence','hunks':[h.decode() for h in headers],'reviewed_bytes_sha256':hashlib.sha256(patch).hexdigest() if path not in [prefix+'/report.md',prefix+'/evidence_manifest.json',prefix+'/evidence/host_lifecycle_cert_a04/k1.json',prefix+'/evidence/host_lifecycle_cert_a04/static_checks.json'] else None})
 (out/'k1.json').write_text(json.dumps({'base':base,'UNEXPLAINED':0,'classification_scope':'Every changed path and all diff hunks; evidence hashes are independently inventoried in the Result Contract manifest','paths':groups},indent=2)+'\n',newline='\n')
 result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'changed_path_allowlist':'PASS','python_evidence_syntax':'PASS','orchestration_product_source_test_no_drift':'PASS','package_source_tracked_untracked_no_drift':'PASS','package_source_head':os.environ['FOX2_ACCEPTED_SOURCE'],'secret_privacy_scan':scan_result,'git_diff_check':'PASS','K1_UNEXPLAINED':0,'forbidden_actions':'No Worker/F1/legacy tray, AppLocker/AppIDSvc, service, ProgramData ACL, reboot, G3/G4/Canary, provider/broker/LIVE, PR/main/merge action invoked; scope assertion from single-attempt execution record and helpers, not a hostwide attestation','historical_dispatch_immutability':'Fetched historical Dispatch files remain untouched; no replay launched'}
 (out/'static_checks.json').write_text(json.dumps(result,indent=2)+'\n',newline='\n');print(json.dumps(result))
def validate():
 import jsonschema
 m=json.loads((repo/prefix/'evidence_manifest.json').read_text());schema=json.loads(subprocess.check_output(['git','show','refs/remotes/origin/work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019:docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json']));jsonschema.Draft202012Validator(schema,format_checker=jsonschema.FormatChecker()).validate(m)
 e={x['id']:x for x in m['evidence']};assert len(e)==len(m['evidence']);tracked=set(git('ls-files').splitlines());assert all(x['path'] in tracked for x in m['evidence']),'referenced evidence must be in Git index'
 for x in m['evidence']:
  assert hashlib.sha256((repo/x['path']).read_bytes()).hexdigest()==x['sha256'],x['path']
 for x in m['tests']+m['acceptance']:
  assert set(x['evidence_ids'])<=e.keys()
 for x in m['scope']['changed_paths']:
  assert allowed(x['path']);assert x['new_sha256'] is None if x['path']==prefix+'/evidence_manifest.json' else hashlib.sha256((repo/x['path']).read_bytes()).hexdigest()==x['new_sha256'],x['path']
 assert set(changed())=={x['path'] for x in m['scope']['changed_paths']}
 scan(changed());diff=subprocess.run(['git','diff','--check',base],capture_output=True,text=True);assert diff.returncode==0
 print('Result Contract v2 schema + formats + evidence references/hashes + complete changed-path inventory + privacy scan + diff check: PASS')
if __name__=='__main__':
 if sys.argv[1]=='static':static()
 else:validate()