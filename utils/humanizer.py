import random


SMALL_REPLIES = [
    "😂",
    "😭",
    "💀",
    "Lmao",
    "Fr?",
    "Bro...",
    "Abe 😂",
    "👀",
    "Bruh 💀",
    "Accha 😂",
    "Sach me? 😭",
    "Ye unexpected tha 💀",
]


def random_small_reply():
    if random.random() < 0.10:  # 10% chance
        return random.choice(SMALL_REPLIES)
    return None


def random_typing_delay():
    return random.uniform(0.8, 2.2)