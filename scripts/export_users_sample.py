#!/usr/bin/env python3
"""Xuất bảng users (hash rút gọn) cho báo cáo — stdout + results/users_sample.md."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import select  # noqa: E402

from app.database import SessionLocal, init_db  # noqa: E402
from app.models import User  # noqa: E402

PREFIX_LEN = 48


def shorten_hash(h: str, n: int = PREFIX_LEN) -> str:
    if len(h) <= n:
        return h
    return h[:n] + "…"


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        users = db.scalars(select(User).order_by(User.id)).all()
    finally:
        db.close()

    lines = [
        "| id | username | algorithm | password_hash (rút gọn) | created_at |",
        "|----|----------|-----------|-------------------------|------------|",
    ]
    for u in users:
        lines.append(
            f"| {u.id} | {u.username} | {u.algorithm} | "
            f"`{shorten_hash(u.password_hash)}` | {u.created_at} |"
        )

    text = "\n".join(lines) + "\n"
    print(text)
    out = ROOT / "results" / "users_sample.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "# Mẫu dữ liệu bảng users (lab)\n\n"
        "Mật khẩu lab dùng khi seed: `Secret123!` (chỉ dùng trong môi trường thử).\n\n"
        + text,
        encoding="utf-8",
    )
    print(f"Wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
