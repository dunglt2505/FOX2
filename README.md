# FOX2 — Vietnam Equities Investment Intelligence

Independent greenfield project for Vietnamese equity investment intelligence.

## Current project state — 2026-10-14

FOX2 is past bootstrap/foundation and is executing two consolidated lanes:

- **M1-A Application:** Foundation + SQLite Store + DSM + APP-BATCH-A backend integration are accepted; next target is APP-BATCH-B (UI + integrated offline acceptance) leading to a runnable localhost M1-A.
- **AgentBridge:** Bridge Batch A is Owner-accepted at `3013f34...` with explicit post-patch validation waiver; Batch B packaging/certification is in pre-execution readiness.

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
- Policy V1.8.9;
- Routing Index V1.3.0;
- PreExec Evidence Protocol v1.1;
- Preflight Receipt Schema v1;
- CHAT Preflight Intake v1.1;
- Dispatch Schema v3;
- Git-first Protocol v12;
- Result Contract v2;
- CHAT Result Intake v9.

Current dispatch transport:

```text
control branch = work/FOX2-DISPATCH-chat
path           = docs/agent_handoff/DISPATCH/<dispatch_id>.json
```

Version is carried in payload/Dictionary, not directory name.

## Project-wide pre-execution evidence

All new/re-scoped executable FOX2 WPs must publish/read a durable preflight receipt before final Agent assignment and executable Dispatch publication.

```text
PASS         -> may proceed to final assignment/Dispatch
BLOCKED      -> durable sanitized Git evidence, no dispatch consumed
INFRA_FAILED -> durable evidence when safely publishable; otherwise explicit local infra failure
```

This is project orchestration infrastructure, not business semantics. Individual WPs add material capability checks to the common receipt instead of inventing separate state machines.

For alternative implementation Agents, FOX2 treats candidate probes as routing evidence and gates readiness on one material aggregate `eligible_agent_route`. Failure of Copilot does not block a task if Codex is an allowed route and passes, and vice versa. A task-pinned Agent remains individually material.

## BRD / technical authority

Released BRD-00/06/08 and Market Data Contract v0.4 remain immutable semantic sources. Machine identity updates do not rewrite them.

Use:
- `docs/brd_mirror/FOX2_BRD_PROJECT_DICTIONARY_BINDING_v1.md`;
- `docs/architecture/FOX2_M1_TECHNICAL_SPEC_REGISTRY_BINDING_v1.md`;
- active Bridge/Usage Candidate specs resolved from the Dictionary.

## Safety boundary

No source-binding, Dictionary entry, technical permission profile or task publication by itself grants main push, PR creation, merge, deploy, provider Production access, broker write or LIVE.
