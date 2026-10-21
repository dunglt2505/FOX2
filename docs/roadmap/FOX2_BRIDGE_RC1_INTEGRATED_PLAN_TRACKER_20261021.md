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
