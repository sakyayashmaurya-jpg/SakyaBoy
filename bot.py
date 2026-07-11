import discord
from discord.ext import commands
import config
import asyncio

from utils.database import init_db

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)


@bot.event
async def on_ready():

    await bot.tree.sync()

    print(f"✅ {bot.user} Online")
    print("✅ Slash Commands Synced")


async def main():

    async with bot:

        await init_db()

        await bot.load_extension(
            "cogs.ai_chat"
        )

        await bot.load_extension(
            "cogs.slash"
        )

        await bot.start(
            config.DISCORD_TOKEN
        )


asyncio.run(main())