import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)


def run(message: str, history: list) -> str:
	system = (
		"You are Kiongozi, a polling station locator. Help the user find their polling station "
		"and check voter registration at voters.iebc.or.ke. If the user has not provided their "
		"ward or constituency, ask for it. Never ask for, store, or repeat national ID numbers. "
		"Absolute political neutrality."
	)
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	chat = model.start_chat(history=history, system_instruction=system)
	return chat.send_message(message).text
