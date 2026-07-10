import asyncio
from discord.ext import commands

from utils.ai import ask_ai
from utils.database import (
    save_user,
    save_message,
    get_history
)


class AIChat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.name != "sakya-ai":
            return

        # User register
        await save_user(
            message.author.id,
            message.author.name
        )

        # Previous history (current message se pehle)
        history = await get_history(message.author.id)

        # AI se reply lo
        async with message.channel.typing():

            await asyncio.sleep(2)

            reply = ask_ai(
                history,
                message.content
            )

        # Ab dono messages save karo
        await save_message(
            message.author.id,
            "user",
            message.content
        )

        await save_message(
            message.author.id,
            "assistant",
            reply
        )

        await message.reply(reply)


async def setup(bot):
    await bot.add_cog(AIChat(bot))