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

Machine registry:
docs/governance/FOX2_PROJECT_DICTIONARY_v1.json

Resolve Policy, Routing, Dispatch Schema, Git-first Protocol, PreExec Protocol, Receipt Schema and CHAT Preflight Intake from the current Dictionary/source-set manifest. Never select versions from filename, recency or main.

If the executable recovery Dispatch binds an evidence-only PreExec publication descended directly from this freeze, use the Dispatch-bound execution base. The INFRA_FAILED receipt commit 8011a29a23fe373e924bf4d1809718036171b211 is historical evidence only. Any other material source drift requires STOP.

## 3. No-replay / recovery state

Prior Dispatch:
FOX2-DISPATCH-BRIDGE-RC1-CODEX-001

Prior control commit:
e2eff7ef5d30026757aa929807eeccc1d6d9d6f6

Disposition:
STOPPED_NEEDS_RECONCILIATION

Facts:
- Agent started only to perform source/capability verification.
- No accepted product implementation/result was published.
- Canary 009 was not claimed or executed.
- APP-BATCH-B remained paused.
- No main/PR/merge/deploy/provider/broker/LIVE action occurred.

NEVER replay Dispatch 001.

Recovery execution requires a new Dispatch with retry_of_dispatch_id = FOX2-DISPATCH-BRIDGE-RC1-CODEX-001, max_runs = 1, exact source/worktree/base binding and one selected Agent tuple.

## 3A. Probe-infrastructure recovery

The exact-head PreExec published at 8011a29a23fe373e924bf4d1809718036171b211 returned INFRA_FAILED because the WPF capability probe itself raised before dotnet build.

This is not a proven .NET/WPF capability failure. The source freeze c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359 corrects the probe to write real UTF-8 LF bytes and regression-tests the generated WPF project content.

Do not replay any earlier Dispatch. Run exactly one fresh PreExec on c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359. Only a durable PASS receipt may open the recovery Dispatch.

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
