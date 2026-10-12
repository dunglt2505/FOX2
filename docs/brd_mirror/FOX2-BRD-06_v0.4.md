# FOX2-BRD-06 — Data Foundation & FOX2 Data Source Manager (DSM)
> **FOX2 release edition · v0.4 · 2026-10-11 · OWNER_APPROVED / LIBRARY_PUBLISHED (subject to verified publication receipt).** This document derives from exact immutable M1 v0.4 ZIP source SHA-256 `1b9fcbc3ad9c79b1c9451b97223862d9de931501309d3543f24fb8dac4125895` (source manifest `0f3ad8f0231e5caef5e054a9ee6486471790b72f21aed1888eb0e10248f8845b`). Original BRD-06 candidate SHA-256 `371bdf675584f45b0e51de0f58a9d0fefb6ad50f4088a4493ba1074001734a0c` is retained unchanged inside that ZIP. All normative functional requirements and technical guards are preserved; editorial status changes only. This document alone does not grant DEV, Git, DNSE access, merge, push, broker access or LIVE. Status of automated tests: `NOT_RUN`. See the FOX2 M1 v0.4 publication receipt for actual Library file identity/readback.


**Project:** FOX2 — Vietnam Equities Investment Intelligence  
**Version:** 0.4 · 2026-10-11 · **Status:** `OWNER_APPROVED / LIBRARY_PUBLISHED` · first published version for this BRD; earlier v0.2/v0.3 were Candidates  
**Owner domain:** `FOX2-BRD-06` · **Accepted runtime:** `NONE`  
**Purpose:** Một cổng dữ liệu chuẩn hóa duy nhất cho FOX2: StockMaster, calendar, dữ liệu DNSE được cấp phép, lựa chọn đường lấy dữ liệu realtime/lịch sử/local, trạng thái chất lượng và luồng cung cấp cho các BRD nội bộ. **Module chính thức đề xuất:** `FOX2 Data Source Manager (DSM)`.

**FOX2-only authority:** `FOX2_POLICY_V1.0.md` (published internal-document governance) và quyết định của Owner FOX2. Tài liệu này không nhận quy định, approval, quyền kỹ thuật hoặc release từ bất kỳ dự án nào khác; chỉ tham chiếu các yêu cầu, hợp đồng và BRD được xác lập trong FOX2.

## Scope and user outcomes
- **M1 ưu tiên dữ liệu thị trường DNSE Production thực** qua FOX2 DSM nếu endpoint, credentials, entitlement, source schema, hợp đồng và host đã được chứng minh. Cấu hình Production **không phải** bằng chứng đã kết nối thành công; tài khoản kết nối dữ liệu không đồng nghĩa quyền gửi lệnh.
- DNSE WebSocket (quan sát realtime), API lịch sử và bản sao market-data lưu tại local chỉ là **các đường lấy dữ liệu** của cùng provider; DSM xác định nguồn theo mục đích sử dụng, chất lượng, độ mới, quyền và phiên. Fixtures `SYNTHETIC` chỉ dùng trong môi trường test cô lập, không tự fallback vào UI đầu tư.
- Hợp đồng dữ liệu point-in-time và source/availability timestamps
- Calendar HOSE/HNX/UPCoM, phiên ATO/ATC tách expected/final, T+2
- Read-only holdings/cash có thể bổ sung sau; Broker order lifecycle là future reference, không implement broker-write V1

## FOX2-only boundary & cross-BRD contract

- **Chủ quyền:** `06` là owner của các requirement `FOX2-06-Rxx`; quyết định nội bộ thuộc Owner FOX2 theo Policy FOX2 V1.0. Không sử dụng tài liệu/quyền/trạng thái từ dự án khác làm gate.
- **Luồng dữ liệu/đầu vào:** Chuẩn chung: FOX2-BRD-00 (định danh và trạng thái); dữ liệu đầu vào bên ngoài qua hợp đồng có quyền truy cập hợp lệ.
- **Luồng dữ liệu/đầu ra:** `FOX2 DSM` là nguồn cấp read-only thống nhất cho StockMaster, market/account snapshots (phân quyền riêng), source-selection audit, source/quality envelopes và typed HTTP/SSE/WebSocket consumer API cho FOX2-BRD-01/02/03/04/05/07/08. Website BRD-08 **không kết nối trực tiếp DNSE** và không tự chọn từ local/socket.
- **Ranh giới trách nhiệm:** BRD-06 là owner của fact/source-truth, không tự tạo BUY/SELL hoặc chấp thuận chiến lược.
- **Quy tắc hợp đồng:** mọi consumer dùng đúng `requirement_id`, source version, assessment/as-of và quality; thay đổi logic thuộc BRD owner phải qua quyết định FOX2 có phạm vi, không tạo bản master song song.

## Functional requirements

| Requirement | Normative FOX2 M1 v0.4 requirement | Primary output | Priority | State |
|---|---|---|---|---|
| `FOX2-06-R01` | Market datum phải có source_id, exchange_ts, received_at, as_of, session, quality, provisional/final, price unit/basis. | `MarketDataEnvelope` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R02` | Dùng LIVE/PERIODIC_LIVE/LATEST_VALID/EOD_CONFIRMED/STALE/GAP_RECOVERING/DELAYED/ENTITLEMENT_BLOCKED/UNAVAILABLE đúng thực chất. | `FeedStatus` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R03` | Không hardcode universal session; calendar version theo venue + holiday/special; không tạo bar giả tại midday/no-trade. | `TradingCalendar` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R04` | Xử lý duplicate, out-of-order, reconnect/backfill, source correction có revision và gap marker. | `FeedPipeline` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R05` | Phân biệt account-as-of với quote-as-of; private scope không được dùng chung public market cache. | `BrokerSnapshotBoundary` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R06` | Bí mật đăng nhập và API key chỉ lưu an toàn ở backend FOX2; không đưa vào mã nguồn, kho Git riêng của FOX2 hoặc log; thiếu quyền dữ liệu thì không scrape hoặc giả mạo nguồn live. | `SourceEntitlement` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R07` | Không có route POST /orders, cancel, amend, cash movement hoặc margin trong V0.1. | `NoBrokerWrites` | P0 | `SPECIFIED_APPROVED` |

## FOX2 Data Source Manager — operating model (`FOX2-DSM`)

**Tên chức năng được Owner yêu cầu:** `FOX2 Data Source Manager`, viết tắt **DSM**. Đây là **module thuộc BRD-06**, không phải một BRD mới và không tạo master dữ liệu song song. `DNSE` là tên provider; `Production` là cấu hình tài khoản/môi trường được Owner mô tả, **chưa được chứng minh live-ready** trong CHAT.

### Luồng kiến trúc và trách nhiệm

1. **Provider Connector:** lớp kết nối DNSE read-only, tách `Market WebSocket Consumer`, `Historical API Client`, `Entitlement/Auth`; endpoint/topic/auth, quota, lịch sử, giấy phép và credential được xác minh từ tài liệu DNSE thực tế **trước runtime**, không đoán URI hoặc cấu trúc payload.
2. **Ingestion & Normalization:** kiểm tra schema, mã CK/sàn, đơn vị, timezone, exchange/event timestamp, received time, correction/revision, duplicate, out-of-order, corporate action và provisional/final.
3. **Local Market Data Store:** lưu có version/provenance và backfill theo quyền dữ liệu; dữ liệu local giữ nguyên `origin_provider=DNSE`, thời điểm sự kiện và độ mới gốc; **không tự đổi thành LIVE** vì vừa đọc file/database.
4. **Source Selection & Health:** chọn đường lấy dữ liệu cho từng loại yêu cầu, instrument và period; bảo đảm entitlement, session calendar, freshness budget đã cấu hình bằng evidence, completeness, gap status và replay/correction; không tùy tiện nối chuỗi nguồn có basis khác nhau.
5. **Unified Read-only Data API:** expose market overview/stock quote/bars/source-health cho các BRD; mỗi phản hồi có `source_id`, provider, transport/acquisition, `as_of`, `received_at`, `first_available_at`, `freshness_state`, `quality`, `selection_reason`, completeness, correction revision và quyền redisplay; không lộ secrets.
6. **Operational controls:** reconnect/backoff/rate-limit, gap detection/backfill, audit ledger, data retention theo provider entitlement, source-health diagnostics; lỗi/cắt quyền/không đủ data → `STALE`/`ENTITLEMENT_BLOCKED`/`UNAVAILABLE`, không bù dữ liệu giả.

### Chính sách chọn nguồn (đề xuất cần thông số provider thực tế)

| Nhu cầu caller | Ưu tiên đủ điều kiện | Không đạt điều kiện |
|---|---|---|
| Intraday/live quote | WebSocket có entitlement, kết nối, event hợp lệ, freshness được nghiệm thu; fallback sang **latest verified snapshot/local** chỉ khi giữ đúng `as_of`, trạng thái và bản chất delayed/stale | Không tự hiển thị `LIVE`; trả `STALE`, `DELAYED`, `LATEST_VALID` hoặc `UNAVAILABLE` chính xác |
| OHLCV lịch sử | Local validated đầy đủ + đúng basis/revision/time cutoff; thiếu đoạn hoặc có corporate-action revision thì historical API/backfill được phép, kiểm soát rate-limit | Giữ gap marker và partial status; không fill bar/volume bằng zero |
| EOD/ATC | Ưu tiên dữ liệu confirmed của phiên, phân biệt expected provisional vs final, lịch HOSE/HNX/UPCoM và nghỉ trưa/ngày lễ | Chưa confirmed thì giữ `provisional=true` hoặc không có giá final |
| Replay/PIT/backtest | Snapshot/revision `first_available_at` không vượt decision cutoff, có lineage và point-in-time rights | `UNAVAILABLE` nếu không tái dựng được dữ liệu hợp lệ tại thời điểm |
| Local-only/offline & mất kết nối | Đọc market data DNSE đã lưu, nếu quyền retained use còn hợp lệ; hiển thị last `as_of` + stale/confirmed thực tế | Không chuyển fixture test thành dữ liệu thật |

**Source selection phải có audit trace:** request/caller/contract revision, selected retrieval channel, rejected options/reasons, event-vs-availability time, source revision, gap/entitlement/freshness verdict; không lưu token hoặc thông tin tài khoản riêng trong log market data.

### Ranh giới Production và an toàn

- Đọc dữ liệu từ tài khoản DNSE Production **chỉ trong phạm vi quyền thực tế được cấp**; xác thực/refresh backend-only, secret store, least privilege, không nhập secret vào BRD, Git, frontend, prompt hoặc log.
- Phân biệt quyền `PUBLIC_MARKET_READ`, `PRIVATE_ACCOUNT_READ` (nếu được cấp sau), và `BROKER_WRITE` (**không hỗ trợ V1**). Không đưa dữ liệu private vào cache chung hay public endpoints.
- Bản thân vận hành Windows/local, khả năng socket và sự tồn tại tài khoản Production là **Owner-reported / HOST_NOT_VERIFIED**; require connection smoke, entitlement tests, sample schema, quotas, terms of storage/redistribution trước khi xác nhận M1 real-data readiness.
- Market data là read-only; không tạo `POST /orders`, cancel/amend, margin, live trading. Website không bao giờ đưa khuyến nghị giả khi không có evidence.

### Thay đổi yêu cầu bổ sung v0.3

| Requirement | Normative FOX2 M1 v0.4 requirement | Output | Priority | State |
|---|---|---|---|---|
| `FOX2-06-R08` | DSM làm owner duy nhất của source-selection; consumers dùng API chung, không tự kết nối WebSocket DNSE. | `DataSourceManager` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R09` | DNSE Production WebSocket/API/local store phải đi qua entitlement, origin provenance, schema và read-only isolation. | `DNSEProviderAdapter` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R10` | Chọn nguồn theo demand (live/history/EOD/PIT/offline), freshness/calendar/revision/availability; trả audit decision. | `SourceSelectionDecision` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R11` | Có local storage phục vụ historical/backfill/reconnect, giữ provenance và không giả đổi timestamp/freshness. | `VersionedLocalMarketStore` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R12` | WebSocket disconnect/gap/out-of-order/reconnect/backfill điều khiển recovery, không che lag bằng fixture. | `FeedRecoveryStatus` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R13` | Production auth/credentials/quota/license/storage/redistribution/tenant-scope phải kiểm chứng và bảo vệ; UNKNOWN chặn đúng nhánh. | `ProviderReadinessGate` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R14` | API thống nhất expose typed provenance, retrieval channel, provider origin, source revision, freshness, quality, as_of và health. | `UnifiedMarketDataAPI` | P0 | `SPECIFIED_APPROVED` |
| `FOX2-06-R15` | Fixture chỉ dùng automated test riêng; không fallback sang fake market values trong investor UI. | `ProductionDataIntegrity` | P0 | `SPECIFIED_APPROVED` |

## Acceptance and negative tests

| Test | Verification scenario | Expected |
|---|---|---|
| `FOX2-06-T01` | ATC expected provisional không bị render như executed final | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-06-T02` | Disconnect chuyển STALE và hiển thị timestamp | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-06-T03` | No-trade symbol không bị coi outage | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-06-T04` | Missing amount không biến thành 0 | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-06-T05` | Không có broker-write API endpoints | Evidence-backed PASS or explicit FAIL/UNAVAILABLE; no implicit LIVE |
| `FOX2-06-T90` | Quét BRD/phụ thuộc: không dùng Policy, approval, release gate hoặc authority từ dự án khác làm governance FOX2; technical reference được gắn nhãn và pinned; các liên kết `FOX2-BRD-xx` hợp lệ phải được giữ | PASS chỉ khi tất cả tham chiếu quản trị là FOX2-only và các dependency nội bộ còn nguyên; trường hợp vi phạm phải FAIL, không tự publish |
| `FOX2-06-T91` | Mã requirement/test cũ được bảo toàn; quyền DEV/Git/LIVE hoặc bằng chứng nghiệm thu không được cấp từ việc sửa câu chữ | PASS khi các ID v0.1 còn đủ và hiệu lực chỉ là `CANDIDATE_FOR_OWNER_REVIEW`; chưa chạy thực tế = NOT_RUN |

### Acceptance additions v0.3 — `SPECIFIED_NOT_EXECUTED`

| Test | Verification scenario | Expected |
|---|---|---|
| `FOX2-06-T06` | LIVE WS fresh với quyền hợp lệ → source selection | `LIVE` có event/as_of/provider/revision, đúng instrument/session |
| `FOX2-06-T07` | WS mất kết nối, có local snapshot cũ | Chỉ trả `STALE/LATEST_VALID` kèm timestamp; không giả LIVE và không dùng SYNTHETIC |
| `FOX2-06-T08` | Historical local có gap/revision sai | Backfill API nếu được phép hoặc `PARTIAL/UNAVAILABLE`, không bịa bar |
| `FOX2-06-T09` | Entitlement deny/expired, Production credentials thiếu | `ENTITLEMENT_BLOCKED`, không query/scrape hoặc bypass |
| `FOX2-06-T10` | Event out-of-order, duplicate, correction, changed price basis | Idempotency + lineage/revision chính xác, UI không tráo dữ liệu |
| `FOX2-06-T11` | Replay có first_available_at sau simulated cutoff | Không leak tương lai vào PIT/research |
| `FOX2-06-T12` | Local stored DNSE đọc lại sau 1 ngày | Origin DNSE giữ nguyên, không restamp as_of/first_available_at thành now |
| `FOX2-06-T13` | Public UI gọi nguồn private account | Không tiết lộ account/holdings/token, log được redacted |
| `FOX2-06-T14` | Production feed bị chặn, test fixtures tồn tại | UI investor `UNAVAILABLE/STALE`; không auto fallback SYNTHETIC |
| `FOX2-06-T15` | Tra source-selection diagnostics | Có chọn/bỏ nguồn và lý do đủ tái hiện; không ghi secrets |

## Out of scope / open gates

- DNSE WS protocol/SDK và Fox REST implementation đã được source-inspected; current FOX2 host access, entitlement, unit mappings, accepted freshness budgets và storage/redisplay rights vẫn cần evidence. Không đồng nhất historical HTTP success với current readiness.
- No release, broker-write, margin or trading automation is granted by this BRD.

## Handoff & traceability

- Producer/consumer boundaries follow `FOX2-BRD-00`; BRD-06 owns data facts and BRD-07 owns empirical acceptance.
- Lịch sử sửa đổi: đối chiếu `FOX2_BRD_V02_CHANGE_MANIFEST_20261011.json` (nguồn là bản FOX2 v0.1); các phiên bản trước chỉ là lịch sử, không làm nguồn quản trị.
- Chỉ số nội bộ: `FOX2_BRD_INDEX_v0.2.md`. Các BRD phụ thuộc được định danh bằng `FOX2-BRD-xx`; không có liên kết quản trị ngoài FOX2.
- On implementation, link each requirement to test IDs, code change, verification status, and separately authorized promotion evidence.

**Change intent v0.3:** Owner yêu cầu DNSE Production và quản lý nguồn động; thiết kế `FOX2 Data Source Manager` tích hợp dữ liệu WebSocket, API lịch sử, bản lưu local, nguồn/quality cho BRD-08, thay mặc định fixture M1. Giữ toàn bộ IDs v0.2; chưa publish, chưa chạy test, chưa cấp quyền DEV/Git/LIVE.

## Revision v0.4 — phạm vi chốt M1

Change ID: FOX2-BCC-M1-DSM-20261011-v04. Tài liệu này là bản đầy đủ kế tiếp của cùng BRD, không tạo BRD master song song. Phạm vi trình duyệt: M1-A và M1-B trong bộ manifest; BRD-01/02/03/04/05/07 chưa được duyệt thuật toán qua gói này. Các yêu cầu ngoài M1 được giữ để truy vết, không kéo vào DEV M1.

Nguồn tham khảo kỹ thuật: Fox commit 740051933ec4fbf29180d0f5fb698c34e8c91ece và DNSE SDK aa55a5117de2534707bca6165b6738e1cc6fc6a4; N1 v1.1-candidate. Source Fox/SDK là evidence kỹ thuật, không mang governance hoặc quyền DEV của dự án đó sang FOX2. Policy duy nhất: FOX2_POLICY_V1.0.md. Accepted runtime vẫn NONE.

Approval gói v0.4 phải bind đúng MANIFEST.json, ba BRD, contract và acceptance; đề nghị grant M1-A trước. M1-B chỉ được kết nối khi gate capability/rights/secret/host đạt. Approval không phải bằng chứng code, test, merge hay LIVE đã hoàn tất.


### FOX2-06-R16 — reuse boundary
Kế thừa thiết kế ReadOnlyClient, normalize_ohlc, atomic cache và metadata của Fox sau scoped extraction. Public adapter chỉ cho phép market endpoints; không copy account methods, CLI accounts(), app bootstrap, synthetic analyze() hoặc toàn dashboard. fox/app.py hiện khởi tạo synthetic snapshot kể cả khi Production selector bật: đây là giới hạn reuse đã kiểm chứng, không được mang sang investor runtime.
Lịch sử Oct 5/7 có HTTP Production 7 series: VNINDEX/VN30/ACB/HPG/FPT/SSI/MWG. Không probe lại toàn tài khoản để chứng minh dữ liệu thị trường. N2 kiểm tra WIP/branch Windows trước khi kết luận WS chưa được dev ở mọi nơi.

### FOX2-06-R17 — immutable observation và store
Mỗi request/message sinh observation riêng, không dùng client.last_metadata dùng chung trong concurrent path. SQLite là lựa chọn DEV: một ingest writer, transaction gồm observation/revision/current pointer/audit; schema migration có version. Payload market chỉ lưu khi retention được phép, hash raw before normalize. Nếu không được lưu raw thì ghi hash và reason, không tuyên bố raw replay available.
Định danh revision gồm source/provider/instrument/venue/board/timeframe/start/basis. Data correction append revision; first_available_at mới là lúc hệ thống thực sự quan sát correction, không backdate. Polling read không tăng revision. Restart giữ timestamp, đánh giá lại rights/freshness. Không sử dụng cache D:/Data/Fox làm store ghi của FOX2.

### FOX2-06-R18 — market-only WebSocket
Provider guide: https://developers.dnse.com.vn/docs/guide/market-data/connect/. Base Production wss://ws-openapi.dnse.com.vn. SDK pinned dùng /v1/stream?encoding=json|msgpack, welcome → action=auth → auth_success → subscribe channels[{name,symbols}] → subscription confirmation. WS HMAC hex trên api_key:timestamp:nonce khác REST Date/Base64 signing; không dùng lẫn.
Ban đầu explicit G1, một equity, resolution 1D để nối history; intraday 1/5/15 là extension có coverage/test riêng. Không mặc định mọi board/resolution. Channels tick.G1.json, security_definition.G1.json, ohlc.1D.json, ohlc_closed.1D.json, market_index.VNINDEX.json / VN30; session channel chỉ sau exact mapping. Order book top_price là tùy chọn, không đồng nhất bid/offer với last trade.
Connection <=8h; server PING mỗi 3 phút, PONG deadline 1 phút; 10 connections/user, 200 streams/connection là caps của provider. Transport control ping/pong và application action ping/pong được xử lý riêng. Guide có ví dụ PING/PONG không nhất quán: verify application behavior theo SDK + observed handshake trước nghiệm thu. Không dùng số này làm stale threshold của giá.
Auth, desired subscription, confirmed subscription, socket health và data freshness là các state riêng. SDK send-success không chứng minh subscribe thành công. Normal close 8h phải recover; không chỉ bắt lỗi abnormal. Queue hữu hạn; reject/mark gap khi overflow; ping không chờ callback thị trường chậm; bảo đảm ordering tới store, không chỉ tới callback dispatch.
SDK/examples là reference: không copy secret-like literals, UAT config, private subscription hoặc raw logs. Market wrapper allowlist capability; startup không tạo broker/OTP/order path.

### FOX2-06-R19 — data mappings
Trade time Seconds/Nanos: lưu raw precision, validate Nanos 0..999999999, không float làm ID; UTC event_at. matchQtty là per-trade; totalVolumeTraded là cumulative, không cộng lặp. OHLC time là start, lastUpdated là update; provisional stream thay phiên bản cùng open bar; ohlc_closed provider-final không đồng nghĩa adjusted hoặc exchange EOD.
HTTP daily t có legacy epoch codec; cần accepted field semantics/units/basis before VERIFIED_PROVIDER. Native unknown không được nhân 1000 theo ví dụ. Volume/turnover/breadth chỉ đúng khi field/unit mapping có evidence. Expected ATO/ATC vẫn provisional, không xem như thực khớp.
Gap recovery không hứa phục hồi ticks nếu historical API chỉ hỗ trợ bars. Bars có thể recover completeness theo timeframe; quote cần snapshot/new event đúng capability. Không tuyên bố restored tick continuity từ OHLC backfill.

### FOX2-06-R20 — capability-scoped gates
read, redisplay, retained_use, network readiness, mapping/unit/time/calendar và freshness config có evidence/expiry riêng. UNKNOWN chặn đúng nhánh. TTL/budget thiếu thì LIVE bị chặn nhưng latest data có thể xem đúng label khi rights hợp lệ. Fixture isolation phải được kiểm thử M1-A trước khi network được bật. API shape là market-data-v0.4-candidate trong 03_Contracts; semantic invariants trong contract spec là bắt buộc, schema shape PASS chưa thay semantic PASS.

### Runtime state machine
DISABLED → CONNECTING → AUTHENTICATING → SUBSCRIBING → SYNCING → READY. READY đòi auth+required subscription ACK+mapping+rights+freshness/gap verdict. Mất socket → RECONNECTING; thiếu entitlement → BLOCKED; exhausted retry/schema corruption → DEGRADED. Reconnect success chưa phải data READY. Feed status theo từng capability, không gắn toàn dashboard LIVE từ socket status.

### Acceptance bổ sung
FOX2-06-T16: public transport deny account/order/private channels; no secret logging.
FOX2-06-T17: request-local metadata không bị cross-request overwrite; store commit/revision atomic.
FOX2-06-T18: schema unavailable timestamps null; semantic OHLC/time/rights guards; genuine zero volume giữ nguyên.
FOX2-06-T19: ACK rejection chặn readiness; reconnect normal8h re-auth/resubscribe, không worker trùng.
FOX2-06-T20: control heartbeat không bị slow consumers chặn; overflow/out-of-order ghi gap.
FOX2-06-T21: provisional/cumulative updates không double-count; final/correction giữ lineage.
FOX2-06-T22: bars backfill không giả khôi phục tick continuity; bounded pagination dừng/no-progress.
FOX2-06-T23: restart/expired rights không restamp hoặc dùng cache trái quyền.
FOX2-06-T24: field/unit mapping không suy từ numerical example; epoch/nanos giữ semantic đúng.
