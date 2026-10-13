# FOX2 — Owner Standing Git Writer Grant for Local Agent Bridge (scope-bound)

Document ID: FOX2-BRG-STANDING-GIT-GRANT-20261013-001
Date: 2026-10-13 (Asia/Ho_Chi_Minh)
Decision authority: FOX2 Owner (direct instruction to permit Bridge to write on one Git branch without per-write approvals).
Recorded by: CHAT, as scope/authority registrar.
Governance: FOX2 Policy V1.8.2 RELEASED_EFFECTIVE (C4/C4A/C5/C5B/C6F).
Implementation: FOX2 Local Agent Bridge Technical Spec v0.3 RELEASED_EFFECTIVE.
Authority state: OWNER_STANDING_APPROVAL=YES; GITHUB_BRANCH_EXISTS=YES; VERIFIED_BRIDGE_HOST_CREDENTIAL=UNKNOWN; VERIFIED_BRANCH_WRITE_ENFORCEMENT=NO; BRIDGE_AUTOMATED_GATE_A=BLOCKED_CAPABILITY_UNAVAILABLE.
This standing Owner scope decision is not itself proof of platform permission, installed Bridge runtime, authenticated Control-plane publisher, or successful Bridge push.

## Explicit single-branch grant

- Repository: `dunglt2505/FOX2` only.
- Branch: `work/FOX2-REVIEW-EVENTS-bridge` **only**.
- Git branch initialized at source-set commit `c9dc41b97ca8bc58f06cc2f3701832ba083422e3`, created by CHAT via connected GitHub and remote readback verified.
- Operational role: specifically identified, authenticated **FOX2 Local Agent Bridge service identity** on the authorized Windows host, once host/identity/credential/capability evidence is verified.
- Standing authorization: repeatable non-main append-only/fast-forward Git commits and pushes of approved, sanitized, task-bound review delivery and Bridge operational *metadata* within the allowed paths, with remote readback of exact commit SHA and ancestry.
- Allowed path effective now under released Technical Spec v0.3: `review_events/<WP_ID>/<RESULT_COMMIT_SHA>.json`, and no other path.
- Reserved, *not executable until separate technical-contract update/review*: future `bridge_status/**`, `recovery_manifests/**`, or similarly named **metadata-only** paths. No raw WIP/source/code checkpoint is authorized by this reservation.
- The standing grant is reusable for qualifying events without repeated Owner permission prompts; it must be revalidated only on material change of branch, role/identity, repository, host, permissions, allowed path policy, source authority, or security/trust conditions, and may be revoked/narrowed by Owner.
- Bridge must perform routine automated technical preflight on **each push** (identity/permissions, lease, branch HEAD/base ancestry, no unrelated WIP, path allowlist, secret scan, idempotency, expected event/result binding and remote readback). This routine check does not seek Owner permission anew.
- No post-facto false `PUSHED_UNREVIEWED`, `REVIEW_READY` or `ACCEPTED` claims on local-only event creation or a failed push.

## Forbidden, unaffected authorities

- `work/FOX2-LOCAL-DISPATCH-chat`: CHAT-owned dispatch/control branch. Bridge strictly **read-only**, never writer. Do not bootstrap this branch merely to satisfy a poller while Gate A trust provenance is unproven.
- `work/FOX2-CHAT-REVIEWS`: CHAT-owned acceptance/review receipts, Bridge cannot authoritatively write review verdicts.
- `main`, any other FOX2 branch, branches belonging to CODEX/COPILOT or other Agents: NOT granted.
- Source code snapshots `agent_bridge/**`, bridge configuration, governance, source contracts, BRD, production data, raw local WIP and database files: NOT granted via this standing branch authority.
- Agent task result code changes require separately gated `CODE_ALLOWED`/`GIT_CODE_PUSH` for an exact WP, even if the Bridge implements the Git transport for that task under a separately verified branch permission. Standing review-event permission is not `GIT_CODE_PUSH`.
- No Agent execution, automatic fallback/substitution, Code/Model changes, policy/source decisions, PR, merge, protected/main push, force push, history rewrite, deletion, config changes, provider or broker access, deploy or LIVE.
- Copilot Pro standing REPORT-only authorization (C6F.2A) remains separate and unchanged.

## Permissions vs platform facts

- Owner scope grant **already given**; **do not ask Owner again per permitted review-event push**.
- The repository is private, personal-owned, and previous readbacks showed `protected=false`; GitHub ruleset effective control-ref enforcement not proven due to plan/API limitation. Branch existence and a grant document do not install any IAM restriction, verify a bridge service identity/token, or make Gate A PASS.
- GitHub repository contents write tokens may have repo-wide reach. Restricting Bridge to the one branch therefore needs verified GitHub-side controls if supported and **mandatory process-level allowlist safeguards**; do not claim GitHub platform enforcement unless demonstrated.
- If actual Git credential cannot be bound to the approved identity/branch/path, return `GIT_BRIDGE_PERMISSION_UNKNOWN` or `BLOCKED_GIT_TRUST`; do not push. No credential dump. Do not create a new unrestricted token.
- A single scoped negative+positive pilot using synthetic sanitized review-event metadata is necessary to demonstrate real remote write/readback and denial of unauthorized paths; do not perform destructive or unauthorized writes, and do not equate this pilot with automated dispatch Gate A.

## Scope for BRG-003 / quota recovery

BRG-003 import of the existing local Bridge source remains a separate **one-time task grant** for exact import branch/worktree/20 reviewed files/credential lane. It is NOT covered by this standing review-event permission. After a scoped DEV/Git code authorization for a *given task* exists, ordinary commits within that authorized WP need not seek new Owner approval on every commit; each write still passes technical checks.
Quota recovery may use the permanent review branch for **sanitized metadata** after approved Technical Spec integration. Actual recovered source/code diffs must remain within the authorized WP execution branch and `GIT_CODE_PUSH` gate.

## Routing snapshot

R0 existing v0.3 topology retained, BRG-002 inventory accepted for planning, BRG-003 not code-authorized.
R1 decision is branch provisioning and bounded standing review/event publication, not runtime DEV.
R2 Owner grant aligned to v0.3 review plane; automated dispatch Gate A BLOCKED, `CODE_ALLOWED=NO`, `MERGE=NO`, `LIVE=NO`.
R3 host Bridge process identity, actual Git scopes/model/quota UNKNOWN.
R4 CHAT governance publisher/recorder for this decision; COPILOT read-only preflight candidate; CODEX future code candidate; WORK risk review candidate.
R5 GitHub branch provisioned without changing Windows user worktree; future Bridge writer exclusivity and local state UNKNOWN.
R6 exact grant document and provisioned ref may be remote-readback verified, but Bridge runtime Git push is not yet verified.
R7 STOP before Bridge service credential provisioning/pilot and all runtime Agent execution until separate prechecks pass.

## Acceptance statuses

OWNER_STANDING_GIT_SCOPE_GRANTED = YES
BRIDGE_OUTPUT_BRANCH_CREATED = YES
BRIDGE_OUTPUT_BRANCH_REMOTE_READBACK = YES
BRIDGE_HOST_SERVICE_IDENTITY_VERIFIED = NO/UNKNOWN
BRIDGE_GIT_PUSH_CAPABILITY_VERIFIED = NO
AUTOMATED_DISPATCH_GATE_A = BLOCKED_CAPABILITY_UNAVAILABLE
CODE_ALLOWED = NO
GIT_CODE_PUSH = NO
PR_CREATE = NO
MERGE_ALLOWED = NO
LIVE = NO
