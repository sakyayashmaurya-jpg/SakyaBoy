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

        friendship = await get_friendship(user.id)

        if friendship:
            xp, level, total_messages, mood = friendship
        else:
            xp = 0
            level = 1
            total_messages = 0
            mood = "Neutral"

        memories = await get_memories(user.id)
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
            value=str(level),
            inline=True
        )

        embed.add_field(
            name="⭐ XP",
            value=str(xp),
            inline=True
        )

        embed.add_field(
            name="💬 Messages",
            value=str(total_messages),
            inline=True
        )

        embed.add_field(
            name="😊 Mood",
            value=str(mood),
            inline=True
        )

        embed.add_field(
            name="🧠 Memories",
            value=str(memory_count),
            inline=True
        )

        embed.set_footer(
            text=f"Requested by {user.name}"
        )

        await interaction.response.send_message(
            embed=embed
        )

    # ----------------------------
    # Memory Command
    # ----------------------------
    @app_commands.command(
        name="memory",
        description="See what SakyaBoy remembers about you."
    )
    async def memory(
        self,
        interaction: discord.Interaction
    ):

        user = interaction.user

        memories = await get_memories(user.id)

        if not memories:

            embed = discord.Embed(
                title="🧠 SakyaBoy Memory",
                description="Mujhe abhi tak tumhare baare me kuch yaad nahi hai 😭",
                color=discord.Color.orange()
            )

            await interaction.response.send_message(
                embed=embed
            )
            return

        embed = discord.Embed(
            title="🧠 SakyaBoy Memory",
            description="Ye cheeze mujhe tumhare baare me yaad hain.",
            color=discord.Color.green()
        )

        for key, value in memories.items():

            pretty_name = (
                key.replace("_", " ")
                .title()
            )

            embed.add_field(
                name=f"📌 {pretty_name}",
                value=value,
                inline=False
            )

        embed.set_footer(
            text=f"{len(memories)} memories stored"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Slash(bot))