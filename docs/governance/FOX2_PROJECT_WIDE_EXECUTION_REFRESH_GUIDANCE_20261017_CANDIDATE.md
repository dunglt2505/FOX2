# FOX2 project-wide execution source refresh guidance

Status: OWNER-DIRECTED CANDIDATE; NOT EFFECTIVE; runtime implementation NOT RUN.
Date: 2026-10-17
Parent observation: dunglt2505/FOX2 at 5d6fab38448a4c33a052fc64f3212eac25972a38.
Controlling proposed contract: docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md.

## Governance and routing guidance

Historical version citations are allowed. A static citation is neither a source selection input nor a stale-source failure by itself. At every actual execution admission, automatically read authenticated live Git using the independently trusted Registry discovery configuration. Resolve Policy, Routing, Dictionary, Protocol and task-specific BRD, specifications, templates, schemas and evidence as one compatible bundle. Record observed candidates, selected immutable commits/paths/SHA-256 and exclusions.

Distinguish the newest observed source from the newest applicable source using authorized lineage, scope, compatibility and approval metadata. Do not rank by filename or commit timestamp. If a potentially applicable newer source cannot be verified, report LATEST_PRESENT_BUT_BLOCKED; do not silently downgrade. An explicitly out-of-scope source may be excluded with evidence. Conflicting lineage or authority fails closed. A file declaring itself EFFECTIVE cannot supply independent authority.

Refresh failure, missing authority or incompatible required schema blocks admission with no cached fallback. Refresh success grants no execution, DEV, release, merge or LIVE permission.

## BRD-related guidance and change impact

Add this rule prospectively to BRD registry-binding guidance and requirements-to-acceptance mapping. Existing BRD business semantics and historical release artifacts remain intact. Classify the shared admission lifecycle change as SEMANTIC_SOURCE_CHANGE under the observed candidate Dictionary, requiring coordinated owning-source review; this classification is a candidate assessment, not a release decision.

Required trace:
- SOURCE-01: historical reference allowed -> static-reference acceptance.
- SOURCE-02: fresh Git resolution before execution -> observed/selected bundle evidence.
- SOURCE-03: trusted applicability and compatibility -> authority/conflict/schema tests.
- SOURCE-04: race-safe admission -> final drift validation and atomic claim tests.
- SOURCE-05: consumed dispatch immutability -> no replay and frozen snapshot tests.
- SOURCE-06: protected gates retained -> denied privilege escalation tests.

Business application runtime should not acquire governance dependencies unless its operation materially requires them. Enforce shared work admission rather than inserting governance metadata into business decisions.

## Protocol and PreExec guidance

Required sequence for new or unstarted execution:
task-state inspection -> live discovery -> verified applicable bundle -> R0-R7 -> material PreExec -> CHAT receipt intake -> final source drift validation -> atomic claim/side effect admission.

The execution boundary must validate the same bundle used for preflight. If material Registry/source drift occurs, invalidate the pending admission and repeat governed resolution/preflight as required, without consuming a dispatch. A TTL alone is insufficient. The production adapter must define how its source revision check and durable claim prevent concurrent claims and stale admission; a pre-claim read by itself does not prove atomicity.

For consumed/started dispatches, inspect durable state first. Never create another execution, replace its immutable source snapshot, regenerate its receipt or rewrite its history. Continuation within an existing attempt retains its admitted source lock; any distinct new attempt requires legitimate authorization and fresh admission. Mid-run updates may trigger a governed stop/reconciliation when required, not hot-swap.

Results must separately record REFRESH, APPLICABILITY, AUTHORITY, PREFLIGHT, EXECUTION and RELEASE outcomes, including NOT_RUN. No synthetic PASS receipts.

## Skills guidance

Apply this shared rule to all FOX2 Skills at invocation and before material actionable operations. Static examples and historical version names may remain. Skills must call the shared resolver/admission service with explicit trusted host configuration and required source families; do not implement competing version selectors in each Skill. An installed package or local cached helper is not proof of a fresh Git check.

Read-only discovery and authorized candidate-document operations can proceed with clearly labeled unverified authority. Source-dependent implementation remains held when required authority/PreExec/ownership is unknown. Do not fabricate Agent dispatch or PreExec for direct CHAT document operations.

## Runtime acceptance matrix

All cases below are REQUIRED, NOT RUN in this continuation:
1. OLD_REFERENCE_ALLOWED: old citation with fresh admissible bundle passes source admission.
2. NEW_SOURCE_BEFORE_RUN: eligible new source is bound despite old authored text.
3. NEW_SOURCE_BLOCKED: unresolved potentially applicable newer source blocks, with no silent downgrade.
4. REFRESH_FAILURE: network/auth/Registry failure produces no claim or side effect.
5. AUTHORITY_CONFLICT: missing independent trust or competing source lineage blocks.
6. BUNDLE_COMPATIBILITY: individually valid but incompatible family/schema combination blocks.
7. DRIFT_BEFORE_CLAIM: source changes after PreExec; no stale side effect or consumed dispatch.
8. CONCURRENT_CLAIM: competing workers yield exactly one admitted execution.
9. CONSUMED_PINNED: repeated poll/restart preserves snapshot and executes zero additional effects.
10. PROTECTED_GATES: refresh success cannot enable merge, release, broker/provider writes or LIVE.
11. ACTUAL_BOUNDARIES: exercise direct-action adapter, Agent PreExec, Bridge dequeue/claim and recovery path; a resolver-only unit test cannot certify rollout.
12. AUDIT: sanitized evidence contains refresh time, Registry identity/revision, candidates, selection/exclusions, source commits/digests, compatibility and attempt identity.

## Current boundary

Existing contract and release-hold receipt were inspected remotely. No current independently trusted Registry location was supplied. No runtime worktree ownership or current PreExec receipt was verified. No runtime files changed, tests executed, dispatch replayed or protected gates altered.

This addendum is reviewable candidate guidance only. Existing governance manifest digests are not rewritten; future authorized publication must generate a new immutable manifest after all coordinated source changes and readback. Local save, Git publication, installed Skills behavior and EFFECTIVE release are separate outcomes.
