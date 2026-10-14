# FOX2 — Git-first Task/Result Protocol v10 — Project Dictionary First

**Status:** CURRENT FOR NEW/RE-SCOPED FOX2 WORK  
**Controlling authority:** Project Dictionary v1 -> Policy V1.8.7 -> Routing Index V1.2.8.  
**Supersedes:** Protocol v9 prospectively. Legacy immutable work retains its frozen source binding unless materially re-scoped.

## 1. Resolve current operating set

Do not hard-code the current Policy/Dispatch/Protocol set in handoff generators.

First read:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

Then resolve the current:
- Policy;
- Routing Index;
- Dispatch Schema;
- Result Contract;
- CHAT intake;
- BRDs/Technical/Data Contract/Acceptance sources relevant to the WP.

## 2. Stable dispatch transport identity

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

## 3. New dispatch contract

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

## 4. Dictionary vs semantics

Dictionary is machine identity/compatibility only.

Policy/BRD/Contract/Technical Spec remain semantic authority.

An Agent/Bridge must not use a Dictionary pointer to reinterpret BRD or safety meaning.

## 5. CLI-first execution

Codex CLI and Copilot CLI remain the primary implementation engines.

Normal coding permission is Dictionary-resolved and currently `FULL_ACCESS`.

No silent Agent/model/tier/reasoning/permission substitution.

## 6. Whole-WP continuity

One bounded WP proceeds through implementation/test/evidence/publication until genuine STOP or final delivery.

Operational state reconciliation is not a new WP.

A registry drift/systemic compatibility issue is corrected once at the shared binding/normalization layer.

## 7. Compatibility

Bridge supports only Dictionary-declared schemas/control branches/paths.

Supported external dispatch schemas normalize into one internal validated payload.

Do not maintain separate execution engines for v3/v2/v0.6.

Current schema must not require code changes merely because Policy version changes; Policy identity is validated by cross-checking the pinned Dictionary.

## 8. Git delivery

```text
git_code_push=YES + delivery_owner=AGENT
=> Agent publishes exact authorized non-main scope

git_code_push=YES + delivery_owner=BRIDGE
=> Bridge publishes exact authorized non-main scope

git_code_push=NO
=> no code-result publication
```

No duplicate publication path.

## 9. Runtime failure

Post-start non-zero/quota/auth/capacity uncertainty:
- `NEEDS_RECONCILIATION`;
- dispatch consumed;
- no blind replay;
- no automatic Agent substitution.

## 10. Result/evidence

Result Contract remains Dictionary-resolved.

Every material PASS must resolve to actual evidence.

Generated evidence follows canonical text/binary rules from applicable Technical Specs.

## 11. CHAT intake

CHAT independently remote-readbacks:
- Dictionary identity;
- Policy/task/prompt/source identities;
- exact remote SHA;
- changed paths;
- tests/evidence;
- delivery owner/publication path;
- compatibility/semantic source consistency.

Delivery is `PUSHED_UNREVIEWED` until CHAT acceptance.

## 12. Non-effects

Protocol v10 creates no main/PR/merge/deploy/Production/provider/broker/LIVE authority.

`PROTOCOL_STATUS=V10_CURRENT / PROJECT_DICTIONARY=V1 / POLICY=V1.8.7 / ROUTING=V1.2.8 / DISPATCH_SCHEMA=V3 / STABLE_DISPATCH_PATH=YES`
