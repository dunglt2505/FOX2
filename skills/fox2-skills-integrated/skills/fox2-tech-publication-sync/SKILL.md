---
name: fox2-tech-publication-sync
description: "Perform authorized Git/Library publication, byte verification and source synchronization without deciding governance authority."
---

# fox2-tech-publication-sync

**FOX2 Layer 3 — Technical and safety methods — Agile Lite 0.5.0**

## Activate when
The task actually requires Git prompt publication, governed document release or Git↔Library file sync.

## Input
Authorized source and destination paths, exact bytes, source authority, writer/WIP rights and intended artifact type.

## Work to perform
1. Determine artifact kind: ordinary native DEV (no separate publication), Bridge task/prompt Git transport, governed document, or expressly requested Git↔Library synchronization.
2. For Bridge Git transport, publish the Prompt Builder's **unchanged** task/prompt content on the authorized non-main branch and verify committed bytes, immutable commit/blob SHA and intended paths. This publication does NOT validate or issue Dispatch or authorize Agent execution.
3. For governed Policy/BRD/TechSpec, check Owner-approved change, existing destination bytes, Git commit and any required Library readback. Update current Registry pointer only in an appropriately authorized release, not by highest version.
4. For file sync, compare SHA-256 of actual source/destination, preserve divergent content without blind overwrite and report conflict or proof of exact readback.
5. Distinguish `SOURCE_PUBLISHED`, `LIBRARY_VERIFIED`, `HUMAN_EFFECTIVE` and `MACHINE_ADOPTED`; no Git push is proof of machine/runtime enforcement.

## Output
Exact source/destination, observed digest/commit, and PUBLISHED/SYNCED/CONFLICT or scoped release HOLD.

## Responsibility boundary
Owns byte movement and verification. Does NOT select authoritative versions, compose prompts, validate Dispatch, operate PreExec, or accept results.

## Common rules
One logical Kanban task; only material checks for selected action. Ordinary native DEV has no mandatory Bridge/PreExec/R0–R7 paperwork. For actual Bridge execution the installed Bridge enforces its own machine protocol and no-replay; never fabricate PASS, permissions or host actions. CHAT owns result acceptance; no broker/LIVE, protected branch or irreversible side effects without real authority. 
