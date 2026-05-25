# Dữ liệu thực nghiệm

*(Chèn vào Chương Kết quả — bảng/biểu đồ; số liệu lấy từ `results/` sau khi chạy script.)*

## 1. Môi trường ghi nhận số liệu

Nguồn: `results/benchmark_environment.txt` (cập nhật mỗi lần chạy benchmark).

| Hạng mục | Giá trị |
|----------|---------|
| Python | 3.9.6 |
| Nền tảng | macOS-15.1-arm64-arm-64bit |
| Mật khẩu mẫu | `Secret123!` (độ dài 10) |
| Số lần lặp benchmark | 1 *(có thể tăng: `scripts/benchmark_hash.py -n 50`)* |
| Thời điểm ghi (UTC) | 2026-05-25T14:58:25+00:00 |

**Lưu ý quan trọng:** Với `bcrypt rounds=20`, một lần băm trên máy đo trên khoảng **~64 giây**; benchmark 50 lần chỉ riêng Bcrypt có thể mất **hàng giờ**. Khi so sánh tương đối ba thuật toán, có thể dùng **cùng số lần lặp nhỏ** (3–10) hoặc ghi rõ trong báo cáo là “một lần đo đại diện”.

---

## 2. Kết quả kiểm thử chức năng

**Bảng 4.x — Kiểm thử thủ công (trình duyệt / curl)**

| ID | Kịch bản | Kết quả mong đợi | Kết quả | Ghi chú |
|----|-----------|------------------|---------|---------|
| TC-01 | Đăng ký `user_bcrypt`, algorithm bcrypt | Tạo user, vào dashboard | Đạt | Seed script hoặc form |
| TC-02 | Đăng ký `user_scrypt`, scrypt | Hash prefix scrypt | Đạt | |
| TC-03 | Đăng ký `user_argon2`, argon2 | Hash `$argon2id$` | Đạt | |
| TC-04 | Đăng nhập đúng MK lab | Vào dashboard | Đạt | |
| TC-05 | Đăng nhập sai MK | Thông báo chung, không vào dashboard | Đạt | |
| TC-06 | Đăng ký trùng username | Lỗi nghiệp vụ | Đạt | |
| TC-07 | MK &lt; 8 ký tự | Từ chối | Đạt | |
| TC-08 | `GET /health` | `{"status":"ok"}` | Đạt | |

*Chèn ảnh: form đăng ký, dashboard, DataGrip bảng `users`.*

---

## 3. Dữ liệu CSDL mẫu (ba tài khoản lab)

Tạo bằng: `python scripts/seed_lab_users.py` (MK lab: `Secret123!`).

**Bảng 4.x — Trích `users` (hash rút gọn)**

| id | username | algorithm | password_hash (rút gọn) | created_at |
|----|----------|-----------|-------------------------|------------|
| 14 | user_bcrypt | bcrypt | `$2b$20$Bdzy2hmxWFwGb4KCbWUpaO2b1mWihzlPy1oFzsa9r…` | 2026-05-25 14:41:56 |
| 15 | user_scrypt | scrypt | `$scrypt$ln=14,r=8,p=1$yLmXkpISAkBIKQVAqPWeMw$Ttj…` | 2026-05-25 14:41:57 |
| 16 | user_argon2 | argon2 | `$argon2id$v=19$m=65536,t=3,p=2$YMz5vzdmLOU8h1Aqx…` | 2026-05-25 14:41:57 |

**Nhận xét (gợi ý):** Cùng mật khẩu `Secret123!` nhưng **ba chuỗi hash hoàn toàn khác**; tiền tố phản ánh thuật toán (`$2b$20$` — cost 20, `$scrypt$`, `$argon2id$`). Salt nằm trong chuỗi, không có cột salt riêng.

Bảng đầy đủ (mọi user trong DB): `results/users_sample.md`.

---

## 4. Kết quả đo hiệu năng băm / xác minh

Phương pháp: gọi trực tiếp `hash_password` và `verify_password` trong `app/auth/hashing.py`, đo bằng `time.perf_counter()`.

**Bảng 4.x — Thời gian (ms), n = 1 lần / thuật toán**

| Thuật toán | Tham số | Hash TB (ms) | Verify TB (ms) |
|------------|---------|--------------|----------------|
| bcrypt | rounds=20 | 64093,96 | 63721,27 |
| scrypt | rounds=14, block_size=8, parallelism=1 | 93,73 | 92,88 |
| argon2 (Argon2id) | time_cost=3, memory_cost=65536, parallelism=2, type=ID | 77,52 | 67,83 |

Nguồn CSV: `results/benchmark_hash.csv`.

**Nhận xét (gợi ý cho Word):**

- Với tham số hiện tại, **Bcrypt (rounds=20)** chậm hơn rất nhiều so với Scrypt và Argon2id trên cùng máy đo — phù hợp mục tiêu “làm chậm tấn công ngoại tuyến”, nhưng cần cân nhắc **trải nghiệm đăng ký** (vài chục giây đến hơn một phút mỗi lần băm).
- **Scrypt** và **Argon2id** cùng cỡ **~70–95 ms** cho một lần băm với cấu hình trong code; Argon2id verify hơi nhanh hơn trong lần đo này.
- Để báo cáo có **min/max/độ lệch chuẩn**, chạy lại: `.venv/bin/python scripts/benchmark_hash.py -n 5` *(ước tính ~5+ phút chỉ riêng Bcrypt)*.

**Biểu đồ:** Vẽ cột từ cột “Hash TB (ms)” — lưu ý trục log hoặc tách hai biểu đồ (Bcrypt riêng, Scrypt/Argon2 chung) vì chênh lệch độ lớn.

---

## 5. Hashcat / tấn công ngoại tuyến (tùy chọn)

| Loại hash | Wordlist | Kết quả | Thời gian | Ghi chú |
|-----------|----------|---------|-----------|---------|
| bcrypt | … | Chưa thực hiện / … | … | Chỉ lab, hash mẫu từ `user_bcrypt` |
| scrypt | … | … | … | |
| argon2id | … | … | … | |

Export hash (ví dụ từ DataGrip, một dòng `password_hash` mỗi loại) vào file local — **không** commit wordlist hay mật khẩu thật.

---

## 6. Cách tái tạo dữ liệu cho báo cáo

```bash
.venv/bin/python scripts/seed_lab_users.py
.venv/bin/python scripts/benchmark_hash.py -n 1    # hoặc -n 5, -n 50
.venv/bin/python scripts/export_users_sample.py
```

Cập nhật lại các bảng trong file này sau khi đổi tham số trong `app/auth/hashing.py`.
