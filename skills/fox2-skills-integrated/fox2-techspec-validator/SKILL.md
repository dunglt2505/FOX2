---
name: fox2-techspec-validator
description: Validate Technical Specs versus BRD and consumer contracts.
---

# fox2-techspec-validator

## Agile Lite Owner-approved precedence

Apply Policy v2.1.0 and `../shared/operating_rules.md`. The single project Kanban task tracks actual outcome, tested changes and review. R0-R7/PreExec/Git task-prompt/Dispatch handoff applies only when chosen controlled technical execution needs it; never an automatic gate on ordinary authorized native DEV. Keep domain and technical compatibility tests, real permissions, historical task pins and no-replay; do not trigger unrelated version upgrades.

## Activate when
A TechSpec/API/schema/interface is proposed or revised.

## Work to perform
Compare requirements, API/data types, units, time/timeout semantics, error cases, compatibility, consumer map, negative tests and module deletion/seam test. Distinguish design gap from implementation gap; candidate corrections only with permission.

## Completion / stop
Spec defects, contract/test requirements and acceptance-ready candidate or HOLD.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** TechSpec/API/schema/interface creation, revision, validation or readiness review.
- **PRECONDITIONS:** Applicable authorized BRD/Dictionary, current TechSpec identity, consumers and acceptance scope.
- **REQUIRED_ACTIONS:** Trace requirements to API types/units/time semantics, errors, compatibility, negative tests and integration seams.
- **REQUIRED_EVIDENCE:** Precise BRD/TechSpec source paths, contract/test references, consumer map and unverified areas.
- **DELIVERABLES:** Defect/compatibility matrix and accepted candidate or explicit HOLD with testable corrections.
- **VALIDATION:** Cross-check BRD meaning, schema, tests and consumer changes; never promote candidate without publication.
- **FAILURE_STATE:** `SPEC_INCOMPLETE` / `CONTRACT_GAP` / `COMPATIBILITY_HOLD` for missing requirements.
- **COMPLETION_GATE:** All applicable interfaces verified or bounded defect/hold list with required acceptance tests.
## Semantic source compatibility
Resolve TechSpec and related BRD/data/acceptance identities from trusted Dictionary; don't replace release semantics with the newest candidate. Trace producers, consumers, schema and tests; distinguish business meaning from identity-only version bump. For any Agent rework generate immutable source-set and Git-published prompt; certify only real Git result/test evidence by CHAT. Avoid changing all documents on a Policy version update.


## v0.3.7 — Domain-specific bounded recovery
Only reopen spec/consumers on evidence of changed contract or semantics; otherwise keep approved design and patch the implicated component.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
