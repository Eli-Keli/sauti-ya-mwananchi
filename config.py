import os

from dotenv import load_dotenv

_ENV_PATH = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=_ENV_PATH)

GOOGLE_CLOUD_PROJECT = os.environ.get("GOOGLE_CLOUD_PROJECT", "gdg-agentathon-2026")
GCS_BUCKET = os.environ.get("GCS_BUCKET", "sauti-ya-mwananchi-legal-docs")
VERTEX_SEARCH_DATASTORE_ID = os.environ.get("VERTEX_SEARCH_DATASTORE_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-1.5-pro")

if GEMINI_API_KEY and not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
