"""Repeatable read-only Result Contract v2, hash, scope and privacy checks."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
from jsonschema import Draft202012Validator, FormatChecker

ROOT=Path(__file__).resolve().parents[4]
AREA=Path(__file__).resolve().parent
PREFIX='reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'
START='208de84f39dcf783bd4ee9053c0288cda9aa0024'
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
git=lambda *a:subprocess.check_output(['git','-C',str(ROOT),*a],text=True).strip()

def paths():
    return sorted(set(git('diff','--name-only',START).splitlines())|set(git('ls-files','--others','--exclude-standard').splitlines()))

def static():
    changed=paths()
    assert all(p in (PREFIX+'report.md',PREFIX+'evidence_manifest.json') or p.startswith(PREFIX+'evidence/host_lifecycle_cert/') for p in changed)
    assert not git('diff','--check',START)
    assert not git('diff','--name-only','2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb','--','agent_bridge')
    secret=rb'(?i)(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|https?://[^\s/]+:[^\s/]+@|(?:authorization|access_token|api_key)\s*[=:])'
    for name in changed:
        path=ROOT/name
        assert path.suffix in ('.json','.md','.py','.txt')
        raw=path.read_bytes()
        assert len(raw)<200_000 and b'\x00' not in raw
        assert not re.search(secret,raw), 'secret scan finding: '+name
        assert not re.search(rb'(?i)[a-z]:[\\/]+users[\\/]+[A-Za-z]',raw), 'private user path: '+name
        assert b'\r\n' not in raw, 'noncanonical evidence text: '+name
        if path.suffix=='.py': compile(raw,name,'exec')
    assert sum((ROOT/p).stat().st_size for p in changed)<500_000
    print('ALLOWLIST/NO_PRODUCT_DRIFT/DIFF/BOUNDED_SECRET_SCAN/SYNTAX=PASS')

def result():
    manifest=json.loads((ROOT/PREFIX/'evidence_manifest.json').read_text())
    schema=json.loads((ROOT/'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text())
    Draft202012Validator(schema,format_checker=FormatChecker()).validate(manifest)
    ids={item['id'] for item in manifest['evidence']}
    assert len(ids)==len(manifest['evidence'])
    targets={item['id'] for item in manifest['tests']+manifest['acceptance']}
    for item in manifest['evidence']:
        assert sha(ROOT/item['path'])==item['sha256'],item['id']
        assert set(item['supports_ids'])<=targets,item['id']
    for item in manifest['tests']+manifest['acceptance']:
        assert set(item['evidence_ids'])<=ids,item['id']
    assert set(paths())=={item['path'] for item in manifest['scope']['changed_paths']}
    for item in manifest['scope']['changed_paths']:
        if item['new_sha256'] is not None:
            assert sha(ROOT/item['path'])==item['new_sha256'],item['path']
        else: assert item['path']==PREFIX+'evidence_manifest.json'
    k1=json.loads((AREA/'k1.json').read_text())
    assert k1['UNEXPLAINED']==0
    assert set(paths())=={item['path'] for item in k1['changes']}
    execution=json.loads((AREA/'execution.json').read_text())
    assert execution['status']=='FAIL' and execution['lifecycle_attempts']==1
    assert execution['stable_uninstall_attempts']==0 and execution['recovery_attempts']==0
    assert any(item['status']=='FAIL' for item in manifest['tests'])
    assert any(item['status']=='NOT_RUN' for item in manifest['acceptance'])
    print('RESULT_CONTRACT_V2/EVIDENCE_HASHES/REFERENCES/CHANGED_PATH_COVERAGE/K1=PASS; HOST_LIFECYCLE=FAIL; REWORK_REQUIRED')

if __name__=='__main__':
    static()
    result()
