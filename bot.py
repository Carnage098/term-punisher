import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "0"))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

COGS = [
    "cogs.admin",
    "cogs.moderation",
    "cogs.player",
    "cogs.reports"
]

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Connecté en tant que {bot.user}")
    print("=" * 40)

    try:
        if GUILD_ID:
            guild = discord.Object(id=GUILD_ID)

            for cog in COGS:
                try:
                    await bot.load_extension(cog)
                    print(f"✅ {cog}")
                except Exception as e:
                    print(f"❌ {cog}: {e}")

            synced = await bot.tree.sync(guild=guild)

        else:
            for cog in COGS:
                try:
                    await bot.load_extension(cog)
                    print(f"✅ {cog}")
                except Exception as e:
                    print(f"❌ {cog}: {e}")

            synced = await bot.tree.sync()

        print(f"Slash commands : {len(synced)}")

    except Exception as e:
        print(e)

if __name__ == "__main__":
    bot.run(TOKEN)
