import discord

from discord.ext import commands
from discord import app_commands

from database import (
    create_report,
    add_witness,
    get_report,
    get_channel_id
)

from config import REPORT_TYPES


class Reports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # ======================================================
    # SIGNALER UN JOUEUR
    # ======================================================

    @app_commands.command(
        name="signaler-joueur",
        description="Signaler un joueur"
    )
    async def signaler_joueur(
        self,
        interaction: discord.Interaction,
        joueur: discord.Member,
        motif: str,
        description: str,
        preuve: str = "",
        anonyme: bool = False,
        souhaite_contact: bool = False
    ):

        motif = motif.upper()

        if motif not in REPORT_TYPES:

            return await interaction.response.send_message(
                "❌ Motif invalide.",
                ephemeral=True
            )

        if motif == "AUTRE" and len(description.strip()) < 15:

            return await interaction.response.send_message(
                "❌ Pour AUTRE, un témoignage détaillé est obligatoire.",
                ephemeral=True
            )

        report_id = await create_report(
            interaction.guild.id,
            interaction.user.id,
            joueur.id,
            motif,
            description,
            preuve,
            anonyme,
            souhaite_contact
        )

        # ===============================
        # LOGS
        # ===============================

        channel_id = await get_channel_id(
            interaction.guild.id,
            "signalements"
        )

        if channel_id:

            channel = interaction.guild.get_channel(
                channel_id
            )

            if channel:

                embed = discord.Embed(
                    title=f"📢 Nouveau signalement #{report_id}",
                    color=discord.Color.orange()
                )

                embed.add_field(
                    name="Joueur signalé",
                    value=joueur.mention,
                    inline=False
                )

                embed.add_field(
                    name="Motif",
                    value=motif,
                    inline=False
                )

                embed.add_field(
                    name="Description",
                    value=description[:1024],
                    inline=False
                )

                auteur = (
                    "ANONYME"
                    if anonyme
                    else interaction.user.mention
                )

                embed.add_field(
                    name="Auteur",
                    value=auteur,
                    inline=False
                )

                if preuve:

                    embed.add_field(
                        name="Preuve",
                        value=preuve,
                        inline=False
                    )

                await channel.send(
                    embed=embed
                )

        await interaction.response.send_message(
            (
                f"✅ Signalement enregistré.\n\n"
                f"Numéro du dossier : #{report_id}"
            ),
            ephemeral=True
        )

    # ======================================================
    # TÉMOIGNAGE
    # ======================================================

    @app_commands.command(
        name="signaler-temoignage",
        description="Ajouter un témoignage"
    )
    async def signaler_temoignage(
        self,
        interaction: discord.Interaction,
        numero_dossier: int,
        temoignage: str,
        preuve: str = ""
    ):

        report = await get_report(
            numero_dossier
        )

        if not report:

            return await interaction.response.send_message(
                "❌ Dossier introuvable.",
                ephemeral=True
            )

        await add_witness(
            numero_dossier,
            interaction.user.id,
            temoignage,
            preuve
        )

        await interaction.response.send_message(
            (
                f"✅ Témoignage ajouté au "
                f"dossier #{numero_dossier}"
            ),
            ephemeral=True
        )

    # ======================================================
    # MES DOSSIERS
    # ======================================================

    @app_commands.command(
        name="mes-signalements",
        description="Voir vos signalements"
    )
    async def mes_signalements(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.send_message(
            (
                "📁 Fonction en cours de développement.\n"
                "Disponible dans la prochaine version."
            ),
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        Reports(bot)
    )
