import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt")

    # Prefer DATABASE_URL if set, else build from PG_* vars, else fallback to SQLite
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        DB_USER = os.getenv("POSTGRES_USER", "postgres")
        DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
        DB_HOST = os.getenv("POSTGRES_HOST", "db")
        DB_PORT = os.getenv("POSTGRES_PORT", "5432")
        DB_NAME = os.getenv("POSTGRES_DB", "property_db")
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", DATABASE_URL)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
