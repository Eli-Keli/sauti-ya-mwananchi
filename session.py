sessions: dict[str, list] = {}


def get_history(session_id: str) -> list:
	return sessions.get(session_id, [])


def update_history(session_id: str, user_message: str, model_reply: str) -> None:
	history = sessions.get(session_id, [])
	history = history + [
		{"role": "user", "parts": [user_message]},
		{"role": "model", "parts": [model_reply]},
	]
	sessions[session_id] = history
