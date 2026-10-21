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
