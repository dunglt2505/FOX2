# Bridge Git Delivery — native implementation result, 2026-10-23

Logical task: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. Status: **PUSHED_UNREVIEWED / HOST_E2E_NOT_RUN**. No new work package.

## Source and publication

- Design: draft PR #25, `a1b4c522fe65c8450ab6c90c8e8a504b742b3e67`; BRD-09 REV4 R36–R47 and acceptance table §16.4 T32–T45; Tech Spec v0.7 REV11 §28.
- Main inspected: `0da03b052c6a63d560e830c7956a2625c0bfe843`. Read all eleven three-layer FOX2 Skills from its 0.5.5 package. Installed plugin cache remains 0.5.3; no plugin/runtime adoption claimed.
- Implementation inspection started at `63669296d67f7135a3a7e1d032ebd441cb84d285`. Isolated local snapshot tree matched remote exactly: `6ea51903b57ce869647495929405d2000c4094e5`.
- Concurrent candidate changes through `b11bf27d673ccc85515b7de54dae74ef6dbf65cc` were inspected and retained. Final code commit: `62477cbd66653cbe98a3e2adfd4d1b21919a2182`, parent b11bf27, on `work/FOX2-BRIDGE-GIT-DELIVERY-INTEGRATED-20261023`.
- Exact tested/published `agent_bridge` subtree: `922db7077737f47d03537f475ffbc70520dec37a`. Local validation commit `45b56891b5f945d3db58fd1a9c95554f4b6d753c` has this identical subtree; its root documentation ancestry differs from the GitHub result commit.
- Publication owner for this native continuation: CODEX, via the connected GitHub publisher because local GitHub CLI authentication was invalid and direct Git network transport unavailable. This does not establish installed Bridge credentials.
- Intermediate native branch commit ba6d5ff is superseded by the integrated result. PR #26 contains the integrated result and keeps the original candidate branch and R5 untouched.

## Implemented behavior

1. Bridge success publication requires trusted host test evidence for every declared required test, bound to the exact staged Git tree. Missing, failed, stale, malformed or interrupted verification blocks commit/push. Tests that change the index, tracked bytes, untracked outputs, branch or HEAD invalidate the gate. The committed tree is checked again before push.
2. Restart publication checks durable test evidence against the exact committed tree before any resumed push. AGENT-owned result handback also checks required tests; Bridge does not issue its push.
3. WIP accepts the UUID execution identity actually emitted by the runner. Recovery manifest paths must satisfy the original report allowlist. A resumed WIP commit must have the original parent and exact granted change set.
4. Preserve the concurrent explicit worktree-root and exclusive-writer checks. Recheck source authority, child quiescence and writer lease immediately before WIP push. Lost proof preserves the durable intent and local files.
5. Read staged/committed blobs with an explicit Git revision separator, avoiding Windows filesystem guessing for long virtual commit:path names.
6. Retain existing explicit BRIDGE draft default, AGENT opt-in, staged secret/path/mode guards, separate WIP ref/index, remote SHA readback, durable ledger-v6 intent and no-replay behavior.

The verifier is a trusted host composition interface, not executable commands or PASS values accepted from Dispatch JSON or Agent stdout. The default without a bound verifier fails closed for required tests.

## Observed validation

| Session | Observed result | Source/scope |
|---|---|---|
| Final focused integration | 235 passed, exit 0 | CODEX/Copilot fake adapters; BRIDGE/AGENT; real local bare remotes; result/WIP tests, ledger, Desktop, E2E and batch fixtures before final writer/root delta |
| Full native Windows regression, short-path clone | 774 passed, exit 0 | Full suite started from the pre-final guard snapshot; unchanged evidence reused. It is not a one-shot full-suite claim on the final guard delta. |
| Final guard regression | 85 passed, exit 0 | Exact final agent_bridge subtree above; test_git_wip_checkpoint, test_git_test_gate, test_git_delivery and test_lock_logging_health |
| Syntax/diff | Passed | Python compile and git diff --check |

Negatives include missing/failed/stale tests, test timeout, mutation during tests, Agent stdout impersonating test proof, wrong remote working directory, UUID mismatch, manifest scope, secrets, missing/false writer or quiescence callbacks, revoked lease, root escape, interrupted push/readback, immutable intent and no replay.

An earlier full run in the long chat directory returned 657 passed / 51 failed / 66 errors, including Windows MAX_PATH failures, the missing fixture verifier and a stale schema-5 health assertion. The fixture and health contract were corrected, then the short-path full run above passed. No failure was relabeled PASS.

These are native source/fixture tests. Fake Agent labels in Git integration are not real installed CODEX/Copilot runs, and test callbacks are not host authority attestations.

## R5 and host boundary

Remote R5 result remains `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`; prior scoped code acceptance and observed usage-limit exit remain historical evidence. Its original worktree was inspected clean. No old task/prompt/source/Policy/Dispatch was rewritten or replayed.

Installed pointer readback remains A04 package `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`, source inventory `6d76f99ce9fcc62bbcf9f2450a45bc920c28b2fd70828353c0a8fea096c5de73`. A read-only control snapshot observed STOPPED, paused=true, setup_complete=true, no current dispatch. Later cross-root R5 ledger inspection did not yield a stable usable snapshot; its attempts are not new admission evidence. A WPF process exists, so no complete no-writer attestation is inferred from that control snapshot.

**Remaining concrete blockers:** installed machine Policy/Dictionary/validator and CLI capability binding; installed Git credential/ref rights; trusted required-test plan/verifier binding; separately source-authorized recovery ref; independent Windows process-tree quiescence and exclusive writer lease. The existing opt-in WIP publisher is not an installed automatic recovery trigger until the real supervisor binds and enforces these inputs. None was invented or supplied as PASS.

Next safe action: use fresh read-only installed-host source/capability and ledger reconciliation, bind the real supervisor/test/recovery interfaces, then execute new authorized non-main normal and interrupted CODEX/Copilot attempts under the same logical task. Preserve consumed R5, local WIP and accepted unaffected evidence.

No main update, PR merge, runtime rollout, installed-host E2E, provider/broker operation or LIVE claim.
