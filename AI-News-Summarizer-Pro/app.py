import os
import time
from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, render_template, request

from config import Config
from utils.extractor import ExtractionError, extract_from_pdf, extract_from_text, extract_from_txt, extract_from_url
from utils.helpers import create_id, ensure_upload_dir, safe_json_response, sanitize_text
from utils.statistics import calculate_statistics
from utils.summarizer import SummarizationError, summarize_text
from utils.validator import ValidationError, validate_article_text, validate_summary_options, validate_uploaded_file, validate_url

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config.from_object(Config)
ensure_upload_dir(app.config["UPLOAD_FOLDER"])

history_store: List[Dict[str, Any]] = []


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(_error):
    return render_template("500.html"), 500


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/summarize")
def summarize():
    try:
        payload = request.get_json(silent=True) or {}
        article_text = validate_article_text(payload.get("article", ""))
        options = validate_summary_options(payload)
        summary_result = summarize_text(article_text, options)
        statistics = calculate_statistics(
            article_text,
            summary_result["summary"],
            summary_result["processingTimeMs"],
            summary_result["modelUsed"],
        )

        history_entry = {
            "id": create_id(),
            "title": summary_result["analysis"]["headline"],
            "summary": summary_result["summary"],
            "source": "Pasted Article",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "favorite": False,
        }
        history_store.append(history_entry)
        return safe_json_response(
            {
                "success": True,
                "summary": summary_result["summary"],
                "analysis": summary_result["analysis"],
                "statistics": statistics,
                "history": history_store,
                "message": "Summary generated successfully.",
            }
        )
    except ValidationError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 400)
    except SummarizationError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 500)
    except Exception as exc:  # pragma: no cover - defensive path
        return safe_json_response({"success": False, "message": f"Unexpected error: {exc}"}, 500)


@app.post("/upload")
def upload():
    try:
        file_storage = request.files.get("file")
        extension, filename = validate_uploaded_file(file_storage)
        ensure_upload_dir(app.config["UPLOAD_FOLDER"])
        file_path = Path(app.config["UPLOAD_FOLDER"]) / file_storage.filename
        file_storage.save(file_path)

        if extension == "txt":
            article_text, source_name = extract_from_txt(str(file_path))
        else:
            article_text, source_name = extract_from_pdf(str(file_path))

        options = validate_summary_options(request.form.to_dict())
        summary_result = summarize_text(article_text, options)
        statistics = calculate_statistics(article_text, summary_result["summary"], summary_result["processingTimeMs"], summary_result["modelUsed"])

        history_entry = {
            "id": create_id(),
            "title": f"{source_name} Summary",
            "summary": summary_result["summary"],
            "source": source_name,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "favorite": False,
        }
        history_store.append(history_entry)
        return safe_json_response(
            {
                "success": True,
                "summary": summary_result["summary"],
                "analysis": summary_result["analysis"],
                "statistics": statistics,
                "history": history_store,
                "message": "Summary generated from uploaded file.",
            }
        )
    except ValidationError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 400)
    except ExtractionError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 422)
    except Exception as exc:  # pragma: no cover - defensive path
        return safe_json_response({"success": False, "message": f"Unexpected error: {exc}"}, 500)


@app.post("/url")
def url_summary():
    try:
        payload = request.get_json(silent=True) or {}
        url_value = validate_url(payload.get("url", ""))
        article_text, title = extract_from_url(url_value)
        options = validate_summary_options(payload)
        summary_result = summarize_text(article_text, options)
        statistics = calculate_statistics(article_text, summary_result["summary"], summary_result["processingTimeMs"], summary_result["modelUsed"])

        history_entry = {
            "id": create_id(),
            "title": title,
            "summary": summary_result["summary"],
            "source": url_value,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "favorite": False,
        }
        history_store.append(history_entry)
        return safe_json_response(
            {
                "success": True,
                "summary": summary_result["summary"],
                "analysis": summary_result["analysis"],
                "statistics": statistics,
                "history": history_store,
                "message": "Summary generated from the news URL.",
            }
        )
    except ValidationError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 400)
    except ExtractionError as exc:
        return safe_json_response({"success": False, "message": str(exc)}, 422)
    except Exception as exc:  # pragma: no cover - defensive path
        return safe_json_response({"success": False, "message": f"Unexpected error: {exc}"}, 500)


@app.get("/history")
def history():
    return safe_json_response({"success": True, "history": history_store})


@app.delete("/history")
def clear_history():
    history_store.clear()
    return safe_json_response({"success": True, "message": "History cleared.", "history": history_store})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
