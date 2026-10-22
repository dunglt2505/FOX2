"""Assemble A03 report-only BLOCKED result; never invokes Bridge or package build."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
WP = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
TASK = 'FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03'
OUT = ROOT / 'reports' / WP
E = OUT / 'evidence/host_lifecycle_cert_a03'
BASE = '534204d5cc39a17fb4b3beb948b9b472d6e550b5'
ACCEPTED = '085cc8302e824dbccf9cbef80422ed48894b9cb4'
BRANCH = 'work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-20261022'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode().strip()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n', encoding='utf-8', newline='\n')


auth = json.loads((E / 'authorization.json').read_text())
blocker = json.loads((E / 'provenance_blocker.json').read_text())
host = json.loads((E / 'limited_host_observation.json').read_text())
assert auth['immutable_envelope_verification'] == 'PASS'
assert blocker['observed_source_git_commit_function_return'] == BASE != ACCEPTED
assert host['task_codex_writer_count'] == 1
assert all(all(row[key] for key in ('model_matches', 'high_matches', 'full_access_matches'))
           for row in host['task_codex_writers'])

historical_ids = [
    'FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001',
    'FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001',
    'FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001',
    'FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001',
]
historical = []
for identity in historical_ids:
    path = 'docs/agent_handoff/DISPATCH/' + identity + '.json'
    blob = git('rev-parse', auth['fetched_control_head'] + ':' + path)
    historical.append(dict(dispatch_id=identity, blob_sha1=blob, replayed=False))
write(E / 'historical_boundaries.json', dict(
    observed_at_utc=NOW, dispatches=historical,
    host_a01=dict(commit='9dd91becf47d934183baf147d0a4f03f4bf5933d', result='FAIL / REWORK_REQUIRED'),
    host_a02=dict(recovery_commit='53c3913899f87ad867c04c14d1da52b27d3cdbec',
                  state='CONSUMED_NO_RESULT', lifecycle='NOT_RUN'),
    host_a03=dict(agent_attempts=1, retries=0, lifecycle='NOT_RUN', result='BLOCKED',
                  disposition='REWORK_REQUIRED', replay_permitted=False),
    manual_consumption_hash_matches_preexec=True,
    database_hash_matches_preexec=False,
    database_hash_note='Read-only observed DB hash differs from PreExec; cause not investigated or attributed. No A03 lifecycle mutation occurred. Durable preservation is NOT_RUN.',
    no_worker_f1_g3_g4_applocker_service_acl_mutation=True,
    note='No historical record was rewritten. No old Dispatch was executed. Hash equality of manual consumption is not a full DB/consumed-ledger certification.'))

criteria = [
    ('AC01', 'PASS', 'E_AUTH', 'Accepted source is the exact ancestor; agent_bridge tree has no drift.'),
    ('AC02', 'BLOCKED', 'E_PROVENANCE', 'Read-only source_git_commit() returned runtime HEAD, incompatible with required accepted source; no manifest created.'),
    ('AC03', 'NOT_RUN', 'E_PROVENANCE', 'Package build/hash/manifest/payload checks stopped before build.'),
    ('AC04', 'NOT_RUN', 'E_HOST', 'Only limited read-only observation; full pre-state snapshot not performed.'),
    ('AC05', 'NOT_RUN', 'E_HOST', 'No WPF surfacing, inspect or cleanup; existing singleton left untouched.'),
]
descriptions = [
    'Install/update exact package', 'Current pointer and installed receipt bind accepted package',
    'Safe paused/setup/no-current-dispatch state', 'Launch twice exactly one WPF',
    'UI inspect/check', 'Live presentation lock', 'Safe state and identity before exit',
    'Explicit graceful exit', 'Zero presentation and released lock', 'Post-exit safe state',
    'Stable external uninstall exactly once', 'Uninstall exit zero',
    'Immediate uninstall postconditions', 'Durable config/database/manual-consumption preservation',
    'Same exact package reinstall', 'Final pointer/source', 'Final setup/paused state',
]
for number, text in enumerate(descriptions, 6):
    criteria.append((f'AC{number:02}', 'NOT_RUN', 'E_PROVENANCE', text + ': stopped before package build or host mutation.'))
criteria += [
    ('AC23', 'PASS', 'E_HISTORY', 'No historical consumed identity was rewritten; manual-consumption hash matches PreExec. No lifecycle/DB preservation PASS claimed.'),
    ('AC24', 'PASS', 'E_HISTORY', 'No old Dispatch replay; this A03 Agent attempt is consumed and cannot be replayed.'),
    ('AC25', 'PASS', 'E_HISTORY', 'No Worker/F1/G3/G4/AppLocker/service/ACL or other forbidden mutation invoked.'),
    ('AC26', 'PASS', 'E_VALIDATION', 'Only the authorized report/evidence paths changed.'),
    ('AC27', 'PASS', 'E_VALIDATION', 'Bounded generated-artifact secret/privacy scan passed.'),
    ('AC28', 'PASS', 'E_VALIDATION', 'Git diff --check passed for generated result changes.'),
    ('AC29', 'PASS', 'E_K1', 'Every changed file and material hunk is JUSTIFIED_GENERATED report/evidence; UNEXPLAINED=0.'),
    ('AC30', 'PASS', 'E_VALIDATION', 'Result Contract v2 schema and evidence hashes validated.'),
    ('AC31', 'NOT_RUN', 'E_VALIDATION', 'Delivery pending at report assembly. Actual push/readback is performed subsequently and remote SHA returned outside this report.'),
]

dispatch = json.loads(subprocess.check_output(['git', '-C', str(ROOT), 'show',
    auth['envelope']['FOX2_DISPATCH_COMMIT'] + ':docs/agent_handoff/DISPATCH/' +
    auth['envelope']['FOX2_DISPATCH_ID'] + '.json']))
dispatch_status = {}
for name in dispatch['required_tests']:
    state = 'NOT_RUN'
    evidence = 'E_PROVENANCE'
    reason = 'Stopped before package build and host mutation; no inferred lifecycle PASS.'
    if name in ('RUNTIME_AUTHORIZATION_ENVELOPE_PRESENT', 'AGENT_REMOTE_PASS_TO_ASSIGN_VERIFICATION_PASS',
                'AGENT_REMOTE_DISPATCH_VERIFICATION_PASS', 'AGENT_REMOTE_PREEXEC_RECEIPT_VERIFICATION_PASS'):
        state, evidence, reason = 'PASS', 'E_AUTH', 'Fetched immutable Git bytes verified against supplied envelope.'
    if name == 'EXACT_ACCEPTED_SOURCE_PACKAGE_BUILD_PROVENANCE':
        state, reason = 'BLOCKED', 'Accepted builder binds runtime HEAD rather than required accepted source.'
    if name in ('CONSUMED_IDENTITIES_PRESERVED', 'NO_OLD_DISPATCH_REPLAY', 'NO_G3_G4_APPLOCKER_SERVICE_ACL_MUTATION'):
        state, evidence, reason = 'PASS', 'E_HISTORY', 'No lifecycle mutation/replay or historical record write occurred.'
    if name in ('CHANGED_PATH_ALLOWLIST_REPORT_EVIDENCE_ONLY', 'SECRET_SCAN', 'GIT_DIFF_CHECK',
                'RESULT_CONTRACT_V2_REPORT_AND_EVIDENCE_MANIFEST'):
        state, evidence, reason = 'PASS', 'E_VALIDATION', 'Generated result static validation.'
    if name == 'K1_UNEXPLAINED_ZERO':
        state, evidence, reason = 'PASS', 'E_K1', 'All result hunks classified JUSTIFIED_GENERATED.'
    dispatch_status[name] = dict(status=state, evidence_id=evidence, reason=reason)
write(E / 'acceptance_mapping.json', dict(result='BLOCKED', disposition='REWORK_REQUIRED',
    task_acceptance=[dict(id=i, status=s, evidence_id=e, reason=r) for i, s, e, r in criteria],
    dispatch_required_tests=dispatch_status, worker_f1_health='NOT_APPLICABLE_PRE_G3',
    final_delivery_note='Read final external pointer for actual observed remote result SHA.'))

report = f'''# FOX2 Host Lifecycle Certification A03 - BLOCKED / REWORK_REQUIRED

## R01 - Identification and submission

Task `{TASK}`, Whole-WP `{WP}`. CODEX gpt-6.1-sol / high / MANUAL_LOCAL / FULL_ACCESS, Owner Windows host. One Agent attempt, zero retries/subagents. Result **BLOCKED**, disposition **REWORK_REQUIRED**; lifecycle **NOT_RUN**. Evidence capture started `{auth['checked_at_utc']}`; report assembled `{NOW}`. Submission BLOCKED for CHAT review. Delivery is initially LOCAL_ONLY; actual push/readback status and remote result SHA are returned outside this report. CHAT acceptance is not claimed.

## R02 - Authority, routing and grants

Runtime envelope and immutable remote Git verification **PASS**. Dispatch `{auth['envelope']['FOX2_DISPATCH_ID']}` at `{auth['envelope']['FOX2_DISPATCH_COMMIT']}`; PASS_TO_ASSIGN `{auth['envelope']['FOX2_PASS_TO_ASSIGN_COMMIT']}`; PreExec/runtime base `{BASE}`. Explicit control/status/governance/task branch fetch succeeded after one transient DNS failure. Dispatch schema blob `1692061941e2bef498515cd0e96b9b3046119ebb` validated. Every supplied environment value, exact task/prompt bytes, PreExec PASS/empty blockers/not-started/not-consumed fields and material capabilities were checked. Initial worktree clean before and after the read-only provenance probe. One task CODEX writer PID 4652 observed, with matching model/high/full-access arguments. PreExec capacity PASS plus active pinned execution; no additional Agent probe started. Current full host capability/safe-state gates were not completed after the provenance STOP.

Report/evidence write and non-main push only. code_allowed=false and git_code_push=false. Schema-v3 legacy decision_receipt.code_allowed=YES does not broaden controlling permissions. No source/test/script fix, PR, merge, main, provider, broker or LIVE authority.

## R03 - Immutable sources and provenance blocker

Accepted source `{ACCEPTED}` is an ancestor of runtime base `{BASE}`. The four intervening paths are only A03 task, prompt, PreExec helper and receipt; no agent_bridge drift. Task commit `33f6176dff86b00df6c9b8b0ef6f8eefce00578e`, SHA-256 `f9e2fe4e285f703edabd8ec1266b0244d520ee2e1be876daf45b332bfcfc1f0f`; prompt commit `db9902a1adbe21f801707ed9680fe38524e92dfc`, blob `ccffde862e11490743e5aabb5c79a4a0986ab9a1`, SHA-256 `170f48485aa44deee24c4e3af1529273343dd5cef3d94489e7e24b11bf1c38ee`.

The unchanged accepted `agent_bridge/scripts/build_user_package.py` obtains `source_git_commit` using `git rev-parse --verify HEAD` (lines 60-96), then writes that return value directly into the manifest (line 175). Its CLI accepts only --output and --build-python. Under existing isolated Python 3.13, importing the builder with bytecode disabled and calling **only source_git_commit()** returned `{BASE}`. The required value is `{ACCEPTED}`. Thus a build on the mandated clean A03 branch cannot meet the exact manifest provenance gate. **No package build ran and no manifest/package/hash exists.** The evidence records a provenance-function result, not a fabricated package failure. No alternate checkout, ref/environment override, manifest rewrite or builder modification was used.

Policy 2.0.0, Dictionary 1.3, Routing Index 1.4.0 and Protocol v12 were resolved via the fetched Governance Registry/source-resolution record and verified by immutable blob/hash. See authorization.json. Bridge TechSpec v0.7 REV10 remains CANDIDATE_NO_PROMOTION; installed adoption is not claimed.

## R04 - Requested versus completed

Requested: exact build, install/update, WPF presentation-only lifecycle, graceful exit, one stable external uninstall, same-package reinstall and durable/final verification. Completed: remote authorization verification, no-drift checks, a read-only provenance probe, limited host observation and report validation. All package and lifecycle operations are NOT_RUN. Host mutation never began; recovery is not applicable and was not attempted. The task's STOP for required source/code correction applies.

## R05 - Changed paths and ownership

Only report.md and evidence_manifest.json are modified; all added paths are below evidence/host_lifecycle_cert_a03/. Every exact path/raw SHA-256 is inventoried in evidence_manifest.json; the manifest self-hash is null to avoid recursion. No product/source/test, immutable handoff, PreExec receipt or historical evidence path changed. All material result hunks are JUSTIFIED_GENERATED, K1 UNEXPLAINED=0. No competing task writer observed.

## R06 - Executed validation

Remote ls-remote and explicit fetch; immutable envelope/source/Governance/Dispatch-schema checks PASS. Direct source_git_commit() probe executed read-only and exposed the BLOCKED provenance condition. No unit tests were run because no code changed and no lifecycle test is authorized past this STOP. Generated result allowlist, secret/privacy scan, git diff --check, evidence raw-hash readback and Result Contract v2 schema checks are recorded in validation.json.

## R07 - Acceptance mapping

All 31 task acceptance items and every Dispatch-required test are individually mapped in acceptance_mapping.json and the manifest. AC02 BLOCKED; build/package gates and every lifecycle step NOT_RUN. Historical no-replay and forbidden-mutation boundaries hold. The required successful lifecycle uninstall count is not satisfied: **actual uninstall attempts=0**, install=0, lifecycle=0, reinstall=0, recovery=0, launch=0, UI exit=0. Worker/F1 health remains NOT_APPLICABLE_PRE_G3, never a health PASS.

## R08 - Evidence and host limits

authorization.json binds fetched immutable identities; provenance_blocker.json records the exact existing builder function and actual return; limited_host_observation.json records only public pointer identities, process PID/path aliases, writer tuple and file hashes; historical_boundaries.json preserves the historical results; acceptance_mapping.json maps requirements; k1.json and validation.json cover result checks. assemble_result.py generates reports only.

Limited observation found existing WPF PID 10608, exactly the current installed package executable, untouched. Config/manual-consumption/uninstall hashes match PreExec. **DB hash differs from PreExec**, with no cause attributed or investigated; no durable-state preservation PASS is claimed. No Bridge CLI, UI seam, scheduler or service operation ran. Full pre-state capture, DB quick-check, current control status and final host certification remain NOT_RUN. No raw config, DB contents, raw prompts, credentials or private user absolute paths are committed.

## R09 - Git delivery

Repository dunglt2505/FOX2, branch `{BRANCH}`, pre-submission HEAD `{BASE}`. Authorized report-only commit/push and remote readback follow static validation. The committed manifest records LOCAL_ONLY at assembly; the final external pointer records the actual observed PUSHED_UNREVIEWED delivery without a self-referential result SHA. No CHAT acceptance or lifecycle PASS is claimed.

## R10 - Blocker, history and next action

CHAT must reconcile the mandated A03 checkout/runtime HEAD with exact accepted-source manifest provenance, or separately authorize a tested builder correction. This TEST cannot change source or silently build from another checkout. Any future execution requires fresh authorization; **do not replay this A03 Dispatch**. Historical host A01 result `9dd91becf47d934183baf147d0a4f03f4bf5933d` remains FAIL / REWORK_REQUIRED. Host A02 remains CONSUMED_NO_RESULT / NOT_RUN, recovery receipt `53c3913899f87ad867c04c14d1da52b27d3cdbec`. All four historical Dispatches remain consumed/no-replay. No recovery success or CLI exit code is treated as certification PASS.

## R11 - Resource accounting

Agent attempts=1, retries=0, subagents=0. Package builds=0, lifecycle attempts=0. Token/credit totals NOT_MEASURED. Transient Git DNS recovery was a read-only transport retry within this single attempt; no Dispatch or lifecycle replay.

## R12 - Decision request

Agent conclusion BLOCKED / REWORK_REQUIRED. Request CHAT REWORK of the provenance contradiction and independent review of this immutable result. No G3/G4/Canary/AppLocker/AppIDSvc/FOX2F1Authority/ProgramData authority ACL/reboot/main/PR/merge/provider/broker/LIVE action occurred.
'''
(OUT / 'report.md').write_text(report, encoding='utf-8', newline='\n')

def changed_paths():
    return sorted(set(git('diff', '--name-only', BASE).splitlines() +
                      git('ls-files', '--others', '--exclude-standard').splitlines() +
                      [f'reports/{WP}/report.md', f'reports/{WP}/evidence_manifest.json']))

def allowed(path):
    return path in [f'reports/{WP}/report.md', f'reports/{WP}/evidence_manifest.json'] or path.startswith(f'reports/{WP}/evidence/host_lifecycle_cert_a03/')

paths = changed_paths()
assert all(allowed(p) for p in paths)
write(E / 'k1.json', dict(observed_at_utc=NOW, UNEXPLAINED=0,
    classification='JUSTIFIED_GENERATED', reason='Only requested report and evidence for A03 pre-build provenance STOP.',
    material_code_hunks=0, result_paths=sorted(set(paths + [str((E/'k1.json').relative_to(ROOT)).replace('\\','/'), str((E/'validation.json').relative_to(ROOT)).replace('\\','/')]))))

# Validate real generated bytes before describing them in the contract.
paths = changed_paths()
scan_patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                 r'gh[pousr]_[A-Za-z0-9]{30,}', r'github_pat_[A-Za-z0-9_]{40,}',
                 r'sk-[A-Za-z0-9_-]{30,}', r'(?i)C:[/\\]Users[/\\]']
findings = []
for path in paths:
    text = (ROOT / path).read_text(encoding='utf-8')
    if path.endswith('/evidence_manifest.json'):
        continue  # replaced below; inherited A02 manifest is not part of this result
    # Scanner definitions are literal regex syntax, not credentials/private paths.
    for pattern in scan_patterns:
        if re.search(pattern, text):
            findings.append(dict(path=path, pattern=pattern))
assert findings == [], findings
assert git('diff', '--check') == ''
write(E / 'validation.json', dict(observed_at_utc=NOW, result_scope='REPORT_ONLY',
    changed_path_allowlist='PASS', source_drift='NONE', secret_privacy_scan='PASS',
    scan_scope='All generated JSON/report bytes plus manual review of report generator; scanner regex definitions are non-secret.',
    diff_check='PASS', k1_unexplained=0, schema_validation='PASS_ON_SUCCESSFUL_ASSEMBLER_COMPLETION',
    evidence_hash_validation='PASS_ON_SUCCESSFUL_ASSEMBLER_COMPLETION', delivery_status='LOCAL_ONLY_AT_ASSEMBLY',
    push_readback='Performed after local commit; observed remote SHA returned outside committed report.',
    limitations=['No build, package validation, host lifecycle or final-state certification executed.']))

evidence_names = {
    'authorization.json': 'E_AUTH', 'provenance_blocker.json': 'E_PROVENANCE',
    'limited_host_observation.json': 'E_HOST', 'historical_boundaries.json': 'E_HISTORY',
    'acceptance_mapping.json': 'E_MAPPING', 'k1.json': 'E_K1', 'validation.json': 'E_VALIDATION',
    'assemble_result.py': 'E_ASSEMBLER', 'report_validation_history.json': 'E_VALIDATION_HISTORY'}
evidence = [dict(id=evidence_names[p.name], path=p.relative_to(ROOT).as_posix(), sha256=digest(p),
    kind='OTHER', observed_at_utc=NOW, description='A03 bounded report evidence: ' + p.name,
    supports_ids=['T_REPORT'] if p.name != 'provenance_blocker.json' else ['T_PROVENANCE'], sanitized=True)
    for p in sorted(E.iterdir()) if p.is_file()]
tests = [dict(id=i, kind=kind, status=state, command_or_method=method,
    environment='Owner Windows / PowerShell 7.6.7 / existing isolated Python 3.13',
    run_at_utc=NOW, evidence_ids=[e], notes=notes) for i, kind, state, method, e, notes in [
    ('T_AUTH', 'READBACK', 'PASS', 'Fetch branches; compare immutable Git blobs/raw hashes; validate Dispatch schema v3.', 'E_AUTH', 'Authorization verified; full host execution gates incomplete.'),
    ('T_PROVENANCE', 'READBACK', 'BLOCKED', 'Import accepted builder with bytecode disabled; call source_git_commit() only.', 'E_PROVENANCE', 'Actual return differs from exact required accepted source. No package built.'),
    ('T_REPORT', 'STATIC', 'PASS', 'Allowlist, secret/privacy scan, diff check, K1, JSON Schema and evidence hashes.', 'E_VALIDATION', 'Report validation only.'),
    ('T_LIFECYCLE', 'INTEGRATION', 'NOT_RUN', 'certify_user_lifecycle.py --package --sha256 --evidence', 'E_PROVENANCE', 'Stopped before package build/host mutation; never invoked.')]]
paths = changed_paths()
manifest = dict(contract_version='2.0', project='FOX2', wp_id=WP, task_id=TASK, change_id=TASK,
    submission_state='BLOCKED', submitted_at_utc=NOW,
    agent=dict(product='CODEX', model='gpt-6.1-sol', mode='TEST / high / MANUAL_LOCAL / FULL_ACCESS',
        host='Owner Windows host; no lifecycle mutation', started_at_utc=auth['checked_at_utc'], finished_at_utc=NOW,
        quota_observation='Immutable PreExec capacity PASS; active pinned Agent. Usage NOT_MEASURED.'),
    routing=dict(policy_check='PASS', task_state_check='PASS', r0='PASS', r1='PASS', r2='PASS',
        r3='PARTIAL', r4='PASS', r5='PASS', r6='PASS', r7='PASS', assignment_check='PASS',
        routing_evidence='Immutable authorization PASS, one current writer observed; current full host gates incomplete after provenance STOP. See E_AUTH/E_HOST.'),
    source=dict(policy_sha256=auth['governance']['policy']['observed_sha256'], policy_version='2.0.0',
        task_commit_sha='33f6176dff86b00df6c9b8b0ef6f8eefce00578e',
        source_manifest_sha256=digest(E/'authorization.json'), approved_base_commit_sha=BASE,
        source_readback_status='PASS', brd_revisions=['Bridge TechSpec v0.7 REV10 CANDIDATE_NO_PROMOTION'],
        previous_evidence_reused=['PreExec and historical receipts used for authorization/history only, never current lifecycle PASS.']),
    permissions=dict(git_source_read=True, git_report_write=True, git_report_push=True, git_code_push=False,
        code_allowed=False, pr_create=False, merge_allowed=False, dnse_production=False, broker_write=False, live=False,
        grant_evidence='Fresh A03 Dispatch permissions and Owner runtime envelope, independently Git-verified.'),
    git=dict(repository='dunglt2505/FOX2', branch=BRANCH, worktree='WORKTREES/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-20261022',
        writer_lease='One task CODEX writer PID 4652; no second task writer observed.', report_path=f'reports/{WP}/report.md',
        delivery_status='LOCAL_ONLY', pr_url=None, local_head_before_submission=BASE),
    scope=dict(requested=['Bounded real Owner-host accepted-package lifecycle certification.'],
        completed=['Immutable authorization verification; exact read-only provenance blocker; limited host observation; report validation.'],
        partial=['Full capability/pre-state gates not completed after provenance STOP.'],
        not_done=['Package build/manifest/hash; all install/WPF/uninstall/reinstall/durable/final-state certification; CHAT acceptance.'],
        explicit_exclusions=['All product/source/test edits; Worker/F1/G3/G4/Canary; AppLocker/service/ACL; main/PR/merge/provider/broker/LIVE.'],
        changed_paths=[dict(path=p, operation='MODIFY' if p in (f'reports/{WP}/report.md', f'reports/{WP}/evidence_manifest.json') else 'ADD',
            intent='A03 report/evidence for pre-build provenance STOP; JUSTIFIED_GENERATED', within_allowed_paths=True,
            new_sha256=None if p.endswith('/evidence_manifest.json') else digest(ROOT/p)) for p in paths], forbidden_paths_touched=False),
    tests=tests, acceptance=[dict(id=i, status=s, evidence_ids=[e], reason=r) for i,s,e,r in criteria], evidence=evidence,
    risks=[dict(id='PROVENANCE_BLOCKER', severity='HIGH', state='BLOCKED',
        impact='Required accepted-source manifest cannot be produced by existing builder on required A03 runtime HEAD.',
        next_action='CHAT reconcile build-source contract or assign separate source fix; no A03 replay.', owner_role='CHAT'),
        dict(id='HOST_NOT_CERTIFIED', severity='HIGH', state='NOT_VERIFIED', impact='All lifecycle operations NOT_RUN.',
        next_action='Fresh authorized certification only after provenance correction and host readiness.', owner_role='CHAT')],
    security=dict(secret_scan='PASS', private_account_data_in_git=False, licensed_raw_feed_in_git=False,
        evidence_redacted=True, check_notes='Public immutable identities/hash-only host observations; no raw config/DB/prompts/private user paths.'),
    usage=dict(attempts=1, retries=0, usage_status='NOT_MEASURED', tokens_used=None, credits_used=None,
        escalation_reason='BLOCKED provenance contract; report REWORK_REQUIRED without editing source.'),
    next_step=dict(requested_chat_decision='REWORK', action='Reconcile required source provenance and builder HEAD identity; review result. No Dispatch replay.',
        owner_role='CHAT', prerequisite_gate='New authorization only after exact source/package provenance and host readiness are satisfiable.'))
write(OUT / 'evidence_manifest.json', manifest)
for pattern in scan_patterns:
    assert re.search(pattern, (OUT/'evidence_manifest.json').read_text()) is None
import jsonschema
jsonschema.validate(manifest, json.loads((ROOT/'docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json').read_text()))
for item in manifest['evidence']:
    assert digest(ROOT/item['path']) == item['sha256']
for item in manifest['scope']['changed_paths']:
    if item['new_sha256']:
        assert digest(ROOT/item['path']) == item['new_sha256']
assert changed_paths() == paths
assert git('diff','--check') == ''
print(json.dumps(dict(result='BLOCKED', disposition='REWORK_REQUIRED', schema='PASS', hashes='PASS',
                      allowlist='PASS', diff_check='PASS', secret_scan='PASS', k1_unexplained=0,
                      changed_paths=len(paths), task_acceptance=len(criteria), dispatch_tests=len(dispatch_status))))
