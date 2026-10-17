# FOX2 — Git-first Task/Result Protocol v12 — Project Dictionary First + Alternative Routes

**Status:** CURRENT FOR NEW/RE-SCOPED FOX2 WORK  
**Controlling authority:** Project Dictionary v1.2 -> Policy V1.8.9 -> Routing Index V1.3.0.  
**Supersedes:** Protocol v11 prospectively. Legacy immutable work retains its frozen source binding unless materially re-scoped.

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

`PROTOCOL_STATUS=V12_CURRENT / PROJECT_DICTIONARY=V1.2 / POLICY=V1.8.9 / ROUTING=V1.3.0 / PREEXEC_PROTOCOL=V1.1 / PREFLIGHT_RECEIPT=V1 / AGENT_ROUTE_MATERIALITY=AGGREGATE / DISPATCH_SCHEMA=V3 / STABLE_DISPATCH_PATH=YES`


## CHAT-FIRST execution — Owner-approved operating addendum (candidate, 2026-10-17)

For FOX2 task intake, CHAT is the default DIRECT EXECUTION OWNER. Before routing to WORK, CODEX or COPILOT, CHAT MUST test current actual tool availability, scope, authority, evidence and whether an independent auditor or execution host is materially required. CHAT directly completes every authorized and technically supported step, with exact readback and evidence. Multiple steps, document volume or project complexity alone do not justify delegation. If execution is partially possible, perform that portion directly and hand off ONLY the bounded residual work, explaining the material reason. WORK is not a routine proxy for CHAT source inspection, documentation editing, Git comparisons or reports. Agent prompting is not task completion when CHAT can execute.

This operating addendum preserves Dictionary-first source identity, pinned Agent/model/permission, project-wide PreExec before final Agent assignment, durable receipts, source lock, exact non-main Git grants, safety/release approval and no-replay. It grants no authority to self-certify EFFECTIVE, alter protected governance semantics without owning approval, merge, deploy or LIVE. The existing document's current release identity remains historical; this branch edit is a candidate revision pending governed publication.
