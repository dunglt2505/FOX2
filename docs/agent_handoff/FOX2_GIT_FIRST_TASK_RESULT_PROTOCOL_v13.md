# FOX2 Git-first Task/Result Protocol v13 — Minimal Management, Scoped Technical Proof

**Owner decision:** 2026-10-22 Agile Lite  
**Supersedes:** v12 for prospective ordinary CHAT-managed tasks after release  
**Compatibility:** v12 and earlier frozen Bridge Dispatches remain immutable and fully supported by their original contracts  
**Status:** OWNER_APPROVED_SOURCE_CANDIDATE until publication/adoption readback

## Minimal project task

A new task carries: `task_id, goal, scope, owner/actor, definition_of_done, status, result_pointer`.
Optional: chosen model/thinking; affected contract and tests; specific risk STOP.
Keep all work and bounded corrections in the same task identity. One status field on the Kanban board.

## Operating flow

`BACKLOG → DOING → (BLOCKED when real blocker) → DONE`

Owner establishes outcome once. CHAT selects a capable actor, handles accessible work directly, and hands over a short coding instruction when required. Agent edits only authorized paths, tests the changed behavior and publishes an observable result. CHAT checks material diff, tests and outstanding risk. No separate administrative handoff or review certificate is needed.

For normal reversible DEV, do **not** require formal R0-R7 matrix, a dedicated PreExec receipt, a Git-published immutable prompt, a Bridge Dispatch or a second Agent audit. A Git task record, issue or approved chat assignment can be the instruction according to available and authorized tools. Do not claim code execution without actual host results.

## Risk-specific checks

Keep actual authentication, writer/worktree isolation, allowed scope, non-destructive Git operations, regression/negative tests proportionate to changed behavior. Protected main/merge, deployment, provider/broker/LIVE, destructive writes, sensitive credentials, material installation/host lifecycle and durable no-replay require independently applicable permissions and risk controls. CHAT escalates only those consequential decisions to Owner when not already authorized.

When Bridge execution is actually chosen, its validated Dispatch v3, pinned Dictionary, preflight/ledger and no-replay remain fully applicable. Do not modify an old Dispatch to fit the new task form. A Bridge BLOCKED event does not block independent native DEV.

## Version selection

One canonical authorized governance pointer; no hard-coded 'current' Policy version in a task template/generator. Prior source pins are historical, not instructions to bulk-upgrade. Only change a named consumer when a real compatible route or semantic requirement changes. Do not couple business BRDs to governance version churn.

## Results

For code: commit/branch (or patch where push is unavailable), affected diff, tests actually run, outstanding defects. For documents: exact deliverable path/content and necessary readback. For investigation: finding, evidence and next action. Missing test != PASS. Correct within same task unless change is materially out of scope or no-replay applies.

**Acceptance outcomes:** DONE | REWORK | BLOCKED. A prior valid PASS may be reused with its scope; the old failing attempt is not erased. No automatic main merge, deploy or LIVE.
