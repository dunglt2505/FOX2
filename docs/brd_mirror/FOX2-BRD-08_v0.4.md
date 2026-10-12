# FOX2-BRD-08 — Investor Dashboard & Stock 360º
> **FOX2 release edition · v0.4 · 2026-10-11 · OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified publication receipt).** This document derives from exact immutable M1 v0.4 ZIP source SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895` (source manifest `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`). Original BRD-08 candidate SHA-256 `31787eef1cedb89775a57ef618ca26268904d59a41c35157f011c3530276513b` is retained unchanged inside that ZIP. All normative functional requirements and technical guards are preserved; editorial status changes only. This document alone does not grant DEV, Git, DNSE access, merge, push, broker access or LIVE. Status of automated tests: `NOT_RUN`. See the FOX2 M1 v0.4 publication receipt for actual Library file identity/readback.


**Project:** FOX2 — Vietnam Equities Investment Intelligence  
**Version:** 0.4 · 2026-10-11 · **Status:** `OWNER_APPROVED / LIBRARY_PUBLISHED` · first published version for this BRD; earlier v0.2/v0.3 were Candidates  
**Owner domain:** `FOX2-BRD-08` · **Accepted runtime:** `NONE`  
**Purpose:** Website localhost hiển thị và giải thích dữ liệu đầu tư từ giai đoạn đầu, không tự tính lại kết quả engine.

**FOX2-only authority:** `FOX2_POLICY_V1.0.md` (published internal-document governance) và quyết định của Owner FOX2. Tài liệu này không nhận quy định, approval, quyền kỹ thuật hoặc release từ bất kỳ dự án nào khác; chỉ tham chiếu các yêu cầu, hợp đồng và BRD được xác lập trong FOX2.

## Scope and user outcomes
- Giao diện đa màn hình: Market Overview, Sector, Discovery, Stock 360°, Portfolio, Risk, Research
- M1 localhost sử dụng **dữ liệu DNSE Production thực nếu source được DSM xác thực đủ quyền, chất lượng và host**; thiếu nguồn thì hiện `UNAVAILABLE/STALE` chứ không thay bằng dữ liệu giả. Test fixture `SYNTHETIC` chỉ hoạt động trong test mode tách biệt, gắn nhãn không phải dữ liệu đầu tư.
- Recharts/Lightweight Charts đề xuất phải kiểm tra bản quyền, chart adapter thay renderer
- Why?/evidence/cutoff/dữ liệu thiếu nhìn thấy ở UI

## FOX2-only boundary & cross-BRD contract

- **Chủ quyền:** `08` là owner của các requirement `FOX2-08-Rxx`; quyết định nội bộ thuộc Owner FOX2 theo Policy FOX2 V1.0. Không sử dụng tài liệu/quyền/trạng thái từ dự án khác làm gate.
- **Luồng dữ liệu/đầu vào:** Đầu vào: FOX2-BRD-06 (`FOX2 Data Source Manager`: quotes, bars, provider provenance, source-selection/quality/health), FOX2-BRD-05 (analytics), FOX2-BRD-02 (opportunities), FOX2-BRD-01 (allocation), FOX2-BRD-03 (risk), FOX2-BRD-04 (exit), FOX2-BRD-07 (research).
- **Luồng dữ liệu/đầu ra:** Đầu ra: các trang localhost Market, Sector, Stock360, Portfolio, Risk và Research với thông tin nguồn/độ mới.
- **Ranh giới trách nhiệm:** BRD-08 chỉ render và điều hướng; không thay đổi dữ liệu nguồn, thuật toán, hạn mức rủi ro hoặc trạng thái lệnh.
- **Quy tắc hợp đồng:** mọi consumer dùng đúng `requirement_id`, source version, assessment/as-of và quality; thay đổi logic thuộc BRD owner phải qua quyết định FOX2 có phạm vi, không tạo bản master song song.

## Functional requirements

| Requirement | Normative FOX2 M1 v0.4 requirement | Primary output | Priority | State |
|---|---|---|---|---|
| `FOX2-08-R01` | Homepage thể hiện VN-Index/HNX/UPCoM theo nguồn, breadth, flow/turnover, rủi ro, nhóm ngành và cổ phiếu kéo/đạp khi có methodology. | `MarketOverview` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R02` | Có Watchlist/Search/Stock360/PriceVolumeChart với chart adapter, raw/adjusted basis và confirmed/provisional. | `StockReview` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R03` | Mỗi widget hiện trạng thái SYNTHETIC/LIVE/STALE/UNAVAILABLE, as_of, coverage và thông báo bất khả dụng. | `SourceBadge` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R04` | UI chỉ render server/domain snapshots có cùng assessment_id và version; không tự sinh BUY/SELL trong JavaScript. | `EvidenceLinks` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R05` | Portfolio/Risk pages phải tránh phô dữ liệu private khi chưa login; placeholders không giả số NAV. | `PrivateView` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R06` | Chart interaction không tự submit, modify hoặc cancel order; ticket tương lai phải qua quyền độc lập. | `NoLiveOrderUI` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R07` | Dashboard có responsive navigation và data diagnostics; render nguồn thật khi DSM VERIFIED, trạng thái không khả dụng khi thiếu feed, không bật mock trong investor mode. | `MVPUsability` | P0 | `SPECIFIED_APPROVED` |

## Acceptance and negative tests

| Test | Verification scenario | Expected |
|---|---|---|
| `FOX2-08-T01` | localhost frontend/API chạy read-only với DSM API thật nếu đủ quyền; thiếu feed phải hiện UNAVAILABLE rõ, fixture chỉ ở isolated test mode | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-08-T02` | Market/Stock/Watchlist điều hướng hoạt động | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-08-T03` | Chart gap, ATC provisional và stale rõ | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-08-T04` | Không có nút live order hay private user leakage | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-08-T90` | Quét BRD/phụ thuộc: không dùng Policy, approval, release gate hoặc authority từ dự án khác làm governance FOX2; technical reference được gắn nhãn và pinned; các liên kết `FOX2-BRD-xx` hợp lệ phải được giữ | PASS chỉ khi tất cả tham chiếu quản trị là FOX2-only và các dependency nội bộ còn nguyên; trường hợp vi phạm phải FAIL, không tự publish |
| `FOX2-08-T91` | Mã requirement/test cũ được bảo toàn; quyền DEV/Git/LIVE hoặc bằng chứng nghiệm thu không được cấp từ việc sửa câu chữ | PASS khi các ID v0.1 còn đủ và hiệu lực chỉ là `CANDIDATE_FOR_OWNER_REVIEW`; chưa chạy thực tế = NOT_RUN |

## FOX2 Data Source Manager integration — M1 real-market UI

`FOX2-BRD-06` duy nhất quyết định nguồn và trạng thái. Dashboard/Stock360 **chỉ gọi typed FOX2 backend API** (`/api/market/overview`, `/api/stocks/{symbol}`, `/api/stocks/{symbol}/bars`, `/api/data-sources/health` là route **đề xuất**, không phải endpoint DNSE đã xác minh). React không tự kết nối DNSE, đọc trực tiếp database, thay `as_of`, hoặc chọn giữa socket và local. Widget hiển thị provider origin, retrieval, source selection reason nếu cần troubleshooting; cảnh báo data staleness/synthetic clearly separated.

**UI response rule:** `LIVE` chỉ khi DSM xác thực; `LATEST_VALID/EOD_CONFIRMED` phải cho biết giá trị cuối theo phiên; `STALE/DELAYED/GAP_RECOVERING` hiển thị banner/cutoff, không biến thành live; `ENTITLEMENT_BLOCKED/UNAVAILABLE` không hiện 0 hoặc số giả. Nếu M1 local không lấy được DNSE tại runtime, homepage vẫn hoạt động với states/diagnostics nhưng **không chế ra giá VN-Index/cổ phiếu**.

**Design input (reference only):** `/Trading/FOX2/90_References_FOX_READONLY/Website_Concept_Design_v1.0/` hiện mới có 1/4 ảnh gốc được xác minh theo lần kiểm kê gần nhất; không khẳng định bộ design hoàn chỉnh và không lấy thư mục tham chiếu làm nguồn thẩm quyền BRD.

### New requirements v0.3

| Requirement | Normative FOX2 M1 v0.4 requirement | Output | Priority | State |
|---|---|---|---|---|
| `FOX2-08-R08` | Mọi widget đọc FOX2 DSM API thay vì gọi trực tiếp DNSE WS/API hay local DB. | `DSMViewAdapter` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R09` | Hiển thị source mode, provider, actual event/as_of, revision, freshness, license-safe status và missing-data health. | `DataProvenancePanel` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R10` | No fallback-to-synthetic in investor mode; fixture chỉ test cô lập, không trộn vào dữ liệu live. | `SourceIntegrityUX` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-08-R11` | `/settings/data-sources` hiển thị diagnostics read-only, tình trạng ws/api/local, entitlement được redact, không thao tác secret ở browser. | `DataSourceDiagnostics` | P1 | `SPECIFIED_APPROVED` |

### New acceptance v0.3 — `SPECIFIED_NOT_EXECUTED`

| Test | Scenario | Expected |
|---|---|---|
| `FOX2-08-T05` | WS thật up, DSM API trả LIVE verified | Widget hiện DNSE + event/as_of + quality; không tự suy trạng thái |
| `FOX2-08-T06` | WS disconnect, store có snapshot cũ | Badge/banners STALE/LATEST_VALID chính xác; không lấy fixture thay |
| `FOX2-08-T07` | Mất entitlement hoặc no market data | UI vẫn mở; số thị trường UNAVAILABLE thay vì 0 hoặc synthetic |
| `FOX2-08-T08` | UI inspector/search/chart | Không có trực tiếp DNSE auth/topic/token/private scope và không bypass DSM |
| `FOX2-08-T09` | Design references mới có 1/4 ảnh | Không claim thiết kế gốc import đủ, không phụ thuộc ảnh thiếu để nghiệm thu UI cơ bản |

## Out of scope / open gates

- Renderer/license, UX breakpoints, UI data freshness và performance budget cần kiểm thử thực
- No release, broker-write, margin or trading automation is granted by this BRD.

## Handoff & traceability

- Producer/consumer boundaries follow `FOX2-BRD-00`; BRD-06 owns data facts and BRD-07 owns empirical acceptance.
- Lịch sử sửa đổi: đối chiếu `FOX2_BRD_V02_CHANGE_MANIFEST_20261011.json` (nguồn là bản FOX2 v0.1); các phiên bản trước chỉ là lịch sử, không làm nguồn quản trị.
- Chỉ số nội bộ: `FOX2_BRD_INDEX_v0.2.md`. Các BRD phụ thuộc được định danh bằng `FOX2-BRD-xx`; không có liên kết quản trị ngoài FOX2.
- On implementation, link each requirement to test IDs, code change, verification status, and separately authorized promotion evidence.

**Change intent v0.3:** tích hợp `FOX2 Data Source Manager` do BRD-06 sở hữu, chuyển website M1 sang dữ liệu DNSE thực qua API chuẩn khi đủ điều kiện, cấm fake fallback. Bản này đã được chốt cho phạm vi M1 và phát hành tài liệu theo receipt; không cấp quyền DEV/Git/LIVE.

## Revision v0.4 — phạm vi chốt M1

Change ID: FOX2-BCC-M1-DSM-20261011-v04. Tài liệu này là bản đầy đủ kế tiếp của cùng BRD, không tạo BRD master song song. Phạm vi trình duyệt: M1-A và M1-B trong bộ manifest; BRD-01/02/03/04/05/07 chưa được duyệt thuật toán qua gói này. Các yêu cầu ngoài M1 được giữ để truy vết, không kéo vào DEV M1.

Nguồn tham khảo kỹ thuật: Fox commit 740051933ec4fbf29180d0f5fb698c34e8c91ece và DNSE SDK aa55a5117de2534707bca6165b6738e1cc6fc6a4; N1 v1.1-candidate. Source Fox/SDK là evidence kỹ thuật, không mang governance hoặc quyền DEV của dự án đó sang FOX2. Policy duy nhất: FOX2_POLICY_V1.0.md. Accepted runtime vẫn NONE.

Approval gói v0.4 phải bind đúng MANIFEST.json, ba BRD, contract và acceptance; đề nghị grant M1-A trước. M1-B chỉ được kết nối khi gate capability/rights/secret/host đạt. Approval không phải bằng chứng code, test, merge hay LIVE đã hoàn tất.


### FOX2-08-R12 — M1 screen contract
React/TypeScript/Vite, FastAPI, modular monolith. Routes /overview, /watchlist, /stocks/:symbol, /settings/data-sources. /sectors,/discovery,/portfolio,/risk,/research hiện navigation và unavailable reason khi engine chưa được nghiệm thu. Missing data không dùng zero cards hoặc fake trend chart.
Stock360 chỉ hiện quote payload của quote capability; history close không giả latest trade. Chart adapter nhận OHLCV đã typed, gap list, basis/unit, provisional và revisions; không sinh bar trong khoảng no-trade hoặc gap. Hiển thị giá-volume đồng bộ cùng dataset; timestamp event/bar start/update/receipt phân biệt.

### FOX2-08-R13 — watchlist thật
Single-user localhost preference scope, không private broker. GET /api/watchlist; PUT /api/watchlist thay toàn danh sách có expected_version/optimistic conflict409, max100 verified instruments. UI gửi mutation chỉ sau người dùng add/remove; atomic persistence, restart giữ list, không fetch provider để pretend holdings. Browser Origin/Host và loopback guard + content-type JSON cho mutation; không phát triển multiuser login trong M1.
Không có mutation preference trong giai đoạn chưa được grant task. Public market operations còn lại GET/read-only. Preference PUT không có broker write semantics.

### FOX2-08-R14 — giao diện review được
Responsive desktop 1440/1024 và mobile390; menu/table không gây page overflow; native chart có label unit unknown; status badges text cùng màu. Mỗi widget có as_of/source/state/coverage và link evidence/audit sanitized. Không đòi đủ 4 ảnh reference mới được nghiệm thu chức năng. Renderer/library/version/license chốt ở implementation lockfile; UI không tự tính scoring, risk hoặc net money flow.

### FOX2-08-R15 — refresh và backend boundary
Browser chỉ gọi FOX2 API; không DNSE secret/topic URLs, không DB đọc trực tiếp. M1 polling conditional GET/cache revision; default manual refresh, polling opt-in theo budget capability đã verify. REST history backfill do scheduler DSM, không mỗi browser poll lại gọi DNSE. No upstream network nếu provider enabled=false. Source unavailable không làm navigation treo.

### Acceptance bổ sung
FOX2-08-T10: watchlist add/remove/restart và concurrent version conflict409 đúng; invalid/unknown ID422.
FOX2-08-T11: per-widget states/native labels/no fake quote; không lẫn history close với trade.
FOX2-08-T12: 1440/1024/390 responsive, chart gaps/provisional, browser console không error.
FOX2-08-T13: investor bundle/API không leak Fox synthetic analysis, private facts, DNSE secrets/direct calls.
FOX2-08-T14: disabled upstream/manual UI refresh không network; no polling-triggered backfill storm.
