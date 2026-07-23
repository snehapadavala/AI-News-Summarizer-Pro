# AI News Summarizer Pro

AI News Summarizer Pro is a premium Flask-based web application that lets users paste articles, upload TXT/PDF files, or enter a news URL to generate concise AI-powered summaries.

## Features

- Paste article text for instant summarization
- Upload TXT and PDF documents
- Extract and summarize content from URLs
- Configure summary length and generation settings
- View summary statistics and analysis metadata
- Copy, download, print, or share summaries
- Keep recent history in memory and inspect it from the UI

## Folder Structure

- app.py — Flask entry point and routes
- config.py — app configuration values
- utils/ — validator, extractor, summarizer, helper, and statistics modules
- templates/ — HTML templates for home, 404, and 500 pages
- static/ — CSS and JavaScript assets
- uploads/ — uploaded files

## Installation

```bash
cd AI-News-Summarizer-Pro
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then visit http://127.0.0.1:5000/.

## Deployment

The app can be deployed using any WSGI-compatible host such as Gunicorn on a cloud server or container platform.

## Future Improvements

- Persist history in a database
- Add user authentication
- Support more AI models and multilingual summarization
