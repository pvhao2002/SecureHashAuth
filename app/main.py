from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app.auth.hashing import HashAlgorithm
from app.auth.service import AuthError, authenticate, register_user
from app.config import SECRET_KEY, STATIC_DIR, TEMPLATES_DIR
from app.database import get_db, init_db
from app.models import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="SecureHashAuth", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=86400 * 7)

if STATIC_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def get_current_user_id(request: Request) -> int | None:
    uid = request.session.get("user_id")
    if uid is None:
        return None
    try:
        return int(uid)
    except (TypeError, ValueError):
        return None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Annotated[Session, Depends(get_db)]):
    user = None
    uid = get_current_user_id(request)
    if uid is not None:
        user = db.get(User, uid)
    flash_ok = request.session.pop("flash_ok", None)
    flash_error = request.session.pop("flash_error", None)
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "user": user,
            "algorithms": [(a.value, a.name.replace("_", " ").title()) for a in HashAlgorithm],
            "flash_ok": flash_ok,
            "flash_error": flash_error,
        },
    )


@app.post("/register")
async def post_register(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...),
    algorithm: str = Form(...),
):
    try:
        algo = HashAlgorithm(algorithm)
    except ValueError:
        request.session["flash_error"] = "Thuật toán không hợp lệ."
        return RedirectResponse("/", status_code=303)
    try:
        user = register_user(db, username, password, algo)
    except AuthError as e:
        request.session["flash_error"] = str(e)
        return RedirectResponse("/", status_code=303)
    request.session["user_id"] = user.id
    request.session["flash_ok"] = "Đăng ký thành công."
    return RedirectResponse("/dashboard", status_code=303)


@app.post("/login")
async def post_login(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    username: str = Form(...),
    password: str = Form(...),
):
    user = authenticate(db, username, password)
    if user is None:
        request.session["flash_error"] = "Sai tên đăng nhập hoặc mật khẩu."
        return RedirectResponse("/", status_code=303)
    request.session["user_id"] = user.id
    request.session["flash_ok"] = "Đăng nhập thành công."
    return RedirectResponse("/dashboard", status_code=303)


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/team", response_class=HTMLResponse)
async def team(request: Request, db: Annotated[Session, Depends(get_db)]):
    user = None
    uid = get_current_user_id(request)
    if uid is not None:
        user = db.get(User, uid)
    members = [
        {
            "name": "Huỳnh Quỳnh Đức",
            "student_id": "2033221009",
            "is_leader": True,
        },
        {
            "name": "Mai Thái Đăng",
            "student_id": "2033220956",
            "is_leader": False,
        },
        {
            "name": "Nguyễn Xuân Cường",
            "student_id": "2033220447",
            "is_leader": False,
        },
    ]
    return templates.TemplateResponse(
        request,
        "team.html",
        {"user": user, "members": members},
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Annotated[Session, Depends(get_db)]):
    uid = get_current_user_id(request)
    if uid is None:
        return RedirectResponse("/", status_code=303)
    user = db.get(User, uid)
    if user is None:
        request.session.clear()
        return RedirectResponse("/", status_code=303)
    flash_ok = request.session.pop("flash_ok", None)
    flash_error = request.session.pop("flash_error", None)
    # Không truyền full hash lên UI — chỉ tiền tố che bớt
    hash_preview = user.password_hash[:24] + "…" if len(user.password_hash) > 24 else user.password_hash
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "user": user,
            "hash_preview": hash_preview,
            "flash_ok": flash_ok,
            "flash_error": flash_error,
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
