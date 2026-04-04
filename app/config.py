import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

SECRET_KEY = os.getenv("SECRET_KEY", "").strip() or secrets.token_hex(32)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/app.db").strip()
