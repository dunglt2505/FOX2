"""Refresh generated Result Contract hashes/K1; preserve source and test facts."""
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import subprocess

import verify_build as verify


def write(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root, out, wp = verify.ROOT, verify.OUT, verify.WP
    path = root / wp / 'evidence_manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    # Material artifact bytes are UTF-8 LF. Do not touch the historical receipt.
    for artifact in out.glob('*.json'):
        if artifact.name != 'samehost_build_a01_live_admission.json':
            artifact.write_text(artifact.read_text(encoding='utf-8'), encoding='utf-8', newline='\n')
    manifest['source']['source_manifest_sha256'] = sha(out / 'source_binding.json')
    if not any(t['id'] == 'assembly-01' for t in manifest['tests']):
        manifest['tests'].append(dict(id='assembly-01', kind='OTHER', status='FAIL',
            command_or_method='Interim evidence assembly and preliminary delivery checks',
            environment='Windows text serialization / reports/** -text',
            run_at_utc=datetime.now(UTC).isoformat(), evidence_ids=['assembly-01'],
            notes='Cache directory enumeration, JSON CRLF and default code-page decoding failed; fixed in evidence assembly only. Original failure retained.'))
    write(path, manifest)
    # Hunk headers, but no content hash, in K1 avoid a self-hash cycle. Iteration
    # stabilizes tracked report/manifest line ranges; new files are wholly added.
    for _ in range(3):
        paths = verify.changed()
        k1 = json.loads((out / 'k1.json').read_text(encoding='utf-8'))
        k1['paths'] = [dict(path=p, classification=verify.classify(p)[0],
            reason=verify.classify(p)[1], hunks=verify.hunks(p)) for p in paths]
        write(out / 'k1.json', k1)
        manifest['scope']['changed_paths'] = []
        for p in paths:
            prior = subprocess.run(['git', 'cat-file', '-e', verify.BASE + ':' + p],
                                   cwd=root, capture_output=True)
            manifest['scope']['changed_paths'].append(dict(path=p,
                operation='MODIFY' if prior.returncode == 0 else 'ADD',
                intent=': '.join(verify.classify(p)), within_allowed_paths=True,
                new_sha256=None if p == wp + 'evidence_manifest.json' else sha(root / p)))
        manifest['evidence'] = []
        for p in sorted(out.iterdir()):
            if not p.is_file() or p.name == 'samehost_build_a01_live_admission.json':
                continue
            identity = p.stem
            kind = ('TEST_LOG' if identity.startswith(('focused-', 'full-', 'static-', 'assembly-'))
                    or identity == 'delivery_checks' else 'SOURCE_READBACK' if identity == 'source_binding'
                    else 'DIFF' if identity == 'k1' else 'OTHER')
            manifest['evidence'].append(dict(id=identity, path=p.relative_to(root).as_posix(),
                sha256=sha(p), kind=kind, observed_at_utc=manifest['submitted_at_utc'],
                description='Bounded A01 ' + p.name + '; source/fixture evidence only',
                supports_ids=['A13'] if identity not in ('focused-01', 'focused-02', 'full-01',
                    'source_binding', 'contract_examples') else ['A10', 'A11', 'A12'] if
                    identity.startswith(('focused-', 'full-')) else ['A9', 'A15'] if
                    identity == 'source_binding' else ['A1', 'A3', 'A4'], sanitized=True))
        write(path, manifest)
    print('RESULT_EVIDENCE_REFRESHED')


if __name__ == '__main__':
    main()
