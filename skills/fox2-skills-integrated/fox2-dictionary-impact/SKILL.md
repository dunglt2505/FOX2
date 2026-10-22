---
name: fox2-dictionary-impact
description: Trace domain dictionary changes and consumer impact.
---

# fox2-dictionary-impact

## Agile Lite Owner-approved operating precedence (2026-10-22)

Use Policy v2.1.0 and canonical `../shared/operating_rules.md` for ONE Kanban / Build -> Test -> Deliver. This Skill's specialized safeguards remain; legacy unconditional R0-R7, full PreExec receipt, Git-published task/prompt, Agent Dispatch, independent review and document release chains are conditional ONLY on a selected material/Bridge/irreversible technical route. Normal authorized native DEV does not need these extra management gates. Fix only actual source/consumer drift, preserve historical bindings and no-replay, never represent UNKNOWN as PASS.

## Activate when
A field, metric, domain identity or naming change is considered.

## Work to perform
Resolve current trusted Dictionary; identify producers, consumers, generated bindings and unknowns; stress edge cases (UNKNOWN vs zero, units, as-of time). No competing glossary or silent field rename.

## Completion / stop
Candidate mapping, affected consumer list, compatibility tests or explicit HOLD for unknown consumers.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Field/metric/identity/term/source-pointer changes and their consumer compatibility.
- **PRECONDITIONS:** Current trusted Dictionary/Registry, precise changed field/identity and consumer inventory scope.
- **REQUIRED_ACTIONS:** Map producers, consumers, generators, protocols/tests and compatibility; distinguish semantic content from identity/pointer; block incompatible unknown dependencies.
- **REQUIRED_EVIDENCE:** Current/candidate field schemas, consumer references, test evidence and approved release receipt for pointer changes.
- **DELIVERABLES:** Candidate mapping and producer/consumer table, tests or explicit remaining unknowns; pointer receipt only when authorized.
- **VALIDATION:** Check units/NULL-vs-zero/time, unmapped consumers, generated binding and compatibility; read back any permitted pointer change.
- **FAILURE_STATE:** `CONSUMER_UNKNOWN` / `COMPATIBILITY_HOLD` / `POINTER_PUBLICATION_HOLD` on gaps.
- **COMPLETION_GATE:** Impact and compatibility verdict evidenced; do not claim updated current pointer unless authorized downstream publication and readback occurred.
## Version/consumer dependency check
Dictionary is the **lookup for version/path and compatibility**, not the source of business semantics or release signatures. Select latest authorized Registry/Dictionary, not the largest version. Before promoting an identity, find schema, generators, Python binding, runtime normalizer, BRD/TechSpec/Protocol/hand-off/result consumers. Avoid per-version filename allowlists; structural validation plus pinned identity verifies future source names. Test unknown consumer and future-version scenarios. After source lock existing Agent tasks retain immutable binding; no replay or silent rebase.

## Current-pointer publication and impact workflow
Consume `fox2-document-publication`'s verified release receipt and `fox2-source-resolver`'s selected scope. Inventory Registry/Dictionary current pointer, release manifest, policy identity, generated version bindings, route schema, dispatch normalizer, result/intake, BRD/TechSpec consumer/test. Apply a pointer change only after actual authorized Git+Library publication readbacks, compatibility review, and permitted writer/release action; read back updated current pointer. An Owner-approved `OWNER_APPROVED_PRINCIPLE` may already guide planning while Dictionary/Registry machine pointer remains old; report this divergence without either reverting human policy or promoting a `PUBLISHED_EFFECTIVE` claim. Never manually duplicate source version across each consumer; use one authorized current-pointer source and validated generation. Any unknown incompatible consumer => HOLD pointer migration. Historical locks unchanged.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
