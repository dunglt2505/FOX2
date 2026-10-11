# FOX2-BRD-00 — Product Vision, Requirements & Common Rules

**Project:** FOX2 — Vietnam Equities Investment Intelligence  
**Version:** 0.2 · 2026-10-11 · **Content approval:** `OWNER_APPROVED_20261011` · **Publication:** `EFFECTIVITY_DETERMINED_BY_LIBRARY_RELEASE_RECEIPT`  
**Owner domain:** `FOX2-BRD-00` · **Accepted runtime:** `NONE`  
**Purpose:** Định nghĩa mục tiêu FOX2, quyền sở hữu yêu cầu, vòng đời quyết định, miền dữ liệu và giới hạn an toàn chung. Không tự chốt release, công thức hay quyền giao dịch.

**FOX2-only authority:** `FOX2_POLICY_V1.0.md` (published internal-document governance) và quyết định của Owner FOX2. Tài liệu này không nhận quy định, approval, quyền kỹ thuật hoặc release từ bất kỳ dự án nào khác; chỉ tham chiếu các yêu cầu, hợp đồng và BRD được xác lập trong FOX2.

## Owner approval and publication provenance

- **Decision:** On 2026-10-11, FOX2 Owner agreed to approve `FOX2-BRD-00 v0.2` on the four stated business points: FOX2 project independence, V1 Vietnam-equity decision support, fixture-labelled localhost from M1, and FOX2-internal ownership and dependencies across BRD-00..08.
- **Approved business source:** `FOX2-BRD-00_CANDIDATE_v0.2.md`, source ID `file_0000000073188211b77c418d08d19d4a`, SHA-256 `50bfeb83c53c31855ee3a11688d93740c7ab080304a63e5ccc49e9a9e833264b`, size 8,267 bytes.
- **Release edition:** This is the same business requirement and acceptance set, with administrative status/approval text adapted for issuance. The release-edition bytes and Library publication readback are identified separately in `FOX2-BRD-00_v0.2_RELEASE_RECEIPT_20261011.json`. No other BRD, Git/DEV or brokerage permissions are approved by this decision.
- **Unresolved business parameters:** Numerical return targets, risk budgets, capital limits and licensed market-data entitlement remain governed by the appropriate FOX2 BRDs and separate Owner decisions.

## Scope and user outcomes
- Toàn bộ thị trường cổ phiếu Việt Nam theo phạm vi nguồn được cấp phép; không hardcode ACB
- Một stock master với source, thời điểm khả dụng, lịch sử symbol/venue/classification
- MVP localhost hoạt động kể từ lần triển khai đầu tiên, có dữ liệu SYNTHETIC minh bạch
- Chia vai trò BRD-00..08; mỗi yêu cầu chỉ có một BRD owner; research không trở thành runtime qua copy-paste
- V1 phân tích/khuyến nghị/shadow, không gửi lệnh/margin/cash-transfer

## Product vision / V1 operating scope

- **Mục đích kinh doanh:** cung cấp phân tích cổ phiếu Việt Nam có thể giải thích, ưu tiên dữ liệu giá, khối lượng, giá trị giao dịch và các dấu hiệu dòng tiền có bằng chứng; thể hiện bối cảnh thị trường → ngành → cổ phiếu.
- **Giá trị cho nhà đầu tư:** giúp theo dõi, phát hiện cơ hội, đánh giá rủi ro, kế hoạch vốn và bảo vệ lợi nhuận; có quyền kết luận `HOLD_CASH / NO_OPPORTUNITY`.
- **Mốc M1:** giao diện localhost chạy trên fixture `SYNTHETIC` được đánh dấu rõ; M2 được thiết kế để có dữ liệu read-only khi nguồn cấp phép thực sự đáp ứng.
- **Phạm vi V1:** nghiên cứu, hiển thị và hỗ trợ quyết định; không gửi lệnh/margin/chuyển tiền; không mặc định có kết nối tài khoản chứng khoán.
- **Chưa quyết định:** mục tiêu tỷ suất sinh lời, ngân sách rủi ro và ngưỡng giao dịch phải được Owner chốt trong BRD phù hợp; không tự đặt số liệu an toàn giả.

## FOX2-only boundary & cross-BRD contract

- **Chủ quyền:** `00` là owner của các requirement `FOX2-00-Rxx`; quyết định nội bộ thuộc Owner FOX2 theo Policy FOX2 V1.0. Không sử dụng tài liệu/quyền/trạng thái từ dự án khác làm gate.
- **Luồng dữ liệu/đầu vào:** Quyền sở hữu yêu cầu, mã định danh, trạng thái quyết định, giới hạn V1 và nguyên tắc dữ liệu chung.
- **Luồng dữ liệu/đầu ra:** FOX2-BRD-01..08 thực hiện chức năng chuyên môn theo hợp đồng riêng. BRD-00 không thay thế công thức, thuật toán hay bằng chứng nghiệm thu của các BRD đó.
- **Ranh giới trách nhiệm:** Tất cả các BRD 01..08 là consumers của chuẩn ID, source envelope và trạng thái. Dữ liệu/nghiệp vụ vẫn do BRD owner chuyên trách quản lý.
- **Quy tắc hợp đồng:** mọi consumer dùng đúng `requirement_id`, source version, assessment/as-of và quality; thay đổi logic thuộc BRD owner phải qua quyết định FOX2 có phạm vi, không tạo bản master song song.

## Functional requirements

| Requirement | Normative FOX2 candidate requirement | Primary output | Priority | State |
|---|---|---|---|---|
| `FOX2-00-R01` | Mỗi yêu cầu mang mã FOX2-xx-Ryy, duy nhất một owner BRD, evidence nguồn, ưu tiên, trạng thái và acceptance ID. | `RequirementRegister` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R02` | Lưu status tách biệt PROPOSED, SPECIFIED, IMPLEMENTED, VERIFIED, ACCEPTED; giả thuyết có ACCEPT/REJECT/DEFER riêng. | `DecisionRegister` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R03` | Không biểu diễn confidence giả là xác suất, không tạo mặc định zero/safe/flat cho dữ liệu thiếu. | `CommonStatus` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R04` | Tất cả đề xuất có source, issued_at, data-as-of, availability cutoff, version và reason/counterevidence. | `EvidenceEnvelope` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R05` | Công bố rõ V1 NO_ORDER_WRITE, NO_MARGIN; nhà đầu tư có thể nhận HOLD_CASH/NO_OPPORTUNITY. | `CapabilityBoundary` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R06` | Tách quyền user/account, data scope và trạng thái shadow khỏi tình trạng thực broker. | `IdentityBoundary` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R07` | BRD-06 là data truth, BRD-05 là evidence, BRD-02 Entry, BRD-03 RiskVeto, BRD-01 Capital, BRD-04 Exit, BRD-07 Validation, BRD-08 Presentation. | `BRDOwnership` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R08` | FOX2 có nguồn thẩm quyền duy nhất là Policy FOX2 V1.0 và quyết định Owner FOX2 trong phạm vi được phép; mọi BRD/acceptance/work package chỉ tham chiếu quản trị nội bộ FOX2. | `ProjectIndependenceBoundary` | P0 | `SPECIFIED_CANDIDATE` |
| `FOX2-00-R09` | Duy trì sơ đồ 00..08 cho data owner, producer/consumer, requirement IDs; giữ liên kết nghiệp vụ nội bộ, không đồng nhất phụ thuộc dữ liệu với quyền phê duyệt tài liệu. | `InternalDependencyRegistry` | P0 | `SPECIFIED_CANDIDATE` |

## Acceptance and negative tests

| Test | Verification scenario | Expected |
|---|---|---|
| `FOX2-00-T01` | Không trùng owner BRD; provenance đầy đủ | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T02` | Thiếu dữ liệu phải UNKNOWN/UNAVAILABLE, không hiện zero | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T03` | Không tồn tại endpoint đặt lệnh hay switch margin trong MVP | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-00-T90` | Quét BRD/phụ thuộc: không có tên file, đường dẫn, Policy, approval, release gate hoặc authority từ dự án khác; các liên kết `FOX2-BRD-xx` hợp lệ phải được giữ | PASS chỉ khi tất cả tham chiếu quản trị là FOX2-only và các dependency nội bộ còn nguyên; trường hợp vi phạm phải FAIL, không tự publish |
| `FOX2-00-T91` | Mã requirement/test cũ được bảo toàn; quyền DEV/Git/LIVE hoặc bằng chứng nghiệm thu không được cấp từ việc sửa câu chữ | PASS cho tính toàn vẹn tài liệu nếu các ID v0.1 còn đủ; hiệu lực tài liệu theo Library release receipt; kiểm thử runtime chưa chạy = NOT_RUN |

## Out of scope / open gates

- Policy FOX2 V1.0 đã được publish cho quản trị tài liệu nội bộ; phê duyệt BRD và các quyền thao tác DEV/Git/LIVE vẫn phải có bằng chứng riêng theo Policy FOX2.
- Các quyền dữ liệu bên thứ ba và nhiều ngưỡng/model chưa nghiệm thu
- No release, broker-write, margin or trading automation is granted by this BRD.

## Handoff & traceability

- Producer/consumer boundaries follow `FOX2-BRD-00`; BRD-06 owns data facts and BRD-07 owns empirical acceptance.
- Lịch sử sửa đổi: đối chiếu `FOX2_BRD_V02_CHANGE_MANIFEST_20261011.json` (nguồn là bản FOX2 v0.1); các phiên bản trước chỉ là lịch sử, không làm nguồn quản trị.
- Chỉ số nội bộ: `FOX2_BRD_INDEX_v0.2.md`. Các BRD phụ thuộc được định danh bằng `FOX2-BRD-xx`; không có liên kết quản trị ngoài FOX2.
- On implementation, link each requirement to test IDs, code change, verification status, and separately authorized promotion evidence.

**Disposition v0.2:** nội dung business v0.2 đã được Owner chấp thuận; tình trạng xuất bản được xác minh bằng Library release receipt riêng, không tự suy ra từ câu chữ. Không cấp quyền thực thi kỹ thuật, Git, broker hay LIVE.
