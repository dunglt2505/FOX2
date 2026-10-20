# FOX2 Bridge — Whole-WP integrated recovery assessment and execution decision candidate

**Date:** 2026-10-20. **Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` (existing; do not create micro-WPs). **Features:** `FOX2-BRIDGE-RC1` TEST/BLOCKED and `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` BUILD/BLOCKED. **Document state:** `CHAT_INDEPENDENT_SYSTEM_ASSESSMENT / ENGINEERING_RECOVERY_CANDIDATE / NOT_EXECUTABLE / NOT_RELEASE_APPROVED`. No agent dispatch, code install, lifecycle mutation, main/merge, Canary or LIVE authority conveyed.

## 1. Decision first

**KEEP** the Bridge Core, Git-first mailbox/immutable Dispatch model, Codex/Copilot adapters, per-user versioned installer and WPF Desktop. **DO NOT REWRITE** the complete product, **DO NOT use the old RC1 archive as a safety upgrade**, and **DO NOT make every FOX2 coding task wait for installed Bridge readiness**. Bridge is an orchestrator transport/executor; CHAT remains source/routing/acceptance authority; permitted Git-first direct CODING routes can run independently if task-specific PreExec/Owner grants allow.

**Target recovery architecture:** ONE admitted current-root Worker/claim authority; the old-root executor is durably retired from all material restart paths, while old SQLite/consumed identity/unknown records survive read-only reconciliation; new claims remain DENIED until independently evidenced authority transition. Build **ONE new versioned safety+F1-capable candidate package**, initially deployed fail-closed, then activate positive claims only after separate retirement/one-writer/rollback evidence and host authorization. The two-state deployment is one artifact, not an excuse to perform F0 reinstall then F1 reinstall as two unrelated WPs. Route B (both unmodified legacy and current executables sharing an atomic authority) is not supported by evidence; no positive unlock via `SINGLE_ROOT` DB edit or a text flag.

**Single recovery objective:** `INTERNAL_FOX2_BRIDGE_READY` after a real end-to-end claim/no-replay/usage/result/CHAT acceptance chain, with separate Canary authorization. Preserve all historical `FAIL/BLOCKED/NOT_RUN` and old one-shot Dispatches; no replay.

## 2. Source and evidence snapshot

Authoritative **human-operating governance** anchor: Owner Registry `docs/governance/FOX2_PROJECTWIDE_GOVERNANCE_REGISTRY.json` blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35` on release branch `work/FOX2-POLICY-V200-OWNER-OVERRIDE-RELEASE-20261019` commit `d34da1e3b4918a902646621b487ca8ad3e05b0e0`; Policy v2.0.0 and Dictionary v1.3 apply to new/scoped CHAT coordination, **installed/machine enforcement NOT_ATTESTED**. TechSpec v0.7 REV10 source `agent_bridge/.../FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md` is explicitly CANDIDATE/NO_DEV_GRANT, not automatically EFFECTIVE. Earlier released baseline and immutable existing task sources must be resolved by authority, not highest filename or `main`.

- **F0 offline:** reviewed snapshot `611ec26c28484de740e963d86de6b00946f1492d` accepted via CHAT direct scoped alternative delivery; `desktop.py` `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2`, `ledger.py` `e97ad916b3d78f085a106bad74bc0ddd2aec82f4`. It forces `DENY_CROSS_ROOT_UNKNOWN` for every configured runtime root, and direct installed-root `SQLiteLedger.claim_dispatch` rejects before database transaction. **F1 positive code NOT_IMPLEMENTED.** CODEX Attempt06 consumed, `AGENT_RESULT_V2_NOT_DELIVERED`; no replay.
- **Real Owner-reported Windows instance (2026-10-20):** `current.json` and receipt stable; `252/252` payload hashes match package manifest. Installed exact `ledger.py` blob `11e779f52b2518a9ac776cdc33192622c37e61df`, `desktop.py` blob `32005141e11ac126ef8944334f3e8f95139c0b8c` equal pre-F0 source at `a3ad10d490993fb4ed4ccfd7d1a73f74cc465581`, **not** F0. Installed `installation.py` and `launcher.py` match unchanged F0 code. These are on-disk module observations, not loaded Worker/process attestation. One-writer/PAUSED/active claims UNKNOWN. Legacy DB exists; startup retirement NOT_VERIFIED.
- **Archived RC1:** `reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_recovery_003/FOX2-Bridge-RC1.zip` exists in Git (64,479,644 bytes; blob `15450a648b70db79a94bf4a24fa69c879d0c4a49`). Historic metadata `FOX2-Bridge-RC1.json` declares package SHA256 `a0516aed...` and source inventory SHA256 `9990e91c...`, matching Owner's installed pointer. Archive content digest independently rehashed **NOT_RUN**; the historic build source freeze `c916de...` is not a demonstrated exact whole-package source set (e.g. installer differs and launcher missing at that SHA). Historic `installed_certification.json` is `PARTIAL_NOT_CERTIFIED`; `stop_receipt.json` states `STOPPED_NEEDS_RECONCILIATION`. History of 399 Python and 30 Desktop contract tests PASS does not certify installed UI, Canary, this new F0 source or today's Worker.
- **Host surfaces:** two FOX2 Scheduler candidates, one current READY, one OTHER DISABLED; 211 tasks/213 actions inspected without errors, 118 non-Exec actions opaque; three matching current-referenced processes with incomplete parent provenance. Neither a point-in-time absence of a legacy process nor root-local `bridge.lock` proves durable legacy non-restart. Legacy database `294,912` bytes reported present, actual consumed/marker content not independently reconciled.
- **RC1:** owner state `FOX2-BRIDGE-RC1` TEST/BLOCKED; `BRIDGE_BOOTSTRAP_CONTROLS_BLOCKED`, exact adoption and remaining final release gates HOLD.

## 3. Systemic defects/root-cause analysis (not separate micro-tasks)

| Class | Evidence-based diagnosis | Product impact | Corrective principle |
|---|---|---|---|
| P0 — Identity authority / split brain | Two SQLite roots, temporary old lock / snapshot migration, no old-binary shared atomic protocol, old executor restart unknown | Potential duplicate dispatch claim after supervisor exit / late legacy claim | One durable authority before positive claim; retire old runnable capability or prove compatible shared atomic protocol; deny UNKNOWN |
| P0 — Source/runtime mismatch | Installed ledger+desktop = PRE_F0; reviewed F0 deny logic not installed | Cannot claim installed no-replay fix or attribute Worker behavior to accepted source | Single authenticated new versioned artifact with exact wheel/module/source file binding; no in-place mixed-file patch |
| P0 — Lifecycle / writer admission | Worker spawned before UI; UI may exist while Worker state unknown; current-root lock only | UI task Ready or visible is not lease proof; upgrades/Canary may race active writer | Quiescence, exclusive worker, in-flight agent/claim negative proofs, restart-proof legacy retirement and rollback |
| P1 — Artifact/source provenance | RC1 zip and manifest internally consistent, but declared build source freeze not an independently verified whole immutable source set | Cannot use self-reported archive hash/manifest to declare installed effective | Hash real artifact bytes, independently map archive/member inventory/build inputs to immutable approved source |
| P1 — Release acceptance | Historical green unit tests and partially passing installed harness coexist with fresh UI Artifact Vault failure and pending independent gate | False closure if code PASS substitutes installed/E2E/canary PASS | ONE gate matrix keyed by exact candidate artifact and test session, fresh observations, independent CHAT result intake |
| P1 — Workflow fragmentation | Repeated point checks, attempts, report receipts and host PowerShell snapshots answer local questions without closing shared product gates | High Owner effort, many commits, repeated proof without effect | One Whole-WP, one aggregated test/adoption receipt, event-driven evidence only when necessary |
| P2 — Governance/transport coupling | Document source/version locks, PreExec and Agent Result v2 status sometimes conflated with Bridge availability | Offline coding delayed although it can be safely Git-first routed | Separate DEV path from installed Bridge release; never bypass policy, no-replay or Agent model HOLD |

**Not proven:** live duplicate claim happened, installed Worker has resumed or is paused, old writer can actually restart now, any signature tampering/malware, full RC1 zip hash was independently verified, or successful Canary. Do not assert these.

## 4. Integrated implementation and release plan — ONE Whole-WP, gate driven

### Phase I — Source/contract consolidation, CHAT DIRECT, offline

- Lock exactly one task-evidence matrix for current Whole-WP: normative BRD / released TechSpec and candidate deltas with approval status, immutable F0 SHA, F1 source contract, versioned installer/runtime surfaces, release acceptance and Owner grants. Preserve completed F0; do not replay attempts or rename old outcomes.
- Choose **Route A** (durable old-executor retirement) for engineering design; define scope of old executable/alias, exact ordinary-user execution paths, OS enforcement capability and backout. Explicitly state trust limit of user/admin who can reverse local controls.
- Specify *one* F1 authority interface/state machine in code: `UNKNOWN -> RETIREMENT_EVIDENCED -> STAGED -> ADMISSIBLE` (proposed), versioned epoch and immutable trusted source/package/host retirement proof; denies for malformed/missing/rollback conditions; same ledger claim-time check for direct, App, Desktop Worker, E2E, Ops; `paused/stop_requested` and immutable model/source/permission gates remain separate. A writable SQLite flag or JSON receipt alone can never grant positive authority. Plan no-replay reconciliation from both DBs and manual markers with crash windows.
- Complete minimal K1 consumer mapping for `ledger.py`, `desktop.py`, `app.py`, `e2e_runner.py`, `ops_runner.py`, `installation.py`, versioned launcher & tests. The last two modules must not be edited absent actual material need.
- **Exit I:** precise future code allowlist/test matrix/source locks and verified available host retirement mechanism. Do not fabricate a signed Host PreExec. `GO_DESIGN` alone never means `PASS_TO_ASSIGN`.

### Phase II — One integrated candidate BUILD/TEST (offline)

- Produce **one** new F1-capable package from a clean, pinned Git source set; preserve accepted F0 fail-closed semantics at install default. No F0-only install detour and no manually overwriting two installed `.py` files.
- Implement trusted authority transition / epoch, claim-time fence and crash/restart guarantee, exact fail-closed rollback and credential/provenance checks. No standalone alternate Manual Local engine.
- Negative tests MUST cover historic six dual-root failures, valid/corrupt legacy marker, late claim after snapshot, old writer exit/restart, two-root writer lock race, direct ledger, paused/stop, alternate config root, claim-before-Agent-spawn, Agent failure/push ambiguity, process crash, duplicate consumed IDs. Positive synthetic test only under explicit simulated enforced old-retirement authority; may not test against real live ledger.
- Full existing core/desktop regression, built-package deterministic archive + package/member hashes + source file inventory + Git revision link; reproducible source-specific test evidence. New compile/test before installed admission. No weakening/skipping regression to turn green.
- **Exit II:** code/tests real PASS + CHAT independent diff/source/Agent result intake + immutable candidate SHA. User instruction currently pins `CODEX gpt-6.1-sol/medium: HOLD CODING`. No new agent assignment or inference of model/quota/host permission now; CHAT direct source/contract work may continue. When un-HOLD occurs, use Prompt Builder, new Git task/prompt/PreExec and one-writer, no Attempt06 replay.

### Phase III — ONE governed host transaction, initially fail-closed

- Before any system mutation, Owner-approved host PreExec must prove exact source-built archive identity, processes and active Agent children, worker quiescence/PAUSED/STOP, no in-flight claim/publication or unknown side effect, both-root consumed/manual evidence and backups, declared rollback, and ability to make old writer **durably non-launchable** across logoff/reboot and manual re-entry under the specified trust model.
- If legacy retirement cannot be enforced/restart-tested without touching production records, **STOP** at fail-closed; no positive claim. Avoid blind real legacy restart as a negative test.
- ONE controlled versioned installation of verified F1-capable archive (hash/manifest/isolated runtime pointer), while Worker remains fail-closed. Attest new installed `ledger.py` and `desktop.py` match released candidate bytes, plus wheel/runtime/module digest, process startup identity and current pointer. Never switch to unsafe old binary as rollback; rollback to DENY+PAUSED with preserved consumed ledger if possible.
- Only after source provenance, quiescent-one-writer, durable old retirement, reconciled identities and epoch evidence all PASS may an **independently authorized** transaction set ADMISSIBLE; fail closed if evidence lost.
- **Exit III:** installed exact candidate verified, legacy restart denied with durable boundary, controls/lease verified, source-bound positive admission passed — **not** permission to run Canary.

### Phase IV — RC1/Canary and operational readiness

- Use one immutable candidate artifact and fresh test instance for UI Artifact Vault local save (not stale file), installer/uninstall/reinstall preservation, Worker/UI restart and single-instance, source+model+permission runtime compatibility, real usage/result Git Result v2 and CHAT independent acceptance.
- Canary009 / COMPAT001 activation at most once only after its own original identity/status/readiness verified and route-specific Owner/PreExec authorization. No rebind/replay of already consumed attempts. Verify result commit/hash, no-replay after restart, fail-closed recovery, and release gates individually.
- Independent reviewer only where normative RC1 audit contract requires, not for repeated administrative admission reviews; CHAT decides `ACCEPT / REWORK / HOLD` after genuine evidence.
- **Exit IV:** actual final approved release gates PASS under exact installed source and permitted action scope; then and only then `INTERNAL_FOX2_BRIDGE_READY`. This is NOT live trading/broker/provider permission.

## 5. Owner effort, cost and dependency policy

- **Owner:** no more broad 211-task/252-file host scans or speculative PowerShell ping-pong. ONE offline safe evidence collector + ONE explicit later executable adoption transaction, each with hard STOPs and redacted evidence, **only if actually needed**. Any request for Owner manual Windows action shall include complete PowerShell **7+** inline and must be source/task/version bound, copy-ready, no placeholder and no unauthorized mutation.
- **CHAT:** owns source resolution, K1, bridge test-gate matrix, release engineering decision, Git publication/readback, Agent acceptance and feature status. Use current non-main branch for scoped documentary changes, no main/merge.
- **COPILOT:** preferred routine coding only when exact source-bound specs and allowed code route/verified quota+permissions exist; **CODEX:** hard cross-root concurrency/SQLite safety and integration only when Owner lifts the existing pinned `gpt-6.1-sol/medium` coding HOLD and route-specific PreExec PASS; **WORK:** a genuinely required independent final audit or unique host/browser capability, not default review. No simultaneous code writer on the same allowed files.
- **Contingency:** Authorized Git-first CODEX/Copilot execution and CHAT review may advance unrelated FOX2 features without Bridge, provided their own source/permissions/quota/PreExec are verified. Bridge cannot self-grant this; existing Owner coding HOLD still applies to its exact bound route.
- Do **not** buy more agents or spawn more Dispatch attempts just to learn another exit code. Consolidate new source changes into one coherent coding assignment when admitted, with a single result contract and acceptance.

## 6. Ready/blocked decision and next real action

| Decision | Verdict |
|---|---|
| Abandon Bridge/rebuild entire product | `NO_GO` — existing tested core, installer and UI provide reusable value |
| Reinstall archived RC1 now | `NO_GO` — installed already carries pre-F0 critical bytes, historic certification partial |
| Install raw F0 source now | `NO_GO` — no authenticated build/install release+quiescence, does not solve positive F1 |
| Clear SQLite `SINGLE_ROOT` / manually erase consumed IDs / dual-DB copy | `PROHIBITED` — cannot prove atomic no-replay, not F1 authority |
| Bridge coding new attempt now | `HOLD` — Owner pinned CODEX coding HOLD; new Agent task needs full Prompt Builder, source and PreExec |
| CHAT-direct integrated recovery contract/acceptance | `GO_SCOPED` — fulfills Owner assessment request under candidate documentary authority |
| Canary/internal-ready now | `NO_GO` — F1, installed source and final gates unsatisfied |

**ONE NEXT_SAFE_ACTION:** finish source-bound Whole-WP **recovery implementation contract** (exact non-overlapping code/test changes, source-to-package attestation chain, atomic no-replay invariants and one host transaction acceptance), then admit ONE new engineering action only when Owner's pinned coding HOLD and relevant PreExec permit. **REAL_BLOCKERS:** no current F1 positive code; no proven durable legacy retirement/one writer; no trusted new F1-capable package on host; pinned CODEX HOLD. **GOAL_MET for assessment:** YES. **GOAL_MET for Bridge product:** NO.

## 7. Governance & Skills readback

`POLICY_CHECK -> TASK_STATE_CHECK -> SOURCE_RESOLUTION -> ROUTING_R0_R7 -> ASSIGNMENT_CHECK` done **for CHAT document/read-only assessment route**. `R0` existing Whole-WP; `R1` multi-feature BUILD/TEST gap; `R2` Scoped Owner instruction to assess/recover, not installed release; `R3` safe Git/report only, no executable PreExec claim; `R4` CHAT direct; `R5` single Git non-main report writer; `R6` remote readback required; `R7` no-replay, retain historical evidence. `ASSIGNMENT_CHECK=NOT_APPLICABLE` (no new Agent).

**Skills actually read:** `fox2-project-health`, `fox2-strategic-agent-triage`, `fox2-source-resolver`, `fox2-techspec-validator`, `fox2-execution-recovery`, `fox2-feature-certification`, `fox2-status-roadmap`, `fox2-governance-preflight`, `fox2-agent-route-runtime`, `fox2-result-review` — REQUIRED/APPLIED as relevant. `fox2-agent-prompt-builder` NOT_APPLICABLE while coding hold/no assignment; `fox2-thread-handoff` NOT_APPLICABLE (no new context transfer); `fox2-document-publication` should be APPLIED to non-main candidate publication before further formal publication; unavailable? NOT_APPLICABLE to released-document flow. No Skills method grants runtime rights.

**STOP:** no new Agent/Dispatch/Task attempt; no source code or installed Python file writes, SQLite edits, process/task service changes, main/merge, Canary/COMPAT001, broker/provider/LIVE.
