# FOX2 — Bridge RC1 Pre-Canary Static Readiness Check

**Date:** 2026-10-18
**Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
**Mode:** CHAT direct / FOX2 Skills v0.2.4 / read-only Git source analysis; publication of this report only.
**Scope:** Stage-specific evidence after Owner's independent-audit waiver. Not Windows installed-host verification, not an executable PreExec, not a fresh release approval.
**Finding:** `STATIC_SOURCE_AND_WAIVER_CHECK=PASS_12_OF_12`; `CURRENT_WINDOWS_LEDGER=NOT_OBSERVED`; `CANARY_PREEXEC=NOT_RUN`; `EVALUATOR_FULL_COVERAGE=UNKNOWN`; **`FOX2_BRIDGE_RC1_PRECANARY_READY=HOLD`**.

## 1. Sources actually inspected

- Owner RC1 approval: `451aaaf617cc2c9b7e4a9f8f6503e75bbc8e95a1:docs/governance/releases/FOX2_OWNER_BRIDGE_RC1_PRECANARY_AUDIT_WAIVER_APPROVAL_20261018.json`, blob `a39c92cb385f36c9eaa12d34e4299c885ae649e4`.
- RC1 acceptance addendum: `aa074802dd12673defd61f43c347c119e9770caf:docs/agent_handoff/FOX2_BRIDGE_RC1_OWNER_WAIVER_ACCEPTANCE_ADDENDUM_20261018.md`, blob `d65fba987cb3777dfb3fd8dbaa46a9f21b00e47f`.
- Scoped publication: `7b59908596b476611b095ff9ffe81d7916367f21:docs/governance/releases/FOX2_OWNER_WAIVER_SCOPED_PUBLICATION_20261018.json`, blob `ff77d91d3d1ffada412d6ebc34651130c615969c`.
- Impact matrix: `6f41212e1c50c1b9d4a22f068ec06512480bae46:docs/governance/releases/FOX2_OWNER_ACCEPTANCE_WAIVER_CHANGE_IMPACT_20261018.json`.
- Frozen RC1 technical task and original gate matrix at `f3d6468fedb553ba6c6192ba5811cb1b26a11ab9`; gate blob `fc126e1b4dd4d4978a322b51aef31e11aaee2e39`.
- Frozen WP-only Registry: `b27f1085ee13d8dce56fd2735e100ea1616e6e23`, bound source `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`, Owner approval `d8e2331674ef1921844f369bfa9e48b82a73c6a1`.
- Locked Canary branch `work/FOX2-BRIDGE-FINAL-CANARY-009` @ `501822a33ef08c7365154913bbc677544856eee5`; control `work/FOX2-DISPATCH-chat` @ `dc79f8143eec471508bf37565bff38442ce0548a`.
- Source code at the frozen Bridge head: `agent_bridge/src/fox2_agent_bridge/{__main__,desktop,ledger,paths,app,e2e_runner,dispatch_schema_v3_contract,installation,ops_runner,project_dictionary}.py` plus `agent_bridge/scripts/bridge_ops.ps1` and `agent_bridge/README.md`.
- Cloud Skills metadata: `fox2-skills-integrated` v0.2.4 / `pluginrel_6ad4c736df548191bd040b44c458e697`; read `fox2-source-resolver`, `fox2-governance-preflight`, `fox2-feature-certification`, `fox2-result-review`, `fox2-execution-recovery`, `fox2-status-roadmap`, `fox2-techspec-validator`, `fox2-strategic-agent-triage`, `fox2-agent-route-runtime`.
- Existing historical verification: 34/34 bounded checks and B2 10/10 source families from earlier Git Result; **not reexecuted**.

## 2. Twelve directly executed static assertions

Assertions were evaluated directly from authenticated Git file bytes in CHAT's JavaScript execution environment. `PASS` in this section means an actual static assertion passed; it does **not** mean Canary readiness or runtime certification.

| # | Assertion | Result |
|---|---|---|
| 1 | Original gate matrix has 40 entries: 38 PASS; `PRECANARY_INDEPENDENT_AUDIT=PENDING`; `ICON_DISPOSITION` explicitly non-gating | PASS |
| 2 | Frozen task's 34 pre-Canary required gate names appear in original matrix; non-waived ones remain PASS in that historical matrix | PASS |
| 3 | Exact Owner authorization refers only to RC1 / only audit gate / `WAIVED_BY_OWNER` / no other WP | PASS |
| 4 | Scoped publication binds the Owner waiver while explicitly withholding pre-Canary readiness | PASS |
| 5 | Negative: APP-B cannot inherit this waiver | PASS |
| 6 | Negative: `SOURCE_FREEZE` cannot inherit this waiver | PASS |
| 7 | Negative: a `PASS` label cannot substitute for the new `WAIVED_BY_OWNER` disposition | PASS |
| 8 | Task retains exact Canary ID, locked branch/head and max_runs=1 | PASS |
| 9 | Source proves `fox2_agent_bridge status` can initialize/migrate the runtime database; cannot be described as an absolutely read-only inspection | PASS (safety finding) |
| 10 | SQLite persisted tables `dispatches` and `executions` with query support can be inspected using read-only SQL when safely opened | PASS (capability identified, not performed on Windows) |
| 11 | No literal `WAIVED_BY_OWNER` or `PRECANARY_INDEPENDENT_AUDIT` handling was found in the five examined runtime modules (`app.py`, `e2e_runner.py`, `dispatch_schema_v3_contract.py`, `__main__.py`, `desktop.py`) | PASS (limited search; cannot conclude absence projectwide) |
| 12 | Existing impact record truthfully marks Windows ledger UNKNOWN, Canary fresh PreExec NOT_RUN and readiness HOLD | PASS |

**Result:** `12 PASS / 0 FAIL`. These are STATIC evidence checks only. All 38 technical PASS gate outcomes are **historical source-receipt PASS**, not freshly reexecuted tests.

## 3. Material pre-Canary host admission still missing

**H1 — Current installed package/source pointer:** Current per-user installation under `%LOCALAPPDATA%\FOX2\AgentBridge` (see `paths.py`) must be read and compared with locked RC1 package/source identity. Relevant paths include `current.json`, `versions/<package_sha256>/receipt.json`. Do not assume a matching Git HEAD proves the executable currently installed on Windows.

**H2 — Current Canary single-use ledger:** Verify the real persisted `data/bridge.db` (and any migration/legacy ledger at `C:\Projects\FOX2-AgentBridge\data\bridge.db`) for the exact immutable `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001` dispatch. Check `dispatches`, `executions`, and `data/manual_consumption.json`, and confirm there are no uncertain, duplicate or claimed starts. If any claim exists or result is uncertain: **STOP / NEEDS_RECONCILIATION; no replay**. Absence from Git is not absence from host ledger.

**H3 — Safe read-only method:** The Git source for `fox2_agent_bridge status` routes through `initialize_runtime` in `__main__.py`. That function calls `ledger.initialize()`, which can create/migrate the SQLite schema, and may insert historical consumed dispatch identities from `manual_consumption.json`. Therefore `bridge_ops.ps1 status` **must not be used as a zero-side-effect attestation**. Prefer a bounded, authenticated host check that reads file metadata and opens the actual SQLite database in SQLite URI `mode=ro` with `PRAGMA query_only=ON`; assess any WAL sidecar/freshness semantics. For strict zero-filesystem-write inspection obtain a correctly captured, transaction-consistent read-only snapshot; never use an `immutable=1` connection to a live WAL database and infer no claim from potentially stale contents. Exact host evidence not yet supplied.

**H4 — Acceptance evaluator compatibility:** Original task says every listed gate must `PASS`, while the owner-approved scoped overlay says one audit gate is `WAIVED_BY_OWNER`. The five inspected executable modules did **not** expose a waiver-aware evaluator. Scope of the code inspection is limited: do not claim the project has no such evaluator. Before automated admission, identify actual consumer (if any) and prove it can apply the authorized exception without changing historical receipt to `PASS`. If no machine consumer exists and the original decision is made by CHAT, record a source-bound human acceptance decision only after H1/H2/H5 independently pass.

**H5 — Fresh Canary-specific PreExec and operational readiness:** Inspect actual current Agent route, permissions, worktree ownership, relevant tool availability/quota evidence, installed config, and exact immutable Canary `agent/model/permission` tuple; produce a durable PreExec under the already effective WP-only governance. UNKNOWN is not PASS. Do not create a new dispatch to prepare this check. No Canary 009 execution is authorized here.

## 4. Decision and next bounded action

```text
RC1_OWNER_AUDIT_WAIVER=APPROVED_SCOPED
RC1_AUDIT_ACTUALLY_PERFORMED=BLOCKED_HISTORICAL_UNCHANGED
STATIC_GATE_RECONCILIATION=PASS_12_OF_12
CURRENT_WINDOWS_PACKAGE_AND_LEDGER=NOT_OBSERVED
CANARY_PREEXEC=NOT_RUN
WAIVER_AWARE_EVALUATOR=NOT_VERIFIED_FULL_COVERAGE
PRECANARY_READINESS=HOLD
CANARY_009_EXECUTED_IN_THIS_STEP=NO
APP_B_RESUMED=NO
```

**Next permitted host work:** H1+H2 first, H4 only insofar as the identified acceptance consumer makes it material, then H5. This must execute in an actual authorized Windows host with source-bound read-only permissions and fresh R3/R5 PreExec. CHAT can directly intake those results and decide readiness; CODEX/COPILOT are conditional host-capability candidates, **not assigned executable tasks yet**. WORK independent audit is no longer required for this waived RC1 checkpoint; other WPs are unaffected.

## 5. Routing R0–R7 and STOP

- R0: Preserve implementation Dispatch 004, earlier 34/34 audit and B2 resolver closure; no replay.
- R1: Stage is RC1 pre-Canary technical readiness, not product implementation.
- R2: Owner waiver is exact-WP-only; Policy v1.9.0 and global Owner Waiver candidate are **NOT EFFECTIVE** and do not rebind the frozen sources. No new DEV/merge/LIVE right.
- R3: CHAT authenticated Git source/readback available. Windows current installed ledger, CODEX/COPILOT host quota/model access **UNKNOWN**.
- R4: CHAT direct static checks complete; hand off only material Windows host checks to a verified route. WORK waived; do not ask Owner for reviewer-admission records.
- R5: Read-only source inspection and one new file in CHAT-owned non-main Governance docs; no protected branch/product or Windows worktree writes.
- R6: Report requires immutable Git result and exact remote byte readback; no Library/global release/effective claim.
- R7: STOP until H1, H2, H4 when applicable, H5 have genuine adequate evidence and CHAT issues separately justified `FOX2_BRIDGE_RC1_PRECANARY_READY`. No Canary execution, APP-B resume, dispatch replay, main/merge/provider/broker/LIVE.
