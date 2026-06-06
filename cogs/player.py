from discord.ext import commands
from discord import app_commands
import discord

from database import (
    get_player_points,
    get_player_infractions
)

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="profil",
        description="Voir votre profil disciplinaire"
    )
    async def profil(
        self,
        interaction: discord.Interaction
    ):

        points = await get_player_points(
            interaction.guild.id,
            interaction.user.id
        )

        embed = discord.Embed(
            title="Profil disciplinaire",
            description=(
                f"Joueur : {interaction.user.mention}\n"
                f"Points : **{points}**"
            )
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    @app_commands.command(
        name="historique",
        description="Voir votre historique"
    )
    async def historique(
        self,
        interaction: discord.Interaction
    ):

        rows = await get_player_infractions(
            interaction.guild.id,
            interaction.user.id
        )

        if not rows:

            return await interaction.response.send_message(
                "Aucune sanction enregistrée.",
                ephemeral=True
            )

        lines = []

        for row in rows[:10]:

            lines.append(
                f"• {row[4]} ({row[5]}) : {row[7]}"
            )

        embed = discord.Embed(
            title="Historique disciplinaire",
            description="\n".join(lines)
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

async def setup(bot):

    await bot.add_cog(
        Player(bot)
    )
