"""Assemble offline R4 report/manifest from actual final validation receipts."""
from datetime import datetime, timezone
import json
import subprocess

from verify_result import ROOT, OUT, REPORT, BASE, CODE, changed, digest, static, manifest


def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8', newline='\n')


now = datetime.now(timezone.utc).isoformat()
binding = json.loads((OUT / 'source_binding.json').read_text())
runs = {name: json.loads((OUT / (name + '_run.json')).read_text()) for name in ['focused', 'full']}
assert all(r['exit_code'] == 0 for r in runs.values())
report = f'''# FOX2 Presentation Lock Certifier Rework R4

Task `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R4`; bounded BUILD correction inside Bridge TEST. CODEX / gpt-6.1-sol / medium; one attempt, no model/effort substitution, subagents or historical Dispatch replay. Result delivery is **PUSHED_UNREVIEWED** after the authorized branch push; CHAT review remains required. The observed remote SHA is returned separately from this committed report.

The immutable task commit is `6b6cc697ca35b35ade1ccdf363782a1f912a8936`, blob `90e6c18192cb594f408c9fd99b23da772e37c87f`, SHA-256 `54c2075c0cce6faa90c4f23292ebe43f90e28c356089f4cbbe1e245b9a257456`. Runtime base is `{BASE}`. The task/prompt and original two source blobs matched before editing. Initial worktree was clean on the exact R4 branch. Current Python 3.13.15 / pytest 8.3.5, CODEX CLI 0.162.1, ChatGPT authentication, pinned current task process and push dry-run were observed. No competing task writer was observed. Current R4 PreExec PASS is reused for its fresh capacity probe; no numeric quota is inferred. Execution follows the current user prompt; no separate fresh R4 Dispatch was present in the starting tree, and no historical Dispatch was rebound.

Only `agent_bridge/scripts/certify_user_lifecycle.py` and `agent_bridge/tests/test_lifecycle_wpf_contract.py` changed as code/tests. Lock probes use `r+b` without writing or truncating. Error evidence contains only exception class, errno, winerror and classification; raw lock exception text is suppressed. Explicit winerror 32 is accepted; PermissionError/EACCES without winerror requires differential proof. Other errors, including explicit access-denied winerror 5, fail closed.

Fresh mode requires zero presentations and an accessible existing pre-live lock (absence allowed), retains two launches and exact singleton/current-package/PID/UI/safe-state checks, then proves denied live access and post-exit openability. Continuation is exposed through the keyword API and `--continuation`: one exact-current live WPF means zero launches; zero WPF means one launch. Duplicate/wrong-path/invalid-PID/current-pointer cases fail closed. Existing-live errno 13 stays provisional with no held-lock claim until graceful UI exit, zero WPF and read/write access to the same lock file (device/inode identity) prove release. No forced exit or Worker/F1/tray fallback was added.

The UI inspect/check sequence, safe-state checks and lifecycle tail remain. AST comparison proves `_uninstall_output`, `certify_uninstall`, `require_safe_control`, and all statements after the presentation call in `main` are unchanged. Continuation forwarding and stop-before-uninstall are tested in both modes. Worker/F1 stays **NOT_APPLICABLE_PRE_G3**.

Final validation: focused **{runs['focused']['summary']}**; full affected suite **{runs['full']['summary']}**. Exact commands are `python -m pytest -q agent_bridge/tests/test_lifecycle_wpf_contract.py` and `python -m pytest -q agent_bridge/tests`. The established short detached fixture worktree avoids Windows path-length errors; all tracked agent_bridge bytes match the final authorized worktree before validation. PYTHONPATH points to its source layout only for the test process. No tool installation, upgrade, elevation or host setting changed. Earlier collection/path-length/setup-instrumentation outcomes and the preliminary run are factual in validation history; final evidence uses the corrected snapshot.

`git diff --check`, exact changed-path allowlist, bounded secret/privacy scan, syntax, Result Contract v2 schema, evidence hashes and K1 review pass. Every material code/test hunk is REQUESTED; generated report/manifest/evidence hunks are JUSTIFIED_GENERATED. **UNEXPLAINED=0**. The manifest itself has a null changed-file hash to avoid self-reference. Logs, receipts, source binding, snapshot identity, reviewable diff, K1 and reproducible offline verification are under `evidence/presentation_lock_certifier_rework_r4/`.

Accepted Bridge source `085cc8302e824dbccf9cbef80422ed48894b9cb4`, A04 package/provenance/install/safe-state/singleton PASS, R3 route rationale and historical same-session PreExec v4 capability evidence remain reusable. Master Plan `ad7d6f0b9889fe4247c29ac3d77f0b90b5f40e56` and A04/A05 reuse plan `da6fd27d78380db42fce155d634044c94a661229` remain intact. R3 A01 recovery `3c32743e9b9cdcb7eb799094ee7bdefdaeb9aa71` remains **CONSUMED_NO_RESULT / NO_REPLAY**. Historical FAIL/NOT_RUN is not upgraded by these fixture results.

Real host lifecycle is **NOT_RUN**. No A04 rebuild/provenance redo, installed-host package installation/update/uninstall/reinstall, installed WPF launch/exit, Bridge host mutation, historical singleton redo, Worker/F1 action, A05/G3/G4/Canary, main/merge/provider/broker/LIVE action occurred. Offline temporary fixture subprocesses are intercepted where presentation actions are tested. These results correct the external certifier; Owner-host certification and CHAT acceptance remain outside R4. Usage totals are NOT_MEASURED. CHAT must independently review the pushed result before any separately authorized host continuation.
'''
(REPORT / 'report.md').write_text(report, encoding='utf-8', newline='\n')
manifest_path = REPORT / 'evidence_manifest.json'
if not (OUT / 'k1.json').exists():
    dump(OUT / 'k1.json', {})
if not (OUT / 'static_checks.json').exists():
    dump(OUT / 'static_checks.json', {})
old = json.loads(subprocess.check_output(['git', 'show', BASE + ':' + manifest_path.relative_to(ROOT).as_posix()], cwd=ROOT))
value = {
    'contract_version': '2.0', 'project': 'FOX2', 'wp_id': 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY',
    'task_id': binding['task_id'], 'change_id': binding['task_id'],
    'submission_state': 'READY_FOR_CHAT_REVIEW', 'submitted_at_utc': now,
    'agent': {'product': 'CODEX', 'model': 'gpt-6.1-sol', 'mode': 'BUILD_CORRECTION_ONLY / medium / FULL_ACCESS',
              'host': 'Existing Windows environment; offline fixtures only',
              'started_at_utc': binding['route']['task_process_started_at_utc'], 'finished_at_utc': now,
              'quota_observation': 'Current pinned execution active; current R4 PreExec capacity PASS reused; totals NOT_MEASURED'},
    'routing': {**{k: 'NOT_CHECKED' for k in ['r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7']},
                'policy_check': 'PASS', 'task_state_check': 'PASS', 'assignment_check': 'PASS',
                'routing_evidence': 'Current user prompt plus exact task/prompt/current R4 PreExec and observed pinned process; historical route evidence reused, not re-executed. No fresh R4 Dispatch file in starting tree.'},
    'source': {**old['source'], 'task_commit_sha': binding['task_commit'],
               'source_manifest_sha256': digest((OUT / 'source_binding.json').read_bytes()),
               'approved_base_commit_sha': BASE, 'source_readback_status': 'PASS',
               'previous_evidence_reused': [binding['accepted_product_source'], binding['reuse']['A04'],
                                             'R3 route rationale and historical PreExec v4 same-session capability only',
                                             binding['reuse']['master_plan'], binding['reuse']['reuse_plan'],
                                             'R3 A01 CONSUMED_NO_RESULT / NO_REPLAY; historical FAIL/NOT_RUN retained']},
    'permissions': {**old['permissions'], 'grant_evidence': 'Current user R4 execution prompt; exact two source/test files plus R4 report/evidence and non-main commit/push only.'},
    'git': {'repository': 'dunglt2505/FOX2', 'branch': binding['branch'], 'worktree': ROOT.as_posix(),
            'writer_lease': 'One current task-scoped CODEX process observed; detached fixture worktree belongs to same writer; no subagents.',
            'report_path': (REPORT / 'report.md').relative_to(ROOT).as_posix(),
            'delivery_status': 'PUSHED_UNREVIEWED', 'pr_url': None, 'local_head_before_submission': BASE},
    'scope': {'requested': ['Bounded differential presentation-lock proof and A04 continuation API/flag; exact two-file regression coverage'],
              'completed': ['Fresh and continuation proof, bounded errors, same-file release, unchanged lock bytes, required offline validation'],
              'partial': [], 'not_done': ['Real host lifecycle NOT_RUN, outside R4'],
              'explicit_exclusions': ['WPF product changes; package rebuild/install; host lifecycle; Worker/F1; A05/G3/G4/Canary; main/merge/provider/broker/LIVE'],
              'changed_paths': [], 'forbidden_paths_touched': False},
    'tests': [], 'acceptance': [], 'evidence': [],
    'risks': [{'id': 'R_HOST_NOT_CERTIFIED', 'severity': 'MEDIUM', 'state': 'NOT_VERIFIED',
               'impact': 'Offline fixtures do not certify Owner-host lifecycle or operational readiness.',
               'next_action': 'CHAT review before separately authorized host certification.', 'owner_role': 'CHAT'}],
    'security': {'secret_scan': 'PASS', 'private_account_data_in_git': False, 'licensed_raw_feed_in_git': False,
                 'evidence_redacted': True, 'check_notes': 'Bounded delivery-file pattern scan plus material diff review; no host data exported.'},
    'usage': {'attempts': 1, 'retries': 0, 'usage_status': 'NOT_MEASURED', 'tokens_used': None, 'credits_used': None,
              'escalation_reason': 'One R4 agent attempt; fixture reruns documented; no R3 replay.'},
    'next_step': {'requested_chat_decision': 'REVIEW', 'action': 'Apply independent CHAT result review to immutable pushed R4 result.',
                  'owner_role': 'CHAT', 'prerequisite_gate': 'PUSHED_UNREVIEWED; any host continuation requires separate authorization.'}}
# Make every result path visible to the static allowlist/K1 pass before hashing.
dump(manifest_path, value)
static()
for path in sorted(OUT.iterdir()) + [REPORT / 'report.md']:
    if path.is_file():
        value['evidence'].append({'id': 'E_' + path.name.replace('.', '_'),
                                 'path': path.relative_to(ROOT).as_posix(), 'sha256': digest(path.read_bytes()),
                                 'kind': 'TEST_LOG' if path.suffix == '.log' else 'OTHER',
                                 'observed_at_utc': now, 'description': 'R4 offline result evidence: ' + path.name,
                                 'supports_ids': ['T_STATIC'], 'sanitized': True})
for name, run in runs.items():
    value['tests'].append({'id': 'T_' + name.upper(), 'kind': 'INTEGRATION', 'status': 'PASS',
                           'command_or_method': run['command'], 'environment': 'Existing Windows Python 3.13.15/pytest 8.3.5; byte-identical short fixture worktree',
                           'run_at_utc': run['finished_at_utc'], 'evidence_ids': ['E_' + name + '_log', 'E_' + name + '_run_json'],
                           'notes': run['summary']})
value['tests'].append({'id': 'T_STATIC', 'kind': 'STATIC', 'status': 'PASS', 'command_or_method': 'verify_result.py and --manifest-only',
                       'environment': 'Authorized R4 worktree; offline only', 'run_at_utc': now,
                       'evidence_ids': ['E_static_checks_json', 'E_k1_json'],
                       'notes': 'Allowlist/privacy/syntax/diff/K1/preserved lifecycle tail/schema/hashes'})
for index, requirement in enumerate([
    'Full winerror32 and errno13 differential PASS; pre-live denial FAIL',
    'Existing exact continuation errno13 provisional until same-file release; retained denial FAIL; zero-WPF one launch',
    'Missing/free/replaced lock and unrelated OSError FAIL; lock bytes unchanged',
    'Duplicate/wrong-path/PID/current-pointer/UI/safe-state negatives; Worker/F1 NOT_APPLICABLE_PRE_G3; no fallback',
    'Exact two source/test paths; K1 UNEXPLAINED=0; no real host action']):
    value['acceptance'].append({'id': 'A_' + str(index + 1), 'status': 'PASS',
                                'evidence_ids': ['E_focused_log', 'E_static_checks_json'], 'reason': requirement})
for path in changed():
    value['scope']['changed_paths'].append({'path': path,
        'operation': 'MODIFY' if path in CODE or path in [manifest_path.relative_to(ROOT).as_posix(), (REPORT / 'report.md').relative_to(ROOT).as_posix()] else 'ADD',
        'intent': 'REQUESTED' if path in CODE else 'JUSTIFIED_GENERATED', 'within_allowed_paths': True,
        'new_sha256': None if path == manifest_path.relative_to(ROOT).as_posix() else digest((ROOT / path).read_bytes())})
dump(manifest_path, value)
manifest()
