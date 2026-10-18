# FOX2 — BRIDGE RC1 WHOLE-WP RECOVERY + IMPLEMENTATION PROMPT

Built with: FOX2 Skill 01 — fox2-agent-prompt-builder
Recovery rule: FOX2 Skill 15 — fox2-execution-recovery
Routing rule: FOX2 Skill 09 — fox2-agent-route-runtime
State: SOURCE-BOUND PROMPT / NOT EXECUTABLE WITHOUT FRESH PREEXEC + CHAT PASS_TO_ASSIGN
Owner-facing WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Target Agent: FROM EXECUTABLE DISPATCH — never infer or substitute
Delivery owner: AGENT only when the executable Dispatch says so

## 1. Mission

Resolve FOX2 Bridge RC1 as one Whole-WP, not as Owner-facing micro-fixes.

The bounded engineering objective is:

~~~
source-bound recovery
-> WPF Desktop App
-> Artifact Vault
-> Worker/UI two-process lifecycle
-> stable launcher/startup
-> package/install/update/uninstall
-> installed-runtime certification
-> real installed poll
-> full regressions/security/diff checks
-> evidence publication
-> PRE-CANARY READY candidate for independent audit
~~~

Do not stop merely because one defect is found. Fix defects that remain inside the same authorized scope and continue until all pre-Canary gates PASS or one genuine material STOP condition remains.

Operational retries, XAML fixes, installer fixes, lifecycle fixes, test repair and evidence repair remain inside this WP.

## 2. Immutable source binding

Task branch:
work/FOX2-BRIDGE-DESKTOP-BATCH-B

Current reconciliation source-freeze:
c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359

Primary task:
docs/agent_handoff/FOX2-BRIDGE-DESKTOP-BATCH-B/task.md

Current source/trust-root manifest:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_CURRENT_SOURCE_SET.json

Current reconciliation record:
reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_RECONCILIATION_001.json

RC1 planning sources:
- reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_RELEASE_PLAN.md
- reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_ACCEPTANCE.json
- reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_ROUTING_INTAKE.md
- reports/BRIDGE-DESKTOP-BATCH-B/evidence/rc1_plan/BRIDGE_RC1_DESKTOP_IMPLEMENTATION_SPEC.md

Project Dictionary:
docs/governance/FOX2_PROJECT_DICTIONARY_v1.json

Resolver Registry for this Whole-WP:
- Registry commit: b27f1085ee13d8dce56fd2735e100ea1616e6e23
- Registry path: docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json
- Registry authority: FOX2
- EFFECTIVE family-manifest commit: d8e2331674ef1921844f369bfa9e48b82a73c6a1
- Owner approval: d8e2331674ef1921844f369bfa9e48b82a73c6a1:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/OWNER_RELEASE_APPROVAL.json
- Scope: WP_ONLY_TRUST_BINDING for FOX2-BRIDGE-RC1-TO-INTERNAL-READY
- Global semantic promotion: NO
- main/merge/deploy/provider/broker/LIVE authority: NO

Run fox2-source-resolver read-only against that exact Registry before product implementation. Resolve the required families through Registry -> EFFECTIVE manifest -> immutable source commit/path -> SHA-256. The Owner approval receipt is the external release-authority evidence for this Whole-WP trust binding. Do not substitute main, filename recency, candidate governance, or the historical RC1 source-set as the Registry itself.

Resolve Policy, Routing, Dispatch Schema, Git-first Protocol, PreExec Protocol, Receipt Schema, CHAT Preflight Intake, Dictionary/generated binding and Bridge Technical Spec through the exact Registry above. Never select versions from filename, recency or main.

If the executable recovery Dispatch binds an evidence-only PreExec publication descended directly from this freeze, use the Dispatch-bound execution base. The INFRA_FAILED receipt commit 8011a29a23fe373e924bf4d1809718036171b211 is historical evidence only. Any other material source drift requires STOP.

## 3. No-replay / recovery state

Historical Dispatch 001:
FOX2-DISPATCH-BRIDGE-RC1-CODEX-001
Control commit: e2eff7ef5d30026757aa929807eeccc1d6d9d6f6
Disposition: STOPPED_NEEDS_RECONCILIATION / DO_NOT_REPLAY

Historical Dispatch 002:
FOX2-DISPATCH-BRIDGE-RC1-CODEX-002
Control commit: c007bb3795997ab1a8937e61f0a3ac6b2042f5f2
Result head: e85ccaadd1fb49664bae07ec71ab607368fc1f0d
Disposition: STOPPED_NEEDS_RECONCILIATION / DO_NOT_REPLAY

Dispatch 002 stopped before product implementation because the installed source-resolver required a compatible Registry plus independently validated release authority. That authority gap is now reconciled by the Owner-approved RC1 trust bundle at Registry commit b27f1085ee13d8dce56fd2735e100ea1616e6e23 and manifest/approval commit d8e2331674ef1921844f369bfa9e48b82a73c6a1.

Facts:
- no accepted product implementation was created by Dispatch 001 or 002;
- e85cca... added only bounded reconciliation evidence under reports/BRIDGE-DESKTOP-BATCH-B/**;
- Canary 009 was not claimed or executed;
- APP-BATCH-B remained paused;
- no main/PR/merge/deploy/provider/broker/LIVE action occurred.

NEVER replay Dispatch 001 or 002.

Recovery execution requires one new Dispatch with retry_of_dispatch_id = FOX2-DISPATCH-BRIDGE-RC1-CODEX-002, max_runs = 1, exact source/worktree/base binding and one selected Agent tuple.

## 3A. Probe-infrastructure recovery

The exact-head PreExec published at 8011a29a23fe373e924bf4d1809718036171b211 returned INFRA_FAILED because the WPF capability probe itself raised before dotnet build.

This is not a proven .NET/WPF capability failure. The source freeze c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359 corrects the probe to write real UTF-8 LF bytes and regression-tests the generated WPF project content.

Do not replay any earlier Dispatch. The fresh PreExec already PASSed at receipt publication commit 67e0147fc03e4396b3e58fe3d8863902e950d4ec for source c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359, including dotnet_wpf_build=PASS, Codex=PASS, eligible_agent_route=PASS, worktree=PASS and no competing writer. The later task-branch commits through e85ccaadd1fb49664bae07ec71ab607368fc1f0d changed only bounded PreExec/reconciliation evidence; no code/task/spec/capability binding changed. Therefore do NOT rerun PreExec solely because of those evidence-only descendants. Rerun only if a material source/code/task/capability/worktree drift is observed.

## 3B. Source-authority reconciliation

Dispatch 002 produced SOURCE_UNVERIFIED because the prior RC1 source-set was not a resolver Registry and did not itself provide independent release approval.

Owner subsequently issued an explicit release approval for the exact immutable sources already bound in FOX2_BRIDGE_RC1_CURRENT_SOURCE_SET_3, solely for this Whole-WP trust binding and without changing source bytes or granting protected authority.

CHAT published:
- Owner approval + ten EFFECTIVE per-family manifests at d8e2331674ef1921844f369bfa9e48b82a73c6a1;
- resolver-compatible Registry at b27f1085ee13d8dce56fd2735e100ea1616e6e23;
- Registry authority = FOX2;
- all family manifests bind source commit c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359 and exact source SHA-256;
- protected authority remains false for main/merge/deploy/provider/broker/LIVE.

This is a WP-scoped trust binding, not a global semantic promotion. Before coding, verify the Registry and manifests read-only with the installed source-resolver. If the exact chain verifies, continue the same Whole-WP; do not open another authority micro-task.



## 3C. Final technical closure after Dispatch 003

Dispatch 003 is historical and MUST NOT be replayed.

Dispatch 003 result head:
`dbaefdf686e06ffdf78b277288515deca9011710`

Fresh final-closure PreExec publication:
`0789e5d8c3944fdc078090f50f18fb2a3abe6b64`

Fresh PreExec source head:
`dbaefdf686e06ffdf78b277288515deca9011710`

Fresh routing evidence:
- Codex PASS;
- Copilot AUTH_REQUIRED / non-material;
- dotnet PASS;
- dotnet_wpf_build PASS;
- eligible_agent_route PASS;
- worktree PASS;
- competing writer NONE_OBSERVED.

The diff from `dbaefdf...` to `0789e5d...` is receipt-only. Use `0789e5d...` as execution base and preserve `dbaefdf...` as the product WIP source/result head.

CHAT result intake accepted these Dispatch 003 facts as already executed evidence:
- 399 Python tests PASS;
- 30 Desktop checks PASS;
- WPF Release build PASS;
- package determinism PASS;
- package `FOX2-Bridge-RC1.zip` SHA-256 `a0516aed3d69564c657dc557b7b09cfaab549d6ab04ce4132e9399b50ce5b4ac`;
- install/update/uninstall/startup/single-instance/process-separation/control-store/support bundle PASS;
- real installed poll PASS / NO_CHANGE / no claims or executions;
- Registry/source authority PASS;
- Canary 009 untouched;
- APP-BATCH-B paused;
- no main/PR/merge/deploy/provider/broker/LIVE action.

Do NOT rerun those gates merely to repeat evidence when there is no relevant code/package change.

### Final-closure objective

Close the remaining technical pre-Canary gap in the SAME Whole-WP:

1. prove a fresh Artifact Vault save initiated through the current installed WPF UI;
2. bind the proof to the current installed UI process and current installed package;
3. verify the newly selected source file SHA-256;
4. verify copied Vault object SHA-256 equals source SHA-256;
5. verify the new record is written atomically into the Vault index;
6. verify record state is exactly `LOCAL_SAVED`;
7. verify `git_synced=false` / not GIT_SYNCED;
8. verify `released=false`;
9. verify the saved record timestamp is newer than the current installed UI process start and this final-closure attempt start;
10. close all four gates together:
   - `ARTIFACT_LOCAL_SAVE=PASS`
   - `ARTIFACT_SHA256_VERIFY=PASS`
   - `ARTIFACT_ATOMIC_INDEX=PASS`
   - `LOCAL_SAVED_NOT_GIT_SYNCED=PASS`.

The proof MUST traverse the installed UI save path. A direct service/assembly call, stale Vault record, Core-only test, pre-existing object, or PowerShell remainder-harness PASS is not sufficient.

Use a fresh synthetic benign file with unique content/name for the attempt. Record before/after Vault index state, installed UI PID/process-start time, installed package hash, source path/hash, resulting artifact ID/path/hash/state, and attempt timestamps in bounded evidence.

### Repair policy

First try certification with no product-code changes.

If the installed UI save cannot be driven or observed because of a genuine product defect, repair only the minimum in-scope code under `agent_bridge/**`, then:
- rebuild/repackage/reinstall only as required by that change;
- rerun tests and installed gates materially affected by that change;
- preserve prior PASS evidence for unaffected gates;
- update the evidence manifest truthfully.

Do not add a test-only production bypass that skips the actual installed UI interaction.

If the remaining failure is only host UI-automation tooling and the product path itself is demonstrably functional, collect a fresh human-observable/UIAutomation receipt only if it still proves the actual installed UI action end-to-end. Never convert a direct service call into UI acceptance.

### Icon disposition

The branded FOX2 icon is NOT a normative RC1 acceptance gate in the bound task/technical spec. No authorized branded icon asset exists in the bound source. Keep the current generic Windows icon for RC1 and record `ICON_NON_GATING_NO_AUTHORIZED_ASSET`. Do not fabricate or source an unapproved icon and do not block pre-Canary technical readiness on it.

### Final-closure completion

If all four Artifact Vault gates PASS and no newly affected required gate fails:
- update report/evidence manifest/acceptance gates;
- mark installed runtime technical certification PASS;
- keep `PRECANARY_INDEPENDENT_AUDIT=PENDING`;
- push only authorized task-branch paths;
- remote-readback exact bytes;
- finish with `FOX2_BRIDGE_RC1_IMPLEMENTATION_PUSHED_UNREVIEWED`.

If a genuine material blocker remains after bounded repair:
- preserve truthful failure evidence;
- push bounded evidence/WIP;
- finish with `FOX2_BRIDGE_RC1_STOPPED_NEEDS_RECONCILIATION`.

Do not claim `FOX2_BRIDGE_RC1_PRECANARY_READY`; CHAT/WORK own the independent audit and that marker.

## 4. Singular pre-execution gate

Do not implement until executable Dispatch proves CHAT already completed:

POLICY_CHECK -> TASK_STATE_CHECK -> ROUTING_R0_R7 -> ASSIGNMENT_CHECK -> PASS_TO_ASSIGN

Fresh PreExec must materially prove:

~~~
git
python
pwsh
schtasks.exe
dotnet
dotnet_wpf_build
local_appdata_per_user_write
eligible_agent_route
worktree ownership
no competing writer
~~~

dotnet_wpf_build is mandatory. A dotnet version check alone is insufficient.

Selected Agent/model/reasoning/permission come only from executable Dispatch.

## 5. Writable boundary

Allowed code:
agent_bridge/**

Allowed reports/evidence:
reports/BRIDGE-DESKTOP-BATCH-B/**

Everything else is READ-ONLY.

No APP-BATCH-B edits. No main push. No PR. No merge. No deploy. No provider write. No broker write. No LIVE. No Canary 009 mutation.

## 6. Final RC1 product shape

Build one coherent installed product:

~~~
FOX2 Bridge RC1
├─ corrected Python Bridge core
├─ .NET 8 WPF Desktop App / MVVM
├─ local Artifact Vault
├─ stable launcher
├─ independent Worker process
├─ independent Desktop UI process
├─ current-user startup integration
└─ deterministic package/install/update/uninstall lifecycle
~~~

Required topology:

~~~
stable launcher
  +--> Python Bridge Worker
  +--> FOX2 Bridge Desktop App
~~~

Desktop App is never Worker owner. GUI crash/close/restart must not stop Worker.

Worker remains owner of Git polling, dispatch validation, durable ledger/replay protection, Agent invocation and result delivery.

Desktop App is presentation/control only.

## 7. Desktop App contract

Technology: .NET 8, WPF, MVVM, native Windows.

Screens:
Dashboard, Activity, Agents, Diagnostics, Artifacts, Settings.

Visual baseline:
background #0B1017
surface #111923
elevated #17212D
border #263241
FOX Orange #F59E0B
info #38BDF8
success #22C55E
critical #EF4444
primary #F4F7FA
secondary #9CA9B7
muted #647383
Segoe UI Variable / Segoe UI

Required UX corrections:
- Check Now must not imply pause bypass; disable or relabel appropriately while PAUSED.
- While PAUSED show polling paused, not a fake countdown.
- Copilot UNVERIFIED must render as Available / auth unverified or equivalent, never Ready/authenticated.
- Raw branch details stay in Diagnostics.
- No placeholder CLI versions.
- Selected navigation state is visible.
- Keyboard focus/basic accessibility/AutomationProperties exist on actionable controls.
- Use a real FOX2 app icon if an authorized source asset exists; otherwise report icon as an explicit remaining acceptance item instead of fabricating one.

Desktop App is single-instance per interactive user.
Closing X hides to Tray and leaves Worker running.

Tray:
Open Dashboard / Pause-Resume / Check now / Open Logs / Exit after current task.

Only explicit graceful exit requests Worker shutdown.

## 8. Fixed control boundary

Desktop App may invoke only:

~~~
control status
control pause
control resume
control check-now
control request-exit
control open-logs
control set-start-with-windows --enabled true|false
diagnostics --output <bounded path>
~~~

Desktop App must not:
- call poll-once, run-next or e2e-once;
- run Git directly;
- read/write Bridge SQLite directly;
- invoke Codex/Copilot directly;
- execute arbitrary shell;
- select routing/model/reasoning/permission;
- grant release/LIVE authority.

Process launching must use argument lists, hidden/no-console execution, bounded timeout, concurrent stdout/stderr drain, safe error display and controlled environment.

## 9. Artifact Vault v1

Root:
%LOCALAPPDATA%\FOX2\BridgeDesktop\Artifacts

Required flow:

~~~
explicit user file selection
-> validate size/path
-> SHA-256 source
-> content-addressed copy
-> SHA-256 copied object
-> exact hash match
-> atomic index write
-> LOCAL_SAVED
~~~

Canonical semantics:
LOCAL_SAVED != GIT_SYNCED != RELEASED

RC1 implements LOCAL_SAVED only.

Vault must not run Git, mutate Bridge ledger, invoke Agents, claim Source Authority, mark RELEASED or grant DEV/merge/LIVE authority.

## 10. Launcher / package / lifecycle

Integrate WPF into the existing per-user deterministic Bridge package.

Required:
- one stable launcher starts Worker and Desktop independently;
- Worker startup does not depend on UI success;
- UI startup never creates a second Worker;
- no visible console in normal use;
- atomic installed package pointer;
- update installs complete new version before pointer switch;
- failed update leaves prior valid version usable;
- uninstall removes owned binaries while preserving intended durable config/data/logs/reports/artifacts;
- repositories/worktrees are never deleted;
- Start with Windows is current-user/limited/interactive, never SYSTEM by default;
- CLI control/diagnostics remain usable without GUI;
- old PowerShell Tray must not remain a competing primary UI after WPF is authoritative.

## 11. One Whole-WP execution strategy

Proceed continuously:

~~~
A inspect launcher/install/runtime contracts
B implement WPF shell + fixed control client + singleton
C implement Artifact Vault
D integrate launcher/startup/package/update/uninstall
E implement/update automated tests
F build WPF on Windows
G run focused lifecycle/contract tests
H run full Bridge regression
I build deterministic RC1 package
J install per-user and certify first-run/startup/update/uninstall
K prove real installed safe poll/control-store path
L run changed-path/secret/diff checks
M publish complete evidence/result once
~~~

If a test reveals an in-scope defect, repair it and continue. Do not request a new micro-task unless the fix crosses source authority, writable scope, selected Agent authority or release/LIVE boundary.

## 12. Required pre-Canary technical gates

All applicable gates must execute and PASS:

~~~
SOURCE_BINDING
FRESH_PREEXEC
DOTNET_WPF_BUILD_CAPABILITY
DESKTOP_APP_BUILD
DESKTOP_APP_CONTRACT_TESTS
DESKTOP_APP_SINGLE_INSTANCE
WORKER_UI_PROCESS_SEPARATION
FIRST_RUN_SETUP
PER_USER_INSTALL
INSTALLER_PACKAGE
UPDATE_PATH
UNINSTALL_PATH
START_WITH_WINDOWS
STARTUP_SINGLE_INSTANCE
PAUSE_RESUME
CHECK_NOW
OPEN_LOGS
SUPPORT_BUNDLE
ARTIFACT_LOCAL_SAVE
ARTIFACT_SHA256_VERIFY
ARTIFACT_ATOMIC_INDEX
LOCAL_SAVED_NOT_GIT_SYNCED
PROJECT_DICTIONARY_BINDING
DISPATCH_V3_SCHEMA_BINDING
DISPATCH_V3_STRUCTURAL_CONFORMANCE
DISPATCH_V3_RUNTIME_COMPATIBILITY
V2_COMPATIBILITY
V06_COMPATIBILITY
REAL_INSTALLED_POLL
CONTROL_STORE_PATH
FULL_BRIDGE_TESTS
CHANGED_PATH_ALLOWLIST
SECRET_SCAN
GIT_DIFF_CHECK
~~~

PRECANARY_INDEPENDENT_AUDIT is owned by WORK/CHAT after this implementation result. The implementation Agent prepares evidence but never self-certifies that independent gate.

## 13. Canary boundary

Canary 009 is OUTSIDE this execution.

Identity:
FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001

Branch:
work/FOX2-BRIDGE-FINAL-CANARY-009

Preserved head:
501822a33ef08c7365154913bbc677544856eee5

Do not edit, replace, claim, execute, create Canary 010, or write a Canary result.

Only CHAT may open Canary after independent audit and FOX2_BRIDGE_RC1_PRECANARY_READY.

## 14. Evidence and delivery

Before coding verify exact branch/worktree/base, clean WIP, no competing writer, exact source/task/prompt/Dispatch binding and required capabilities.

During execution keep code under agent_bridge/** and evidence under reports/BRIDGE-DESKTOP-BATCH-B/**.

Never rewrite historical immutable evidence to manufacture PASS.

At completion:
- run required tests;
- changed-path allowlist;
- secret scan;
- git diff --check;
- stage only authorized paths;
- commit;
- push exact non-main task branch;
- verify remote SHA/readback.

Expected final report artifacts:
reports/BRIDGE-DESKTOP-BATCH-B/report.md
reports/BRIDGE-DESKTOP-BATCH-B/evidence_manifest.json
reports/BRIDGE-DESKTOP-BATCH-B/evidence/**

Result remains PUSHED_UNREVIEWED until CHAT intake.

## 15. Genuine STOP conditions

STOP only for a material condition:
- source/task/prompt/Dispatch mismatch;
- wrong branch/worktree/base;
- competing writer;
- selected Agent capability/auth/quota failure;
- required fix crosses allowed source/authority;
- Desktop App would require direct Git/ledger/Agent execution;
- Worker/replay safety cannot be preserved;
- installer/update/uninstall cannot be made safe inside scope;
- secret/private exposure;
- required test/security failure remains unresolved after bounded repair;
- push/remote-readback failure;
- Canary 009 claim/execution;
- APP-BATCH-B resume;
- main/PR/merge/deploy/provider/broker/LIVE action.

After Agent start, uncertain failure is NEEDS_RECONCILIATION. Never blind replay.

## 16. Completion contract

Successful bounded implementation + technical pre-Canary certification must finish exactly with:

FOX2_BRIDGE_RC1_IMPLEMENTATION_PUSHED_UNREVIEWED

A genuine material STOP must finish exactly with:

FOX2_BRIDGE_RC1_STOPPED_NEEDS_RECONCILIATION

Before the marker, report:
- exact local/remote commit SHA;
- changed paths;
- test counts/results;
- package identity/hash if built;
- installed-runtime result;
- real-poll result;
- remaining independent gate PRECANARY_INDEPENDENT_AUDIT;
- Canary 009 untouched;
- no main/merge/deploy/provider/broker/LIVE action.

## 17. Anti-fragmentation rule

This prompt deliberately replaces piecemeal Bridge execution.

Do not create Owner-facing child tasks for WPF, Artifact Vault, launcher, installer, update, uninstall, startup, test repair, packaging repair, evidence repair or local reconciliation. Those are internal stages of FOX2-BRIDGE-RC1-TO-INTERNAL-READY.

Create a new task only for a genuine material source/authority boundary that cannot be resolved inside this Whole-WP.
