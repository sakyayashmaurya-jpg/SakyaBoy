import asyncio

from utils.fun import fun_reply
from utils.ai import ask_ai
from utils.personality import get_personality
from utils.emotions import detect_emotion
from utils.humanizer import (
    random_small_reply,
    random_typing_delay
)


async def generate_reply(
    history,
    memories,
    level,
    clean_message
):
    emotion = detect_emotion(clean_message)

    # Personality
    history.insert(
        0,
        {
            "role": "system",
            "content": get_personality(level)
        }
    )

    # Memories
    if memories:

        memory_text = "\n".join(
            f"{k}: {v}"
            for k, v in memories.items()
        )

        history.insert(
            0,
            {
                "role": "system",
                "content": f"""
Known facts about this user:

{memory_text}

Use these naturally.
Only mention them when relevant.
"""
            }
        )

    # Emotion
    history.insert(
        0,
        {
            "role": "system",
            "content": f"""
Current emotion: {emotion}

Laughing → playful
Sad → supportive
Angry → calm
Excited → energetic
Friendly → warm
Curious → natural
Neutral → normal
"""
        }
    )

    # Fun replies first
    reply = fun_reply(clean_message)

    if reply:
        return reply

    # Humanizer
    reply = random_small_reply()

    if reply:
        return reply

    # AI
    await asyncio.sleep(
        random_typing_delay()
    )

    return ask_ai(
        history,
        clean_message
    )