#!/usr/bin/env python3
"""Tạo 3 tài khoản lab (bcrypt / scrypt / argon2) — mật khẩu cố định cho thử nghiệm."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.auth.hashing import HashAlgorithm  # noqa: E402
from app.auth.service import AuthError, register_user  # noqa: E402
from app.database import SessionLocal, init_db  # noqa: E402

LAB_PASSWORD = "Secret123!"
USERS = [
    ("user_bcrypt", HashAlgorithm.BCRYPT),
    ("user_scrypt", HashAlgorithm.SCRYPT),
    ("user_argon2", HashAlgorithm.ARGON2),
]


def main() -> None:
    init_db()
    db = SessionLocal()
    try:
        for username, algo in USERS:
            try:
                register_user(db, username, LAB_PASSWORD, algo)
                print(f"Created {username} ({algo.value})")
            except AuthError as e:
                print(f"Skip {username}: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
