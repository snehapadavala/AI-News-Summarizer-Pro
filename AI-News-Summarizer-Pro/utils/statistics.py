import re
from typing import Dict, Any


def calculate_statistics(original_text: str, summary_text: str, processing_time_ms: float, model_used: str) -> Dict[str, Any]:
    """Compute useful summarization metrics."""
    original_words = len(re.findall(r"\b\w+\b", original_text))
    summary_words = len(re.findall(r"\b\w+\b", summary_text))
    compression_percent = round(max(0, 100 - (summary_words / original_words * 100)) if original_words else 0, 1)

    return {
        "originalWords": original_words,
        "summaryWords": summary_words,
        "compressionPercentage": compression_percent,
        "readingTimeSaved": max(1, round((original_words / 200) - (summary_words / 200))),
        "originalLength": len(original_text),
        "summaryLength": len(summary_text),
        "sentenceCount": len(re.findall(r"[^.!?]+[.!?]", summary_text)),
        "processingTime": round(processing_time_ms, 2),
        "modelUsed": model_used,
    }
