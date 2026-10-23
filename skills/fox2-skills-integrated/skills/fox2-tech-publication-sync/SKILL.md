---
name: fox2-tech-publication-sync
description: "Perform authorized Git/Library publication, byte verification and source synchronization without deciding governance authority."
---

# fox2-tech-publication-sync

**FOX2 Layer 3 — Technical and safety methods — Agile Lite 0.5.0**

## Activate when
The task requires Git task/prompt publication, **Agent/Bridge result commit/readback**, governed document release or Git↔Library file sync.

## Input
Authorized source and destination paths, exact bytes, source authority, writer/WIP rights and intended artifact type.

## Work to perform
1. Determine artifact kind: native DEV (no required publication of its *prompt*, but **code results must reach authorized Git**), Bridge task/prompt Git transport, **Agent/Bridge result delivery**, governed document, or expressly requested Git↔Library synchronization.
2. For Bridge Git transport, publish the Prompt Builder's **unchanged** task/prompt content on the authorized non-main branch and verify committed bytes, immutable commit/blob SHA and intended paths. This publication does NOT validate or issue Dispatch or authorize Agent execution.
3. For Agent results: verify branch, remote commit SHA, actual pushed code/reports, correct authorized publisher, and any writer/path/result constraints. Agent-owned delivery = Agent commit/push; Bridge-owned delivery = Bridge commit/push, while Agent leaves Git history unchanged. For an Agent without push access, only an explicitly authorized CHAT publisher may publish **exact supplied artifacts** with author/publisher provenance and readback. Do not treat local files or chat prose as a Git delivery. Publication proof does not equal CHAT acceptance.
4. For governed Policy/BRD/TechSpec, check Owner-approved change, existing destination bytes, Git commit and any required Library readback. Update current Registry pointer only in an appropriately authorized release, not by highest version.
5. For file sync, compare SHA-256 of actual source/destination, preserve divergent content without blind overwrite and report conflict or proof of exact readback.
6. Distinguish `SOURCE_PUBLISHED`, `LIBRARY_VERIFIED`, `HUMAN_EFFECTIVE` and `MACHINE_ADOPTED`; no Git push is proof of machine/runtime enforcement.

**Project progress documents:** For a management-approved Board/Master Plan delta, publish only exact authorized files to the allowed Git ref with expected-base protection and full remote readback. Do not overwrite historical Master Plans or merge protected main. Return observed SHA/path or `SYNC_PENDING` with the precise permission/conflict blocker; do not choose task status or invent acceptance.

## Output
Exact source/destination and observed digest/remote commit SHA, with `GIT_RESULT_PUBLISHED`/`GIT_DELIVERY_PENDING` for result transport, or PUBLISHED/SYNCED/CONFLICT for source and document transport. Never claim task DONE.

## Responsibility boundary
Owns byte movement and verification. Does NOT select authoritative versions, compose prompts, validate Dispatch, operate PreExec, or accept results.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
