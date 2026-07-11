import discord
from discord.ext import commands
from discord import app_commands

from utils.database import (
    get_friendship,
    get_memories
)


class Slash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ----------------------------
    # Ping Command
    # ----------------------------
    @app_commands.command(
        name="ping",
        description="Shows the bot latency."
    )
    async def ping(
        self,
        interaction: discord.Interaction
    ):

        latency = round(
            self.bot.latency * 1000
        )

        await interaction.response.send_message(
            f"🏓 Pong! `{latency} ms`"
        )

    # ----------------------------
    # Profile Command
    # ----------------------------
    @app_commands.command(
        name="profile",
        description="Shows your SakyaBoy profile."
    )
    async def profile(
        self,
        interaction: discord.Interaction
    ):

        user = interaction.user

        friendship = await get_friendship(
            user.id
        )

        if friendship:
            xp, level, total_messages, mood = friendship
        else:
            xp = 0
            level = 1
            total_messages = 0
            mood = "Neutral"

        memories = await get_memories(
            user.id
        )

        memory_count = len(memories)

        embed = discord.Embed(
            title="👤 SakyaBoy Profile",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(
            url=user.display_avatar.url
        )

        embed.add_field(
            name="❤️ Friendship Level",
            value=level,
            inline=True
        )

        embed.add_field(
            name="⭐ XP",
            value=xp,
            inline=True
        )

        embed.add_field(
            name="💬 Messages",
            value=total_messages,
            inline=True
        )

        embed.add_field(
            name="😊 Mood",
            value=mood,
            inline=True
        )

        embed.add_field(
            name="🧠 Memories",
            value=memory_count,
            inline=True
        )

        embed.set_footer(
            text=f"Requested by {user.name}"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Slash(bot))