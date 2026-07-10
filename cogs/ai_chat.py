import asyncio
import discord
from discord.ext import commands

from utils.ai import ask_ai


class AIChat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.name != "sakya-ai":
            return

        async with message.channel.typing():

            await asyncio.sleep(2)

            reply = ask_ai(message.content)

        await message.reply(reply)


async def setup(bot):
    await bot.add_cog(AIChat(bot))