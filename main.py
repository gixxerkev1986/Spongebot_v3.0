import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s')
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
    logger.info(f"Spongebot is online als {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        logger.info(f"Slash commands gesynchroniseerd: {[cmd.name for cmd in synced]}")
    except Exception as e:
        logger.error(f"Fout bij syncen van commands: {e}")

# Commands hieronder

@tree.command(name="ping", description="Test of de bot werkt.", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    logger.info("/ping ontvangen")
    await interaction.response.send_message("Pong!")

@tree.command(name="analyse", description="Mock analyse van coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. KAS, BTC, FET")
async def analyse(interaction: discord.Interaction, coin: str):
    logger.info(f"/analyse ontvangen voor: {coin}")
    await interaction.response.send_message(f"Mock analyse voor {coin.upper()}...\n(TA komt eraan!)")

@tree.command(name="trending", description="Toon mock trending coins", guild=discord.Object(id=GUILD_ID))
async def trending(interaction: discord.Interaction):
    logger.info("/trending ontvangen")
    await interaction.response.send_message("Trending coins (mock): KAS, FET, SOL")

@tree.command(name="addcoin", description="Voeg coin toe aan portfolio (mock)", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Coin naam (bv. KAS)")
async def addcoin(interaction: discord.Interaction, coin: str):
    logger.info(f"/addcoin ontvangen voor: {coin}")
    await interaction.response.send_message(f"{coin.upper()} is toegevoegd aan je mock portfolio!")

@tree.command(name="statustradesim", description="Toon mock tradesimulatie status", guild=discord.Object(id=GUILD_ID))
async def statustradesim(interaction: discord.Interaction):
    logger.info("/statustradesim ontvangen")
    await interaction.response.send_message("Gesimuleerde trades:\n+12% winst op KAS\n-4% verlies op BTC")

# Start de bot
bot.run(TOKEN)
