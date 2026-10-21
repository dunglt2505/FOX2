# FOX2 Bridge RC1 — F1 host authority contract (offline design; NOT_ATTESTED)

Whole-WP: `FOX2-BRIDGE-RC1-TO-INTERNAL-READY`. This is a design/negative-test evidence artifact, **not** an effective Policy or positive claim permission. Source code remains F0 fail-closed at installed root.

## Threat and trust boundary

The legacy Bridge process is **not** a participant in any new SQLite lease or new IPC lock. A current-runtime lock, file, configuration flag, SQLite `bridge_meta`, process absence snapshot, scheduled-task disable or Git manifest alone cannot prevent a previously installed legacy executable from starting again. Two SQLite ledgers can independently accept the same dispatch identity. No positive F1 claim may rely on either ledger alone.

## Mandatory independently enforced F1 authority (all conjunctive)

1. **Durable old-executor retirement:** An operating-system enforced and independently verifiable policy must block **all legacy launch surfaces and equivalent executable/script entry points**, including copied paths and automatic restart. The policy must remain enforced after user logoff, reboot, service/task reconfiguration and ordinary user attempts to remove the block. A mere ACL editable by the same legacy principal is insufficient. Verify actual enforcement with nonproduction synthetic probes; absence of a running legacy process is insufficient.
2. **Distinct trust anchor:** A trusted authority operating outside the Bridge process and outside the legacy user's mutable state must attest policy identity, scope, signer/issuer, epoch, package/source identity, and live revocation. SQLite rows, `current.json`, Git task files and self-signed receipts cannot serve as trust anchors.
3. **Single global namespace:** The authority must atomically serialize claim IDs across current and all historical roots. Before activation it must reconcile historical consumed IDs, in-flight/uncertain executions and manual consumption markers. Unknown or ambiguous identity => deny. The authority must prevent rollback to any runnable legacy writer.
4. **Claim-time freshness and execution lifetime:** A claim and every spawn must be conditioned on an authenticated, non-replayable, bounded authority lease bound to the exact source/package, dispatch ID, epoch and owner. Expiration, lost heartbeat, service failure, policy drift, clock rollback, ownership change, crash, restart, or lease revocation => deny further claims/spawns; already-claimed uncertain work must remain consumed, not replayed.
5. **OS evidence before package activation:** Test actual old-entrypoint denial and current approved-entrypoint permission in an isolated Windows environment, including restart/logoff, attempted bypass, copied scripts, alternate roots and direct ledger calls. A GitHub Actions ephemeral runner proves source/build/tests only, not the Owner host's retirement enforcement.

## Release decision

- F0 negatives: **retain**; new tests demonstrate that forged `bridge_meta` values do not unlock the installed root and that an unfenced old SQLite ledger can still claim independently.
- F1 positive authority: **NOT_IMPLEMENTED / NOT_ATTESTED**. No `SINGLE_ROOT` metadata migration, CLI `--config`, current root path change, temporary process kill, or unprivileged sandbox test is acceptable as a substitute.
- Package `5691a0d39873e9465ff6595a76ec0817013e55920440ec944e2dd9319dfa1112`: **CI-only F0 DENY quarantine**, not a production F1 artifact.
- Installed migration, Canary009, C4 `INTERNAL_FOX2_BRIDGE_READY`: **HOLD**.

## NEXT_SAFE_ACTION

Select and validate an enforceable Windows retirement mechanism and its independent authority principal; then implement a trusted F1 claim/lease protocol in the existing integrated Whole-WP. Keep a single package rollout after that. No executable host action or agent retry is authorized by this document.
