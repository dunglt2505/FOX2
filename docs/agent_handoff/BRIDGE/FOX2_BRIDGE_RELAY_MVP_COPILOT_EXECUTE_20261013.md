# FOX2 — BRIDGE_RELAY_MVP — COPILOT WHOLE-WP EXECUTION

**Project:** FOX2  
**WP_ID:** `FOX2-BRIDGE-RELAY-MVP`  
**Execution class:** `AUTHORIZED_MATERIAL_DEV / BOOTSTRAP_PATH`  
**Agent:** GitHub Copilot  
**Owner decision:** 2026-10-13 — “Tốt, triển khai đi” after approving the simplified Bridge plan.  
**Assignment model:** ONE whole-WP assignment. Internal BRG labels are evidence checkpoints only; do not stop after each label unless a genuine STOP condition occurs.

## 1. Current released authority

Policy:
- `FOX2_POLICY_V1.8.5.md`
- Library SHA-256: `351a1eb39b32894f522c0302e7af6f793c7a0a8b2f365ff82a5d169d974819e2`
- Git source commit: `772a7e137c4257e46cf2ae14680a72324eb07dec`
- Git path: `docs/governance/FOX2_POLICY_V1.8.5.md`
- Git blob: `5b38b6bd6776b5ef3a771ba2297f4565c2d9abed`

Routing:
- `FOX2_AGENT_PROMPT_POLICY_V1_2_6_EFFECTIVE_ROUTING_INDEX_20261013.md`
- Library SHA-256: `bd9d66962782f552646a0ab93a5f121ca9d1fcff74d965495d3ce88dd001aa20`
- Git source commit: `772a7e137c4257e46cf2ae14680a72324eb07dec`
- Git path: `docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_6_EFFECTIVE_ROUTING_INDEX_20261013.md`
- Git blob: `263966d1c5e0eb3900a73c2f1327312f2cf94ec9`

Bridge Technical:
- `FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.6.md`
- Library SHA-256: `d49a5e05c045dd2cfec85f3a49dc3fb1ecd221bacc3a6f3835fc19a83d0af190`
- Git source commit: `772a7e137c4257e46cf2ae14680a72324eb07dec`
- Git path: `docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.6.md`
- Git blob: `ad4f118f6d32408d3e39c2e71fafc81b4f571956`

Bridge source baseline:
- branch: `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`
- immutable base: `58efb364098b69e1723dcf2097bb1b77192e7415`
- source subtree: `agent_bridge/**`
- prior result: 60 tests PASS on imported sanitized baseline.

## 2. Git/worktree ownership

Create or reuse only the dedicated Bridge MVP worktree:

`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RELAY-MVP-COPILOT`

Task branch:

`work/FOX2-BRIDGE-RELAY-MVP-copilot`

Base SHA:

`58efb364098b69e1723dcf2097bb1b77192e7415`

Do not use the Owner main workspace as implementation worktree.

Allowed code paths:

- `agent_bridge/**`

Allowed result paths:

- `reports/FOX2-BRIDGE-RELAY-MVP/report.md`
- `reports/FOX2-BRIDGE-RELAY-MVP/evidence_manifest.json`
- `reports/FOX2-BRIDGE-RELAY-MVP/evidence/**`

Permissions for this WP:

```text
CODE_ALLOWED = YES
GIT_CODE_PUSH = YES
GIT_REPORT_WRITE = YES
GIT_REPORT_PUSH = YES
PR_CREATE = NO
MERGE_ALLOWED = NO
PROVIDER_PRODUCTION = NO
BROKER_WRITE = NO
LIVE = NO
```

No direct main push. No force push. No merge.

## 3. Objective

Implement the smallest practical **Bridge Relay MVP**:

```text
CHAT Git dispatch
  -> Bridge receives immutable task
  -> correct isolated FOX2 worktree/workspace
  -> selected local Agent: Copilot or Codex
  -> Agent performs bounded task/test
  -> Agent may push its own authorized non-main branch
  -> Bridge records observable execution/result pointers
  -> CHAT remote readback/review
```

Bridge is transport/launcher only.

Do NOT add:
- semantic result review;
- CHAT review receipt writer;
- GitHub Issue review queue;
- auto-rework;
- auto-merge/deploy;
- Production/broker/LIVE;
- a second governance engine.

## 4. Reuse first

Before editing:
1. inspect the existing `agent_bridge/**` baseline;
2. identify what BRG-010/020 behavior already exists and reuse it;
3. do not recreate working core/poller/ledger/logging components;
4. preserve existing passing tests unless a behavior must change under v0.6.

Internal old BRG numbers may be noted only as traceability.

## 5. First action — one small integration pilot

Before building more framework, run one bounded technical pilot.

### 5.1 Discover actual supported integration surfaces

Inspect factual current capabilities only:

- `code --help`
- Copilot CLI help/subcommands
- Codex CLI help/subcommands
- installed VS Code/Copilot/Codex integration points
- official supported API/command documentation if directly available

Do not infer that an external CLI/SDK-created session is the exact already-open VS Code Agent session.

Record:

`VS_CODE_EXISTING_SESSION_INJECTION = VERIFIED | UNVERIFIED | UNSUPPORTED`

### 5.2 Preferred path order

Use the first supported path that works:

A. stable supported direct VS Code/Agent integration targeting exact workspace/session;
B. workspace-bound Copilot/Codex CLI session;
C. one-click VS Code handoff prepared by Bridge.

Path C is acceptable for bootstrap. Failure of A is not a reason to build a new framework.

### 5.3 Harmless pilot task

Create a dedicated temporary pilot worktree/branch under the authorized Bridge MVP test scope or a clearly isolated FOX2 pilot branch.

The pilot must prove:

1. Bridge receives one immutable Git task;
2. Bridge resolves/opens the exact isolated worktree/workspace;
3. Copilot OR Codex receives the exact test prompt;
4. Agent makes one harmless test-only change;
5. one small test runs;
6. one authorized non-main commit/result is produced;
7. Bridge captures observable status/test/commit/result identity;
8. no main/merge/Production/LIVE action occurs.

If one-click handoff is required, stop only at the user-click boundary and provide one precise action. Do not redesign the architecture.

## 6. Implement only the missing Relay MVP pieces

Required runtime component set:

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

Requirements:
- exact FOX2 repo/control source;
- immutable dispatch identity;
- single-use/replay-safe claim;
- correct workspace/worktree resolution;
- minimum runtime material checks only;
- no duplicate Policy/R0-R7/assignment evaluation;
- no silent Agent/model/mode substitution;
- model/mode/quota `NOT_EXPOSED` is not a generic blocker;
- launch/supervise Agent through a supported path;
- capture sanitized execution state;
- preserve restart/replay safety.

## 7. Two-lane behavior

Target:

`MAX_ACTIVE_AGENT_EXECUTIONS = 2`

Prove with two harmless independent tasks when technically ready:

- one Copilot lane;
- one Codex lane;
- separate dispatch IDs;
- separate worktrees;
- separate branches;
- non-overlapping writable paths.

A block/failure in one lane must not stop the other safe lane.

Do not share one mutable worktree.

## 8. Tests

Keep all existing tests green.

Add focused tests for:
- immutable envelope validation;
- replay/conflict;
- workspace resolution;
- material-vs-nonmaterial runtime facts;
- Copilot adapter supported-path selection;
- Codex adapter supported-path selection;
- one-click fallback;
- no duplicate governance;
- process/result state;
- two independent active lanes;
- collision blocks only the conflicting lane;
- restart does not replay completed dispatch.

Use local fixtures/temp repos where possible.

## 9. Result delivery

Before final push:
- run the full `agent_bridge` test suite;
- run compile/static checks already used by the project;
- run `git diff --check`;
- inspect actual staged paths;
- scan for secrets/private paths;
- ensure all staged paths are within allowed code/report paths.

Create:

`reports/FOX2-BRIDGE-RELAY-MVP/report.md`

and:

`reports/FOX2-BRIDGE-RELAY-MVP/evidence_manifest.json`

Commit and push only:

`work/FOX2-BRIDGE-RELAY-MVP-copilot`

Then independently read back the full remote SHA.

Maximum final execution state:

`PUSHED_UNREVIEWED`

Do not self-accept.

## 10. Genuine STOP conditions only

STOP for:
- material source/hash mismatch;
- actual worktree/writer collision;
- path outside authorized scope;
- required test failure that cannot be repaired in scope;
- secret/private material exposure;
- denied required Git/write access;
- selected Agent/integration path unavailable with no supported A/B/C path;
- unsafe process/runtime behavior.

Do NOT stop merely because:
- numeric quota percentage is not exposed;
- model/Optimize/Thinking is not exposed for transport-only steps;
- `C:\Projects\FOX2-AgentBridge` is not itself a Git worktree;
- review automation is not configured;
- direct injection into an already-open VS Code session is unavailable while one-click fallback works;
- an unrelated FOX2 lane is blocked.

## 11. Final return

Return:

```text
FOX2 BRIDGE_RELAY_MVP RESULT

SOURCE_READBACK:
WORKTREE:
BRANCH:
BASE_SHA:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:

VS_CODE_EXISTING_SESSION_INJECTION:
INTEGRATION_PATH_USED:
COPILOT_RELAY:
CODEX_RELAY:
MAX_ACTIVE_AGENT_EXECUTIONS:
DUAL_LANE_TEST:

FILES_CHANGED:
TESTS:
TEST_RESULT:
SECRET_SCAN:

RESULT_REPORT:
EVIDENCE_MANIFEST:
COMMIT:
PUSH:

EXECUTION_STATE:
  PUSHED_UNREVIEWED | BLOCKED | FAILED

OPEN_GATES:
STOP_REASON:
```

Stop after the whole MVP result. Do not start review automation or merge work.
