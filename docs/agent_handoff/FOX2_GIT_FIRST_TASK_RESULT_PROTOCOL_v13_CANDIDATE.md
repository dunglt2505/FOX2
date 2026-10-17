# FOX2 — Git-first Task/Result Protocol v13 CANDIDATE — Project Dictionary First + Alternative Routes

**Status:** CANDIDATE / NOT CURRENT UNTIL GOVERNED RELEASE  
**Controlling authority:** Project Dictionary v1.3 CANDIDATE -> Policy V1.9.0 CANDIDATE -> Routing Index V1.4.0 CANDIDATE.  
**Proposed supersession:** Protocol v12 prospectively, only after release. Legacy immutable work retains its frozen source binding unless materially re-scoped.

## 1. Resolve current operating set

Do not hard-code the current Policy/Dispatch/Protocol set in handoff generators.

First read:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

Then resolve the current:
- Policy;
- Routing Index;
- PreExec Evidence Protocol;
- Preflight Receipt Schema;
- CHAT Preflight Intake;
- Dispatch Schema;
- Result Contract;
- CHAT Result Intake;
- BRDs/Technical/Data Contract/Acceptance sources relevant to the WP.

## 2. Project-wide pre-execution phase

No new/re-scoped executable FOX2 WP skips directly from source-ready to Dispatch.

Required sequence:

```text
SOURCE_READY
 -> bind material preflight requirements
 -> run project-wide preflight
 -> publish/read durable Preflight Receipt
 -> CHAT Preflight Intake
 -> PASS_TO_ASSIGN
 -> final assignment
 -> executable Dispatch publication
```

For `BLOCKED`, no executable Dispatch exists, no implementation Agent starts and `dispatch_consumed=NO`.

For `INFRA_FAILED`, publish a sanitized receipt when Git publication itself remains safe; otherwise surface explicit local infrastructure failure.

The current contracts are Dictionary-resolved and include:
- `FOX2_PREEXEC_EVIDENCE_PROTOCOL_v1.1.md`;
- `FOX2_PREFLIGHT_RECEIPT_SCHEMA_v1.json`;
- `FOX2_CHAT_PREFLIGHT_INTAKE_CHECKLIST_v1.1.md`.

A Preflight Receipt is not an Agent Result.

## 3. Alternative Agent route evidence

For a WP that allows more than one implementation Agent, preflight evaluates candidate routes as alternatives.

- individual Copilot/Codex probes are routing evidence and normally NON_MATERIAL;
- `eligible_agent_route` is the MATERIAL aggregate readiness capability;
- aggregate PASS requires at least one allowed candidate PASS;
- candidate failure remains visible to CHAT for cost/capability comparison;
- no runner/Bridge may select or substitute the Agent automatically;
- CHAT finalizes one route after Intake;
- if the immutable task pins one specific Agent as materially required, that candidate itself is MATERIAL and aggregate alternatives cannot override it.

## 4. Stable dispatch transport identity

New current dispatches use the Dictionary-resolved control branch and canonical path.

At this release:

```text
control branch:
work/FOX2-DISPATCH-chat

dispatch path:
docs/agent_handoff/DISPATCH/<dispatch_id>.json
```

The folder name intentionally does not include the schema version.

Schema identity belongs in the payload and Dictionary.

Legacy path/control identities remain supported only according to the Dictionary compatibility map.

## 5. New dispatch contract

New/re-scoped WPs use the Dictionary-resolved current Dispatch Schema, currently v3.

Dispatch v3 additionally binds the exact Dictionary identity:

```json
"dictionary": {
  "version": "...",
  "git_path": "docs/governance/FOX2_PROJECT_DICTIONARY_v1.json",
  "git_commit_sha": "<full SHA>",
  "sha256": "<sha256>"
}
```

The dispatch also binds Policy, Task, Prompt, Source, routing tuple, execution path, delivery owner, permissions, runtime contract, tests and STOP conditions.

Bridge validates those values against the pinned Dictionary; it does not independently decide what the current identifiers should be.

## 6. Dictionary vs semantics

Dictionary is machine identity/compatibility only.

Policy/BRD/Contract/Technical Spec remain semantic authority.

An Agent/Bridge must not use a Dictionary pointer to reinterpret BRD or safety meaning.

## 7. CLI-first execution

Codex CLI and Copilot CLI remain the primary implementation engines.

Normal coding permission is Dictionary-resolved and currently `FULL_ACCESS`.

No silent Agent/model/tier/reasoning/permission substitution.

## 8. Whole-WP continuity

One bounded WP proceeds through implementation/test/evidence/publication until genuine STOP or final delivery.

Operational state reconciliation is not a new WP.

A registry drift/systemic compatibility issue is corrected once at the shared binding/normalization layer.

## 9. Compatibility

Bridge supports only Dictionary-declared schemas/control branches/paths.

Supported external dispatch schemas normalize into one internal validated payload.

Do not maintain separate execution engines for v3/v2/v0.6.

Current schema must not require code changes merely because Policy version changes; Policy identity is validated by cross-checking the pinned Dictionary.

## 10. Git delivery

```text
git_code_push=YES + delivery_owner=AGENT
=> Agent publishes exact authorized non-main scope

git_code_push=YES + delivery_owner=BRIDGE
=> Bridge publishes exact authorized non-main scope

git_code_push=NO
=> no code-result publication
```

No duplicate publication path.

## 11. Runtime failure

Post-start non-zero/quota/auth/capacity uncertainty:
- `NEEDS_RECONCILIATION`;
- dispatch consumed;
- no blind replay;
- no automatic Agent substitution.

## 12. Result/evidence

Result Contract remains Dictionary-resolved.

Every material PASS must resolve to actual evidence.

Generated evidence follows canonical text/binary rules from applicable Technical Specs.

## 13. CHAT result intake

CHAT independently remote-readbacks:
- Dictionary identity;
- Policy/task/prompt/source identities;
- exact remote SHA;
- changed paths;
- tests/evidence;
- delivery owner/publication path;
- compatibility/semantic source consistency.

Delivery is `PUSHED_UNREVIEWED` until CHAT acceptance.

## 14. Non-effects

Protocol v11 creates no main/PR/merge/deploy/Production/provider/broker/LIVE authority.

`PROTOCOL_STATUS=V13_CANDIDATE / PROJECT_DICTIONARY=V1.2 / POLICY=V1.8.9 / ROUTING=V1.3.0 / PREEXEC_PROTOCOL=V1.1 / PREFLIGHT_RECEIPT=V1 / AGENT_ROUTE_MATERIALITY=AGGREGATE / DISPATCH_SCHEMA=V3 / STABLE_DISPATCH_PATH=YES`


## 15. CHAT direct execution path — candidate

For supported authorized read-only, document drafting, Git/Library candidate edit, and evidence reconciliation, CHAT executes the requested operation directly and independently reads back destination bytes. It emits a direct-work evidence record (operation, allowed path, before/after blob or digest, exact branch/commit, source status, conflicts and completion verdict), **not** an Agent Result or invented PreExec Receipt. Only actual implementation delegated to an Agent enters PreExec -> Dispatch -> Agent Result -> CHAT Intake. For mixed tasks, finish CHAT-supported operations first and dispatch only the material residual portion. Preserve existing frozen WP/dispatch identities, no replay and protected release rights. No candidate protocol changes the runtime contract until governed promotion.

`PROTOCOL_V13=CANDIDATE / DIRECT_CHAT_WORK=YES_WHEN_AUTHORIZED / AGENT_PROTOCOL=UNCHANGED_UNTIL_RELEASE`

## Git latest-at-execution — Phase A prospective candidate integration

Status: CANDIDATE_NOT_EFFECTIVE. Applies prospectively only after the required authority and compatibility gates; this amendment grants no runtime/DEV, merge, release or LIVE permission.

1. **Historical references remain valid.** Old version numbers in BRDs, Policy, Specs, Protocols, templates and reports are historical references, not execution pins. Do not rewrite them in bulk merely because a newer version exists.
2. **Refresh live Git before every execution.** At CHAT direct actionable admission, Agent PreExec and dequeue before first claim, automatically contact authenticated GitHub at the authorized Registry location; read current Registry, manifests, publication and supersession metadata and newly published versions. Record observation time, Registry ref/commit and all relevant candidates. If the trusted Registry location or live access is unavailable, record SOURCE_UNVERIFIED / AUTHORITY_UNVERIFIED / GIT_UNAVAILABLE and HOLD dependent execution; cache or Library must never silently substitute.
3. **Choose newest applicable.** Evaluate scope, owning authority, release approval, compatibility and target environment; distinguish LATEST_GIT_OBSERVED from LATEST_APPLICABLE. Record selected and rejected versions with reasons. A newer unqualified version is LATEST_PRESENT_BUT_BLOCKED and goes through the applicable gate; do not silently promote it or downgrade to the version in authored text. A qualified older source requires an explicit, evidenced applicability decision under the gate.
4. **Lock before claim/effect.** Recheck material Registry/source-head drift immediately before first claim or side effect. Drift invalidates affected stale PreExec/routing and requires permitted revalidation before start. Freeze repository, Registry and manifest commits, source path/commit, Git blob and SHA-256 of exact bytes, scope/compatibility verdict and approval evidence into the attempt source lock. Refresh/lock is not a release approval.
5. **Preserve running Dispatches.** Consumed/started Dispatches retain their original immutable source locks; no hot-swap, mutation or automatic replay. Newer sources affect subsequent work or explicit governed stop/reconciliation. Queued unstarted work refreshes and rebinds only before claim, within existing permissions.

Evidence must distinguish REFRESH_PASS, APPLICABILITY_PASS, RELEASE_AUTHORITY_PASS, EXECUTION_PASS and EFFECTIVE_RELEASE_PASS. Static document verification proves none of the runtime or release claims. CHAT result intake compares actual execution to its frozen lock; live discovery for follow-up does not retroactively rebind that execution.

Normative candidate detail: `docs/governance/FOX2_GIT_LATEST_AT_EXECUTION_CONTRACT_v1_CANDIDATE.md`. Source commit/hash must be resolved at execution; this path/reference is not proof that this Candidate is EFFECTIVE.
