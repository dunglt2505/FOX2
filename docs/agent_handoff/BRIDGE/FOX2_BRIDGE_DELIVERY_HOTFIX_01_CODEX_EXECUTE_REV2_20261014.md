# FOX2 Bridge Delivery Hotfix 01 — Codex CLI Execution REV2

**WP:** `FOX2-BRIDGE-DELIVERY-HOTFIX-01`
**Dispatch generation:** replacement after dispatch 001 preflight-only block
**Date:** 2026-10-14
**Status:** `EXECUTABLE / TASK-BOUND DEV / STOP_AT_PUSHED_UNREVIEWED`

## 0. Why REV2 exists

Dispatch `FOX2-BRIDGE-DELIVERY-HOTFIX-01-CODEX-001` launched Codex successfully but Codex stopped before mutation because the prompt incorrectly required two host-level preflight checks from inside the Codex sandbox:

- remote Git connectivity check, which failed through the sandbox proxy;
- Windows process inspection via `Get-CimInstance`, which was denied.

Those checks are not Agent implementation responsibilities.

For REV2:
- CHAT/Bridge own remote source/branch and writer-preflight responsibility;
- Codex owns only exact-worktree local validation, implementation and tests;
- Codex MUST NOT call remote Git or inspect the host process table.

## 1. Exact source / branch / worktree

Repository: `dunglt2505/FOX2`

Branch:
`work/FOX2-BRIDGE-DELIVERY-HOTFIX-01-codex`

Base SHA:
`398bebf9c48e7694c69c3416a5780715f025e7b5`

Worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DELIVERY-HOTFIX-01-CODEX`

CHAT has independently verified the remote task branch still equals the exact base SHA before publishing this replacement dispatch.

## 2. Local preflight only

Before editing, verify only:

- current working directory is the exact worktree above;
- current branch is `work/FOX2-BRIDGE-DELIVERY-HOTFIX-01-codex`;
- local HEAD is exactly `398bebf9c48e7694c69c3416a5780715f025e7b5`;
- local worktree/index is clean.

Allowed local Git examples:
- `git rev-parse HEAD`
- `git branch --show-current`
- `git status --short`

Do **not** run:
- `git ls-remote`
- `git fetch`
- `git pull`
- `git push`
- any remote Git command
- `Get-CimInstance`
- `Get-Process` for competing-writer discovery
- WMI/CIM/process-table inspection.

If local branch/HEAD/status fails the exact checks, STOP without mutation and end with:

`FOX2_BRIDGE_DELIVERY_HOTFIX_01_BLOCKED`

Do **not** print the success marker when blocked.

## 3. Writable scope

Writable:
- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`

Read-only:
- all FOX2 product code;
- docs;
- reports;
- .gitattributes;
- provider/broker/LIVE paths;
- main.

No package installation.

## 4. Fix A — CRLF-aware whitespace validation

Current post-Agent delivery uses Git diff whitespace checks that falsely reject normal CRLF lines in report/evidence files where `reports/** -text` preserves bytes.

Implement Bridge-owned Git whitespace checking so:
- normal CRLF EOL is accepted;
- actual trailing spaces/tabs are still rejected;
- LF behavior remains unchanged;
- both unstaged and staged checks use the safe behavior;
- result/evidence bytes are **not mutated merely to satisfy the check**.

Prefer Git-native behavior equivalent to:

`git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff [--cached] --check`

or an equally safe deterministic approach.

Regression tests:
1. CRLF-only staged text passes;
2. CRLF + real trailing blank fails;
3. LF + real trailing blank still fails.

## 5. Fix B — useful sanitized Git diagnostics

For non-zero Git commands, error text must include bounded sanitized content from both stdout and stderr.

Requirements:
- existing redaction preserved;
- credential-bearing URLs/tokens/private values must not leak;
- stdout-only diagnostic must produce a non-empty useful message;
- stdout/stderr labels only when useful;
- bounded total message size.

Regression tests:
- non-zero Git command with stdout-only diagnostic is surfaced;
- stderr-only diagnostic works;
- combined stdout+stderr is bounded/redacted.

## 6. Fix C — post-Agent delivery failure is a recovery state

When Agent execution has succeeded but Bridge later fails while validating/staging/committing/pushing:

- preserve WIP/index/worktree;
- persist a distinct terminal/non-auto-rerunnable delivery-recovery state;
- persist enough exact context to recover delivery safely;
- normal `run-next` must not reselect/relaunch the Agent;
- do not create an automatic Agent retry loop.

Reuse current ledger/result fields where sufficient. Bump schema only if truly necessary.

Regression test must prove:
- Agent exit 0 + delivery failure => delivery-recovery-required;
- subsequent normal queue selection does not launch the Agent again.

## 7. Fix D — explicit delivery-only recovery CLI

Add an explicit recovery path, preferably:

`fox2-bridge recover-delivery --dispatch-path <exact immutable dispatch path>`

Equivalent clear CLI naming is acceptable.

Recovery must:
- never invoke Codex/Copilot adapter;
- reread exact immutable dispatch through existing Bridge transport;
- verify persisted dispatch identity/payload consistency;
- verify exact local worktree/branch/HEAD and remote task branch using **Bridge runtime**, not Agent sandbox;
- preserve WIP/index; never reset/clean/stash/rebase;
- recompute changed paths;
- enforce dispatch code/report allowlists;
- enforce required result paths and original persisted successful Agent stdout marker;
- run the new CRLF-aware whitespace checks;
- commit/push only the authorized task branch;
- verify exact remote result SHA;
- finish as `PUSHED_UNREVIEWED` or explicit recovered equivalent with the same review semantics.

STOP safely if source/head/branch/scope/dispatch changed.

Regression tests must prove:
- recovery does not invoke Agent;
- mismatch/drift/out-of-scope cases fail closed;
- valid existing WIP is committed/pushed once and remote SHA is verified.

## 8. Compatibility

Preserve:
- dispatch schema v0.6;
- existing Codex/Copilot direct routes;
- current CODEX-only normal `run-next` auto-selection;
- replay/single-use semantics;
- no main/merge/Production/provider/broker/LIVE authority.

Do not refactor unrelated Bridge code.

## 9. Tests

Run at minimum:
- focused changed-module tests;
- full `agent_bridge/tests`;
- syntax/import checks as relevant;
- `git diff --check` for your own source changes;
- changed-path scope check.

Tests must be local/offline. Do not require GitHub connectivity from Codex.

No result report files are required for this hotfix.

## 10. Git ownership

Codex:
- edits/tests only;
- MUST NOT run `git add`, `git commit`, `git push`.

Bridge:
- validates result;
- commits/pushes authorized task branch after Codex returns success.

## 11. Final response contract

If implementation is actually complete and tests pass, summarize:
- changed files;
- test commands/results;
- CRLF regression result;
- stdout+stderr diagnostic result;
- delivery-recovery state result;
- recover-delivery result;
- proof recovery does not call Agent;
- limitations.

Then end with exactly:

`FOX2_BRIDGE_DELIVERY_HOTFIX_01_READY`

If blocked before implementation or required tests fail, do **not** print that marker. End instead with:

`FOX2_BRIDGE_DELIVERY_HOTFIX_01_BLOCKED`
