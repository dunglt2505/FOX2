# FOX2 — F1 legacy retirement / installed admission evidence readiness

**Date:** 2026-10-20. **Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION`. **Task type:** CHAT read-only evidence reconciliation and candidate gating; NO F1 installed execution or coding task.

## Current gate state

`F0_OFFLINE_BUILD=ACCEPTED_CHAT_DIRECT_SCOPED` at source `611ec26c28484de740e963d86de6b00946f1492d` by report `008c6e7d1a1c2d7456a3530ce6e3f38e88510600`, independent acceptance `62e7629b8fedcb47ff0ddb59d6e1d02b9df4cb09`, and CHAT-direct formal disposition `4d3330f8f0cf1f3aeaaacc611ff406301858ebbc`. CODEX Attempt06 consumed and Agent Result v2 not delivered. F0 acceptance does **not** certify installed or real-Agent behavior.

`F1_DURABLE_LEGACY_RETIREMENT=NOT_VERIFIED` · `INSTALLED_POSITIVE_ADMISSION=HOLD` · `WORKER_ONE_WRITER=UNKNOWN` · `CANARY009=HOLD` · `INTERNAL_READY=NOT_ATTESTED`.

## Actual Git/runtime facts

- Final F0 source `611ec26...:agent_bridge/src/fox2_agent_bridge/desktop.py`, blob `b835842eb72dfeba84c8a7c20eb7ec85076c4ae2`, executes `ledger.initialize(cross_root_authority_unknown=True)` for **every configured runtime root**. This is intentional fail-closed protection. **F1 positive admission cannot be achieved by declaring the current F0 source operationally ready**; a separately reviewed durable-authority transition and compatible code/tests would be needed.
- The current ledger performs local SQLite transactional claim validation; no evidence exists that an old separate legacy executable/database shares that atomic identity mechanism. A copy of old SQLite into new at boot and temporary lock alone cannot prevent old-binary restart and duplicate claims. Do not clear `DENY_CROSS_ROOT_UNKNOWN` because a one-time inventory appears negative.
- Last Owner-host read-only inventory on 2026-10-20, summarized in `44390e142f3dc5a7eace0a97c5b28c545d376b0b:docs/roadmap/FOX2_BRIDGE_DURABLE_FENCING_OFFLINE_BUILD_DECISION_20261020.md`: legacy `C:\\Projects\\FOX2-AgentBridge\\data\\bridge.db` PRESENT (294,912 bytes); old launcher names absent in inspected locations; current Bridge processes/current logon task observed; another disabled FOX2 task unclassified. Last two parent processes only partially attributed. None proves durable old-writer retirement or current Worker PAUSED/claims.
- Read-only inventory contract `8f072f99c22a8201a3c6f04ba5dafa62ea55d2fc:docs/roadmap/FOX2_BRIDGE_LEGACY_HOST_LIFECYCLE_INVENTORY_CONTRACT_20261020.md` forbids touching SQLite bytes, persistent controls, jobs, services, installed files or private credentials. An owner-host negative snapshot is only `NO_LEGACY_ENTRYPOINT_OBSERVED_IN_SCOPED_INVENTORY`, never `DURABLE_RETIREMENT_VERIFIED`.

## F1 evidence / gate matrix

| Material gate | Current proof | Verdict | Actual exit evidence needed |
|---|---|---|---|
| G1 Complete old/current executable, version, launcher, startup and alternate-root identity | Scoped Owner-host snapshots; missing full launcher/alias/supervisor closure | PARTIAL / UNKNOWN | Passive full eligible entrypoint/root/alias/signer inventory with redacted readback, installed artifact hashes |
| G2 Current Bridge Worker state, process/lease and runtime owner | Three current-root candidate processes observed; no control/lease read | UNKNOWN | Safely verified passive PAUSED/STOP/single writer/lease and process lineage; don't run a status command that mutates initialization |
| G3 Durable old writer fencing / retirement | Missing legacy launch.ps1, disabled unrelated task and no observed old PID insufficient | NOT_VERIFIED | A separately authorized durable disable/replace of *all* old launch surfaces with restart-denial proof and rollback; OR a genuinely joint atomic identity authority honored by both binaries |
| G4 Consumed dispatch identity across both roots | Old legacy DB present but bytes/rows not inspected in this scope | UNKNOWN / PROTECT | Non-destructive, separately admitted source/host verification of consumed IDs and manual markers with strict privacy/reconciliation, no deleting or copying mutable live DB as a shortcut |
| G5 Positive-authority transition and dual-root invariants | F0 always initializes configured runtime roots in DENY mode | NOT_IMPLEMENTED / HOLD | Versioned candidate source/TechSpec/acceptance with genuine verified-authority transition; negative/restart/concurrency/rollback tests, no ad hoc editable token |
| G6 Installed exact-source adoption and rollback | F0 code exists only in Git source and offline runs | NOT_RUN | Installed package SHA, authenticated permitted artifact/process mapping, quiescence, backup/rollback, pre/post upgrade tests |
| G7 Real installed no-replay and one-shot positive Manual Local | No admitted installed run; no real Agent | NOT_RUN / HOLD | Fresh route-bound PreExec, observed exclusive one-writer, eligible exact prompt/model/profile; one authorized run and same consumed-ID restart check |
| G8 Final RC1/Canary acceptance | Seven final gates not run on this subject | NOT_RUN / HOLD | Exact source/config/readback/usage/restart/CHAT intake gates after separate Canary authorization |

## F1 route decision (R0–R7)

`R0` Existing Whole-WP and feature BUILD/BLOCKED; `R1` F1 evidence readiness only; `R2` human scoped Owner engineering direction, no new installed activation consent claimed; `R3` no PreExec for read-only Git/document analysis, but NEW host executable route requires fresh material gates; `R4` CHAT direct analysis, no WORK or CODEX delegated; `R5` report-only dedicated non-main Git branch, no competing code writer invoked; `R6` Git report/readback, no runtime change; `R7` preserve old one-shot identities and strict F1 exit evidence; `ASSIGNMENT_CHECK=NOT_APPLICABLE`.

Two *candidate* technical ways to unlock F1 are (A) **durably retire all eligible old launchers/binaries** then implement attested authority transition in the current installed build, or (B) **prove a joint atomic consumed-ID authority shared by both binaries**, including old executable compatibility. There is currently **no evidence** route B is feasible without changing the legacy binary, so no positive path is selected.

**Immediate safe next host dependency:** one short private, passive Windows inventory of executable/launcher roots, exact current installed package hash and Worker control provenance, with public-output sanitization. Existing Owner host evidence is reused, not re-run as generic audit. Any privacy-sensitive host evidence stays local/private until independently reviewed; do not push raw process command lines, user IDs, tokens, or SQLite bytes to public Git. If no direct host connection, host proof is a true environmental blocker, not an excuse to replay CODEX Attempt06.

**STOP:** no installation, disabling/removing tasks, registry edits, legacy DB modifications, Worker start/resume, self-signed positive token, Dispatch001/Canary009 replay, main/merge/provider/broker/LIVE. Owner's earlier explicit coding HOLD on `CODEX/gpt-6.1-sol/medium` stays in force unless a new authorized route changes it.

**NEXT_SAFE_ACTION:** request only the missing passive host F1 fields, validate private read-only results, choose a material F1 authority/rollback design under existing Whole-WP, and admit a NEW host/code task only after genuinely new source/route PreExec/one-writer gates and Prompt Builder. No F1 runtime execution has begun.
