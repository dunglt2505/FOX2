"""Seal local source/result hashes without staging, committing or networking."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
REPORT = ROOT / 'reports/FOX2-M1-P2-03'
EVIDENCE = REPORT / 'evidence'
BASE = 'f70f0237356c4f27afb0e6760b01870228ba3739'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


source_entries = [entry for entry in json.loads(
    (ROOT / 'reports/FOX2-M1-P2-02/evidence/source_readback.json').read_text())['sources']
    if '/P2-02/' not in entry['path']]
source_entries += [{'path':'docs/brd_mirror/FOX2-BRD-08_v0.5.md', 'commit':BASE}]
sources = []
for entry in source_entries:
    path = entry['path']
    local = ROOT/path
    commit = BASE if local.exists() else entry['commit']
    blob = git('rev-parse', f'{commit}:{path}')
    if local.exists():
        assert git('hash-object', path) == blob
        data = local.read_bytes()
    else:
        # Accepted P2-02 receipt pins governance sources on a separate source
        # commit. Reuse those local Git objects; no checkout or network fetch.
        assert blob == entry['blob']
        data = subprocess.check_output(['git','cat-file','blob',blob], cwd=ROOT)
    sources.append({'path':path, 'commit':commit, 'blob':blob,
                    'location':'worktree' if local.exists() else 'accepted_receipt_pinned_local_git_object',
                    'sha256':hashlib.sha256(data).hexdigest()})
for name, commit in (
        ('FOX2_M1_P2_03_DSM_SOURCE_DESIGN_LOCK_20261014.md', '97b68bd67ef84675dabcfdd656f95ffb7d78511e'),
        ('FOX2_M1_P2_03_CODEX_EXECUTE_20261014.md', 'b0b1168a51275b8c94940f455860bee24c0aff0f')):
    path = 'docs/agent_handoff/M1/P2-03/' + name
    blob = git('rev-parse', f'{commit}:{path}')
    assert git('hash-object', path) == blob
    sources.append({'path':path, 'commit':commit, 'blob':blob,
                    'sha256':hashlib.sha256((ROOT/path).read_bytes()).hexdigest()})
(EVIDENCE/'source_readback.json').write_text(json.dumps(sources, indent=2), encoding='utf-8')

files = []
for folder in ('backend/src/fox2/dsm', 'tests/p2_03', 'reports/FOX2-M1-P2-03'):
    files.extend(path for path in (ROOT/folder).rglob('*') if path.is_file()
                 and path.name not in ('evidence_manifest.json', 'final_checks.json'))
patterns = [r'-----BEGIN [A-Z ]*PRIVATE KEY-----', r'AKIA[0-9A-Z]{16}',
            r'gh[pousr]_[A-Za-z0-9]{30,}', r'sk-[A-Za-z0-9]{32,}',
            r'(?i)(?:password|api_key|access_token|client_secret)\s*[:=]\s*[\x22\x27][^\x22\x27]{8,}']
for path in files:
    content = path.read_text(encoding='utf-8')
    assert not any(re.search(pattern, content) for pattern in patterns), path.name
    assert not any(line.rstrip() != line for line in content.splitlines()), path.name
assert not git('diff', '--check')
changed = [line[3:] for line in subprocess.check_output(
    ['git','status','--porcelain','--untracked-files=all'], cwd=ROOT, text=True).splitlines()]
assert all(path.startswith(('backend/src/fox2/dsm/', 'tests/p2_03/',
                           'reports/FOX2-M1-P2-03/')) for path in changed)
assert not git('diff', '--name-only')  # All preexisting tracked files unchanged.
quality = json.loads((EVIDENCE/'quality.json').read_text())
assert all(result['exit_code'] == 0 for result in quality['results'].values())
checks = {'changed_path_allowlist':'PASS', 'preexisting_tracked_files_unchanged':'PASS',
          'secret_scan':'PASS', 'all_new_files_whitespace':'PASS', 'git_diff_check':'PASS',
          'source_blob_readback':'PASS', 'network_attempts':0,
          'evidence_hashes':'SHA256 listed and independently reread during sealing'}
(EVIDENCE/'final_checks.json').write_text(json.dumps(checks,indent=2), encoding='utf-8')
files.append(EVIDENCE/'final_checks.json')
acceptance = ['FOX2-06-T'+suffix for suffix in ('02','03','04','07','08','09','15','16','18')]
acceptance += ['FOX2-N1-T'+suffix for suffix in ('01','02','07','09')]
manifest = {
    'work_package':'FOX2-M1-P2-03', 'state':'READY_FOR_BRIDGE_COMMIT_PUSH',
    'initial_head':git('rev-parse','HEAD'), 'accepted_upstream':BASE,
    'branch':git('branch','--show-current'), 'worktree':str(ROOT),
    'final_commit_sha':None, 'remote_readback_sha':None, 'git_delivery':'BRIDGE_OWNED_NOT_RUN',
    'model_variant':'NOT_EXPOSED', 'thinking':'NOT_EXPOSED', 'quota':'NOT_EXPOSED',
    'tests':quality['results'], 'checks':checks,
    'acceptance':[{'id':item, 'offline_subcase':'PASS', 'canonical':'PARTIAL',
                   'provider_api_ui':'NOT_RUN', 'mapping':'report.md acceptance table'} for item in acceptance],
    'not_run':['provider','API','frontend','LIVE','Production','broker/account','deployment','commit/push'],
    'files':[{'path':path.relative_to(ROOT).as_posix(),
              'sha256':hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes':path.stat().st_size}
             for path in sorted(files)],
}
target = REPORT/'evidence_manifest.json'
target.write_text(json.dumps(manifest,indent=2), encoding='utf-8')
reread = json.loads(target.read_text())
for item in reread['files']:
    assert hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest() == item['sha256']
assert not any(re.search(pattern,target.read_text()) for pattern in patterns)
print('PASS: scope, preservation, secrets, whitespace, sources and all evidence hashes')
