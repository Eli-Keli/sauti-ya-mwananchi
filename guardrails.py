JAILBREAK_PHRASES = [
	"ignore previous",
	"pretend you are",
	"your new instructions",
	"vote for",
	"best candidate",
	"worst party",
	"endorse",
	"forget your rules",
	"act as",
	"dan mode",
]

NEUTRAL_RESPONSE = (
	"Sauti ya Mwananchi upholds absolute political neutrality and cannot comment "
	"on candidates or parties."
)


def is_jailbreak(text: str) -> bool:
	lowered = text.lower()
	return any(phrase in lowered for phrase in JAILBREAK_PHRASES)
