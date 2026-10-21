# FOX2 Bridge RC1 — Integrated Whole-WP plan and evidence tracker
Date: 2026-10-21
Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY
Feature: FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION
Class: CHAT DIRECT DESIGN CANDIDATE / NOT EFFECTIVE / NO EXECUTION AUTHORIZATION
Base result: 804b2e21cd2f8793168ca24bc402e5cdcdb70b3e
F1: DENY. Canary009: HOLD. Internal Ready: NOT_ATTESTED.

## Outcome
One versioned, provenance-bound Bridge package whose Windows trusted broker is the only authorized claim/spawn actor; legacy executors are durably denied; no duplicate/replayed dispatch after restart, crash, rollback or loss of authority. No live deployment is authorized by this plan.

## Whole-WP gates (NOT micro-WPs)
| Gate | Stage | Initial status | Required evidence / exit | Owner |
|---|---|---|---|---|
| G1 Design lock | DESIGN | IN_PROGRESS | Reviewed F1 host trust boundary, Windows retirement mechanism, protocol interfaces, consumers, threat tests and accepted design disposition | CHAT |
| G2 Integrated build | BUILD | BLOCKED_BY_ROUTE_AUTHORITY | Versioned broker/service, authenticated IPC, global atomic claim, lease/revocation, OS fence, installer, full consumer wiring; code review and CI | CODEX/COPILOT as authorized; CHAT accepts |
| G3 Isolated Windows | TEST | NOT_RUN | Actual synthetic denial/allowed spawn, copy/alias/reboot/logoff/revocation/crash/rollback, old/current root reconciliation and zero duplicate | Windows host actor; CHAT reviews |
| G4 Installed adoption | DEPLOY | NOT_RUN | Explicit install authorization, quiescent one-writer, source/package hashes, retired legacy, one-shot activation, restart/no-replay and fail-closed rollback | Authorized host actor; CHAT |
| G5 RC1 certification | TEST/DEPLOY | HOLD | All mandatory Canary009/C4 gates, independent F1 review where required, CHAT acceptance and explicit release decision | CHAT + independent reviewer |

## Tracking contract
Record for EACH gate: STAGE, STATUS, EVIDENCE (commit/path/run), SOURCE_SHA, EXIT_GATE, BLOCKER, ACTOR, AS_OF, NEXT_SAFE_ACTION, CHAT_VERDICT.
Permitted statuses: NOT_STARTED, IN_PROGRESS, BLOCKED, READY_FOR_REVIEW, ACCEPTED, UNKNOWN, NOT_RUN, HOLD.
Do not use arbitrary completion percentages. Existing F0/C3 and StrictMode tests remain scoped historical evidence, not host certification.
Update only this opened feature in the operational Feature Status Registry after verifying writer and source; this candidate plan does not replace the Registry.
Git result pushed != CHAT accepted != EFFECTIVE != RUNTIME_ENFORCED.

## Dependency and cost controls
G1 before G2 implementation assignment; G2 before G3; G3 before G4; G4 before G5. No extra host discovery loops except targeted evidence for a specific G1/G3 gap. No duplicate Dispatch, no reuse of consumed attempts. One integrated BUILD scope with disjoint file ownership if multiple coders. No WORK default coding. No merge/main/Canary/LIVE.
Existing explicit GPT-6.1 Sol coding HOLD must be re-resolved for a NEW executable task; G1 design candidate does not lift it.

## Source boundaries
Human operating governance: Registry at d34da1e3b4918a902646621b487ca8ad3e05b0e0; Policy 2.0.0, Dictionary 1.3, Routing 1.4.0, Git-first Protocol 12 (scoped human authority; runtime NOT_ATTESTED). Bridge TechSpec v0.7 REV10 is a candidate, not EFFECTIVE. Existing Route A design at 7a5af1457dd094d79d870f3eee9bc2d68e494882; F1 host authority contract under reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/f1_host_authority_contract.md. Validate all source SHA-256 and current supersession before executable binding.

## NEXT_SAFE_ACTION
Complete G1 design decision matrix, identify enforceable Windows retirement option with host constraints, finalize protocol/consumer acceptance; then review and decide G1 ACCEPT or HOLD. No executable handoff until Policy/Task/Source/R0-R7/PreExec/one-writer gates are satisfied.

## G1 evidence-based gate snapshot — 2026-10-21 (CHAT)
Source snapshot: 62be753a775b2bb59538213d3738f3e239af38cf; documentary review: docs/architecture/FOX2_BRIDGE_F1_G1_BRDSPEC_COMPATIBILITY_AND_HOST_GATE_20261021.md (same commit). This is an operational candidate snapshot, not an approval or host attestation.

| Gate | STAGE | STATUS | EVIDENCE | SOURCE_SHA | EXIT_GATE | BLOCKER | NEXT_SAFE_ACTION | ACTOR |
|---|---|---|---|---|---|---|---|---|
| G1 | DESIGN | IN_PROGRESS | G1 architecture at d05252a; BRD/TechSpec reconciliation at 62be753 | 62be753a775b2bb59538213d3738f3e239af38cf | Host-supported, independently issued legacy OS execution deny + bounded service claim/spawn protocol + consumer and acceptance trace + CHAT design acceptance | Host edition, policy issuer and provider capability unverified; OS fence and spec addenda not accepted | Collect narrow read-only Windows capability evidence; select enforceable OS policy and lock service/protocol/design acceptance | CHAT; authorized Windows evidence provider |
| G2 | BUILD | BLOCKED | F0 scoped offline work and historical Windows CI only | 442721769dcca2643e111b6fefc16f2a2924cc94 | Integrated broker/service, consumer wiring, tests and reviewed result | G1 not accepted; explicit GPT-6.1 Sol coding HOLD and new route PreExec outstanding | Resolve G1, then recheck coding authority and executable route without replay | CHAT / permitted coder |
| G3 | TEST | NOT_RUN | No isolated positive host certificate | 62be753a775b2bb59538213d3738f3e239af38cf | Negative and positive Windows isolation/reboot/copy/rollback/replay gates | G2 unavailable | Run only on separately authorized isolated Windows host after accepted build | Windows host actor / CHAT |
| G4 | DEPLOY | NOT_RUN | No F1 installed adoption receipt | 62be753a775b2bb59538213d3738f3e239af38cf | Authorized one-shot source-bound install, OS legacy retirement and no-replay | G3 not accepted; installed identity/one-writer not attested | Hold installation until separate admission | Host actor / CHAT |
| G5 | TEST/DEPLOY | HOLD | Historical scoped C3, not C4 or Canary009 | 62be753a775b2bb59538213d3738f3e239af38cf | All RC1/Canary/C4 and independent review gates plus explicit release authority | G3/G4 missing, Canary HOLD | Preserve NOT_ATTESTED until all gates verified | CHAT / independent reviewer |

G1 design disposition: **HOLD_FOR_HOST_CAPABILITY_AND_CONTRACT_ADDENDUM**, not FAIL of already-reviewed candidate design. Technical position: OS-enforced independent legacy retirement is mandatory before positive claim; WDAC/App Control or AppLocker is not selected until actual host capability, policy issuer and administrator separation are verified. Trusted service performs atomic claim and actual child spawn, while desktop/tray remains interactive and does not gain project authority. Untrusted workers must never spawn based on bearer tokens alone. Enforce fail-closed rollback, tombstone preservation, and full direct-consumer closure.

Do not treat 493/23 Windows CI, 11/11 StrictMode tests or prior F0 results as installed host enforcement. F1 DENY; Canary009 HOLD; INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED. No new Dispatch, code, service install, merge, Canary or LIVE authorized by this tracker update.

## G1 continuation — Windows enforcement choice narrowed / host observation pending
Design decision artifact: docs/architecture/FOX2_BRIDGE_F1_G1_WINDOWS_ENFORCEMENT_DECISION_CANDIDATE_20261021.md at f15f8efba214d0f5a3ca51304ff5127d293356cc.
Read-only host probe: reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/evidence/g1_host_capability_readonly_20261021.ps1 at 74d83520ae8dda4ff89534d6d746bc06f9fcd428.

Decision candidate:
- Preferred: signed App Control for Business enforced policy + Secure Boot + policy issuer/admin boundary independent from ordinary Bridge requester.
- Conditional fallback: AppLocker only with effective enforcement, complete EXE/script/installer/DLL legacy-surface coverage, and independently administered policy distribution.
- Neither: G1 HOLD; no weakened positive authorization path.

Current gate state:
- STAGE=DESIGN
- STATUS=IN_PROGRESS
- EVIDENCE=BRD_TECHSPEC_RECONCILED_PLUS_WINDOWS_ENFORCEMENT_DECISION_CANDIDATE
- SOURCE_SHA=f15f8efba214d0f5a3ca51304ff5127d293356cc
- EXIT_GATE=SUPPORTED_HOST_MECHANISM_PLUS_INDEPENDENT_POLICY_AUTHORITY_PLUS_SERVICE_PROTOCOL_CONSUMER_ACCEPTANCE
- BLOCKER=OWNER_HOST_CAPABILITY_JSON_NOT_YET_OBSERVED; POLICY_ISSUER_INDEPENDENCE_NOT_ATTESTED
- ACTOR=CHAT_DIRECT_DESIGN; OWNER_MANUAL_READ_ONLY_HOST_PROBE_ONLY_FOR_UNAVAILABLE_LOCAL_HOST_ACCESS
- NEXT_SAFE_ACTION=RUN_EXACT_READ_ONLY_G1_HOST_CAPABILITY_PROBE_ON_OWNER_WINDOWS_HOST_AND_RETURN_REDACTED_JSON; THEN_CHAT_SELECTS_MECHANISM_AND_ISSUES_G1_DESIGN_DISPOSITION
- CHAT_VERDICT=HOLD_FOR_NARROW_HOST_EVIDENCE_NOT_DESIGN_REJECTION

Probe execution does not authorize service/policy changes, code execution through Bridge, installation, G2 coding, Canary or LIVE. Output remains evidence only; actual denial/bypass/reboot enforcement is deferred to G3.

## G1 EXIT — DESIGN ACCEPTED (2026-10-21)
CHAT acceptance: docs/architecture/FOX2_BRIDGE_F1_G1_DESIGN_ACCEPTANCE_20261021.md at 9c27e7c7104facdb7f083350f38d2451939b6c2a.
Owner-host evidence intake: docs/roadmap/FOX2_BRIDGE_F1_G1_OWNER_HOST_CAPABILITY_INTAKE_20261021.md at 21f9b36159c020f60efd4468abc7c6b284c9e3e6.

| Gate | STAGE | STATUS | EVIDENCE | EXIT_GATE | BLOCKER | NEXT_SAFE_ACTION | CHAT_VERDICT |
|---|---|---|---|---|---|---|---|
| G1 | DESIGN | ACCEPTED | BRD/TechSpec reconciliation + host-capability intake + locked AppLocker/service/protocol/consumer contract | MET_FOR_DESIGN_ONLY | NONE_FOR_G1 | Run G2 entry governance/source/route review; do not code while explicit coding HOLD remains | ACCEPT_DESIGN_ONLY |
| G2 | BUILD | BLOCKED | Historical F0/CI only; no new integrated F1 build assignment | Accepted G1 + separate coding authority + source lock + route PreExec + one writer | OWNER_EXPLICIT_GPT_6_1_SOL_HOLD_CODING remains preserved unless separately lifted | Prepare/read-only G2 entry review only; no Dispatch | HOLD_EXECUTABLE |
| G3 | TEST | NOT_RUN | No isolated AppLocker enforcement certificate | Accepted integrated build + isolated Windows authorization | G2 unavailable | Wait | NOT_RUN |
| G4 | DEPLOY | NOT_RUN | No installed policy/service adoption | G3 acceptance + install authority | G3 unavailable | Wait | NOT_RUN |
| G5 | TEST/DEPLOY | HOLD | Historical scoped C3 only | G3/G4 + final Canary/C4/independent gates | G3/G4 missing | Wait | HOLD |

G1 boundary clarification: effective AppLocker policy and running AppIDSvc are NOT prerequisites for DESIGN acceptance; requiring them in G1 would improperly execute G3/G4. They remain mandatory before any positive runtime authority. Current Owner host observation has empty effective AppLocker collections and AppIDSvc stopped, therefore installed enforcement remains NOT_ATTESTED.

Selected G2 baseline: AppLocker Enforce-rules OS fence administered outside ordinary Bridge requester + privileged F1 Windows service owning authenticated IPC, global atomic consumed-ID state, lease/revocation and actual child spawn. Signed App Control is optional hardening, not G2 prerequisite. F1 positive runtime remains DENY.

## G2 entry review — non-executable scope locked
Candidate: docs/architecture/FOX2_BRIDGE_F1_G2_INTEGRATED_BUILD_SCOPE_CANDIDATE_20261021.md at 9410edb0d88631c33ffda8494b238ec9f4446dc1.

G2 remains one integrated BUILD gate. CHAT inspected the actual agent_bridge code tree and locked the future build envelope: trusted Windows service + authenticated IPC + AppLocker policy artifact support + service-owned atomic claim/spawn + consumer convergence + offline/Windows-CI tests. This is not a coding task or Dispatch.

G2 STATUS=BLOCKED. Existing Owner coding HOLD is preserved; no executable source lock, route PreExec, one-writer receipt, task.md or prompt.md has been created. Historical consumed attempts are not replayed.

## G2 source/route/PreExec entry — source ready, execution HOLD
Entry review: docs/architecture/FOX2_BRIDGE_F1_G2_SOURCE_ROUTE_PREEXEC_ENTRY_20261021.md at 0feff4223746a48e449bb961eecabb1d86388e41.

Resolved governance source for prospective G2: Projectwide Registry 1f04d62; Source Resolution b04ded4; Policy 2.0.0 @ 96175ac; Dictionary 1.3 @ b25f7f7; Routing 1.4.0 @ bcd0089; Protocol 12 @ f2a8bc8. BRD-09/Bridge TechSpec remain candidates; task-specific G1 Design Acceptance 9c27e7c is the accepted F1 design delta.

Route candidate: CODEX / Owner-pinned GPT-6.1 Sol / HIGH / MANUAL_LOCAL dedicated non-main worktree. Installed Bridge is not used to modify itself. Actual CLI/model/auth/capacity/worktree readiness remains ROUTE_NOT_VERIFIED until a task-specific PreExec is lawfully run.

G2 remains BLOCKED solely at executable entry by preserved Owner coding HOLD. No task.md, prompt.md, Dispatch or Agent start. The source/route preparation above does not consume an attempt and does not alter F1 DENY / Canary HOLD.

## G2 task-specific PreExec contract prepared — execution still HOLD
Candidate: docs/architecture/FOX2_BRIDGE_F1_G2_PREEXEC_CONTRACT_CANDIDATE_20261021.md at 2f8fa342613ec7f64204d8e192559847581235e6.

Key finding: current shared `bridge` PreExec registration cannot be reused unchanged because it binds the historical Desktop Batch-B WP/branch/task/receipt and CODEX medium reasoning. G2 requires the current Whole-WP plus GPT-6.1 Sol / HIGH. Reusing Batch-B identity would be a false source/task binding.

Planned future G2 identity is now reserved at design level: `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021`, fork base `4d492e96cd18bc836a48aae7e76ae4ab4fa631a8`, exact G2 task/prompt/preflight/result paths documented in the contract. The branch/worktree and those files remain NOT_CREATED while coding HOLD is active.

Code provenance check: compare accepted StrictMode result `804b2e21cd2f8793168ca24bc402e5cdcdb70b3e` to preparation base `4d492e96...` is 19 commits ahead with only G1/G2 docs, Feature Status and read-only host probe changes; no agent_bridge source/test/runtime code drift observed in that interval.

PreExec contract state = PREPARED; PreExec execution = NOT_RUN; route verification = NOT_RUN; task/prompt = NOT_PUBLISHED; Agent = NOT_STARTED.

## G2 executable entry opened by Owner — 2026-10-21
Owner directive `Tiếp tục làm đi, ko cần dừng lại` supersedes the prior `Giữ gpt-6.1-sol; HOLD coding` for this G2 DEV attempt only. Historical HOLD remains factual; no synthetic PASS.

Owner lift record: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/owner_directives/G2_CODING_HOLD_LIFT_20261021.md` @ fe926ad24d89231e5cf80f0f48ea44eb36887834.

G2 executable branch created: `work/FOX2-BRIDGE-F1-G2-INTEGRATED-BUILD-20261021` from fe926ad24d89231e5cf80f0f48ea44eb36887834.
- task.md published @ 653e49fc0d0f15981bf230995925c89d6994723d; blob 7f0b82e56f7bfa001e40bb176bb26b0ef918c609.
- prompt.md published @ eec25e64a66fed7afc3f45b4d490e6a944e8fe6c; blob d72b78d7300e51a1797c50cf01feacf02a3c9bf3.
- Dictionary 1.2 machine-binding compatibility with Governance Dictionary 1.3 recorded @ ca684b09b3eaea7fa2ce7fc7983f890384202296; scoped verdict PASS_SCOPED for PreExec-only machine identities.

Current G2 branch source head for PreExec: `ca684b09b3eaea7fa2ce7fc7983f890384202296`.
PreExec receipt = NOT_RUN; Agent = NOT_STARTED; Dispatch = NOT_CREATED. Next action is Owner-manual PowerShell 7 task-specific PreExec only; CHAT must remote-intake the receipt before CODEX implementation launch.

## G2 A01 PreExec intake — PASS_TO_ASSIGN
Owner-host task-specific PreExec published remote receipt `94c936b1d93bbfcee5818db24dd75bd9bb32733f`.

CHAT remote readback verified:
- receipt parent exactly `ca684b09b3eaea7fa2ce7fc7983f890384202296`;
- commit changes only `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/preexec/g2_preflight.json`;
- receipt status PASS, blockers empty;
- CODEX `gpt-6.1-sol` / `high` / FULL_ACCESS material route PASS;
- eligible_agent_route PASS;
- G2 task/prompt/Dictionary compatibility identities PASS;
- worktree PASS / competing_writer NONE_OBSERVED;
- dispatch unpublished/unconsumed; Agent not started;
- branch HEAD equals receipt commit.

Immutable task SHA-256: `708ab8addd6e6cbcde581bc03efc66dfb518eb8ac575d568c2be825827e649b9`.
Immutable prompt SHA-256: `a9bda49bede3955996226801d231fefe690088490de5ed9ddfe13ab055625bed`.

Verdict: `PASS_TO_ASSIGN` for one CODEX A01 implementation attempt only. No merge/Canary/LIVE rights. Next: Owner-manual PowerShell 7 exact CODEX launch; then Git result remote readback + fox2-result-review.


## G2 A01 acceptance and G3 test-entry preparation — 2026-10-21

- G2 code remote: `66e8f0a8b3a93140b5f908628b55ac965e15b96e`.
- G2 result/evidence remote: `ac1d1184255945b2c4304641360a1e661ff2d7bd`.
- CHAT review receipt: `reports/FOX2-BRIDGE-RC1-TO-INTERNAL-READY/chat_reviews/G2_A01_CHAT_RESULT_REVIEW_20261021.md` @ `dcf42dd76c8f22e155d469d356e1f1219f3d7b14`.
- Verdict: `CHAT_ACCEPT — G2 BUILD ONLY`.
- Final test evidence: focused 61 PASS; affected regression 200 PASS; full Bridge 557 PASS; Windows native 3 PASS; Desktop Release build PASS; static/package-contract PASS.
- Historical FAIL receipts remain preserved; G3/G4 and full offline package remain NOT_RUN as recorded.
- Feature transition: BUILD exit accepted; current stage TEST.
- G3 non-executable entry/gates prepared at `docs/architecture/FOX2_BRIDGE_F1_G3_HOST_ENFORCEMENT_TEST_ENTRY_CANDIDATE_20261021.md` @ `f0fcc1bfefa682701f3d9a9f8e0a24d2ab33b071`.
- G3 status: `ENTRY_PREPARED / EXECUTION_BLOCKED`.
- Real blocker: no explicit Owner grant for isolated privileged G3 host mutations; no G3 host PreExec. No service install/start/AppLocker apply has occurred.
- Runtime remains F1 DENY / Canary HOLD / INTERNAL_FOX2_BRIDGE_READY NOT_ATTESTED.

## Whole-Bridge reassessment — 2026-10-21

Class: CHAT DIRECT PLAN/HEALTH REASSESSMENT. No Agent execution, host mutation, Canary, merge or LIVE action is authorized by this section.

### Skill coverage

- `fox2-status-roadmap`: REQUIRED / APPLIED — reconciled current Whole-WP stage/status/evidence and critical path.
- `fox2-source-resolver`: REQUIRED / APPLIED — current Governance Registry release head remains `d34da1e3b4918a902646621b487ca8ad3e05b0e0`; Policy 2.0.0 / Dictionary 1.3 / Routing 1.4.0 / Protocol 12 are the current Owner-approved governance source set for new/re-scoped CHAT work; installed runtime remains separately not attested.
- `fox2-project-health`: REQUIRED / APPLIED — separated CODE_IMPLEMENTED / TEST_EVIDENCED / PRODUCT_USABLE / ACCEPTED / RUNTIME_ENFORCED / RELEASED.
- `fox2-techspec-validator`: REQUIRED / APPLIED — BRD-09 REV3 and Bridge TechSpec v0.7 REV10 remain global candidates; accepted G1/G2/same-host design receipts supply scoped requirements without globally promoting those candidate documents.
- `fox2-governance-preflight`: REQUIRED / APPLIED — no new executable action is taken by this reassessment.
- `fox2-execution-recovery`: REQUIRED / APPLIED — historical consumed attempts remain immutable/no-replay; current same-host A01 is published but unconsumed.
- `fox2-agent-route-runtime`: REQUIRED / APPLIED — CHAT owns planning/review directly; host-only coding remains CODEX only after exact current task/Dispatch gates; WORK is reserved for a genuinely independent certification question.
- `fox2-feature-certification`: REQUIRED / APPLIED — historical partial PASS is not current installed certification.

### Current evidence snapshot

1. **Governance/source**
   - Projectwide Governance Registry release branch observed head: `d34da1e3b4918a902646621b487ca8ad3e05b0e0`.
   - BRD-09 REV3: global `CANDIDATE / NO_DEV_GRANT`; product requirements T01–T35 remain the intended Bridge product contract.
   - Bridge TechSpec v0.7 REV10: global `CANDIDATE`; no global promotion is inferred.
   - Scoped design/implementation acceptance is carried by immutable CHAT receipts below.

2. **Accepted/reusable — do not redo**
   - F0 scoped offline safety closure remains historical accepted evidence.
   - StrictMode defect: corrected; 11/11 focused PASS and hosted Windows CI 493 Bridge + 23 package PASS remain historical scoped evidence.
   - G1 trusted-service/AppLocker design: `CHAT_ACCEPT — DESIGN ONLY` @ `9c27e7c7104facdb7f083350f38d2451939b6c2a`.
   - G2 isolated-host integrated F1 build: code `66e8f0a8b3a93140b5f908628b55ac965e15b96e`, evidence `ac1d1184255945b2c4304641360a1e661ff2d7bd`, CHAT review `dcf42dd76c8f22e155d469d356e1f1219f3d7b14`; final tests focused 61, regression 200, full Bridge 557, native Windows 3, Desktop Release build PASS.
   - Same-host design rework: `CHAT ACCEPT — SAME-HOST DESIGN REWORK` @ `0837361aa97f5d7f2116868cb2273eeac3acd0dc`.
   - Same-host A01 metadata PreExec + live route admission PASS; remote admission evidence commit `0962ec74617613ff01a629926e64b7ae8b122979`.
   - CHAT PASS_TO_ASSIGN `2c7c233d4afeda5462241f4126a16f075840157e`.
   - Executable Dispatch `FOX2-DISPATCH-BRIDGE-RC1-SAMEHOST-BUILD-A01-CODEX-001` published/read back @ `7efb5d98d8b51a26c8e3de1a0b808a0f48b3885c`, blob `b7461f9273d5a1e0a6cdbc38e787070bdd650e8e`, max_runs=1. Task implementation has NOT started and this Dispatch is UNCONSUMED.

3. **Current code reality**
   - Compare accepted G2 code `66e8f0a8...` to current same-host branch `0962ec7...`: no same-host product-code implementation has landed; subsequent changes are G3/same-host task, tooling and evidence.
   - Current F1 policy/service therefore still reflect the accepted isolated-host model, including the monolithic policy identity and Enforce assumptions that triggered the same-host redesign.
   - Installed positive F1 authority remains DENY.

4. **Historical Desktop/package lane**
   - Batch-B evidence shows installer, per-user install, update, setup, Tray/Worker, startup single-instance and diagnostics PASS at that historical source.
   - `UNINSTALL_PATH=FAIL`; cause remained UNKNOWN because captured stderr was not retained.
   - Full Bridge tests after the material stop, real eligible FOX2 dispatch, restart/no-replay, result remote-readback and usage snapshot were NOT_RUN in that lifecycle attempt.
   - Therefore old Batch-B package success cannot certify current package lifecycle or rollback safety.

5. **Installed provenance**
   - Previous host evidence found installed ledger/desktop bytes matching pre-F0 sources, not the later F0/F1 accepted code.
   - A trusted current same-host F1 installed package has not been identified/adopted.
   - Protected service/AppLocker runtime enforcement is NOT_ATTESTED.

6. **Canary / final readiness**
   - Historical Canary009 branch now contains Agent result commit `117812c1ef9117e8d156f908018ad845127a53ee` with a PASS marker, parent `501822a33ef08c7365154913bbc677544856eee5`.
   - This proves a historical Agent result exists; it does NOT prove current Canary acceptance, current-source validity, C4 or `INTERNAL_FOX2_BRIDGE_READY`.
   - Policy v2.0.0 preserves Canary009 as a consumed historical identity and forbids silent replay. No new plan may reuse that attempt.
   - Current `INTERNAL_FOX2_BRIDGE_READY = NOT_ATTESTED`.

### Problem matrix

| ID | Problem | Class | Current evidence | Why it matters | Required closure |
|---|---|---|---|---|---|
| B1 | Isolated-host F1 policy unsafe for Owner's only daily-use host | DESIGN→BUILD gap | same-host acceptance `0837361...`; current code still G2 model | machine-wide allowlist/DLL enforcement can break unrelated apps | finish existing same-host A01; dual digests, safe baseline, Exe/Script mandatory, MSI/DLL conditional, HostFence dual check |
| B2 | Same-host implementation not executed | BUILD | Dispatch `7efb5d98...` PUBLISHED_UNCONSUMED; branch `0962ec7...` | G3 cannot start on stale isolated model | run exactly one existing A01 attempt only after immediate launcher rechecks; CHAT result review |
| B3 | Package/uninstall/rollback lifecycle incomplete | BUILD/TEST | Batch-B uninstall FAIL; later gates NOT_RUN | physical-host enforcement without proven rollback is unacceptable | reproduce uninstall failure with retained stderr; fix one systemic lifecycle defect; deterministic package + install/update/uninstall + rollback certification |
| B4 | Installed source/package provenance stale | DEPLOY gate | host matched pre-F0 modules; current accepted F1 package absent | cannot prove running code equals accepted source | build source-bound package manifest; install only accepted bytes; read back installed module hashes |
| B5 | G3 physical-host AppLocker/service enforcement NOT_RUN | TEST | historical isolated G3 BLOCKED; same-host target decision active | source tests do not prove OS enforcement/no-bypass | AuditOnly compatibility baseline + rollback proof, then bounded Enforce test on Lenovo with explicit privileged admission |
| B6 | Legacy execution retirement / one-authority transition not runtime-proven | TEST/DEPLOY | G1/G2 source design/tests only | copied/legacy paths may bypass trusted service after install | prove OS-level legacy deny, service-only claim/spawn, restart/revoke/clock/replay, consumer closure on host |
| B7 | Old Canary009 result is historical, not current certification | RECOVERY/CERT | `117812c1...` marker only; no current CHAT acceptance; no-replay policy | replay or treating marker as current PASS would corrupt evidence | freeze old identity as CONSUMED_HISTORICAL_RESULT_NOT_CURRENT_ACCEPTANCE; use new final-canary identity after G4 |
| B8 | BRD-09/TechSpec global candidate vs scoped F1 addenda | SPEC/CONTRACT | BRD-09 REV3 + v0.7 REV10 candidates; task-specific acceptances exist | final product certification needs one coherent requirement trace | before final certification, produce trace matrix from BRD-09 T01–T35 + accepted F1 same-host deltas to current tests/runtime evidence; global publication only if Owner chooses |
| B9 | Normal UX still depends on manual PowerShell during engineering route | PRODUCTIZATION | BRD-09 requires no per-task PowerShell; current A01 route is MANUAL_LOCAL | acceptable for development, not final Bridge UX | certify background Worker/Tray Git mailbox path on accepted installed package after security/adoption closure |

### Revised execution sequence — one Whole-WP, no micro-WP inflation

#### Phase 0 — State freeze and evidence reconciliation
**Owner:** CHAT direct  
**Status:** COMPLETE_FOR_PLANNING  
**Actions:** preserve all consumed attempts; classify old Canary009 result as historical/not current acceptance; keep same-host A01 as PUBLISHED_UNCONSUMED; do not rerun G1/G2/F0/StrictMode work.  
**Exit:** one unambiguous critical path and no replay ambiguity.

#### Phase 1 — Same-host security BUILD closure
**Owner:** CODEX for host-only coding, CHAT for intake  
**Existing executable identity:** same-host A01 / Dispatch `7efb5d98...`; do not mint a replacement while it remains valid and unconsumed.  
**Scope:** composite AppLocker model, host-safe baseline validation, `effective_policy_digest`, `f1_control_digest`, HostFence dual identity, conditional MSI/DLL, audit/rollback artifact support, tests only; no host mutation.  
**Acceptance:** focused same-host tests + full Bridge regression + no host mutation + K1 UNEXPLAINED=0 + Result Contract + CHAT ACCEPT.  
**STOP:** any task/Dispatch/base drift, consumed claim, writer collision, security contradiction or required real host mutation.

#### Phase 2 — Package lifecycle + rollback closure
**Owner:** CHAT analysis first; CODEX only for proven code defect through a new source-bound task after Phase 1 acceptance.  
**Scope:** reconcile historical Batch-B uninstall failure against current package code; retain actual stderr/exit classification; fix systemic lifecycle defect once; build a deterministic current package; certify install → update → uninstall/rollback without deleting repositories/worktrees; canonical UTF-8/LF evidence.  
**Acceptance:** uninstall PASS on current package; rollback artifact usable; full package/lifecycle tests PASS; no historical receipt rewrite.  
**Reason for sequencing:** do not invalidate the already-admitted Phase-1 base by starting a competing shared `agent_bridge/**` writer, and do not perform physical enforcement until rollback is proven.

#### Phase 3 — Physical Lenovo G3 audit-to-enforce TEST
**Owner:** authorized host actor; CHAT controls admission/review.  
**Entry gates:** Phase 1 + Phase 2 CHAT accepted; exact package/source hashes; Administrator PowerShell 7; physical Lenovo identity; clean/quiescent one-writer; current AppLocker/AppIDSvc snapshot; rollback files validated; explicit privileged G3 authority.  
**Step A AuditOnly/non-blocking:** collect required-app compatibility and policy baseline; no positive F1 claim.  
**Step B bounded Enforce:** Exe + Script mandatory; MSI/DLL only if audited need; install/start service only within explicit G3 authority; copied/legacy/current identities, caller forgery, alias/copy, reboot/logoff, service crash/revoke, policy drift and rollback tested.  
**Exit:** G3 CHAT ACCEPT or bounded HOLD/rollback. G3 PASS is not G4 adoption.

#### Phase 4 — G4 installed adoption
**Owner:** authorized host actor + CHAT.  
**Scope:** install exact accepted package, protected ProgramData root, service identity/ACL, accepted AppLocker policy, retire legacy positive paths, bind installed source/package digests, one-shot adoption, restart/no-replay.  
**Acceptance:** installed module hashes match accepted package; only trusted service can claim/spawn; restart proves no replay; fail-closed rollback works; installed Tray/Worker/setup/startup remain functional.  
**Exit:** `RUNTIME_ENFORCED=VERIFIED` for the scoped Bridge runtime only.

#### Phase 5 — Current-source RC1 certification / final canary
**Owner:** CHAT; independent reviewer only for the specifically required independent security/certification question.  
**Rule:** do NOT replay Canary009. Create a new immutable final-canary attempt identity only after G4 acceptance and fresh preflight.  
**Coverage:** BRD-09 P0 scenarios relevant to internal readiness; current Dispatch v3/Dictionary binding; exact Agent model/permission; one real eligible FOX2 task through background Bridge; result push/readback; usage snapshot; crash/restart/no-replay; package lifecycle; security negatives; C4/current acceptance gates.  
**Exit:** CHAT acceptance + explicit internal release decision. Only then `INTERNAL_FOX2_BRIDGE_READY=ATTESTED`.

### Critical-path ordering

`Phase 1 same-host BUILD → Phase 2 package/rollback → Phase 3 physical G3 → Phase 4 installed adoption → Phase 5 new final certification`.

Do not parallelize new Bridge code writers while the published same-host A01 remains unconsumed. Read-only analysis may continue in parallel. After Phase 1 acceptance, a second writer is permitted only if file ownership is provably disjoint and current Policy limits are respected.

### Status summary

- CODE_IMPLEMENTED: **PARTIAL / substantial** — historical Desktop + accepted G2 F1 source exist; same-host delta missing.
- TEST_EVIDENCED: **STRONG_OFFLINE / INCOMPLETE_HOST** — G2 regression strong; package uninstall and physical enforcement unresolved.
- PRODUCT_USABLE: **NOT_VERIFIED_CURRENT** — old installed lifecycle partly worked, current accepted package/runtime not adopted.
- ACCEPTED: **SCOPED** — G1/G2/same-host design and admission evidence only.
- RUNTIME_ENFORCED: **NO / NOT_ATTESTED**.
- RELEASED_INTERNAL_READY: **NO**.

### Immediate next safe action

Do not create another Bridge WP or new same-host task. Preserve current executable same-host A01/Dispatch unconsumed. When execution resumes, recheck its exact branch/base/Dispatch/writer state and run that single attempt; then CHAT performs immutable result review. If any binding drift is observed before start, HOLD and re-resolve rather than rebinding silently.

