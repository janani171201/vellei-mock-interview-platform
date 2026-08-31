# Vellei AI Mock Interview Platform - MVP

This is an end-to-end text mock-interview MVP based on the supplied Vellei specification.

## Features
- Candidate and job/JD context ingestion
- Interview session creation and start
- Stateful question sequencing
- Adaptive follow-up logic
- Structured answer evaluation
- Diagnostic report with strengths, gaps and recommendations
- SQLite persistence
- Optional OpenAI integration
- Deterministic fallback mode without an API key
- Minimal HTML demo UI
- Pytest tests

## Windows setup

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and http://127.0.0.1:8000/static/index.html.

Put the API key only in `.env`; never put it in browser JavaScript.

Run tests:

```powershell
pytest -q
```
