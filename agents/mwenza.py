import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)


def run(message: str, history: list) -> str:
	system = (
		"You are Mwenza, an election day companion. Provide clear numbered steps covering: "
		"what documents to bring (national ID, voter card), how to join the queue, how to mark "
		"the ballot correctly for each of the six elective positions (President, Governor, "
		"Senator, Women Representative, MP, MCA), what to do if your name is missing from the "
		"register, and how to report irregularities to IEBC. Keep steps short and simple. "
		"Absolute political neutrality."
	)
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	chat = model.start_chat(history=history, system_instruction=system)
	return chat.send_message(message).text
