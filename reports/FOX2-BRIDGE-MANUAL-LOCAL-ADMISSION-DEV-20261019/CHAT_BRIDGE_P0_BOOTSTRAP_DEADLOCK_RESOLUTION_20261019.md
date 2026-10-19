# FOX2 Bridge P0 — Resolving Bootstrap Deadlock (CHAT, 2026-10-19)

**Whole-WP:** FOX2-BRIDGE-RC1-TO-INTERNAL-READY; existing bounded infrastructure dependency `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019`.  
**Stage:** CHAT source/route reconciliation only — **not** a PreExec receipt, executable prompt, new Agent Dispatch, engineering code change, approved override, or Canary certification.  
**Result:** `ROOT_CAUSE_IDENTIFIED / MINIMUM_NATIVE_DEV_ALTERNATIVE_DESIGNED / ROUTE_REBIND_AND_HOST_PREEXEC_NOT_VERIFIED`.

## Immutable references independently read

1. Governance `main@e26fc7aa87e787852407261db90506b3516ba5de`, Policy v2.0.0 (blob `2d373f374f906bf7959062050bbeae5350b0c482`), §§1, 3, 8, 9. Policy explicitly separates native CLI DEV prerequisites from installed Bridge bootstrap; Owner decisions do not convert technical FAIL to PASS.
2. Original Bridge implementation baseline `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`, especially `agent_bridge/src/fox2_agent_bridge/dispatch_normalizer.py`, `preexec/engine.py`, `preexec/profiles.py`, `app.py`, `__main__.py`.
3. Bounded infrastructure Owner grant `c23d28bd56d9d06d64561dcf255b2d94227f6acc:docs/governance/releases/FOX2_MANUAL_LOCAL_ADMISSION_OWNER_EXECUTION_AUTHORIZATION_20261019.json`: six named primary code/test paths, exact task binding. Owner permission for that **scope** exists; no repeat grant for the same six paths. The recorded **execution route** is still conditional `BRIDGE_E2E_ONCE_ONLY_AFTER_ACTUAL_HOST_ADMISSION`; it does **not** independently authorize a new NATIVE CLI handoff.
4. Immutable Manual Local PreExec `1ce109b9a4c538b255c6d8ffc6be8b4dccecf65d:reports/FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION-DEV-20261019/preexec/preflight_receipt.json`: `BLOCKED`, sole material blocker `CHECK_BRIDGE_BOOTSTRAP_CONTROLS`; CODEX marker-only PASS; Copilot current eligibility for **this** work UNKNOWN. New infrastructure Agent/Dispatch not started/published by that receipt.
5. Existing companion `work/FOX2-MANUAL-ADMISSION-QUIESCENCE-chat-20261019@1aaec11927320016e8e8ee5da273471724c10c72`: Q0–Q6 worker identity/ledger/lock runbook, including historic host-reported two workers, `paused=true`, stop flag transitions, prevention of unrelated auto-execution and valid alternative STOP semantics.
6. PreExec compatibility WP `work/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018@fd3141f8e825931f9ee17d68c740e3b36230aa96`: task-specific PreExec `PASS`, CODEX marker PASS / COPILOT `AUTH_REQUIRED` historical. Its immutable `FOX2-DISPATCH-PREEXEC-COMPAT-CODEX-001` uses `MANUAL_LOCAL`, is PUBLISHED/HOLD and **cannot serve as a bootstrap or be replayed**.
7. Pre-Canary audit `541bf35e3bdb95b701bd1cdc22b0bdbe87333110:reports/BRIDGE-RC1-PRECANARY-AUDIT-20261018/final_admission_determination.md`: substantive prior 38 technical gates PASS; independent reviewer provenance/admission not certified (`BLOCKED`). Canary009 HEAD `501822a33ef08c7365154913bbc677544856eee5` unchanged at last remote read.

## Actual deadlock and what NOT to do

- `MANUAL_LOCAL` is a Dictionary/Dispatch identity but the inspected Bridge normalizer rejects non-`BRIDGE` for auto-execution. The protected compatibility Dispatch needs a manual entrypoint **which is not yet implemented**.
- The candidate infrastructure implementation itself was routed to installed `BRIDGE e2e-once`. That route must respect worker PAUSED / stop_requested, OS singleton ownership and atomic ledger claim. Its **BLOCKED** PreExec is correctly fail-closed for that route, **not** an Agent coding failure.
- Two historic worker processes, a shared lock and sticky `stop_requested` following `request-exit` make `resume`, direct SQLite update, arbitrary kill, forged status or retry dangerous. Never reinterpret the old BLOCKED receipt as PASS.
- Consequently *using the broken Bridge to implement a fix for Bridge* is a circular bootstrap dependency. A new independent DEV route is the smallest plausible way around it; the current task's already-published Dispatch and identity cannot be relabeled in place.

## Minimal route separation — proposed, NOT issued

### Lane DEV: code implementation without Bridge worker

1. Retain **same existing infrastructure WP and six approved primary code/test paths**, original Owner code approval and all immutable source history. CHAT records a **new explicitly authorized execution-path amendment** selecting an actual native CODEX (or independently eligible COPILOT) CLI DEV session, rather than claiming the old `BRIDGE` admission passed. Until that scoped route amendment is authorized and read back, `CODE_ALLOWED_FOR_NATIVE_EXECUTION=HOLD_ROUTE_CHANGE`.
2. Perform a **fresh task-specific shared PreExec v1** for this genuinely independent native route: Git task/source SHA, chosen CLI authenticated access/capacity/model, worktree and OS-backed exclusive writer, permissions, no prior attempt/claim, safe runtime single-use attempt ledger, exact report destination and expected-head publication. These **DEV** checks are material; installed worker PAUSED, Bridge daemon singleton and `e2e-once` bootstrap are **not** material if the new route actually never uses Bridge.
3. CHAT reviews R0–R7, picks least-cost eligible route; preferred *conditional* CODEX `gpt-6.1-sol/medium/FULL_ACCESS` based on latest bounded marker, COPILOT only if fresh auth/capability. WORK is not code executor. No Agent assignment before actual route-specific PASS or separately explicit scoped Owner override with recorded residual risk; neither exists in this file.
4. Publish **new, distinct** immutable Git-first prompt/task/source-set and native attempt claim in permitted path/branch **after admission**; run exactly once under the proven exclusive writer. Agent produces six-path bounded diff, synthetic race/crash/claim/no-replay tests, full needed regression, `report.md`/`evidence_manifest.json` on non-main Git; CHAT verifies ACCEPT/REWORK/HOLD. No original Dispatch001 or Canary009 claim/replay; no silent backend/protocol/schema mutation.
5. This closes *code implementation only*. An agent's Git push or hosted tests cannot mean installed Bridge supports Manual Local.

### Lane operational: installed Bridge and Canary (later)

- After native DEV acceptance, under separate authorized host maintenance window collect existing Q0/Q1 read-only process/ledger/startup/lock evidence; if needed, implement **source-bound safe worker quiescence and atomic one-shot handoff** with rollback without mutating unrelated workers/ledgers or exposing eligible auto-dispatches.
- Install/adopt the accepted Manual Local mechanism only with true host runtime compatibility, singleton and no-replay checks; then consider the protected immutable Dispatch001 **once only** after fresh status/claim validation and its own effective gates.
- Pre-Canary independent audit B1 is a **later OPERATIONAL_RELEASE gate**, not a precondition for coding. Either establish a truly independent reviewer with verifiable provenance and substantive assessment, or obtain a *specific explicit Owner risk decision* changing the internal audit requirement. Do not self-certify independence, invent WORK admission or repeat unchanged 399/30 tests.
- Canary009 stays HOLD until relevant gates genuinely pass and authorized exactly-once launch is separately permitted.

## Policy/Route check: read-only reconciliation, not Agent assignment

- **R0:** Existing technical closure 399 Python / 30 Desktop historical PASS reused. PreExec compatibility task PASS reused only within its own identity. Original Manual Local BLOCKED remains.
- **R1:** Engineering route design / READ_ONLY, not coding or operational launch.
- **R2:** Owner infrastructure code scope proved; existing allowed BRIDGE route technically BLOCKED. **Native execution-path amendment authority UNKNOWN/NOT_VERIFIED** and shall not be invented.
- **R3:** Git connector access PASS; fresh host native model/quota/worktree/attempt control UNKNOWN; earlier CODEX marker PASS is not current admission.
- **R4:** CHAT directly resolves docs/source; CODEX candidate for complicated guarded code, COPILOT candidate on fresh usable auth, WORK reserved for actual independent pre-Canary audit. No executable assignee today.
- **R5:** This CHAT report branch is separate from all Windows Agent code worktrees. No code or runtime writer collision created. Windows local worktree/writer UNKNOWN for future execution.
- **R6:** Git-first path, source/attempt/readback and result acceptance remain mandatory before any Agent coding handoff. Prior consumed/published identities immutable.
- **R7:** **Next materially unblockable action is selecting and admitting a native DEV route** for the *existing* Manual Local task; then actual code/test; then installed admission; independent pre-Canary audit; gated Canary009. Stop on new route unapproved, host UNKNOWN, source drift, competing writer, no durable claim, worker-lock conflict or out-of-scope code.

`BRIDGE_PRIORITY=P0 / ROOT_CAUSE=CIRCULAR_BRIDGE_BOOTSTRAP / CURRENT_BRIDGE_PREEXEC=BLOCKED_PRESERVED / OWNER_CODE_SCOPE=APPROVED_BOUNDED / CODEX_MARKER=HISTORICAL_PASS / NEW_NATIVE_ROUTE_AUTHORITY=NOT_YET_ESTABLISHED / NATIVE_PREEXEC=NOT_RUN / EXECUTABLE_ASSIGNMENT=HOLD / PRECANARY_AUDIT=BLOCKED / CANARY009=HOLD / PRODUCT_LIVE=NO`
