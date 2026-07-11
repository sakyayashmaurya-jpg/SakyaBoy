import re


LAUGH = [
    "😂", "🤣", "lol", "lmao", "rofl", "xd", "xD", "hehe", "haha", "hahaha"
]

SAD = [
    "😢", "😭", "sad", "depressed", "alone", "cry", "rona", "dukhi", "hurt"
]

ANGRY = [
    "😡", "🤬", "angry", "mad", "gussa", "hate", "bc", "wtf"
]

LOVE = [
    "❤️", "❤", "love", "ily", "cute", "pyar", "fav"
]

EXCITED = [
    "🔥", "🎉", "let's go", "lets go", "yay", "woo", "omg", "op", "w"
]


def detect_emotion(message: str):

    msg = message.lower()

    for word in LAUGH:
        if word.lower() in msg:
            return "laughing"

    for word in SAD:
        if word.lower() in msg:
            return "sad"

    for word in ANGRY:
        if word.lower() in msg:
            return "angry"

    for word in LOVE:
        if word.lower() in msg:
            return "friendly"

    for word in EXCITED:
        if word.lower() in msg:
            return "excited"

    if re.search(r"\?+$", msg):
        return "curious"

    return "neutral"