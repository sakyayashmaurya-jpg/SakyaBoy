import asyncio
from discord.ext import commands

from utils.extractor import extract_memory
from utils.memory_filter import should_extract_memory
from utils.reply_engine import generate_reply
from utils.rate_limit import is_rate_limited
from utils.cooldown import is_on_cooldown

from utils.database import (
    save_user,
    save_message,
    get_history,
    save_memory,
    get_memories,
    update_friendship,
    get_friendship
)


class AIChat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        # Ignore bots
        if message.author.bot:
            return

        # Reply only in AI channel or when mentioned
        if (
            message.channel.name != "sakya-ai"
            and self.bot.user not in message.mentions
        ):
            return

        # Remove bot mention
        clean_message = message.content.replace(
            self.bot.user.mention,
            ""
        ).strip()

        if not clean_message:
            clean_message = "hi"

        # -------------------------
        # Anti Spam
        # -------------------------
        if is_rate_limited(
            message.author.id,
            clean_message
        ):
            return

        # -------------------------
        # User Cooldown
        # -------------------------
        if is_on_cooldown(
            message.author.id
        ):
            return

        # -------------------------
        # Reply Context
        # -------------------------
        if (
            message.reference
            and message.reference.resolved
            and message.reference.resolved.author.id == self.bot.user.id
        ):
            previous_reply = message.reference.resolved.content

            clean_message = (
                f"Previous bot message:\n"
                f"{previous_reply}\n\n"
                f"User replied:\n"
                f"{clean_message}"
            )

        # -------------------------
        # Save User
        # -------------------------
        await save_user(
            message.author.id,
            message.author.name
        )

        # -------------------------
        # Friendship
        # -------------------------
        await update_friendship(
            message.author.id
        )

        friendship = await get_friendship(
            message.author.id
        )

        if friendship:
            xp, level, total_messages, mood = friendship
        else:
            xp, level, total_messages, mood = (
                0, 1, 0, "neutral"
            )

        # -------------------------
        # Memory Extraction
        # -------------------------
        if should_extract_memory(clean_message):

            memories = extract_memory(
                clean_message
            )

            for key, value in memories.items():
                await save_memory(
                    message.author.id,
                    key,
                    value
                )

        # -------------------------
        # Chat History
        # -------------------------
        history = await get_history(
            message.author.id,
            limit=8
        )

        # -------------------------
        # Memories
        # -------------------------
        memories = await get_memories(
            message.author.id
        )

        # -------------------------
        # Generate Reply
        # -------------------------
        async with message.channel.typing():

            reply = await generate_reply(
                history=history,
                memories=memories,
                level=level,
                clean_message=clean_message
            )

        # -------------------------
        # Save Conversation
        # -------------------------
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

        # -------------------------
        # Send Reply
        # -------------------------
        await message.reply(reply)


async def setup(bot):
    await bot.add_cog(AIChat(bot))