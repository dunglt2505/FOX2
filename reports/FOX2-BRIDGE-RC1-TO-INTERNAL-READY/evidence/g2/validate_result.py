"""Final schema, digest, K1, scope and credential-pattern delivery checks."""
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[4]
DIRECTORY = ROOT / 'reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
OUT = DIRECTORY / 'evidence/g2'


def main():
    manifest = json.loads((DIRECTORY / 'evidence_manifest.json').read_text())
    schema = json.loads((ROOT / 'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(manifest)
    ids = [e['id'] for e in manifest['evidence']]
    assert len(ids) == len(set(ids)), 'duplicate evidence identities'
    for item in manifest['evidence']:
        assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['sha256'], item['path']
    k1 = json.loads((OUT / 'k1.json').read_text())
    assert k1['unexplained_hunks'] == 0
    assert all(p['classification'] in ('REQUESTED', 'NECESSARY_DEPENDENCY', 'JUSTIFIED_GENERATED')
               and p['hunks'] for p in k1['paths'])
    for item in manifest['scope']['changed_paths']:
        if item['new_sha256'] is not None:
            assert hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest() == item['new_sha256'], item['path']
    pattern = re.compile(r'(?i)(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{20,}|'
                         r'AKIA[A-Z0-9]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|'
                         r'authorization["\x27]?\s*[:=]\s*["\x27]?Bearer\s+[A-Za-z0-9._~-]{16,})')
    for item in manifest['scope']['changed_paths']:
        assert not pattern.search((ROOT / item['path']).read_text(encoding='utf-8')), 'credential pattern in changed material'
    assert subprocess.run(['git', 'diff', '--quiet', k1['final_implementation_sha'], '--',
        'agent_bridge/src', 'agent_bridge/tests', 'agent_bridge/scripts'], cwd=ROOT).returncode == 0
    assert subprocess.run(['git', 'diff', '--check'], cwd=ROOT).returncode == 0
    assert manifest['permissions']['merge_allowed'] is False and manifest['permissions']['live'] is False
    result = dict(command='python evidence/g2/validate_result.py', exit_code=0,
        observed_at=datetime.now(UTC).isoformat(), schema='PASS', evidence_sha256='PASS',
        changed_sha256='PASS', k1='PASS', credential_pattern_scan='PASS',
        implementation_unchanged='PASS', host_enforcement='NOT_RUN_G3')
    if '--record' in sys.argv:
        (OUT / 'delivery_checks.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n',
                                                 encoding='utf-8', newline='\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
