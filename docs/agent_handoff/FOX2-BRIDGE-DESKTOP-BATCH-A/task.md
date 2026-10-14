# BRIDGE-DESKTOP-BATCH-A — Executable Task

**Status:** EXECUTABLE / WHOLE-WP / OWNER-AUTHORIZED
**Governance:** FOX2 Policy V1.8.6 + Routing Index V1.2.7
**Protocol:** Dispatch Schema v2 + Git-first Protocol v9
**Execution path:** MANUAL_LOCAL
**Delivery owner:** AGENT

## Source binding

- Accepted FIX-01 base: `ef9f290e73c4f4500900528656212c38acf43a4f`
- FIX-01 parent: `ceeb2bb2db3e09c2c2ad485a82a70c4f446e8e6a`
- Policy V1.8.6 source commit: `116c362b9c6243ebaa23ad17df3104d9f07c50d5`
- Routing V1.2.7 source commit: `c8474b059f372bb37cfe4989f44b92f346a7146d`
- Master plan: `cc7fa95ea7ff5613b3fdb33c26245834089050ca:docs/roadmap/FOX2_MASTER_EXECUTION_PLAN_20261014.md`
- Bridge Technical Spec active candidate: `cc7fa95ea7ff5613b3fdb33c26245834089050ca:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md` REV7
- Usage/CHAT Routing Contract active candidate: `cc7fa95ea7ff5613b3fdb33c26245834089050ca:docs/architecture/FOX2_AGENT_USAGE_TELEMETRY_ROUTING_CONTRACT_v0.1_CANDIDATE.md` REV4
- Source authority is CHAT-verified. Agent MUST NOT redo governance/source-release discovery.

## Role / Agent

- Role: Bridge core/product-control implementation Agent
- Agent: CODEX CLI
- Model policy: PINNED
- Model: `gpt-6.1-sol`
- Reasoning: `high`
- Permission profile: `FULL_ACCESS`
- Git delivery: Agent-owned exact task branch

High reasoning is selected because this batch contains recovery/replay/concurrency/permission semantics.

## Whole-WP objective

Complete the remaining related Bridge core/product-control work in ONE implementation round. Do not create standalone coding rounds for telemetry, model routing, Full Access, permission preflight, Tray usage display, artifact hygiene or Copilot profile handling.

Implement/test together:

1. background Worker + Git durable mailbox behavior;
2. pause/resume/check-now, bounded backoff, single-instance and restart reconciliation;
3. exact CODEX/COPILOT adapter registry and immutable execution tuple;
4. CODEX pinned model + reasoning;
5. COPILOT Native Auto + CHAT-selected tier;
6. FULL_ACCESS default and permission preflight;
7. fail-closed permission mismatch; no silent permission downgrade;
8. capability-based Material Tool Compatibility Rule;
9. requested/observed execution configuration + usage/capacity telemetry persistence;
10. post-start quota/auth/capacity -> NEEDS_RECONCILIATION;
11. no blind replay and no automatic Agent substitution;
12. dispatch-owned Git delivery semantics; no duplicate publication path;
13. Tray IPC/status/startup and read-only usage/model/permission display;
14. canonical generated-text artifact pipeline;
15. one combined final acceptance/evidence cycle.

## Writable scope

Allowed:
- `agent_bridge/**`
- `reports/BRIDGE-DESKTOP-BATCH-A/**`

Everything else READ-ONLY.

Do not modify Policy/BRD/business application/backend/frontend/provider/broker code.

## Permission contract

Normal coding profile:
`FULL_ACCESS`

CODEX intent:
- sandbox = `danger-full-access`
- approval policy = `never`

COPILOT Full Access intent:
- allow-all semantics for dispatch-required tools/paths/URLs.

Full Access is technical permission only. It does NOT grant main/merge/deploy/Production/provider/broker/LIVE authority.

If an exact requested permission profile cannot be applied, fail before Agent execution. Never silently downgrade.

## Tool compatibility

Do not gate on version string equality.

Continue when required task capabilities are available and validation passes. Record non-material version deviations.

Block/hold only if a material required capability is missing/unknown.

## Canonical artifact pipeline

Generated textual Bridge evidence (JSON/XML/TXT/MD/LOG/CSV where applicable):
- UTF-8;
- LF;
- no trailing whitespace;
- deterministic serialization where practical;
- final newline where applicable;
- shared helper/path rather than per-file fixes;
- post-generation hygiene check;
- final `git diff --check`.

Byte-preservation/binary evidence follows its own contract.

## Required acceptance

At minimum:
- WORKER_RECOVERY=PASS
- CODEX_EXACT_CONFIG=PASS
- COPILOT_EXACT_POLICY=PASS
- USAGE_PERSISTENCE=PASS
- POST_START_QUOTA_RECONCILIATION=PASS
- NO_REPLAY=PASS
- NO_AGENT_SUBSTITUTION=PASS
- GIT_DELIVERY_POLICY_ALIGNED=PASS
- NO_DUPLICATE_PUBLICATION_PATH=PASS
- FULL_ACCESS_CODEX=PASS
- FULL_ACCESS_COPILOT=PASS
- PERMISSION_PREFLIGHT=PASS
- MATERIAL_TOOL_COMPATIBILITY=PASS
- NON_MATERIAL_VERSION_MISMATCH_CONTINUES=PASS
- MATERIAL_CAPABILITY_MISSING_BLOCKS=PASS
- CANONICAL_GENERATED_ARTIFACT_PIPELINE=PASS
- TEXT_ARTIFACT_HYGIENE=PASS
- TRAY_READ_ONLY_USAGE_DISPLAY=PASS
- FULL_BRIDGE_TESTS=PASS
- SECRET_SCAN=PASS
- CHANGED_PATH_ALLOWLIST=PASS
- GIT_DIFF_CHECK=PASS

Use local/fake CLI fixtures where paid real Agent invocation is not necessary. Do not fabricate observed quota/model fields.

## Git authority

`git_code_push=YES`, `delivery_owner=AGENT`.

Agent may stage/commit/push exact allowed task branch after validation.

No PR/main/merge/deploy/provider/broker/LIVE.

## STOP

Stop only for material:
- wrong branch/base/task;
- overlapping writer on `agent_bridge/**`;
- required Full Access cannot be applied;
- required capability missing;
- required test/security failure;
- out-of-scope code needed;
- actual quota/capacity prevents execution;
- secret exposure;
- push/readback failure.

Operational Git-index cleanup, non-material version mismatch and evidence regeneration are not new WPs.

## Delivery

Create:
- `reports/BRIDGE-DESKTOP-BATCH-A/report.md`
- `reports/BRIDGE-DESKTOP-BATCH-A/evidence_manifest.json`
- material evidence under `reports/BRIDGE-DESKTOP-BATCH-A/evidence/**`

Then commit/push exact branch and return:
`FOX2_BRIDGE_DESKTOP_BATCH_A_PUSHED_UNREVIEWED`
