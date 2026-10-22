import json,sys,subprocess,hashlib,importlib.util,os
from pathlib import Path
from datetime import datetime,timezone
repo=Path.cwd();out=repo/'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04';pkgsrc=Path(os.environ['FOX2_PACKAGE_SOURCE_WORKTREE']);builder=pkgsrc/'agent_bridge/scripts/build_user_package.py';output=Path(r'C:\Projects\FOX2-artifacts\host_lifecycle_cert_a04\FOX2-Bridge-085cc830-A04.zip')
assert not (out/'build_attempt.json').exists(),'one build already attempted'
assert not output.exists(),'output exists'
assert subprocess.check_output(['git','-C',str(pkgsrc),'status','--porcelain=v1','--untracked-files=all']).strip()==b''
assert subprocess.check_output(['git','-C',str(pkgsrc),'rev-parse','HEAD']).decode().strip()==os.environ['FOX2_ACCEPTED_SOURCE']
assert subprocess.check_output(['git','hash-object','--no-filters',str(builder)]).decode().strip()=='2417212e5677a2061e3957544a99e2ba80f46f4d'
spec=importlib.util.spec_from_file_location('a04_builder',builder);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);assert m.source_git_commit()==os.environ['FOX2_ACCEPTED_SOURCE']
for forbidden in [repo,pkgsrc,Path(os.environ['LOCALAPPDATA'])/'FOX2/AgentBridge']:
 assert not output.is_relative_to(forbidden)
record={'build_attempts':1,'started_at_utc':datetime.now(timezone.utc).isoformat(),'builder':'WORKTREES/FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04/agent_bridge/scripts/build_user_package.py','package_path':'ARTIFACTS/host_lifecycle_cert_a04/'+output.name,'source_git_commit_preprobe':m.source_git_commit(),'build_python':'WORKTREES/FOX2-BRIDGE-DESKTOP-BATCH-B/agent_bridge/.build-venv/Scripts/python.exe'}
(out/'build_attempt.json').write_text(json.dumps(record,indent=2)+'\n')
r=subprocess.run([sys.executable,'-I','-B',str(builder),'--output',str(output),'--build-python',sys.executable],cwd=pkgsrc,capture_output=True,text=True,timeout=600)
record.update(exit_code=r.returncode,finished_at_utc=datetime.now(timezone.utc).isoformat(),package_sha256=hashlib.sha256(output.read_bytes()).hexdigest() if output.is_file() else None)
(out/'build_attempt.json').write_text(json.dumps(record,indent=2)+'\n');(out/'build.log').write_text((r.stdout+'\n'+r.stderr).replace(os.environ['USERPROFILE'],'UserProfile'),encoding='utf-8');print(json.dumps(record));sys.exit(r.returncode)