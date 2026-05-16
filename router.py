import google.generativeai as genai

import config

genai.configure(api_key=config.GEMINI_API_KEY)

_ROUTER_PROMPT = """
Classify this user message into exactly one agent:
- mwalimu: civic education, Constitution of Kenya, voting rights, Elections Act, IEBC rules
- kiongozi: finding polling station, voter registration status
- ukweli: fact-checking a claim or image about an election
- mwenza: what to do on election day, ballot marking, queues, what to bring
- msaidizi: greetings, unclear queries, anything else

Reply with ONLY the agent name, nothing else.
Message: {message}
"""


def route(message: str) -> str:
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	response = model.generate_content(_ROUTER_PROMPT.format(message=message))
	agent = response.text.strip().lower()
	allowed = {"mwalimu", "kiongozi", "ukweli", "mwenza", "msaidizi"}
	return agent if agent in allowed else "msaidizi"
