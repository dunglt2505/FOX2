"""Inventory all fetched Git refs, preserving exact byte identities, no promotion."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/FOX2-SKILLS-INTEGRATED-RELEASE/evidence'
OUT.mkdir(parents=True, exist_ok=True)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


refs = git('for-each-ref', '--format=%(refname)', 'refs/remotes/origin', 'refs/tags').decode().splitlines()
inventory = []
blobs = {}
for ref in refs:
    commit = git('rev-parse', ref).decode().strip()
    found = []
    for line in git('ls-tree', '-r', ref).decode().splitlines():
        meta, path = line.split('\t', 1)
        if re.search(r'(?i)(SOURCE_INDEX|DICTIONARY|REGISTRY|RELEASE_MANIFEST|dispatch/|SKILLS|MASTER_EXECUTION|AGENTS\.md)', path):
            blob = meta.split()[2]
            raw = git('cat-file', 'blob', blob) if blob not in blobs else None
            if raw is not None:
                blobs[blob] = {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
                (OUT / (blob + Path(path).suffix)).write_bytes(raw)
            found.append({'path': path, 'blob': blob})
    inventory.append({'ref': ref, 'commit': commit, 'sources': found})
(OUT / 'git_discovery.json').write_text(json.dumps({'status': 'DISCOVERY_ONLY', 'refs': inventory, 'blobs': blobs}, indent=2), encoding='utf-8', newline='\n')
print(json.dumps({'refs': len(refs), 'unique_blobs': len(blobs)}))
