# FOX2 — CHAT Result Review — Presentation Lock Certifier R5

Date: 2026-10-22
Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`
Feature: `FOX2-BRIDGE-RC1`
Stage: bounded BUILD correction within Bridge TEST
Task: `FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5`
Dispatch: `FOX2-DISPATCH-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-CODEX-001`
Runtime base: `59ba8b50136ac5bcee7cf2d2edbf65e360812b78`
Observed remote result: `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`

## Verdict

**CHAT_ACCEPT — R5 bounded code/test correction only.** The Bridge Whole-WP remains **DOING / TEST**, **INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED**.

The Owner launcher output independently establishes `FOX2_DISPATCH_CONSUMED=TRUE`, `FOX2_NO_REPLAY=TRUE`, `FOX2_CODEX_EXIT=1` (usage limit), and `FOX2_RESULT_DELIVERY=PUSHED_UNREVIEWED`. Do **NOT** rerun this R5 Dispatch. Exit code 1 is retained as an execution observation; it is not relabeled 0. The published complete result and actual test evidence are accepted despite this post-delivery quota error; the exit code does not itself attest a successful Agent process.

## Independent Git readback / scope

- Result branch `work/FOX2-BRIDGE-RC1-PRESENTATION-LOCK-CERTIFIER-REWORK-R5-20261022` read back at SHA `10326dd116ccbfa90a70db4f4c8ec27487ee4fbf`.
- Exactly one result commit descended directly from runtime base `59ba8b50136ac5bcee7cf2d2edbf65e360812b78`.
- Git comparison shows **18 changed paths, 0 unauthorized**: exactly two allowed code/test paths, 16 R5 result/evidence files.
- Independently fetched all 18 Git files as original bytes. Computed SHA-256 for all; **17/17 non-null manifest digests match**. The manifest self-entry has `new_sha256=null` to avoid self-reference.
- Exact task and prompt blob identities match, and R5 report/source_binding bind the fresh R5 Dispatch, pinned model `gpt-6.1-sol / medium`, and R5 PreExec receipt.
- Source delta: `agent_bridge/scripts/certify_user_lifecycle.py` adds an exact `pre_live.classification == OPENABLE` gate for `ACCESS_DENIED_REQUIRES_DIFFERENTIAL`. `ABSENT + errno13/no-winerror` fails closed before UI action; explicit `SHARING_VIOLATION/winerror32` stays supported; existing-live provisional continuation keeps its post-exit lock-release proof.
- Only `agent_bridge/tests/test_lifecycle_wpf_contract.py` changed as a test file; new parametrized fresh/zero-WPF absent-lock scenarios cover sharing-violation positive and errno13 negative cases. Retained other negative and lifecycle tests.
- Material diff inspected; Git result K1 reports `UNEXPLAINED=0`. Agent static evidence reports diff-check, syntax, lifecycle-tail AST, privacy scan and schema checks PASS. Independent SHA/path verification corroborates its file inventory; CHAT did not independently run Windows tests.

## Test evidence readback

- `focused.log` and `focused_run.json`: `69 passed in 2.95s`, exit code 0.
- `full.log` and `full_run.json`: `686 passed in 440.19s`, exit code 0.
- Testing used a detached short-path snapshot; `test_snapshot.json` claims 106 tracked agent_bridge files byte-identical to the R5 result. This test-host claim is supported by submitted evidence, not independently rerun by CHAT.
- Initial collection failed due to PYTHONPATH/source-layout resolution. It was corrected before the two final successful test runs; the initial failure is preserved in `validation_history.json`.
- Real Windows Owner-host lifecycle was **NOT_RUN** in R5; no installed package mutation, worker, broker, provider or LIVE execution was authorized by this task.

## Preserved baseline, blocker and next action

- Reuse accepted A04 source/package/provenance/install/safe-control/singleton evidence, including the exact A04 package SHA-256 `f99c7add1b99bad938d977f634fd8a88e20763f5e35aaadf5cfe3072a1a327ee`. **A04 overall lifecycle result remains truthful FAIL/CHAT_REWORK**, not retroactive PASS.
- R4 remained `CHAT_REWORK`; R4 and R5 consumed Dispatches are NO_REPLAY. Do not automatically promote the historical accepted product lineage `085cc8302e824dbccf9cbef80422ed48894b9cb4` or assume corrected R5 certifier bytes are installed in the A04 package.
- Residual next action: `BRIDGE_INTERNAL_VALIDATION` as one integrated, separately authorized Owner-Windows-host run covering live WPF presentation/lock proof, safe exit, current package verification, one uninstall and reinstall of the **same** A04 package, preserved state, internal local trial and stop/restart with no replay/no Worker regression. Verify the **external R5 certifier** used by this run matches the accepted R5 source and is applicable to the installed A04 package; do not build a new package just for evidence.
- This review **does not** authorize deployment, broker/provider writes, main merge, LIVE or blind replay. If a real host prerequisite is not ready, record its specific blocker while retaining the Bridge Whole-WP identity.

Decision: `R5_CHAT_ACCEPT`; `BRIDGE_TEST_PENDING_HOST_VALIDATION`; `INTERNAL_FOX2_BRIDGE_READY=NOT_ATTESTED`.
