import os
import re
from typing import Any, Dict

from flask import request

from config import Config


class ValidationError(ValueError):
    """Raised when user input does not meet required constraints."""


def validate_article_text(article_text: str) -> str:
    """Validate pasted article content."""
    if not article_text or not article_text.strip():
        raise ValidationError("Please provide an article to summarize.")

    cleaned = article_text.strip()
    if len(cleaned) < 80:
        raise ValidationError("The article is too short to summarize meaningfully.")
    if len(cleaned) > Config.MAX_ARTICLE_CHARS:
        raise ValidationError("The article is too large. Please shorten it or upload a file.")
    return cleaned


def validate_summary_options(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Validate summary settings from the client."""
    mode = payload.get("mode", "medium")
    if mode not in {"short", "medium", "detailed"}:
        mode = "medium"

    max_length = int(payload.get("maxLength", 130))
    min_length = int(payload.get("minLength", 40))
    beam_search = bool(payload.get("beamSearch", False))
    temperature = float(payload.get("temperature", 0.7))
    top_k = int(payload.get("topK", 50))
    top_p = float(payload.get("topP", 0.95))

    if max_length < 30:
        max_length = 30
    if min_length < 10:
        min_length = 10
    if max_length < min_length:
        max_length = min_length + 20

    return {
        "mode": mode,
        "max_length": max_length,
        "min_length": min_length,
        "beam_search": beam_search,
        "temperature": max(0.0, min(1.5, temperature)),
        "top_k": max(1, top_k),
        "top_p": max(0.0, min(1.0, top_p)),
    }


def validate_url(url_value: str) -> str:
    """Validate that the URL looks like a valid web page link."""
    if not url_value or not url_value.strip():
        raise ValidationError("Please provide a valid news URL.")
    if len(url_value) > Config.MAX_URL_LENGTH:
        raise ValidationError("URL is too long.")

    pattern = re.compile(r"^https?://\S+$", re.IGNORECASE)
    if not pattern.match(url_value.strip()):
        raise ValidationError("The URL must start with http:// or https://")
    return url_value.strip()


def validate_uploaded_file(file_storage) -> tuple[str, str]:
    """Validate uploaded files and return the saved path and filename."""
    if file_storage is None:
        raise ValidationError("No file was uploaded.")

    filename = file_storage.filename or ""
    if not filename:
        raise ValidationError("The uploaded file is missing a name.")

    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in Config.ALLOWED_EXTENSIONS:
        raise ValidationError("Only TXT and PDF files are supported.")

    file_storage.stream.seek(0, os.SEEK_END)
    file_size = file_storage.stream.tell()
    file_storage.stream.seek(0)
    if file_size > Config.MAX_UPLOAD_SIZE:
        raise ValidationError("The file is too large. The limit is 10MB.")

    return extension, filename
