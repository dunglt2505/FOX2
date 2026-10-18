# FOX2 — Canary009 PreExec Compatibility: Minimal Implementation Scope (CANDIDATE)

**Status:** `PRE-DEV / CANDIDATE_NOT_AUTHORIZED_FOR_CODE`
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Purpose:** Approval-ready technical change package, **not** an executable Agent assignment, code change, PreExec receipt or permission grant.
**Contract:** `docs/governance/releases/FOX2_CANARY009_PREEXEC_COMPATIBILITY_CONTRACT_CANDIDATE_20261018.md`
**Consumer matrix:** `docs/governance/releases/FOX2_CANARY009_PREEXEC_COMPATIBILITY_CONSUMER_MATRIX_20261018.json`

## 1. Authority and phase boundaries

Owner already approved the scoped **receipt-location** exception at commit `84ac87fbccc947c16490fb9365dc5a3d8e49661c`; do not revisit it. That exception does **not** authorize changing Schema v1, CHAT intake v1.1, shared producer, generated Dictionary or installed runtime.

**Required distinct future permissions:** (A) Owner/owning-source authorization for a prospective existing-published-dispatch **semantic contract** and its version/consumer selector; (B) explicit bounded **code scope** and code writer after a fresh PreExec for **this new coding task**; (C) subsequent governed contract/source release and compatibility tests; (D) separate Windows runtime adoption, host worktree verification, pinned-agent probe and Canary-specific durable PreExec. Approval of A does not itself grant B–D.

Do not label `CODE_ALLOWED`, `RELEASED_EFFECTIVE`, `PASS_TO_ASSIGN`, `FOX2_BRIDGE_RC1_PRECANARY_READY` or Canary permission as granted by this candidate. Source/authority conflicts remain HOLD.

## 2. Proposed implementation source and isolation (not created)

- Repository `dunglt2505/FOX2`.
- **Proposed implementation base:** `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9` (inspected frozen runtime baseline). Must re-check its ancestry against authorized current material source before accepting; DO NOT silently rebase onto main/latest Policy or newer product code.
- **Proposed bounded code branch (currently NOT_CREATED/NOT_AUTHORIZED):** `work/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018`.
- **Proposed Windows code worktree:** `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018`. Actual ACL, ownership, git registration, clean WIP and exclusive writer remain **UNKNOWN** until examined on the host.
- **Never use as development checkout:** `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`. Its immutable Dispatch, prompt and HEAD are protected.
- **Candidate code writer:** one of eligible COPILOT or CODEX, selected only by CHAT after R3/R5 admission. Current last-known Codex v0.162.1 account quota 44%/69% at prior observation, pinned Canary capability not proven; Copilot v1.0.98 quota/auth current UNKNOWN. No Agent assigned. Worker/Canary may not be used as an Agent probe.
- **Delivery permission proposal:** single-writer, bounded non-main code+test/report commit/push after PreExec and CHAT PASS_TO_ASSIGN; no main/PR/merge/deploy/provider/broker/LIVE. Owner must grant actual repo/host write scope before issuance.

### Exact phase-1 source/test allowlist proposal

These already exist at inspected baseline; only necessary minimal edits upon approved CODE_ALLOWED:

1. `agent_bridge/src/fox2_agent_bridge/preexec/engine.py` — two source identities, published-dispatch observation, split publishing and fail-closed writer/race/readback checks.
2. `agent_bridge/src/fox2_agent_bridge/preexec/profiles.py` — explicit existing-published Canary009 cohort identity; unchanged old profiles.
3. `agent_bridge/scripts/preexec.py` — explicit compatible CLI selection / publication locator without reinterpreting legacy flags.
4. `agent_bridge/tests/test_preexec.py` — targeted compatibility, same-branch v1 regression, safe remote fixture and negative/race/no-replay tests.

**Only if proven required** after focused impact:
- `agent_bridge/src/fox2_agent_bridge/preexec/probes.py` (already working pinned probe should be reused, not redesigned);
- `agent_bridge/scripts/generate_project_dictionary.py`, `agent_bridge/src/fox2_agent_bridge/project_dictionary.py`, `agent_bridge/tests/test_project_dictionary.py` (Dictionary source / generated binding must be versioned and approved first);
- `docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/preflight.ps1` (keep legacy thin adapter unchanged by default);
- `agent_bridge/src/fox2_agent_bridge/e2e_runner.py`, `agent_bridge/src/fox2_agent_bridge/dispatch_poller.py` (no demonstrated need to edit; changes not pre-authorized).
No `agent_bridge/**` blanket allowlist is granted. Any added path needs an updated approved scope and PreExec materiality review before write.

### Prospective schema/intake source candidates — no canonical version chosen

Any new schema/intake/protocol source files must be **new** names without changing v1 EFFECTIVE; candidate staging path suggestions (not yet created nor authoritative):

- `docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_EXISTING_DISPATCH_EXTENSION_CANDIDATE_20261018.json`
- `docs/agent_handoff/FOX2_CHAT_PREFLIGHT_EXISTING_DISPATCH_INTAKE_CANDIDATE_20261018.md`
- `docs/agent_handoff/FOX2_PREEXEC_EXISTING_DISPATCH_CONTRACT_ADDENDUM_CANDIDATE_20261018.md`

These are proposed **candidate filenames, not official schema IDs/version declarations**. Semantic source owner/Owner must decide controlled independent version vs extension, version number, effective routing and runtime generated binding. Do not hot-swap an already installed runtime or frozen v1 Dictionary.

## 3. Phase order — no circular permission workaround

```text
Candidate contract + consumer evidence (this CHAT action)
 -> explicit scoped Owner/owning-source semantic contract approval
 -> bounded coding WP/task approval on a NEW NON-CANARY branch
 -> run EXISTING v1 pre-dispatch PreExec for this NEW coding task, publish/read back on that task branch
 -> CHAT PASS_TO_ASSIGN after verified writer/capability/quota/source
 -> one eligible implementation Agent (no silently changing pinned Canary agent)
 -> exact diff + targeted tests + v1 regression + negative safety tests
 -> verify Git result bytes and CHAT intake
 -> governed prospective contract/Registry/consumer release and adoption
 -> only then Windows Canary worktree, exact pinned tuple probe, fresh ledger and compatible durable Canary PreExec on the approved evidence branch
 -> CHAT separate pre-Canary readiness decision
```

**No chicken-and-egg:** Existing Schema v1 correctly covers the NEW coding WP because it has no executable Dispatch at the point of its own preflight. The Canary009 published=true case must only use the new contract **after** actual compatible adoption. Do not publish a fake Canary receipt or waive PreExec capability gates.

## 4. Acceptance tests — mandatory, scoped, safe fixtures

- **V1 preservation:** Existing `test_preflight_durable_statuses`, pinned alternative route, hygiene, WIP, stale receipt, writer lock, hook, exact readback and secret/redaction tests still pass without changes to v1 fixtures or historic receipts. Do not recertify unchanged full Windows installer suites merely for this delta.
- **True existing dispatch:** Fixture with `published=true`, exact dispatch/prompt/source-set/Owner binding, recent verified `consumed=false` and `started=false` can produce a compatible candidate receipt only under separately authorized schema profile and after all material checks. No future user-visible PASS before remote readback.
- **Falsehood rejection:** Force `published=false` for an already-published dispatch; must REJECT. Feed `published=true` to Schema v1; must REJECT, proving old schema is unchanged.
- **Identity negatives:** Wrong dispatch ID, path, original SHA-256 `a8756aa6...`, prompt SHA-256 `dd9f45c5...`, task commit `501822a...`, Registry `b27f1085...`, Owner exception commit `84ac87f...` or artifact bytes must REJECT before probe/write.
- **Ledger negatives:** Either `consumed=true`, `started=true`, an unrecognized field, UNKNOWN/stale timestamps or conflicting per-user/legacy/manual-consumption records → BLOCKED/NEEDS_RECONCILIATION, no readiness.
- **Dual-head isolation:** A receipt commit on evidence branch must never change locked Canary head nor substitute evidence HEAD as task source; simulated expected-head mismatches must STOP.
- **Ownership:** Fail on nonexclusive writer, wrong branch, unrelated staged/untracked files, Git rename conflicts, unsafe cleanups, required host permission missing.
- **Publication:** Reject expected remote head drift, unapproved branch/path, non-fast-forward, Git hook mutation, secret-scan failure, invalid JSON, byte-readback mismatch; no `RECEIPT_PUSHED` in failure.
- **Operational isolation:** All tests use disposable Git test remotes and synthetic dispatch IDs, never actual `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001` claim; forbidden commands `e2e-once`, `run-next`, worker resume, `poll-once`, deployment, provider/broker calls.
- **Consumer compatibility:** Explicitly test old intake and new cohort routing/validation, generated Dictionary only if approved, all identified caller entry points; unknown material consumer inventory remains HOLD.

Evidence assertions above are **acceptance criteria**, not executed runtime tests.

## 5. Routing and safety before engineering assignment

- R0: Preserve completed 38 technical PASS, 10/10 WP authority checks, Owner waiver and location grant. No replay.
- R1: Phase is proposed semantic contract and code change; not RC1 implementation reprise and not Canary launch.
- R2: SOURCE_AUTHORITY for code contract change = **MISSING**; `CODE_ALLOWED=HOLD`; freeze main/Canary/control/runtime; source release gates separate.
- R3: Need fresh Windows code Agent auth/capacity/model and host ownership, selected route and rights before code task; historical quota alone is inadequate.
- R4: CHAT direct docs now; COPILOT candidate for simple scoped code if demonstrably eligible/cost-effective; CODEX candidate for material concurrent writer/publish correctness; neither automatically assigned. WORK only if a later independent readiness check is specifically required, not the waived audit.
- R5: Proposed branch/worktree not created. Exclusive writer/clean WIP UNKNOWN; no implementation writer yet.
- R6: New coding WP must first obtain its own actual v1 PreExec and remote readback; code Git diff/test and subsequent contract release are separate proofs.
- R7: STOP on source drift, unapproved code/semantic changes, uncertain ledger, wrong worktree, concurrency/replay, mismatch, non-readback; no DEV/main/merge/LIVE/Canary from this document.

## 6. Expected deliverables after separate approval

An authorized engineering Agent would deliver exact scoped diff, tests/fixture evidence, sanitized reports and immutable Git remote readback on its approved non-main branch, then CHAT intake. The release owner would separately certify the newly authorized semantic schema/intake profile and producer compatibility at a governed release checkpoint before any installed runtime change.

**Current phase:** `CONTRACT_CANDIDATE_GIT_DOCUMENTATION`; `IMPLEMENTATION_AUTHORITY=BLOCKED_NOT_REQUESTED_IN_THIS_TASK`; `CANARY_HOST_WORKTREE=NOT_RUN`; `CANARY_PREEXEC=NOT_RUN`; `READINESS=NOT_GRANTED`.
