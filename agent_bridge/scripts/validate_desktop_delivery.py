"""Read-only Git/scope/secret checks and reproducible Desktop evidence manifest."""
from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / 'reports/BRIDGE-DESKTOP-01-02'
EXPECTED_HEAD = '4778d78a11e844b6938157fcb0532664169a68d3'
LOCK = 'docs/agent_handoff/BRIDGE/FOX2_BRIDGE_DESKTOP_01_02_SOURCE_DESIGN_LOCK_20261014.md'
EXPECTED_BLOB = '6683781beb03a9c7deea9260c2d6553798e298ad'
ALLOW = ('agent_bridge/', 'reports/BRIDGE-DESKTOP-01-02/')


def git(*args):
    return subprocess.run(['git', '-C', str(ROOT), *args], capture_output=True, check=True).stdout


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    changed = set(filter(None, git('diff','--name-only','-z').decode().split('\0')))
    changed.update(filter(None,git('ls-files','--others','--exclude-standard','-z').decode().split('\0')))
    changed.add('reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json')
    changed.add('reports/BRIDGE-DESKTOP-01-02/evidence/verification.json')
    assert all(path.startswith(ALLOW) for path in changed), 'changed path outside exact allowlist'
    assert git('rev-parse','HEAD').decode().strip() == EXPECTED_HEAD
    assert git('hash-object',LOCK).decode().strip() == EXPECTED_BLOB
    assert not git('diff','--cached','--name-only'), 'task index must remain unstaged'
    git('diff','--check')
    patterns = [r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b',
                r'\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b', r'(?i)\bBearer\s+\S+',
                r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----']
    scanned=[]
    for path in REPORT.rglob('*'):
        if path.is_file():
            content=path.read_text(encoding='utf-8')
            assert not any(re.search(pattern,content) for pattern in patterns), 'report secret scan failed'
            scanned.append(path.relative_to(ROOT).as_posix())
    scanned = sorted(set(scanned) | {
        'reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json',
        'reports/BRIDGE-DESKTOP-01-02/evidence/verification.json'})
    suite=ET.parse(REPORT/'evidence/pytest.xml').getroot().find('testsuite')
    assert suite is not None and suite.attrib['failures'] == '0' and suite.attrib['errors'] == '0'
    assert suite.attrib['skipped'] == '0'
    now=datetime.now(UTC).isoformat()
    verification={'verified_at_utc':now,'status':'PASS','head':EXPECTED_HEAD,'source_lock_blob':EXPECTED_BLOB,
                  'changed_path_allowlist':'PASS','changed_paths':sorted(changed),'git_diff_check':'PASS',
                  'task_index_unstaged':'PASS','report_secret_scan':'PASS','secret_scan_files':sorted(scanned),
                  'pytest':{key:suite.attrib[key] for key in ('tests','failures','errors','skipped')}}
    (REPORT/'evidence/verification.json').write_text(json.dumps(verification,indent=2)+'\n',encoding='utf-8')
    files=[{'path':path,'sha256':sha(ROOT/path)} for path in sorted(changed)
           if (ROOT/path).is_file() and path != 'reports/BRIDGE-DESKTOP-01-02/evidence_manifest.json']
    manifest={'schema_version':1,'dispatch_id':'FOX2-BRIDGE-DESKTOP-01-02-CODEX-002',
              'work_package':'BRIDGE-DESKTOP-01-02','delivery_status':'LOCAL_DELIVERY_READY_BRIDGE_PUBLICATION_PENDING',
              'generated_at_utc':now,'base_sha':EXPECTED_HEAD,'source_lock_blob':EXPECTED_BLOB,
              'allowed_write_scope':['agent_bridge/**','reports/BRIDGE-DESKTOP-01-02/**'],
              'verification':verification,'files':files,'manifest_self_hash':'EXCLUDED',
              'evidence_classes':{'regression':'UNIT_LOCAL','poller_remote_transport':'SIMULATED_WITH_REAL_GIT_HISTORY',
                                 'agent_execution':'FAKE_AGENT','recovery_remote_result':'SIMULATED_VERIFIER',
                                 'powershell_dotnet':'REAL_HEADLESS_CONSTRUCTION_AND_PARSE',
                                 'startup':'MOCKED_SCHEDULER_CMDS_EXECUTED_IN_POWERSHELL'},
              'not_run':['REAL_WINDOWS_LOGON','MANUAL_TRAY_INTERACTION','NORMAL_HIDDEN_LAUNCH_USABILITY',
                         'MANUAL_PAID_AGENT_CANARIES','ACTUAL_CLI_AUTO_MODEL_TIER_CREDIT_CANARY',
                         'DESKTOP_03_SETUP_INSTALL_UPDATE_UNINSTALL','T21_T22_GENERIC_COMMUNITY_RELEASE'],
              'auto_tier_status':'AUTO_TIER_NOT_ENFORCED','quota_status':'NOT_EXPOSED',
              'acceptance_support_ids':['T01','T02','T03','T04','T05','T06','T07','T08','T09','T10','T11','T12',
                                        'T13','T14','T15','T16','T17','T20'],
              'acceptance_real_world_certification':'NOT_CLAIMED','git_publication_owner':'BRIDGE',
              'post_delivery_review_owner':'CHAT'}
    (REPORT/'evidence_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    # Scan the completed outputs too, including the manifest and verification.
    for name in scanned:
        content=(ROOT/name).read_text(encoding='utf-8')
        assert not any(re.search(pattern,content) for pattern in patterns), 'completed report secret scan failed'
    print(json.dumps({'status':'PASS','tests':suite.attrib['tests'],'changed_paths':len(changed),
                      'secret_scan':'PASS','diff_check':'PASS'}))


if __name__ == '__main__':
    main()
