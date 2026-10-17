# FOX2 latest-at-execution continuation review

Date: 2026-10-17
Status: CANDIDATE ANALYSIS AND STATIC CHECKS COMPLETED; RUNTIME ADMISSION HELD.
Owner scope: read Git, analyze impacts, update candidate documentation, perform static checks. No runtime modification without verified source/current PreExec/worktree access.

## Observed immutable evidence

- Control branch work/FOX2-DISPATCH-chat: b27f1085ee13d8dce56fd2735e100ea1616e6e23.
- Registry path: docs/governance/FOX2_RC1_TRUST_BUNDLE_20261017/REGISTRY.json.
- Approval and ten manifests: d8e2331674ef1921844f369bfa9e48b82a73c6a1.
- Important path distinction: REGISTRY.json returned 404 at that approval ref; it exists at the control HEAD. This is not a manifest failure.
- Registry, manifests and approval explicitly bind only FOX2-BRIDGE-RC1-TO-INTERNAL-READY. Global semantic promotion and protected effects are false.
- All ten source contents fetched as base64 through the authenticated GitHub connector at c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359 matched manifest SHA-256 and connector Git blob identity.
- Task and local worktree HEAD: e85ccaadd1fb49664bae07ec71ab607368fc1f0d; working tree clean. Named path C:/Projects/FOX2-worktrees/FOX2-BRIDGE-DESKTOP-BATCH-B exists and was read after approved read-only access. No write or ownership lock was acquired.
- Historical PreExec at reports/BRIDGE-DESKTOP-BATCH-B/preexec/local_preflight.json reports PASS, including WPF, at c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359. Its source_head differs from current HEAD. This does not by itself invalidate WPF capability, but it is not current readiness evidence for this new scope.
- Historical source_verification_stop.json at the task HEAD records STOPPED_NEEDS_RECONCILIATION and no worker claim for Dispatch 002. That receipt predates the wrapper solution; do not promote or rewrite its status. Current ledger consumption was not queried and remains UNKNOWN.

## Source authority assessment

Technical chain structure and byte identity PASS for the RC1 wrapper. Independent external owning-authority verification was not established by reading its recorded approval. The current Owner explicitly limits this bundle to RC1 and requires independent verification. Project-wide authority remains AUTHORITY_UNVERIFIED; no competing authority was proven.

The installed shared resolver was executed with an injected read-only transport containing the just-fetched immutable Git responses. Ten bind_effective calls returned matching technical bindings, and a digest-corruption fixture was rejected. This is a captured-data static check, not execution-time live enforcement.

The helper explicitly delegates external approval verification to its caller. It does not enforce whole-WP scope or candidate ordering. Its CLI VERIFIED_EFFECTIVE text must not be consumed as a substitute for independent authority/scope validation.

## Impact crosswalk

| Surface | Inspected observation / required candidate change | Acceptance |
|---|---|---|
| Governance / Dictionary | Separate historical citation, observed candidate, applicable bundle and authority; require scope-compatible approvals and source lineage. Existing historical references remain valid. | SOURCE-01/02/03/06 |
| BRD binding guidance / BRD-to-tech mapping | Add prospective execution admission invariants and trace to the owning requirements; preserve business semantics and frozen releases. No canonical BRD modified. | SOURCE-01 through SOURCE-06 |
| Protocol / PreExec / intake | Bind refresh evidence to the actual attempt; reconcile material head drift and obtain a current receipt before implementation. | SOURCE-02/03/04 |
| Skills / shared resolver | One shared resolution/admission contract; scope and independent trust belong in the host caller; no per-Skill competing selector or stale cache fallback. Installed Skills unchanged. | SOURCE-02/03/06 |
| preexec/engine.py at task HEAD | contracts() lines 194-210 reads the supplied immutable source_head and generated hashes. publish() lines 321-361 checks task branch/readback; that is distinct from live project Registry refresh and candidate selection. Preserve these existing guards. | source bundle refresh and receipt drift tests |
| dispatch_poller.py at task HEAD | query_control_sha/fetch_control verifies transport; poll_once has a NO_CHANGE return; PollResult explicitly marks trusted_for_execution=false. Transport freshness does not establish governance applicability. Required source refs can change independently of dispatch-control content. | unchanged-control/new-source case and pre-claim drift |
| ledger.py at task HEAD | claim_dispatch() lines 388-430 uses BEGIN IMMEDIATE and rejects existing dispatch IDs. Preserve this durable exactly-once guard. The API shown carries no refreshed source bundle identity; integration must prove the admitted binding reaches the actual execution boundary. | duplicate claim and snapshot preservation |
| Runtime execution caller | Full app.py read failed with a remote disconnect. No claim is made that all launch paths were inspected or that admission is wholly absent. Inspect caller, recovery/resume and direct-action adapters when runtime work is admitted. | end-to-end boundary and installed host tests |

## Static verification

static_results.json records 15 passed checks:
- ten immutable source bindings, SHA-256, Git blobs, scope/protected flags;
- one corrupt digest rejected by the existing resolver;
- RC1-only scope consistency;
- observed receipt/task HEAD difference;
- syntax parsing of PreExec engine and dispatch poller.

No runtime modules imported/executed, WPF rebuild, race test, current PreExec, installed runtime test, dispatch claim or replay occurred. Static success does not satisfy the runtime acceptance matrix.

Local reproducibility files are in work/latest-execution-review: snapshot.json, static_review.py, engine.py, dispatch_poller.py, static_results.json. These are analysis captures; sources/ and the runtime worktree were not edited.

## Updated routing precheck R0-R7

POLICY_CHECK: observed scoped Policy 1.8.9 bytes and candidate project-wide guidance; newest project-wide EFFECTIVE policy not certified. No policy check PASS fabricated.
TASK_STATE_CHECK / R0: prior guidance and contract already present; reuse documentation branch; historical stopped work and consumed-dispatch boundaries retained.
R1: independent document/static-analysis stage; runtime implementation held.
R2: direct candidate writes/static checks explicitly authorized; CODE_ALLOWED for runtime HOLD; project-wide authority UNKNOWN; release/merge/LIVE closed.
R3: CHAT connector read/write/readback works. Current Codex usage allowed; 23% five-hour, 77% weekly used at probe. Copilot earlier startup failed and historical receipt says AUTH_REQUIRED; current auth/quota UNKNOWN. WORK access/quota UNKNOWN.
R4: direct CHAT chosen for supported candidate/static work. CODEX and COPILOT considered for future runtime but not admitted. WORK is unnecessary for completed work and cannot be assumed to access Windows. No delegation.
R5: existing dedicated documentation branch owned by this continuation; its observed HEAD before writes 113d5217f20349c528a051a8c71aaee44f1eba46. Runtime read access confirmed; write ownership/competing writer state not currently verified. No runtime edits.
R6: prior immutable guidance readback exact; continuation artifacts require exact remote readback. No source synchronization to Library or installed plugin claimed.
R7: CHAT/current model configuration completes guidance, static evidence and readback. STOP runtime until scope-appropriate independent authority, material current PreExec and exact writer/worktree permissions are verified. No automatic task assignment.
ASSIGNMENT_CHECK: no executable dispatch or delegated task issued.

## Remaining runtime gates

1. Project-wide applicable source discovery and independent owning-authority chain: BLOCKED/UNVERIFIED. Do not substitute RC1 authority.
2. Current task-specific PreExec with material drift reconciliation and required host capability: BLOCKED/NOT_RUN.
3. Runtime single-writer ownership and exact permitted paths: UNKNOWN; read access alone is insufficient.
4. Actual admission integration, race/no-replay tests and installed behavior: NOT_RUN.

No Owner question is required for this evidence update. Resolve remaining facts from Git/host evidence where available. This report grants no DEV, main, merge, release, deployment, provider/broker or LIVE permission.
