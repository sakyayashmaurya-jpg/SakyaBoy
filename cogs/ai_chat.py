import asyncio
from discord.ext import commands

from utils.fun import fun_reply
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

        # Reply if message is in AI channel OR bot is mentioned
        if (
            message.channel.name != "sakya-ai"
            and self.bot.user not in message.mentions
        ):
            return

        # Remove bot mention from message
        clean_message = message.content.replace(
            self.bot.user.mention,
            ""
        ).strip()

        if not clean_message:
            clean_message = "hi"

        # Save user
        await save_user(
            message.author.id,
            message.author.name
        )

        # Fun Engine First
        reply = fun_reply(clean_message)

        # Agar fun reply nahi mila to AI use karo
        if reply is None:

            history = await get_history(
                message.author.id,
                limit=8
            )

            async with message.channel.typing():

                await asyncio.sleep(1)

                reply = ask_ai(
                    history,
                    clean_message
                )

        # Save messages
        await save_message(
            message.author.id,
            "user",
            clean_message
        )

        await save_message(
            message.author.id,
            "assistant",
            reply
        )

        await message.reply(reply)


async def setup(bot):
    await bot.add_cog(AIChat(bot))