"""Real authenticated readback and native release-byte reconciliation, not authority."""
import base64
import hashlib
import json
import subprocess
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shared.local_git import LocalGit
from shared.core import digest

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'reports/FOX2-SKILLS-INTEGRATED-RELEASE/evidence'
adapter = LocalGit(ROOT)
adapter.refresh()
def command(*args):
    return subprocess.check_output(list(args),cwd=ROOT)
ref = 'origin/work/FOX2-AGENT-USAGE-TELEMETRY-01-chat'
head = command('git','rev-parse',ref).decode().strip()
mp = 'docs/governance/FOX2_AGENT_ROUTE_MATERIALITY_RELEASE_MANIFEST_20261014.json'
manifest = json.loads(adapter.read_file(mp,head))
source = manifest['source_set_head']
rows = []
for entry in manifest['files']:
    content = adapter.read_file(entry['path'], source)
    blob = hashlib.sha1(b'blob '+str(len(content)).encode()+b'\0'+content).hexdigest()
    rows.append({'path':entry['path'],'commit':source,'sha256':digest(content),'bytes':len(content),
                 'blob_matches_manifest':blob == entry['blob_sha']})
dp = 'docs/governance/FOX2_PROJECT_DICTIONARY_v1.json'
remote = json.loads(command('gh','api','repos/dunglt2505/FOX2/contents/'+dp+'?ref='+source))
remote_bytes = base64.b64decode(remote['content'])
local_bytes = adapter.read_file(dp,source)
result = {'status':'AUTHENTICATED_GIT_BYTES_VERIFIED_NOT_EFFECTIVITY', 'ref':ref,'observed_head':head,
          'manifest_path':mp,'source_set_head':source,'files':rows,
          'github_api_dictionary_sha256':digest(remote_bytes),
          'github_api_matches_git':remote_bytes == local_bytes,
          'library_mirror_status':manifest['library_mirror_status'],
          'authority_status':'BLOCKED_OWNER_AUTHORIZED_CURRENT_TRUST_ANCHOR_NOT_ESTABLISHED'}
(OUT/'git_readback.json').write_text(json.dumps(result,indent=2),encoding='utf-8', newline='\n')
print(json.dumps({'matched_files':sum(x['blob_matches_manifest'] for x in rows),'total':len(rows),
                  'github_api_matches_git':result['github_api_matches_git']}))
