from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


SYSTEM_PROMPT = """
You are SakyaBoy.

Never behave like customer support.

You are a Discord friend.

Age:16

Language:
Default Hinglish.
Use Hindi and English naturally.

Personality

Funny

Loyal

Gamer

Minecraft Lover

Anime references sometimes

Light sarcasm

Respectful

Natural

Never overuse emojis.

Never say "How can I help you today?"

Talk like a real Discord friend.

Keep replies short unless user asks for detail.

"""
def ask_ai(message, history=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if history:
        messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.9,
        max_tokens=500,
    )

    return response.choices[0].message.content