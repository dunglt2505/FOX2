---
name: fox2-result-review
description: Accept, rework or block real Agent Git results, including Bridge PUSHED_UNREVIEWED outputs.
---

# fox2-result-review

## Activate when
CHAT receives an actual Agent result or must decide whether a task is DONE.

## Work to perform
Native DEV: compare actual changed artifact/diff and focused test results against acceptance; mark DONE, REWORK or BLOCKED within the same logical Kanban task; no new assignment when receiving an existing result.

Bridge result: require observed `dispatch_id`, original task/prompt/source identities, selected actor and delivery owner, actual Git result branch/commit/SHA and Bridge/ledger state. `AGENT` delivery means Agent commit/push verified by Bridge; `BRIDGE` delivery means Bridge commit/push verifies after Agent leaves Git unchanged. `PUSHED_UNREVIEWED` means transport completed, not CHAT accepted. Fetch observed remote SHA, check ancestry, changed allowlisted paths, code diff, required result/report artifacts (`reports/<WP>/report.md`, `reports/<WP>/evidence_manifest.json` where task contract requires), tests actually run, negative/security relevant results and remaining risks. No fabricated report file or PASS based on Agent self-declaration.

CHAT returns `CHAT_ACCEPTED`/DONE, `REWORK` (scoped defect and safe fix in SAME logical task), or `BLOCKED` with one concrete blocker. For any already claimed/consumed attempt, correction needs a new authorized immutable attempt if Bridge runs it; never replay original Dispatch. Remote Git push, CI, code existence, feature acceptance and LIVE status are distinct.

## Completion / stop
Produce the concrete deliverable and actual proof with DONE/REWORK/BLOCKED or a precisely named lower execution state. Do not mark completed because a prompt, Dispatch, tool invocation or plan exists. CHAT owns the end-to-end result.

## Shared operating and Bridge applicability
Apply shared `../../shared/operating_rules.md`. A routine reversible independent native task needs no Bridge Dispatch, manual R0–R7 artifact or immutable prompt publication. When and only when the actual execution is Bridge-controlled, follow `../../shared/bridge_e2e_v041.md` and the **installed** runtime contract, not an assumed current version. All source/receipt/test evidence must be observed, not invented. Old consumed attempts remain immutable and non-replayable. Complete outcomes in the SAME logical task; do not create administrative micro-WPs.
