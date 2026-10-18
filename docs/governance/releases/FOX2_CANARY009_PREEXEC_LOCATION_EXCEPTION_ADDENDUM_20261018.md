# FOX2 Canary009 — Owner-approved PreExec receipt location exception

Status: OWNER_APPROVED / PROSPECTIVE_WP_ONLY_EFFECTIVE_ON_GIT_PUBLICATION_AND_EXACT_READBACK.
Operational compatibility: BLOCKED. This document is not a Preflight Receipt, executable Dispatch, PASS_TO_ASSIGN or readiness grant.

Recorded: 2026-10-18T22:11:45.572606+07:00. Whole-WP: FOX2-BRIDGE-RC1-TO-INTERNAL-READY. Authority: exact current human Owner directive recorded in `docs/governance/releases/FOX2_CANARY009_OWNER_PREEXEC_LOCATION_APPROVAL_20261018.json` (SHA-256 `5aff45f9a14ab43d5247709964639bd014ea2c21147900beff20bf8e5c250cfd`). It is a recorded directive, not a cryptographic Owner signature.

## Approved exception

For immutable dispatch `FOX2-BRIDGE-FINAL-CANARY-009-CODEX-001` only, prospectively replace the receipt-location requirement in frozen PreExec v1.1 section 4 and CHAT Preflight Intake v1.1 item 2 with publication and exact immutable readback on:

- Branch: `work/FOX2-BRIDGE-RC1-PREEXEC-EVIDENCE-20261018`
- Path: `reports/BRIDGE-DESKTOP-BATCH-B/evidence/final009/preexec/preflight_receipt.json`

This is a separate publication locator. The receipt's task identity remains `work/FOX2-BRIDGE-FINAL-CANARY-009`, source head `501822a33ef08c7365154913bbc677544856eee5`. Do not relabel the evidence branch as the execution branch. CHAT must verify receipt bytes and this sidecar binding together. No receipt exists as a result of this publication.

## Immutable bindings and ancestry

`docs/governance/releases/FOX2_CANARY009_PREEXEC_LOCATION_SOURCE_BINDING_20261018.json` carries live-verified Registry, release approval, all ten frozen source hashes, source-set identity, executable task/dispatch hash, prompt hash and enclosing task context. Its SHA-256 is `1a5789a6d9c87d78428051f4f8e0c8fbec85cd9ca4c0dd7e4cf1bb37a680a862`.

Dispatch bytes SHA-256: `a8756aa6e66e98ba0a6fcc0995bf72fd175ef103a8bf9f27f79466535112576a` at `dc79f8143eec471508bf37565bff38442ce0548a`. Prompt SHA-256: `dd9f45c5ac5f62bc8c65c53fe629a15d67381fe794e18956347fd1e9999ba3e0` at `530cc64feedbab463cefb0f5baed4e9919f25f15`. Canary head remains `501822a33ef08c7365154913bbc677544856eee5`. There is no distinct Canary task.md in its locked tree; the immutable executable task identity is the dispatch plus prompt, with the enclosing Batch-B task separately hashed as context.

Registry: `b27f1085ee13d8dce56fd2735e100ea1616e6e23`, WP_ONLY_TRUST_BINDING. Frozen source-set commit: `c916de489e0aee51d6fe30c5b8b4cd9f4cd9a359`; source-set SHA-256: `325d20ba6599f012f73046449e882c85c66395aeaeebce027a85d4a5fcf5841e`.

The evidence branch is a documentation child of prior binding-decision commit `c73d1146463490e62bb698744e0f14ad9b189e0b`. It is not a child execution checkout of the Canary. No merge of source lines is performed. The known Dictionary excludes it from supported control refs; the base tree contains no dispatch candidate paths or GitHub workflow. The poller queries its configured supported control ref. No runtime/config/watcher is changed and universal absence of unknown external watchers is not claimed.

## Existing published dispatch: truthful state and stop

The existing executable dispatch is already published: `executable_dispatch_published=true`. It must never be stated false or silently redefined to mean no newly published dispatch. Current consumed/start state has not been reobserved; the historical report of unclaimed/unconsumed at 21:46:06 +07 is not a current ledger attestation. Do not claim, start, replace, replay or reset the dispatch.

The frozen schema v1 requires published=false even for BLOCKED/INFRA_FAILED receipts; intake item 7 requires the same. A local Draft202012Validator check of the dispatch_state subschema rejects the truthful published=true value even under the hypothetical unclaimed premise. This is a contract test, not a host receipt. The actual shared producer hardcodes false and couples task branch, worktree, source head and push destination. It cannot implement this split destination unchanged.

Consequently, this location exception does not authorize a truthful canonical receipt under current contracts. Receipt generation/publication and executable readiness remain BLOCKED pending separately authorized compatible shared schema/intake/producer resolution. Do not forge PASS, add unknown schema fields, change original sources, or introduce a task-local state machine. `docs/governance/releases/FOX2_CANARY009_PREEXEC_LOCATION_SCOPED_IMPACT_20261018.json` records exact consumer hashes, line evidence, checks and routing.

## Preserved gates and non-effects

The original policies, Registry, schemas, task/prompt, dispatch bytes, historic receipts and locked Canary branch remain unchanged. This addendum extends the source binding only for this prospective location exception; it neither rebinds frozen base sources nor promotes global Policy/Registry EFFECTIVE. Audit waiver remains WAIVED_BY_OWNER, not audit PASS.

Real Windows worktree ownership, writer exclusion, pinned CODEX gpt-6.1-sol / medium / FULL_ACCESS probe and host PreExec remain unperformed in this action. No durable PASS receipt, implementation assignment, Canary execution, DEV, merge or LIVE authority is created. max_runs=1 and BRIDGE delivery owner remain immutable. CHAT alone retains the release/readiness decision after all material gates and exact remote evidence pass.
