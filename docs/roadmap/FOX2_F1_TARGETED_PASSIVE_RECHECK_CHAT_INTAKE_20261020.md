# FOX2 — CHAT F1 targeted passive host recheck intake (2026-10-20)

**Existing Whole-WP:** `FOX2-BRIDGE-RC1-TO-INTERNAL-READY` · **Feature:** `FOX2-BRIDGE-MANUAL-LOCAL-ADMISSION` · **Stage:** BUILD / BLOCKED.

## Owner-supplied evidence and provenance

Owner pasted console JSON in the active conversation: schema `FOX2_F1_TARGETED_PASSIVE_RECHECK_V1`, `mode=READ_ONLY_NO_AGENT_NO_SQLITE`, `observed_utc=2026-10-20T14:19:12.6441716Z` (21:19:12 ICT). **This is Owner-host-reported point-in-time output, not remotely verified runtime attestation, not an Agent result, and not a replacement for installed-control readback.** This public Git review omits personal paths, actual hashes, raw action arguments, process command lines, IDs and credentials.

Bound source/authority: Governance Registry blob `1c28a6372a1cbbfd5341691ac9a5f98c8aa03e35` on Owner governance release branch; Policy v2.0.0 governs scoped CHAT work, installed enforcement NOT_ATTESTED. Previous F1 snapshot review `ef597fad40c6b02dfe2a88bb9b976020fc3ff210:docs/roadmap/FOX2_F1_PASSIVE_HOST_SNAPSHOT_CHAT_INTAKE_20261020.md`; F1 matrix `cdfdb703abe83c76f7aaac7cbd14e5b020a7b106:docs/roadmap/FOX2_F1_LEGACY_RETIREMENT_ADMISSION_READINESS_20261020.md`.

## Verified only within the Owner-reported snapshot

- Exactly TWO currently enumerated Bridge-named executable candidates under **versioned/package subtree** (relative depth 4): `FOX2.Bridge.Desktop.exe`, 152064 bytes, FileVersion `1.0.0.0`; and `fox2-bridge.exe`, 108458 bytes, FileVersion empty. Owner-provided SHA256s match the two ordinal `CURRENT_EXECUTABLE_1` and `CURRENT_EXECUTABLE_2` snapshots at 14:13:09Z. Name-to-digest reconciliation `PASS_OWNER_OUTPUTS`, **NOT** installed source/package Git commit provenance.
- Exactly THREE matching observed processes: current-referenced Python parent process not observed; Python child parent observed as current-referenced Python; current-referenced desktop executable parent not observed. No control-state or OS writer-lease validation. `ONE_WRITER=UNKNOWN`.
- TWO scheduled-task candidates returned: current SID Bridge task `Ready`, pwsh action CURRENT_REFERENCE; unrelated/other FOX2 candidate `Disabled`, pwsh action OTHER_FOX2_REFERENCE. An enabled task can restart software and a disabled task is not proof that all old launch surfaces are disabled.
- **More than one repeated** `TASK_ITEM_PropertyNotFoundException` under `errors`, visibly many identical occurrences. We do not rely on an exact count. As a result `SCHEDULED_TASK_INVENTORY=PARTIAL_WITH_ERRORS`; inability to inspect skipped actions must not be interpreted as absence of other FOX2 launchers.
- **Likely tooling defect:** the PowerShell 7 strict-mode script directly accessed `$action.Execute` and `$action.Arguments`; Scheduled Task actions may have alternate CIM subtypes/properties. An absent property would throw `PropertyNotFoundException` and be caught per task. This is a plausible diagnosis from the source and error class, **not demonstrated cause for any specific task** without property-safe recheck.
- User-host output still explicitly marks `installed_source_adoption=NOT_ATTESTED`, `worker_state=NOT_ATTESTED`, `legacy_retirement=NOT_VERIFIED`. The prior legacy SQLite DB remains PRESENT in older snapshot. No SQLite/installed controls or process state changed in this interaction.

## Scoped acceptance and blockers

`ACCEPT_SCOPED_EXECUTABLE_NAME_HASH_MAPPING` · `HOST_OBSERVATION_PARTIAL` · `SCHEDULED_TASK_AUDIT_INCOMPLETE` · `F1_DURABLE_RETIREMENT_NOT_VERIFIED` · `INSTALLED_ONE_WRITER_UNKNOWN` · `F1_POSITIVE_ADMISSION_HOLD` · `CANARY_HOLD`.

Current F0 source `611ec26c28484de740e963d86de6b00946f1492d` intentionally denies configured runtime positive claims under unresolved dual-root authority. It has already received bounded offline CHAT acceptance; **do not** claim installed adoption or positive claim authorization, clear `DENY_CROSS_ROOT_UNKNOWN`, fabricate Agent Result v2 or replay consumed CODEX Attempt06.

## NEXT_SAFE_ACTION

Replace only the faulty Scheduled Task observation with a property-safe **read-only** enumeration that:
1. Reads optional action properties using `PSObject.Properties['Execute']` and `['Arguments']`, without direct missing-property access under strict mode; preserves unknown action class, error counts and completeness markers.
2. Differentiates `Exec` actions from `ComHandler` or other actions; reports task class/root-reference only, no raw commands or identities.
3. Returns a global `coverage=COMPLETE` only when enumeration and all per-item observations have no errors. `UNKNOWN` if any task/action couldn't be inspected.

No new Agent/coding assignment, no runtime/DB/task edits, no installed launch/Canary or main/merge/provider/broker/LIVE. A clean Scheduled Task inventory still does NOT prove durable legacy retirement; F1 positive admission stays gated on old-writer restart-proof retirement or shared atomic authority, and actual installed source/lease/rollback evidence.

**R0–R7:** existing BUILD/BLOCKED WP; Owner-provided read-only evidence; CHAT-direct result intake; no Agent/host pre-execution requirement for document work; non-main Git report only with readback; `ASSIGNMENT_CHECK=NOT_APPLICABLE`. Skills: source-resolver, result-review, feature-certification, status-roadmap and governance-preflight APPLIED; new Agent Prompt Builder NOT_APPLICABLE.
