import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import httpx

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

@tree.command(name="analyse", description="AI technische analyse van een coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. kaspa, fet, link")
async def analyse(interaction: discord.Interaction, coin: str):
    logger.info(f"/analyse gestart voor: {coin}")
    try:
        await interaction.response.defer()
    except Exception as e:
        logger.warning(f"Kon interaction.defer() niet uitvoeren: {e}")

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {
                "role": "user",
                "content": f"Geef een korte technische analyse van de coin {coin.upper()}, met een inschatting van de trend, RSI, volume en een potentieel instapmoment."
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
            logger.info(f"OpenRouter status: {response.status_code}")
            logger.debug(f"OpenRouter response: {response.text}")

            if response.status_code == 200:
                result = response.json()
                analyse_tekst = result["choices"][0]["message"]["content"]
                await interaction.followup.send(f"AI-analyse voor {coin.upper()}:\n\n{analyse_tekst}")
            else:
                await interaction.followup.send("Er ging iets mis met de AI-analyse.")
    except Exception as e:
        logger.exception("Fout bij AI-aanvraag")
        await interaction.followup.send("Er ging iets fout tijdens het ophalen van de analyse.")

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
