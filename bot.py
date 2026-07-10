import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# Bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"✅ Logged in as {bot.user}")
    print("🤖 SakyaBoy AI Online!")
    print("=" * 40)

bot.run(TOKEN)