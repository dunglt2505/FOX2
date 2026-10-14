# FOX2 — Agent Usage Telemetry 01 — Roadmap Mapping v0.3 Candidate

**Work package:** `FOX2-AGENT-USAGE-TELEMETRY-01`  
**Status:** `CANDIDATE / ABSORBED_INTO_BRIDGE_DESKTOP_BATCH_A / NO_STANDALONE_DEV`  
**Date:** 2026-10-14  
**Source contract:** `FOX2_AGENT_USAGE_TELEMETRY_ROUTING_CONTRACT_v0.1_CANDIDATE.md`  
**Overall Bridge plan:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.7_CANDIDATE.md` REV4  
**Dependency:** `BRIDGE-DESKTOP-01-02-FIX-01 = PASS`

## Decision

`FOX2-AGENT-USAGE-TELEMETRY-01` remains a normative requirement contract, but it is **not** implemented as a separate DEV round.

Its runtime work is absorbed into the same Bridge Desktop batch that already touches:

- Worker;
- Agent adapters;
- execution supervisor;
- recovery/reconciliation;
- ledger/result persistence;
- local status surface;
- Tray.

This avoids reopening the same modules in multiple coding cycles.

## Overall Bridge execution plan

```text
BRIDGE-DESKTOP-01-02-FIX-01
    corrective only; frozen scope
              |
              | PASS + CHAT readback
              v
BRIDGE-DESKTOP-BATCH-A
CORE + ROUTING + USAGE + TRAY
              |
              | PASS
              v
BRIDGE-DESKTOP-BATCH-B
SETUP + PACKAGE + REAL FOX2 CERTIFICATION
              |
              | PASS
              v
INTERNAL FOX2 BRIDGE READY
              |
              v
BRIDGE-DESKTOP-05
standalone/community extraction later only
```

## Batch A — one implementation round

Batch A combines the remaining related work of historical Desktop-01, Desktop-02 and Agent Usage Telemetry:

- background Worker / Git mailbox loop;
- restart/reconciliation/no-replay;
- exact dual-Agent dispatch;
- CLI-FIRST execution baseline;
- CHAT-owned `permission_profile=FULL_ACCESS` default;
- Bridge `AGENT_PERMISSION_PREFLIGHT` and exact CLI permission application;
- fail-closed permission mismatch with no silent downgrade;
- Copilot Native Auto + CHAT-selected tier;
- Codex pinned model + reasoning;
- structured requested/observed result;
- usage/quota extraction when exposed;
- ledger persistence;
- post-start quota failure reconciliation;
- CHAT-readable status;
- Tray IPC/status/startup;
- Tray usage/model display-only;
- Copilot process-scoped profile canary;
- no silent substitution;
- Full Access permission enabled; Autopilot remains a separate CHAT-controlled execution mode.

### Batch A exit

One combined acceptance run must prove:

```text
WORKER_RECOVERY=PASS
CODEX_EXACT_CONFIG=PASS
COPILOT_EXACT_POLICY=PASS
USAGE_PERSISTENCE=PASS
POST_START_QUOTA_RECONCILIATION=PASS
NO_REPLAY=PASS
NO_AGENT_SUBSTITUTION=PASS
FULL_ACCESS_CODEX=PASS
FULL_ACCESS_COPILOT=PASS
PERMISSION_PREFLIGHT=PASS
NO_PERMISSION_DOWNGRADE=PASS
TRAY_READ_ONLY_USAGE_DISPLAY=PASS
```

Do not split these into separate Owner-facing DEV WPs unless a genuine technical blocker requires isolation.

## Batch B — one release-readiness round

Batch B combines historical Desktop-03 + Desktop-04:

- first-run setup;
- per-user installed runtime;
- installer/update/uninstall;
- sanitized diagnostics;
- one real eligible FOX2 WP executed through Bridge;
- non-main result push/readback;
- usage snapshot available to CHAT for the next routing cycle;
- restart confirms no replay.

### Batch B exit

```text
INSTALLABLE_INTERNAL_BUILD=PASS
REAL_FOX2_WP_E2E=PASS
CHAT_REMOTE_READBACK=PASS
NEXT_ROUTING_USAGE_AVAILABLE=PASS
RESTART_NO_REPLAY=PASS
```

## DEV gate

Do not publish Batch A until:

```text
BRIDGE-DESKTOP-01-02-FIX-01 = PASS
CHAT readback = PASS
v0.7 REV4 + Usage Contract REV2 = approved/bound
exact post-FIX base SHA = verified
one writer/worktree = reserved
allowed code/report paths = bound
```

Expected Batch A implementation scope:

```text
agent_bridge/**
reports/BRIDGE-DESKTOP-BATCH-A/**
```

Expected Batch B implementation scope is bound separately because packaging paths may differ.

No main/merge/deploy/provider/broker/LIVE.

## Planning rule

Keep the Bridge plan coarse-grained:

```text
FIX -> BATCH A -> BATCH B -> READY
```

Do not create separate implementation rounds for adapter model policy, usage telemetry, Tray usage display, ledger fields or Copilot profile handling when they can be changed and tested together inside Batch A.

`ROADMAP_MAPPING_STATUS=INTEGRATED / BASELINE=CLI_FIRST_FULL_ACCESS_DEFAULT / NO_STANDALONE_USAGE_DEV_ROUND`.
