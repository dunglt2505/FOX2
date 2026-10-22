# FOX2 — CHAT Result Review — Host Lifecycle Certification A03

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Task: `FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001`
Result SHA: `883ea51a429baf6749fa3fd412cc9ebb044f6efc`

## Verdict

**CHAT_REWORK — A03 RESULT ACCEPTED AS TRUTHFUL BLOCKED REPORT; HOST LIFECYCLE CERTIFICATION NOT ACCEPTED**

The Git result delivery and evidence integrity are accepted. The requested lifecycle TEST is not accepted because it was not run.

A03 Dispatch is consumed and MUST NOT be replayed.

## Result delivery / provenance

CHAT independently remote-read verified:

- runtime base: `534204d5cc39a17fb4b3beb948b9b472d6e550b5`;
- result: `883ea51a429baf6749fa3fd412cc9ebb044f6efc`;
- ancestry: result is ahead by 2 commits, behind 0;
- changed paths: 12;
- unauthorized paths: 0;
- no `agent_bridge` product/source/test change;
- report path present;
- evidence manifest present;
- Result Contract v2 schema blob: `b7617cc5c75c288c7997c64536a22fb836b8200b`;
- manifest schema validation: zero errors;
- all 10 evidence file SHA-256 values independently recomputed and matched;
- report SHA-256 independently recomputed and matched manifest inventory;
- K1 `UNEXPLAINED=0`;
- delivery is `PUSHED_UNREVIEWED`, not prior CHAT acceptance.

## Material result

Agent correctly stopped before package build or host mutation.

Observed accepted builder:
`agent_bridge/scripts/build_user_package.py`
blob:
`2417212e5677a2061e3957544a99e2ba80f46f4d`

The unchanged accepted builder's `source_git_commit()` resolves:

`git rev-parse --verify HEAD`

from the worktree containing the builder, and directly writes that value to:

`manifest.source_git_commit`.

On the A03 orchestration/task worktree the exact return was:

`534204d5cc39a17fb4b3beb948b9b472d6e550b5`

but the package acceptance gate requires:

`085cc8302e824dbccf9cbef80422ed48894b9cb4`.

Therefore an A03 package build in the A03 task worktree cannot satisfy its own provenance requirement.

No package was built. No package manifest/hash exists. Install=0, lifecycle=0, stable uninstall=0, reinstall=0, recovery=0. G3/G4/Canary remain NOT_RUN.

## Acceptance review

Accepted from A03:
- runtime authorization envelope verification PASS;
- immutable source/task/prompt/PreExec/Dispatch/PASS_TO_ASSIGN verification PASS;
- report/result contract and evidence integrity PASS;
- historical consumed identities preserved;
- no replay;
- no forbidden Worker/F1/G3/G4/AppLocker/service/ACL mutation;
- report-only path scope PASS;
- secret/privacy scan PASS;
- git diff check PASS;
- K1 PASS.

Not accepted / not run:
- exact package build and manifest provenance;
- install/update;
- WPF lifecycle;
- graceful exit / presentation-lock release;
- stable uninstall;
- durable preservation certification;
- same-package reinstall;
- final safe installed state;
- lifecycle TEST exit gate.

A03 acceptance mapping is truthful: PASS=10, BLOCKED=1, NOT_RUN=20.

## Additional host observation

A03 limited observation recorded one exact-current WPF process and no lifecycle mutation.

The DB file SHA-256 differed from A03 PreExec. A03 did not investigate cause and did not claim durable preservation PASS. This historical difference must not be converted to failure or pass. A fresh lifecycle attempt must capture a new bounded pre-mutation baseline and compare its own post-state to that baseline.

## Root cause classification

**EXECUTION/PROVENANCE CONTRACT CONTRADICTION — not a product implementation regression.**

The builder behavior is internally coherent: package provenance follows the HEAD of the worktree from which product sources are packaged.

The contradiction came from asking a single task worktree to satisfy both:
1. contain post-source task/prompt/PreExec/receipt commits; and
2. make builder HEAD equal the earlier accepted product source commit.

## Minimal correction

Do not patch or override the package manifest and do not edit the accepted builder merely to bypass provenance.

Fresh A04 should use two explicitly separated worktrees:

1. **Orchestration worktree**
   - fresh A04 task branch;
   - contains immutable task/prompt/PreExec/receipt and later result reports;
   - CODEX execution occurs here.

2. **Package-source worktree**
   - dedicated detached Git worktree at exact accepted product source:
     `085cc8302e824dbccf9cbef80422ed48894b9cb4`;
   - clean product tree;
   - no task/report commits;
   - read/build source only;
   - invoke that worktree's unchanged `agent_bridge/scripts/build_user_package.py`;
   - builder's own `source_git_commit()` must return exactly the accepted source before build;
   - resulting manifest must independently equal the accepted source;
   - package output remains outside BridgeRoot and outside Git.

No source ref override, environment override, manifest rewrite or builder modification is authorized.

## Next safe action

Create fresh task:
`FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04`

using the same accepted BUILD source and accepted WPF lifecycle contract, but with the split orchestration/package-source worktree contract above.

Then:
fresh A04 PreExec → CHAT PASS_TO_ASSIGN → fresh A04 Dispatch → exactly one Owner-host execution attempt → CHAT result review.

G3 remains locked.
