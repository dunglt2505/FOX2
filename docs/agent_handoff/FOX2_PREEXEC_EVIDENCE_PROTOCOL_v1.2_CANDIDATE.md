# FOX2 — Pre-Execution Evidence Protocol v1.2 CANDIDATE

**Status:** CANDIDATE / NOT EFFECTIVE  
**Scope:** FOX2 project-wide; all new/re-scoped executable work  
**Controlling authority:** Project Dictionary v1.3 CANDIDATE -> Policy V1.9.0 CANDIDATE -> Routing Index V1.4.0 CANDIDATE  
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

## 7. Alternative Agent route materiality

When a task permits multiple implementation Agents, those Agent probes are alternatives, not simultaneous prerequisites.

Canonical semantics:

```text
candidate: COPILOT -> routing evidence -> normally NON_MATERIAL
candidate: CODEX   -> routing evidence -> normally NON_MATERIAL

eligible_agent_route -> MATERIAL aggregate
  PASS    = at least one allowed candidate PASS
  FAIL    = no allowed candidate proves current execution readiness
```

Rules:
- a failed preferred candidate does not make the receipt BLOCKED when another allowed route passes;
- candidate failure remains durable evidence so CHAT can compare cost/capability;
- candidate probes never select themselves; CHAT selects the final Agent after receipt intake;
- no Bridge/runner/Agent may silently substitute an alternative route;
- if the task explicitly pins one Agent because of a material requirement, that candidate is MATERIAL and no aggregate alternative may override its failure;
- numeric quota telemetry is optional when a live execution probe already demonstrates readiness.

The machine Receipt Schema v1 does not require a version bump for this rule: candidate capabilities use the existing `material` field and the aggregate is represented as another capability entry.

## 8. Worktree hygiene

A preflight may remove/reset only stale evidence that is objectively proven to belong solely to the current preflight receipt.

If any unrelated WIP exists, HOLD/INFRA_FAILED. Do not stash/reset/rebase unrelated work to make preflight pass.

## 9. Agent probe semantics

A minimal probe is execution-readiness evidence, not implementation.

A probe:
- must not edit product code;
- must not change routing by itself;
- must not silently substitute Agent/model/tier/reasoning;
- may prove that a selected candidate can execute with the requested permission profile;
- may classify auth/quota/capacity/config/tool failure.

A successful candidate probe does not grant merge/deploy/provider/broker/LIVE authority.

## 10. CHAT intake

CHAT evaluates receipts using:

`docs/agent_handoff/FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.md`

Only CHAT may convert preflight evidence into final assignment/Dispatch publication.

## 11. Project-wide implementation

All FOX2 handoff generators, local preflight runners, Bridge readiness surfaces and future executable-WP launchers must implement this protocol or a generated/shared implementation derived from it.

Do not fork task-specific state machines. WP-specific checks are extensions to the common receipt, not replacements.

## 12. Non-effects

This protocol grants no main/PR/merge/deploy/provider/broker/LIVE authority and changes no BRD/Data Contract/M1 Acceptance semantics.

`FOX2_PREEXEC_EVIDENCE_PROTOCOL_V1_1=RELEASED_EFFECTIVE / DURABLE_RECEIPT=REQUIRED / AGENT_ROUTE_MATERIALITY=AGGREGATE / PRESTART_FAILURE_DISPATCH_CONSUMED=NO / PROJECT_WIDE=YES`


## Direct CHAT operation vs Agent pre-execution — proposed v1.2 amendment

Before invoking this Agent PreExec protocol, CHAT runs DIRECT_EXECUTION_CHECK: Is the Owner-authorized deliverable a read-only analysis, candidate documentation/source sync or a bounded connector operation that CHAT itself can safely perform and verify? If yes, use CHAT's operation-specific permission/source/destination/readback controls, *not* synthetic Agent probes, receipts or dispatches. If only a residual part requires a coding host, complete direct work first and run this PreExec for that exact residual executable WP. No existing Agent-bound preflight may be skipped. Preserve `max_runs=1`, evidence durability, PASS/BLOCKED/INFRA_FAILED semantics and Agent-pinned material capabilities. This candidate does not change schema v1 or deployed shared implementation before release.

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
