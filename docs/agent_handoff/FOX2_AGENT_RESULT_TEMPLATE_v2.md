# FOX2 — Agent Result Report (Contract v2)

> **Entry point:** `reports/<WP_ID>/report.md`. Replace placeholders with observed facts; never invent evidence. Store companion `evidence_manifest.json` conforming to `FOX2_AGENT_RESULT_SCHEMA_v2.json`. Every `NOT_RUN`, `BLOCKED`, and limitation is useful evidence of scope; do not hide it.

## R01 — Identification & submission
- Project / WP / Task / Change: `FOX2` / `<WP_ID>` / `<TASK_ID>` / `<CHANGE_ID>`
- Agent product · model · mode · host (observed): `...`
- Start UTC / finish UTC / report UTC: `...`
- Submission state: `READY_FOR_CHAT_REVIEW | PARTIAL | BLOCKED | LOCAL_ONLY` (never ACCEPTED)

## R02 — Authority, routing, grants
- Effective Policy & hash: `FOX2 Policy V1.3`, `<SHA256>`
- Policy, Task State, R0–R7, Assignment checks: `...` (link detail if needed)
- Owner grant and actual Git capability: `...`; CODE_ALLOWED / REPORT_WRITE / REPORT_PUSH / MERGE / PROVIDER / LIVE: `...`
- STOP reason (or NONE): `...`

## R03 — Immutable input bindings
- Git repo · task commit · task path · source manifest path/hash: `...`
- Approved base full SHA · released BRD/contract revision(s): `...`
- Source readback (expected/observed SHA-256): `...`
- Reused previous evidence / conditions invalidating that reuse: `...`

## R04 — Requested vs completed (delta summary)
- Requested: `...`
- Completed with evidence IDs: `...`
- Partial/deferred/not done and **why**: `...`
- Explicit exclusions: `...`

## R05 — Changed paths / ownership
| Exact path | ADD/MODIFY/DELETE | Reason | Within allowlist | SHA-256 / diff evidence |
|---|---|---|---|---|
| `...` | `...` | `...` | `YES/NO` | `...` |
- Worktree / branch / writer lease / tracked, untracked and ignored WIP collision: `...`
- Protected docs, runtime/code, secrets touched? `YES/NO/NOT_CHECKED` plus details

## R06 — Executed tests & negative controls
| Test ID | Positive/negative | Command/tool + environment | UTC | PASS/FAIL/BLOCKED/NOT_RUN | Evidence ID |
|---|---|---|---|---|---|
| `...` | `...` | `...` | `...` | `...` | `...` |
Do not treat a simulated safety rule as actual branch protection or Production verification.

## R07 — Requirement / acceptance mapping
| Requirement / acceptance ID | Status | Evidence ID(s) | Deviations / remaining work |
|---|---|---|---|
| `...` | `PASS/FAIL/BLOCKED/NOT_RUN/NOT_APPLICABLE` | `...` | `...` |

## R08 — Evidence inventory
| Evidence ID | Relative Git path | Raw SHA-256 | Provenance/time | Claims supported |
|---|---|---|---|---|
| `...` | `reports/<WP_ID>/evidence/...` | `...` | `...` | `...` |
No secret, private account details, licensed DNSE raw feed, or huge unredacted log in Git.

## R09 — Git delivery / immutable pointer
- Repo · task branch · base commit: `...`
- Push: `LOCAL_ONLY | PUSH_BLOCKED | PUSHED_UNREVIEWED`
- Current branch HEAD prior to report commit: `...`
- PR URL if observed: `...`
- **After actual push, give remote commit SHA OUTSIDE THIS COMMITTED REPORT**, via Copilot/WORK's final one-line pointer or GitHub PR. A committed report must not attempt to contain its own Git SHA.
- CHAT has **not** accepted this result until it reads the immutable commit and records a separate review receipt.

## R10 — Blockers, risks, data/security boundaries
| Risk ID | Severity | Unresolved impact | Next action / owner |
|---|---|---|---|
| `...` | `...` | `...` | `...` |
- Secret scan + sanitization outcome: `PASS / BLOCKED / NOT_RUN`; rights/licensing/provenance: `...`

## R11 — Resource / retry accounting
- Attempts / retries / observed quota and token/credit use (or `NOT_MEASURED`): `...`
- Escalation if any and evidence: `...`

## R12 — Decision request to CHAT
- Agent conclusion: `READY_FOR_CHAT_REVIEW | PARTIAL | BLOCKED | LOCAL_ONLY`
- Exact CHAT decision requested: `REVIEW | REQUEST_SOURCE | REQUEST_GRANT | REWORK | STOP`
- Next actor, smallest precise action, prerequisite gate: `...`

**Final one-line pointer after a real push:** `FOX2 | <WP_ID> | <repo> | <branch> | <observed full 40-hex remote commit SHA> | <PR URL or NONE> | PUSHED_UNREVIEWED`.
