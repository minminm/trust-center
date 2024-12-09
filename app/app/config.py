"""
Global Configuration for Application
"""

import logging
import os
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOTENV_PATH = os.path.join(BASE_DIR, ".env")
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)

# Get configuration from environment
BACKEND_PORT = int(os.getenv("PORT", "8080"))

LOGGING_LEVEL = logging.INFO

SECRET_KEY = "YP9h7S0L+wXt06f5RSg/gQ=="

# DB configuration
DB_PORT = 5432
DB_DB_NAME = "trust_center"
DB_UNAME = "postgres"
DB_PASSWD = "123456"
DB_VERSION = "16"
DB_CLUSTER_NAME = "main"
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg://{DB_UNAME}:{DB_PASSWD}@localhost:{DB_PORT}/{DB_DB_NAME}"
)

# JWT
JWT_SECRET_KEY = "YP9h7S0L+wXt06f5RSg/gQ=="
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
