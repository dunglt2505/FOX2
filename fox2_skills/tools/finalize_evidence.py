"""Run verification and record exact package hashes; no release/push action."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT/'fox2_skills'
REPORT = ROOT/'reports/FOX2-SKILLS-INTEGRATED-RELEASE'
EVIDENCE = REPORT/'evidence'
def digest(raw): return hashlib.sha256(raw).hexdigest()
def write(path, data): path.write_text(json.dumps(data,indent=2),encoding='utf-8', newline='\n')

# Retain imported release claims as explicitly historical provenance.
provenance = PACKAGE/'provenance'; provenance.mkdir(exist_ok=True)
for name in ['RELEASE_README.md','RELEASE_MANIFEST_CANDIDATE.json']:
    old = PACKAGE/name
    if old.exists(): old.rename(provenance/name)
legacy = PACKAGE/'tests/legacy_git_resolver.py'
text = legacy.read_text(encoding='utf-8')
start = text.index("if __name__=='__main__':")
legacy.write_text(text[:start]+"if __name__=='__main__':\n    print(json.dumps({'status':'UNVERIFIED','reason':'Legacy Candidate CLI disabled; use native_registry with host authority verifier'}))\n    raise SystemExit(2)\n",encoding='utf-8', newline='\n')

env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8')
tests = subprocess.run([sys.executable,'-m','unittest','discover','-s','tests','-v'],cwd=PACKAGE,capture_output=True,text=True,env=env)
(EVIDENCE/'unittest.txt').write_text(tests.stdout+tests.stderr,encoding='utf-8', newline='\n')
if tests.returncode: raise SystemExit('Tests failed; see unittest.txt')
env['PYTHONPATH'] = str(ROOT/'.qa-deps')
validation = []
for skill in sorted((PACKAGE/'skills').iterdir()):
    proc = subprocess.run([sys.executable, str(Path.home()/'.codex/skills/.system/skill-creator/scripts/quick_validate.py'),str(skill)],capture_output=True,text=True,env=env)
    validation.append({'skill':skill.name,'exit_code':proc.returncode,'output':proc.stdout+proc.stderr})
write(EVIDENCE/'skill_validation.json',validation)
if any(x['exit_code'] for x in validation): raise SystemExit('Skill validation failed')

source = Path.home()/'Downloads'
inputs = []
for path in sorted(source.glob('FOX2_SKILLS*')):
    if path.is_file(): inputs.append({'path':str(path),'sha256':digest(path.read_bytes()),'bytes':path.stat().st_size})
write(EVIDENCE/'input_inventory.json',inputs)
original = zipfile.ZipFile(source/'FOX2_SKILLS_V07_CANDIDATE_DISTRIBUTION_20261016.zip')
claims = json.loads(original.read('RELEASE_MANIFEST_CANDIDATE.json'))
write(EVIDENCE/'candidate_import_check.json',{'status':'BYTE_CHECK_ONLY','files':[{'path':x['path'],'matches':digest(original.read(x['path']))==x['sha256']} for x in claims['files']]})

files = {}
for path in sorted(PACKAGE.rglob('*')):
    if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc' and path.name != 'release_manifest.json':
        files[path.relative_to(PACKAGE).as_posix()] = {'sha256':digest(path.read_bytes()),'bytes':path.stat().st_size}
write(PACKAGE/'release_manifest.json',{'status':'INTEGRATION_PENDING_NOT_READY','generated_utc':datetime.now(timezone.utc).isoformat(),
       'source_lock':'../reports/FOX2-SKILLS-INTEGRATED-RELEASE/evidence/git_readback.json',
       'source_binding_evidence_sha256':digest((EVIDENCE/'git_readback.json').read_bytes()),
       'source_authority_status':'UNVERIFIED',
       'excludes':['release_manifest.json','__pycache__','*.pyc'],'files':files})
print(json.dumps({'tests_exit_code':tests.returncode,'skills_validated':len(validation),'hashed_package_files':len(files)}))
