# FOX2 — Agent Usage Telemetry 01 — Roadmap Mapping v0.1 Candidate

**Work package:** `FOX2-AGENT-USAGE-TELEMETRY-01`  
**Status:** `CANDIDATE / QUEUED_AFTER_FIX_01 / NO_DEV_GRANT`  
**Date:** 2026-10-14  
**Source contract:** `FOX2_AGENT_USAGE_TELEMETRY_ROUTING_CONTRACT_v0.1_CANDIDATE.md`  
**Dependency:** `BRIDGE-DESKTOP-01-02-FIX-01 = PASS`

## Roadmap position

```text
BRIDGE-DESKTOP-01-02-FIX-01
        |
        | PASS
        v
FOX2-AGENT-USAGE-TELEMETRY-01
        |
        | PASS
        v
normal FOX2 Bridge operation / next eligible WP
```

This feature is intentionally separate from FIX-01. No corrective scope is expanded.

## Simple execution plan

### Step 1 — Runtime contract and adapters

Implement the immutable Agent configuration in Bridge:

- Copilot: `NATIVE_AUTO` + `auto_tier`;
- Codex: pinned `model` + `reasoning_effort`;
- no silent fallback/substitution;
- structured result fields for requested/observed configuration.

### Step 2 — Telemetry, persistence and CHAT read surface

Add:

- usage/quota extraction when officially exposed;
- ledger/result persistence;
- Codex five-hour reset normalization contract;
- status/read surface for CHAT and read-only Tray display;
- Copilot per-task runtime profile only after its canary passes.

### Step 3 — One end-to-end certification

Run focused tests/canaries proving:

- both Agents execute exact dispatch configuration;
- telemetry survives success and quota failure;
- no replay/substitution;
- Tray remains display-only;
- CHAT can use the persisted snapshot for the next routing decision.

If all acceptance criteria pass, CHAT may mark the feature ready for normal routing use.

## DEV dispatch gate

Do not publish the DEV dispatch until:

```text
BRIDGE-DESKTOP-01-02-FIX-01 = PASS
source contract = Owner-approved executable Candidate or released
exact base SHA = verified
one writer/worktree = reserved
allowed code/report paths = bound
```

Expected implementation scope:

```text
agent_bridge/**
reports/FOX2-AGENT-USAGE-TELEMETRY-01/**
```

No main/merge/deploy/provider/broker/LIVE.

`ROADMAP_MAPPING_STATUS=CANDIDATE / SIMPLE_3_STEP_PLAN / WAIT_FIX_01_PASS`.
