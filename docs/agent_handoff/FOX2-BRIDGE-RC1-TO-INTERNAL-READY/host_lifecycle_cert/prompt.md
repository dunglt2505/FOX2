FOX2 — CODEX EXECUTION PROMPT — CURRENT-PACKAGE OWNER-HOST LIFECYCLE CERTIFICATION A01

Role: CODEX — Primary host-lifecycle certification owner
Model: gpt-6.1-sol
Thinking: high
Mode: Execute bounded TEST certification end-to-end
Project: FOX2 only
Repository: dunglt2505/FOX2
Branch: work/FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-20261021
Permission profile: FULL_ACCESS only within this task
Max Agent attempts: 1
No replay / no model substitution

TASK ID

FOX2-BRIDGE-RC1-HOST-LIFECYCLE-CERT-A01

Do not assume or hard-code a future Dispatch sequence number.

The Owner launcher must remote-verify one exact fresh executable Dispatch before this CODEX process starts. Treat only that verified Dispatch as executable.

IMMUTABLE TASK

Path:
docs/agent_handoff/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/host_lifecycle_cert/task.md

Task commit:
d95f08ceed2f5a25ad288b9630ffc87b698f329c

Task blob SHA-1:
86e0afaec6f6e47c9d15b51564a38bf5167a892b

Task raw SHA-256:
95d64b3cb3999c55700ded2a6451cd9ffa23872fb87fd00c97df7edbb8c06221

ACCEPTED SOURCE

Accepted source/result base:
2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb

Accepted implementation:
fab3642b818415428ae3f67965430e3ea0b11401

CHAT A03 review:
37691b71b64de03091de9908014da2256c1d2901

This source includes the accepted corrected stable-external lifecycle harness.

EXECUTION START

The current HEAD at process start must equal the exact fresh Dispatch runtime_contract.base_sha verified by the Owner launcher.

The accepted source 2faa33f9... must be an ancestor.

Pre-start changes after 2faa33f9... may contain only this task/prompt/PreExec/receipt evidence. No product-code drift is permitted.

HOST-MUTATION AUTHORITY

This task authorizes only the per-user Bridge package lifecycle required for Phase 2 TEST:

1. build exact package from accepted source;
2. install/update exact package using supported per-user installer;
3. establish/verify safe paused state;
4. run corrected lifecycle certification;
5. stable external uninstall exactly once;
6. reinstall exact same package;
7. verify durable state and final installed state;
8. bounded recovery to reinstall the same exact package if needed after a failure.

This authority does NOT extend to:
- AppLocker;
- AppIDSvc;
- FOX2F1Authority service;
- ProgramData authority ACL;
- reboot;
- G3/G4;
- Canary;
- main/PR/merge;
- provider/broker/LIVE.

PRE-MUTATION RULES

Before first package mutation:

1. verify exact branch/runtime base/task/prompt/PreExec/Dispatch;
2. verify clean worktree and one writer;
3. verify source 2faa33f9... ancestor and no pre-start product drift;
4. verify PowerShell 7, Python, Git, CODEX, dotnet and an already-existing compatible isolated build Python;
5. do not install tools or dependencies to make capability pass;
6. build package outside BridgeRoot;
7. verify package SHA-256 and manifest;
8. require package manifest source_git_commit exactly:
   2faa33f9ab4d06bcc51c8fd1d2c7040fc06a29cb
9. capture bounded pre-state evidence;
10. if any gate fails, STOP before host mutation.

PACKAGE BUILD

Use:
agent_bridge/scripts/build_user_package.py

Use only an already-existing isolated build Python that satisfies the script's own environment checks.

The package file must live outside BridgeRoot and remain available for the full lifecycle and bounded recovery.

Record:
- build Python identity/version without secrets;
- package path alias, not private user-specific path in committed evidence;
- package SHA-256;
- package manifest;
- source_git_commit;
- dictionary/source identities;
- deterministic/provenance checks performed.

Do not commit package binaries.

REAL LIFECYCLE

Follow task.md exactly.

Install/update with:
agent_bridge/scripts/install_user.ps1

Then establish required paused state.

Run:
agent_bridge/scripts/certify_user_lifecycle.py

with exact package, SHA-256 and bounded evidence output.

The corrected lifecycle harness must use stable external BridgeRoot/uninstall.ps1 exactly once.

Do not invoke installed Python for uninstall.

FAILURE / RECOVERY

Once host mutation begins, preserve the first observed failure.

Never rerun the lifecycle certification or stable uninstall in this Dispatch.

If a post-mutation failure leaves Bridge unavailable, bounded recovery may reinstall the same exact accepted package from the retained external package file.

Recovery success does NOT turn lifecycle FAIL/BLOCKED into PASS.

Record original failure and recovery separately.

CODE WRITES

No product, script or test edits are allowed.

If any source/code fix appears necessary, STOP and report REWORK_REQUIRED. Do not modify code in this host-certification task.

REPOSITORY WRITE PATHS

Only:
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/report.md
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence_manifest.json
- reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/host_lifecycle_cert/**

Required result must preserve historical A03 and Batch-B evidence by Git history; do not rewrite historical FAIL.

VALIDATION

Required:
- exact source/package provenance;
- real install/update result;
- real corrected uninstall result;
- real reinstall result;
- durable config/data/manual consumption preservation;
- final exact installed pointer/receipt;
- paused/final health state;
- no old Dispatch replay;
- no G3/G4 mutation;
- changed-path allowlist;
- git diff --check;
- bounded secret scan;
- K1 UNEXPLAINED=0;
- Result Contract v2.

REAL HOST EVIDENCE

Do not commit:
- raw config contents;
- database contents;
- passwords/tokens;
- raw prompts;
- private account data;
- unnecessary full local paths.

Use hashes, bounded sanitized summaries and path aliases.

GIT DELIVERY

After certification:

1. write/update only authorized report/evidence paths;
2. validate Result Contract v2;
3. commit evidence;
4. push only the authorized non-main branch;
5. independently read remote branch head;
6. return observed remote result SHA outside committed report.

Do not claim CHAT acceptance.

Final submission state is PUSHED_UNREVIEWED.

STOP

STOP before mutation on missing capability, source drift, dirty worktree, competing writer, unsafe installed state, package provenance mismatch or missing fresh PreExec.

After mutation begins, do not blindly retry. Preserve first failure and use only the bounded same-package recovery defined above.

Return truthful PASS / FAIL / BLOCKED / NEEDS_RECONCILIATION boundaries.
