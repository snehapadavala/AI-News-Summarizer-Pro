import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application configuration values."""

    SECRET_KEY = os.getenv("SECRET_KEY", "ai-news-summarizer-pro")
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    ALLOWED_EXTENSIONS = {"txt", "pdf"}
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "facebook/bart-large-cnn")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "sshleifer/distilbart-cnn-12-6")
    MAX_SUMMARY_CHARS = int(os.getenv("MAX_SUMMARY_CHARS", 2200))
    MAX_ARTICLE_CHARS = int(os.getenv("MAX_ARTICLE_CHARS", 25000))
    MAX_URL_LENGTH = int(os.getenv("MAX_URL_LENGTH", 2048))
