# FOX2 — Pre-Execution Evidence Protocol v1

**Status:** RELEASED_EFFECTIVE  
**Scope:** FOX2 project-wide; all new/re-scoped executable work  
**Controlling authority:** Project Dictionary v1.1 -> Policy V1.8.8 -> Routing Index V1.2.9  
**Purpose:** provide one durable, fail-closed evidence lifecycle before executable Dispatch publication.

## 1. Boundary

Pre-execution evidence answers whether CHAT has enough current material facts to finalize an execution assignment. It is not application acceptance, not Agent result evidence and not post-start reconciliation.

The project-wide boundary is:

```text
task/source ready
 -> bind material preflight requirements
 -> run non-implementation preflight
 -> publish/read Preflight Receipt
 -> CHAT closes R3/R5
 -> final Agent assignment
 -> executable Dispatch
 -> Agent execution
 -> Agent result
 -> CHAT result intake
```

## 2. States

### PASS

All bound material capability/worktree checks required to start the WP are proven sufficient.

PASS requires a durable receipt and CHAT remote readback before final assignment/dispatch.

### BLOCKED

A material prerequisite is missing, unavailable, denied or proven incompatible.

Examples include missing Node/npm for a React WP, unavailable required Windows packaging capability, Agent auth/capacity failure, wrong worktree, or material permission-profile mismatch.

BLOCKED:
- publishes a sanitized receipt when the task branch is safely writable;
- does not publish executable Dispatch;
- does not start an implementation Agent;
- does not consume a dispatch;
- does not trigger replay semantics;
- remains the same WP unless material scope changes.

### INFRA_FAILED

The preflight/evidence mechanism itself could not complete. Examples: unsafe worktree state, Git publication failure, receipt serialization failure, or inability to establish a safe task worktree.

If a safe publication path exists, publish a sanitized INFRA_FAILED receipt. If publication itself is the failing capability, surface an explicit local failure and do not claim Git evidence exists.

## 3. Durable receipt

The current machine contract is:

`docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`

A receipt records only bounded evidence required for routing and pre-execution readiness. Raw CLI output, secrets and unrestricted environment dumps are prohibited.

The receipt must identify:
- project/WP/task branch;
- exact source/task head used by the preflight;
- timestamp;
- overall status;
- material capability observations;
- sanitized blockers;
- worktree/writer state;
- candidate route if one is demonstrably executable;
- explicit facts that executable Dispatch is not yet published/consumed and implementation Agent has not started.

## 4. Git publication

When safe Git publication is available, PASS and BLOCKED receipts are committed/pushed to the exact non-main task branch under its authorized report/evidence path.

Required publication sequence:

```text
write canonical receipt
 -> git add exact receipt
 -> git diff --cached --check
 -> verify staged allowlist
 -> commit
 -> push exact task branch
 -> remote readback exact SHA
 -> only then emit RECEIPT_PUSHED
```

No success marker may be emitted earlier.

## 5. Canonical text

Generated receipt/evidence text is UTF-8 without BOM, LF line endings, deterministic where practical, no trailing whitespace, final newline when textual, and secret-safe.

Platform-default CRLF is not accepted merely because the host is Windows.

## 6. Failure preservation

A preflight should preserve the first material blocker while continuing only those checks that are safe and useful for diagnosis/evidence.

Do not cascade missing-variable errors after a known prerequisite failure.

Do not erase a blocker merely because another Agent/tool is also unavailable.

Agent probe evidence should record safe fields such as:
- product;
- CLI version when observable;
- exit code;
- sanitized failure class;
- required permission profile;
- whether the expected proof marker was observed.

Do not persist raw prompt responses or credential-bearing stderr by default.

## 7. Worktree hygiene

A preflight may remove/reset only stale evidence that is objectively proven to belong solely to the current preflight receipt.

If any unrelated WIP exists, HOLD/INFRA_FAILED. Do not stash/reset/rebase unrelated work to make preflight pass.

## 8. Agent probe semantics

A minimal probe is execution-readiness evidence, not implementation.

A probe:
- must not edit product code;
- must not change routing by itself;
- must not silently substitute Agent/model/tier/reasoning;
- may prove that a selected candidate can execute with the requested permission profile;
- may classify auth/quota/capacity/config/tool failure.

A successful candidate probe does not grant merge/deploy/provider/broker/LIVE authority.

## 9. CHAT intake

CHAT evaluates receipts using:

`docs/agent_handoff/FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.md`

Only CHAT may convert preflight evidence into final assignment/Dispatch publication.

## 10. Project-wide implementation

All FOX2 handoff generators, local preflight runners, Bridge readiness surfaces and future executable-WP launchers must implement this protocol or a generated/shared implementation derived from it.

Do not fork task-specific state machines. WP-specific checks are extensions to the common receipt, not replacements.

## 11. Non-effects

This protocol grants no main/PR/merge/deploy/provider/broker/LIVE authority and changes no BRD/Data Contract/M1 Acceptance semantics.

`FOX2_PREEXEC_EVIDENCE_PROTOCOL_V1=RELEASED_EFFECTIVE / DURABLE_RECEIPT=REQUIRED / PRESTART_FAILURE_DISPATCH_CONSUMED=NO / PROJECT_WIDE=YES`
