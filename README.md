# FOX2 — Vietnam Equities Investment Intelligence

Independent greenfield project for Vietnamese equity investment intelligence.

## Current project state — 2026-10-14

FOX2 is past bootstrap/foundation and is executing two consolidated lanes:

- **M1-A Application:** Foundation + SQLite Store + DSM + APP-BATCH-A backend integration are accepted; next target is APP-BATCH-B (UI + integrated offline acceptance) leading to a runnable localhost M1-A.
- **AgentBridge:** FIX-01 is accepted; Bridge Batch A is in same-WP Project Dictionary/Dispatch compatibility rework, followed by Batch B packaging/certification.

No broker order execution, margin, cash transfer or LIVE authority is implied.

## Machine-readable project source registry

The canonical current identity/compatibility registry is:

`docs/governance/FOX2_PROJECT_DICTIONARY_v1.json`

All new/re-scoped FOX2 handoffs and runtime tooling that need governance/transport identities resolve them from that Dictionary or a generated binding derived only from it.

The Dictionary owns machine identity such as:
- current Policy/Routing/Protocol/Dispatch source;
- active BRD/Technical/Data Contract/Acceptance paths;
- dispatch schema compatibility;
- control branches;
- dispatch path conventions;
- execution identifier enums.

It does **not** own business meaning. Policy/BRDs/Data Contracts/Technical Specs remain semantic authority.

## Current governance

Resolve exact versions from the Dictionary. At this baseline:
- Policy V1.8.7;
- Routing Index V1.2.8;
- Dispatch Schema v3;
- Git-first Protocol v10;
- Result Contract v2;
- CHAT Intake v9.

Current dispatch transport:

```text
control branch = work/FOX2-DISPATCH-chat
path           = docs/agent_handoff/DISPATCH/<dispatch_id>.json
```

Version is carried in payload/Dictionary, not directory name.

## BRD / technical authority

Released BRD-00/06/08 and Market Data Contract v0.4 remain immutable semantic sources. Machine identity updates do not rewrite them.

Use:
- `docs/brd_mirror/FOX2_BRD_PROJECT_DICTIONARY_BINDING_v1.md`;
- `docs/architecture/FOX2_M1_TECHNICAL_SPEC_REGISTRY_BINDING_v1.md`;
- active Bridge/Usage Candidate specs resolved from the Dictionary.

## Safety boundary

No source-binding, Dictionary entry, technical permission profile or task publication by itself grants main push, PR creation, merge, deploy, provider Production access, broker write or LIVE.
