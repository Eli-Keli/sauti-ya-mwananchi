import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gdg-agentathon-2026")
GCS_BUCKET = os.environ.get("GCS_BUCKET", "sauti-ya-mwananchi-legal-docs")
VERTEX_SEARCH_DATASTORE_ID = os.environ.get("VERTEX_SEARCH_DATASTORE_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")
