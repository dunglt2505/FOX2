# FOX2 — BRIDGE_RELAY_MVP — COPILOT CLI EXECUTION V2

**Project:** FOX2  
**WP_ID:** `FOX2-BRIDGE-RELAY-MVP`  
**Agent endpoint:** GitHub Copilot CLI  
**Execution path:** `BRIDGE_DIRECT_COPILOT_CLI`  
**Owner correction:** 2026-10-13 — Bridge phải chuyển task qua **Copilot CLI**, không phụ thuộc vào session Copilot đang mở trong VS Code.

## 1. Core rule

Bridge launches Copilot CLI directly in the exact isolated worktree.

```text
CHAT Git dispatch
  -> Local Bridge
  -> resolve exact FOX2 worktree
  -> launch Copilot CLI programmatically in that cwd
  -> Copilot CLI edits/tests
  -> authorized task result
  -> CHAT remote readback/review
```

VS Code may be open and Copilot CLI may share editor/workspace context, but an existing VS Code Agent session is **not required** for this WP and is not an execution gate.

## 2. Current released authority

Use:
- FOX2 Policy V1.8.5
- Routing Index V1.2.6
- Bridge Technical Spec v0.6

Bridge source baseline:
- branch: `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`
- base: `58efb364098b69e1723dcf2097bb1b77192e7415`
- source: `agent_bridge/**`

Task branch:
- `work/FOX2-BRIDGE-RELAY-MVP-copilot`

Worktree:
- `C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RELAY-MVP-COPILOT`

Allowed code:
- `agent_bridge/**`

Allowed reports:
- `reports/FOX2-BRIDGE-RELAY-MVP/report.md`
- `reports/FOX2-BRIDGE-RELAY-MVP/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RELAY-MVP/evidence/**`

Permissions:
- code write/push on task branch: YES
- report write/push on task branch: YES
- main push: NO
- merge: NO
- Production/provider/broker/LIVE: NO

## 3. Copilot CLI integration

Use the actual installed Copilot CLI discovered by the Bridge runtime.

Do not depend on VS Code UI injection.

Before first launch:
1. resolve the actual Copilot executable;
2. run harmless `--version` / help capability discovery;
3. verify authentication status by supported means;
4. run from the exact target worktree as current working directory;
5. use Copilot CLI's supported programmatic prompt interface;
6. use the current installed CLI's actual supported flags only.

GitHub documents programmatic Copilot CLI invocation with a prompt flag (`-p` / `--prompt`). Use a non-interactive invocation suitable for automation. If the installed CLI supports `--no-ask-user`, silent/machine-readable output, model selection, and scoped tool/path permissions, use them where appropriate and record what was actually observed.

Do not invent unsupported flags.

## 4. Model/mode handling

No exact Copilot model has been Owner-pinned for this Bridge engineering WP.

Therefore:
- use the supported configured/default Copilot CLI model unless an exact task dispatch later pins one;
- if the CLI exposes the actual selected model, record it;
- if it does not, record `NOT_EXPOSED`;
- do not stop solely because numeric quota, Optimize, or a model label is not exposed.

No silent substitution is allowed when a future dispatch explicitly pins a model.

## 5. Implement the smallest Relay MVP

Reuse existing Bridge code. Add only what is missing:

```text
DispatchPoller
DispatchEnvelopeValidator
ReplayGuard
RuntimeAttestor
WorkspaceResolver
AgentRelay
ExecutionLedger
CopilotAdapter
CodexAdapter
```

For CopilotAdapter:
- launch Copilot CLI directly;
- cwd = exact task worktree;
- prompt = exact immutable task prompt;
- minimal required permissions;
- capture exit status/stdout/stderr safely;
- capture observable test/result/commit pointers;
- never inherit broad secrets unnecessarily.

Do not implement semantic review, Issue queue, review receipts, auto-rework, auto-merge or deployment.

## 6. Pilot

Before adding more framework, prove one harmless Copilot CLI relay:

1. Bridge receives immutable test dispatch;
2. exact isolated worktree resolved;
3. Bridge starts Copilot CLI programmatically in that worktree;
4. Copilot performs one harmless test-only change;
5. one small test runs;
6. authorized non-main result commit is produced/pushed if allowed;
7. Bridge records observable execution/test/result identity;
8. CHAT can read back the remote result.

The pilot does not require an existing VS Code session.

## 7. Dual Agent target

After Copilot CLI relay works, implement CodexAdapter similarly using the supported Codex CLI surface.

Target:
`MAX_ACTIVE_AGENT_EXECUTIONS = 2`

Prove one Copilot CLI lane and one Codex CLI lane can coexist in separate worktrees/branches with non-overlapping write scopes.

## 8. Genuine STOP only

STOP for material source/hash mismatch, writer collision, unauthorized path, required test failure not repairable in scope, secret exposure, denied required Git access, or actual Copilot CLI unavailability/auth failure.

Do NOT stop because:
- VS Code session injection is unavailable;
- no VS Code Agent session is open;
- model/Optimize/quota is not exposed when not pinned/material;
- review automation is absent;
- unrelated lane is blocked.

## 9. Delivery

Run full Bridge tests, compile/static checks, `git diff --check`, scope check and secret scan.

Create canonical result files under:
`reports/FOX2-BRIDGE-RELAY-MVP/**`

Commit/push only:
`work/FOX2-BRIDGE-RELAY-MVP-copilot`

Return maximum state:
`PUSHED_UNREVIEWED`

Do not self-accept.
