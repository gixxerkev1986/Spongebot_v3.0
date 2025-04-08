import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s')
logger = logging.getLogger("spongebot")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

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

@tree.command(name="ping", description="Test of Spongebot werkt", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    logger.info("/ping ontvangen")
    await interaction.response.send_message("Pong! Spongebot leeft.")

@tree.command(name="analyse", description="Mock analyse van een coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. kaspa, fet, link")
async def analyse(interaction: discord.Interaction, coin: str):
    logger.info(f"/analyse ontvangen voor {coin}")
    await interaction.response.send_message(f"Mock analyse voor {coin.upper()}: RSI 47, lichte bullish trend.")

@tree.command(name="trending", description="Mock lijst met trending coins", guild=discord.Object(id=GUILD_ID))
async def trending(interaction: discord.Interaction):
    logger.info("/trending ontvangen")
    await interaction.response.send_message("Trending coins (mock): KAS, FET, LINK, TAO, JOE")

@tree.command(name="addcoin", description="Mock coin toevoegen aan portfolio", guild=discord.Object(id=GUILD_ID))
async def addcoin(interaction: discord.Interaction):
    logger.info("/addcoin ontvangen")
    await interaction.response.send_message("Coin succesvol toegevoegd aan je mock portfolio.")

@tree.command(name="statustradesim", description="Mock overzicht van tradesimulaties", guild=discord.Object(id=GUILD_ID))
async def statustradesim(interaction: discord.Interaction):
    logger.info("/statustradesim ontvangen")
    await interaction.response.send_message("Mock TradeSim: 2x winst, 1x verlies — winstpercentage 66.7%.")

bot.run(TOKEN)
