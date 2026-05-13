"""Configuration file for Grocery Finance System."""

import os
import secrets
from datetime import timedelta

# Database Configuration
# On Render, the persistent disk is mounted at /opt/render/project/src/data
_RENDER_DISK = "/opt/render/project/src/data"
if os.path.exists("/opt/render/project/src"):
    DB_PATH = _RENDER_DISK
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(DB_PATH, exist_ok=True)
DATABASE_URL = f"sqlite:///{DB_PATH}/grocery_finance.db"

# Security Configuration — read from environment variable for production
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# App Settings
APP_NAME = "Grocery Finance System"
APP_VERSION = "1.0.0"
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# File Upload Settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "../uploads")
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB

# AI Model Settings
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "../models")
SCALER_SAVE_PATH = os.path.join(MODEL_SAVE_PATH, "scalers")

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)
os.makedirs(SCALER_SAVE_PATH, exist_ok=True)
