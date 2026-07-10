import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Discord
# ==========================

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

# ==========================
# AI
# ==========================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"

# ==========================
# Bot
# ==========================

BOT_NAME = "SakyaBoy"

AI_CHANNEL = "sakya-ai"

PREFIX = "!"

DEBUG = True