import discord

from discord.ext import commands
from discord import app_commands

from database import (
    is_modo,
    add_infraction,
    get_player_points,
    get_player_infractions,
    get_all_reports_pending,
    get_all_reports_by_user,
    get_infraction_count
)

from config import (
    INFRACTIONS,
    GRAVITIES,
    WARNING_THRESHOLD,
    PROBATION_THRESHOLD,
    SUSPENDED_THRESHOLD,
    BANNED_THRESHOLD
)


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def check_modo(
        self,
        interaction: discord.Interaction
    ):

        if not await is_modo(
            interaction.guild.id,
            interaction.user
        ):

            await interaction.response.send_message(
                "❌ Réservé aux modérateurs.",
                ephemeral=True
            )

            return False

        return True

    # ======================================================
    # SANCTIONNER
    # ======================================================

    @app_commands.command(
        name="moderation-sanctionner",
        description="Sanctionner un joueur"
    )
    async def sanctionner(
        self,
        interaction: discord.Interaction,
        joueur: discord.Member,
        infraction: str,
        gravite: str,
        raison: str
    ):

        if not await self.check_modo(interaction):
            return

        infraction = infraction.upper()
        gravite = gravite.upper()

        if infraction not in INFRACTIONS:

            return await interaction.response.send_message(
                "❌ Infraction invalide.",
                ephemeral=True
            )

        if gravite not in GRAVITIES:

            return await interaction.response.send_message(
                "❌ Gravité invalide.",
                ephemeral=True
            )

        points = GRAVITIES[gravite]["points"]

        total = await add_infraction(
            interaction.guild.id,
            joueur.id,
            interaction.user.id,
            infraction,
            gravite,
            points,
            raison
        )

        statut = "Normal"

        if total <= BANNED_THRESHOLD:
            statut = "⛔ Banni Ligue"

        elif total <= SUSPENDED_THRESHOLD:
            statut = "🔴 Suspendu"

        elif total <= PROBATION_THRESHOLD:
            statut = "🟡 Probation"

        elif total <= WARNING_THRESHOLD:
            statut = "⚠️ Avertissement"

        embed = discord.Embed(
            title="Sanction appliquée",
            color=discord.Color.red()
        )

        embed.add_field(
            name="Joueur",
            value=joueur.mention,
            inline=False
        )

        embed.add_field(
            name="Infraction",
            value=infraction,
            inline=True
        )

        embed.add_field(
            name="Gravité",
            value=gravite,
            inline=True
        )

        embed.add_field(
            name="Points",
            value=str(points),
            inline=True
        )

        embed.add_field(
            name="Total",
            value=str(total),
            inline=True
        )

        embed.add_field(
            name="Statut",
            value=statut,
            inline=True
        )

        embed.add_field(
            name="Raison",
            value=raison[:1024],
            inline=False
        )

        await interaction.response.send_message(
            embed=embed
        )

    # ======================================================
    # DOSSIER
    # ======================================================

    @app_commands.command(
        name="moderation-dossier",
        description="Voir le dossier d'un joueur"
    )
    async def dossier(
        self,
        interaction: discord.Interaction,
        joueur: discord.Member
    ):

        if not await self.check_modo(interaction):
            return

        points = await get_player_points(
            interaction.guild.id,
            joueur.id
        )

        sanctions = await get_infraction_count(
            interaction.guild.id,
            joueur.id
        )

        reports = await get_all_reports_by_user(
            interaction.guild.id,
            joueur.id
        )

        statut = "Normal"

        if points <= BANNED_THRESHOLD:
            statut = "⛔ Banni Ligue"

        elif points <= SUSPENDED_THRESHOLD:
            statut = "🔴 Suspendu"

        elif points <= PROBATION_THRESHOLD:
            statut = "🟡 Probation"

        elif points <= WARNING_THRESHOLD:
            statut = "⚠️ Avertissement"

        embed = discord.Embed(
            title=f"Dossier de {joueur}",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Points",
            value=str(points),
            inline=True
        )

        embed.add_field(
            name="Infractions",
            value=str(sanctions),
            inline=True
        )

        embed.add_field(
            name="Signalements",
            value=str(len(reports)),
            inline=True
        )

        embed.add_field(
            name="Statut",
            value=statut,
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    # ======================================================
    # SIGNALEMENTS
    # ======================================================

    @app_commands.command(
        name="moderation-signalements",
        description="Voir les signalements en attente"
    )
    async def signalements(
        self,
        interaction: discord.Interaction
    ):

        if not await self.check_modo(interaction):
            return

        reports = await get_all_reports_pending()

        if not reports:

            return await interaction.response.send_message(
                "✅ Aucun signalement en attente.",
                ephemeral=True
            )

        lines = []

        for report in reports[:20]:

            lines.append(
                f"#{report[0]} | Joueur : <@{report[3]}> | Motif : {report[4]}"
            )

        embed = discord.Embed(
            title="Signalements en attente",
            description="\n".join(lines),
            color=discord.Color.blurple()
        )

        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )
