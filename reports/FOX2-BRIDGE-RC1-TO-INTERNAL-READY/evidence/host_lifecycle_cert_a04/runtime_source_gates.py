# Sanitized review copy: the executed absolute CODEX capability path uses LOCALAPPDATA here.
import os,sys,json,hashlib,subprocess,importlib.util
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd(); out=repo/'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04'
checks={}; details={}
def run(*args,cwd=repo):
 r=subprocess.run([str(a) for a in args],cwd=cwd,capture_output=True,text=True,timeout=60)
 return r
def git(*args,cwd=repo):
 r=run('git',*args,cwd=cwd); assert r.returncode==0, ('git failed',args,r.stderr); return r.stdout.strip()
def check(n,v):
 checks[n]=bool(v)
 if not v: raise RuntimeError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
try:
 names='DISPATCH_ID DISPATCH_COMMIT RUNTIME_BASE ACCEPTED_SOURCE PASS_TO_ASSIGN_COMMIT PASS_TO_ASSIGN_PATH PREEXEC_RECEIPT_COMMIT CONTROL_BRANCH STATUS_BRANCH PACKAGE_SOURCE_WORKTREE OWNER_LAUNCHER_VERIFIED'.split()
 env={n:os.environ.get('FOX2_'+n) for n in names};check('envelope_present',all(env.values()));details['envelope']=env
 expected={'DISPATCH_ID':'FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001','ACCEPTED_SOURCE':'085cc8302e824dbccf9cbef80422ed48894b9cb4','CONTROL_BRANCH':'work/FOX2-DISPATCH-chat','STATUS_BRANCH':'work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021','PASS_TO_ASSIGN_PATH':'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A04_PASS_TO_ASSIGN_20261022.md','PACKAGE_SOURCE_WORKTREE':r'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04','OWNER_LAUNCHER_VERIFIED':'TRUE'}
 check('fixed_values',all(env[n]==v for n,v in expected.items()))
 branch='work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022';base=env['RUNTIME_BASE'];source=env['ACCEPTED_SOURCE'];pkg=Path(env['PACKAGE_SOURCE_WORKTREE'])
 check('orchestration_path',repo==Path(r'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022'))
 check('orchestration_clean',git('status','--porcelain=v1','--untracked-files=all')=='')
 check('branch_head',git('branch','--show-current')==branch and git('rev-parse','HEAD')==base)
 remote=git('ls-remote','--heads','origin','refs/heads/'+branch).split()[0];check('remote_head',remote==base)
 check('source_ancestor',run('git','merge-base','--is-ancestor',source,base).returncode==0)
 check('receipt_runtime_base',env['PREEXEC_RECEIPT_COMMIT']==base)
 check('no_product_drift',git('diff','--name-only',source,base,'--','agent_bridge')=='')
 dpath='docs/agent_handoff/DISPATCH/'+env['DISPATCH_ID']+'.json'
 for label,br,commit,path in [('dispatch',env['CONTROL_BRANCH'],env['DISPATCH_COMMIT'],dpath),('pass_to_assign',env['STATUS_BRANCH'],env['PASS_TO_ASSIGN_COMMIT'],env['PASS_TO_ASSIGN_PATH'])]:
  ref='refs/remotes/origin/'+br
  check(label+'_fetched_contains_commit',run('git','merge-base','--is-ancestor',commit,ref).returncode==0)
  check(label+'_same_bytes_at_fetched_tip',git('rev-parse',commit+':'+path)==git('rev-parse',ref+':'+path))
 d=json.loads(git('show',env['DISPATCH_COMMIT']+':'+dpath));details['dispatch']=d
 check('dispatch_identity',d['dispatch_id']==env['DISPATCH_ID'] and d['target_agent']=='CODEX' and d['max_runs']==1 and d['source']['commit_sha']==source)
 check('dispatch_route',d['routing']=={'model_policy':'PINNED','auto_tier':None,'model':'gpt-6.1-sol','reasoning_effort':'high','permission_profile':'FULL_ACCESS'} and d['execution_path']=='MANUAL_LOCAL')
 check('dispatch_permissions',d['permissions']['code_allowed'] is False and d['permissions']['git_code_push'] is False and d['permissions']['git_report_write'] and d['permissions']['git_report_push'])
 allowed=['reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md','reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json','reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**']
 check('dispatch_runtime',d['runtime_contract']['base_sha']==base and d['runtime_contract']['branch']==branch and d['runtime_contract']['worktree']==str(repo) and d['runtime_contract']['allowed_code_paths']==[] and d['runtime_contract']['allowed_report_paths']==allowed)
 for name,commitkey in [('task','commit_sha'),('prompt','git_commit'),('policy','git_commit_sha'),('dictionary','git_commit_sha')]:
  item=d[name];p=item.get('path',item.get('git_path'));c=item[commitkey];raw=subprocess.check_output(['git','show',c+':'+p])
  check(name+'_hash',sha(raw)==item['sha256']);details[name+'_identity']={'commit':c,'path':p,'blob':git('rev-parse',c+':'+p),'sha256':sha(raw)}
  if name in ('task','prompt'):check(name+'_runtime_bytes',git('rev-parse',c+':'+p)==git('rev-parse',base+':'+p) and sha((repo/p).read_bytes())==item['sha256'])
 check('task_exact',d['task']['commit_sha']=='8fdc2f7181e7f3e9a7f56ea72472fe3d2d2cea43' and details['task_identity']['blob']=='50d77f3039d2a8f9ce40105457da8e18b639289d')
 rp='reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a04.json';raw=subprocess.check_output(['git','show',base+':'+rp]);receipt=json.loads(raw)
 check('preexec_exact_hash',sha(raw)=='c3505039d6b89fba324d4c4354f29e5b106026d2be5bee1dab50ce8d5378eb25')
 check('preexec_pass',receipt['status']=='PASS' and receipt['blockers']==[] and receipt['agent_execution_started'] is False and receipt['dispatch_state']['dispatch_consumed'] is False and receipt['dispatch_state']['executable_dispatch_published'] is False)
 pta=git('show',env['PASS_TO_ASSIGN_COMMIT']+':'+env['PASS_TO_ASSIGN_PATH'])
 check('pass_to_assign_binding',all(s in pta for s in [base,env['DISPATCH_ID'],'FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04','PASS_TO_ASSIGN',rp]))
 check('same_repository',Path(git('rev-parse','--git-common-dir')).resolve()==Path(git('rev-parse','--git-common-dir',cwd=pkg)).resolve())
 check('package_worktree_path',Path(git('rev-parse','--show-toplevel',cwd=pkg))==pkg)
 check('package_detached_exact',run('git','symbolic-ref','-q','HEAD',cwd=pkg).returncode==1 and git('rev-parse','HEAD',cwd=pkg)==source)
 check('package_clean_before_probe',git('status','--porcelain=v1','--untracked-files=all',cwd=pkg)=='')
 builder=pkg/'agent_bridge/scripts/build_user_package.py';blob='2417212e5677a2061e3957544a99e2ba80f46f4d'
 check('builder_blob',git('hash-object','--no-filters',builder,cwd=pkg)==blob and git('rev-parse',source+':agent_bridge/scripts/build_user_package.py')==blob)
 check('builder_raw_bytes',builder.read_bytes()==subprocess.check_output(['git','show',source+':agent_bridge/scripts/build_user_package.py']))
 sys.dont_write_bytecode=True;spec=importlib.util.spec_from_file_location('builder_a04',builder);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 probe=m.source_git_commit();details['source_git_commit_probe']=probe;check('builder_source_probe',probe==source)
 check('package_clean_after_probe',git('status','--porcelain=v1','--untracked-files=all',cwd=pkg)=='')
 check('isolated_python',sys.prefix!=sys.base_prefix and sys.version_info[:2]==(3,13));details['python_version']=sys.version;details['build_environment']=m.inspect_build_environment(Path(sys.executable))
 check('dotnet',run('dotnet','--version').stdout.strip()=='8.0.426')
 check('codex_cli',run(Path(os.environ['LOCALAPPDATA'])/'Programs/OpenAI/Codex/bin/codex.exe','--version').stdout.strip()=='codex-cli 0.162.1')
 details['no_provenance_override_environment']={k:v for k,v in os.environ.items() if k.upper().startswith(('GIT_','PYTHON'))};check('no_git_override',not any(k.upper() in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES') for k in os.environ))
 details['verdict']='PASS'
except Exception as e:
 details['verdict']='BLOCKED';details['first_failure']=str(e)
finally:
 out.mkdir(parents=True,exist_ok=True);details.update(checks=checks,observed_at_utc=datetime.now(timezone.utc).isoformat());(out/'runtime_source_gates.json').write_text(json.dumps(details,indent=2)+'\n',encoding='utf-8');print(json.dumps({'verdict':details['verdict'],'checks':checks,'first_failure':details.get('first_failure')}))
 sys.exit(0 if details['verdict']=='PASS' else 1)