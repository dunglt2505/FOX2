# FOX2 — M1 v0.4 document release status / Windows preflight handoff

- **Decision:** OWNER_APPROVED, FOX2 M1-only BRD-00/06/08 + DSM data contract/schema, 105 tests and M1 roadmap.
- **Official Library publication:** 8/8 files uploaded and read back at matching raw SHA-256; formal receipt `FOX2_M1_V04_LIBRARY_RELEASE_RECEIPT_20261011.json`.
- **Source:** exactly one original frozen ZIP; `/Trading_Candidates/FOX2/20261011_M1_V04_EXACT_SOURCE/FOX2_M1_BRD_v0.4_20261011.zip`; SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895`.
- **Manifest:** SHA-256 `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`; 16/16 members verified.
- **Historical:** v0.2 BRD-00 retained, superseded by M1 v0.4 business revision; 06/08 previous 0.2/0.3 candidate snapshots unaffected.
- **Source publication DOES NOT authorize code:** CODE_ALLOWED=NO, Git mirror not yet written or verified, Windows host/WIP/model/quota/one-writer UNKNOWN, DNSE rights NOT VERIFIED.
- **M1-A planned:** provider disabled and localhost loopback; DSM/store/API/UI/watchlist semantics; fixtures are isolated test-only, investor UI unavailable/stale rather than fake prices.
- **M1-B planned:** DNSE public-market read only, read/redisplay/retention rights and host evidence prerequisite; historical Fox source referenced read-only, no credential or private data copying.
- **Next gate P1:** designated eligible Agent may execute an approved **read-only** Windows preflight, report repository/branch/HEAD/WIP/worktrees/access/model/quota without edits. Based on evidence, CHAT will verify source binding, mirror writer and separate exact DEV grant before coding.

## Published document identities

| Document | Published file ID | SHA-256 |
|---|---|---|
| `01_BRD/FOX2-BRD-00_v0.4.md` | `file_0000000042e88207ac43931c68a08d4a` | `e13b00581ab04c4bb2aabbfb196aec06475c2b0fc44d5b366ca2e382444ebef8` |
| `01_BRD/FOX2-BRD-06_v0.4.md` | `file_000000008b108211a99718fec9842fff` | `be3ce2d664401b176019d063182684f3ae043690c16a4c83b38ff43eea24dd1e` |
| `01_BRD/FOX2-BRD-08_v0.4.md` | `file_000000005c3c821186a3a79a9a670221` | `0e8b3c4206fee03f732588063eeb92ebb07af97d2164f06495a7f7539a893ca7` |
| `03_Data_Contracts/FOX2_MARKET_DATA_CONTRACT_v0.4.md` | `file_0000000080888207abd1cfe11289a447` | `ee63c40237f5fba84ea44abb95ae09ce5a06858a821f7fb3f47b7ec22a912dd2` |
| `03_Data_Contracts/FOX2_MARKET_DATA_v0.4.schema.json` | `file_0000000038fc8209804a20cdfa88697c` | `821914afe00a7d17de2c9ec805982f72ecffb455dbeff781759db395bc57bd52` |
| `05_Acceptance/FOX2_M1_ACCEPTANCE_v0.4.csv` | `file_00000000ed7c8207b68718624be6cf7c` | `ad1fd6ef4b4b150132366a5ccf1d465aa347e6411060f32fae4672777fb4bf92` |
| `05_Acceptance/FOX2_M1_V04_CHANGE_CONTRACT_AND_REQUIREMENT_MAP.md` | `file_00000000996c820689c45a0fcb66f2b8` | `cdc01892853ad87b563f962e567701ff37687950b5d4a166967487d2230dc73b` |
| `06_Roadmap/FOX2_M1_ROADMAP_v0.3.md` | `file_00000000f2fc8211a14ca7c90ad10b65` | `96e567e6743e5f4182b09737912a4e67b01cc7b0868a0499e1fa79e6181e14a8` |

## Agent roles (not dispatched)

- CHAT: completed L0 publish; coordinates source synchronization / preflight verification.
- COPILOT: preferred if actually accessible for Windows read-only preflight, routine API/UI after separately authorized M1-A; actual model/effort/quota still UNKNOWN.
- CODEX: optional DSM/store/WS if actual eligibility/quota and source/worktree/grant verified; concurrency review at WS checkpoint.
- WORK: no blanket audit; targeted review only if risk/actual gate warrants.
- STOP: no source mirror claims, no DEV, no changes to Fox old project, no DNSE real-data claims, no Git push/merge/remote actions without explicit permissions.
