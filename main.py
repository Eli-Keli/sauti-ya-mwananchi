from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents import kiongozi, msaidizi, mwalimu, mwenza, ukweli
from guardrails import NEUTRAL_RESPONSE, is_jailbreak
from router import route
from session import get_history, update_history

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str
    message: str
    image_base64: str | None = None


class ChatResponse(BaseModel):
    agent: str
    reply: str


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    if is_jailbreak(req.message):
        return ChatResponse(agent="msaidizi", reply=NEUTRAL_RESPONSE)

    history = get_history(req.session_id)
    agent = route(req.message)

    if agent == "mwalimu":
        reply = mwalimu.run(req.message, history)
    elif agent == "kiongozi":
        reply = kiongozi.run(req.message, history)
    elif agent == "ukweli":
        reply = ukweli.run(req.message, history, req.image_base64)
    elif agent == "mwenza":
        reply = mwenza.run(req.message, history)
    else:
        reply = msaidizi.run(req.message, history)

    update_history(req.session_id, req.message, reply)
    return ChatResponse(agent=agent, reply=reply)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}