"""Kiểm thử nhanh: đăng ký, đăng nhập, dashboard, sai mật khẩu."""

from __future__ import annotations


def test_home_ok(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "SecureHashAuth" in r.text


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_team_page_ok(client):
    r = client.get("/team")
    assert r.status_code == 200
    for fragment in (
        "Huỳnh Quỳnh Đức",
        "Mai Thái Đăng",
        "Nguyễn Xuân Cường",
        "2033221009",
        "2033220956",
        "2033220447",
        "Nhóm trưởng",
        "Mã số sinh viên",
    ):
        assert fragment in r.text


def test_register_login_dashboard_bcrypt(client):
    r = client.post(
        "/register",
        data={
            "username": "alice",
            "password": "secret123",
            "algorithm": "bcrypt",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers.get("location") == "/dashboard"

    r2 = client.get("/dashboard", follow_redirects=False)
    assert r2.status_code == 200
    assert "alice" in r2.text
    assert "BCRYPT" in r2.text.upper() or "bcrypt" in r2.text.lower()

    client.get("/logout")
    r3 = client.post(
        "/login",
        data={"username": "alice", "password": "secret123"},
        follow_redirects=False,
    )
    assert r3.status_code == 303
    assert r3.headers.get("location") == "/dashboard"


def test_register_scrypt_and_argon2(client):
    for user, algo in [("bob", "scrypt"), ("carol", "argon2")]:
        r = client.post(
            "/register",
            data={
                "username": user,
                "password": "password99",
                "algorithm": algo,
            },
            follow_redirects=False,
        )
        assert r.status_code == 303, (user, r.text[:500])


def test_login_wrong_password(client):
    client.post(
        "/register",
        data={
            "username": "dave",
            "password": "correcthorse",
            "algorithm": "bcrypt",
        },
        follow_redirects=True,
    )
    client.get("/logout")
    r = client.post(
        "/login",
        data={"username": "dave", "password": "wrongpassword"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers.get("location") == "/"


def test_duplicate_username(client):
    data = {"username": "eve", "password": "longenough1", "algorithm": "bcrypt"}
    assert client.post("/register", data=data, follow_redirects=False).status_code == 303
    r2 = client.post("/register", data=data, follow_redirects=False)
    assert r2.status_code == 303
    assert r2.headers.get("location") == "/"
