"""
Module tích hợp ba giải thuật băm mật khẩu: Bcrypt, Scrypt, Argon2id.
Dùng passlib; chuỗi trả về chứa salt và tham số (định dạng modular crypt).
"""

from __future__ import annotations

from enum import Enum

from passlib.context import CryptContext
from passlib.hash import argon2, bcrypt, scrypt

_verify_ctx = CryptContext(schemes=["argon2", "bcrypt", "scrypt"], deprecated="auto")


class HashAlgorithm(str, Enum):
    BCRYPT = "bcrypt"
    SCRYPT = "scrypt"
    ARGON2 = "argon2"


def hash_password(plain_password: str, algorithm: HashAlgorithm) -> tuple[str, str]:
    """
    Băm mật khẩu theo thuật toán chỉ định.
    Trả về (password_hash, algorithm_key) để lưu CSDL.
    """
    if algorithm == HashAlgorithm.BCRYPT:
        digest = bcrypt.using(rounds=12).hash(plain_password)
    elif algorithm == HashAlgorithm.SCRYPT:
        digest = scrypt.using(rounds=14, block_size=8, parallelism=1).hash(plain_password)
    else:
        digest = argon2.using(
            time_cost=3,
            memory_cost=65536,
            parallelism=2,
            type="ID",
        ).hash(plain_password)

    return digest, algorithm.value


def verify_password(plain_password: str, stored_hash: str) -> bool:
    try:
        return _verify_ctx.verify(plain_password, stored_hash)
    except ValueError:
        return False


def detect_algorithm_from_hash(stored_hash: str) -> str | None:
    if stored_hash.startswith("$argon2"):
        return HashAlgorithm.ARGON2.value
    if stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"):
        return HashAlgorithm.BCRYPT.value
    if "scrypt" in stored_hash[:20].lower() or stored_hash.startswith("$scrypt$"):
        return HashAlgorithm.SCRYPT.value
    return None
