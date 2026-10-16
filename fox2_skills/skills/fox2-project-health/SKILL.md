---
name: fox2-project-health
description: Assess FOX2 health from current Git evidence, work states, risks and open gates.
---
# FOX2 Skill 03 — project-health

## Objective
Assess FOX2 health from current Git evidence, work states, risks and open gates.

## Mandatory Git-first source preflight
Before **every new task or material dispatch**, run the shared read-only resolver at `../../shared/native_registry.py` against the **authenticated, current FOX2 Registry location** supplied by the execution host. Resolve all required source families (Policy, Routing, Dictionary, Protocol, plus task-specific BRD, technical specs, templates, schemas and evidence) through Registry → release manifest → immutable Git commit/path → content SHA-256. **Never hardcode version numbers, select the highest filename version, trust Git `main` alone, or infer EFFECTIVE from commit recency.** The host must independently validate Registry authority and release approval; a Git file's self-assertion is insufficient. Do not fall back to cached/Library sources when live Git verification fails.

If a required source is missing, stale, conflicting, inaccessible, or unverified, return `SOURCE_UNVERIFIED` or `SOURCE_CONFLICT` with evidence and **hold dependent execution**. Do not fabricate approvals, permissions, hashes or release status. Preserve the approved immutable source lock for in-flight work; require material impact review before rebind. Resolver performs read-only checks and grants no DEV, merge, publication, or LIVE authorization.

## Execution sequence
1. Parse request, existing work package, task state, and no-replay constraints.
2. Verify current Git Registry authority and resolve the required EFFECTIVE sources using the shared resolver. Capture registry ref, registry commit, manifest ref/commit, source commit/path and SHA-256 in the task evidence.
3. Verify policy, routing, allowed paths, permissions, source lock, acceptance and stop conditions. Resolve routing once per dispatch, not per substep.
4. Perform only the bounded objective: assess fox2 health from current git evidence, work states, risks and open gates.
5. Return evidence-backed result and next handoff with source binding and any blockers; never declare PASS without executed tests and readback.

## Acceptance
- Source versions are dynamically resolved at invocation, never pinned in this Skill.
- Unverifiable/conflicting governance fails closed.
- Existing task source lock and no-replay are respected.
- Output records exact source provenance and observed execution evidence.
- Candidate documentation is not authority to install, release, merge, or deploy.

## Integrated input/output contract

Required input: task_id, cutoff, actual state, scoped authority, source lock, evidence receipts, and facts, unknowns, blockers, next_milestone.

Resolve only relevant source families: roadmap. Use the host-authorized native Registry adapter; no synthetic Registry schema is runtime authority.

Reconcile acceptance with evidence cutoff; never infer completion from commits.

Use [shared runtime](../../shared/runtime.py) for contract/preflight and evidence readback. `PREPARED_FOR_HOST_REVIEW` validates supplied input structure and byte receipts only; complete the Skill-specific workflow above in the host before judging semantic acceptance. Return output, source lock, cutoff, factual evidence, unknowns, and typed holds.

STOP dependent actions for missing material source/authority, conflict, replay, failed readback or writer collision. Continue independent work. Errors: UNVERIFIED, SOURCE_CONFLICT, UNAVAILABLE, BLOCKED. Never interpret helper success as host acceptance or release authority.

Acceptance scenarios: provide the listed inputs with valid host bindings and evidence; reject missing inputs, material unverified sources and completed task replay. Host behavior must also satisfy: Reconcile acceptance with evidence cutoff; never infer completion from commits.
