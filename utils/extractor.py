import json
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)


SYSTEM_PROMPT = """
Extract user memories.

Return ONLY JSON.

If nothing useful exists return:

{}

Possible keys:

name
age
city
country
favorite_game
favorite_anime
favorite_food
favorite_color
birthday
nickname
gender

Examples:

User:
My name is Alex.

Output:
{"name":"Alex"}

User:
I love Valorant.

Output:
{"favorite_game":"Valorant"}

User:
Nothing.

Output:
{}
"""


def extract_memory(message):

    response = client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0,
        max_tokens=120
    )

    text = response.choices[0].message.content

    try:
        return json.loads(text)
    except:
        return {}