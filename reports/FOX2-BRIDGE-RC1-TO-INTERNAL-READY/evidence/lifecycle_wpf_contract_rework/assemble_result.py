"""Assemble the A02 BUILD report/manifest from actual, independently rerun evidence."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
WP = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
PREFIX = 'reports/' + WP + '/'
BASE = '4504bf95dd2baf474b30f896b23365c52fe10c9f'
ORIGINAL = 'e7d5acf51dddcbc95324a992ad6be2773e61285f'
SNAPSHOT = '1a11fa0b232a69f0c26a0b4029c331ee2a8c840f'
git = lambda *a: subprocess.check_output(['git', '-C', str(ROOT), *a])
digest = lambda b: hashlib.sha256(b).hexdigest()
now = datetime.now(timezone.utc).isoformat()
binding = json.loads((OUT / 'source_binding.json').read_text())
claim = binding['claim']
dispatch = json.loads(git('show', claim['dispatch_commit'] + ':' + binding['dispatch_path']))
runs = sorted([json.loads(p.read_text()) for p in OUT.glob('*_run.json')], key=lambda r: r['started_at_utc'])
focused = next(r for r in reversed(runs) if r['suite'] == 'focused' and r['exit_code'] == 0)
full = next(r for r in reversed(runs) if r['suite'] == 'full' and r['exit_code'] == 0)
for run in [focused, full]:
    assert re.search(r'=+ \d+ passed in [\d.]+s(?: \([^)]+\))? =+', run['output_tail']), run
    assert run['output_tail'] in (OUT / run['log']).read_text()
focused_summary = focused['output_tail'].strip('= ')
full_summary = full['output_tail'].strip('= ')
failed_runs = [r for r in runs if r['exit_code']]
if failed_runs:
    assert all(r['suite'] == 'full' and not r['environment']['process_core_longpaths'] for r in failed_runs)
    environment_note = 'The initial full-suite failure is retained verbatim. Git MAX_PATH behavior required only a child-process core.longpaths=true override on the final run. No repository/global Git configuration, test or host setting changed.'
else:
    environment_note = 'The focused and full runs passed without a core.longpaths override. No repository/global Git configuration, test or host setting changed.'

# Markdown is a readable companion; structured inventory/hashes live in the manifest.
report = f'''# FOX2 Lifecycle/WPF Contract Rework A02 â€” BUILD result

## R01 â€” Identification and submission

Task `{claim['task_id']}`; Whole-WP `{WP}`. CODEX `gpt-6.1-sol`, high, MANUAL_LOCAL, task-scoped FULL_ACCESS. One fresh A02 Agent attempt, no retries or subagents. Started `{claim['started_at_utc']}`; report assembled `{now}`. Delivery state after the authorized branch push is **PUSHED_UNREVIEWED**. CHAT acceptance is not claimed.

## R02 â€” Authority, routing and start gates

Fresh Dispatch `{claim['dispatch_id']}` is at `{claim['dispatch_commit']}`, blob `{claim['dispatch_blob']}` on `work/FOX2-DISPATCH-chat`. It grants bounded code/report writes and non-main result push, with no PR/merge/provider/broker/LIVE permission. The task-specific PreExec REV3 receipt at `{BASE}` and CHAT PASS_TO_ASSIGN `61b75156bb4b241b88a26c0c11cb8af79f79a94b` bind this route. Policy 2.0.0, Dictionary 1.3, Routing Index 1.4.0 and Protocol v12 immutable bytes were verified independently. Source bytes and task-scoped execution authority are verified; global publication/runtime promotion is not claimed. TechSpec v0.7 REV10 remains **CANDIDATE_NO_PROMOTION**.

Required-versus-observed gates: exact branch/worktree/base and remote task head PASS; recovery ancestor PASS; task/prompt/PreExec/Dispatch hashes PASS; Dispatch schema blob `1692061941e2bef498515cd0e96b9b3046119ebb` PASS; current launcher claim/model/effort/FULL_ACCESS PASS; initial worktree clean PASS; no pre-start product drift PASS; one task Agent process PID {claim['process_id']} observed PASS. Fresh PreExec authenticated capacity probe PASS and this pinned execution is active; numeric quota is not measured. Only the two bound task/prompt additions and PreExec receipt separate recovery snapshot from runtime base. Start verdict: **GO for offline BUILD only**. See `evidence/lifecycle_wpf_contract_rework/source_binding.json` for identities, R0â€“R7 provenance and observations.

## R03 â€” Immutable inputs and A01 preservation

Runtime base `{BASE}`; original runtime base `{ORIGINAL}`; recovery snapshot `{SNAPSHOT}`. Task commit `{claim['task_commit']}`, task SHA-256 `{dispatch['task']['sha256']}`. Prompt commit `{claim['prompt_commit']}`, blob `{dispatch['prompt']['git_blob_sha1']}`, prompt SHA-256 `{claim['prompt_sha256']}`.

A01/CODEX-001 remains EXITED_CONSUMED, exit 1, CODEX_USAGE_LIMIT, NEEDS_RECONCILIATION, no Git result, no CHAT acceptance and no replay. Its recovery provenance JSON is byte-identical. Salvage is input, never accepted evidence. Every inherited source/test hunk was reviewed; provisional evidence and A01-bound helpers were replaced with fresh A02 execution evidence. `salvage_review.json`, `k1.json`, `original_to_final_diff.json` and `salvage_to_final_diff.json` distinguish retained salvage from A02 corrections.

## R04 â€” Implemented behavior and corrections

The harness uses stable `BridgeRoot/launch.ps1` twice and validates one current-package `FOX2.Bridge.Desktop.exe` by its exact installed executable path, current package pointer and inspected UI PID. It requires paused=true, setup_complete=true and explicit current_dispatch=null. No desktop-tray health, legacy launcher-process health, Worker heartbeat or Worker start is required. Worker/F1 health is **NOT_APPLICABLE_PRE_G3**, never a health PASS.

Existing `certify_rc1_ui.ps1` supplies inspect/check/explicit exit. Inspect validates all six navigation entries and the current presentation PID; check proves Check Now disabled while paused. The harness observes the held presentation lock, rechecks safe control and exact presentation identity, invokes graceful UI exit, waits boundedly for zero presentations, observes lock release and rechecks STOPPED/paused/setup/no-current-dispatch before uninstall. No forced-exit path was added.

Three A02 proof gaps were corrected: absent current_dispatch no longer passes as null; only WinError 32 sharing violation proves a live FileShare.None lock, while access-denied/other errors fail; process queries fail on PowerShell errors and must return an explicit array, so null cannot falsely prove exit. Negative fixtures also cover process-query failure/timeout, PID changes and unsafe state changes before/after exit. Correct salvaged behavior was retained.

## R05 â€” A03 preservation and changed-path ownership

Only the allowed lifecycle harness and two test files contain material source/test changes. `test_rc1_launcher.py` was rerun unchanged. A03 `certify_uninstall` and `_uninstall_output` ASTs match the original runtime base. Stable external PowerShell 7 at `BridgeRoot/uninstall.ps1`, synchronous single attempt, installed-Python exclusion, sanitized bounded output, nonzero/timeout/start/postcondition stop-once behavior and checkpoint-before-reinstall semantics remain intact.

Configuration/database/manual-consumption checks and historical Batch-B consumed identities 001â€“004 remain intact. Successful reinstall uses the same package/SHA, verifies the current package, and rechecks the safe stopped/paused state. No historical consumed identity was replayed or rewritten. The protected launcher/F1/installation/UI/WPF source files retain original Git blobs and raw bytes from a same-base checkout. All other agent_bridge paths remain unchanged.

The complete changed-path inventory and raw SHA-256 values are in `evidence_manifest.json`; the manifest's own hash is null to avoid self-reference. No unrelated WIP was present or introduced. Test artifacts are isolated in a detached short fixture worktree, with no second material writer.

## R06 â€” Executed validation and environment

Focused lifecycle/WPF + launcher + package + installation: **{focused_summary}**. Full `agent_bridge/tests`: **{full_summary}**. Real command lines, cwd, environment, UTC times, exit codes and unabridged logs are retained in `*_run.json` and associated `.log` files.

The short detached A02 test worktree at `C:/Projects/FOX2/.git/wpf-a02-test` starts from the exact runtime base and has byte-for-byte copies of the final allowed source/test files; all tracked agent_bridge files were compared before each run. This follows the established short-worktree test approach for Windows MAX_PATH. No test was edited or skipped to hide environment behavior. {environment_note}

An initial generated-evidence formatting check found CRLF trailing-whitespace diagnostics; its output is retained in diff_check_initial.log. A02-generated text was normalized to LF and writers now request LF explicitly; the immutable recovery provenance bytes were preserved. A later staged check flagged the literal blank context lines in unified-diff evidence; exact Git stdout is now stored in JSON, with that failed validation output preserved in static_validation_history.json. Syntax/compile checks, static parsing of the generated PowerShell query (without executing it), changed-path allowlist, forbidden production-file byte identity, immutable recovery provenance, A03 AST identity, git diff --check, bounded secret scan and K1 **UNEXPLAINED=0** all pass. K1 classifies material hunks against both original runtime base and salvage as REQUESTED or NECESSARY_DEPENDENCY; regenerated evidence is JUSTIFIED_GENERATED. Result Contract v2 schema and evidence/changed-file hash readback are verified by `verify_result.py --manifest-only`.

## R07 â€” Requirements and evidence

All Dispatch-required offline checks are mapped individually in the manifest. Singleton/current identity/safe state/UI/lock/exit tests use intercepted process boundaries; launcher tests retain worker_started=False. Stable-uninstall success and nonzero/timeout/start/postcondition stop-once cases are rerun, along with durable-state assertions. No prior A01 PASS substitutes for an A02 result. Historical host lifecycle FAIL remains unchanged in Git history.

Evidence includes source binding, test snapshot byte hashes, actual pytest receipts/logs, salvage review, both source diffs, hunk classifications, static checks and Result Contract validation output. The manifest binds every evidence item with raw SHA-256. Observed remote result SHA is returned outside this committed report.

## R08 â€” Scope, risks and next owner

Real installed-host lifecycle: **NOT_RUN**. No actual package install/update/uninstall/reinstall, installed WPF launch, Task Scheduler change, Bridge durable data/config/database change, Worker/F1 start, AppLocker/AppIDSvc/service/ACL change, reboot, G3/G4/Canary, main/PR/merge or provider/broker/LIVE action occurred during A02 BUILD. Tests exercise temporary offline fixtures.

Fixture validation does not certify Owner-host lifecycle, F1 adoption, G3/G4 or operational readiness. Usage totals are NOT_MEASURED; attempts=1, retries=0. CHAT must independently review this immutable pushed BUILD result. Any future real host certification needs its own authorized binding and material PreExec. No CHAT acceptance or feature-stage promotion is claimed here.
'''
(ROOT / PREFIX / 'report.md').write_text(report, encoding='utf-8', newline='\n')

static_log = OUT / 'static_validation.log'
if static_log.exists() and 'Traceback' in static_log.read_text():
    history_path = OUT / 'static_validation_history.json'
    history = json.loads(history_path.read_text()) if history_path.exists() else {'runs': []}
    history['runs'].append({'command': 'python verify_result.py', 'exit_code': 1, 'status': 'FAIL',
        'reason': 'Previous validation log retained literal diff context whitespace; archive exact output in JSON before refreshing the live log.',
        'output': static_log.read_text()})
    history_path.write_text(json.dumps(history, indent=2) + '\n', encoding='utf-8', newline='\n')
static_log.write_text('', encoding='utf-8', newline='\n')
static = subprocess.run([sys.executable, str(OUT / 'verify_result.py')], capture_output=True, text=True)
(OUT / 'static_validation.log').write_text(static.stdout + static.stderr, encoding='utf-8', newline='\n')
assert static.returncode == 0, static.stdout + static.stderr

run_ids = {r['name']: 'E_' + r['name'].upper() for r in runs}
focus_id, full_id = run_ids[focused['name']], run_ids[full['name']]
static_requirements = {'PYTHON_SYNTAX_STATIC', 'CHANGED_PATH_ALLOWLIST', 'FORBIDDEN_FILE_BYTE_IDENTITY',
    'SECRET_SCAN', 'GIT_DIFF_CHECK', 'K1_UNEXPLAINED_ZERO'}
reasons = {
    'NO_LEGACY_DESKTOP_TRAY_HEALTH_DEPENDENCY': 'test_no_legacy_tray_worker_heartbeat_or_f1_g3_mutation; no tray or legacy launcher health probe.',
    'LAUNCH_TWICE_ONE_WPF_PRESENTATION': 'test_launch_twice_exact_singleton_paused_ui_and_graceful_exit; duplicate/missing presentation negatives.',
    'EXACT_CURRENT_PACKAGE_PRESENTATION_IDENTITY': 'Positive exact package path/current pointer/UI PID; old_package, unknown_path, pointer_drift, wrong_ui_pid and pid_changed rejected.',
    'PAUSED_SETUP_NO_CURRENT_DISPATCH_PRE_G3': 'Paused/setup/null tests reject unsafe values and absent fields; unsafe pre/post-exit control rejected.',
    'CERTIFY_RC1_UI_INSPECT_CHECK_EXIT_REUSED': 'Positive fixture verifies the existing script/action argv and inspect -> check -> exit order; UI failures rejected.',
    'GRACEFUL_WPF_EXIT_BEFORE_UNINSTALL': 'Positive integration gates uninstall on explicit UI exit, count zero and lock release; exit timeout/retained lock rejected.',
    'NO_WORKER_START_OR_HEARTBEAT_REQUIREMENT': 'Process/CLI fixtures reject any Worker command; no heartbeat in state or evidence; launcher reports worker_started=False.',
    'WORKER_F1_HEALTH_NOT_APPLICABLE_PRE_G3': 'Fixture asserts worker_f1_health=NOT_APPLICABLE_PRE_G3; no health PASS claim.',
    'NO_F1_G3_MUTATION': 'Mocked lifecycle process boundary, source guard and unchanged F1/G3 production paths.',
    'STABLE_EXTERNAL_UNINSTALL_SUCCESS': 'End-to-end stable external supervisor exit 0, preserved durable fixtures, checkpoint before exact reinstall.',
    'STABLE_EXTERNAL_UNINSTALL_FAILURE_STOP_ONCE': 'Nonzero, timeout, start failure, incomplete postconditions, changed config/consumption and unreadable checks persist evidence and prevent retry/reinstall.',
    'INSTALLATION_AND_PACKAGE_TESTS': 'test_installation.py and test_rc1_package.py rerun in focused and full suites.',
    'RC1_LAUNCHER_TESTS': 'Unchanged test_rc1_launcher.py rerun; presentation-only/F1 denial assertions preserved.',
    'FULL_AGENT_BRIDGE_TESTS': full_summary + '; all tests collected, no skips/exclusions.',
    'REAL_HOST_LIFECYCLE_REMAINS_NOT_RUN': 'BUILD boundary honored; all lifecycle calls in changed fixtures intercepted; real installed-host certification NOT_RUN.'}
acceptance = []
for req in dispatch['required_tests']:
    if req in static_requirements:
        ids, reason = ['E_STATIC', 'E_STATIC_LOG'], 'Fresh static/identity/AST/allowlist/diff/scan/K1 execution.'
    elif req == 'RESULT_CONTRACT_V2_REPORT_AND_EVIDENCE_MANIFEST':
        ids, reason = ['E_MANIFEST_VALIDATION'], 'Dictionary-resolved Result Contract v2 schema, evidence hashes, path hashes and references read back.'
    elif req == 'REAL_HOST_LIFECYCLE_REMAINS_NOT_RUN':
        ids, reason = ['E_SOURCE', focus_id], reasons[req]
    elif req == 'FULL_AGENT_BRIDGE_TESTS':
        ids, reason = [full_id], reasons[req]
    else:
        ids, reason = [focus_id], reasons[req]
    acceptance.append({'id': req, 'status': 'PASS', 'evidence_ids': ids, 'reason': reason})
acceptance += [{'id': 'REAL_HOST_LIFECYCLE_CERTIFICATION', 'status': 'NOT_RUN', 'evidence_ids': [], 'reason': 'Outside offline BUILD authorization.'},
               {'id': 'CHAT_ACCEPTANCE', 'status': 'NOT_RUN', 'evidence_ids': [], 'reason': 'Independent CHAT intake follows PUSHED_UNREVIEWED delivery.'}]
tests = [{'id': 'T_' + r['name'].upper(), 'kind': 'INTEGRATION', 'status': r['status'],
    'command_or_method': subprocess.list2cmdline(r['argv']), 'environment': json.dumps({'cwd': r['cwd'], **r['environment']}),
    'run_at_utc': r['started_at_utc'], 'evidence_ids': [run_ids[r['name']]], 'notes': r['output_tail']} for r in runs]
tests += [
    {'id': 'T_STATIC', 'kind': 'STATIC', 'status': 'PASS', 'command_or_method': 'python evidence/lifecycle_wpf_contract_rework/verify_result.py', 'environment': 'Offline source/evidence checks; PowerShell query parsed only.', 'run_at_utc': now, 'evidence_ids': ['E_STATIC', 'E_STATIC_LOG'], 'notes': 'Includes K1 and A03/protected production byte identity.'},
    {'id': 'T_SOURCE', 'kind': 'READBACK', 'status': 'PASS', 'command_or_method': 'python evidence/lifecycle_wpf_contract_rework/bind_source.py', 'environment': 'Read-only Git/source/PreExec/Dispatch/claim/process inventory.', 'run_at_utc': binding['checked_at_utc'], 'evidence_ids': ['E_SOURCE'], 'notes': 'Source bytes and scoped authority verified; no runtime/global promotion.'},
    {'id': 'T_MANIFEST', 'kind': 'READBACK', 'status': 'PASS', 'command_or_method': 'python evidence/lifecycle_wpf_contract_rework/verify_result.py --manifest-only', 'environment': 'Dictionary-resolved immutable Result Contract schema; local raw-byte evidence readback.', 'run_at_utc': now, 'evidence_ids': ['E_MANIFEST_VALIDATION'], 'notes': 'Executed after manifest assembly, with stable validation log included.'}]

value = {'contract_version': '2.0', 'project': 'FOX2', 'wp_id': WP, 'task_id': claim['task_id'], 'change_id': claim['task_id'],
    'submission_state': 'READY_FOR_CHAT_REVIEW', 'submitted_at_utc': now,
    'agent': {'product': 'CODEX', 'model': claim['model'], 'mode': 'BUILD_CORRECTION_ONLY / high / MANUAL_LOCAL / FULL_ACCESS',
        'host': 'Owner Windows host; offline temporary fixtures', 'started_at_utc': claim['started_at_utc'], 'finished_at_utc': now,
        'quota_observation': binding['auth_capacity'] + '; usage totals NOT_MEASURED'},
    'routing': {**{k: 'PASS' for k in ['policy_check', 'task_state_check', *['r' + str(i) for i in range(8)], 'assignment_check']},
        'routing_evidence': 'Fresh Dispatch and CHAT PASS_TO_ASSIGN plus PreExec REV3; current launcher claim and single process. See source_binding.json.'},
    'source': {'policy_sha256': dispatch['policy']['sha256'], 'policy_version': dispatch['policy']['version'],
        'task_commit_sha': claim['task_commit'], 'source_manifest_sha256': digest((OUT / 'source_binding.json').read_bytes()),
        'approved_base_commit_sha': BASE, 'source_readback_status': 'PASS', 'brd_revisions': ['Bridge TechSpec v0.7 REV10 remains CANDIDATE_NO_PROMOTION; no semantic promotion.'],
        'previous_evidence_reused': ['Recovery snapshot is salvage input only; no A01 PASS reused. A01 consumed/quota failure and historical host FAIL preserved. Fresh A02 tests/static/K1 rerun.']},
    'permissions': {'git_source_read': True, 'git_report_write': True, 'git_report_push': True, 'git_code_push': True, 'code_allowed': True,
        'pr_create': False, 'merge_allowed': False, 'dnse_production': False, 'broker_write': False, 'live': False,
        'grant_evidence': 'Owner task plus fresh A02 Dispatch/CHAT PASS_TO_ASSIGN; offline BUILD only; exact authorized non-main result push.'},
    'git': {'repository': 'dunglt2505/FOX2', 'branch': dispatch['runtime_contract']['branch'], 'worktree': str(ROOT),
        'writer_lease': 'One current task CODEX PID ' + str(claim['process_id']) + '; one running consumed launcher claim; no subagents or competing material writer observed.',
        'report_path': PREFIX + 'report.md', 'delivery_status': 'PUSHED_UNREVIEWED', 'pr_url': None, 'local_head_before_submission': BASE},
    'scope': {'requested': ['Finish and independently verify salvaged lifecycle/WPF certification within the four allowed code/test paths.'],
        'completed': ['Presentation-only WPF contract retained/corrected; negative fixtures; A03 durable uninstall regressions; focused/full tests; static/K1/Result Contract evidence.'],
        'partial': [], 'not_done': ['CHAT acceptance; real installed-host lifecycle certification; G3/G4 adoption.'],
        'explicit_exclusions': ['Real installed lifecycle, Worker/F1, AppLocker/service/ACL, G3/G4/Canary, main/PR/merge/provider/broker/LIVE.'],
        'changed_paths': [], 'forbidden_paths_touched': False},
    'tests': tests, 'acceptance': acceptance, 'evidence': [],
    'risks': [{'id': 'R_HOST_NOT_CERTIFIED', 'severity': 'MEDIUM', 'state': 'NOT_VERIFIED',
        'impact': 'Offline fixture success does not certify the installed Owner-host lifecycle, F1 adoption or G3/G4 readiness.',
        'next_action': 'Independent CHAT intake; separately authorized host certification if approved.', 'owner_role': 'CHAT'}],
    'security': {'secret_scan': 'PASS', 'private_account_data_in_git': False, 'licensed_raw_feed_in_git': False,
        'evidence_redacted': True, 'check_notes': 'Bounded changed-delivery-file scan; no credentials or Bridge durable host data read or changed.'},
    'usage': {'attempts': 1, 'retries': 0, 'usage_status': 'NOT_MEASURED', 'tokens_used': None, 'credits_used': None,
        'escalation_reason': 'No Agent retry or replay; fixture reruns within this one A02 attempt only.'},
    'next_step': {'requested_chat_decision': 'REVIEW', 'action': 'Independently review immutable A02 code/diff/tests/evidence; no acceptance claimed.',
        'owner_role': 'CHAT', 'prerequisite_gate': 'CHAT result intake; any future host lifecycle requires its own authorized task and material PreExec.'}}
known = {r['log']: (run_ids[r['name']], ['T_' + r['name'].upper()]) for r in runs}
known.update({'source_binding.json': ('E_SOURCE', ['T_SOURCE']), 'static_checks.json': ('E_STATIC', ['T_STATIC']),
              'static_validation.log': ('E_STATIC_LOG', ['T_STATIC']), 'manifest_validation.log': ('E_MANIFEST_VALIDATION', ['T_MANIFEST'])})

def write_manifest():
    value['evidence'] = []
    for i, path in enumerate(sorted(OUT.iterdir())):
        assert path.is_file(), path
        eid, supports = known.get(path.name, ('E_ARTIFACT_' + str(i), ['T_STATIC']))
        value['evidence'].append({'id': eid, 'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()),
            'kind': 'TEST_LOG' if path.suffix == '.log' else 'DIFF' if path.suffix == '.diff' else 'OTHER',
            'observed_at_utc': now, 'description': 'A02 offline BUILD evidence: ' + path.name,
            'supports_ids': supports, 'sanitized': True})
    value['evidence'].append({'id': 'E_REPORT', 'path': PREFIX + 'report.md', 'sha256': digest((ROOT / PREFIX / 'report.md').read_bytes()),
        'kind': 'REPORT', 'observed_at_utc': now, 'description': 'A02 bounded BUILD result report.', 'supports_ids': ['T_MANIFEST'], 'sanitized': True})
    paths = sorted(set(git('diff', '--name-only', BASE).decode().splitlines()) |
        set(git('ls-files', '--others', '--exclude-standard').decode().splitlines()) |
        {p.relative_to(ROOT).as_posix() for p in OUT.iterdir()} | {PREFIX + 'report.md', PREFIX + 'evidence_manifest.json'})
    value['scope']['changed_paths'] = [{'path': path,
        'operation': 'MODIFY' if subprocess.run(['git', 'cat-file', '-e', BASE + ':' + path], cwd=ROOT, capture_output=True).returncode == 0 else 'ADD',
        'intent': 'REQUESTED: scoped lifecycle/WPF code/tests and fresh A02 evidence; generated evidence JUSTIFIED_GENERATED.',
        'within_allowed_paths': True, 'new_sha256': None if path == PREFIX + 'evidence_manifest.json' else digest((ROOT / path).read_bytes())}
        for path in paths if path != PREFIX + 'evidence/lifecycle_wpf_contract_rework/recovery_codex001_snapshot.json']
    (ROOT / PREFIX / 'evidence_manifest.json').write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')

# The validation log has constant text and contains no self-referential manifest hash.
validation_path = OUT / 'manifest_validation.log'
validation_path.touch(exist_ok=True)
write_manifest()
validation = subprocess.run([sys.executable, str(OUT / 'verify_result.py'), '--manifest-only'], capture_output=True, text=True)
validation_path.write_text(validation.stdout + validation.stderr, encoding='utf-8', newline='\n')
assert validation.returncode == 0, validation.stdout + validation.stderr
write_manifest()
final = subprocess.run([sys.executable, str(OUT / 'verify_result.py'), '--manifest-only'], capture_output=True, text=True)
assert final.returncode == 0 and final.stdout == validation.stdout, final.stdout + final.stderr
print('A02 BUILD result assembled: focused ' + focused_summary + '; full ' + full_summary)
print(final.stdout, end='')
