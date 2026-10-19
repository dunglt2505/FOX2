# FOX2 coding handoff candidate — NOT EXECUTABLE

Status: CANDIDATE_DOCUMENT_ONLY_NOT_EXECUTION_AUTHORIZATION. This file is not an executable assignment. Do not start from this candidate. CHAT must bind the published exact prompt commit/blob/hash to a separately authorized Dispatch after final state/writer checks.

## Role and tuple
Implement the bounded shared PreExec compatibility task FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018, FOX2 only.
Selected route retained from accepted intake: CODEX / PINNED / gpt-6.1-sol / medium / FULL_ACCESS. No fallback, reasoning/model change, subagent or second implementation lane.
Proposed later execution path MANUAL_LOCAL and delivery owner AGENT are CHAT handoff design choices for this single existing Windows worktree. They have not been launched or activated. Git delivery, after activation, is exact non-main scope only, max_runs=1. Full Access creates no protected authority.

## Immutable sources and authority
- Repository dunglt2505/FOX2.
- Task 502f2aefbda35e4fec134dfb9d5f15f3222660d5:docs/agent_handoff/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/task.md; SHA-256 82326622a477e2822caefd1d96abddfb4e30522cff19524e13c9cdebe7db9813.
- Accepted PreExec fd3141f8e825931f9ee17d68c740e3b36230aa96:reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/preexec/preflight_receipt.json; SHA-256 f3ab51d0932dd2d08b88bbf217cca10bcc98334d373c86854cbaaa26ee2a30f9. Its source_head remains 502f2aefbda35e4fec134dfb9d5f15f3222660d5.
- CHAT intake b2879ed71d55fd9e4488c8dcef0a2fff012f7d9c:docs/governance/releases/FOX2_PREEXEC_COMPAT_CHAT_CORRECTION_INTAKE_20261019.json; SHA-256 71ac65cdf0990588d218c261ea152ee1aedaca78a7998d70fb3c67e870d069d0; PASS_TO_ASSIGN, no Dispatch/start.
- Registry b27f1085ee13d8dce56fd2735e100ea1616e6e23:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json.
- Owner release d8e2331674ef1921844f369bfa9e48b82a73c6a1:docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/OWNER_RELEASE_APPROVAL.json.
- Bounded Owner grant bdaa6fd2be14b03e607fa52f91aa237596481780:docs/governance/releases/FOX2_CANARY009_PREEXEC_COMPAT_OWNER_SEMANTIC_CODE_AUTHORIZATION_20261018.json.
- Frozen governance c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359; resolve Dictionary v1.2, Policy v1.8.9, Routing v1.3, PreExec v1.1, receipt v1, intake v1.1, Dispatch v3 and Git-first v12 from Registry/Dictionary. No main/new-policy rebind.
- Compatibility package 1e01fa9936a7f4b7c1ad097e55801c27c5319bf0:docs/governance/releases/FOX2_CANARY009_PREEXEC_COMPATIBILITY_CHANGE_PACKAGE_20261018.json. Read and verify its three artifact paths/digests before design. Their older candidate status describes that publication phase; later bounded Owner grant and intake control current permission. No global EFFECTIVE release.
- WP-only authority rests on user-bound trust anchors plus recorded approval chain; not cryptographic signatures or Git self-declarations.

## Entry gate after future activation
Validate actual immutable Dispatch/schema/prompt source and exact permissions. Recheck POLICY_CHECK -> TASK_STATE_CHECK -> ROUTING_R0_R7 -> ASSIGNMENT_CHECK without conflating historical PASS with current state. Reuse accepted PreExec; do not run its launcher/publisher or replay probes. If new material facts invalidate readiness, STOP and return to CHAT.
Read current and supported legacy controls, read-only host ledger and manual consumption for THIS task. No claim about Canary consumption follows from zero matches for this task.
Verify single writer, correct Git owner, clean WIP and exclusive execution admission using applicable shared mechanisms. A process count snapshot alone is not a writer lock. Preserve other work.

## Worktree, base and source identity
Branch work/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018; resolve the exact expected Windows worktree from the immutable task and validate actual host access and ownership before execution.
Expected implementation starting HEAD/base is fd3141f8e825931f9ee17d68c740e3b36230aa96. Frozen runtime baseline f3d6468fedb553ba6c6192ba5811cb1b26a11ab9 is ancestry/context, not a reset target. Task source 502f2aefbda35e4fec134dfb9d5f15f3222660d5, implementation base fd3141f8e825931f9ee17d68c740e3b36230aa96, future prompt commit and control publication commit are distinct identities. Stop on unexplained drift; no reset/rebase/stash/rebind.

## Required change
Add a separately authenticated existing-published-dispatch revalidation profile to reusable shared PreExec. Separate task branch/source head from receipt publication branch/head. Preserve legacy v1 schema bytes, historical receipts, behavior and existing consumers. Do not fork a task-local validator.
Require exact dispatch/prompt/task/Registry/Owner bindings before any probe/publication, honest published=true, current actual ledger and fail-closed consumed/started/unknown state, exclusive writer/WIP, expected-head guarded publication, exact allowlisted receipt diff and immutable remote byte readback.
Consumer analysis is mandatory: use the package matrix and real callers; explicitly identify material unknown consumers. Generated Dictionary edits are not implicitly permitted.

## Exact writable scope after activation
Primary source/test paths:
- agent_bridge/src/fox2_agent_bridge/preexec/engine.py
- agent_bridge/src/fox2_agent_bridge/preexec/profiles.py
- agent_bridge/scripts/preexec.py
- agent_bridge/tests/test_preexec.py
Only if necessary for the approved semantic change, new candidate artifacts:
- docs/agent_handoff/FOX2_PREFLIGHT_RECEIPT_EXISTING_DISPATCH_EXTENSION_CANDIDATE_20261018.json
- docs/agent_handoff/FOX2_CHAT_PREFLIGHT_EXISTING_DISPATCH_INTAKE_CANDIDATE_20261018.md
- docs/agent_handoff/FOX2_PREEXEC_EXISTING_DISPATCH_CONTRACT_ADDENDUM_CANDIDATE_20261018.md
Exact result/evidence paths selected within this WP:
- reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/report.md
- reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/result.json
- reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/test_summary.json
- reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/tests.junit.xml
- reports/FOX2-BRIDGE-RC1-PREEXEC-COMPAT-DEV-20261018/diff_trace.json
Do not rewrite the accepted preexec/preflight_receipt.json. Do not edit probes.py, generated Dictionary/generator/tests, poller/runner/config or any other path without specific source-impact proof and CHAT allowlist extension before write. No blanket directory permission.

## Required validation
- Existing legacy PreExec v1 PASS/BLOCKED/INFRA_FAILED regression, schema and historical bytes unchanged
- Separate published=true profile: authenticated identities and current safe ledger; v1 rejects published=true
- Reject wrong dispatch/task/prompt/Registry/Owner binding before probe/publication
- Consumed/started/unknown/stale/conflicting ledger fails closed
- Distinct task and evidence locators; protected Canary head invariant
- Expected-head and writer races; unrelated WIP, hooks, secrets and invalid serialization fail closed
- Push/readback mismatch never emits success; exact one-file receipt publication
- Known consumer inventory and old/new selector tests; material unknown consumers remain HOLD
- Relevant focused/full PreExec regression using synthetic fixtures and disposable remotes only
Use synthetic dispatch IDs, fixtures and disposable remotes only. Check original Canary identity/digest contracts as source data without claiming/executing the real Dispatch. Preserve original dispatch SHA-256 a8756aa6e66e98ba0a6fcc0995bf72fd175ef103a8bf9f27f79466535112576a and prompt SHA-256 dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0 as authenticated reference bindings.
Every material diff hunk maps to REQUESTED / NECESSARY_DEPENDENCY / JUSTIFIED_GENERATED in diff_trace.json, with requirement/test evidence. No drive-by refactor. Do not weaken fixtures/tests to obtain PASS. Excluded/not-run checks remain explicit.

## Delivery after activated authorized run
One Agent owns exact non-main source/test/report commit/push. Verify staged path allowlist, canonical generated UTF-8/LF, diff check, secrets, expected remote head and exact immutable readback. No force push or history rewrite. Produce source-bound report, actual test summary/JUnit, diff trace and Dictionary-resolved Result Schema v2 result.json. Agent delivery remains PUSHED_UNREVIEWED until CHAT result intake; it is not released EFFECTIVE.

## Protected state and STOP
Canary work/FOX2-BRIDGE-FINAL-CANARY-009 remains 501822a33ef08c7365154913bbc677544856eee5. Preserve its Dispatch FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001 and prompt, original four location-exception files under grant 84ac87fbccc947c16490fb9365dc5a3d8e49661c, installed runtime, provider/broker and live state.
- Unverified authority or source/hash drift
- Wrong branch/worktree, unrelated WIP, competing writer or required permission failure
- Task already dispatched/consumed/started or uncertain state
- Material selected-route capability change; no automatic substitution or probe replay
- Out-of-allowlist dependency requires CHAT scope adjustment before touching
- Unknown material consumer or unsupported frozen schema/runtime compatibility
- Protected Canary branch/head/dispatch/prompt change
- Secret/hook/expected-head/publication/readback failure
- No main/merge/PR/deploy/install/runtime adoption/provider/broker/LIVE or Canary execution
Never poll-once, run-next, e2e-once, resume/launch workers, claim/replay Canary or install/adopt runtime. Installation, governed contract release and future Canary PreExec/readiness are separate gates.
Post-start nonzero/auth/capacity uncertainty -> NEEDS_RECONCILIATION, consumed dispatch, no blind retry or silent Agent substitution.
Copilot remains FAIL/AUTH_REQUIRED/nonmaterial; receipt 1.0.98 is corrected append-only as operator-attested 1.0.95. Do not repair auth or promote capability. Numeric quota NOT_EXPOSED is permissible under frozen policy after live readiness proof; do not invent telemetry.
