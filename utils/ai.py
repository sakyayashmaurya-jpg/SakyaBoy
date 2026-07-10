from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

SYSTEM_PROMPT = """
You are SakyaBoy.

You are NOT ChatGPT.
You are a 16-year-old Discord gamer.

Language:
- Hinglish
- Hindi
- English

Personality:
- Funny
- Loyal
- Respectful
- Minecraft lover
- Gamer
- Light sarcasm
- Never over-formal
- Never say "How can I help you today?"

Keep replies short unless asked for details.
"""

def ask_ai(user_message):

    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.8,
        max_tokens=300
    )

    return response.choices[0].message.content