---
name: fox2-status-roadmap
description: Summarize FOX2 achieved, in-flight and upcoming work based on receipts.
---

# fox2-status-roadmap

## Agile Lite Owner-approved precedence

Use project-wide Policy v2.1.0 and `../shared/operating_rules.md`: one Kanban task, actual delivered result, necessary testing, CHAT acceptance. Historical R0-R7/PreExec/Git-prompt/Dispatch requirements apply only to the technical route which materially needs them. Preserve each specialized skill's real technical evidence requirements, protected operations, source history and no-replay. Avoid administrative micro-WPs and version-only churn.

## Activate when
Project roadmap/status request OR open/load/continue one FOX2 feature whose Stage/Status/Evidence must be checked (lazy per-feature classification).

## Work to perform
Resolve trustworthy task/evidence snapshots; compute what actually passed vs deferred and blocked; sort next work by critical path, permission, risk and cost. Don’t restate historical PASS as a current certification.

## Completion / stop
Dated snapshot with source binding, workstreams, next owner and entry gate.


Completion is governed by the **Execution Contract v0.3.6** below; apply conditional obligations only when triggered, report bounded HOLD otherwise.

## Execution Contract v0.3.6 — observable completion
- **TRIGGER:** Roadmap/status/next milestone request OR opening/continuing one feature without verified stage status.
- **PRECONDITIONS:** Current Whole-WP/feature identity, authorized sources and record/write permissions for any lazy label.
- **REQUIRED_ACTIONS:** Validate feature Stage/Status/Evidence from current BRD/code/tests/receipts; upsert only opened feature if authorized, not a bulk sweep.
- **REQUIRED_EVIDENCE:** Feature/source SHA, time, stage exit proof and old-vs-new status; permission/readback evidence for any Git write.
- **DELIVERABLES:** Dated roadmap or one-feature status record with `STAGE/STATUS/EVIDENCE/EXIT_GATE/NEXT_SAFE_ACTION` and blocker.
- **VALIDATION:** No infer PASS/PLAN from missing data; readback any permitted upsert; keep parallel child feature states distinct.
- **FAILURE_STATE:** `FEATURE_STATUS_UNKNOWN` / `WRITE_BLOCKED` / `STATUS_STALE` for missing evidence or authorizations.
- **COMPLETION_GATE:** Dated truthful status, exactly one feature updated when eligible, next safe action; no automatic mass migration.
## Operational progress priorities
Resolve current Owner priority and latest authorized Dictionary/Registry for each task; do not copy frozen old `BRIDGE_FIRST` order as current. Report Git-first lifecycle in separate statuses: task & prompt published; Agent pickup/started; Git result pushed; CHAT acceptance; build/product usable. Distinguish CODE-FIRST offline DEV (can proceed independently) from Bridge installed readiness and Canary release. Never infer active work from prompt alone or count micro-WPs as delivery.

## Feature-on-load SDLC status: lazy, evidence-first (v0.3.5)
When OWNER/CHAT opens, loads, continues or asks the status of ONE feature, resolve the feature identity and Whole-WP; inspect any existing Feature Status record and evidence snapshot. If missing/stale, derive one row from authorized BRD/TechSpec/acceptance, task/agent Git results, tests, CHAT intake and route-specific runtime receipts. Use `STAGE=PLAN|DESIGN|BUILD|TEST|DEPLOY|MAINTAIN|UNKNOWN`; `STATUS=NOT_STARTED|IN_PROGRESS|BLOCKED|READY_FOR_REVIEW|ACCEPTED|UNKNOWN`; `EVIDENCE=UNKNOWN|SOURCE_VERIFIED|TEST_EVIDENCED|CHAT_ACCEPTED|RUNTIME_VERIFIED`; additionally `EXIT_GATE`, `SOURCE_SHA`, `AS_OF`, `NEXT_SAFE_ACTION` and proof paths. Explicit `UNKNOWN` / `NOT_VERIFIED` is mandatory where evidence is insufficient; NEVER infer pass from a stage label or self-reported completion.
Treat Feature Status Registry as an operational record (suggested path `docs/roadmap/FOX2_FEATURE_STATUS.json`), not new Governance source/authority. On a *permitted update* to an opened feature, safely upsert only that feature with Git readback, no destructive overwrite, competing writer or Issue-level mislabel for multiple features. Owner has authorized lazy on-open feature tagging, not bulk tagging: after checking an actual authorized Git write route/branch, upsert the one opened feature without re-requesting the same Owner approval. If permissions or required scope are absent, display the proposed row and `WRITE_BLOCKED` without claiming Git publication. Pure read-only analysis unrelated to feature loading remains non-mutating. Do not inventory or bulk-tag the project when publishing Skills. Separate human-accepted scope, real test exit gates, host/runtime and release permissions. GitHub Issues/Projects labels are optional derived displays, not the primary feature source. Updates need authorized branch/path and one-writer gate.


## v0.3.7 — Domain-specific bounded recovery
Report per gate `PASSED_REUSABLE / PASSED_HISTORICAL_NOT_CURRENT / FAILED / NOT_RUN / BLOCKED`, without resetting unaffected accepted outcomes or Whole-WP because one downstream gate failed. Give one corrective next action.


## v0.3.7 — Project-wide focused correction and PASS preservation
FOX2 all stages: earliest causal divergence. Accepted PASS is REUSE_VERIFIED by default; no blanket recheck. Retest only changed fact→affected gate or mandatory gates. CONSUMED Attempt cannot replay; accepted PASS evidence from it is reusable. NOT_RUN/UNKNOWN remain scoped.
