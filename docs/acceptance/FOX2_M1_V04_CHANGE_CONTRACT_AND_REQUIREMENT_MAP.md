# BCC và requirement → acceptance v0.4
Change ID FOX2-BCC-M1-DSM-20261011-v04; OWNER_APPROVED / LIBRARY_PUBLISHED, subject to actual readback.
Tất cả IDs cũ bảo toàn; đây là revision của00/06/08, supersedes BRD-00 v0.2 only after successful release/readback. Chốt sliceM1, các thuật toán01..05/07 không được phê duyệt trong gói. Source authority FOX2 PolicyV1.0+Owner; technical reuse không import governance.
| Requirement | Test IDs |
|---|---|
| FOX2-00-R01 | FOX2-00-T01 |
| FOX2-00-R02 | FOX2-00-T05 |
| FOX2-00-R03 | FOX2-00-T02, FOX2-N1-T03 |
| FOX2-00-R04 | FOX2-N1-T01, FOX2-N1-T06 |
| FOX2-00-R05 | FOX2-00-T03 |
| FOX2-00-R06 | FOX2-06-T13, FOX2-08-T04 |
| FOX2-00-R07 | FOX2-00-T01, FOX2-00-T06 |
| FOX2-00-R08 | FOX2-00-T90 |
| FOX2-00-R09 | FOX2-00-T01, FOX2-00-T91 |
| FOX2-00-R10 | FOX2-00-T04, FOX2-06-T14, FOX2-N1-T12 |
| FOX2-00-R11 | FOX2-00-T05, FOX2-00-T06, FOX2-00-T07 |
| FOX2-06-R01 | FOX2-06-T18, FOX2-06-T24 |
| FOX2-06-R02 | FOX2-06-T06, FOX2-06-T07, FOX2-N1-T02 |
| FOX2-06-R03 | FOX2-06-T03, FOX2-N1-T09 |
| FOX2-06-R04 | FOX2-06-T10, FOX2-06-T19, FOX2-06-T20, FOX2-06-T21, FOX2-06-T22 |
| FOX2-06-R05 | FOX2-06-T13 |
| FOX2-06-R06 | FOX2-06-T09, FOX2-06-T16 |
| FOX2-06-R07 | FOX2-06-T05, FOX2-06-T16 |
| FOX2-06-R08 | FOX2-06-T15, FOX2-08-T08 |
| FOX2-06-R09 | FOX2-06-T16, FOX2-06-T24 |
| FOX2-06-R10 | FOX2-06-T06, FOX2-06-T07, FOX2-06-T08, FOX2-06-T11 |
| FOX2-06-R11 | FOX2-06-T12, FOX2-06-T17, FOX2-06-T23 |
| FOX2-06-R12 | FOX2-06-T19, FOX2-06-T20, FOX2-06-T22 |
| FOX2-06-R13 | FOX2-06-T09, FOX2-N1-T07 |
| FOX2-06-R14 | FOX2-N1-T11, FOX2-06-T18 |
| FOX2-06-R15 | FOX2-06-T14, FOX2-N1-T12 |
| FOX2-06-R16 | FOX2-WS08, FOX2-06-T16 |
| FOX2-06-R17 | FOX2-06-T17, FOX2-06-T12, FOX2-N1-T06 |
| FOX2-06-R18 | FOX2-WS01, FOX2-WS02, FOX2-WS03, FOX2-WS04, FOX2-06-T19 |
| FOX2-06-R19 | FOX2-WS05, FOX2-WS07, FOX2-06-T22, FOX2-06-T24 |
| FOX2-06-R20 | FOX2-N1-T02, FOX2-N1-T07, FOX2-06-T23 |
| FOX2-08-R01 | FOX2-08-T05, FOX2-N1-T10 |
| FOX2-08-R02 | FOX2-08-T02, FOX2-08-T03, FOX2-08-T10, FOX2-08-T11 |
| FOX2-08-R03 | FOX2-08-T06, FOX2-08-T07, FOX2-08-T11 |
| FOX2-08-R04 | FOX2-08-T13 |
| FOX2-08-R05 | FOX2-08-T04, FOX2-06-T13 |
| FOX2-08-R06 | FOX2-08-T04 |
| FOX2-08-R07 | FOX2-08-T01, FOX2-08-T02, FOX2-08-T12 |
| FOX2-08-R08 | FOX2-08-T08, FOX2-08-T13 |
| FOX2-08-R09 | FOX2-08-T05, FOX2-08-T06, FOX2-08-T07 |
| FOX2-08-R10 | FOX2-N1-T12, FOX2-08-T13 |
| FOX2-08-R11 | FOX2-06-T15, FOX2-08-T08 |
| FOX2-08-R12 | FOX2-08-T02, FOX2-08-T03, FOX2-08-T11, FOX2-08-T12 |
| FOX2-08-R13 | FOX2-08-T10 |
| FOX2-08-R14 | FOX2-08-T09, FOX2-08-T12 |
| FOX2-08-R15 | FOX2-08-T14, FOX2-08-T13 |

Impact: BRD00 product/M1 boundary;06 data/schema/store/WS;08 presentation/watchlist. API changes owned06; preference presentation/domain owned08. New mode PROVIDER_NATIVE_UNVERIFIED and local preference PUT are explicit material changes requiring exact scope decision.
Publication flow: exact manifest decision → actual Library source publication/readback/receipt → Git mirror only for Git handoff → receiver hashes/source resolution → host/model/quota/one-writer/scoped DEV grant → M1-A. Permission conditions are not test PASS; runtime remains NOT_RUN.
Source drift or contract changes require updated BCC/re-pin; no reapproval loop for unchanged recorded Owner grant.
