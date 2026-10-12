# FOX2 reusable delta publication procedure

Publisher input: exact released Library path/file ID/version, release receipt, raw byte SHA256 and byte count, current SOURCE_INDEX, approved branch/base and writer scope. Do not infer latest release from root duplicates or filenames.

Compare each verified source digest with index + actual Git tree. SAME→reuse; NEW/CHANGED with legitimate release→eligible delta; missing receipt/hash mismatch→BLOCK; Candidate→exclude; historical→retain identity. If a prior platform safety refusal applies, stop that affected transfer until a supported compliant path is established; do not split/re-encode/re-route denied content.

Compute delta.json before write: ADD/MODIFY path, source identity/hash/bytes, old blob if any, target blob, authority receipt, allowed scope. Never delete or rewrite canonical Library from Git. Check .gitattributes -text for exact snapshots and CRLF data; Git object API bytes and local checkout behavior must be distinguished.

Commit/publish only the task-owned non-main branch with expected remote head and force=false. Verify actual remote SHA; read every changed source at that immutable commit; compare byte count/SHA256/version/receipt. Update SOURCE_INDEX with previously observed verification commit and record sync_receipt.json. A containing commit cannot self-reference its own SHA; final pointer/PR supplies the actual SHA outside committed report.

CHAT intake: fetch mandatory report+manifest at final SHA; schema v2 check, source/grant/path diff, every PASS evidence/hash, missingness/security and actual vs simulated checks. Store independent reviewer decision separately. Acceptance does not grant integration/DEV/provider.

Stop on safety/source drift/lease mismatch/secret risk. No global FOX/Silkworm/Mantis migration. No automatic background scheduler installed in this WP. This procedure is supported manual delta publication using connected APIs; it is not an unattended sync daemon.
