from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.hashing import HashAlgorithm, hash_password, verify_password
from app.models import User

MIN_PASSWORD_LENGTH = 8
MAX_USERNAME_LENGTH = 64


class AuthError(Exception):
    pass


def register_user(
    db: Session,
    username: str,
    password: str,
    algorithm: HashAlgorithm,
) -> User:
    username = username.strip()
    if not username or len(username) > MAX_USERNAME_LENGTH:
        raise AuthError("Tên đăng nhập không hợp lệ.")
    if len(password) < MIN_PASSWORD_LENGTH:
        raise AuthError(f"Mật khẩu cần ít nhất {MIN_PASSWORD_LENGTH} ký tự.")

    exists = db.scalar(select(User.id).where(User.username == username))
    if exists is not None:
        raise AuthError("Tên đăng nhập đã được sử dụng.")

    digest, algo_key = hash_password(password, algorithm)
    user = User(username=username, password_hash=digest, algorithm=algo_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate(db: Session, username: str, password: str) -> User | None:
    username = username.strip()
    if not username:
        return None
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
