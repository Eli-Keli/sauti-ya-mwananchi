import google.generativeai as genai

import config
import rag

genai.configure(api_key=config.GEMINI_API_KEY)


def run(message: str, history: list) -> str:
	chunks = rag.search_legal_docs(message)
	context = "\n\n".join(chunks) if chunks else "No documents found."

	system = (
		"You are Mwalimu, a civic educator who answers ONLY from the provided documents. "
		"Cite every fact with its source (e.g. 'Article 38 of the Constitution of Kenya 2010' "
		"or 'Section 22 of the Elections Act Cap 7'). If the answer is not in the documents, "
		"say so and do not guess. Absolute political neutrality.\n\n"
		"DOCUMENTS:\n"
		f"{context}"
	)
	model = genai.GenerativeModel(config.GEMINI_MODEL)
	chat = model.start_chat(history=history, system_instruction=system)
	return chat.send_message(message).text
