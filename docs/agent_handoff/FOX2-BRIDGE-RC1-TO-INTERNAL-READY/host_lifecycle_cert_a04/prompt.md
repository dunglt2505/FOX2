FOX2 — CODEX EXECUTION PROMPT — CURRENT-PACKAGE OWNER-HOST LIFECYCLE CERTIFICATION A04

Role: CODEX — Primary host-lifecycle certification executor
Model: gpt-6.1-sol
Thinking: high
Mode: Execute bounded TEST certification end-to-end
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022
Permission profile: FULL_ACCESS only within this task
Max Agent attempts: 1
No replay / no model substitution

Prompt revision: FRESH_A04_SPLIT_PACKAGE_SOURCE_WORKTREE

A04 is a fresh TEST attempt after truthful A03 provenance BLOCKED result.

Historical A03 Dispatch
FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001
is permanently consumed and MUST NOT be replayed.

A03 result:
883ea51a429baf6749fa3fd412cc9ebb044f6efc

CHAT A03 review:
eced60bc22e7294bf49b367791c122ad91a97f43

A03 lifecycle certification remained NOT_RUN: no package build, no install/update, no host lifecycle mutation.

A04 changes only the execution/build context contract. Product/source/test code remains the accepted BUILD result.

TASK ID

FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a04/task.md

Task commit:
8fdc2f7181e7f3e9a7f56ea72472fe3d2d2cea43

Task blob SHA-1:
50d77f3039d2a8f9ce40105457da8e18b639289d

Task raw SHA-256:
397e179c63666ce611e2c03cfb988ccbd9290a72b9643014fe1ff0588bfb7aa8

ACCEPTED PRODUCT SOURCE

085cc8302e824dbccf9cbef80422ed48894b9cb4

CHAT BUILD acceptance:
cdf9f9c919102a2337ef357f4b658dc9993f48e5

ACCEPTED PACKAGE BUILDER

Path:
agent_bridge/scripts/build_user_package.py

Blob:
2417212e5677a2061e3957544a99e2ba80f46f4d

The builder is intentionally unchanged.

A04 MUST NOT patch the builder, override its source identity, rewrite manifest.source_git_commit or fabricate provenance.

WHY A04 EXISTS

The accepted builder obtains package source provenance from the Git HEAD of the worktree containing the builder.

A03 executed CODEX in an orchestration task worktree whose HEAD necessarily contained post-product task/prompt/PreExec/receipt commits. Therefore source_git_commit() returned the runtime base instead of the accepted product source.

A04 solves this without product code change by using two different worktrees:

1. ORCHESTRATION WORKTREE
   C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-20261022

   Purpose:
   - immutable A04 task/prompt/PreExec/receipt;
   - CODEX runtime;
   - result report/evidence Git writes.

2. PACKAGE-SOURCE WORKTREE
   C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04

   Purpose:
   - exact product source for package build only;
   - detached HEAD;
   - HEAD exactly 085cc8302e824dbccf9cbef80422ed48894b9cb4;
   - no task/report commits;
   - no source edits.

The package MUST be built using the builder in the PACKAGE-SOURCE WORKTREE, never using the copy in the orchestration worktree.

RUNTIME AUTHORIZATION ENVELOPE

Future PASS_TO_ASSIGN and Dispatch commit SHAs are intentionally unknown when this prompt is published.

At actual CODEX start the Owner-visible launcher MUST supply:

FOX2_DISPATCH_ID
FOX2_DISPATCH_COMMIT
FOX2_RUNTIME_BASE
FOX2_ACCEPTED_SOURCE
FOX2_PASS_TO_ASSIGN_COMMIT
FOX2_PASS_TO_ASSIGN_PATH
FOX2_PREEXEC_RECEIPT_COMMIT
FOX2_CONTROL_BRANCH
FOX2_STATUS_BRANCH
FOX2_PACKAGE_SOURCE_WORKTREE
FOX2_OWNER_LAUNCHER_VERIFIED

Expected fixed values:

FOX2_DISPATCH_ID =
FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A04-CODEX-001

FOX2_ACCEPTED_SOURCE =
085cc8302e824dbccf9cbef80422ed48894b9cb4

FOX2_CONTROL_BRANCH =
work/FOX2-DISPATCH-chat

FOX2_STATUS_BRANCH =
work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021

FOX2_PASS_TO_ASSIGN_PATH =
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A04_PASS_TO_ASSIGN_20261022.md

FOX2_PACKAGE_SOURCE_WORKTREE =
C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04

FOX2_OWNER_LAUNCHER_VERIFIED =
TRUE

FOX2_PREEXEC_RECEIPT_COMMIT must equal FOX2_RUNTIME_BASE.

Before package build or any host mutation, CODEX MUST independently verify:

1. all required environment variables exist;
2. fixed values above match;
3. local + remote A04 orchestration branch HEAD equal FOX2_RUNTIME_BASE;
4. accepted source is an ancestor of runtime base;
5. FOX2_PREEXEC_RECEIPT_COMMIT equals runtime base;
6. fetched control branch contains FOX2_DISPATCH_COMMIT and the exact A04 Dispatch path;
7. Dispatch binds this exact task/prompt/source/runtime base, CODEX, gpt-6.1-sol/high, FULL_ACCESS, max_runs=1;
8. Dispatch controlling permissions have code_allowed=false and git_code_push=false;
9. result writes only report.md/evidence_manifest.json/evidence/host_lifecycle_cert_a04/**;
10. fetched status branch contains the supplied PASS_TO_ASSIGN commit/path;
11. PASS_TO_ASSIGN names A04 task, same runtime-base/receipt commit and planned A04 Dispatch ID;
12. A04 PreExec receipt at runtime base is PASS with empty blockers, Agent not started and Dispatch not consumed at PreExec;
13. orchestration worktree is clean and has no agent_bridge product/source/test drift from accepted source;
14. exactly one task-scoped CODEX writer;
15. package-source worktree passes the package-source gates below.

The environment envelope transports evidence only. Git remains authoritative.

Do NOT require PASS_TO_ASSIGN/Dispatch to exist in the orchestration task branch.

PACKAGE-SOURCE WORKTREE GATE

Before package build require:

- exact path from FOX2_PACKAGE_SOURCE_WORKTREE;
- same Git repository;
- detached HEAD;
- HEAD exactly 085cc8302e824dbccf9cbef80422ed48894b9cb4;
- clean tracked/untracked worktree before build;
- accepted builder blob exactly 2417212e5677a2061e3957544a99e2ba80f46f4d;
- accepted builder raw source unchanged;
- no branch checkout;
- no cherry-pick/rebase/reset that changes source identity;
- no product edits;
- no source/ref/environment override to fake provenance.

Using the already-existing compatible isolated build Python, import the PACKAGE-SOURCE builder with bytecode disabled and call source_git_commit() only.

Require exact return:

085cc8302e824dbccf9cbef80422ed48894b9cb4

If this read-only probe differs, STOP before package build or host mutation.

HOST MUTATION AUTHORITY

Only the per-user Bridge lifecycle needed for this TEST:

1. optional bounded surface + graceful close of one exact-current stale WPF presentation;
2. build one exact accepted-source package outside BridgeRoot/worktrees;
3. install/update exact package;
4. verify paused/setup/current_dispatch=null;
5. WPF presentation-only lifecycle certification;
6. graceful WPF exit;
7. stable external uninstall exactly once;
8. reinstall same exact package;
9. durable/final state verification;
10. bounded same-package recovery reinstall after post-mutation failure only when task conditions permit.

Forbidden:
- Worker/F1 start;
- desktop_tray health manufacture;
- AppLocker/AppIDSvc;
- FOX2F1Authority service;
- ProgramData authority ACL;
- reboot;
- G3/G4;
- Canary;
- source/test edits;
- PR/main/merge;
- provider/broker/LIVE.

HIDDEN/MINIMIZED CURRENT WPF

If one exact-current WPF exists and UI inspect reports only Installed Desktop window unavailable:

- reverify exact current package/path/PID;
- require paused/setup/current_dispatch=null;
- require Worker/legacy absent;
- invoke stable BridgeRoot/launch.ps1 exactly once only to signal the existing singleton show event;
- require process count remains exactly one;
- require same PID and path;
- wait boundedly for certify_rc1_ui.ps1 -Action inspect;
- require UI PID equals same PID;
- recheck safe state;
- invoke explicit UI exit once;
- require zero presentation processes;
- require presentation-lock release.

STOP before install on second process, PID/path drift, UI still unavailable, unsafe control drift or graceful-exit failure.

No force kill and no Worker/F1 fallback.

PACKAGE BUILD

Build exactly once using ONLY:

C:\Projects\FOX2-worktrees\FOX2-BRIDGE-RC1-PACKAGE-SOURCE-085CC830-A04\agent_bridge\scripts\build_user_package.py

Use only the already-existing compatible isolated build Python.

Package output:
- outside BridgeRoot;
- outside both Git worktrees;
- survives uninstall/reinstall;
- not committed.

After build verify:
- package SHA-256;
- manifest format;
- manifest.source_git_commit exactly accepted source;
- dictionary version/hash;
- source_files hashes;
- wheel_source_modules hashes;
- package payload hashes;
- Desktop payload exists;
- package source provenance derives from package-source worktree, not orchestration HEAD.

No manifest rewrite.

PRE-STATE

Before first install/update capture bounded sanitized A04 baseline:

- installed state/current pointer/source receipt;
- WPF count/path/PID;
- Worker state;
- paused/setup/current_dispatch;
- startup preference;
- config SHA-256;
- DB hash/identity and SQLite quick-check when safe;
- manual-consumption hash;
- stable uninstall hash;
- owned versions;
- scheduler state;
- historical consumed identities;
- exact package SHA/source.

A historical DB hash change before A04 is neither PASS nor FAIL. Preservation is measured from the fresh A04 pre-mutation baseline.

INSTALL / SAFE STATE

Use:
agent_bridge/scripts/install_user.ps1

with exact package + SHA-256.

Require:
- per-user;
- no elevation/system install;
- exact current pointer/source receipt;
- no Worker/F1 start.

Then require:
paused=true
setup_complete=true
current_dispatch=null

REAL LIFECYCLE

Run:
agent_bridge/scripts/certify_user_lifecycle.py

with exact package/SHA and bounded evidence path outside installed versions.

Accepted lifecycle must exercise:

- setup/startup checks;
- WPF stable launch twice;
- exactly one current-package presentation;
- UI inspect/check;
- six expected navigation screens;
- Check Now disabled while paused;
- held presentation lock;
- safe-control recheck;
- explicit graceful exit;
- zero presentations;
- lock release;
- post-exit STOPPED/paused/setup/current_dispatch=null;
- diagnostics;
- stable external BridgeRoot/uninstall.ps1;
- uninstall postconditions;
- durable preservation from A04 pre-state;
- exact same package reinstall;
- final exact pointer/source/setup/paused safe state;
- historical consumed identities unchanged.

Worker/F1 health remains NOT_APPLICABLE_PRE_G3.

Successful path stable-uninstall attempt count = exactly one.

FAILURE / RECOVERY

Once any host mutation begins:

- preserve first failure;
- never rerun lifecycle certification;
- never retry stable uninstall;
- never replay Dispatch;
- never change package/source silently.

If host becomes unusable after mutation, bounded recovery may reinstall the same exact package once when needed.

Recovery success does not convert FAIL/BLOCKED into PASS.

If product/source code correction is required, STOP REWORK_REQUIRED. This TEST has no code-write permission.

REPOSITORY WRITE SCOPE

Only:

reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a04/**

No product/source/test/handoff/PreExec changes during Agent execution.

REQUIRED ACCEPTANCE

Truthfully map all A04 task acceptance items.

At minimum prove:

- runtime envelope remote verification PASS;
- orchestration no-drift PASS;
- detached accepted-source package worktree PASS;
- builder exact and source_git_commit pre-probe PASS;
- package built once with exact accepted-source manifest;
- pre-state captured;
- install/update PASS;
- safe paused state;
- WPF launch twice singleton;
- UI inspect/check;
- lock held;
- graceful exit;
- zero WPF + lock release;
- post-exit safe state;
- stable uninstall exactly once;
- uninstall exit 0;
- immediate uninstall postconditions;
- durable state preserved from A04 baseline;
- same exact package reinstall;
- final exact installed state;
- consumed identities preserved;
- no replay;
- no forbidden Worker/F1/G3/G4/AppLocker/service/ACL mutation;
- result path allowlist;
- secret scan;
- git diff --check;
- K1 UNEXPLAINED=0;
- Result Contract v2;
- remote pushed result.

RESULT DELIVERY

Push actual report/evidence to the authorized non-main A04 task branch.

Return observed remote result SHA outside committed report.

Result remains PUSHED_UNREVIEWED until CHAT review.

STOP

STOP before mutation on any authorization/provenance/package-source-worktree mismatch, unsafe host state, dirty worktree, missing capability, competing writer or source drift.

After mutation starts, preserve first failure and use only the bounded same-package recovery rule.
