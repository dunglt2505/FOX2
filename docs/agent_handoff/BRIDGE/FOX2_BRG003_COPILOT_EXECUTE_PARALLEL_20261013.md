# FOX2 — COPILOT EXECUTION PROMPT — BRG-003 SANITIZED SOURCE BASELINE
Date: 2026-10-13
Execution mode: MANUAL_LOCAL_START / AUTONOMOUS_BOUNDED_EXECUTION / STOP_AT_PUSHED_UNREVIEWED
Agent lane: COPILOT / BRIDGE BOOTSTRAP
Issue: https://github.com/dunglt2505/FOX2/issues/10

## 0. CHAT routing decision
This prompt is the executable handoff for BRG-003 under FOX2 Policy V1.8.4 and Routing Index V1.2.5.

Routing result:
- target architecture: CHAT -> Git control plane -> Local Bridge -> Agent -> Git result -> CHAT review
- actual stage: BOOTSTRAP
- execution path class: BOOTSTRAP_PATH
- current trust mode: BOOTSTRAP_PINNED_GIT
- Agent choice: COPILOT
- reason: existing clean BRG-003 Windows worktree/source context, lowest rework, file scope disjoint from CODEX P2-01
- WORK: not required for this bounded import
- CODEX: forbidden from this worktree/scope
- CHAT: owns Git/source/readback/acceptance
- OWNER_SCOPE_APPROVED=YES
- CHAT_ASSIGNMENT_CHECK=PASS_CONDITIONAL_ON_IMMEDIATE_LOCAL_RUNTIME_CHECK

If the local runtime check below PASSes, this prompt activates:
`CODE_ALLOWED=YES_FOR_BRG003_SANITIZED_IMPORT_ONLY`
`GIT_CODE_PUSH=YES_OWN_BRANCH_ONLY`

No further Owner approval is required inside this WP.

## 1. Authoritative sources
Read and bind exactly:

### FOX2 Policy
- Version: V1.8.4 RELEASED_EFFECTIVE
- Library SHA256: `481790b2512ea1cd4891fe1b03258175d68d9bfae71158d19283bd003c560f5a`
- Git: `a366f509899cec97f64316cb111b29a3849325b5:docs/governance/FOX2_POLICY_V1.8.4.md`
- Blob: `483a74ff39339e653bbd7bbfba0feaf7b1c003e9`

### Routing Index
- Version: V1.2.5 EFFECTIVE_DERIVATIVE
- Git: `7b6e30e0712071da3a576e1ebda2dce364aa7dff:docs/governance/FOX2_AGENT_PROMPT_POLICY_V1_2_5_EFFECTIVE_ROUTING_INDEX_20261013.md`
- Blob: `3ea18c06af93cd059b7e29c6f09914ac4a0298a7`

### Bridge Technical Spec
- Version: v0.5 RELEASED_EFFECTIVE
- SHA256: `2d182972b5edd6ccfd72c83b07d97907fa7fb63ed6eaa4de68b03b7e5165740a`
- Git: `8010a121e1d8b3f244da7dd856931b1bce41da21:docs/architecture/FOX2_LOCAL_AGENT_BRIDGE_TECHNICAL_SPEC_v0.5.md`
- Blob: `1ce788e84628764f1b58459e93aecd5c7fde641e`

### Accepted 20-file source manifest
- Git: `8c217d122f171de5bfef9b2c7cca6c823cd32eaa:docs/agent_handoff/BRIDGE/FOX2_BRG003_20FILE_HASH_RECONCILIATION_20261013.json`
- Blob: `3ef8852964214c99161ed9ff4e463cb677af51cd`

Do not rerun historical report-to-report reconciliation unless local source bytes now differ.

## 2. Exact local ownership
Source project:
`C:\Projects\FOX2-AgentBridge`

Target FOX2 worktree:
`C:\Projects\FOX2-worktrees\FOX2-BRG-003`

Target branch:
`work/FOX2-BRG-003-SOURCE-BASELINE-copilot`

Expected initial HEAD:
`c8a0d517b8655868053e4923f5947c12975a5865`

Remote target branch now exists at the same base.

Writer lease:
- COPILOT ONLY on this exact worktree/branch
- CODEX and other Agents MUST NOT write here

Allowed repository scope:
`agent_bridge/**`

Everything outside `agent_bridge/**` is denied.

## 3. Immediate local runtime check — do this first
Perform only the minimum current-state checks:
1. `git rev-parse HEAD`
2. `git branch --show-current`
3. `git status --short --branch --untracked-files=all`
4. verify origin is `dunglt2505/FOX2`
5. verify no `index.lock`
6. verify this exact worktree is not owned by another active writer/process
7. verify remote branch exists and points to the expected initial base before first write
8. verify the 20 source files in `C:\Projects\FOX2-AgentBridge` still match the accepted path/size/SHA256 manifest
9. observe actual Copilot model/mode/quota only if exposed; use `NOT_EXPOSED` honestly

Do NOT:
- reset, rebase, stash, clean or checkout another branch;
- inspect/delete/modify SQLite DB/WAL/SHM sidecars;
- inspect `.venv`, logs, caches, `control.git` or generated artifacts beyond filename-level exclusion needed to avoid copying them;
- install packages or use network package installers.

STOP if:
- branch/HEAD mismatch;
- dirty/untracked WIP not created by this run;
- collision/active writer;
- source hash drift;
- actual source contains a real secret;
- target remote branch has unexpected commits.

If runtime check PASSes, continue automatically. Do not ask Owner again.

## 4. Import exactly the accepted source baseline
Create/populate only:
`agent_bridge/**`

Copy the accepted 20 files into the target prefix preserving their relative paths:

- `agent_bridge/pyproject.toml`
- `agent_bridge/README.md`
- `agent_bridge/src/fox2_agent_bridge/**` from the accepted manifest
- `agent_bridge/tests/**` from the accepted manifest

Also create:
`agent_bridge/.gitignore`

The .gitignore MUST exclude at least:
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `*.egg-info/`
- `.env`
- `.env.*`
- `*.db`
- `*.db-shm`
- `*.db-wal`
- logs/cache/temp generated files appropriate to this package

## 5. Sanitize COPIES only
Do not modify the original `C:\Projects\FOX2-AgentBridge` source.

Resolve only the already-known publication issues in the target copies:
1. user-specific absolute Windows paths in config/tests -> portable/synthetic test paths;
2. `ghp_`-shaped test tokens -> construct synthetic test values at runtime or replace with clearly non-secret safe fixtures that still exercise parsing/redaction semantics;
3. credential-in-URL fixtures -> clearly fake/non-secret URI values;
4. email-like fixtures -> clearly synthetic test values when they are not semantically required.

Do not weaken the tests just to remove the fixture shape. Preserve the behavior being tested.

Explicitly DO NOT import:
- `config/bridge.example.toml`
- `reports/BRG-010.md`
- `reports/BRG-020.md`
- runtime DB/sidecars
- logs
- `.venv`
- caches
- generated metadata
- any other file not listed in the accepted 20-file manifest

## 6. Security and integrity checks
Before commit:
- compare imported path count against expected 20 source files + `.gitignore` + optional task result report created by this run;
- document every intentional sanitized delta from the accepted source SHA;
- scan target/staged content for real secret patterns;
- ensure no absolute personal Windows path remains in imported target content unless explicitly required and safely synthetic;
- `git diff --check`;
- verify `git status` shows changes only under `agent_bridge/**`.

Do not claim imported files are byte-identical after sanitization. Report exact changed paths and reasons.

## 7. Offline tests
No provider/network activity.

Run from `agent_bridge` using already-installed tooling only:
- Python syntax/import smoke appropriate to the package;
- `python -m pytest -q` if pytest is already available;
- package-specific offline tests only;
- no package installation and no external HTTP/provider calls.

If a dependency required for the accepted existing test suite is missing, STOP with `BLOCKED_TOOLCHAIN`; do not install it without CHAT review.

If tests expose defects inside `agent_bridge/**`, you MAY fix them only when:
- fix is within BRG-003 sanitized-baseline scope;
- it does not implement later BRG-010..040 feature work;
- tests remain offline.
Otherwise STOP and report.

## 8. Result evidence
Create a sanitized result file:
`agent_bridge/reports/BRG-003_RESULT.md`

Include:
- source manifest identity;
- initial/final HEAD;
- imported file inventory;
- sanitization delta;
- secret-scan result;
- tests/commands/results;
- actual model/mode/quota if exposed;
- final `git status`;
- STOP conditions encountered, if any.

No credentials, raw environment secrets or DB contents in the report.

## 9. Commit and push
Only after all required checks PASS:
1. stage only `agent_bridge/**`
2. commit with a clear BRG-003 message
3. push ONLY:
   `work/FOX2-BRG-003-SOURCE-BASELINE-copilot`
4. read back the remote branch head if possible

Do NOT:
- push/main/merge/rebase/force-push;
- open a PR unless CHAT later requests it;
- edit docs/governance/architecture/backend/source_freshness/frontend;
- start BRG-010..040 in this run;
- launch another Agent.

## 10. Final response format
Return exactly:

```text
FOX2 BRG-003 COPILOT RESULT

POLICY_READBACK:
ROUTING_INDEX_READBACK:
BRIDGE_SPEC_READBACK:
SOURCE_MANIFEST_READBACK:

ACTUAL_MODEL:
ACTUAL_MODE:
QUOTA_STATUS:

WORKTREE:
BRANCH:
INITIAL_HEAD:
FINAL_LOCAL_HEAD:
REMOTE_HEAD:
CLEAN_BEFORE:
CLEAN_AFTER:
WRITER_COLLISION:

SOURCE_HASH_CHECK:
IMPORTED_SOURCE_FILE_COUNT:
SANITIZED_DELTA:
EXCLUDED_FILES:
SECRET_SCAN:

TESTS:
TEST_RESULT:

COMMIT:
PUSH:
RESULT_REPORT:

EXECUTION_STATE:
  PUSHED_UNREVIEWED
  | BLOCKED_SOURCE
  | BLOCKED_COLLISION
  | BLOCKED_SECRET
  | BLOCKED_TOOLCHAIN
  | BLOCKED_TEST
  | BLOCKED_PUSH
  | BLOCKED_SCOPE
  | BLOCKED_OTHER

OPEN_GATES:
STOP_REASON:
```

STOP at `PUSHED_UNREVIEWED`. CHAT performs remote independent acceptance.
