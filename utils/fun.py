import random

FUN_REPLIES = {
    "😂": [
        "😭",
        "Abe 😂",
        "Control bhai 😂",
        "Lmao",
        "💀"
    ],

    "😭": [
        "😂",
        "Abe ro mat 😭",
        "Skill issue 💀",
        "Lmao"
    ],

    "ok": [
        "W.",
        "Finally 😂",
        "Nice.",
        "Bas itna?"
    ],

    "okk": [
        "👍",
        "Theek hai 😂",
        "Roger that."
    ],

    "hmm": [
        "👀",
        "Bol bhi de.",
        "Suspicious..."
    ],

    "hi": [
        "Yo 😎",
        "Oye 😂",
        "Bol bro.",
        "Aa gaya finally."
    ],

    "hello": [
        "Yo 👋",
        "Hello ji 😎",
        "Kya scene?"
    ],

    "bye": [
        "Take care 👋",
        "Ghost mat ho jana 😂",
        "Milte hain."
    ],

    "good night": [
        "Good night 🌙",
        "Sapne me diamonds milen 😂"
    ]
}


def fun_reply(message: str):
    msg = message.lower().strip()

    if msg in FUN_REPLIES:
        return random.choice(FUN_REPLIES[msg])

    return None