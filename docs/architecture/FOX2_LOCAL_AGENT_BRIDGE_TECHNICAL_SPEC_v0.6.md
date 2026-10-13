# FOX2 — Local Agent Bridge Technical Specification v0.6

**Document ID:** `FOX2-LOCAL-AGENT-BRIDGE-SPEC`  
**Version:** `0.6`  
**Project:** `FOX2 ONLY`  
**Status:** `RELEASED_EFFECTIVE / SIMPLIFIED_RELAY_MVP`  
**Date:** 2026-10-13  
**Released predecessor:** `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.5.md`  
**Purpose:** simplify Bridge to its intended job: receive an already-approved FOX2 command, relay it to the selected local Agent in the correct workspace, and return execution evidence for CHAT review.

> **Owner release decision 2026-10-13:** “Tốt, triển khai đi”. Bridge is a transport/launcher. It is not a second governance engine, semantic reviewer, project scheduler or acceptance authority.

## 1. Target architecture

```text
CHAT
  -> Git dispatch
  -> Local Bridge
  -> correct FOX2 worktree / VS Code workspace
  -> selected Agent (Copilot or Codex)
  -> Agent implements/tests
  -> Agent pushes authorized non-main result
  -> CHAT independently reads back and reviews immutable result
```

## 2. Core Bridge responsibilities

### B1. Receive
Poll only the configured FOX2 control ref and discover immutable dispatch artifacts.

### B2. Verify transport identity
Verify project/repository/control ref, immutable dispatch commit/path/blob, payload/hash, dispatch identity and replay state.

Do not re-evaluate BRD, routing or Owner decisions already bound by CHAT.

### B3. Verify minimum runtime launch safety
Immediately before launch verify only runtime facts that can materially affect correct execution:

- selected Agent executable/integration path exists;
- exact target worktree/workspace is resolved;
- branch/base mapping is correct;
- no conflicting writer/WIP ownership exists;
- requested model/mode is available when the selected integration surface exposes and requires it;
- required local/Git access exists.

`NOT_EXPOSED` is not automatically a failure. It blocks only when material to launch correctness.

### B4. Relay and supervise
Launch or hand off the exact approved task to the selected Agent with the exact worktree/workspace, prompt and bounded configuration. Capture safe status, test/result pointers and process/hand-off outcome. No silent substitution.

### B5. Record single-use execution

```text
DISCOVERED -> CLAIMED -> RELAYED/RUNNING -> AGENT_EXITED | BLOCKED | FAILED
```

A claimed/completed dispatch must not relaunch automatically.

## 3. What Bridge does not own

Bridge does not own:

- Policy/BRD/R0-R7/Assignment re-evaluation;
- project decomposition or priority scheduling;
- semantic code/result review;
- CHAT acceptance receipt;
- auto-rework;
- auto-merge/deploy;
- provider/broker/LIVE decisions;
- GitHub Issue review queue as a prerequisite;
- turning every technical checkpoint into a separate WP;
- exclusive publication of task result commits.

When the task grant allows it, the coding Agent may commit/push only its own non-main task branch and authorized code/report paths. CHAT independently verifies the remote result.

## 4. Parallel execution

```text
MAX_ACTIVE_AGENT_EXECUTIONS = 2
```

The intended normal case is one Copilot lane plus one Codex lane when independent.

Each execution must have:

- distinct WP/dispatch ID;
- distinct worktree/workspace;
- distinct non-main branch;
- non-overlapping writable paths;
- explicit writer ownership.

A conflict blocks only the conflicting launch. The other safe lane continues.

## 5. Development source of truth

Bridge development source is the Git-backed FOX2 subtree:

```text
agent_bridge/**
```

The local directory:

```text
C:\Projects\FOX2-AgentBridge
```

is a runtime/install instance. It is not a second development source of truth.

New Bridge development changes should originate from Git-backed `agent_bridge/**` and then be installed/synced to the local runtime explicitly.

## 6. Minimal component model

Required core:

```text
DispatchPoller
DispatchEnvelopeValidator
ReplayGuard
RuntimeAttestor
WorkspaceResolver
AgentRelay
ExecutionLedger
```

AgentRelay may contain two small adapters:

```text
CopilotAdapter
CodexAdapter
```

No Bridge-core requirement for:

```text
semantic ResultInspector
Bridge-owned GitDeliveryVerifier
ReviewOutbox
ReviewEventEmitter
CHAT ReviewReceiptWriter
GitHub Issue Review Queue
```

Those may exist later as separate automation components if actually useful, but are not prerequisites for Bridge command relay.

## 7. VS Code / CLI integration model

### 7.1 What is already plausible

Copilot CLI can operate with workspace/editor context and may surface a session associated with VS Code. That is useful for handing a task into the correct workspace.

### 7.2 What is NOT yet proven

Do **not** assume that a session created externally by SDK/CLI is the same session as the Agent chat/session already open in VS Code.

The specific unresolved capability is:

```text
Can an external Bridge use a stable supported VS Code API to create/select the exact Copilot/Codex Agent session in the already-open VS Code workspace and submit the prompt programmatically?
```

Until this is demonstrated, mark:

```text
VS_CODE_EXISTING_SESSION_INJECTION = UNVERIFIED
```

### 7.3 Required technical pilot before more Bridge framework work

Run one small E2E pilot only. Do not build another framework around it.

```text
1. CHAT publishes one harmless test task to GitHub.
2. Bridge receives the task.
3. Bridge resolves/opens the exact isolated FOX2 worktree as the VS Code workspace.
4. Bridge selects Copilot or Codex and requested model/mode only when the supported UI/API exposes that control.
5. Agent makes one harmless test change in the isolated worktree.
6. Agent runs one small test.
7. Agent creates/pushes one authorized non-main test commit, or produces the exact commit-ready result if the integration surface cannot push directly.
8. Bridge captures observable status/result/test/commit identity.
9. CHAT reads back the remote immutable result.
```

Success answers the practical integration question. Failure should identify only the missing integration capability, not trigger new architecture layers.

### 7.4 Preferred integration order

Try in this order:

**Path A — supported direct integration**  
Use a documented/stable VS Code/Copilot/Codex API/command if it can target the exact workspace/session and provide observable status.

**Path B — workspace-bound CLI session**  
If direct existing-session injection is unavailable, start a supported CLI/Agent session bound to the exact worktree/workspace. Treat it as a distinct session even if VS Code displays it.

**Path C — one-click VS Code handoff**  
If no stable external session-creation API is available, Bridge prepares the exact workspace + prompt/task and exposes one clear action for the Owner to launch/send it in VS Code. After that click, Bridge may observe/result-track only through supported mechanisms.

Path C is acceptable for bootstrap. It is not a reason to redesign Bridge.

## 8. Model / mode handling

Bridge never invents capability.

```text
if integration surface exposes model/mode selection:
    select exact authorized value and verify when observable
else:
    record NOT_EXPOSED
    block only if exact selection is material to the Owner-approved task
```

For transport-only actions, model/mode/quota are `NOT_APPLICABLE`.

## 9. One macro implementation assignment

Replace the Owner-facing micro-sequence `BRG-010`, `020`, `030`, `040`, ... with one bounded macro assignment:

```text
BRIDGE_RELAY_MVP
```

Internal evidence checkpoints may retain old BRG labels for traceability, but Copilot continues through them without a new Owner handoff unless a genuine STOP occurs.

`BRIDGE_RELAY_MVP` contains only:

```text
existing core reuse
-> polling
-> immutable envelope validation/replay
-> workspace resolution
-> runtime attestation
-> Copilot/Codex relay
-> 2-lane isolation
-> small E2E pilot
```

Do not implement review automation, auto-rework or merge/deploy as part of this MVP.

## 10. Minimal dispatch envelope

```yaml
schema_version: <supported>
project: FOX2
dispatch_id: <unique>
wp_id: <exact>
repository: dunglt2505/FOX2
control_commit_sha: <immutable>
agent:
  product: COPILOT|CODEX
  requested_model_or_mode: <value-or-NOT_APPLICABLE>
execution_path: BRIDGE_DIRECT|VSCODE_ONE_CLICK
worktree: <exact>
branch: <exact non-main>
base_sha: <full SHA>
prompt:
  git_commit: <full SHA>
  path: <exact>
  sha256: <exact>
allowed_code_paths: [...]
allowed_report_paths: [...]
permissions:
  code_allowed: YES|NO
  git_code_push: YES|NO
  git_report_write: YES|NO
  git_report_push: YES|NO
  merge_allowed: NO
  production_provider: NO
  broker_write: NO
  live: NO
max_runs: 1
```

Bridge references immutable CHAT decision/source receipts; it does not semantically rerun them.

## 11. Material runtime blocks

Block only for material launch/transport problems:

- wrong project/repo/control artifact;
- immutable payload/hash mismatch;
- replay/conflicting dispatch;
- selected Agent/integration path unavailable;
- exact requested configuration unavailable when materially required;
- worktree/workspace/branch/base mismatch;
- writer/WIP collision;
- required Git permission unavailable;
- path ownership conflict;
- unsafe secret exposure.

Not generic blockers by themselves:

- `C:\Projects\FOX2-AgentBridge` lacking `.git`;
- numeric quota percentage not exposed;
- Optimize/Thinking not exposed for transport-only work;
- unrelated WP/gate blocked;
- review automation not configured;
- inability to inject into the already-open VS Code session when `VSCODE_ONE_CLICK` fallback is available.

## 12. MVP acceptance

Bridge Relay MVP is ready when:

1. GitHub test dispatch is discovered at immutable SHA;
2. replay protection works;
3. Bridge resolves the correct isolated worktree/workspace;
4. one Copilot task can be relayed successfully by a supported direct path or one-click VS Code handoff;
5. one Codex task can be relayed successfully by a supported direct path or one-click VS Code handoff;
6. model/mode selection is exact where supported and truthfully `NOT_EXPOSED` where not;
7. Agent makes a harmless change and runs a small test;
8. result/test/commit state is observable enough for CHAT remote readback;
9. two independent lanes can coexist without writer/path collision;
10. Bridge restart does not replay a completed dispatch;
11. no main/merge/Production/broker/LIVE authority is created.

## 13. Release transition

With v0.6 released:

- v0.5 remains historical evidence;
- reuse valid BRG-010/020 evidence instead of rebuilding it;
- stop treating internal BRG checkpoints as separate Owner assignments;
- stop requiring Bridge to own semantic review or exclusive result publication;
- treat VS Code existing-session injection as an optional integration optimization, not a prerequisite to relay MVP;
- keep direct supported automation as the target when technically proven; until then use one-click VS Code handoff.
