# FOX2 — Bridge Q0/Q1 Host Read-Only Evidence Assignment

**Assignment type:** NEW READ_ONLY HOST EVIDENCE TASK within the EXISTING Whole-WP `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. This is NOT a new engineering WP and NOT an executable Bridge Dispatch.
**Role / engine / thinking:** CODEX, pinned `gpt-6.1-sol`, `medium`.
**Actor:** CODEX CLI on FOXLE-PC, invoked by Owner via an explicit sandbox `read-only` host PowerShell. CHAT owns source resolution, admission decisions, remote readback and acceptance. No WORK independent audit.
**Scope / stage:** Q0 live process/lock/ledger/startup observation and Q1 safe reversible quiescence design, READ_ONLY recovery/TEST admission diagnostic. No code, worker, control or service mutation.

## Immutable inputs
- Repository `dunglt2505/FOX2`. Base of this CHAT-owned handoff branch and **unchanged host infrastructure worktree**: `work/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019@1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d`.
- Existing infrastructure `task.md` identity: `482d26d71c5c95f028f9b4110349e4d318bcb342:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/task.md`; SHA256 `ffd9b35b8e98d1dc7ae824945cba963d96c8cd0e1cf67e42220ab2cacafab188`.
- Original Owner grant: `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`; does NOT waive PreExec/controls/no-replay.
- Material BLOCKED actual PreExec: `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json` (`CHECK_BRIDGE_BOOTSTRAP_CONTROLS`).
- Governing read-only Q0/Q1 runbook: `23702bf815db5fbf838f07d1334ce19dcf1db0d2:docs/agent_handoff/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/CHAT_PREEXEC_BLOCKED_INTAKE_AND_WORKER_QUIESCENCE_CANDIDATE_20261019.md`.
- Owner/CHAT current evidence and 40+7 gates: `93b4305a4f900cec5cbd954ae7b18cc259ddf508:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261019_BRIDGE_P0_OWNER_PRIORITY.md`.
- Canonical Bridge audited code `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`; C3 `435154487e8e9bf6eab54a12f1f329e63787aa84` accepted only for frozen audit.
- Protected control Dispatch ref `work/FOX2-DISPATCH-chat@3f885b2d24cb131b5e96dfdb67a44677599197e2` and Canary worktree ref `work/FOX2-BRIDGE-FINAL-CANARY-009@501822a33ef08c7365154913bbc677544856eee5`.
- Human governance currently Policy 2.0.0/Dictionary 1.3/Routing 1.4/Protocol 12 on new work; original frozen 1.8.9/1.2/1.3 remains bound to old Dispatches. No machine adoption inferred.

## Tasks and acceptance
1. Recheck exact local infrastructure branch/HEAD and remote Git HEAD read-only, clean worktree, separate Worker vs Agent process provenance, PIDs/parents/executable and startup lineage; compare actual installed runtime/pointer and config identities. Avoid printing raw credential-bearing command lines or full private locations.
2. Read live current and any known legacy SQLite through `mode=ro`, `PRAGMA query_only=ON`: worker pause/stop, current execution, nonterminal CLAIMED/RUNNING/PUBLISHING/NEEDS_RECONCILIATION, duplicate IDs, exact COMPAT001/Canary/infra identities, manual markers. Do not confuse zero exact rows with absolute proof never started.
3. Determine actual owner of `bridge.lock`, singleton process and competing start sources; an existing lock file or temporarily free lock is not a continuously-held lease.
4. Q1 design only: identify SID-qualified startup, legacy Recovery disabled state, UI/tray and auto-restart launchers, pending unrelated auto-executable Dispatches, plausible safe reversible maintenance/quiescence plan with rollback and continuous lock-to-claim admission. Determine `SAFE_EXISTING_SUPPORTED_PATH` vs `HOLD_UNIMPLEMENTED_CONTROL_HANDOFF` and gaps, without performing changes.
5. Confirm source semantics: `request-exit` sets stop_requested, `resume` doesn't clear it; atomic claim rejects paused/stop. Do NOT try the unsafe control sequence.
6. Return `Q0_VERDICT`, `Q1_DESIGN_VERDICT`, `CONTINUOUS_WRITER_LEASE`, `EXACT_REPLAY_STATE`, `CURRENT_BOOTSTRAP_ADMISSION`, `SAFE_NEXT_ACTION`; label failed, unknown and not-run honestly. Max ~1500 words, sanitised with source/command categories and observation UTC timestamps.

## Permissions, STOP and result delivery
- `READ_ONLY`: no launch, dispatch claim, resume, stop, task scheduler change, lock acquisition, SQLite write, git fetch/push/reset, code edit, code probe, agent spawn or Canary. `ASSIGNMENT_CHECK=PASS_FOR_READ_ONLY_DIAGNOSTICS_ONLY`, NOT CODEX coding PASS or pre-Canary release grant.
- If process observation requires admin rights, capture ACCESS_DENIED and STOP affected determination; no privilege elevation, no fabricated PASS.
- Git Result Contract: `reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/report.md` + `evidence_manifest.json` and remote result SHA OUTSIDE committed artifacts, for CHAT `ACCEPT/REWORK/HOLD`. **Because selected CODEX route is sandbox read-only with NO Git writer authorization**, Owner's wrapper exports actual report+manifest bytes to a local TEMP folder; Owner transfers these actual files to CHAT, which can publish to a separately authorized non-main report destination only after safety and provenance checks. Do not claim Git delivery/acceptance from terminal prose.
- One diagnostic pass, not a new executable Agent Dispatch. `COMPAT001=HOLD`, `CANARY009=HOLD`, `INTERNAL_READY=NOT_ATTESTED`.
