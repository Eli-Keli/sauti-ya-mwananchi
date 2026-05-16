import os

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gdg-agentathon-2026")
GCS_BUCKET = os.environ.get("GCS_BUCKET", "sauti-ya-mwananchi-legal-docs")
VERTEX_SEARCH_DATASTORE_ID = os.environ.get("kenyan-legal-knowledge_1778934505364")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
