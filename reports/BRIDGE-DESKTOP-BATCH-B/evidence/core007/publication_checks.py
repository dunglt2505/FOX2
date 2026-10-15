"""Read-only checks and bounded new evidence for stopped Dispatch 007."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
BASE = 'ce7a8253926b7489c79311e26d7dc75ba8c81fc6'
sys.path.insert(0, str(ROOT/'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import secret_scan


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def save(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2)+'\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    assert git('branch', '--show-current').decode().strip() == 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
    assert (EV/'stop.json').is_file()
    assert not (EV/'isolated_summary.json').exists()
    focused = ET.parse(EV/'focused.xml').getroot().find('testsuite')
    full = ET.parse(EV/'full.xml').getroot().find('testsuite')
    assert int(focused.attrib['tests']) == 22
    assert int(full.attrib['tests']) == 367
    for suite in (focused, full):
        assert all(int(suite.attrib[k]) == 0 for k in ('failures', 'errors', 'skipped'))
    paths = sorted(set(git('diff', BASE, '--name-only').decode().splitlines() +
                       git('ls-files', '--others', '--exclude-standard').decode().splitlines()))
    code = {'agent_bridge/src/fox2_agent_bridge/installation.py', 'agent_bridge/tests/test_installation.py'}
    reports = {'reports/BRIDGE-DESKTOP-BATCH-B/dispatch_007_report.md',
               'reports/BRIDGE-DESKTOP-BATCH-B/dispatch_007_manifest.json'}
    assert code <= set(paths)
    assert all(p in code | reports or p.startswith('reports/BRIDGE-DESKTOP-BATCH-B/evidence/core007/') for p in paths)
    historical = json.loads((EV/'historical_hashes.json').read_text())
    for p, sha in historical.items():
        assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == sha, p
    for p in paths:
        secret_scan((ROOT/p).read_bytes())
    subprocess.run(['git', '-C', str(ROOT), 'diff', '--check'], check=True)
    checks = dict(changed_path_allowlist='PASS', secret_scan='PASS', git_diff_check='PASS',
                  historical_evidence_byte_preservation='PASS', historical_file_count=len(historical),
                  paths=paths, full_tests=367, focused_tests=22, real_runtime_touched=False)
    save(EV/'publication_checks.json', checks)
    gates = {}
    for name in ('FIRST_RUN_SETUP', 'PER_USER_INSTALL', 'UPDATE_PATH', 'SANITIZED_DIAGNOSTICS_BUNDLE', 'INSTALLED_TRAY_WORKER'):
        gates[name] = dict(status='PASS', scope='disposable profile only; real-user recovery not authorized after lifecycle failure')
    gates['STARTUP_SINGLE_INSTANCE'] = dict(status='PARTIAL', scope='disposable installed launcher/Tray/Worker single instance PASS; actual logon-task registration NOT_RUN')
    gates['INSTALLER_PACKAGE'] = dict(status='PASS', scope='two byte-identical new builds')
    gates['INSTALL_SUBPROCESS_ENV_ISOLATION'] = dict(status='PASS', scope='focused tests and observed real packaged subprocesses')
    gates['CONTAMINATED_PARENT_ENV_REGRESSION'] = dict(status='PASS', scope='install and update only; entire disposable lifecycle FAIL at uninstall')
    gates['UNINSTALL_PATH'] = dict(status='FAIL', scope='first disposable installed uninstall exit 2; sanitized inner subprocess failure; no retry')
    for name in ('PROJECT_DICTIONARY_BINDING', 'DISPATCH_V3_SCHEMA_BINDING',
                 'DISPATCH_V3_STRUCTURAL_CONFORMANCE', 'DISPATCH_V3_RUNTIME_COMPATIBILITY',
                 'V2_COMPATIBILITY', 'V06_COMPATIBILITY', 'REAL_ELIGIBLE_FOX2_DISPATCH',
                 'EXACT_AGENT_CONFIGURATION', 'FULL_ACCESS_PERMISSION', 'RESULT_REMOTE_READBACK',
                 'USAGE_SNAPSHOT', 'RESTART_NO_REPLAY', 'REINSTALL', 'DURABLE_PRESERVATION_ACROSS_REINSTALL',
                 'REAL_PER_USER_RECOVERY'):
        gates[name] = dict(status='NOT_RUN', scope='final installed-runtime certification not reached; preflight/source tests do not discharge this gate')
    gates['FULL_BRIDGE_TESTS'] = dict(status='PASS', scope='367 tests, one invocation, exact changed code before packaging')
    for name, key in (('CHANGED_PATH_ALLOWLIST', 'changed_path_allowlist'), ('SECRET_SCAN', 'secret_scan'), ('GIT_DIFF_CHECK', 'git_diff_check')):
        gates[name] = dict(status=checks[key], scope='new 007 publication files')
    save(EV/'acceptance_gates.json', dict(status='STOPPED_NEEDS_RECONCILIATION', bridge_ready=False,
         isolated_lifecycle='FAIL', real_runtime_touched=False, gates=gates))
    report_root = ROOT/'reports/BRIDGE-DESKTOP-BATCH-B'
    artifacts = [report_root/'dispatch_007_report.md', *sorted(EV.rglob('*'))]
    files = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size,
                  sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in artifacts if p.is_file()]
    manifest = dict(dispatch_id='FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-007',
                    source_head=BASE, branch='work/FOX2-BRIDGE-DESKTOP-BATCH-B',
                    control_commit='7bac9176a24bbcbdd49f2074f88d355c5d88d906',
                    status='STOPPED_NEEDS_RECONCILIATION', bridge_ready=False,
                    real_runtime_touched=False, dispatch_consumed=True, files=files)
    save(report_root/'dispatch_007_manifest.json', manifest)
    secret_scan((report_root/'dispatch_007_manifest.json').read_bytes())
    for p in EV.rglob('*'):
        if p.is_file():
            secret_scan(p.read_bytes())
    print(json.dumps(checks, indent=2))
