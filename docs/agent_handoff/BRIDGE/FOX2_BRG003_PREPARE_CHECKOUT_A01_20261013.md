# FOX2 — BRG-003 / Phase A: PREPARE_CHECKOUT (non-DEV)
Date: 2026-10-13 · Task ref: BRG-003-PREPARE-A01 · Status: OWNER_CONTINUE_SCOPE_RECORDED / CONDITIONAL_NON_DEV_PREPARATION / NO_CODE_GRANT

## Authority and scope

On 2026-10-13, Owner replied **"làm tiếp nha"** to CHAT's immediately preceding plan: **the next action is a separately bounded PREPARE_CHECKOUT**, prior to any Bridge source import. Interpret this contextual direction only for **preparing/checking an isolated Git checkout**, not as the previously missing whole-BRG-003 DEV grant. CHAT may coordinate and publish this bounded preparation task, subject to actual actor, source, rights and workspace checks. Any later material DEV requires a separate, explicit task-scoped authorization.

POLICY_CHECK: FOX2 Policy V1.8.2 RELEASED_EFFECTIVE; Agent Prompt Routing Index V1.2.2 effective derivative; Bridge Technical v0.4 RELEASED_EFFECTIVE (CHAT Library governance + architecture inventory exhausted to next_cursor=null on 2026-10-13). Recipient does not falsely claim direct Library access. Release conflict -> BLOCKED_SOURCE_VERSION.

Immutable Git source:
- Repository: `dunglt2505/FOX2`, private.
- **Exact base commit (not main nor mutable branch tip):** `c8a0d517b8655868053e4923f5947c12975a5865` (remote verified, not yet local).
- Fetchable source reference: `refs/heads/work/FOX2-BRG-003-MANIFEST-RECOVERY-chat-20261013`; before fetch confirm it still contains required base commit.
- Policy Git blob: `0783c024d19f96a0b87ab770dad80bab449fa21f`.
- Agent Prompt Routing Index Git blob: `7d697a8db00a0ebbbb6eb68285fbf5ed2eade5ab`.
- Bridge Spec v0.4 Git blob: `e74402d294c713a07a08b2c4e68b6caafbe2ad48`.
- Original 20-file SHA256 baseline: `docs/agent_handoff/BRIDGE/FOX2_BRG003_20FILE_HASH_RECONCILIATION_20261013.json`, blob `3ef8852964214c99161ed9ff4e463cb677af51cd`. Copilot independently rechecked 20/20 local files on 2026-10-13 (13:32–13:36 ICT). No inventory or security test repetition needed unless an actual delta is observed.

## Agent route and execution classification

- Role: Windows checkout preparer / source-readback collector
- Candidate: COPILOT in VS Code, cheapest eligible actual mode when observed. **Do not invent an engine/model, optimize setting, or numeric quota.**
- Quota source: `NOT_EXPOSED` if UI/provider offers no accessible numerical quota. This is NOT a quota PASS or a grant for material implementation.
- This handoff is **Phase A non-DEV Git metadata-only preparation**, not material implementation. If the actually usable Copilot session/model/permission cannot be observed sufficiently even for bounded preparation, or paywall/quota prevents operating, STOP and report `PREPARE_BLOCKED_AGENT_ELIGIBILITY`. Never assert a fabricated premium model/credit balance.
- Compare: CHAT can verify remote Git/document source but cannot operate the Owner's Windows worktree; COPILOT is the observed Windows host inspector, lower cost than new CODEX/WORK review; CODEX keeps existing sessions untouched; WORK not needed for mechanical preparation. No authorization to run other agents.
- `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `GIT_REPORT_PUSH=NO`, `PR_CREATE=NO`, `MERGE_ALLOWED=NO`, `LIVE=NO`.

## Exclusive target and operation limits

- Current FOX2 root: `C:\Projects\FOX2`; must remain unchanged, no destructive reset/checkout/clean/stash/rebase.
- Reserved target: `C:\Projects\FOX2-worktrees\FOX2-BRG-003`.
- Reserved new **LOCAL-ONLY** branch: `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`.
- Only one assigned actor, Copilot, for this *target directory/branch* during Phase A. Do not modify any CODEX-owned directories or shut down existing Codex processes. The target's prior absence is not proof of ownership; record actual isolation and exclusive assignment when created. If evidence suggests a second writer, STOP before any write.
- Permitted writes solely **Git's necessary checkout/worktree/branch metadata** at reserved target, local Git object storage created by an exact non-destructive fetch, and required worktree metadata in the existing FOX2 .git repository. No application/doc edits anywhere.
- Explicitly forbidden: copying, reading into Git, editing or staging `C:\Projects\FOX2-AgentBridge`; creating/modifying `agent_bridge/**` in the worktree; any staged changes, commits, remote branch create/push, tests, SQLite DB/WAL/SHM opening/checkpoint/deletion, local secrets, Git credential modifications, `main`, Bridge event/control branches, forced Git operations, dispatch, broker or LIVE.

## Ordered gated actions (ONLY if preparer's non-DEV eligibility and Owner-context grant are acceptable under effective policy)

0. Read this prompt from pinned Git commit and reconfirm exact source/head status. Record observed Copilot product/model/mode *if shown*. Record unexposed fields as `NOT_EXPOSED`. Do not ask Owner to attest what is unobservable. If required qualification remains materially unknown for even this non-DEV operation, STOP without mutation.
1. Under `C:\Projects\FOX2`, verify `origin` points at `https://github.com/dunglt2505/FOX2.git` without credentials embedded; root `git status --porcelain` empty; no `index.lock`; reserved branch/target do **not** exist locally or remotely; `git worktree list --porcelain` shows no conflicting ownership. Confirm no active assigned Agent currently owns target. On anomaly STOP.
2. Read-only `git ls-remote origin refs/heads/work/FOX2-BRG-003-MANIFEST-RECOVERY-chat-20261013` and verify the expected commit is still reachable; no change to source identity. Do NOT assume branch movement is permission to switch base.
3. Non-destructively fetch exactly `refs/heads/work/FOX2-BRG-003-MANIFEST-RECOVERY-chat-20261013` without switching/root worktree edits. Verify `git cat-file -t c8a0d517b8655868053e4923f5947c12975a5865` = commit and exact tree blobs above via `git ls-tree`. On mismatch STOP.
4. Run `git worktree add -b work/FOX2-BRG-003-SOURCE-BASELINE-copilot C:\Projects\FOX2-worktrees\FOX2-BRG-003 c8a0d517b8655868053e4923f5947c12975a5865` exactly once, only if target does not exist and prechecks passed. The new branch remains **LOCAL ONLY**.
5. Verify at target: HEAD exact base, branch exact reserved name, `git status --porcelain=v1 --untracked-files=all` empty, `git worktree list --porcelain` names exact directory, root checkout remains unchanged/clean, no remote target branch created. Report lease holder `COPILOT/BRG-003-PREPARE-A01` and evidence of target isolation; if cannot prove adequate exclusive writer, report `WRITER_CONDITIONAL/UNKNOWN`, **not PASS**, and STOP there.
6. Report all facts directly in Copilot Chat; do not write or push evidence file as this task has no report-push grant.

## Required completion report

`FOX2 BRG-003 PREPARE_CHECKOUT EVIDENCE`: source identity and latest-Library attestation, selected model/mode or NOT_EXPOSED, quota availability or NOT_EXPOSED, root original HEAD+dirty status, exact `ls-remote` observation, fetch status, target worktree branch/HEAD/status, actual writer reservation/isolation evidence, existing Codex-process collisions if actually observed, changed local paths *only git metadata*, runtime/file WIP unaffected, tests NOT_RUN, remote push NOT_RUN, `CODE_ALLOWED=NO`, `GIT_CODE_PUSH=NO`, `OPEN_GATES`.

Completion state can be `CHECKOUT_PREPARED_UNREVIEWED` (not source import READY, not writer proof beyond evidence), `BLOCKED_AGENT_ELIGIBILITY`, `BLOCKED_WRITER`, or `BLOCKED_SOURCE_VERSION`. Any uncertain/failed prerequisite => STOP and preserve what was safely completed; no force cleanup.
