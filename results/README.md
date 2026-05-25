# Kết quả thực nghiệm

Chạy từ thư mục gốc project (có `.venv` và `requirements.txt`):

```bash
.venv/bin/python scripts/seed_lab_users.py
.venv/bin/python scripts/benchmark_hash.py -n 1    # nhanh; -n 50 với bcrypt rounds=20 rất lâu
.venv/bin/python scripts/export_users_sample.py
```

| File | Mô tả |
|------|--------|
| `benchmark_hash.csv` | Thời gian băm/xác minh (ms); mặc định script `-n 10`, báo cáo có thể `-n 50` |
| `benchmark_environment.txt` | Python, platform, ngày ghi |
| `users_sample.md` | Bảng users (hash rút gọn) cho Word |

**Lưu ý:** `data/app.db` không commit (`.gitignore`). Regenerate sau khi seed.

Hashcat (tùy chọn): export hash từ DB — không commit wordlist/mật khẩu thật.
