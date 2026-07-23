import html
import re
import secrets
from pathlib import Path
from typing import Any, Dict

from flask import jsonify


def sanitize_text(value: str) -> str:
    """Escape HTML so user-supplied text is safe to render."""
    if not value:
        return ""
    return html.escape(str(value), quote=False)


def safe_json_response(payload: Dict[str, Any], status_code: int = 200):
    """Return a JSON response with consistent structure."""
    return jsonify(payload), status_code


def ensure_upload_dir(directory: str) -> None:
    """Create the directory if it does not exist."""
    Path(directory).mkdir(parents=True, exist_ok=True)


def create_id() -> str:
    """Create a short unique identifier."""
    return secrets.token_hex(4)


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """Estimate reading time in minutes."""
    words = len(re.findall(r"\b\w+\b", text))
    return max(1, round(words / words_per_minute))


def normalize_whitespace(text: str) -> str:
    """Collapse repeated whitespace and preserve sentence boundaries."""
    return re.sub(r"\s+", " ", text).strip()
