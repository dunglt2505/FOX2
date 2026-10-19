# FOX2 — CODEX Q0/Q1 Host Read-Only Inspection

Role: CODEX — Windows Host Evidence Inspector
Engine/Model: CODEX CLI / gpt-6.1-sol (PINNED)
Thinking: Medium
Project: FOX2
SDLC Stage: Bridge RC1 TEST admission diagnosis
Mode: STRICT READ_ONLY, one inspection, NO code edits, NO Git writes, NO agent delegation
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Supporting existing infrastructure WP: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019

## Frozen sources and task
Repo: dunglt2505/FOX2
Existing Windows worktree: C:\Projects\FOX2-worktrees\FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019
Expected branch: work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019
Expected HEAD: 1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d
Original task: 482d26d71c5c95f028f9b4110349e4d318bcb342:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md
Task SHA-256: ffd9b35b8e98d1dc7ae824945cba963d96c8cd0e1cf67e42220ab2cacafab188
Owner scoped grant: c23d28bd56d9d06d64561dcf255b2d94227f6acc
Q0/Q1 runbook candidate: 23702bf815db5fbf838f07d1334ce19dcf1db0d2:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/CHAT_PREEXEC_BLOCKED_INTAKE_AND_WORKER_QUIESCENCE_CANDIDATE_20261019.md
Original material PreExec BLOCKED: 1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json
RC1 audit baseline: f3d6468fedb553ba6c6192ba5811cb1b26a11ab9
C3 accepted result: 435154487e8e9bf6eab54a12f1f329e63787aa84
Bridge roadmap/40+7 gates: 93b4305a4f900cec5cbd954ae7b18cc259ddf508:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261019_BRIDGE_P0_OWNER_PRIORITY.md
Protected control head: work/FOX2-DISPATCH-chat@3f885b2d24cb131b5e96dfdb67a44677599197e2
Protected Canary009 head: work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5

## Q0 — Verify live host reality (no mutation)
1. Read exact local branch/HEAD/worktree status and remote head with read-only commands. Report differences as STOP; NEVER fetch/checkout/reset/clean.
2. Using Get-CimInstance (if access allows), attribute Bridge Python worker(s) and parent launcher(s), WPF/tray, CODEX processes and relevant scheduled tasks; report sanitized PID, process name, user SID when safely accessible, executable basename plus installed-vs-other classification, parent PID, start UTC. Do not print raw command line, credentials, full private user path or secret environment variables.
3. Read installed Bridge current.json/config and database IDs read-only. SQLite connections must be URI mode=ro + PRAGMA query_only=ON. Identify current/legacy worker paused and stop_requested, current dispatch/execution and nonterminal claim states, current vs legacy ledger divergence, manual marker exact matches for infrastructure WP/COMPAT001/Canary009. Never infer NEVER_STARTED from zero rows.
4. Inspect bridge.lock metadata and existing OS lock owner only by safe read-only observation. Do NOT attempt to seize/clear/release any OS lock; a lock-file existence check alone is inconclusive. If lock ownership cannot be tested without acquisition, mark NOT_VERIFIED instead of probing.
5. Identify actual Windows Task Scheduler startup sources (canonical FOX2Bridge-<SID>, historical FOX2-Bridge-B-Recovery), trigger/action category, enabled/disabled, UI/tray auto-restart and possible competing supervisors. Sanitize arguments; preserve legacy Recovery as disabled. Do not change anything.

## Q1 — Design only, never operate
6. Reconcile whether two observed Python processes are launcher+child, competing controllers or UNKNOWN. Identify any unrelated auto_execute dispatch that could run on resume; if control graph cannot be proven, STOP.
7. From actual installed code, assess whether a supported, reversible Q1 maintenance gate can prevent new entrants while retaining pause/stop semantics and continuous exclusive writer through atomic durable claim. State the precise supported commands if known, but DO NOT RUN THEM.
8. Explicitly check known hazard: request-exit sets stop_requested=true; resume does not clear it; paused or stop_requested prevents claim; naive request-exit -> resume -> e2e-once is NOT SAFE. If no supported atomic handoff exists, return HOLD_UNIMPLEMENTED_CONTROL_HANDOFF and the minimum source-change boundary, no code implementation.
9. Distinguish operationally required canonical BRIDGE bootstrap from optional manual-local infrastructure. Do not add a manual-only implementation to the critical path absent necessity.

## Hard STOP
Never run a Bridge Worker, e2e-once, run-next, poll, request-exit, resume, pause/unpause, Start/Stop-Process, task scheduler mutation, agent-probe, installer/update/uninstall, test suite, sqlite update, lock acquisition, git fetch/push/rebase/reset/checkout, code edit, or protected Canary/COMPAT001 claim/replay. No privilege elevation or permission upgrade. Observe only, and no second Agent.
If access is denied or source/host cannot be attributed, report ACCESS_DENIED or UNKNOWN; NEVER invent PASS.

## Required output — exactly a sanitized Markdown report
Return:
- OBSERVED_UTC and EXACT_GIT/OWNER/SOURCE_BINDING;
- HOST_RUNTIME_IDENTITY, WORKER_PROCESS_LINEAGE, SINGLETON_LOCK_OBSERVATION;
- PAUSED/STOP_REQUESTED, CONTROL_STARTUP_SOURCES;
- DURABLE_LEDGER_EXACT_MATCHES_AND_NONTERMINAL (with named stores and gaps);
- AUTO_EXECUTE_UNRELATED_RISK and WORKTREE_WRITER_EXCLUSIVITY;
- Q0_VERDICT = PASS_OBSERVED / HOLD_WORKER_IDENTITY_UNKNOWN / PARTIAL;
- Q1_DESIGN_VERDICT = SAFE_SUPPORTED_DESIGN_ONLY / HOLD_UNIMPLEMENTED_CONTROL_HANDOFF / UNKNOWN;
- R0-R7/ASSIGNMENT: READ_ONLY_EVIDENCE_ONLY, NO_EXECUTION_AUTHORITY;
- NEGATIVE_EVIDENCE_LIMITS; MINIMUM_SAFE_NEXT_ACTION and actors.

Use bounded paragraphs/table, <=1500 words. Include specific evidence command categories and timing. Never claim Continuous Lease PASS from a snapshot, no-start proof, fresh PreExec PASS, Agent execution, READY or release. Return the full final report for host export; do not push or write to repo. CHAT will verify and publish report.md plus evidence_manifest.json from ACTUAL exported bytes when received, then independently ACCEPT/REWORK/HOLD.
