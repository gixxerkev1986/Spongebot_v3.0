import discord
from discord.ext import commands
import os
import asyncio

print("⚙️ Spongebot wordt opgestart...")

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = int(os.environ.get("GUILD_ID"))  # via environment

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Ingelogd als: {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Slash commands gesynchroniseerd met GUILD {GUILD_ID} ({len(synced)} commando's)")
    except Exception as e:
        print(f"❌ Slash sync fout: {e}")
    await load_cogs()


async def load_cogs():
    cogs = ["ping", "trending", "addcoin", "statustradesim", "analyse"]
    for cog in cogs:
        try:
            await bot.load_extension(f"commands.{cog}")
            print(f"✅ {cog}.py geladen")
        except Exception as e:
            print(f"❌ Fout bij laden {cog}.py: {e}")
async def load_cogs():
    try:
        await bot.load_extension("commands.ping")
        print("✅ ping.py geladen")
    except Exception as e:
        print(f"❌ Fout bij laden ping.py: {e}")

async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())