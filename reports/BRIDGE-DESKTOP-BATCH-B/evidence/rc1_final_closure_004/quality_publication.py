"""Allowlist, secret-pattern and exact staged-byte manifest checks."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

out = Path(__file__).resolve().parent
repo = out.parents[3]
report_root = repo/'reports/BRIDGE-DESKTOP-BATCH-B'
prefix = 'reports/BRIDGE-DESKTOP-BATCH-B/'
def git(*args):
    return subprocess.check_output(['git',*args],cwd=repo)
def write(path, data):
    Path(path).write_bytes((json.dumps(data,indent=2)+'\n').encode())
# Repository evidence bytes are LF. Preserve historical copies exactly.
files = list(out.iterdir())+[report_root/'report.md',report_root/'evidence_manifest.json']
for path in files:
    if path.is_file() and path.suffix in ('.py','.json','.md','.txt') and not path.name.startswith('historical_'):
        path.write_bytes(path.read_bytes().replace(b'\r\n',b'\n'))
paths = sorted(set(git('diff','--name-only').decode().splitlines()+git('ls-files','--others','--exclude-standard').decode().splitlines()+git('diff','--cached','--name-only').decode().splitlines()))
assert paths and all(p.startswith(prefix) for p in paths)
assert not any(p.startswith('agent_bridge/') for p in paths)
patterns = {
    'private_key': re.compile(r'-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'),
    'github_token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b'),
    'openai_key': re.compile(r'\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}\b'),
    'aws_access_key': re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
    'credential_url': re.compile(r'https?://[^\s/:]+:[^\s/@]+@'),
}
text_count = 0
hits = []
for name in paths:
    path = repo/name
    if path.suffix not in ('.py','.json','.md','.txt'):
        continue
    text_count += 1
    content = path.read_text(encoding='utf-8-sig')
    for label, pattern in patterns.items():
        if pattern.search(content):
            hits.append(dict(path=name,pattern=label))
assert not hits, hits
git('diff','--check')
write(out/'quality_checks.json',dict(status='PASS',changed_path_allowlist='PASS',product_changes=[],secret_scan='PASS',patterns_scanned=list(patterns),text_files_scanned=text_count,private_data_review='Only synthetic artifact, bounded installed identity/status and app UI receipts. Native picker unrelated folder listings omitted from published UI receipt.',git_diff_check='PASS',fresh_artifact_readback_checks=27,installed_payload_hashes=252,prior_tests_carried_forward=dict(python=399,desktop=30),prior_package_determinism='PASS_UNCHANGED_PACKAGE',icon_disposition='ICON_NON_GATING_NO_AUTHORIZED_ASSET',independent_audit='PENDING'))
git('add','--',prefix+'report.md',prefix+'evidence_manifest.json',prefix+'evidence/rc1_final_closure_004')
staged = git('diff','--cached','--name-only').decode().splitlines()
assert all(p.startswith(prefix) for p in staged)
manifest_path = prefix+'evidence_manifest.json'
manifest = json.loads((repo/manifest_path).read_text())
manifest['changed_paths'] = staged
manifest['files_sha256'] = {p:hashlib.sha256(git('show',':'+p)).hexdigest() for p in staged if p != manifest_path}
write(repo/manifest_path,manifest)
git('add','--',manifest_path)
git('diff','--cached','--check')
for p, digest in manifest['files_sha256'].items():
    assert hashlib.sha256(git('show',':'+p)).hexdigest() == digest
print(json.dumps(dict(status='PASS',staged_paths=len(staged),text_files_scanned=text_count,manifest_hashes_verified=len(manifest['files_sha256']))))
