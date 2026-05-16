# Sauti ya Mwananchi

Sauti ya Mwananchi is a multi-agent civic participation chatbot for Kenya's elections. It routes user queries to specialized agents for civic education, polling station guidance, fact checking, and election day support while enforcing strict political neutrality.

## Features
- Multi-agent routing for targeted help
- FastAPI backend with a single /chat endpoint
- RAG search for legal and election documents (Mwalimu agent)
- In-memory session history (no persistence)
- Neutrality guardrails for political content

## Project structure

```
sauti-ya-mwananchi/
├── main.py
├── router.py
├── guardrails.py
├── session.py
├── rag.py
├── config.py
├── agents/
│   ├── __init__.py
│   ├── msaidizi.py
│   ├── mwalimu.py
│   ├── kiongozi.py
│   ├── ukweli.py
│   └── mwenza.py
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Requirements
- Python 3.11+
- A Google Gemini API key
- Vertex AI Search datastore for legal documents (optional but recommended)

## Environment variables
Copy `.env.example` to `.env` and fill in values:

```
GOOGLE_CLOUD_PROJECT=gdg-agentathon-2026
GCS_BUCKET=sauti-ya-mwananchi-legal-docs
VERTEX_SEARCH_DATASTORE_ID=your-datastore-id-here
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-1.5-pro
```

## Install

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run locally

```
uvicorn main:app --host 0.0.0.0 --port 8080
```

Health check:

```
curl http://localhost:8080/health
```

## Chat API

`POST /chat`

Request body:

```json
{
	"session_id": "abc123",
	"message": "Nipateje kituo changu cha kupigia kura?",
	"image_base64": null
}
```

Response:

```json
{
	"agent": "kiongozi",
	"reply": "..."
}
```

## Notes
- Session history is stored in memory only and resets when the server restarts.
- The system enforces political neutrality and will not comment on candidates or parties.
- Mwalimu uses RAG; if the datastore is not configured, it will still respond but may return "not in documents".
