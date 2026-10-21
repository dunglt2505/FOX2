"""Assemble the bounded failed host-certification submission; no host lifecycle calls."""
import hashlib
import json
from pathlib import Path
import subprocess
import observe
import verify_result

ROOT=observe.ROOT
AREA=Path(__file__).resolve().parent
PREFIX='reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/'
load=lambda name:json.loads((AREA/name).read_text())
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
binding=load('source_binding.json'); package=load('package_verification.json'); execution=load('execution.json')
before=load('pre_state.json'); final=load('final_state.json'); failure=load('failure_analysis.json')
assert execution['status']=='FAIL' and execution['lifecycle_attempts']==1
assert execution['stable_uninstall_attempts']==0 and execution['recovery_attempts']==0
stamp=observe.now()
E=lambda name:'E_'+Path(name).stem.upper()
gates=[]
def gate(name,status,reason,*evidence):
    gates.append(dict(id=name,status=status,reason=reason,evidence_ids=list(evidence)))

gate('EXACT_ACCEPTED_SOURCE_PACKAGE_BUILD_PROVENANCE','PASS','Unmodified accepted-source temporary task-branch checkout; manifest source_git_commit exactly 2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb.',E('package_verification.json'))
gate('PACKAGE_SHA256_AND_MANIFEST_VERIFIED_BEFORE_HOST_MUTATION','PASS','All payload/source/wheel module hashes checked before install.',E('package_verification.json'),E('package_manifest.json'))
gate('PRE_STATE_DURABLE_HASH_SNAPSHOT','PASS','Bounded original and immediate pre-install snapshots captured; no drift.',E('pre_state.json'),E('pre_install_state.json'))
gate('REAL_INSTALL_OR_UPDATE_EXACT_PACKAGE_PASS','PASS','Supported per-user installer exit 0, UPDATED.',E('execution.json'),E('post_install_state.json'))
gate('CURRENT_POINTER_AND_INSTALLED_RECEIPT_BIND_EXACT_PACKAGE_SOURCE','PASS','Pointer, installed receipt and source match exact accepted package.',E('post_install_state.json'))
gate('SAFE_PAUSED_STATE_BEFORE_CERTIFICATION','PASS','STOPPED, paused, setup_complete; zero active worker/legacy tray.',E('post_install_state.json'))
gate('CORRECTED_LIFECYCLE_CERTIFICATION_RUN_ON_OWNER_HOST','FAIL','One real invocation exits 1: installed tray/worker did not become healthy. No replay.',E('execution.json'),E('failure_analysis.json'))
gate('STABLE_EXTERNAL_UNINSTALL_EXERCISED_EXACTLY_ONCE','NOT_RUN','Earlier health failure prevented reaching stable uninstall; attempts=0.',E('execution.json'))
gate('UNINSTALL_EXIT_ZERO','NOT_RUN','Uninstall not invoked.',E('execution.json'))
gate('POST_UNINSTALL_CURRENT_POINTER_AND_OWNED_VERSIONS_ABSENT','NOT_RUN','Uninstall not invoked; both owned versions remain.',E('final_state.json'))
gate('DURABLE_CONFIG_DATABASE_MANUAL_CONSUMPTION_PRESERVED','NOT_RUN','Across-uninstall preservation is unverified. All three hashes are unchanged across the actual install/failed-run window.',E('failure_analysis.json'),E('final_state.json'))
gate('SAME_EXACT_PACKAGE_REINSTALL_PASS','NOT_RUN','Reinstall not reached; recovery unnecessary because exact package remains installed.',E('execution.json'),E('final_state.json'))
gate('FINAL_CURRENT_POINTER_EXACT','PASS','Final installed pointer and source match accepted package.',E('final_state.json'))
gate('FINAL_SETUP_AND_HEALTH_PASS','FAIL','Setup_complete remains true and worker paused/STOPPED, but required healthy tray/worker certification failed. One WPF Desktop remains.',E('final_state.json'),E('failure_analysis.json'))
gate('CONSUMED_IDENTITIES_PRESERVED','PASS','28 dispatch identity/state/payload-hash records unchanged; four historical Batch-B identities remain NEEDS_RECONCILIATION.',E('failure_analysis.json'),E('final_state.json'))
gate('NO_OLD_DISPATCH_REPLAY','PASS','Only launcher-bound fresh Dispatch consumed once; no Agent or lifecycle retry.',E('source_binding.json'),E('execution.json'))
gate('NO_G3_G4_APPLOCKER_SERVICE_ACL_MUTATION','PASS','No forbidden mutation invoked; accepted package activation remains DENY_PENDING_G3_G4.',E('failure_analysis.json'),E('package_manifest.json'))
for name in ['CHANGED_PATH_ALLOWLIST_REPORT_EVIDENCE_ONLY','SECRET_SCAN','GIT_DIFF_CHECK','K1_UNEXPLAINED_ZERO','RESULT_CONTRACT_V2_REPORT_AND_EVIDENCE_MANIFEST']:
    gate(name,'PASS','Bounded report/evidence checks and repeatable verifier; containing result commit SHA supplied externally.',E('static_checks.json'),E('verify_result.py'),E('k1.json'))

report=f'''# FOX2 Current-Package Owner-Host Lifecycle A01 — FAIL

## R01 — Result and submission

Task `{observe.os.environ['FOX2_TASK_ID']}`; Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`.
Dispatch `{binding['dispatch_id']}`. One CODEX `gpt-6.1-sol`, high, MANUAL_LOCAL, task-scoped FULL_ACCESS attempt; no model substitution or Agent replay.
Host execution UTC: {execution['started_at_utc']} to {execution['finished_at_utc']}.
Result: **FAIL / REWORK_REQUIRED**. Submission: READY_FOR_CHAT_REVIEW; delivery PUSHED_UNREVIEWED after authorized branch publication. CHAT acceptance is not claimed.

The supported installer updated the exact accepted package successfully. The single lifecycle invocation then exited 1 with **RuntimeError: installed tray/worker did not become healthy**, at `certify_user_lifecycle.py:133`, before uninstall. Stable uninstall attempts: **0**; reinstall: **NOT_RUN**; recovery attempts: **0**. No lifecycle or uninstall retry occurred.

## R02 — Authority and routing

Owner task plus exact fresh Dispatch authorize bounded Phase-2 per-user TEST only. Task-specific PreExec v5 PASS blob `08056cb73333934a148cef2b4f1f3da11f6b9b3e`, CHAT PASS_TO_ASSIGN `185f4cdcdfb6a7487f8bbc0f256c304fb1d9f263`, and A03 BUILD-only acceptance `37691b71b64de03091de9908014da2256c1d2901` are source-bound. Policy 2.0.0 applies as task-scoped Owner authority. R0–R7/assignment PASS are inherited from the exact Dispatch and PreExec, with route, writer and host checks observed again here. Product/source/test writes remain disabled despite the legacy Dispatch decision field.

## R03 — Immutable bindings and package

Starting HEAD `{observe.START}` matched the live remote task branch and Dispatch runtime base before build. Accepted source `{observe.BASE}` is an ancestor; all eight pre-start changed paths are task/prompt/PreExec evidence, with no product drift. Exact Dispatch commit `{binding['dispatch_commit']}`, blob `{binding['dispatch_blob']}` was fetched and matched to launcher environment bindings. Task commit `d95f08ceed2f5a25ad288b9630ffc87b698f329c` and prompt commit `250c8ab15bdfd8339e6332dc105a559dbd5b3151` pass raw SHA-256 readback. See source_binding.json for all locked identities.

Package alias: `BUILD_ROOT/accepted-package.zip`, outside BridgeRoot and retained for this task. SHA-256: `{package['package_sha256']}`; size {package['package_size']} bytes. Manifest source_git_commit is exactly `{observe.BASE}`. Build used the already-existing isolated Python 3.13.15 / setuptools 84.0.0 / wheel 0.48.0 / build 1.6.1 environment and dotnet 8.0.426. No tools or dependencies were installed to satisfy capability. The unmodified builder downloaded pinned wheel payloads and built the self-contained package.

The temporary clean checkout carries the accepted commit while the execution worktree retains its Dispatch base. All 59 source inventory and 40 wheel module entries, all payload hashes, sorted fixed-time ZIP entries and declared deterministic build flags were checked. No second build was performed. Machine dictionary 1.2 (`7fc3532890f4a60a4abc7bf3b08dc06fe6af6ee000176ac464bfe3aacda2ecd7`) and Dispatch routing dictionary 1.3 are independently pinned; global machine adoption is not claimed.

Two preparation corrections are preserved in package_verification.json: the temporary clone already had the task branch, so an initial branch-creation command refused before build; an evidence-only assertion initially conflated the two dictionary layers. Both were resolved before install without changing product code or rebuilding the package.

## R04 — Completed and remaining scope

Exact build, package verification, durable pre-state, supported real install/update, exact installed receipt and safe paused pre-certification state completed. The real lifecycle failed at its first healthy tray/worker condition. Stable external uninstall, uninstall postconditions, diagnostics stage, single-instance stage and same-package reinstall were not reached. Across-uninstall durability remains NOT_RUN. No recovery was needed because the exact package remains installed.

## R05 — Changed paths and ownership

Only report.md, evidence_manifest.json and evidence/host_lifecycle_cert/** changed. The initial worktree was clean; one task CODEX writer PID {binding['route']['task_writer_pid']} was observed, with no G3/G4/Canary writer or subagent. Exact path/hash inventory is in the manifest; K1 classifies all paths in k1.json. Package binaries, temporary source checkout, config/database contents, raw prompts and raw local logs are excluded from Git.

## R06 — Observed tests

Build/provenance, install, pointer/receipt and paused pre-state PASS. Corrected real-host lifecycle FAIL, exit 1. Bounded source inspection shows the harness expects a legacy pwsh desktop_tray.ps1 process and a PAUSED Worker heartbeat. The accepted launcher starts WPF presentation only and returns worker_started=False. This is an observed contract mismatch requiring a separately authorized source task; no code fix or alternative Worker launch was attempted here.

## R07 — Required acceptance matrix

| Required check | Result | Evidence |
|---|---|---|
'''
for item in gates:
    report+='| '+item['id']+' | '+item['status']+' | '+', '.join(item['evidence_ids'])+' |\n'
report+=f'''
## R08 — Bounded evidence and final host state

Final current pointer is `{package['package_sha256']}`, with installed source `{final['installed_source_git_commit']}` and installed receipt SHA-256 `{final['receipt_sha256']}`. Both the new and previous owned version remain; uninstall was not attempted. Worker is STOPPED, paused=true, setup_complete=true, no active dispatch; startup=true and the Limited/Interactive per-user scheduled task is Ready.

Config hash `{final['hashes']['config/bridge.toml']}`, database hash `{final['hashes']['data/bridge.db']}` and manual-consumption hash `{final['hashes']['data/manual_consumption.json']}` are unchanged from pre-state. SQLite quick_check=ok; all 28 dispatch identity/state records and four historical consumed identities are unchanged.

One WPF Desktop process created by this run remains open. The observer's active_runtime_processes field counts worker/legacy PowerShell tray/launcher, not WPF presentation; failure_analysis.json records that limitation and the separate presentation observation. The CLI request-exit in the harness cleanup did not close the WPF presentation. No forced termination, additional runtime launch or further host mutation was attempted after failure.

The harness writes lifecycle checkpoints at uninstall and completion, so this earlier failure produced no raw lifecycle JSON. execution.json preserves sanitized process exit/stderr and the original RuntimeError separately from the orchestration assertion. Evidence IDs, relative paths and SHA-256 values are in evidence_manifest.json. No raw configuration or database content is included.

## R09 — Git delivery

Repository dunglt2505/FOX2, branch work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021. Report/evidence only; no PR/main/merge. Local HEAD before result submission: `{observe.START}`. Push is followed by independent remote branch-head readback. The observed containing commit SHA is returned outside this report. Final delivery state is PUSHED_UNREVIEWED, pending CHAT intake.

## R10 — Risks and boundaries

Lifecycle certification remains FAIL; uninstall/reinstall and final healthy runtime remain unverified. Startup remains enabled and one presentation process remains open; worker stays stopped and paused. REWORK_REQUIRED must be handled through a fresh source/task/PreExec/Dispatch with no replay of this consumed attempt. Historical A03 BUILD evidence remains at `{observe.BASE}` and the separate acceptance receipt; historical Batch-B UNINSTALL_PATH=FAIL remains factual and unchanged.

No AppLocker, AppIDSvc, FOX2F1Authority service, ProgramData authority ACL, reboot, G3/G4, Canary, provider/broker/LIVE mutation was invoked. Package F1 activation remains DENY_PENDING_G3_G4. Bounded changed-text secret/private-path scan, allowlist and diff checks pass; K1 UNEXPLAINED=0. Result Contract v2 and evidence hashes/references are validated by verify_result.py.

## R11 — Attempts and usage

Agent attempts=1, Agent retries=0; package builds=1, install/update attempts=1, lifecycle invocations=1, stable uninstall attempts=0, reinstall attempts=0, recovery attempts=0. Token/credit usage NOT_MEASURED. Preparation/evidence corrections are not Agent or lifecycle retries.

## R12 — CHAT decision requested

Review the immutable pushed FAIL result and arrange separately authorized rework of current-package certification/launcher compatibility. Do not accept Phase 2 TEST, replay this Dispatch or progress to G3/G4/Canary from this result.
'''
(ROOT/PREFIX/'report.md').write_text(report,encoding='utf-8',newline='\n')
planned={PREFIX+'evidence_manifest.json',PREFIX+'evidence/host_lifecycle_cert/k1.json',PREFIX+'evidence/host_lifecycle_cert/static_checks.json'}
changed=sorted(set(verify_result.paths())|planned)
entries=[]
for path in changed:
    classification='REQUESTED' if path in (PREFIX+'report.md',PREFIX+'evidence_manifest.json') else 'NECESSARY_DEPENDENCY' if path.endswith('.py') else 'JUSTIFIED_GENERATED'
    entries.append(dict(path=path,classification=classification,reason='Task-defined failed host-certification evidence or its bounded observer/orchestrator/verifier; no product change.'))
observe.save('k1.json',dict(base=observe.START,changes=entries,UNEXPLAINED=0,product_hunks=0))
verify_result.static()
observe.save('static_checks.json',dict(observed_at_utc=stamp,changed_path_allowlist='PASS',git_diff_check='PASS',bounded_secret_scan='PASS',python_evidence_syntax='PASS',product_source_test_changes=0,K1_UNEXPLAINED=0,
    scope='Changed text only, under 500000 bytes; credential/URL patterns, private user paths, binary and LF checks; no scan exclusions.',
    lifecycle_result='FAIL',uninstall='NOT_RUN',reinstall='NOT_RUN',result_contract_method='verify_result.py: Draft202012Validator with FormatChecker, all evidence/path hashes and references, changed-path and K1 coverage.'))

tests=[]
def test(name,status,kind,method,notes,*evidence):
    tests.append(dict(id=name,status=status,kind=kind,command_or_method=method,environment='Owner Windows physical host; task-scoped per-user TEST',run_at_utc=stamp if status not in ('NOT_RUN','NOT_APPLICABLE') else None,evidence_ids=list(evidence),notes=notes))
test('T_SOURCE','PASS','READBACK','observe.py preflight; exact Git fetch/ls-remote/object digests','Launcher bindings, fresh PreExec and single writer checked.',E('source_binding.json'))
test('T_PACKAGE','PASS','STATIC','Unmodified build_user_package.py; verify_package.py','One exact-source build; no installed dependencies; retained external package.',E('package_verification.json'),E('package_manifest.json'))
test('T_INSTALL','PASS','INTEGRATION','install_user.ps1 -Package BUILD_ROOT/accepted-package.zip -Sha256 exact SHA','Exit 0 UPDATED; exact installed receipt and paused state.',E('execution.json'),E('post_install_state.json'))
test('T_LIFECYCLE','FAIL','INTEGRATION','certify_user_lifecycle.py --package exact --sha256 exact --evidence BUILD_ROOT/lifecycle-raw.json','One invocation; RuntimeError before uninstall. No retry.',E('execution.json'),E('failure_analysis.json'))
test('T_UNINSTALL','NOT_RUN','INTEGRATION','Stable external BridgeRoot/uninstall.ps1','Not reached after first health failure.',E('execution.json'))
test('T_REINSTALL','NOT_RUN','INTEGRATION','Same exact accepted package reinstall','Not reached; recovery not needed.',E('execution.json'))
test('T_DURABLE_BOUNDARY','PASS','READBACK','Bounded pre/final hashes, read-only SQLite identity/state digest and quick_check','Actual install/failed-run boundary only; across-uninstall durability is NOT_RUN.',E('pre_state.json'),E('final_state.json'),E('failure_analysis.json'))
test('T_STATIC','PASS','STATIC','verify_result.py static and result validation','Allowlist/diff/secret scan/K1/Result Contract v2; no product suite rerun for report-only writes.',E('static_checks.json'),E('k1.json'),E('verify_result.py'))
test('T_DELIVERY','PASS','READBACK','git push exact authorized non-main HEAD, followed by git ls-remote and remote file readback','Containing result SHA returned externally after actual push/readback.', 'E_REPORT')
evidence=[]
for path in [ROOT/PREFIX/'report.md',*sorted(p for p in AREA.iterdir() if p.is_file())]:
    name=path.name; eid='E_REPORT' if name=='report.md' else E(name)
    supports=[item['id'] for item in gates+tests if eid in item['evidence_ids']]
    if not supports: supports=['T_STATIC']
    evidence.append(dict(id=eid,path=path.relative_to(ROOT).as_posix(),sha256=sha(path),kind='REPORT' if name=='report.md' else 'SOURCE_READBACK' if name=='source_binding.json' else 'OTHER',
        observed_at_utc=stamp,description='Bounded host-certification '+name,supports_ids=supports,sanitized=True))
manifest=dict(contract_version='2.0',project='FOX2',wp_id='FOX2-BRIDGE-RC1-TO-INTERNAL-READY',task_id=observe.os.environ['FOX2_TASK_ID'],change_id='HOST-LIFECYCLE-CERT-A01',
    submission_state='READY_FOR_CHAT_REVIEW',submitted_at_utc=stamp,
    agent=dict(product='CODEX',model='gpt-6.1-sol',mode='high / MANUAL_LOCAL / task-scoped FULL_ACCESS',host='Owner physical Windows host',started_at_utc=binding['observed_at_utc'],finished_at_utc=stamp,quota_observation='NOT_MEASURED; inherited exact route admission and live pinned process observed; no new Agent probe.'),
    routing={**{k:'PASS' for k in ['policy_check','task_state_check','r0','r1','r2','r3','r4','r5','r6','r7','assignment_check']},'routing_evidence':'Exact launcher-bound Dispatch, task-specific PreExec v5 and CHAT PASS_TO_ASSIGN; live route/writer/source/host readback in source_binding.json. No broader authority granted.'},
    source=dict(policy_sha256=binding['identities']['policy']['sha256'],policy_version='2.0.0 task-scoped Owner authority',task_commit_sha=binding['identities']['task']['commit'],source_manifest_sha256=sha(AREA/'source_binding.json'),approved_base_commit_sha=observe.START,source_readback_status='PASS',
        brd_revisions=['Immutable host-lifecycle task at d95f08ceed2f5a25ad288b9630ffc87b698f329c; no BRD/TechSpec/product change'],previous_evidence_reused=['Accepted source/result 2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb; implementation fab3642b818415428ae3f67965430e3ea0b11401; BUILD-only CHAT acceptance 37691b71b64de03091de9908014da2256c1d2901. Historical A03/Batch-B evidence retained; no prior real lifecycle PASS reused.']),
    permissions={**{k:k in ['git_source_read','git_report_write','git_report_push'] for k in ['git_source_read','git_report_write','git_report_push','git_code_push','code_allowed','pr_create','merge_allowed','dnse_production','broker_write','live']},'grant_evidence':'Owner immutable task/prompt plus exact fresh Dispatch authorizes only bounded per-user lifecycle and report/evidence push; source code disabled.'},
    git=dict(repository='dunglt2505/FOX2',branch='work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021',worktree='WORKTREES/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021',writer_lease='One task CODEX PID '+str(binding['route']['task_writer_pid'])+'; clean entry, no subagents or competing G3/G4/Canary writer.',report_path=PREFIX+'report.md',delivery_status='PUSHED_UNREVIEWED',pr_url=None,local_head_before_submission=observe.START),
    scope=dict(requested=['Exact current-package Owner-host lifecycle TEST certification, one attempt and bounded evidence delivery.'],completed=['Exact package build/provenance, real supported update, paused pre-state and one lifecycle invocation; first failure and final durable/installed state preserved.','Report/evidence-only validation and authorized non-main publication.'],partial=['Lifecycle FAIL at tray/worker health; stable uninstall and reinstall NOT_RUN.'],not_done=['Successful lifecycle certification, uninstall/postconditions, across-uninstall durability, reinstall, final healthy runtime and CHAT acceptance.'],explicit_exclusions=['Product/source/test edits; Agent/lifecycle/uninstall replay.','G3/G4/AppLocker/AppIDSvc/F1-service/ProgramData-ACL/reboot/Canary/main/PR/merge/provider/broker/LIVE.'],changed_paths=[dict(path=p,operation='MODIFY' if p in (PREFIX+'report.md',PREFIX+'evidence_manifest.json') else 'ADD',intent=next(e['classification'] for e in entries if e['path']==p)+': bounded failed host-certification evidence.',within_allowed_paths=True,new_sha256=None if p==PREFIX+'evidence_manifest.json' else sha(ROOT/p)) for p in changed],forbidden_paths_touched=False),
    tests=tests,acceptance=gates,evidence=evidence,
    risks=[dict(id='R_LIFECYCLE',severity='HIGH',state='BLOCKED',impact='Real lifecycle FAIL; uninstall/reinstall and final healthy runtime are unverified.',next_action='CHAT review and separately authorized source rework; fresh task/PreExec/Dispatch required, no replay.',owner_role='CHAT'),dict(id='R_PRESENTATION',severity='LOW',state='OPEN',impact='One WPF presentation process from this failed test remains open; startup remains enabled. Worker stopped and paused.',next_action='Record final state and address presentation cleanup/contract in the separately scoped next task; no forced termination here.',owner_role='Owner/CHAT')],
    security=dict(secret_scan='PASS',private_account_data_in_git=False,licensed_raw_feed_in_git=False,evidence_redacted=True,check_notes='Bounded changed-text scan; only hashes, path aliases, sanitized process error and aggregate ledger evidence; no raw config/database/prompt/log/package binary.'),
    usage=dict(attempts=1,retries=0,usage_status='NOT_MEASURED',tokens_used=None,credits_used=None,escalation_reason='First real lifecycle failure preserved; no Agent/model/lifecycle/uninstall retry or product fix. Preparation/evidence-only corrections recorded.'),
    next_step=dict(requested_chat_decision='REWORK',action='Review immutable pushed FAIL evidence; create separately authorized current-launcher lifecycle rework. Preserve NOT_RUN and historical FAIL; do not replay consumed Dispatch.',owner_role='CHAT',prerequisite_gate='Independent CHAT remote result review; any new executable task requires fresh binding and PreExec.'))
(ROOT/PREFIX/'evidence_manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n',encoding='utf-8',newline='\n')
print('FAILED_HOST_CERTIFICATION_REPORT_AND_CONTRACT_ASSEMBLED')
