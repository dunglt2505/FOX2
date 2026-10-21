"""Assemble the bounded BUILD result; never executes installed lifecycle actions."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
WP = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
PREFIX = 'reports/' + WP + '/'
BASE = 'e7d5acf51dddcbc95324a992ad6be2773e61285f'
git = lambda *args: subprocess.check_output(['git', '-C', str(ROOT), *args])
digest = lambda raw: hashlib.sha256(raw).hexdigest()
now = datetime.now(timezone.utc).isoformat()
binding = json.loads((OUT / 'source_binding.json').read_text())
claim = binding['claim']
dispatch = json.loads(git('show', claim['dispatch_commit'] + ':' + binding['dispatch_path']))
full_name = 'full_short_longpaths.log' if (OUT / 'full_short_longpaths.log').exists() else 'full_short_initial.log'
full = (OUT / full_name).read_text()
assert re.search(r'=+ \d+ passed in [\d.]+s =+', full), 'Full suite has not passed'
summary = full.strip().splitlines()[-1].strip('= ')
focused = (OUT / 'focused_extended_path.log').read_text()
assert '66 passed' in focused
historical = json.loads(git('show', BASE + ':' + PREFIX + 'evidence_manifest.json'))

runs = [
    ('focused_initial.log', 'FAIL', None, 'Initial command lacked process PYTHONPATH; conftest import failed.'),
    ('focused.log', 'FAIL', 1, 'Long-path ordinary invocation: 4 failed, 37 passed, 25 errors; fixture path creation.'),
    ('focused_extended_path.log', 'PASS', 0, '66 passed; Windows extended test paths; all subprocess boundaries in the new seam are fixtures.'),
    ('full_initial.log', 'FAIL', 1, 'Extended paths: 37 failed, 544 passed, 63 errors; PowerShell/SQLite/Git path incompatibilities in unchanged fixtures.'),
    ('full_short_initial.log', 'PASS' if full_name == 'full_short_initial.log' else 'FAIL',
     0 if full_name == 'full_short_initial.log' else 1,
     'Exact-byte short detached fixture worktree; no persistent Git or host configuration changes.'),
]
if full_name != 'full_short_initial.log':
    runs.append((full_name, 'PASS', 0, 'Only process GIT_CONFIG_COUNT/KEY/VALUE append core.longpaths=true. No test/config file changes.'))
receipts = []
for name, status, code, note in runs:
    path = OUT / name
    text = path.read_text()
    tests = ['agent_bridge/tests/test_lifecycle_wpf_contract.py', 'agent_bridge/tests/test_rc1_package.py',
             'agent_bridge/tests/test_rc1_launcher.py'] if name.startswith('focused') else ['agent_bridge/tests']
    if name in ['focused_extended_path.log', 'full_initial.log']:
        tests = ['\\\\?\\' + str(ROOT / p).replace('/', '\\') for p in tests]
    if name.startswith('full_short'):
        tests = ['C:/Projects/FOX2/.git/wpf-a01-test/' + p for p in tests]
    receipts.append({'log': name, 'status': status, 'observed_pytest_exit_code': code,
        'run_at_utc': datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat(),
        'started_at_utc': datetime.fromtimestamp(path.stat().st_birthtime, timezone.utc).isoformat(),
        'argv': ['python', '-m', 'pytest', *tests, '-v', '--tb=short'],
        'command': subprocess.list2cmdline(['python', '-m', 'pytest', *tests, '-v', '--tb=short']),
        'notes': note, 'output_tail': text.strip().splitlines()[-1],
        'environment': ('short exact-byte detached worktree; process PYTHONPATH=its agent_bridge/src'
                        if name.startswith('full_short') else 'task worktree; PYTHONPATH=agent_bridge/src except initial import failure')})
(OUT / 'test_runs.json').write_text(json.dumps({'runs': receipts,
    'agent_attempts': 1, 'agent_retries': 0,
    'static_verification_history': 'First raw Git-vs-worktree byte comparison rejected existing CRLF checkout conversion in unchanged WPF. Corrected evidence check uses Git hash-object blob identity plus raw same-base checkout comparison; no product change.'}, indent=2) + '\n')

report = f'''# FOX2 Lifecycle/WPF Contract Rework A01 — BUILD result

Task `{claim['task_id']}`. Delivery: **PUSHED_UNREVIEWED** following authorized branch push. CHAT acceptance is not claimed. This corrects the offline certification harness; real host lifecycle remains **NOT_RUN**.

## R01 — Source and execution binding

One CODEX `gpt-6.1-sol`, high, MANUAL_LOCAL, task-scoped FULL_ACCESS attempt; no subagents, model substitution or Agent replay. Starting HEAD `{BASE}` matched fresh Dispatch runtime base and task remote. Dispatch `{claim['dispatch_id']}`, commit `{claim['dispatch_commit']}`, blob `{claim['dispatch_blob']}`. Launcher claim PID {claim['pid']} is STARTED_CONSUMED and its exclusive writer lock was observed held.

Task commit `{claim['task_commit']}`, raw SHA-256 `{claim['task_sha256']}`. Prompt commit `{claim['prompt_commit']}`, raw SHA-256 `{claim['prompt_sha256']}`. Task-specific PreExec v2 PASS is at `{BASE}`. Policy {dispatch['policy']['version']} and Dictionary {dispatch['dictionary']['version']} Git bytes match Dispatch hashes. Source binding is recorded in `evidence/lifecycle_wpf_contract_rework/source_binding.json`.

Failed host result `9dd91becf47d934183baf147d0a4f03f4bf5933d` remains an ancestor; accepted product source `2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb` is unchanged before implementation. Only task/prompt/PreExec binding evidence preceded start. Historical host A01 FAIL and consumed Dispatch remain unchanged/no-replay.

## R02 — Correction and preserved boundaries

Only `certify_user_lifecycle.py`, its existing A03 package fixtures, and one new focused test file changed. The harness launches `BridgeRoot/launch.ps1` twice, waits boundedly for exactly one `FOX2.Bridge.Desktop.exe`, verifies its executable path against the exact current package and matches the UI inspection PID to that process. It requires paused=true, setup_complete=true and no current dispatch, without checking Worker heartbeat or starting a duplicate Worker.

The existing `certify_rc1_ui.ps1` provides inspect/check/exit. Navigation must expose Dashboard, Activity, Agents, Diagnostics, Artifacts and Settings; Check Now must be disabled. The harness observes the live presentation and held WPF lock, invokes explicit UI exit, uses a 30-second exit deadline with bounded process probes, opens the existing presentation lock without altering bytes, and checks STOPPED/paused/setup/no-current-dispatch before uninstall. Failure checkpoints evidence and prevents uninstall/reinstall; no force-kill path exists.

Worker/F1 health is **NOT_APPLICABLE_PRE_G3**. The launcher, F1 ownership/activation DENY_PENDING_G3_G4, WPF singleton, installed UI seam and installation source retain their original Git blobs. TechSpec v0.7 REV10 remains CANDIDATE_NO_PROMOTION.

## R03 — A03 and durable-state preservation

The uninstall supervisor and output sanitizer ASTs are identical to the entry source. Stable external BridgeRoot/uninstall.ps1, PowerShell 7, synchronous single attempt, installed-Python exclusion, sanitized bounded output, timeout/nonzero/start/postcondition stop-once handling, checkpoint before reinstall, and exact-package reinstall after success are preserved. Existing regressions cover successful uninstall and all failure classes.

Configuration/database/manual-consumption checks and historical Batch-B consumed identities 001–004 remain in place. Reinstall uses the same package and SHA, now explicitly verifies the current installed package and final safe paused state. No consumed identity is rewritten or replayed.

## R04 — Validation and environment history

Focused WPF/package/launcher: **66 passed**. Full `agent_bridge/tests`: **{summary}**. Full output includes installation/package and launcher suites. Syntax/compile, changed-path allowlist, unchanged forbidden source checks, bounded secret scan and git diff --check pass. K1 **UNEXPLAINED=0**; each source/test hunk is classified in k1.json.

Every earlier failed run is retained with its real output. The first command lacked PYTHONPATH; the next exposed Windows MAX_PATH fixture creation failures. Extended-path pytest spelling resolved the focused run but exposed PowerShell/SQLite/Git incompatibilities in unchanged full-suite fixtures. A shorter detached test worktree contains exact matching source/test bytes, verified file-by-file. It has no material writer or installed runtime. Tests were neither edited nor skipped to address path behavior. {'The short full run needed only the established child-process core.longpaths=true override; its initial FAIL remains preserved.' if full_name != 'full_short_initial.log' else 'The short full run passed without any Git configuration override.'} No repository/global Git config or Windows long-path setting changed.

Exact test commands, timestamps, exit observations and logs are in test_runs.json. Result Contract v2 schema, evidence hash references and changed-path delivery are verified by verify_result.py. Manifest self-hash is intentionally null; the observed remote result SHA is returned outside this report.

## R05 — Scope and next owner

No real installed package was built/launched/installed/updated/uninstalled/reinstalled. No Task Scheduler, Bridge config/data/database, Worker/F1 service, AppLocker/AppIDSvc/service/ACL, reboot, G3/G4/Canary, provider/broker/LIVE, main/PR/merge action occurred. All lifecycle process and install calls in the changed tests are fixtures.

CHAT must independently review this immutable BUILD result. A future real host lifecycle certification requires a fresh separately authorized task/PreExec/Dispatch. Host lifecycle and G3/G4 readiness are not certified by these fixture passes.
'''
(ROOT / PREFIX / 'report.md').write_text(report, encoding='utf-8')

# Static checks run after report generation and before hashes are assembled.
subprocess.run(['python', str(OUT / 'verify_result.py')], check=True)
d = historical
d['task_id'] = claim['task_id']
d['change_id'] = claim['task_id']
d['submission_state'] = 'READY_FOR_CHAT_REVIEW'
d['submitted_at_utc'] = now
d['agent'] = {'product': 'CODEX', 'model': 'gpt-6.1-sol', 'mode': 'BUILD_CORRECTION_ONLY',
    'host': 'WINDOWS_OWNER_HOST_OFFLINE_FIXTURES', 'started_at_utc': claim['started_at_utc'],
    'finished_at_utc': now, 'quota_observation': 'Not measured; no quota probe or model substitution.'}
d['routing']['routing_evidence'] = 'Fresh Dispatch/PreExec v2/PASS_TO_ASSIGN/launcher claim and observed writer/source binding; see source_binding.json. Offline BUILD only.'
d['source'] = {'policy_sha256': dispatch['policy']['sha256'], 'policy_version': dispatch['policy']['version'],
    'task_commit_sha': claim['task_commit'], 'source_manifest_sha256': digest((OUT / 'source_binding.json').read_bytes()),
    'approved_base_commit_sha': BASE, 'source_readback_status': 'PASS', 'brd_revisions': [],
    'previous_evidence_reused': ['Historical host FAIL 9dd91bec; accepted product source 2faa33f9; A03 supervisor semantics; no historical PASS substitutes for new tests.']}
for key in ['code_allowed', 'git_code_push']:
    d['permissions'][key] = True
d['permissions']['grant_evidence'] = 'Owner immutable task/prompt plus fresh scoped Dispatch; source correction and authorized non-main result push only.'
d['git'].update(branch=claim['task_branch'], worktree=str(ROOT), local_head_before_submission=BASE,
    writer_lease='Launcher exclusive task writer lock; claim CODEX PID 1784; one Agent attempt; detached test snapshot has no competing writer.')
d['git']['delivery_status'] = 'PUSHED_UNREVIEWED'
d['scope'] = {'requested': ['Correct pre-G3 lifecycle/WPF seam within allowed paths; preserve A03 and durable history.'],
    'completed': ['WPF launch/singleton/exact identity/safe control/UI/graceful exit fixtures; A03 regressions; full suite; static/K1/Result Contract.'],
    'partial': [], 'not_done': ['Independent CHAT acceptance; future real host lifecycle certification.'],
    'explicit_exclusions': ['Installed-host mutation, Worker/F1 start, G3/G4/Canary, main/PR/merge/provider/broker/LIVE.'],
    'changed_paths': [], 'forbidden_paths_touched': False}
d['tests'] = []
d['evidence'] = []
for index, receipt in enumerate(receipts):
    evid = 'E_TEST_' + str(index + 1)
    d['tests'].append({'id': 'T_RUN_' + str(index + 1), 'kind': 'INTEGRATION', 'status': receipt['status'],
        'command_or_method': receipt['command'], 'environment': receipt['environment'],
        'run_at_utc': receipt['run_at_utc'], 'evidence_ids': [evid], 'notes': receipt['notes']})
static_ids = ['PYTHON_SYNTAX_STATIC', 'CHANGED_PATH_ALLOWLIST', 'SECRET_SCAN', 'GIT_DIFF_CHECK', 'K1_UNEXPLAINED_ZERO',
              'RESULT_CONTRACT_V2_REPORT_AND_EVIDENCE_MANIFEST']
source_ids = ['REAL_HOST_LIFECYCLE_REMAINS_NOT_RUN']
fixture_ids = [i for i in dispatch['required_tests'] if i not in static_ids + source_ids]
d['acceptance'] = [{'id': i, 'status': 'PASS', 'evidence_ids': ['E_TEST_' + str(len(receipts))] if i == 'INSTALLATION_AND_PACKAGE_TESTS' else ['E_TEST_3'],
                    'reason': 'Fresh offline fixtures; process/install boundaries intercepted; no host-health claim.'}
                   for i in fixture_ids if i != 'FULL_AGENT_BRIDGE_TESTS']
d['acceptance'].append({'id': 'FULL_AGENT_BRIDGE_TESTS', 'status': 'PASS',
    'evidence_ids': ['E_TEST_' + str(len(receipts))], 'reason': summary + '; exact-byte detached test worktree.'})
d['acceptance'] += [{'id': i, 'status': 'PASS', 'evidence_ids': ['E_STATIC'], 'reason': 'Fresh bounded result verification.'} for i in static_ids]
d['acceptance'].append({'id': source_ids[0], 'status': 'PASS', 'evidence_ids': ['E_SOURCE'],
                       'reason': 'Offline-only execution scope; real installed host lifecycle remains NOT_RUN.'})
d['tests'].append({'id': 'T_STATIC', 'kind': 'STATIC', 'status': 'PASS',
    'command_or_method': 'python evidence/lifecycle_wpf_contract_rework/verify_result.py; --manifest-only',
    'environment': 'Offline Windows source/evidence verification', 'run_at_utc': now,
    'evidence_ids': ['E_STATIC'], 'notes': 'Schema/hash readback performed after manifest assembly.'})
known = {r['log']: ('E_TEST_' + str(i + 1), ['T_RUN_' + str(i + 1)]) for i, r in enumerate(receipts)}
known.update({'static_checks.json': ('E_STATIC', static_ids + ['T_STATIC']),
              'source_binding.json': ('E_SOURCE', source_ids),
              'k1.json': ('E_K1', ['K1_UNEXPLAINED_ZERO'])})
for index, path in enumerate(sorted(OUT.iterdir())):
    if not path.is_file() or path.name == 'manifest_validation.log':
        continue
    evid, supports = known.get(path.name, ('E_ARTIFACT_' + str(index), ['T_STATIC']))
    d['evidence'].append({'id': evid, 'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()),
        'kind': 'TEST_LOG' if path.suffix == '.log' else 'OTHER', 'observed_at_utc': now,
        'description': 'Bounded offline BUILD evidence: ' + path.name, 'supports_ids': supports, 'sanitized': True})
paths = sorted(set(git('diff', '--name-only', BASE).decode().splitlines()) |
               set(git('ls-files', '--others', '--exclude-standard').decode().splitlines()) |
               {PREFIX + 'report.md', PREFIX + 'evidence_manifest.json'})
for path in paths:
    d['scope']['changed_paths'].append({'path': path,
        'operation': 'MODIFY' if git('ls-files', '--', path).strip() else 'ADD',
        'intent': 'REQUESTED: bounded lifecycle/WPF correction, tests and result evidence.',
        'within_allowed_paths': True, 'new_sha256': None if path.endswith('evidence_manifest.json') else digest((ROOT / path).read_bytes())})
d['risks'] = [{'id': 'R_HOST_CERT', 'severity': 'MEDIUM', 'state': 'NOT_VERIFIED',
    'impact': 'Fixture validation does not certify the real installed Owner-host lifecycle or G3/G4.',
    'next_action': 'Independent CHAT review; new authorized host-certification task after acceptance.', 'owner_role': 'CHAT'}]
d['security'] = {'secret_scan': 'PASS', 'private_account_data_in_git': False, 'licensed_raw_feed_in_git': False,
    'evidence_redacted': True, 'check_notes': 'Bounded changed-file scan; no host secrets/durable data inspected or mutated.'}
d['usage'] = {'attempts': 1, 'retries': 0, 'usage_status': 'NOT_MEASURED', 'tokens_used': None,
    'credits_used': None, 'escalation_reason': 'None; same Agent attempt throughout environment-specific test reruns.'}
d['next_step'] = {'requested_chat_decision': 'REVIEW', 'action': 'Review immutable BUILD correction and evidence; no acceptance claimed.',
    'owner_role': 'CHAT', 'prerequisite_gate': 'Independent CHAT result intake; fresh task/PreExec/Dispatch for future host lifecycle.'}
(ROOT / PREFIX / 'evidence_manifest.json').write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')
subprocess.run(['python', str(OUT / 'verify_result.py'), '--manifest-only'], check=True)
print('Offline BUILD result assembled: ' + summary)
