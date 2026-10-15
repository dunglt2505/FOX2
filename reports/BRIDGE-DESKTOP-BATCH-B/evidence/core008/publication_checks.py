"""Publish truthful stopped 008 evidence; never operates on a runtime."""
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
EV = Path(__file__).parent
REPORT = ROOT/'reports/BRIDGE-DESKTOP-BATCH-B'
BASE = '0c739db91553ab8dd39a30b221f079b9538b0836'
sys.path.insert(0, str(ROOT/'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import secret_scan


def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT),*args])


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n', encoding='utf-8', newline='\n')


if __name__ == '__main__':
    assert git('branch','--show-current').decode().strip() == 'work/FOX2-BRIDGE-DESKTOP-BATCH-B'
    assert git('rev-parse','HEAD').decode().strip() == BASE
    assert json.loads((EV/'real_stop.json').read_text())['status'] == 'STOPPED_NEEDS_RECONCILIATION'
    assert json.loads((EV/'isolated_summary.json').read_text())['status'] == 'PASS'
    assert not (EV/'real_summary.json').exists()
    tests = json.loads((EV/'tests.json').read_text())
    assert tests['full_invocations'] == tests['focused_invocations'] == 1
    assert tests['full_exit'] == tests['focused_exit'] == 0
    assert tests['full_tests'] == 373 and tests['focused_tests'] == 29
    historical = json.loads((EV/'historical_hashes.json').read_text())
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == sha for p,sha in historical.items())
    source_path = 'agent_bridge/src/fox2_agent_bridge/installation.py'
    before = ast.parse(git('show',BASE+':'+source_path).decode())
    after = ast.parse((ROOT/source_path).read_text())
    for name in ('_installation_environment','_run'):
        find = lambda tree: next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == name)
        assert ast.dump(find(before)) == ast.dump(find(after))
    gates = {}
    for name, scope in {
        'WINDOWS_SELF_UNINSTALL_HANDOFF':'installed Python refuses before spawn/delete; stable external bootstrap synchronous deletion PASS',
        'INSTALL_SUBPROCESS_ENV_ISOLATION':'007 functions unchanged; focused regressions and packaged observed subprocesses PASS',
        'CONTAMINATED_PARENT_ENV_REGRESSION':'complete disposable install through uninstall/reinstall/restart PASS',
        'FIRST_RUN_SETUP':'disposable and real paused repeated setup PASS',
        'PER_USER_INSTALL':'disposable and exact certified real package installation PASS',
        'INSTALLER_PACKAGE':'two byte-identical package builds PASS',
        'UPDATE_PATH':'complete disposable update PASS; no second real update attempted',
        'UNINSTALL_PATH':'complete disposable stable external uninstall and owned real reconciliation PASS',
        'DURABLE_PRESERVATION_ACROSS_REINSTALL':'disposable preservation; real backup, stable hashes and original dispatch row values preserved',
        'FULL_BRIDGE_TESTS':'373 PASS; one full invocation after substantive changes',
        'CHANGED_PATH_ALLOWLIST':'explicit code/report allowlist',
        'SECRET_SCAN':'all changed publication files; no raw private backup included',
        'GIT_DIFF_CHECK':'git diff --check',
    }.items():
        gates[name] = dict(status='PASS', scope=scope)
    gates['STARTUP_SINGLE_INSTANCE'] = dict(status='PARTIAL', scope='disposable PASS; real registration and read-only canonical ownership PASS; required literal assertion failed; real Tray/Worker NOT_RUN')
    gates['SANITIZED_DIAGNOSTICS_BUNDLE'] = dict(status='PARTIAL', scope='disposable pre/post-reinstall diagnostics PASS; final real diagnostics NOT_RUN')
    gates['INSTALLED_TRAY_WORKER'] = dict(status='PARTIAL', scope='disposable PASS; real NOT_RUN after startup assertion stop')
    gates['RESTART_NO_REPLAY'] = dict(status='PARTIAL', scope='disposable restart and two fresh real installed process claim-rejections PASS; real Tray/Worker restart NOT_RUN')
    for name in ('PROJECT_DICTIONARY_BINDING','DISPATCH_V3_SCHEMA_BINDING',
                 'DISPATCH_V3_STRUCTURAL_CONFORMANCE','DISPATCH_V3_RUNTIME_COMPATIBILITY',
                 'V2_COMPATIBILITY','V06_COMPATIBILITY'):
        gates[name] = dict(status='NOT_RUN', scope='full source suite PASS; final installed-runtime certification not reached')
    for name in ('EXACT_AGENT_CONFIGURATION','FULL_ACCESS_PERMISSION'):
        gates[name] = dict(status='NOT_RUN', scope='manual execution/007 readiness evidence preserved; final installed Agent application certification not reached')
    for name in ('REAL_ELIGIBLE_FOX2_DISPATCH','RESULT_REMOTE_READBACK','USAGE_SNAPSHOT'):
        gates[name] = dict(status='NOT_RUN', scope='requires new immutable control-branch certification canary; none invented')
    gates['REAL_PER_USER_RECOVERY'] = dict(status='PARTIAL', scope='owned partial state reconciled and certified package installed; stopped before real startup/Tray/Worker certification')
    save(EV/'acceptance_gates.json', dict(status='STOPPED_NEEDS_RECONCILIATION', bridge_ready=False,
         recovered_ready_for_final_canary=False, disposable_lifecycle='PASS',
         real_root_mutated_only_after_disposable_pass=True, gates=gates))
    paths = set(git('diff',BASE,'--name-only').decode().splitlines()+
                git('ls-files','--others','--exclude-standard').decode().splitlines())
    paths |= {'reports/BRIDGE-DESKTOP-BATCH-B/dispatch_008_manifest.json',
              'reports/BRIDGE-DESKTOP-BATCH-B/evidence/core008/publication_checks.json'}
    allowed = {source_path,'agent_bridge/tests/test_installation.py','agent_bridge/README.md',
               'reports/BRIDGE-DESKTOP-BATCH-B/dispatch_008_report.md',
               'reports/BRIDGE-DESKTOP-BATCH-B/dispatch_008_manifest.json'}
    assert all(p in allowed or p.startswith('reports/BRIDGE-DESKTOP-BATCH-B/evidence/core008/') for p in paths)
    subprocess.run(['git','-C',str(ROOT),'diff','--check'],check=True)
    checks = dict(changed_path_allowlist='PASS', secret_scan='PASS', git_diff_check='PASS',
        historical_evidence_byte_preservation='PASS', historical_file_count=len(historical),
        installer_environment_007_ast_unchanged=True, full_tests=373, focused_tests=29,
        full_invocations=1, paths=sorted(paths))
    save(EV/'publication_checks.json',checks)
    artifacts = [REPORT/'dispatch_008_report.md', *sorted(EV.rglob('*'))]
    files = [dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,
                  sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in artifacts if p.is_file()]
    save(REPORT/'dispatch_008_manifest.json',dict(
        dispatch_id='FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-008', dispatch_consumed=True,
        control_commit='737e9851b2367f5e2aeb6597d0445b6df0ffcc71', source_head=BASE,
        branch='work/FOX2-BRIDGE-DESKTOP-BATCH-B', status='STOPPED_NEEDS_RECONCILIATION',
        bridge_ready=False, isolated_lifecycle='PASS', real_recovery='PARTIAL',
        real_final_state='STOPPED / PAUSED; owned logon task registered', files=files))
    for p in paths:
        secret_scan((ROOT/p).read_bytes())
    print(json.dumps({k:v for k,v in checks.items() if k != 'paths'}))
