import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)


def run(message: str, history: list) -> str:
	system = (
		"You are Msaidizi, the friendly front-end of Sauti ya Mwananchi. "
		"Greet users, explain what the system can do, and handle general queries. "
		"Respond in the user's language (English, Kiswahili, or Sheng). "
		"Absolute political neutrality: never mention candidates, parties, or political opinions."
	)
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	chat = model.start_chat(history=history, system_instruction=system)
	return chat.send_message(message).text
