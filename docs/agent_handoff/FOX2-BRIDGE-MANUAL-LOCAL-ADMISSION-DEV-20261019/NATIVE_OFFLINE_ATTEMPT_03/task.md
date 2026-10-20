# FOX2 — Native Offline Manual Local Admission, Attempt 03: Cross-root Durable No-Replay

**Status:** TASK_CANDIDATE_NON_EXECUTABLE; **not yet dispatched, no CODEX coding invocation authorized.** Date: 2026-10-20.
**Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY; existing infrastructure WP FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019; this is a NEW attempt within SAME WP, not a micro-WP.
**Attempt ID:** FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-OFFLINE-ATTEMPT-03.
**Host route only after fresh task-specific PreExec and CHAT Git admission:** CODEX / OpenAI CLI / PINNED gpt-6.1-sol / medium / FULL_ACCESS bounded to exact paths / agent owns Git result / max one coding invocation.

## Source / governance

- Frozen test-only CODE branch: work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03 @ 5a82d08694f217415890f24802261aed625aa111. This is a direct child of 65c50f7831722300a5418d0e9bc21f9f95988147; only changed path is agent_bridge/tests/test_e2e_runner.py, exact blob 7b2a2c48e6bf4225d849dc7a7a32126652b0c3be (+90 lines). It carries the six known failing fixture assertions from CODEX Attempt02 with no old report or production implementation. Current state is TEST_NEGATIVE_RED, not accepted behavior or PASS.
- Fresh Windows target worktree: C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019-NATIVE-ATTEMPT-03. Do not reuse or modify earlier Attempt01/02 worktrees or durable attempt markers.
- CHAT accepted blocked evidence only from previous result dd3e46616c1f5dd2643eead3901ceaa1693cc6d6 and independent review 3b4ebbed504911836f327b53e9f8da20a5dd0be6. Historical attempts 01/02 CONSUMED and immutable, cannot replay, restart or modify their markers/receipts/report contracts.
- Binding technical design candidate: bd5cd44e31ceb7384b558c8fb08ccefd98dfb9e6:docs/roadmap/FOX2_BRIDGE_CROSS_ROOT_NO_REPLAY_DESIGN_CONTRACT_CANDIDATE_20261020.md (blob 6e6d56df130b7153539a2bf1dba9f86d2fe591e4). Design is candidate, no release/adoption permission.
- Existing Owner scope grant: c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json (conditional shared dependencies only after CHAT exact K1); scoped human operating governance Registry d34da1e3b4918a902646621b487ca8ad3e05b0e0 (Policy v2.0.0 Owner-approved principle; not installed runtime enforcement), Dictionary v1.3 b25f7f728de67cf8595bf24f22fcbd79ef50babc, Routing v1.4.0 bcd008983b61349646a5198ff243069f81484fae, Git-first Protocol v12 f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa, Result Schema v2 docs/agent_handoff/FOX2_AGENT_RESULT_SCHEMA_v2.json.
- Old frozen Bridge RC1 f3d6468fedb553ba6c6192ba5811cb1b26a11ab9; Canary009 HOLD, COMPAT001 PUBLISHED_HOLD, old Bridge bootstrap PreExec BLOCKED. No current installed/Canary source adoption claim.

## Exact code/test change allowlist (10 paths total)

Original Owner six:
1. agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py
2. agent_bridge/src/fox2_agent_bridge/e2e_runner.py
3. agent_bridge/src/fox2_agent_bridge/app.py
4. agent_bridge/src/fox2_agent_bridge/__main__.py
5. agent_bridge/tests/test_project_dictionary.py
6. agent_bridge/tests/test_e2e_runner.py

Four CHAT-confirmed K1 conditional dependencies under the existing Owner grant:
7. agent_bridge/src/fox2_agent_bridge/desktop.py
8. agent_bridge/tests/test_desktop.py
9. agent_bridge/src/fox2_agent_bridge/ledger.py
10. agent_bridge/tests/test_runtime_ledger.py

Only four result files may be added:
- reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md
- reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/evidence_manifest.json
- reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/test_summary.json
- reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/diff_trace.json

No modifications to process_lock.py, ops_runner.py, config.py, startup/install scripts, dictionary/schema/registry/PreExec, other tests or shared library code. If actual design requires another path, STOP with exact consumer/K1 evidence before any such edit; no implied wildcard. Other tests may be executed read-only on isolated fixtures. Preserve all existing receipts and the six failing test identities/meaning; no XFAIL/skip/delete/weaken to get green tests.

## Engineering objective, mandatory safety

Implement the candidate shared fail-closed cross-root identity guard using the SAME normal validation and atomic claim/checkpoint/adapter path; expose an explicitly selected MANUAL_LOCAL route only after known-safe identity gate. No clone stack or private one-off marker bypass.

Cross-root invariants: consumed/unknown identity in either ledger or legacy/current manual marker is DENY; recent legacy writer claims after snapshot are DENY; legacy writer restart after current exits cannot replay a current claim. Both-root evidence must be validated under correct locks; if operational legacy retirement/fencing cannot be proven, new admission MUST be denied, not a guessed READY state. Any allowed claim must have a durable single authority, with all claim callsites sharing its gate; same DB BEGIN IMMEDIATE alone is not sufficient. PAUSED/stop_requested/honor_controls and auto BRIDGE rejection of MANUAL_LOCAL stay unchanged. Fail closed on malformed marker, unknown root, wrong source/model/Owner/identity, migration crash or ambiguous delivery. No installed bridge lock/ledger edits, Worker resume, protected Dispatch execution or live provider.

**Design choice:** Prefer conservative durable fence in shared ledger plus strict legacy reconciliation and separately evidenced legacy retirement. Agent must prove no replay for both live cooperating processes and after process exit/restart; a transient dual-root file lock is insufficient on its own. If exact ten file code/test scope cannot implement it safely, STOP with honest BLOCKED report and evidence, not partial unsafe code. Full MANUAL_LOCAL feature acceptance is conditional on sound cross-root identity contract, not only six green tests.

## Tests and delivery acceptance

Run synthetic fixture-only six historical negative tests, current/legacy marker corrupted and missing, split DB 3 consumed states, late legacy claim, startup/stop/PAUSED, claim concurrency across both roots, crash windows and post-stop legacy resurrection. Positive manual route only if test fixture explicitly satisfies durable fencing; normal auto BRIDGE refuses manual. Run fresh focused test_e2e_runner, test_project_dictionary, test_desktop, test_runtime_ledger, test_ops_runner and test_preexec existing regressions where available. No Agent integration or host installed Worker, protected COMPAT001/Canary009 tests. Real PASS/FAIL/NOT_RUN only, no historical counts as current PASS.

For every material code hunk, K1 classification REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED with exact path, consumer and test. Validate test failure root causes, changed-path allowlist, diff --check, secret scan, schema Result v2 and actual Git remote publish. Agent commits/pushes only to CODE branch and supplies observed remote SHA outside committed report/manifest. Mandatory real reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md and evidence_manifest.json plus test_summary and diff_trace, even when blocked. CHAT independent acceptance required; no Agent self-ACCEPT.

## Binding and STOP before any Agent launch

This document is a PREEXEC TASK CANDIDATE, NOT execution clearance. CHAT must obtain new worktree clean/remote-bound SHA, current one-writer/marker evidence, **fresh Attempt03 route-specific PreExec** on this precise worktree with independently remote-readback receipt, then publish immutable CODEX prompt (same source-bound task), and a **separate** CHAT final admission binding task/prompt/PreExec and R0–R7. No prompt, host CODEX coding or Attempt03 durable coding marker is yet issued. PreExec bounded marker may be used after prechecks and documented as a small AI request, not coding Agent.

At every stage preserve attempt01/attempt02 markers, report Git histories, original PreExec BLOCKED cases and paused Canary. Never reset --hard, clean old worktree, force push, merge/main, install, trigger Worker, provider/broker/LIVE, replay or bypass STOP.

**NEXT_SAFE_ACTION:** CHAT remote-readback this task+source then FOXLE-PC create new isolated worktree and perform fresh native task PreExec once; after receipt PASS CHAT publish prompt/admission and only then CODEX can execute one coding attempt.
