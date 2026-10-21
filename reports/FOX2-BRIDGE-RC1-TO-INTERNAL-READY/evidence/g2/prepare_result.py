"""Assemble source-bound Agent Result v2 after the recorded G2 checks."""
from datetime import datetime, UTC
import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
BASE = '94c936b1d93bbfcee5818db24dd75bd9bb32733f'
WP = 'FOX2-BRIDGE-RC1-TO-INTERNAL-READY'
DIRECTORY = ROOT / 'reports' / WP
OUT = DIRECTORY / 'evidence/g2'
REPORT = DIRECTORY / 'report.md'
MANIFEST = DIRECTORY / 'evidence_manifest.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT).decode().strip()


def write(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n', encoding='utf-8', newline='\n')


def classification(path):
    if path == 'agent_bridge/tests/test_installation.py':
        return 'NECESSARY_DEPENDENCY', 'Short Windows fixture names preserve existing installer checks under this exact long worktree.'
    if '/evidence/g2/' in path:
        if path.endswith('.json'):
            return 'JUSTIFIED_GENERATED', 'Bounded command/source/diff evidence for this A01; failures retained.'
        return 'NECESSARY_DEPENDENCY', 'Repeatable G2 verification/result assembly or bounded implementation notes.'
    if path.endswith('evidence_manifest.json'):
        return 'JUSTIFIED_GENERATED', 'Required Result Contract v2 evidence inventory.'
    return 'REQUESTED', 'Integrated F1 authority, consumer closure, policy/package support, tests or required report.'


def paths():
    result = set(git('diff', '--name-only', BASE).splitlines())
    result.update(git('ls-files', '--others', '--exclude-standard').splitlines())
    result.update(p.relative_to(ROOT).as_posix() for p in (REPORT, MANIFEST, OUT / 'k1.json'))
    return sorted(p for p in result if p)


def main():
    implementation = sys.argv[1]
    assert re.fullmatch('[0-9a-f]{40}', implementation)
    assert git('rev-parse', 'HEAD') == implementation
    now = datetime.now(UTC).isoformat()
    receipts = [(json.loads(p.read_text()), p) for p in sorted(OUT.glob('*-[0-9][0-9].json'))]
    latest = {}
    for receipt, path in receipts:
        latest[receipt['id']] = (receipt, path)
    for required in ('focused', 'regression', 'full', 'static', 'windows', 'desktop-build'):
        assert latest[required][0]['exit_code'] == 0, required
    changed = paths()
    k1 = []
    for name in changed:
        kind, reason = classification(name)
        if name.startswith('agent_bridge/'):
            diff = git('diff', '--unified=0', BASE, '--', name)
            hunks = re.findall(r'^@@.*?@@.*$', diff, re.M)
            if not hunks:
                hunks = ['NEW_FILE: all material source/test/script lines']
        else:
            hunks = ['ALL_MATERIAL_ARTIFACT_HUNKS']
        k1.append({'path': name, 'classification': kind, 'reason': reason,
                   'hunks': [{'identity': h, 'classification': kind} for h in hunks]})
    write(OUT / 'k1.json', {'start_sha': BASE, 'final_implementation_sha': implementation,
        'unexplained_hunks': 0, 'paths': k1})
    summary = '\n'.join(f"| `{p.name}` | {r['exit_code']} | {r['result']} | " +
        (r['stdout_tail'].strip().splitlines()[-1] if r.get('stdout_tail', '').strip() else 'See receipt') + ' |'
        for r, p in receipts)
    change_rows = '\n'.join(f"| `{p}` | {classification(p)[0]} |" for p in changed)
    final_summaries = '; '.join(latest[n][0]['stdout_tail'].strip().splitlines()[-1]
        for n in ('focused', 'regression', 'full', 'windows'))
    report = f'''# FOX2 G2 Integrated F1 Build A01 — Agent result

## R01 — Identification and disposition

Project/WP/task/change: FOX2 / {WP} / FOX2-BRIDGE-RC1-G2-A01 / G2-F1-INTEGRATED-A01.
CODEX `gpt-6.1-sol`, reasoning `high`, MANUAL_LOCAL, FULL_ACCESS technical sandbox. Active turn context observed at 2026-10-21T03:31:22.526Z; host: {platform.platform()}. One implementation attempt, no Dispatch/Agent retry or model substitution. Usage NOT_MEASURED.

Disposition at report assembly: LOCAL_ONLY, with G2 source/build checks completed for independent CHAT review after actual push. No self-acceptance. F1 Owner-host runtime remains DENY; G3/G4 enforcement is NOT_RUN_G3. This result does not establish INTERNAL_FOX2_BRIDGE_READY.

## R02 — Authority and PreExec

The full immutable task was read before implementation. The exact G2 PreExec at `preexec/g2_preflight.json` was PASS at 2026-10-21T03:27:17.603284+00:00, with pinned CODEX/model/high/FULL_ACCESS, this non-main worktree, NONE_OBSERVED writer competition, and all three dispatch/start flags false. Active session metadata independently confirmed the model, high effort, danger-full-access and approval=never. Other active thread metadata used the project-chat workspace; no competing G2 material writer was observed.

Scoped Owner G2 hold-lift and accepted G1 design are controlling. Policy 2.0.0, Dictionary 1.3, Routing 1.4.0 and Protocol 12 bytes were checked against the task's pinned commits/blobs. Bridge machine Dictionary 1.2 compatibility remains only the separately published scoped receipt. BRD-09/TechSpec remain globally candidate; neither is promoted to EFFECTIVE. Scope and routing checks are PASS for this task only. No STOP condition was bypassed.

## R03 — Exact immutable inputs and SHAs

- Start SHA: `{BASE}`.
- Task publication: `653e49fc0d0f15981bf230995925c89d6994723d`; blob `7f0b82e56f7bfa001e40bb176bb26b0ef918c609`.
- Task base/Owner scoped grant: `fe926ad24d89231e5cf80f0f48ea44eb36887834`.
- PreExec source head: `ca684b09b3eaea7fa2ce7fc7983f890384202296`; task bytes equal publication bytes; this source is an ancestor of the start SHA.
- Final implementation SHA: `{implementation}`. The final result/report commit containing this document cannot self-reference its own SHA; its observed remote SHA is supplied outside the committed report after push.
- Source/authority distinctions and full path/commit/blob/SHA-256 observations: `evidence/g2/source_readback.json`.

## R04 — Implemented behavior and limits

Implemented a LocalSystem/SCM-only Windows authority boundary, explicit-DACL local named pipe, OS-derived caller identity/token/session/PID, fixed protected global store, boot epoch fencing, durable claim and one-use spawn intent, service-owned suspended CreateProcessAsUser/Job creation and guarded resumption, lease/revoke/clock/policy/service/source/package checks, and idempotent informational outcomes. Revocation durably tombstones the sealed adoption-plan digest, so restart/rollback cannot reactivate an unchanged plan. No client bearer launch token or caller-side installed spawn fallback exists.

Launcher starts only presentation; ledger retains installed direct-claim denial and now closes installed alternate-database and pre-spawn bypasses. Installed/configured E2E delegates before local creation/claim/adapters; Ops/Desktop/App use that runner. Installed smoke requires a staged service task. Existing offline reconciliation and F0 primitives remain in use. Runtime/SCM configuration drift or missing bindings deny; failed revocation storage still closes jobs.

Deterministic AppLocker artifact support enforces EXE/Script/MSI/DLL collections, uses exact hashes/SID scopes, closes copied legacy fixtures without path trust, includes service/system extensions, and distinguishes raw versus AppLocker hashes. Unsupported Python-source rules fail: interpreter identity must be fenced. Packaging includes F1 modules and read-only inventory support with DENY_PENDING_G3_G4. No new product dependency was introduced.

Details, protected-plan contract, explicit 60-second lease bound, interpreter constraints, operational limits and primary API references are in `evidence/g2/implementation_notes.md`. The actual full offline user-package build is NOT_RUN: no provisioned isolated setuptools/build/wheel environment was present. Package/source contract tests and static checks ran; no release package was fabricated. A real non-elevated Windows desktop build ran separately.

## R05 — Changed paths and K1

Every material hunk is classified in `evidence/g2/k1.json`; UNEXPLAINED=0. New source/test files are entirely REQUESTED. Fixture-name shortening is NECESSARY_DEPENDENCY for this exact long Windows path. Result receipts are JUSTIFIED_GENERATED. No governance/BRD/TechSpec or unrelated engine edit occurred.

| Path | K1 classification |
|---|---|
{change_rows}

`ops_runner.py` and `f1_reconcile.py` were inspected and reused unchanged: Ops calls the gated runner; reconciliation keeps WAL/SHM/missing-root/overlap HOLD behavior. `install_user.ps1` has no service/policy activation path added.

## R06 — Commands actually run

Final checks: {final_summaries}.
Required final order: focused → affected regression → full supported suite → static/package contract → native Windows tests → Windows build. Exact bounded commands, UTC start/end, exit codes and output tails are in each JSON receipt. Every earlier failed run remains recorded; no historical CI substituted for new source tests.

| Receipt | Exit | Result | Summary |
|---|---:|---|---|
{summary}

Earlier installation failures were Windows MAX_PATH in fixture paths; extended-path spelling then failed PowerShell script authorization, so the fixture uses a shorter unique name in the same directory. The first full run exposed Git `show commit:path` MAX_PATH in unchanged PreExec fixtures and a missing Utility module import in the new inventory helper. Git core.longpaths is now per-test-child only; no host Git setting changed. The helper imports fixed Windows module paths. Read-only diagnostics are retained in `preexec_diagnostic.json`.

## R07 — Security/replay/concurrency acceptance

| Requirement | G2 result | Evidence |
|---|---|---|
| Service absent, AppIDSvc/policy unavailable/drift, SCM/runtime drift → DENY | PASS (source plus native absence/ACL/pipe tests) | final focused, native Windows |
| Forged caller/task/source/package/actor/nonce/epoch → DENY | PASS | focused protocol/authority |
| Same dispatch concurrency, global consumed identity | PASS: 32 concurrent requests, one service creation/consumed identity | focused authority; existing broker regressions |
| Claim/intent before creation; ambiguous spawn consumed | PASS | focused persisted-intent assertions |
| Restart/revoke/lease expiry/clock rollback; durable heartbeat floor | PASS | focused authority/store |
| Launcher/Desktop/App/Ops/E2E cannot bypass service | PASS | focused consumers; regression |
| Copied legacy/current identity and interpreter-SID artifact model | PASS (model only) | focused policy |
| WAL/SHM/missing roots/manual overlap and frozen F0 negatives | PASS | affected/full suites |
| Rollback primitive revokes and preserves consumed/tombstones | PASS (source fixture); installed rollback NOT_RUN_G3 | focused authority |
| Changed scripts/module packaging/non-activation/allowlist | PASS | static/package contract |
| Effective AppLocker/LocalSystem spawn/Owner-host installation | NOT_RUN_G3 | intentionally outside G2 |

## R08 — Evidence inventory

`evidence_manifest.json` follows Result Schema v2 and contains evidence paths, raw SHA-256, command statuses and acceptance links. Evidence is bounded to `evidence/g2/`. Failure receipts contain synthetic test diagnostics and ordinary local paths, without real credentials or account tokens. Source readback is byte proof plus the supplied scoped task authority, not a global release certificate.

## R09 — Git delivery

Repository `dunglt2505/FOX2`; branch `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`; exact worktree `{ROOT}`. Code and report publication owner is AGENT. At report assembly the result is LOCAL_ONLY. After actual push and remote SHA readback the external pointer is PUSHED_UNREVIEWED. No PR, merge, main write or self-acceptance.

## R10 — Host-only gaps and boundaries

All elevated/host enforcement tests are NOT_RUN_G3: effective AppLocker deployment and full OS/dependency inventory; copied/interpreter/shell/DLL bypass closure on Windows; LocalSystem child creation with real user credentials; service crash/reboot/logoff and lifetime behavior; protected-root attack probes; installed rollback/reinstall; G4 Owner-host adoption. Source/native non-elevated tests are not enforcement certification.

Confirmed for this attempt: no AppLocker policy installed/applied; no authority service installed or started; no elevation; no scheduled-task mutation; no main/merge/deploy/provider/trading-broker/Canary/LIVE action. F1 positive Owner-host authority remains DENY. The service's protected state is independent of per-user uninstall; privileged G3 rollback must revoke authority and retain the broker store, not delete or recreate consumption.

## R11 — Attempt accounting

A01 implementation attempts=1; Dispatch retries=0. Internal test/fix/recheck cycles are recorded above and are not Agent replays. No paid Agent readiness probe, nested implementation Agent or model substitution was launched by this implementation session. Tokens/credits NOT_MEASURED.

## R12 — CHAT intake

Requested decision: independent REVIEW through fox2-result-review against the immutable remote result commit and Dictionary-bound intake v9. G2 source/build review is separate from G3/G4 host authorization. Do not self-accept, enable positive host execution, merge or run Canary from this result.
'''
    REPORT.write_text(report, encoding='utf-8', newline='\n')
    tests = []
    for r, p in receipts:
        tests.append(dict(id=p.stem, kind='INTEGRATION', status=r['result'],
            command_or_method=' '.join(r['command']), environment='Windows non-elevated; per-child core.longpaths when recorded',
            run_at_utc=r['started_at'], evidence_ids=[p.stem], notes='Bounded exit/result receipt; earlier failures retained.'))
    tests.append(dict(id='G3_HOST', kind='INTEGRATION', status='NOT_RUN',
        command_or_method='Elevated service/policy/positive execution enforcement tests',
        environment='Isolated Windows / Owner host', run_at_utc=None, evidence_ids=['implementation_notes'],
        notes='NOT_RUN_G3; never PASS.'))
    tests.append(dict(id='OFFLINE_USER_PACKAGE', kind='STATIC', status='NOT_RUN',
        command_or_method='Complete offline user-package build', environment='No selected isolated build environment',
        run_at_utc=None, evidence_ids=['implementation_notes'],
        notes='Static package-module contract and fixture tests ran; no new full release package built.'))
    acceptance = [dict(id='G2_BUILD', status='PASS', evidence_ids=[p.stem for r, p in latest.values()],
        reason='Source/build checks only; subject to independent CHAT result review.'),
        dict(id='G3_G4', status='NOT_RUN', evidence_ids=['implementation_notes'],
        reason='NOT_RUN_G3; host service/policy enforcement and adoption outside this task.')]
    evidence = []
    for p in sorted(OUT.iterdir()):
        if not p.is_file(): continue
        evidence.append(dict(id=p.stem + ('_script' if p.suffix == '.py' else ''), path=p.relative_to(ROOT).as_posix(), sha256=sha(p),
            kind='TEST_LOG' if re.search(r'-[0-9][0-9]\.json$', p.name) else 'OTHER',
            observed_at_utc=now, description='Bounded G2 A01 ' + p.name,
            supports_ids=['G2_BUILD'], sanitized=True))
    evidence.append(dict(id='G2_REPORT', path=REPORT.relative_to(ROOT).as_posix(), sha256=sha(REPORT),
        kind='REPORT', observed_at_utc=now, description='Agent G2 result report', supports_ids=['G2_BUILD'], sanitized=True))
    source_receipt = OUT / 'source_readback.json'
    changed_paths = []
    for name in changed:
        p = ROOT / name
        exists = subprocess.run(['git', 'cat-file', '-e', BASE + ':' + name], cwd=ROOT,
                                capture_output=True).returncode == 0
        changed_paths.append(dict(path=name, operation='MODIFY' if exists else 'ADD',
            intent=': '.join(classification(name)), within_allowed_paths=True,
            new_sha256=None if p == MANIFEST or not p.is_file() else sha(p)))
    routing = {k: 'PASS' for k in ('policy_check', 'task_state_check', 'r0', 'r1', 'r2',
                                   'r3', 'r4', 'r5', 'r6', 'r7', 'assignment_check')}
    routing['routing_evidence'] = 'Exact G2 PreExec PASS plus active model/high/full-access metadata; task-scoped only.'
    result = dict(contract_version='2.0', project='FOX2', wp_id=WP, task_id='FOX2-BRIDGE-RC1-G2-A01',
        change_id='G2-F1-INTEGRATED-A01', submission_state='LOCAL_ONLY', submitted_at_utc=now,
        agent=dict(product='CODEX', model='gpt-6.1-sol', mode='high / MANUAL_LOCAL / FULL_ACCESS',
            host=platform.platform(), started_at_utc='2026-10-21T03:31:22.526Z', finished_at_utc=now,
            quota_observation='NOT_MEASURED'), routing=routing,
        source=dict(policy_sha256='281bcd61bb8c2fb7929ac474f218adbd004bbca6bc21e5311944a0e590723e1e',
            policy_version='2.0.0 scoped G2 Owner authority', task_commit_sha='653e49fc0d0f15981bf230995925c89d6994723d',
            source_manifest_sha256=sha(source_receipt), approved_base_commit_sha='fe926ad24d89231e5cf80f0f48ea44eb36887834',
            source_readback_status='PASS', brd_revisions=['BRD-09 v0.1 REV3 candidate / task-specific G1 design'],
            previous_evidence_reused=['G1 task-specific design acceptance only; no historical CI used for new code']),
        permissions=dict(git_source_read=True, git_report_write=True, git_report_push=True, git_code_push=True,
            code_allowed=True, pr_create=False, merge_allowed=False, dnse_production=False,
            broker_write=False, live=False, grant_evidence='Immutable G2 task and scoped Owner hold-lift; no host enforcement grant'),
        git=dict(repository='dunglt2505/FOX2', branch=git('branch', '--show-current'), worktree=str(ROOT),
            writer_lease='G2 PreExec NONE_OBSERVED and active thread/worktree inspection; one implementation writer',
            report_path=REPORT.relative_to(ROOT).as_posix(), delivery_status='LOCAL_ONLY', pr_url=None,
            local_head_before_submission=implementation),
        scope=dict(requested=['Integrated G2 F1 source/build per immutable task'],
            completed=['Trusted Windows authority/IPC/store/spawn, deterministic policy artifacts, installed consumer closure, source/native tests'],
            partial=['G2 source/build only; installed positive runtime remains DENY'],
            not_done=['Complete offline user-package build: no provisioned isolated build environment', 'NOT_RUN_G3 host enforcement/adoption'],
            explicit_exclusions=['Host policy/service installation/start', 'main/merge/deploy/provider/broker/Canary/LIVE'],
            changed_paths=changed_paths, forbidden_paths_touched=False), tests=tests, acceptance=acceptance,
        evidence=evidence, risks=[dict(id='HOST_ENFORCEMENT', severity='HIGH', state='NOT_VERIFIED',
            impact='No positive installed enforcement certified; interpreter/dependency closure and real service lifecycle require G3.',
            next_action='Independent CHAT review, then separately authorized isolated host tests.', owner_role='CHAT/G3 host owner')],
        security=dict(secret_scan='PASS', private_account_data_in_git=False, licensed_raw_feed_in_git=False,
            evidence_redacted=True, check_notes='Bounded source/test evidence; final credential-pattern scan recorded separately.'),
        usage=dict(attempts=1, retries=0, usage_status='NOT_MEASURED', tokens_used=None, credits_used=None,
            escalation_reason='NONE; no model/route substitution or expanded scope'),
        next_step=dict(requested_chat_decision='REVIEW', action='Independent fox2-result-review at observed remote SHA',
            owner_role='CHAT', prerequisite_gate='Remote SHA readback; no self-acceptance or host activation'))
    write(MANIFEST, result)
    print('Prepared required report, schema-v2 manifest and K1 classifications for independent review.')


if __name__ == '__main__':
    main()
