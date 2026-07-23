import re
import time
from typing import Any, Dict, List

try:
    from transformers import pipeline
except ImportError:  # pragma: no cover - optional dependency
    pipeline = None

from config import Config


class SummarizationError(RuntimeError):
    """Raised when summarization fails."""


def _split_sentences(text: str) -> List[str]:
    """Split a piece of text into meaningful sentences."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [part.strip() for part in parts if part.strip()]


def _fallback_summarize(text: str, max_length: int, min_length: int) -> str:
    """Create a deterministic fallback summary without external AI models."""
    sentences = _split_sentences(text)
    if not sentences:
        return text[: max_length]

    if len(sentences) <= 2:
        return " ".join(sentences)

    target = max(2, min(4, len(sentences) // 2))
    summary_sentences = sentences[:target]
    summary = " ".join(summary_sentences)
    if len(summary) > max_length:
        summary = summary[: max_length - 3].rsplit(" ", 1)[0] + "..."
    if len(summary) < min_length:
        summary = summary + " " + sentences[target] if target < len(sentences) else summary
    return summary


def _extract_keywords(text: str, limit: int = 5) -> List[str]:
    """Extract a simple keyword list using token frequency."""
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [word for word in words if word not in {"that", "with", "from", "this", "have", "about", "their", "there"}]
    counts: Dict[str, int] = {}
    for word in filtered:
        counts[word] = counts.get(word, 0) + 1
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [word for word, _ in ranked[:limit]]


def _generate_headline(text: str) -> str:
    """Generate a simple headline from the first meaningful words."""
    tokenized = re.findall(r"\b[a-zA-Z]{3,}\b", text)
    if not tokenized:
        return "News Summary"
    words = tokenized[:8]
    return " ".join(words).title() + "..."


def _extract_points(text: str, limit: int = 3) -> List[str]:
    """Extract the first few sentences as important points."""
    sentences = _split_sentences(text)
    return sentences[:limit]


def _categorize(text: str) -> str:
    """Classify the article into a general topic."""
    lower = text.lower()
    if any(term in lower for term in ["election", "government", "policy", "parliament", "president"]):
        return "Politics"
    if any(term in lower for term in ["tech", "software", "ai", "startup", "innovation"]):
        return "Technology"
    if any(term in lower for term in ["sport", "football", "basketball", "olympic"]):
        return "Sports"
    if any(term in lower for term in ["economy", "market", "finance", "stock", "business"]):
        return "Business"
    if any(term in lower for term in ["health", "medical", "disease", "hospital"]):
        return "Health"
    return "General"


def _detect_sentiment(text: str) -> str:
    """Estimate sentiment by checking a small positive/negative word list."""
    lower = text.lower()
    positive_terms = ["good", "great", "success", "boost", "growth", "improve", "win", "strong"]
    negative_terms = ["bad", "loss", "decline", "fail", "risk", "crisis", "attack", "injury", "fraud"]
    positive_score = sum(1 for term in positive_terms if term in lower)
    negative_score = sum(1 for term in negative_terms if term in lower)
    if positive_score > negative_score:
        return "Positive"
    if negative_score > positive_score:
        return "Negative"
    return "Neutral"


def _detect_language(text: str) -> str:
    """Return a simple language label."""
    if re.search(r"[\u0080-\uFFFF]", text):
        return "Unknown"
    return "English"


def _extract_entities(text: str) -> List[str]:
    """Extract capitalized words and named entities heuristically."""
    entities = re.findall(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text)
    return entities[:8]


def summarize_text(text: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a summary and a lightweight analysis from an article."""
    start_time = time.time()
    max_length = options.get("max_length", 130)
    min_length = options.get("min_length", 40)

    summary = ""
    model_used = "fallback"

    if pipeline is not None:
        try:
            summarizer = pipeline("summarization", model=Config.DEFAULT_MODEL, tokenizer=Config.DEFAULT_MODEL, device=-1)
            result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            summary = result[0]["summary_text"].strip()
            model_used = Config.DEFAULT_MODEL
        except Exception:
            try:
                summarizer = pipeline("summarization", model=Config.FALLBACK_MODEL, tokenizer=Config.FALLBACK_MODEL, device=-1)
                result = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
                summary = result[0]["summary_text"].strip()
                model_used = Config.FALLBACK_MODEL
            except Exception:
                summary = _fallback_summarize(text, max_length, min_length)
    else:
        summary = _fallback_summarize(text, max_length, min_length)

    analysis = {
        "keywords": _extract_keywords(text),
        "headline": _generate_headline(summary or text),
        "importantPoints": _extract_points(summary or text),
        "category": _categorize(text),
        "sentiment": _detect_sentiment(text),
        "language": _detect_language(text),
        "entities": _extract_entities(text),
    }

    processing_time_ms = round((time.time() - start_time) * 1000, 2)
    return {
        "summary": summary or _fallback_summarize(text, max_length, min_length),
        "analysis": analysis,
        "modelUsed": model_used,
        "processingTimeMs": processing_time_ms,
    }
