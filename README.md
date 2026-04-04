# SecureHashAuth — Băm mật khẩu hiện đại trong hệ thống xác thực

Dự án theo hướng **nghiên cứu và triển khai** các giải thuật **Bcrypt**, **Scrypt** và **Argon2** trong ngữ cảnh xác thực người dùng.

---

## Chạy ứng dụng Web

```bash
cd /Users/kira/Desktop/workspace/SecureHashAuth
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Mở trình duyệt: [http://127.0.0.1:8000](http://127.0.0.1:8000). CSDL SQLite tạo tại `data/app.db`. Kiến trúc & lưu đồ: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

**Production:** đặt biến môi trường `SECRET_KEY` (chuỗi bí mật cố định) để cookie phiên không bị mất mỗi lần khởi động lại server.

### Kiểm thử

**Tự động (pytest):**

```bash
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/pytest tests/ -v
```

**Thủ công trên trình duyệt:** chạy `uvicorn` như trên → mở `/` → thử Đăng ký (chọn từng thuật toán), Đăng xuất, Đăng nhập sai/đúng, xem `/dashboard`.

**Thủ công bằng curl (giữ cookie phiên):**

```bash
# Trang chủ
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8000/

# Đăng ký (lưu cookie vào jar)
curl -c jar.txt -b jar.txt -X POST http://127.0.0.1:8000/register \
  -d "username=testuser&password=secret123&algorithm=bcrypt" -w "\n%{http_code}\n" -D -

# Dashboard (gửi lại cookie)
curl -b jar.txt -s http://127.0.0.1:8000/dashboard | head -c 200
```

---

## Mục tiêu

- Tìm hiểu các phương pháp **lưu trữ mật khẩu an toàn**.
- Phân tích nguyên lý hoạt động của **Bcrypt**, **Scrypt** và **Argon2**.
- So sánh **mức độ bảo mật** và **hiệu năng** giữa các thuật toán.
- Xây dựng hệ thống xác thực người dùng có áp dụng các thuật toán băm mật khẩu.
- Thực hiện **kiểm thử** và **đánh giá** khả năng chống tấn công.

---

## Yêu cầu

### Phân tích kỹ thuật

- Làm rõ sự khác biệt giữa:
  - **Bcrypt** — thiên về **tốn CPU** (CPU-intensive).
  - **Scrypt** — thiên về **tốn bộ nhớ** (memory-intensive).
  - **Argon2** — hàm **memory-hard** (khó song song hóa tấn công vét cạn trên phần cứng chuyên dụng).
- Thiết kế **mô hình thử nghiệm** để so sánh:
  - **Tốc độ băm** (hashing speed).
  - **Mức chiếm dụng tài nguyên** hệ thống (**CPU**, **RAM**).

### Kiểm thử độ “bền” mật khẩu đã băm

- Dựng **môi trường giả lập** dùng công cụ như **Hashcat** hoặc **John the Ripper** để thử phá (offline) và so sánh độ khó thực tế giữa các thuật toán / tham số cấu hình.

### Phát triển phần mềm

- Lập trình **ứng dụng Web hoặc API** bằng **Python**, tích hợp các thuật toán qua thư viện phù hợp (ví dụ: **passlib**, **argon2-cffi**).
- **Đánh giá** và đưa ra **khuyến nghị** lựa chọn thuật toán / tham số theo **tiêu chuẩn bảo mật** và thực tiễn triển khai hiện nay.

### Môi trường và công cụ

| Hạng mục | Gợi ý |
|----------|--------|
| Ngôn ngữ | Python (Passlib, Argon2, Bcrypt) |
| Giao diện | Web hoặc dòng lệnh (CLI) |
| Hệ điều hành | Windows, Linux |
| Ngữ cảnh tham chiếu | Apache, PHP, MySQL, CMS (ví dụ WordPress) |
| Lab / kiểm thử | Máy ảo (VirtualBox, VMware), **Hashcat**, **Docker** |
| Tùy chọn bổ sung | Máy có **GPU**, **Kali Linux**, **Wireshark** (phân tích lưu lượng nếu cần) |

### Nội dung báo cáo / sản phẩm (theo đề cương)

- Khảo sát **sự cố an toàn** liên quan mật khẩu và các biện pháp bảo vệ (**hash**, **salt**, **pepper**, …).
- Phân tích cấu trúc **Bcrypt**, **Scrypt**, **Argon2**.
- Thiết kế **lưu đồ** quy trình băm và kiểm tra mật khẩu; **kịch bản tấn công vét cạn** để so sánh.
- Triển khai đủ ba thuật toán, **CSDL lưu trữ an toàn**, kiểm thử **latency**, **throughput**, và kịch bản **Hashcat**.

---

## Lộ trình thực hiện (12 tuần)

| Tuần | Nội dung công việc |
|------|---------------------|
| **1** | Tìm hiểu lý thuyết về các phương pháp lưu trữ mật khẩu an toàn. |
| **2** | Nghiên cứu tài liệu về hàm băm mật khẩu và các công cụ hỗ trợ. |
| **3** | Phân tích chi tiết cơ chế nội tại của **Bcrypt**, **Scrypt** và **Argon2**. |
| **4** | Xây dựng môi trường Lab. |
| **5** | Thu thập dữ liệu mẫu; cài đặt công cụ bẻ khóa mật khẩu (chuẩn bị đối chứng). |
| **6** | Thiết kế kiến trúc module xác thực và lưu đồ xử lý băm mật khẩu. |
| **7** | Viết module tích hợp **ba** giải thuật băm. |
| **8** | Xây dựng cơ sở dữ liệu lưu trữ an toàn. |
| **9** | Thực hiện bài test **tốc độ (latency)** và **khả năng chịu tải (throughput)**. |
| **10** | Đánh giá qua các kịch bản tấn công **Hashcat**; so sánh độ khó của từng giải thuật. |
| **11** | Hoàn thiện báo cáo và slide trình bày. |
| **12** | Nộp báo cáo và bảo vệ đề tài. |

---

## Kế hoạch 7 tuần và phân công nhóm (3 thành viên)

Nhóm: **Đức**, **Đăng**, **Cường**. Mỗi tuần nên có **họp ngắn 1 buổi** (tiến độ, khó khăn) và **cập nhật Git / tài liệu** theo phần phụ trách.

### Vai trò nền (giữ xuyên suốt)

| Thành viên | Trọng tâm phụ trách | Ghi chú |
|------------|---------------------|---------|
| **Đức** | **Điều phối kỹ thuật**, luồng xác thực tổng thể, **Bcrypt**, API / tích hợp module | Ưu tiên kiến trúc, code review, thống nhất interface giữa các thuật toán. |
| **Đăng** | **Scrypt**, **cơ sở dữ liệu** (lược đồ bảng user, salt/hash), **đo hiệu năng** (latency, throughput, CPU/RAM) | Ưu tiên dữ liệu lưu trữ an toàn và bảng số so sánh. |
| **Cường** | **Argon2**, **lab tấn công** (Hashcat / John), môi trường thử (VM/Docker), **slide / minh họa kết quả** | Ưu tiên kịch bản offline crack và trình bày đánh giá. |

*Lưu ý:* Ba người **cùng chịu trách nhiệm** nộp báo cáo; tuần 7 mọi người **đọc lại toàn bộ** để đồng nhất thuật ngữ và số liệu.

### Lộ trình theo tuần

#### Tuần 1 — Lý thuyết & phạm vi

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Khảo sát nghiệp vụ, rủi ro mật khẩu (online/offline) | Chủ trì; khung chương 1–2 báo cáo | Hỗ trợ tìm case breach, tài liệu OWASP | Hỗ trợ tìm công cụ crack, video/hướng dẫn Hashcat |
| Phân vùng tài liệu: hash, salt, pepper, KDF | Viết nháp mục “mô hình đe dọa” | Nghiên cứu sâu **Bcrypt** (cost, giới hạn độ dài pass) | Nghiên cứu **Scrypt** + **Argon2** (memory-hard, tham số) |
| Đầu ra tuần | Checklist yêu cầu phần mềm + sơ đồ nghiệp vụ | 2–3 trang phân tích Bcrypt (có nguồn trích dẫn) | 2–3 trang so sánh Scrypt/Argon2 + bảng tham số gợi ý |

#### Tuần 2 — Thiết kế & môi trường

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Thiết kế kiến trúc (API, module chọn hash) | **Chủ trì** lưu đồ tổng; quy ước đặt tên, cấu trúc repo | Thiết kế **ERD / bảng users** (username, algo, salt, hash, params) | Dựng **VM hoặc Docker**; cài Hashcat (và/hoặc John); thử chạy mẫu |
| Môi trường Python | Review `requirements.txt`, nhánh Git chung | Cài passlib, chạy demo **Bcrypt** đầu tiên | Cài **Argon2-cffi**, demo hash/verify |
| Đầu ra tuần | Tài liệu thiết kế (PDF/Markdown trong repo) | Script tạo DB + insert mẫu | Ảnh chụp màn hình lab + log lệnh cài đặt |

#### Tuần 3 — Cài đặt lõi

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Luồng đăng ký / đăng nhập | **API** nhận `algorithm` hoặc cấu hình; **Bcrypt** tích hợp hoàn chỉnh | **Scrypt** (passlib); lưu đúng trường params | **Argon2** (argon2-cffi); đồng bộ format lưu CSDL |
| Kiểm tra | Unit test verify từng loại hash | Migration / seed dữ liệu test | Thử đăng ký 3 user với 3 thuật toán khác nhau |
| Đầu ra tuần | Postman/OpenAPI hoặc curl mẫu | Bảng DB thực tế có 3 loại bản ghi | Bảng “tham số đã dùng” (cost, memory, …) |

#### Tuần 4 — Hoàn thiện chức năng & giao diện

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Ghép module; xử lý lỗi; cấu hình | Code **chọn thuật toán** (env/config); rà soát không log mật khẩu | Rà soát **SQL injection**, quyền DB, backup | **Giao diện web đơn giản** hoặc CLI có menu (đăng ký/đăng nhập) |
| Bảo mật cơ bản | Rate limit / delay đăng nhập (tối thiểu) | Index, không lưu plaintext | Kiểm tra HTTPS nếu triển khai web |
| Đầu ra tuần | Bản demo chạy end-to-end trên máy nhóm | Checklist bảo mật CSDL (ghi trong báo cáo) | Video ngắn hoặc ảnh luồng UI |

#### Tuần 5 — Đo lường hiệu năng

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Benchmark | Định nghĩa kịch bản (số lần hash, độ dài pass) | **Chạy đo** latency & throughput; ghi **CPU/RAM** (vd. `ps`, Activity Monitor, `time`) | Chuẩn bị **bộ mật khẩu mẫu** (yếu/trung/bền) cho tuần 6 |
| Báo cáo số liệu | Đồng nhất định dạng bảng biểu | Xuất CSV/Excel; **biểu đồ** (matplotlib hoặc Sheets) | Viết nháp đoạn “nhận xét hiệu năng” |
| Đầu ra tuần | Bảng so sánh 3 thuật toán (cùng máy, cùng pass) | File số liệu gắn vào repo (folder `results/`) | Phụ lục tham số thử nghiệm |

#### Tuần 6 — Kiểm thử tấn công offline

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Hashcat / John | Export **chuỗi hash** mẫu (đúng format từng algo) — không dùng MK thật ngoài lab | Chạy wordlist cố định; **ghi thời gian** / số lần thử | **Chủ trì** kịch bản crack; so sánh độ “khó” giữa Bcrypt / Scrypt / Argon2 |
| Đánh giá | Nhận xét tại sao MK yếu vẫn bị bẻ | Liên hệ salt + cost | Viết mục “kết quả tấn công” + hạn chế thử nghiệm |
| Đầu ra tuần | Appendix lệnh Hashcat (ẩn dữ liệu nhạy cảm) | Bảng thời gian / trạng thái crack | Kết luận sơ bộ + khuyến nghị tham số |

#### Tuần 7 — Báo cáo, slide, duyệt cuối

| Công việc | Đức | Đăng | Cường |
|-----------|-----|------|-------|
| Báo cáo | **Tổng hợp** chương tổng quan + kiến trúc + Bcrypt; chỉnh luận văn thống nhất | Chương **CSDL + Scrypt + thử nghiệm hiệu năng** | Chương **Argon2 + Hashcat + kết luận & khuyến nghị** |
| Slide & demo | Slide **kiến trúc & demo luồng**; **điều phối** buổi tập bảo vệ | Slide **số liệu & biểu đồ** | Slide **tấn công & kết luận**; chạy **demo** trước hội đồng |
| Đầu ra tuần | Bản PDF báo cáo + slide full | Kiểm tra trích dẫn, bảng số | Checklist nộp + máy demo sạch |

### Công việc chung mỗi tuần (cả 3)

- Cập nhật tiến độ cho GVHD (theo quy định lớp).
- Ghi **CHANGELOG** ngắn: việc đã xong / đang làm / bị block.
- Không commit mật khẩu thật, token, hay dump DB có dữ liệu cá nhân.

---

## Tài liệu tham khảo (gợi ý)

1. *Real-World Cryptography* — David Wong, Manning Publications, 2021.  
2. Percival, C., *Stronger Key Derivation via Sequential Memory-Hard Functions* (Scrypt).  
3. OWASP — [Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).  
4. Hoàng Thu Phương, “Nghiên cứu đánh giá độ mạnh mật khẩu trong hệ thống xác thực,” *Tạp chí Khoa học và Công nghệ ATTT*, 2024.

---
