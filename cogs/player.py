from discord.ext import commands
from discord import app_commands
import discord

class Player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    player = app_commands.Group(
        name="player",
        description="Commandes joueur"
    )

    @player.command(
        name="profile",
        description="Voir son profil"
    )
    async def profile(
        self,
        interaction: discord.Interaction
    ):

        embed = discord.Embed(
            title="Profil joueur",
            description=f"Joueur : {interaction.user.mention}"
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Player(bot))
