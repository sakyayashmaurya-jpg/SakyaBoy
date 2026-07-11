MEMORY_KEYWORDS = [
    "my name",
    "mera naam",
    "i am",
    "i'm",
    "main hu",
    "main hoon",
    "age",
    "years old",
    "birthday",
    "born",
    "city",
    "from",
    "live in",
    "favorite",
    "favourite",
    "pasand",
    "love",
    "nickname",
    "call me",
    "school",
    "college",
    "job",
    "work",
    "game",
    "minecraft",
    "valorant"
]


def should_extract_memory(message: str) -> bool:
    message = message.lower()

    return any(keyword in message for keyword in MEMORY_KEYWORDS)