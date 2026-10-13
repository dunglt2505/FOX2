# FOX2 — M1-0 Windows Preflight | Git-first task record

**Record status:** `PREPARED_IN_LIBRARY / NOT_DISPATCHED / GIT_TASK_MIRROR_PENDING`  
**Policy:** `FOX2_POLICY_V1.2.md` (released Library SHA-256 `bd43e0b878a4b671866486e0d8247b39dfb0f42a0391d50b273e85b697e9d350`)  
**Task ID:** `FOX2-M1-0-DNSE-REALDATA-PREFLIGHT`  
**WP ID:** `FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY`  
**Owner:** CHAT (coordination) | **Candidate executor:** COPILOT on Windows, model/mode/quota `UNKNOWN/NOT_VERIFIED`

## R0: Reuse evidence, do not redo

The previous Windows readiness returned `BLOCKED`, **not PASS**. The Windows host was observed; local Git WIP, Policy/local source bytes, Copilot model/quota, data rights and DNSE market-store metadata remain unknown. Published M1 v0.4 8-file Library source set stays authoritative; M1 v0.4.1 / M2 v0.4.2 remain Candidates. Existing M1-0 prompt V1.1 is history; this Git-first task/policy V1.2 is its successor **when mirrored and dispatched**.

## Read sources from Git/local only

- Expected future Git task: `docs/agent_handoff/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/task.md` plus `source_manifest.json` at a **pinned full commit** — `GIT_MIRROR_PENDING` now.
- Policy V1.2 exact Library SHA above; receiving Agent must verify the mirror/local bytes, not browse ChatGPT Trading Library.
- Prior remote `main` observation: `f311c1fc5b2f37962b30d4af3d90cc8dc30bd8a8` (recheck; NOT an approved task baseline).
- Source-set manifest from M1-0 preflight ZIP: SHA-256 `160892e7132072f54526500ca2b1d9e44bce4b48c2eeb7b35b16efeea39f8285` (receiver check still NOT_RUN). Verify 8/8 frozen snapshots.

## Allowed behavior — conditional read-only inspection

After `POLICY_CHECK → TASK_STATE_CHECK → R0–R7 → ASSIGNMENT_CHECK` and successful actual model/host/quota/source/rights/WIP checks: inspect Git `C:\Projects\FOX2`, legacy `C:\Projects\Fox` technical reference read-only, local public-market DNSE connector/store **metadata only**. Do not query Production, authorize credentials, read private account data, open WebSocket, install tools, edit code, run provider tests or manipulate Git state.

## Git result destination and rights separation

Proposed result: `reports/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY/report.md` and `evidence_manifest.json` on an isolated branch `work/FOX2-WP-M1-0-DNSE-HOST-EVIDENCE-READONLY-copilot` **only after** writer ownership, branch and `GIT_REPORT_WRITE/ GIT_REPORT_PUSH` independently PASS.

`GIT_SOURCE_READ=UNKNOWN` · `GIT_REPORT_WRITE=NO` · `GIT_REPORT_PUSH=NO` · `CODE_ALLOWED=NO` · `GIT_CODE_PUSH=NO` · `MERGE_ALLOWED=NO` · `DNSE_PRODUCTION=NO` · `BROKER_WRITE=NO` · `LIVE=NO` for the current preparatory checkpoint.

**Do not infer** report-push approval from this file or from a read-only preflight prompt. If no push authority, return `REPORT_LOCAL_ONLY/PUSH_BLOCKED` and let CHAT route an authorized evidence-only writer. A chat response alone is not evidence published to Git.

## Required report and STOP

Supply R0–R7, Policy/hash, actual Copilot model/mode/quota (or observed UNKNOWN), Git origin/HEAD/tracked/untracked/ignored WIP/writer, source 8/8, DNSE existing metadata, rights/retention, real-data slice or NOT_VERIFIED, risk/negative checks, STOP and precise next action. Never claim `ACCEPTED` or `M1-0 PASS` without independent CHAT review of immutable Git evidence and separate scoped authority.
