import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import init_db

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

# ==========================================================
# INTENTS
# ==========================================================

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

# ==========================================================
# BOT
# ==========================================================

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# ==========================================================
# COGS
# ==========================================================

COGS = [
    "cogs.admin",
    "cogs.moderation",
    "cogs.player",
    "cogs.reports"
]

# ==========================================================
# STARTUP
# ==========================================================

@bot.event
async def setup_hook():

    print("Initialisation base de données...")

    await init_db()

    print("Base de données prête.")

    for cog in COGS:

        try:

            await bot.load_extension(cog)

            print(f"✅ Cog chargé : {cog}")

        except Exception as e:

            print(f"❌ Erreur chargement {cog}")
            print(e)

# ==========================================================
# READY
# ==========================================================

@bot.event
async def on_ready():

    print("\n" + "=" * 50)
    print("TeRom-Punisher connecté")
    print("=" * 50)

    print(f"Bot : {bot.user}")
    print(f"ID  : {bot.user.id}")

    print("\nServeurs connectés :")

    for guild in bot.guilds:

        print(
            f"- {guild.name} "
            f"({guild.id})"
        )

    print()

    try:

        if GUILD_ID:

            guild = discord.Object(
                id=GUILD_ID
            )

            synced = await bot.tree.sync(
                guild=guild
            )

            print(
                f"✅ Slash synchronisées "
                f"(serveur test) : {len(synced)}"
            )

        else:

            synced = await bot.tree.sync()

            print(
                f"✅ Slash globales : "
                f"{len(synced)}"
            )

    except Exception as e:

        print("❌ Erreur sync")

        print(e)

    print("=" * 50)

# ==========================================================
# ERREURS SLASH COMMANDS
# ==========================================================

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error
):

    print(error)

    try:

        if interaction.response.is_done():

            await interaction.followup.send(
                "❌ Une erreur est survenue.",
                ephemeral=True
            )

        else:

            await interaction.response.send_message(
                "❌ Une erreur est survenue.",
                ephemeral=True
            )

    except Exception:

        pass

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    if not TOKEN:

        raise ValueError(
            "DISCORD_TOKEN manquant dans le .env"
        )

    bot.run(TOKEN)
