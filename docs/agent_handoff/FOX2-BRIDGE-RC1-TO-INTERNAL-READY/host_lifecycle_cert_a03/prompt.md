FOX2 — CODEX EXECUTION PROMPT — CURRENT-PACKAGE OWNER-HOST LIFECYCLE CERTIFICATION A03

Role: CODEX — Primary host-lifecycle certification executor
Model: gpt-6.1-sol
Thinking: high
Mode: Execute bounded TEST certification end-to-end
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-20261022
Permission profile: FULL_ACCESS only within this task
Max Agent attempts: 1
No replay / no model substitution

Prompt revision: FRESH_A03_RUNTIME_AUTHORIZATION_ENVELOPE

A03 is a fresh attempt after consumed/no-result Host Lifecycle A02.

Historical A02 Dispatch
`FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001`
is permanently consumed and MUST NOT be replayed.

CHAT recovery receipt:
`53c3913899f87ad867c04c14d1da52b27d3cdbec`

A02 lifecycle certification remained NOT_RUN: no package build, no host lifecycle mutation, no Git result commit.

IMPORTANT — EXECUTION AUTHORITY VISIBILITY

This file is a Git-published executable prompt candidate, but its existence is NOT execution authority.

CHAT must still complete, before CODEX is started:
1. a fresh task-specific A03 route/host PreExec PASS;
2. a fresh A03 PASS_TO_ASSIGN;
3. exactly one fresh A03 executable Dispatch;
4. remote readback of that exact Dispatch;
5. an Owner-visible PowerShell 7 launcher that verifies all immutable gates.

Those artifacts are intentionally created AFTER this immutable prompt. Their future commit SHAs therefore MUST NOT be hard-coded into this prompt.

At actual CODEX process start, the verified Owner launcher MUST supply the runtime authorization envelope defined below. CODEX MUST fetch and verify the referenced immutable Git artifacts before any package build or host mutation.

A valid runtime envelope plus successful remote Git verification is the Agent-visible proof that CHAT completed the post-prompt authorization chain. Do NOT require PASS_TO_ASSIGN, Dispatch, or the PowerShell launcher text to be copied into this task branch.

Never reuse any historical consumed Dispatch.

TASK ID

FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert_a03/task.md

Task commit:
33f6176dff86b00df6c9b8b0ef6f8eefce00578e

Task blob SHA-1:
687dfc109ed438db5a5b69b75486f1a32994eb9d

Task raw SHA-256:
f9e2fe4e285f703edabd8ec1266b0244d520ee2e1be876daf45b332bfcfc1f0f

ACCEPTED SOURCE

Accepted A02 BUILD result:
085cc8302e824dbccf9cbef80422ed48894b9cb4

CHAT acceptance:
cdf9f9c919102a2337ef357f4b658dc9993f48e5

A02 BUILD result is the exact package/source baseline for this TEST.

Historical real-host lifecycle result:
9dd91becf47d934183baf147d0a4f03f4bf5933d

Historical verdict:
FAIL / REWORK_REQUIRED

That failure remains factual and must not be rewritten.

HISTORICAL NO-REPLAY IDENTITIES

Never replay:
- FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01-CODEX-001
- FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A01-CODEX-001
- FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001
- FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A02-CODEX-001

The future A03 Dispatch identity is fixed as:
FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001

It must have max_runs=1 and a fresh runtime base from the A03 PreExec PASS receipt.

A02 remains CONSUMED_NO_RESULT / certification NOT_RUN. Do not reinterpret its CODEX exit 0 as TEST PASS.

GOVERNANCE BINDING

Resolve and verify current authorized Governance before execution.

Current resolved set at task publication:
- Policy 2.0.0 commit 96175ac4f39197794a04e695f0046fa7ef9321fe
- Dictionary 1.3 commit b25f7f728de67cf8595bf24f22fcbd79ef50babc
- Routing Index 1.4.0 commit bcd008983b61349646a5198ff243069f81484fae
- Git-first Protocol v12 commit f2a8bc8e6ce0785a800d78a3c384f205fdc5a6fa
- effective Dispatch Schema v3 blob 1692061941e2bef498515cd0e96b9b3046119ebb

Bridge TechSpec v0.7 REV10 remains CANDIDATE_NO_PROMOTION.

EXECUTION START RULE — RUNTIME AUTHORIZATION ENVELOPE

The future PASS_TO_ASSIGN and Dispatch commit SHAs are not known when this prompt is published. The Owner-visible launcher must inject them at actual CODEX start.

Required environment variables:
- FOX2_DISPATCH_ID
- FOX2_DISPATCH_COMMIT
- FOX2_RUNTIME_BASE
- FOX2_ACCEPTED_SOURCE
- FOX2_PASS_TO_ASSIGN_COMMIT
- FOX2_PASS_TO_ASSIGN_PATH
- FOX2_PREEXEC_RECEIPT_COMMIT
- FOX2_CONTROL_BRANCH
- FOX2_STATUS_BRANCH
- FOX2_OWNER_LAUNCHER_VERIFIED

Expected fixed values:
- FOX2_DISPATCH_ID = FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001
- FOX2_ACCEPTED_SOURCE = 085cc8302e824dbccf9cbef80422ed48894b9cb4
- FOX2_CONTROL_BRANCH = work/FOX2-DISPATCH-chat
- FOX2_STATUS_BRANCH = work/FOX2-BRIDGE-F1-G1-INTEGRATED-DESIGN-20261021
- FOX2_PASS_TO_ASSIGN_PATH = reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/HOST_LIFECYCLE_CERT_A03_PASS_TO_ASSIGN_20261022.md
- FOX2_OWNER_LAUNCHER_VERIFIED = TRUE
- FOX2_PREEXEC_RECEIPT_COMMIT must equal FOX2_RUNTIME_BASE

Expected fresh Dispatch path:
docs/agent_handoff/DISPATCH/FOX2-DISPATCH-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03-CODEX-001.json

Expected A03 PreExec receipt path:
reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/host_lifecycle_cert_a03.json

Before package build or any host mutation, CODEX MUST:

1. require every environment variable above;
2. require local HEAD and remote A03 task branch HEAD equal FOX2_RUNTIME_BASE;
3. require FOX2_PREEXEC_RECEIPT_COMMIT equals FOX2_RUNTIME_BASE;
4. require accepted source 085cc830... is an ancestor of runtime base;
5. fetch FOX2_CONTROL_BRANCH from origin;
6. require FOX2_DISPATCH_COMMIT is readable and resolves the exact expected fresh A03 Dispatch path;
7. parse that Dispatch JSON and require:
   - dispatch_id equals the expected A03 ID;
   - target_agent=CODEX;
   - model=gpt-6.1-sol;
   - reasoning_effort=high;
   - permission_profile=FULL_ACCESS;
   - source.commit_sha=085cc830...;
   - runtime_contract.base_sha=FOX2_RUNTIME_BASE;
   - task commit/path/SHA-256 match this A03 task;
   - prompt commit/path/blob/SHA-256 match THIS immutable prompt;
   - permissions.code_allowed=false;
   - permissions.git_code_push=false;
   - report/evidence writes only;
   - max_runs=1;
8. fetch FOX2_STATUS_BRANCH from origin;
9. require FOX2_PASS_TO_ASSIGN_COMMIT is readable and resolves FOX2_PASS_TO_ASSIGN_PATH;
10. require that PASS_TO_ASSIGN artifact names:
    - task FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A03;
    - verdict PASS_TO_ASSIGN;
    - the same A03 PreExec receipt/runtime-base commit;
    - the planned fresh A03 Dispatch ID;
11. read the A03 PreExec receipt from FOX2_RUNTIME_BASE and require PASS, blockers empty, Agent not started, Dispatch not consumed at PreExec, host-safe material capabilities PASS;
12. require exact task/prompt SHA-256, clean worktree, one task-scoped writer and current route/capacity PASS;
13. require changes between accepted source and runtime base contain only A03 task/prompt/PreExec/receipt setup, with no agent_bridge product/source/test drift.

The environment variables are evidence transport only. They do not override Git. If any supplied value cannot be independently resolved from Git or disagrees with fetched immutable bytes, STOP before mutation.

Do NOT block merely because PASS_TO_ASSIGN or Dispatch are absent from the task branch: they live on their separately supplied status/control branches by design.

Do NOT require the Owner-visible PowerShell script text to exist in Git. CHAT's launcher gate is represented to CODEX by FOX2_OWNER_LAUNCHER_VERIFIED=TRUE plus the immutable envelope checks above.

HOST MUTATION AUTHORITY

This task authorizes only the per-user Bridge lifecycle needed to certify Phase-2 TEST:

1. optional bounded surface-and-graceful-close of one exact current-package stale WPF presentation before install;
2. build one exact accepted package outside BridgeRoot;
3. install/update that exact package;
4. establish/verify paused/setup/no-current-dispatch state;
5. launch and certify accepted WPF presentation-only lifecycle;
6. gracefully exit the WPF presentation;
7. stable external uninstall exactly once;
8. reinstall the exact same package;
9. verify durable state and final safe installed state;
10. bounded same-package recovery reinstall after a post-mutation failure only when needed.

This does NOT authorize:
- Worker/F1 start or health manufacture;
- AppLocker;
- AppIDSvc;
- FOX2F1Authority service;
- ProgramData authority ACL;
- reboot;
- G3/G4;
- Canary;
- main/PR/merge;
- provider/broker/LIVE.

ACCEPTED WPF CONTRACT

Before G3 the accepted architecture is presentation-only.

Required:
- stable launch entrypoint: BridgeRoot/launch.ps1;
- launch twice -> exactly one current-package FOX2.Bridge.Desktop.exe;
- current package pointer/path and inspected UI PID all agree;
- paused=true;
- setup_complete=true;
- current_dispatch field exists and is null;
- Worker/F1 health = NOT_APPLICABLE_PRE_G3;
- no Worker/F1 start;
- no Worker heartbeat requirement;
- certify_rc1_ui.ps1 reused for inspect/check/exit;
- six expected UI navigation screens;
- Check Now disabled while paused;
- presentation lock held while live;
- safe state and exact presentation rechecked before exit;
- explicit graceful UI exit;
- zero WPF presentation processes after exit;
- lock release;
- STOPPED/paused/setup_complete/current_dispatch=null after exit;
- only then may stable uninstall proceed.

If any code or old task still expects desktop_tray.ps1 health, Worker heartbeat or Worker/F1 activation, STOP and return REWORK_REQUIRED. Do not work around the accepted contract.

PRE-MUTATION CAPABILITY RULES

Before package build or host mutation verify:
- Owner physical Windows host;
- PowerShell 7;
- Git;
- Python required by orchestration;
- CODEX CLI exact compatible route;
- dotnet required by deterministic Desktop package build;
- existing isolated build Python compatible with build_user_package.py;
- no dependency/tool installation needed;
- exact source/task/prompt/PreExec/Dispatch;
- no G3/G4/Canary active;
- current installed Bridge state read-only captured;
- WPF presentation state read-only captured;
- Worker state read-only captured;
- durable hashes/identities captured read-only;
- package build output root is outside BridgeRoot;
- no unsafe active process that makes mutation ambiguous.

No tool installation, host configuration change or alternate Agent route is permitted to make a gate pass.

OPTIONAL PRE-INSTALL STALE WPF RECONCILIATION / CLEANUP

If exactly one WPF presentation exists before package mutation, re-verify:
- exact current package executable path;
- current pointer identity;
- safe paused/setup/no-current-dispatch state;
- no Worker/F1 or legacy tray process.

If the existing presentation is visible, require the UI inspect PID to equal the observed WPF PID.

If the existing exact-current presentation is hidden/minimized and the UI seam reports only `Installed Desktop window unavailable`:
- invoke stable `BridgeRoot/launch.ps1` exactly once;
- this invocation is only to signal the already-running singleton show-event;
- require WPF process count remains exactly one;
- require PID and executable path remain unchanged;
- wait boundedly for `certify_rc1_ui.ps1 -Action inspect` to succeed;
- require inspect PID equals the same WPF PID.

Only after visible exact identity is proven:
- recheck safe paused/setup/no-current-dispatch state;
- invoke explicit UI `exit` exactly once;
- wait boundedly for zero WPF presentations;
- require presentation lock release;
- record this as pre-test cleanup only.

STOP before install if stable launch creates a second presentation, PID/path drifts, UI remains unavailable, safe state drifts, or graceful exit fails.

No force kill. No Worker/F1 fallback.

PACKAGE BUILD

Use:
agent_bridge/scripts/build_user_package.py

Build from accepted source ancestry on the clean A03 task branch.

Use only an already-existing compatible isolated build Python.

Package:
- must remain outside BridgeRoot through uninstall/recovery;
- must be built once;
- must not be committed;
- must have computed SHA-256;
- manifest must be verified;
- manifest.source_git_commit must equal:
  085cc8302e824dbccf9cbef80422ed48894b9cb4
- verify source/payload/wheel-module hashes;
- record build Python and dotnet identities without private paths/secrets.

If source_git_commit differs, STOP before mutation.

PRE-STATE

Capture bounded sanitized evidence before first install:
- installed state/current pointer/source receipt;
- WPF process count/path/PID;
- Worker status;
- paused/setup/current-dispatch;
- startup preference;
- stable uninstall supervisor identity/hash;
- owned versions;
- Task Scheduler state;
- config SHA-256;
- DB identity/hash and quick-check if safe;
- manual-consumption SHA-256;
- historical consumed dispatch identity/state summary.

Never commit raw config, DB contents, secrets, tokens, raw prompts or unnecessary private absolute paths.

INSTALL / UPDATE

Use:
agent_bridge/scripts/install_user.ps1

Use exact package path and SHA-256.

Requirements:
- per-user only;
- no elevation;
- no service/AppLocker/ACL mutation;
- current pointer exact;
- installed receipt/source exact;
- Worker/F1 not started.

SAFE STATE

Before lifecycle script:
- paused=true;
- setup_complete=true;
- explicit current_dispatch=null;
- no extra WPF presentation;
- no Worker/F1/tray state that conflicts with accepted WPF-only contract.

Do not launch Worker/F1 to make a check green.

REAL LIFECYCLE

Run:
agent_bridge/scripts/certify_user_lifecycle.py

Arguments must bind:
- exact package;
- exact package SHA-256;
- bounded evidence path outside installed versions.

The accepted script must exercise:
- setup/startup checks;
- WPF launch twice;
- exact singleton identity;
- UI inspect/check;
- held presentation lock;
- safe-state recheck;
- explicit graceful exit;
- zero presentations;
- lock release;
- post-exit STOPPED/paused/setup/no-current-dispatch;
- diagnostics;
- stable external BridgeRoot/uninstall.ps1;
- immediate uninstall postconditions;
- durable config/data/manual-consumption preservation;
- exact same package reinstall;
- reinstalled setup/final safe state;
- historical consumed identities unchanged.

Stable uninstall attempt count must be exactly one on the successful lifecycle path.

Worker/F1 remains NOT_APPLICABLE_PRE_G3.

FAILURE AND RECOVERY

Once any host mutation begins:
- preserve first failure;
- never rerun lifecycle certification in this Dispatch;
- never retry stable uninstall;
- never replay Dispatch;
- never silently change package/source.

If host becomes unusable after mutation, bounded recovery may reinstall the same exact package once when needed.

Recovery:
- must be separately recorded;
- does not convert FAIL/BLOCKED into PASS;
- does not authorize G3/G4 or any broader mutation.

If a source/code fix is required:
STOP with REWORK_REQUIRED.
Do not edit code/tests/scripts in this TEST task.

REPOSITORY WRITE SCOPE

No product/source/test edits.

Only:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert_a03/**

Temporary build/package data are excluded from Git.

REQUIRED ACCEPTANCE

Prove all task.md acceptance items truthfully.

At minimum:
- runtime authorization envelope + remote PASS_TO_ASSIGN/Dispatch/PreExec verification PASS before mutation;
- exact source/package provenance;
- package build/manifest/hash PASS before mutation;
- pre-state snapshot;
- exact install/update PASS;
- safe paused WPF pre-state;
- launch twice one WPF PASS;
- exact current presentation/UI identity PASS;
- UI inspect/check PASS;
- live lock PASS;
- explicit graceful exit PASS;
- zero WPF + lock release PASS;
- post-exit safe control PASS;
- stable uninstall exactly once PASS;
- immediate uninstall postconditions PASS;
- durable state preservation PASS;
- exact same package reinstall PASS;
- final pointer/source/setup/paused state PASS;
- historical consumed identities preserved;
- no replay;
- no Worker/F1/G3/G4/AppLocker/service/ACL mutation;
- changed-path allowlist;
- git diff --check;
- secret scan;
- K1 UNEXPLAINED=0;
- Result Contract v2;
- remote pushed result.

RESULT STATES

Return exactly truthful PASS / FAIL / BLOCKED / NEEDS_RECONCILIATION boundaries.

Do not relabel:
- historical host A01 FAIL;
- historical consumed Dispatches;
- NOT_RUN operations;
- bounded recovery success.

GIT DELIVERY

After execution:
1. write only authorized result paths;
2. validate Result Contract v2;
3. commit evidence;
4. push only this non-main branch;
5. read remote branch head;
6. return observed remote result SHA outside committed report.

Final submission is PUSHED_UNREVIEWED.

Do not claim CHAT acceptance.

STOP

STOP before mutation for any source/task/prompt/PreExec/Dispatch drift, missing capability, dirty worktree, competing writer, unsafe state or package provenance mismatch.

After mutation begins, preserve the first result and follow only the bounded recovery rule.
