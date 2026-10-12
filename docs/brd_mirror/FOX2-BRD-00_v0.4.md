# FOX2-BRD-00 — Product Vision, Requirements & Common Rules
> **FOX2 release edition · v0.4 · 2026-10-11 · OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified publication receipt).** This document derives from exact immutable M1 v0.4 ZIP source SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895` (source manifest `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`). Original BRD-00 candidate SHA-256 `31a448b7e17d81ff5b6e77ef31da6a0d25f09024331f8b1b5f28b9c354644849` is retained unchanged inside that ZIP. All normative functional requirements and technical guards are preserved; editorial status changes only. This document alone does not grant DEV, Git, DNSE access, merge, push, broker access or LIVE. Status of automated tests: `NOT_RUN`. See the FOX2 M1 v0.4 publication receipt for actual Library file identity/readback.


**Project:** FOX2 — Vietnam Equities Investment Intelligence  
**Version:** 0.4 · 2026-10-11 · **Status:** `OWNER_APPROVED / LIBRARY_PUBLISHED` · **Historical baseline:** `PUBLISHED v0.2`  
**Owner domain:** `FOX2-BRD-00` · **Accepted runtime:** `NONE`  
**Purpose:** Định nghĩa mục tiêu FOX2, quyền sở hữu yêu cầu, vòng đời quyết định, miền dữ liệu và giới hạn an toàn chung. Không tự chốt release, công thức hay quyền giao dịch.

**FOX2-only authority:** `FOX2_POLICY_V1.0.md` (published internal-document governance) và quyết định của Owner FOX2. Tài liệu này không nhận quy định, approval, quyền kỹ thuật hoặc release từ bất kỳ dự án nào khác; chỉ tham chiếu các yêu cầu, hợp đồng và BRD được xác lập trong FOX2.

## Baseline and revision governance

- **Previous published BRD (retained as superseded historical baseline):** `/Trading/FOX2/01_BRD/FOX2-BRD-00_v0.2.md`, Library source file `file_000000002844821188bceb05f5c87669`, raw SHA-256 `adf043885d4759b72cbd9fd161d8b5762af725495b5cbc59c5858df1f4cf4bf4`. Owner-approved v0.2 is not silently superseded.
- **Approved M1 design change:** Owner clarified M1 does **not** require synthetic fixture as production data, and DNSE Production + WebSocket + local store belong behind `FOX2 Data Source Manager` owned by BRD-06. This material revision has been adopted for the limited FOX2 M1 slice; actual document publication/effectivity is evidenced by its separate Library release receipt.
- **Unresolved:** Historical Fox Production HTTP and official WS protocol evidence exist; current FOX2 auth/access, mapping, entitlement, persistence rights, Windows host and source freshness must be verified before accepting runtime market data; no DEV or LIVE authority by document revision.

## Scope and user outcomes
- Toàn bộ thị trường cổ phiếu Việt Nam theo phạm vi nguồn được cấp phép; không hardcode ACB
- Một stock master với source, thời điểm khả dụng, lịch sử symbol/venue/classification
- MVP localhost hoạt động ngay ở M1; dữ liệu thị trường **DNSE thật** do FOX2 DSM (BRD-06) cung cấp khi đã xác minh quyền/kết nối/quality. Thiếu nguồn thật thì hiện UNAVAILABLE/STALE, không fallback fixture vào investor view.
- Chia vai trò BRD-00..08; mỗi yêu cầu chỉ có một BRD owner; research không trở thành runtime qua copy-paste
- V1 phân tích/khuyến nghị/shadow, không gửi lệnh/margin/cash-transfer

## Product vision / V1 operating scope

- **Mục đích kinh doanh:** cung cấp phân tích cổ phiếu Việt Nam có thể giải thích, ưu tiên dữ liệu giá, khối lượng, giá trị giao dịch và các dấu hiệu dòng tiền có bằng chứng; thể hiện bối cảnh thị trường → ngành → cổ phiếu.
- **Giá trị cho nhà đầu tư:** giúp theo dõi, phát hiện cơ hội, đánh giá rủi ro, kế hoạch vốn và bảo vệ lợi nhuận; có quyền kết luận `HOLD_CASH / NO_OPPORTUNITY`.
- **Mốc M1:** giao diện localhost dùng DSM read-only. DNSE WebSocket/API lịch sử và local versioned store có thể chạy trong M1 khi quyền/schema/host thực tế PASS; mất nguồn phải hiển thị đúng trạng thái. `SYNTHETIC` chỉ dùng ở automated test cô lập. **M2** mở rộng độ bao phủ, lịch sử, completeness, recovery và hardening dữ liệu; không bắt M1 dùng fake data trước.
- **Phạm vi V1:** nghiên cứu, hiển thị và hỗ trợ quyết định; không gửi lệnh/margin/chuyển tiền; không mặc định có kết nối tài khoản chứng khoán.
- **Chưa quyết định:** mục tiêu tỷ suất sinh lời, ngân sách rủi ro và ngưỡng giao dịch phải được Owner chốt trong BRD phù hợp; không tự đặt số liệu an toàn giả.

## FOX2-only boundary & cross-BRD contract

- **Chủ quyền:** `00` là owner của các requirement `FOX2-00-Rxx`; quyết định nội bộ thuộc Owner FOX2 theo Policy FOX2 V1.0. Không sử dụng tài liệu/quyền/trạng thái từ dự án khác làm gate.
- **Luồng dữ liệu/đầu vào:** Quyền sở hữu yêu cầu, mã định danh, trạng thái quyết định, giới hạn V1 và nguyên tắc dữ liệu chung.
- **Luồng dữ liệu/đầu ra:** FOX2-BRD-01..08 thực hiện chức năng chuyên môn theo hợp đồng riêng. BRD-00 không thay thế công thức, thuật toán hay bằng chứng nghiệm thu của các BRD đó.
- **Ranh giới trách nhiệm:** Tất cả các BRD 01..08 là consumers của chuẩn ID, source envelope và trạng thái. Dữ liệu/nghiệp vụ vẫn do BRD owner chuyên trách quản lý.
- **Quy tắc hợp đồng:** mọi consumer dùng đúng `requirement_id`, source version, assessment/as-of và quality; thay đổi logic thuộc BRD owner phải qua quyết định FOX2 có phạm vi, không tạo bản master song song.

## Functional requirements

| Requirement | Normative FOX2 M1 v0.4 requirement | Primary output | Priority | State |
|---|---|---|---|---|
| `FOX2-00-R01` | Mỗi yêu cầu mang mã FOX2-xx-Ryy, duy nhất một owner BRD, evidence nguồn, ưu tiên, trạng thái và acceptance ID. | `RequirementRegister` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R02` | Lưu status tách biệt PROPOSED, SPECIFIED, IMPLEMENTED, VERIFIED, ACCEPTED; giả thuyết có ACCEPT/REJECT/DEFER riêng. | `DecisionRegister` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R03` | Không biểu diễn confidence giả là xác suất, không tạo mặc định zero/safe/flat cho dữ liệu thiếu. | `CommonStatus` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R04` | Tất cả đề xuất có source, issued_at, data-as-of, availability cutoff, version và reason/counterevidence. | `EvidenceEnvelope` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R05` | Công bố rõ V1 NO_ORDER_WRITE, NO_MARGIN; nhà đầu tư có thể nhận HOLD_CASH/NO_OPPORTUNITY. | `CapabilityBoundary` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R06` | Tách quyền user/account, data scope và trạng thái shadow khỏi tình trạng thực broker. | `IdentityBoundary` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R07` | BRD-06 là data truth, BRD-05 là evidence, BRD-02 Entry, BRD-03 RiskVeto, BRD-01 Capital, BRD-04 Exit, BRD-07 Validation, BRD-08 Presentation. | `BRDOwnership` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R08` | FOX2 có nguồn thẩm quyền duy nhất là Policy FOX2 V1.0 và quyết định Owner FOX2 trong phạm vi được phép; mọi BRD/acceptance/work package chỉ tham chiếu quản trị nội bộ FOX2. | `ProjectIndependenceBoundary` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-00-R09` | Duy trì sơ đồ 00..08 cho data owner, producer/consumer, requirement IDs; giữ liên kết nghiệp vụ nội bộ, không đồng nhất phụ thuộc dữ liệu với quyền phê duyệt tài liệu. | `InternalDependencyRegistry` | P0 | `SPECIFIED_APPROVED` |

### Proposed new requirement for the material change

| Requirement | Normative FOX2 M1 v0.4 requirement | Output | Priority | State |
|---|---|---|---|---|
| `FOX2-00-R10` | M1 không mặc định sử dụng synthetic market data; BRD-06 DSM là owner duy nhất việc lựa chọn nguồn DNSE WebSocket/API/local. Website chỉ hiển thị dữ liệu thật đã verify hoặc trạng thái thiếu/stale, fixture tách test. | `M1DataSourceBoundary` | P0 | `SPECIFIED_APPROVED` |

## Acceptance and negative tests

| Test | Verification scenario | Expected |
|---|---|---|
| `FOX2-00-T01` | Không trùng owner BRD; provenance đầy đủ | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T02` | Thiếu dữ liệu phải UNKNOWN/UNAVAILABLE, không hiện zero | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T03` | Không tồn tại endpoint đặt lệnh hay switch margin trong MVP | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T90` | Quét BRD/phụ thuộc: không dùng Policy, approval, release gate hoặc authority từ dự án khác làm governance FOX2; technical reference được gắn nhãn và pinned; các liên kết `FOX2-BRD-xx` hợp lệ phải được giữ | PASS chỉ khi tất cả tham chiếu quản trị là FOX2-only và các dependency nội bộ còn nguyên; trường hợp vi phạm phải FAIL, không tự publish |
| `FOX2-00-T91` | Mã requirement/test cũ được bảo toàn; quyền DEV/Git/LIVE hoặc bằng chứng nghiệm thu không được cấp từ việc sửa câu chữ | PASS cho tính toàn vẹn tài liệu nếu các ID v0.1 còn đủ; hiệu lực tài liệu theo Library release receipt; kiểm thử runtime chưa chạy = NOT_RUN |

### Additional acceptance for BRD-00 v0.3 — `SPECIFIED_NOT_EXECUTED`

| Test | Scenario | Expected |
|---|---|---|
| `FOX2-00-T04` | Chạy M1 không có DNSE entitlement, fixtures có trong tests | UI hiện UNAVAILABLE/STALE, không giả giá và không quảng bá LIVE |

## Out of scope / open gates

- Policy FOX2 V1.0 đã được publish cho quản trị tài liệu nội bộ; phê duyệt BRD và các quyền thao tác DEV/Git/LIVE vẫn phải có bằng chứng riêng theo Policy FOX2.
- Các quyền dữ liệu bên thứ ba và nhiều ngưỡng/model chưa nghiệm thu
- No release, broker-write, margin or trading automation is granted by this BRD.

## Handoff & traceability

- Producer/consumer boundaries follow `FOX2-BRD-00`; BRD-06 owns data facts and BRD-07 owns empirical acceptance.
- Lịch sử sửa đổi: đối chiếu `FOX2_BRD_V02_CHANGE_MANIFEST_20261011.json` (nguồn là bản FOX2 v0.1); các phiên bản trước chỉ là lịch sử, không làm nguồn quản trị.
- Chỉ số nội bộ: `FOX2_BRD_INDEX_v0.2.md`. Các BRD phụ thuộc được định danh bằng `FOX2-BRD-xx`; không có liên kết quản trị ngoài FOX2.
- On implementation, link each requirement to test IDs, code change, verification status, and separately authorized promotion evidence.

**Disposition v0.3:** Đề xuất thay đổi material so với BRD-00 v0.2 đã publish. Chưa được phê duyệt exact revision, chưa publish; v0.2 vẫn effective. Không cấp quyền DEV, Git, broker hay LIVE.

## Revision v0.4 — phạm vi chốt M1

Change ID: FOX2-BCC-M1-DSM-20261011-v04. Tài liệu này là bản đầy đủ kế tiếp của cùng BRD, không tạo BRD master song song. Phạm vi trình duyệt: M1-A và M1-B trong bộ manifest; BRD-01/02/03/04/05/07 chưa được duyệt thuật toán qua gói này. Các yêu cầu ngoài M1 được giữ để truy vết, không kéo vào DEV M1.

Nguồn tham khảo kỹ thuật: Fox commit 740051933ec4fbf29180d0f5fb698c34e8c91ece và DNSE SDK aa55a5117de2534707bca6165b6738e1cc6fc6a4; N1 v1.1-candidate. Source Fox/SDK là evidence kỹ thuật, không mang governance hoặc quyền DEV của dự án đó sang FOX2. Policy duy nhất: FOX2_POLICY_V1.0.md. Accepted runtime vẫn NONE.

Approval gói v0.4 phải bind đúng MANIFEST.json, ba BRD, contract và acceptance; đề nghị grant M1-A trước. M1-B chỉ được kết nối khi gate capability/rights/secret/host đạt. Approval không phải bằng chứng code, test, merge hay LIVE đã hoàn tất.


### FOX2-00-R11 — nghiệm thu theo milestone
M1-A: localhost DSM/API/UI chạy được, trạng thái thiếu nguồn đúng, fixture chỉ ở isolated test. M1-B: một luồng dữ liệu thật qua ingest → store → API → chart/quote với provenance nhất quán; market realtime/recovery được kiểm chứng theo capability. Không gọi M1-A là real-data MVP. M1 được chốt ở M1-B; M2 mở rộng universe/depth/soak/PIT, M3 analytics, M4 portfolio/exit advisory.

Không yêu cầu chốt thuật toán M3/M4 để làm M1. Chỉ cần phê duyệt đúng slice BRD-00/06/08 + contract và acceptance M1. M0 toàn bộ chín BRD có thể còn mở trong khi M1 slice đã được chốt; roadmap phải ghi rõ thay đổi dependency này.

### M1 scope chính xác
- Market Overview: VNINDEX/VN30 ban đầu; HNX/UPCOM hiển thị nếu source được verify. Breadth/turnover do provider cung cấp được render có nhãn, không suy diễn thành FOX2 score/net inflow.
- Stock360: quote khi đủ nguồn; OHLCV lịch sử, volume, provisional/gap/basis/source. Một mã là vertical slice ban đầu, coverage mở rộng theo nguồn; không giới hạn sản phẩm vĩnh viễn vào bảy mã Fox.
- Search/watchlist: universe được xác minh, coverage công bố; watchlist là preference thật lưu local, không phải holdings hoặc broker state.
- Source diagnostics: capability REST/WS/store, subscription/gap/rights trạng thái rõ, đã redact.
- Sector/Discovery/Risk/Capital/Exit/Portfolio/Research: navigation + chưa khả dụng khi chưa có engine. Không dùng score, NAV, recommendation giả.

### Boundary dữ liệu native
Dữ liệu provider thật nhưng unit/basis chưa verify có mode PROVIDER_NATIVE_UNVERIFIED, chỉ được xem trong diagnostic native view khi read/redisplay hợp lệ. Trục ghi “đơn vị gốc chưa xác minh”; không đổi hệ số, không tính định giá/tín hiệu. Không tính phần này là normalized real-data acceptance. Nếu thiếu usage rights thì UNAVAILABLE, không dùng native view để bypass.

### Acceptance bổ sung
FOX2-00-T05: M1-A PASS không đóng M1-B hoặc tuyên bố LIVE.
FOX2-00-T06: chỉ chốt slice 00/06/08 không tự ACCEPT thuật toán 01..05/07.
FOX2-00-T07: native diagnostic không xuất hiện như normalized quote/analysis.
