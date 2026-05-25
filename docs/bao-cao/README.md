# Tài liệu bổ sung báo cáo khóa luận

Ba phần thiếu trong báo cáo — sẵn sàng copy vào Word:

| File | Nội dung |
|------|----------|
| [01-nguyen-ly-du-lieu-bam.md](01-nguyen-ly-du-lieu-bam.md) | Nguyên lý **dữ liệu băm** theo **Bcrypt / Scrypt / Argon2id** (không trọng tâm luồng đăng ký) |
| [02-moi-truong-trien-khai.md](02-moi-truong-trien-khai.md) | Web chạy trên đâu (Uvicorn, FastAPI, SQLite, port 8000) |
| [03-du-lieu-thuc-nghiem.md](03-du-lieu-thuc-nghiem.md) | Khung + **số liệu** thực nghiệm (cập nhật khi chạy script) |

**Script hỗ trợ:**

```bash
.venv/bin/python scripts/seed_lab_users.py      # 3 user lab
.venv/bin/python scripts/benchmark_hash.py -n 1  # CSV (bcrypt rounds=20 ~60s/lần)
.venv/bin/python scripts/export_users_sample.py # bảng mẫu cho báo cáo
```

Sơ đồ draw.io: `docs/drawio/ch3-3.3.1-mo-hinh-tang.drawio`, `ch3-3.5.1-luong-dang-ky.drawio`, `ch3-3.5.2-luong-dang-nhap.drawio`.
