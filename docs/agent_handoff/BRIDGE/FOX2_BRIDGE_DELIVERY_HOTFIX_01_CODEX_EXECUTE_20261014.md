# FOX2 Bridge Delivery Hotfix 01 — Codex CLI Execution

**WP:** `FOX2-BRIDGE-DELIVERY-HOTFIX-01`
**Date:** 2026-10-14
**Status:** `EXECUTABLE / TASK-BOUND DEV / STOP_AT_PUSHED_UNREVIEWED`

## 0. Objective

Fix the confirmed post-Agent Git delivery defects exposed by `FOX2-M1-P2-03-CODEX-001` so FOX2 can continue using the Bridge/Codex CLI path safely without wasting a successful Agent run.

The incident proved:
- Codex exited 0 and produced the required delivery marker;
- Bridge staged authorized WIP;
- `git diff --cached --check` rejected CRLF report evidence because `reports/** -text` preserves CRLF;
- useful Git diagnostics were emitted on stdout, but the Bridge error wrapper surfaced only stderr, producing `Git workspace command failed: `;
- recovery correctly preserved WIP and avoided a second expensive Codex run.

Do not reimplement governance or desktop/tray productization in this hotfix.

## 1. Immutable source/base

Repository: `dunglt2505/FOX2`

Task branch:
`work/FOX2-BRIDGE-DELIVERY-HOTFIX-01-codex`

Base:
`398bebf9c48e7694c69c3416a5780715f025e7b5`

Base is the currently proven Bridge Relay MVP source used for Codex/Copilot CLI E2E.

Preferred worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRIDGE-DELIVERY-HOTFIX-01-CODEX`

Before mutation verify:
- remote task branch still equals the exact base SHA;
- exact target branch is not attached to another worktree;
- target worktree is absent or clean and owned by this task;
- no competing writer is modifying `agent_bridge/**`.

If any materially conflicts, STOP without modifying other worktrees.

## 2. Exact writable scope

Writable:
- `agent_bridge/src/fox2_agent_bridge/**`
- `agent_bridge/tests/**`

Everything else is read-only.

Do not modify:
- FOX2 product backend/frontend;
- docs/governance/BRDs/specs;
- reports;
- control dispatch files;
- .gitattributes;
- provider/broker/LIVE code;
- main.

No package installation.

## 3. Required fix A — CRLF-aware staged whitespace gate

The Bridge must **not mutate Agent result/evidence bytes solely to make Git whitespace validation pass**. In particular it must not normalize report files after the Agent has sealed hashes.

Replace the current generic staged diff check with a Bridge-owned whitespace check that:
- treats CR at EOL as a line terminator, not trailing whitespace;
- still rejects true trailing spaces/tabs and standard Git whitespace errors;
- works for both unstaged tracked diff and staged diff;
- is deterministic on Windows.

Use Git's whitespace configuration or an equivalent safe Git-native mechanism. A preferred form is functionally equivalent to:

`git -c core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol diff [--cached] --check`

Do not weaken path scope, acceptance verification, secret boundaries or actual whitespace checks.

Tests must prove:
1. a report file containing only normal CRLF line endings passes the staged check;
2. a CRLF line containing an actual trailing blank still fails;
3. normal LF behavior remains unchanged.

## 4. Required fix B — bounded sanitized stdout + stderr diagnostics

When a Git command returns non-zero, Bridge diagnostics must include useful bounded sanitized content from **both stdout and stderr**.

Requirements:
- preserve existing redaction;
- never leak credential-bearing remote URLs, Authorization values or secret-like context;
- clearly identify stdout/stderr only when present;
- bounded message size;
- if stderr is empty and stdout contains a Git diagnostic, the error must no longer be blank.

Add a regression test reproducing a non-zero Git command with stdout-only diagnostics and verify the message contains the sanitized stdout.

## 5. Required fix C — post-Agent delivery failure is recoverable, not rerunnable

After a selected Agent exits successfully but Bridge fails during result verification/staging/commit/push, Bridge must distinguish **Agent execution success** from **Git delivery failure**.

Required behavior:
- preserve the worktree/WIP/index;
- persist a terminal/non-auto-rerunnable state such as `DELIVERY_RECOVERY_REQUIRED`;
- persist exact dispatch ID, dispatch path, branch, worktree, base/before HEAD, Agent product/exit code and sanitized delivery error;
- explicitly record that Agent relaunch is not authorized by recovery;
- normal `run-next` must continue to skip this dispatch because it already has durable state;
- no automatic Agent rerun.

Do not create a generic auto-retry loop.

## 6. Required fix D — explicit delivery-only recovery command

Provide an explicit CLI recovery path for a delivery failure without launching an Agent again.

Recommended UX:

`fox2-bridge recover-delivery --dispatch-path <exact immutable dispatch path>`

Equivalent naming is acceptable if clear and tested.

Recovery must:
1. start Bridge normally and acquire the same process/single-instance protection;
2. locate durable dispatch/execution state and require a recoverable post-Agent delivery condition;
3. reread the exact immutable dispatch from configured control Git;
4. verify dispatch identity/payload consistency with persisted state;
5. verify exact existing worktree/branch and local HEAD still equal the pre-Agent/base head expected for Bridge-owned Git delivery;
6. verify remote task branch still equals the expected pre-delivery head, unless remote already contains the exact verified result;
7. preserve existing WIP and staged content; never reset/clean/stash/rebase;
8. recompute changed paths from the current worktree/index;
9. enforce exact dispatch allowlists and required result paths;
10. use the **persisted successful Agent stdout** for stdout-marker acceptance when the original dispatch requires it;
11. run the new CRLF-aware Git whitespace checks;
12. commit/push only the authorized task branch;
13. remote-readback the exact resulting SHA;
14. update ledger/runtime result to `PUSHED_UNREVIEWED` (or an explicit recovered equivalent whose meaning is identical for CHAT review);
15. never call Codex/Copilot adapter during recovery.

If the task branch changed remotely, local HEAD changed, WIP is out of scope, acceptance evidence is missing, immutable dispatch differs, or recovery cannot prove safety, STOP and preserve WIP.

Do not try to repair arbitrary implementation/test failures in recovery.

## 7. Compatibility

Preserve:
- current dispatch schema v0.6;
- existing successful Codex/Copilot direct execution routes;
- `run-next` CODEX-only auto-select policy;
- replay/single-use behavior;
- current no-main/no-merge/no-provider/no-broker/no-LIVE boundaries;
- existing runtime report compatibility where possible.

A ledger schema bump is allowed only if actually required and must have migration tests. Prefer using existing flexible state/result fields if sufficient.

## 8. Required tests

At minimum add regression tests for:

1. staged CRLF-only report content passes;
2. staged CRLF + true trailing whitespace fails;
3. stdout-only Git failure diagnostic is visible;
4. stdout/stderr diagnostic is redacted/bounded;
5. Codex exit 0 + delivery Git failure persists recoverable delivery state rather than generic rerunnable failure;
6. recover-delivery does not invoke Agent adapter;
7. recovery rejects dispatch/payload mismatch;
8. recovery rejects local HEAD/remote branch drift;
9. recovery rejects out-of-scope WIP;
10. recovery successfully commits/pushes existing authorized WIP and verifies remote SHA;
11. successful normal Codex delivery still works;
12. replay/run-next does not reselect a delivery-recovery-required dispatch;
13. existing Bridge test suite passes.

Use offline/local Git fixtures only. No provider/broker/network service calls other than test Git remotes contained in temporary fixtures.

## 9. Validation

Run:
- focused tests for changed modules;
- full `agent_bridge/tests` suite;
- syntax/import checks as relevant;
- `git diff --check`;
- staged path scope check.

Do not create result report files for this hotfix; this deliberate choice avoids relying on the exact report-line-ending path being repaired.

## 10. Git ownership

Codex:
- edits/tests only;
- MUST NOT run `git add`, `git commit`, `git push`, merge or PR.

Bridge:
- verifies changed paths;
- commits/pushes the task branch after Codex returns the marker.

No main merge.

## 11. Required final response

Summarize:
- exact files changed;
- tests run/results;
- whether CRLF-only / actual trailing-whitespace regressions pass;
- whether stdout+stderr error diagnostics pass;
- whether delivery-recovery state and explicit recovery CLI pass;
- whether recovery proves no Agent relaunch;
- any limitations.

End with exactly:

`FOX2_BRIDGE_DELIVERY_HOTFIX_01_READY`
