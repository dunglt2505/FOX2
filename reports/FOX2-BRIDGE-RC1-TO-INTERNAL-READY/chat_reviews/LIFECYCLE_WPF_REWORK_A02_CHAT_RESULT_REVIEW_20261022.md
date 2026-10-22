# FOX2 — CHAT Result Review — Lifecycle/WPF Contract Rework A02

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Task: `FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-CODEX-001`
Result branch: `work/FOX2-BRIDGE-RC1-LIFECYCLE-WPF-CONTRACT-REWORK-A02-20261022`
Observed result SHA: `085cc8302e824dbccf9cbef80422ed48894b9cb4`

## Verdict

**CHAT_ACCEPT — A02 BUILD LIFECYCLE/WPF CONTRACT REWORK ONLY**

This accepts the bounded A02 source/test/evidence correction. It does not certify the real installed-host lifecycle and does not authorize G3/G4/Canary/main/merge/provider/broker/LIVE.

## Immutable execution chain

Verified:
- recovery snapshot: `1a11fa0b232a69f0c26a0b4029c331ee2a8c840f`;
- original runtime base: `e7d5acf51dddcbc95324a992ad6be2773e61285f`;
- A02 task: `f796306ca4e79b9ab61cd436cf69a5f28ede4faf`;
- task blob: `3beb3bf2f3c2a76dcd8b10308f3670da98e70424`;
- task SHA-256: `7bfe425ad18f372960fb0440cd8694fb1a2a86edd7bd10cac5b105817f73d58c`;
- A02 prompt: `56e4c1eeb9341062fdb8ec52110e4e5c44c329e2`;
- prompt blob: `faef3f5cf4b6d286d7a30cb4200c6b6526ed55b2`;
- prompt SHA-256: `a9b07516ce8f5b31ffb7b404f993407855cb1449f28be244011902630df5f201`;
- PreExec REV3 PASS receipt: `4504bf95dd2baf474b30f896b23365c52fe10c9f`;
- PreExec receipt blob: `827fb02b57a49483b8a5be7589170d38cbb9df59`;
- PreExec receipt SHA-256: `0d265137e1567a2b47999e99716cacca9c6121bb2ac606688b949b4f88aa6c2f`;
- PASS_TO_ASSIGN: `61b75156bb4b241b88a26c0c11cb8af79f79a94b`;
- Dispatch commit: `126e8d857e7e4964fe05a47d558215763779535f`;
- Dispatch blob: `0997c8126e24dbf973949fb14610324b49b99bdc`;
- Dispatch SHA-256: `b4ee5b36de3a85318dafcafcc2593b2f4c94433f8c82a723264743324cc02aac`;
- runtime base: `4504bf95dd2baf474b30f896b23365c52fe10c9f`;
- result SHA: `085cc8302e824dbccf9cbef80422ed48894b9cb4`.

A01/CODEX-001 remains historical `EXITED_CONSUMED`, no result, no CHAT acceptance and **NO_REPLAY**.

## Git result provenance

Result branch independently read back at exact result SHA.

Runtime base -> result:
- status: ahead;
- exactly 1 commit;
- merge base equals runtime base;
- 25 changed paths;
- unauthorized paths: 0.

Final remote readback:
- result branch == result SHA;
- control branch == exact A02 Dispatch commit.

The result report remains `PUSHED_UNREVIEWED`; this separate CHAT receipt is the acceptance authority.

Git commit author metadata is `Copilot`, but actor provenance is not inferred from that label. CODEX execution is independently proven by the immutable Dispatch, durable consumed attempt claim, observed CODEX process and one-writer evidence. This metadata mismatch is recorded as non-material for A02 acceptance.

## Code review / K1

Material code/test changes are only:
- `agent_bridge/scripts/certify_user_lifecycle.py`;
- `agent_bridge/tests/test_lifecycle_wpf_contract.py`;
- `agent_bridge/tests/test_rc1_package.py`.

Reviewed A02 corrections:
1. absent `current_dispatch` now fails closed instead of being treated as null;
2. WPF process observation uses PowerShell error-stop semantics and requires an explicit JSON array;
3. only Windows sharing-violation `winerror=32` proves the live presentation lock; access denied/other errors fail;
4. negative fixtures cover query failure/timeout/null result/PID drift/unsafe state changes;
5. package fixture models FileShare.None with `winerror=32`.

The presentation contract remains WPF-only, uses stable `BridgeRoot/launch.ps1`, keeps Worker/F1 `NOT_APPLICABLE_PRE_G3`, reuses the unchanged UI inspect/check/exit seam and performs graceful UI exit before uninstall.

K1 result:
- REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED only;
- **UNEXPLAINED = 0**.

## Tests and retained failures

Focused lifecycle/WPF + launcher + package + installation:
- **103 passed in 3.34s**
- exit 0.

Full `agent_bridge/tests`:
- **653 passed in 236.02s**
- exit 0;
- no long-path process override required.

Historical intermediate static-validation failures caused by whitespace in generated evidence are preserved in `static_validation_history.json`; they are not rewritten as PASS. Final generated evidence was corrected and final `git diff --check` is exit 0.

## Static / security / immutable boundaries

Verified:
- Python syntax/static checks PASS;
- generated PowerShell syntax PASS;
- changed-path allowlist PASS;
- forbidden production-file byte identity PASS;
- A03 uninstall AST identity PASS;
- final `git diff --check` PASS;
- bounded secret scan PASS;
- recovery provenance byte identity PASS;
- Result Contract v2 manifest validation PASS.

Protected source paths are not in the result diff, including:
- `agent_bridge/src/fox2_agent_bridge/launcher.py`;
- `agent_bridge/src/fox2_agent_bridge/f1_service.py`;
- `agent_bridge/src/fox2_agent_bridge/installation.py`;
- `agent_bridge/scripts/certify_rc1_ui.ps1`;
- `agent_bridge/desktop_app/**`.

`test_rc1_launcher.py` is unchanged and was rerun.

## Independent manifest/hash review

Effective Result Schema v2 blob:
`b7617cc5c75c288c7997c64536a22fb836b8200b`.

Independent schema validation of `evidence_manifest.json`:
- errors: **0**.

CHAT independently recomputed raw Git SHA-256 values for every manifest evidence item:
- **22 / 22 evidence hashes matched**.

CHAT also independently recomputed final hashes for all 3 material code/test files:
- **3 / 3 matched**.

Manifest correctly records:
- `REAL_HOST_LIFECYCLE_CERTIFICATION = NOT_RUN`;
- `CHAT_ACCEPTANCE = NOT_RUN` before this receipt;
- `forbidden_paths_touched = false`;
- attempts = 1;
- retries = 0;
- usage = NOT_MEASURED.

## Acceptance matrix

- immutable assignment/result chain: PASS
- ancestry / remote readback: PASS
- changed-path scope: PASS
- presentation-only architecture: PASS
- current package/WPF singleton proof contract: PASS
- fail-closed control/process/lock semantics: PASS
- Worker/F1 pre-G3 exclusion: PASS
- stable uninstall semantics preserved: PASS
- focused regressions: PASS
- full suite: PASS
- K1 UNEXPLAINED=0: PASS
- forbidden bytes: PASS
- secret/diff/static: PASS
- Result Contract v2: PASS
- recovery provenance: PASS
- real installed-host lifecycle: **NOT_RUN**
- G3/G4/Canary: **NOT_RUN**

## Uncovered surfaces

Still intentionally unverified:
1. real current-package WPF lifecycle on the Owner Windows host;
2. real explicit WPF graceful exit + lock release;
3. real stable uninstall/postconditions;
4. real exact-package reinstall and durable-state preservation;
5. G3/G4 and final Canary/C4.

Offline BUILD fixtures do not substitute for those stages.

## NEXT_SAFE_ACTION

A02 BUILD correction is accepted.

Prepare a **fresh Git-first real-host lifecycle TEST certification task** bound to accepted result `085cc8302e824dbccf9cbef80422ed48894b9cb4`.

The next task must:
- use a new task/Dispatch identity;
- run fresh route-specific host PreExec;
- authorize only the lifecycle mutations required by the certification;
- exercise current-package WPF launch/inspect/check/graceful-exit, stable uninstall and exact-package reinstall;
- preserve durable state and historical consumed identities;
- stop before Worker/F1/G3/G4/AppLocker/service/ACL/Canary;
- produce a new immutable result for CHAT review.

No A01 or A02 Dispatch replay is permitted.
