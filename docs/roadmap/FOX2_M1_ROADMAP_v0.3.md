# FOX2 roadmap M1 v0.3 — OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified receipt)
> **FOX2 release edition · v0.4 · 2026-10-11 · OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified publication receipt).** This document derives from exact immutable M1 v0.4 ZIP source SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895` (source manifest `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`). Original roadmap candidate SHA-256 `9e6e4d9fa73aed9f110ed09a8d828e584fa665efb221ffc43ddb18b43b538e69` is retained unchanged inside that ZIP. All normative functional requirements and technical guards are preserved; editorial status changes only. This document alone does not grant DEV, Git, DNSE access, merge, push, broker access or LIVE. Status of automated tests: `NOT_RUN`. See the FOX2 M1 v0.4 publication receipt for actual Library file identity/readback.

Supersedes roadmap DSM v0.2 upon actual Library publication/readback; this is the next version of the same roadmap, not another progress master. Retained baseline copy is in 90_SourceEvidence. Current Policy/BRD00v0.2/main docs remain verified; no code accepted. M0 full-nine-BRD closure is not a prerequisite for this Owner-approved M1 slice.
| Step | Deliverable | Gate | Current |
|---|---|---|---|
| P0 | exact v0.4 00/06/08+contract+tests scope approval and source publication | Owner selects exact manifest; upload/readback; Git mirror only when Git handoff used | OWNER_APPROVED_LIBRARY_PUBLICATION_SUBJECT_TO_RECEIPT |
| P1 | Windows readiness + reuse inventory | current repo/HEAD/WIP/worktrees/one-writer/model/quota; no WIP cleanup | NOT_RUN |
| P2 | M1-A contract/DSM/store/API | provider disabled; isolated fixtures; unavailable semantics; no account/order path | NOT_STARTED |
| P3 | M1-A UI | overview/search/watchlist/Stock360/diagnostics; API contract pinned; no fake investor values | NOT_STARTED |
| P4 | M1-A checkpoint | offline negative + API/UI/state/store evidence; no realdata/LIVE claim | NOT_RUN |
| P5 | M1-B REST data slice | scoped read+redisplay+retention evidence, actual source mapping; reuse Fox patterns | BLOCKED_HOST_RIGHTS_UNKNOWN |
| P6 | M1-B WS data slice | rights/auth/sub ACK + one-symbol/index/frame ingest + data freshness/calendar config | BLOCKED_HOST_RIGHTS_UNKNOWN |
| P7 | M1-B recovery+acceptance | disconnect/restart/overflow/normal close/backfill; actual in-session evidence; focused independent reviewer if required by approved risk scope | NOT_RUN |
| M2 | expand coverage/depth/PIT/soak/corporate actions | accepted M1 baseline, separate rights/data gates | NOT_STARTED |
| M3/M4 | analytics/risk/capital/exit/shadow | own BRD/method evidence; no automatic scope expansion | NOT_STARTED |
P1 is read-only scope/eligibility collection, not coding dispatch. P2/P3 can proceed before provider rights are resolved once M1-A source/DEV/host gates pass. P5/P6 never run from approval of P2 alone. Serial writer first; parallel UI/API only with frozen contract and verified disjoint worktrees. Watchlist PUT is local preferences only. No promised completion date without actual host effort estimates.
