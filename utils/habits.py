import random

STARTERS = [
    "Waise...",
    "Btw...",
    "Acha sun 😂",
    "Ek baat bolu?",
    "Oye...",
    "Bro...",
    "Hmm...",
    "Acha chhod...",
    "Wait 😂",
    "Sach bolu?"
]


def add_habit(reply: str):

    # 20% chance
    if random.random() > 0.20:
        return reply

    starter = random.choice(STARTERS)

    return f"{starter}\n{reply}"