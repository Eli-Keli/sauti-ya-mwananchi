import base64

import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)


def run(message: str, history: list, image_base64: str | None = None) -> str:
	system = (
		"You are Ukweli, an election fact-checker. For every claim return exactly one verdict: "
		"VERIFIED ✓ — supported by IEBC, the Constitution, or a credible official source; "
		"UNVERIFIED ⚠ — insufficient evidence (this is a valid and required verdict); "
		"FALSE ✗ — directly contradicted by official sources. Always cite the grounding source. "
		"Never speculate. Absolute political neutrality."
	)
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	chat = model.start_chat(history=history, system_instruction=system)

	if image_base64:
		image_bytes = base64.b64decode(image_base64)
		image_part = {"mime_type": "image/jpeg", "data": image_bytes}
		return chat.send_message([message, image_part]).text

	return chat.send_message(message).text
