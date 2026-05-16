from __future__ import annotations

import base64
from typing import Optional

from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools.function_tool import FunctionTool
from google.genai import types

from config import GEMINI_MODEL
import rag

APP_NAME = "sauti-ya-mwananchi"


def _search_legal_docs(query: str) -> dict:
    snippets = rag.search_legal_docs(query)
    return {"snippets": snippets}


msaidizi = LlmAgent(
    name="msaidizi",
    model=GEMINI_MODEL,
    instruction=(
        "You are the front door for Sauti ya Mwananchi. Be neutral, multilingual, "
        "and helpful. Keep answers short and actionable. Do not endorse any party "
        "or candidate. If asked for personal political advice, decline and offer "
        "general civic information instead."
    ),
)

mwalimu = LlmAgent(
    name="mwalimu",
    model=GEMINI_MODEL,
    instruction=(
        "You are the legal explainer. Use the tool to fetch official legal snippets "
        "and answer only from those snippets. Always cite sources with short labels "
        "like [Source 1]. If no sources are returned, say you do not have enough "
        "official information." 
    ),
    tools=[FunctionTool(_search_legal_docs)],
)

kiongozi = LlmAgent(
    name="kiongozi",
    model=GEMINI_MODEL,
    instruction=(
        "You guide voters to polling stations and steps. Never ask for national ID. "
        "Ask for county, constituency, and ward to help locate the polling station." 
    ),
)

ukweli = LlmAgent(
    name="ukweli",
    model=GEMINI_MODEL,
    instruction=(
        "You are a fact checker. Provide a verdict at the top: VERIFIED, UNVERIFIED, "
        "or FALSE. Then explain briefly and cite reliable sources when possible. If "
        "an image is provided, analyze it carefully before responding." 
    ),
)

mwenza = LlmAgent(
    name="mwenza",
    model=GEMINI_MODEL,
    instruction=(
        "You guide election day procedures: what to bring, how to vote, queue tips, "
        "and how to report issues. Provide concise steps." 
    ),
)

router = LlmAgent(
    name="router",
    model=GEMINI_MODEL,
    instruction=(
        "Route the user to exactly one sub-agent using transfer_to_agent. "
        "Use mwalimu for legal or constitutional questions. Use ukweli for fact "
        "checking or claims. Use kiongozi for polling station or location guidance. "
        "Use mwenza for election day process questions. Otherwise use msaidizi."
    ),
    sub_agents=[msaidizi, mwalimu, kiongozi, ukweli, mwenza],
)

runner = InMemoryRunner(agent=router, app_name=APP_NAME)


async def _ensure_session(user_id: str, session_id: str) -> None:
    session = await runner.session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )


def _build_message(message: str, image_base64: Optional[str]) -> types.Content:
    parts: list[types.Part] = [types.Part(text=message)]
    if image_base64:
        image_bytes = base64.b64decode(image_base64)
        parts.append(
            types.Part(
                inline_data=types.Blob(
                    mime_type="image/jpeg",
                    data=image_bytes,
                )
            )
        )
    return types.Content(role="user", parts=parts)


def _extract_text_parts(content: object) -> list[str]:
    if isinstance(content, dict):
        parts = content.get("parts")
    else:
        parts = getattr(content, "parts", None)
    if not parts:
        return []

    texts: list[str] = []
    for part in parts:
        if isinstance(part, dict):
            text = part.get("text")
        else:
            text = getattr(part, "text", None)
        if text:
            texts.append(text)
    return texts


async def run_adk_chat(
    message: str,
    session_id: str,
    image_base64: Optional[str] = None,
) -> tuple[str, str]:
    user_id = session_id
    await _ensure_session(user_id, session_id)

    new_message = _build_message(message, image_base64)
    last_text = ""
    last_agent = "msaidizi"

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        content = getattr(event, "content", None)
        if content:
            texts = _extract_text_parts(content)
            if texts:
                last_text = texts[-1]

        author = getattr(event, "author", None)
        if author:
            last_agent = author

        is_final = getattr(event, "is_final_response", None)
        if callable(is_final) and is_final():
            break

    if not last_text:
        last_text = "Sorry, I could not generate a response."

    return last_agent, last_text
