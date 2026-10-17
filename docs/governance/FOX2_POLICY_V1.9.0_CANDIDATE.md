# FOX2 — POLICY V1.9.0 CANDIDATE | PROJECT DICTIONARY + ALTERNATIVE-ROUTE PREEXEC

**Document ID:** `FOX2-POLICY-V1`  
**Version:** `1.9.0`  
**Status:** `CANDIDATE / OWNER-APPROVED CHAT-FIRST CHANGE / NOT RELEASED_EFFECTIVE`  
**Project:** `FOX2 ONLY`  
**Date:** 2026-10-14  
**Proposed predecessor:** `FOX2_POLICY_V1.8.9.md`  
**Machine-readable source registry:** `FOX2_PROJECT_DICTIONARY_v1.json`

> **Owner release direction 2026-10-14:** use one project-wide machine-readable Dictionary/Registry for FOX2 versions, identifiers, paths and compatibility; additionally, all FOX2 pre-execution readiness checks now use one durable project-wide evidence protocol. A local preflight failure must not disappear merely because an Agent was never launched.

## 1. Authority split

FOX2 now separates **machine identity** from **semantics**.

```text
PROJECT DICTIONARY
  -> current/legacy versions
  -> canonical paths
  -> control branches
  -> schema compatibility
  -> machine identifiers

POLICY / BRD / DATA CONTRACT / TECH SPEC
  -> meaning
  -> authority
  -> requirements
  -> safety semantics
  -> implementation semantics

CODE
  -> reads Dictionary or generated binding
  -> must not invent duplicated current identity constants
```

The Dictionary does not supersede semantic sources. If a Dictionary entry and an owning semantic source conflict in meaning, STOP and resolve the owning source; do not reinterpret semantics from JSON metadata.

## 2. Project Dictionary rule

For all new/re-scoped FOX2 work, CHAT first resolves:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`.

The Dictionary is the single machine-readable source of truth for:
- current Policy and Routing versions/paths;
- current Dispatch Schema and Git-first Protocol;
- active BRD/Technical/Data Contract/Acceptance identities;
- current and supported legacy dispatch schemas;
- current/supported control branches;
- canonical dispatch path conventions;
- accepted machine enums used by handoffs/runtime;
- generated runtime-binding targets.

A document may repeat an identifier for human readability, but executable code and handoff generators MUST NOT independently define competing "current" values.

## 3. Runtime binding rule

Runtime code that needs FOX2 governance/transport identifiers MUST either:

1. load the canonical Dictionary; or
2. import a generated binding produced solely from that Dictionary.

A generated binding must carry source Dictionary version/path and have a drift test.

Hand-written duplicate constants such as current dispatch schema version, current control branch, current dispatch directory or current Policy version are prohibited when they can be derived from the Dictionary.

This rule does not force business-domain runtime code to import governance metadata when it has no material need for it.

## 4. Coordinated source updates

Dictionary changes are classified:

- `IDENTITY_ONLY`: version/path pointer update, no semantic change;
- `COMPATIBILITY_EXPANSION`: add supported schema/path/tool compatibility; affected Technical Spec/tests must update;
- `SEMANTIC_SOURCE_CHANGE`: meaning/authority changes; owning Policy/BRD/Contract/Technical source must change through its normal process.

Do not bump business BRDs merely because a machine pointer changes.

Released documents remain immutable historical evidence; new bindings/addenda or newer revisions supersede them prospectively.

## 5. FOX2 operating model

```text
Owner
  -> CHAT resolves Project Dictionary
  -> CHAT decides/decomposes/binds exact WP
  -> up to two independent implementation lanes
       -> Copilot CLI
       -> Codex CLI
  -> optional Local Bridge transport/supervision
  -> selected Agent implements/tests
  -> authorized delivery owner publishes exact non-main result
  -> CHAT independently reads back and accepts/reworks
```

CHAT remains routing/source-binding/acceptance authority.

Bridge remains transport/supervision, not a second governance engine.

## 6. Whole-WP continuity

Bounded WPs continue through implementation/test/evidence/publication without repeated Owner confirmation unless a material input changes.

Operational reconciliation is not a new WP.

A systemic defect affecting shared infrastructure, registry binding, generator, adapter, ledger, permission path or evidence pipeline is fixed once in the current dependency-safe batch.

## 7. Executable handoff baseline

Every new/re-scoped executable handoff binds:
- Project Dictionary identity;
- exact Policy/Task/Prompt/Source identities;
- Agent Product + model policy/tier/model/reasoning;
- permission profile;
- execution path;
- delivery owner;
- worktree/branch/base;
- allowed code/report paths;
- Git permissions;
- required tests/capabilities;
- STOP conditions;
- `max_runs=1`.

The current Dispatch Schema is resolved from the Dictionary rather than named independently by implementations.

## 8. CLI-FIRST and permission baseline

Codex CLI and Copilot CLI are primary implementation engines.

Normal coding permission remains:

`permission_profile = FULL_ACCESS`.

CHAT selects the permission profile. Execution layers apply it exactly or fail closed.

Canonical semantics remain:
- Codex Full Access = danger-full-access + approval never semantics;
- Copilot Full Access = allow-all tools/paths/URLs semantics.

Full Access is technical execution permission only. It creates no main/merge/deploy/Production/provider/broker/LIVE authority.

## 9. Dispatch-owned Git delivery

```text
git_code_push=YES + delivery_owner=AGENT
=> selected Agent publishes exact authorized non-main task branch

git_code_push=YES + delivery_owner=BRIDGE
=> Bridge publishes exact authorized non-main task scope

git_code_push=NO
=> no code-result publication
```

CHAT always performs independent immutable remote readback.

No duplicate publication path.

## 10. Material Tool Compatibility

```text
VERSION_MATCH != READINESS

REQUIRED_CAPABILITIES_SUFFICIENT
+ REQUIRED_TESTS_PASS
+ TASK_SEMANTICS_CORRECT
= READY
```

Dictionary version identity is used for compatibility lookup, not as a substitute for task-material capability validation.

Non-material version deviation is recorded and continues. Missing material capability blocks. Unknown material capability holds.

## 11. Bridge compatibility boundary

Bridge supports only dispatch/control/path identities declared supported by the Dictionary.

Supported external dispatch schemas MUST normalize into one internal validated execution representation. Do not maintain one execution engine per schema.

Bridge MUST NOT:
- accept arbitrary control branches;
- infer current schema/path from filenames;
- silently convert unsupported schemas;
- change Agent/model/tier/reasoning/permission/delivery owner;
- rerun CHAT governance;
- blind replay;
- substitute Agent;
- merge/deploy or grant Production/provider/broker/LIVE authority.

## 12. Project-wide pre-execution evidence protocol

This rule applies to **all new or re-scoped executable FOX2 work**, regardless of whether the later execution path is Bridge, manual local CLI or VS Code one-click.

Before CHAT publishes an executable Dispatch or finalizes the selected implementation Agent, the task must have a durable pre-execution receipt conforming to the Dictionary-resolved Preflight Receipt Schema.

Canonical states:

```text
PREEXEC PASS
  -> durable sanitized receipt
  -> CHAT remote readback
  -> R3/R5 may close
  -> assignment may become final
  -> executable Dispatch may be published

PREEXEC BLOCKED
  -> durable sanitized receipt when Git publication is technically safe
  -> CHAT remote readback
  -> no executable Dispatch
  -> no Agent implementation run
  -> dispatch_consumed = NO
  -> resolve the material blocker without creating a micro-WP

PREEXEC INFRA_FAILED
  -> publish a sanitized failure receipt when a safe Git publication path exists
  -> otherwise emit an explicit local infrastructure failure
  -> never claim PUSHED unless remote readback succeeded
```

Project-wide invariants:

- preflight evidence is **not** an Agent result and MUST NOT use Agent Result Schema merely to reuse a container;
- preflight failure before executable dispatch publication does not consume a dispatch and does not trigger post-start replay semantics;
- a preflight tool must preserve the first material failure state while still attempting safe evidence publication;
- failure receipts contain sanitized classifications and bounded evidence only; secrets, raw tokens, credential-bearing URLs and unrestricted CLI output are prohibited;
- generated textual receipts use canonical UTF-8/LF and must pass the shared hygiene gate;
- stale state may be auto-cleaned only when objectively proven to belong solely to the current preflight receipt; unrelated WIP remains fail-closed;
- a tool MUST NOT print or return a success marker such as `PUSHED` until commit, push and remote readback have all succeeded;
- missing material capability remains `BLOCKED`; unknown material capability remains `HOLD`;
- Agent candidates are alternative execution routes unless the immutable task explicitly pins one Agent as materially required;
- individual candidate probes are routing evidence and are NON_MATERIAL by default when another allowed route can satisfy the task;
- project Agent readiness is represented by one MATERIAL aggregate capability such as `eligible_agent_route`;
- `eligible_agent_route=PASS` requires at least one CHAT-allowed candidate to prove current execution readiness with the bound permission/model policy;
- failure of a preferred candidate does not block when another allowed route passes; CHAT still performs the final route selection and no execution layer may silently substitute the Agent;
- if a task explicitly requires one specific Agent/tool for correctness, that pinned candidate becomes MATERIAL and its failure blocks.
- project-wide preflight semantics are defined by the Dictionary-resolved `FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.md` and machine receipt schema.

This protocol is a shared FOX2 execution invariant. Individual WPs may add material capability checks but MUST NOT weaken or replace it with task-local semantics.

## 13. Post-start failure

After Agent start, quota/auth/capacity/non-zero uncertainty remains:

```text
NEEDS_RECONCILIATION
dispatch consumed
no blind replay
no automatic Agent substitution
```

## 14. Source transition

New/re-scoped WPs use the current Dictionary and sources it resolves.

In-flight WPs are not automatically invalidated by a newer Dictionary/source release. Rebind only when the change is material to that WP.

## 15. Parallel writers

`MAX_PARALLEL_MATERIAL_WRITERS` is resolved from the Dictionary and currently equals 2.

Parallel lanes require dependency safety, distinct branches/worktrees and non-overlapping writable paths.

## 16. Non-effects

This release creates no blanket DEV, PR, main push, merge, deploy, Production/provider write, broker write or LIVE authority.

It does not change BRD-00/06/08 business semantics, Market Data Contract v0.4 semantics or M1 acceptance semantics merely by introducing the Dictionary.

## 17. Release acceptance

For new/re-scoped FOX2 work:
- Project Dictionary is resolved first;
- no competing hard-coded current identity constants;
- generated/runtime bindings must prove dictionary drift detection;
- current dispatch/control/path identity comes from Dictionary;
- supported legacy dispatches normalize into one execution path;
- Policy/BRD/Contract semantics remain in their owning documents;
- CLI-first, Full Access default, dispatch-owned Git delivery and capability-based readiness remain active;
- whole-WP continuity remains preferred over micro-fix fragmentation;
- every new/re-scoped executable WP has a Dictionary-resolved durable pre-execution receipt before final assignment/dispatch;
- BLOCKED pre-execution evidence is remotely readable when safe publication is possible and never masquerades as an Agent result or consumed dispatch.

`FOX2_POLICY_V1_8_9_STATUS=RELEASED_EFFECTIVE / PROJECT_DICTIONARY=V1.2 / PREEXEC_EVIDENCE=PROJECT_WIDE / AGENT_ROUTE_MATERIALITY=AGGREGATE / CLI_FIRST=YES / FULL_ACCESS_DEFAULT=YES / GIT_DELIVERY=DISPATCH_OWNED / IDENTITY_SOURCE=SINGLE_REGISTRY`


## 13. CHAT-FIRST execution authority — proposed prospective change (Owner direction 2026-10-17)

- CHAT is the default **direct actor** for FOX2. When the requested result can be executed with present tools, existing grants, source protection and verified destination readback, CHAT completes it. Reporting a plan, delegating to WORK, generating a CODEX prompt or suggesting Work is **not** completion when direct execution was feasible.
- CHAT MUST inspect task-state/source gates and decide `DIRECT_CHAT`, `CHAT_PARTIAL_THEN_DELEGATE`, `CODEX`, `COPILOT`, or `WORK_INDEPENDENT_AUDIT` with explicit reasons. Complexity, time, file count or need to inspect many documents are not reasons for handoff by themselves.
- Owner grants CHAT a standing bounded governance execution mandate for non-main **candidate** preparation, Git documentation writes and remote readback when path/write permissions and conflict checks permit. The mandate does not grant canonical release, source promotion, main merge, LIVE or expansion of protected rights. CHAT may perform authorized publication only after independent source/approval/manifest verification.
- CHAT performs source verification, BRD/spec drafting, governance impact assessment, Dictionary reference comparisons, status/roadmap analysis, Git/Library readback, report intake and safe task-state reconciliation directly whenever supported. Do not assign WORK for routine Git/Library reading; WORK is an independent assurance boundary or required capability unavailable to CHAT.
- CODEX/COPILOT are used for actual implementation host/build/runtime tests not executable through CHAT; do not split a whole WP into trivial handoff fragments. Do not route merely because a specialist exists.
- PreExec PASS/BLOCKED/INFRA_FAILED, durable receipts and R3/R5 apply **before Agent executable assignments**. They are not a requirement to fabricate an Agent probe/Dispatch for direct CHAT read-only analysis, drafting or authorized document Git writes. Direct CHAT writes require their own operation-specific rights, source and destination safety/readback gates.
- Preserve pinned Agent/model, single writer, no replay and every immutable in-flight source binding. CHAT must not self-certify EFFECTIVE, modify the grant that governs itself, bypass material authority conflicts or silently reclassify a protected release as routine work.
- Follow release lifecycle: Candidate -> authorized source verification -> manifest/digest + authority + supersession -> publication + independent readback -> EFFECTIVE; pending steps retain proper explicit states.

`CHAT_FIRST_POLICY_CHANGE=CANDIDATE / DIRECT_EXECUTION=DEFAULT / OWNER_STANDING_CANDIDATE_SCOPE=YES / UNVERIFIED_RELEASE=HOLD / MAIN=NO / MERGE=NO / LIVE=NO`

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
