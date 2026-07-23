import os
import re
from pathlib import Path
from typing import Tuple

import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader

from utils.helpers import normalize_whitespace


class ExtractionError(ValueError):
    """Raised when content cannot be extracted from the provided source."""


def extract_from_text(text: str) -> Tuple[str, str]:
    """Extract text from a plain text article."""
    cleaned = normalize_whitespace(text)
    if not cleaned:
        raise ExtractionError("The supplied text was empty.")
    return cleaned, "Paste Article"


def extract_from_pdf(file_path: str) -> Tuple[str, str]:
    """Extract text from a PDF document."""
    path = Path(file_path)
    if not path.exists():
        raise ExtractionError("The PDF could not be found.")

    try:
        reader = PdfReader(str(path))
        text_chunks = [page.extract_text() or "" for page in reader.pages]
        content = "\n".join(text_chunks)
        cleaned = normalize_whitespace(content)
    except Exception as exc:  # pragma: no cover - runtime error path
        raise ExtractionError(f"PDF parsing failed: {exc}") from exc

    if not cleaned:
        raise ExtractionError("The PDF did not contain readable text.")
    return cleaned, path.name


def extract_from_txt(file_path: str) -> Tuple[str, str]:
    """Extract text from a TXT file."""
    path = Path(file_path)
    if not path.exists():
        raise ExtractionError("The TXT file could not be found.")

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="latin-1")

    cleaned = normalize_whitespace(content)
    if not cleaned:
        raise ExtractionError("The TXT file did not contain readable text.")
    return cleaned, path.name


def extract_from_url(url: str) -> Tuple[str, str]:
    """Fetch a webpage and extract its article content."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ExtractionError(f"Unable to fetch URL: {exc}") from exc

    try:
        soup = BeautifulSoup(response.text, "html.parser")
    except Exception as exc:  # pragma: no cover - runtime error path
        raise ExtractionError(f"HTML parsing failed: {exc}") from exc

    for bad_tag in soup(["script", "style", "nav", "footer", "aside", "header"]):
        bad_tag.decompose()

    paragraphs = [p.get_text(" ", strip=True) for p in soup.find_all(["p", "li", "article"])]
    text = "\n".join(paragraph for paragraph in paragraphs if paragraph)
    cleaned = normalize_whitespace(text)

    if not cleaned:
        raise ExtractionError("The URL did not contain article content that could be extracted.")

    title = soup.title.get_text(strip=True) if soup.title else "News Article"
    return cleaned, title
