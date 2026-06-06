import discord

from discord.ext import commands
from discord import app_commands

from database import (
    is_admin,
    set_role_id,
    set_channel_id,
    create_season,
    get_settings
)


class Administration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    administration = app_commands.Group(
        name="administration",
        description="Gestion du bot"
    )

    async def check_admin(
        self,
        interaction: discord.Interaction
    ):

        if not await is_admin(
            interaction.guild.id,
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ Réservé aux Admins.",
                ephemeral=True
            )

            return False

        return True

    # ======================================================
    # ROLE
    # ======================================================

    @administration.command(
        name="definir-role",
        description="Définir un rôle du bot"
    )
    @app_commands.describe(
        type_role="admin, modo, warning, probation, suspendu ou banni",
        role="Rôle Discord"
    )
    async def definir_role(
        self,
        interaction: discord.Interaction,
        type_role: str,
        role: discord.Role
    ):

        if not await self.check_admin(interaction):
            return

        type_role = type_role.lower()

        valid = [
            "admin",
            "modo",
            "warning",
            "probation",
            "suspendu",
            "banni"
        ]

        if type_role not in valid:

            return await interaction.response.send_message(
                f"❌ Type invalide.\n\n{', '.join(valid)}",
                ephemeral=True
            )

        await set_role_id(
            interaction.guild.id,
            type_role,
            role.id
        )

        await interaction.response.send_message(
            f"✅ Rôle **{type_role}** défini sur {role.mention}"
        )

    # ======================================================
    # SALON
    # ======================================================

    @administration.command(
        name="definir-salon",
        description="Définir un salon"
    )
    @app_commands.describe(
        type_salon="signalements, sanctions ou appel",
        salon="Salon Discord"
    )
    async def definir_salon(
        self,
        interaction: discord.Interaction,
        type_salon: str,
        salon: discord.TextChannel
    ):

        if not await self.check_admin(interaction):
            return

        type_salon = type_salon.lower()

        valid = [
            "signalements",
            "sanctions",
            "appel"
        ]

        if type_salon not in valid:

            return await interaction.response.send_message(
                f"❌ Type invalide.\n\n{', '.join(valid)}",
                ephemeral=True
            )

        await set_channel_id(
            interaction.guild.id,
            type_salon,
            salon.id
        )

        await interaction.response.send_message(
            f"✅ Salon **{type_salon}** défini sur {salon.mention}"
        )

    # ======================================================
    # SAISON
    # ======================================================

    @administration.command(
        name="creer-saison",
        description="Créer une nouvelle saison"
    )
    async def creer_saison(
        self,
        interaction: discord.Interaction,
        nom: str
    ):

        if not await self.check_admin(interaction):
            return

        await create_season(
            interaction.guild.id,
            nom
        )

        await interaction.response.send_message(
            f"✅ Saison créée : **{nom}**"
        )

    # ======================================================
    # CONFIG
    # ======================================================

    @administration.command(
        name="config",
        description="Afficher la configuration"
    )
    async def config(
        self,
        interaction: discord.Interaction
    ):

        if not await self.check_admin(interaction):
            return

        settings = await get_settings(
            interaction.guild.id
        )

        embed = discord.Embed(
            title="Configuration TeRom-Punisher"
        )

        embed.add_field(
            name="Admin",
            value=settings[1] or "Non défini",
            inline=False
        )

        embed.add_field(
            name="Modo",
            value=settings[2] or "Non défini",
            inline=False
        )

        embed.add_field(
            name="Warning",
            value=settings[3] or "Non défini",
            inline=False
        )

        embed.add_field(
            name="Probation",
            value=settings[4] or "Non défini",
            inline=False
        )

        embed.add_field(
            name="Suspendu",
            value=settings[5] or "Non défini",
            inline=False
        )

        embed.add_field(
            name="Banni",
            value=settings[6] or "Non défini",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        Administration(bot)
    )
