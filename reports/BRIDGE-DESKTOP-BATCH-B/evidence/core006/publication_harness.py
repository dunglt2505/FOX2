"""Publish the terminal 006 evidence only; never resume its test harness."""
import datetime, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(r'C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DESKTOP-BATCH-B')
OUT=ROOT/'reports/BRIDGE-DESKTOP-BATCH-B'; EV=OUT/'evidence/core006'
BASE='28550c49f07075c80cd730da9be80c72e5bc5e76'
CONTROL='fa262cebc3965a1c32042aceb4742326a4533ed7'
BRANCH='work/FOX2-BRIDGE-DESKTOP-BATCH-B'
sys.path.insert(0,str(ROOT/'agent_bridge/src'))
from fox2_agent_bridge.preexec.engine import writer_lock, competing_writer, secret_scan

def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args])
def write(path,value): path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n',encoding='utf-8',newline='\n')
def digest(raw): return hashlib.sha256(raw).hexdigest()

with writer_lock(ROOT):
    assert git('rev-parse','HEAD').decode().strip()==BASE
    assert git('branch','--show-current').decode().strip()==BRANCH
    assert not competing_writer(ROOT)
    launch=json.loads((EV/'launch.json').read_text()); stop=json.loads((EV/'stop.json').read_text())
    assert stop['dispatch_consumed'] and stop['no_retry']
    assert all(digest((ROOT/p).read_bytes())==h for p,h in launch['prior_evidence_hashes'].items())
    isolated=Path(launch['disposable_runtime_root'])
    assert isolated.resolve().is_relative_to(Path('C:/Temp/fox2-core006-u_7p0m_1').resolve())
    assert not (isolated/'current.json').exists()
    assert list((isolated/'versions').iterdir())==[]
    write(EV/'terminal.json',{
        'status':'STOPPED_NEEDS_RECONCILIATION','dispatch_consumed':True,'max_runs':1,'no_retry':True,
        'stopped_gate':'PER_USER_INSTALL','installed_command_exit_code':1,
        'failure_detail_limit':'Harness captured the nonzero installation command status but did not persist its stderr. Exact inner installation exception/root cause is UNKNOWN; do not infer an uninstall defect or source defect.',
        'disposable_root':str(isolated),'pointer_exists':False,'version_directories_remaining':0,
        'install_rollback_observation':'Empty versions directory and no current.json after failed install; no durable user data was present in this new profile.',
        'quarantined_runtime':'No reads, writes, launches, restarts, pointer operations, uninstall, or process termination directed at the real per-user runtime.',
        'source_code_changes':False,'prior_reports_byte_preserved':True,'prior_dispatches_replayed':False,
        'full_pytest_invocations':0,'installed_fixture_invocations':0,'uninstall_lifecycle_invocations':0,
        'host_tooling_modified':False,'disposable_assets_retained_for_diagnosis':True,
        'execution_note':'One integrated attempt stopped at first required Core test failure. The harness is evidence, not authorization to rerun it.'})
    d=json.loads(git('show',CONTROL+':docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-DESKTOP-BATCH-B-CODEX-006.json'))
    gates=[]
    for name in d['required_tests']:
        status='NOT_RUN'; reason='Stopped at isolated PER_USER_INSTALL before this installed-runtime acceptance check.'
        evidence=['evidence/core006/terminal.json']
        if name=='PER_USER_INSTALL':
            status='FAIL'; reason='Verified package installation command in the isolated profile exited 1. Exact inner exception was not retained; no retry.'
        elif name=='INSTALLER_PACKAGE':
            status='PASS'; reason='Two isolated builds of the pinned source produced byte-identical offline packages; package construction only, installation failed separately.'; evidence=['evidence/core006/package.json','evidence/core006/build_environment.json']
        elif name=='UNINSTALL_PATH':
            status='DEFERRED_OWNER_PRIORITY'; reason='Owner deferred uninstall; historical FAIL remains factual. No uninstall lifecycle or repair attempted.'
            evidence=['dispatch_005_report.md','evidence/dispatch_004_stop.json']
        elif name in ('PROJECT_DICTIONARY_BINDING','DISPATCH_V3_SCHEMA_BINDING','DISPATCH_V3_STRUCTURAL_CONFORMANCE','DISPATCH_V3_RUNTIME_COMPATIBILITY','V2_COMPATIBILITY','V06_COMPATIBILITY'):
            reason='Immutable launch hashes/schema checks passed where applicable; current installed-runtime compatibility certification was not reached. Carry-forward debt remains.'; evidence=['evidence/core006/launch.json','evidence/core006/terminal.json']
        elif name in ('EXACT_AGENT_CONFIGURATION','FULL_ACCESS_PERMISSION'):
            reason='Fresh pinned CODEX/gpt-6.1-sol/medium/FULL_ACCESS launch probe passed; installed Bridge execution/configuration attestation was not reached.'; evidence=['evidence/core006/launch.json']
        elif name=='RESULT_REMOTE_READBACK':
            reason='NOT_RUN at the commit snapshot. This report-only publication is verified afterward by exact remote ref, fetch, parent, path and byte readback; host-observed receipt is emitted separately to avoid commit self-reference.'
        elif name in ('CHANGED_PATH_ALLOWLIST','SECRET_SCAN','GIT_DIFF_CHECK'):
            status='PASS'; reason='Final publication checks, repeated before commit; see verification.json.'; evidence=['evidence/core006/verification.json']
        gates.append({'gate':name,'status':status,'reason':reason,'evidence':evidence})
    assert len(gates)==24 and len({g['gate'] for g in gates})==24
    write(EV/'acceptance_gates.json',{'snapshot':'before report commit; post-push publication proof is a separate host-observed receipt','gates':gates,'count':24,'internal_fox2_bridge_ready':False,'bridge_core_validated':False})
    report='''# FOX2 Dispatch 006 — isolated Core attempt stopped

Status: STOPPED_NEEDS_RECONCILIATION. Dispatch 006 consumed exactly once; no replay or automatic retry. BRIDGE_CORE_VALIDATED is not earned. INTERNAL_FOX2_BRIDGE_READY=NO.

Control commit: fa262cebc3965a1c32042aceb4742326a4533ed7. Source HEAD: 28550c49f07075c80cd730da9be80c72e5bc5e76. Branch: work/FOX2-BRIDGE-DESKTOP-BATCH-B. The complete immutable Dispatch JSON and CORE-006 prompt were read from Git; all Dictionary/Policy/Task/Prompt hashes, prompt blob identity and full Dispatch-v3 structural validation passed at launch. The existing PASS PreExec receipt is published by source HEAD and binds its receipt-only parent e8598a1a2933fe3c640bfb4c34c3cbfd59b37ed2; that relationship was explicitly verified.

The exact clean worktree, matching remote source, no observed competing writer, exclusive worktree OS lock, required Windows tools and a fresh pinned Codex auth/capacity response probe passed. Requested route: CODEX / PINNED / gpt-6.1-sol / medium / FULL_ACCESS (danger-full-access, approval never). This is launch evidence, not installed-runtime certification.

The disposable profile was C:\\Temp\\fox2-core006-u_7p0m_1\\user. Its runtime resolved to C:\\Temp\\fox2-core006-u_7p0m_1\\user\\AppData\\Local\\FOX2\\AgentBridge, disjoint from the quarantined per-user runtime. Only test assets and an isolated build venv were created there. The installed runtime was never read, launched, repaired, restarted, uninstalled, or pointed elsewhere. No host-user startup task was changed.

Two complete package builds produced identical SHA-256 6e96ee19ea103e7bd606a63abf071d00de6fa3c6cd1663b8d9d921b01d70b3a9. The isolated build used Python 3.13.15, setuptools 84.0.0 and pinned dependency versions recorded in build_environment.json. The host Python environment was not changed. Package evidence records the full manifest and both build identities.

PER_USER_INSTALL failed: the source installer command targeting the disposable profile exited 1. The harness retained its command status but did not retain stderr, so the exact inner exception and root cause are UNKNOWN. No source defect or uninstall cause is asserted. Subsequent read-only inspection of the disposable runtime found no current.json and an empty versions directory. The attempt stopped at this required Core gate; there was no installation retry, lifecycle recovery, source edit, second DEV run or full pytest invocation. The harness is retained as provenance and must not be treated as replay authorization.

FIRST_RUN_SETUP, UPDATE_PATH, startup/login, installed Tray/Worker, diagnostics, installed compatibility, eligible dispatch/result, installed route enforcement, usage, restart/no-replay and full Bridge tests were not reached. Source prechecks do not discharge the six installed compatibility obligations. Historical 354-test and 004 focused/lifecycle evidence remains historical, without recertification.

All 24 original gate identities are recorded in evidence/core006/acceptance_gates.json: four fresh PASS at the pre-publication snapshot (package construction, changed-path allowlist, secret scan, diff check), one FAIL (isolated per-user install), one DEFERRED_OWNER_PRIORITY (uninstall), eighteen NOT_RUN. The report-only remote readback is pending at this immutable snapshot and is emitted separately after publication. Successful publication does not turn the failed Core run into a PASS.

UNINSTALL_PATH=DEFERRED_OWNER_PRIORITY; its historical failure remains factual. No uninstall fix was attempted. Prior code, tests, reports and claims for Dispatches 001–005 are preserved byte-for-byte, and none was replayed. Only new reports/BRIDGE-DESKTOP-BATCH-B files are published. Disposable test assets remain for bounded diagnosis; no cleanup or uninstall was performed.

Delivery is one report-only commit/push on the authorized non-main task branch. Exact remote SHA, fetched commit, parent, changed paths and every published artifact's bytes must be read back before PUSHED_UNREVIEWED is reported. A host-observed receipt avoids embedding a commit's own SHA in its contents. CHAT owns independent acceptance. No PR, main, merge, deploy, provider, broker or LIVE action occurred.
'''
    (OUT/'dispatch_006_report.md').write_text(report,encoding='utf-8',newline='\n')
    shutil_copy=Path(__file__).read_bytes(); (EV/'publication_harness.py').write_bytes(shutil_copy)
    changed=[p.decode() for p in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if p]
    assert not git('diff','--name-only').strip() and not git('diff','--cached','--name-only').strip()
    assert all(p.startswith('reports/BRIDGE-DESKTOP-BATCH-B/') for p in changed)
    write(EV/'verification.json',{'status':'PASS','initial_source':BASE,'changed_path_allowlist':'PASS','secret_scan':'PASS','git_diff_check':'PASS','prior_reports_hash_check':'PASS','source_and_tests_unchanged':True,'changed_paths_before_final_manifest':changed,'publication_scope':'report-only','remote_readback_at_snapshot':'PENDING_HOST_OBSERVED_RECEIPT'})
    files=[p for p in EV.rglob('*') if p.is_file()]+[OUT/'dispatch_006_report.md']
    write(OUT/'dispatch_006_manifest.json',{'dispatch_id':d['dispatch_id'],'control_commit':CONTROL,'source_head':BASE,'status':'STOPPED_NEEDS_RECONCILIATION','delivery_owner':'AGENT','branch':BRANCH,'result_remote_sha':'HOST_OBSERVED_POINTER_AFTER_PUSH','bridge_ready':False,'core_validated':False,'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size} for p in sorted(files)],'manifest_self_hash':'Excluded; verified against committed/fetched bytes'})
    new=[p.decode() for p in git('ls-files','--others','--exclude-standard','-z').split(b'\0') if p]
    for name in new:
        raw=(ROOT/name).read_bytes(); secret_scan(raw)
        assert not re.search(rb'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|\bBearer\s+[A-Za-z0-9_.-]{16,}',raw)
        assert not raw.startswith(b'\xef\xbb\xbf') and b'\r\n' not in raw
    git('add','--',*new); git('diff','--cached','--check')
    staged=[p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p]
    assert set(staged)==set(new)
    git('commit','-m','FOX2 Dispatch 006: record isolated Core install failure; defer uninstall')
    head=git('rev-parse','HEAD').decode().strip()
    assert git('rev-parse','HEAD^').decode().strip()==BASE
    assert not git('status','--porcelain=v1','--untracked-files=all').strip()
    assert not competing_writer(ROOT)
    expected={p:git('show',head+':'+p) for p in staged}
    git('push','origin','HEAD:refs/heads/'+BRANCH)
    remote=git('ls-remote','--refs','origin','refs/heads/'+BRANCH).decode().split()[0]
    assert remote==head
    git('fetch','origin','refs/heads/'+BRANCH)
    fetched=git('rev-parse','FETCH_HEAD').decode().strip(); assert fetched==head
    assert all(git('show',fetched+':'+p)==raw for p,raw in expected.items())
    assert git('diff',BASE,fetched,'--name-only','-z').split(b'\0')==git('diff',BASE,head,'--name-only','-z').split(b'\0')
    receipt={'delivery':'PUSHED_UNREVIEWED','execution':'STOPPED_NEEDS_RECONCILIATION','dispatch_consumed':True,'dispatch_runs':1,'source_head':BASE,'result_commit':head,'remote_ref':remote,'fetched_commit':fetched,'parent':BASE,'branch':BRANCH,'remote_artifact_byte_readback':'PASS','changed_paths':staged,'changed_path_count':len(staged),'result_remote_readback':'PASS_REPORT_PUBLICATION_ONLY','core_validated':False,'bridge_ready':False,'worktree_clean':not git('status','--porcelain=v1','--untracked-files=all').strip(),'verified_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    metadata=Path(git('rev-parse','--absolute-git-dir').decode().strip())
    write(metadata/'fox2-dispatch-006-publication-readback.json',receipt)
    print(json.dumps(receipt,indent=2))
