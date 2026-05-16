from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from adk_app import run_adk_chat
from guardrails import NEUTRAL_RESPONSE, is_jailbreak

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

    agent, reply = await run_adk_chat(
        message=req.message,
        session_id=req.session_id,
        image_base64=req.image_base64,
    )
    return ChatResponse(agent=agent, reply=reply)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}