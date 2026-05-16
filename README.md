# Sauti ya Mwananchi

Sauti ya Mwananchi is a multi-agent civic participation chatbot for Kenya's elections. It bridges the gap between "I am registered" and "I know what I am voting for" by giving neutral, verified, and practical guidance to voters in plain language.

## Problem we are solving
Kenyan youth registered in record numbers, but many still lack clear, trusted, and neutral information about their rights, voting rules, and what to do on election day. This project helps voters understand the process, find where to vote, and avoid misinformation without pushing any political agenda.

## Agent architecture
The system uses Google ADK with a coordinator agent that delegates each message to exactly one specialized agent. Sessions are handled by ADK's in-memory session service and are not persisted.

Agents:
- Msaidizi: front-door and orchestrator, multilingual, handles greetings and unclear queries
- Mwalimu: civic educator, answers only from official documents using RAG
- Kiongozi: polling station and registration guidance (voters.iebc.or.ke)
- Ukweli: fact-checker for election claims and images, returns one verdict
- Mwenza: election day companion with short, step-by-step instructions

Tools and services:
- Google ADK (LlmAgent + InMemoryRunner) for routing and responses
- Gemini (text + vision) as the model backend
- Vertex AI Search for legal document retrieval
- FastAPI for the backend API

How they communicate:
- main.py receives the request and calls the ADK runner in adk_app.py
- the coordinator agent delegates to a sub-agent using transfer_to_agent
- ADK stores events in an in-memory session scoped to session_id

## Run locally

Requirements:
- Python 3.11+
- Gemini API key
- Vertex AI Search datastore (optional but recommended)

Setup:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run:
```
uvicorn main:app --host 0.0.0.0 --port 8080
```

Health check:
```
curl http://localhost:8080/health
```

Chat API:
```
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-1","message":"Nipateje kituo changu cha kupigia kura?","image_base64":null}'
```

## Deployed version
Live UI (Cloud Run):
https://sauti-ya-mwananchi-804854368817.europe-west2.run.app/

How to interact:
1. Open the link above.
2. Ask a question in English, Kiswahili, or Sheng.
3. The system routes you to the right agent and responds in the same language.

## Demo
Live demo URL:
https://sauti-ya-mwananchi-804854368817.europe-west2.run.app/

## Team
- Emmanuel - Team Member
- Isaac - Team Member
- Glory - Team Member
- Isabella - Team Member

## Data handling and political neutrality policy (Challenge 06)
- No voter ID data is collected, stored, or repeated. If asked, the system refuses and asks only for ward or constituency.
- Session history is in memory only and resets when the server restarts.
- Mwalimu only answers from official documents and cites each fact. If the answer is not in the documents, it says so.
- Ukweli always returns exactly one grounded verdict: VERIFIED, UNVERIFIED, or FALSE, with a source.
- The system is politically neutral and does not comment on candidates, parties, or endorsements.
