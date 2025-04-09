import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio

# Logging setup
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s')
logger = logging.getLogger("spongebot")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

@bot.event
async def on_ready():
    logger.info(f"Bot is online als {bot.user}")
    try:
        # Forceer zowel globale als guild-specifieke sync
        global_synced = await tree.sync()
        logger.info(f"✅ Globale slash commands: {[cmd.name for cmd in global_synced]}")
        guild_synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        logger.info(f"✅ Guild slash commands ({GUILD_ID}): {[cmd.name for cmd in guild_synced]}")
    except Exception as e:
        logger.error(f"❌ Fout bij slash sync: {e}")
    
    await load_cogs()

async def load_cogs():
    cogs = ["ping", "trending", "addcoin", "statustradesim", "analyse"]
    for cog in cogs:
        try:
            await bot.load_extension(f"commands.{cog}")
            logger.info(f"✅ Module geladen: {cog}.py")
        except Exception as e:
            logger.error(f"❌ Fout bij laden {cog}.py: {e}")

async def main():
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
