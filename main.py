import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import httpx
import datetime
import uuid

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s')
logger = logging.getLogger("spongebot")

# Load env vars
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

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
        logger.error(f"Fout bij slash sync: {e}")

# -----------------------
# Slash commands
# -----------------------

@tree.command(name="ping", description="Test of de bot werkt.", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    logger.info("/ping ontvangen")
    await interaction.response.send_message("Pong!")

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

@tree.command(name="analyse", description="Voer een multi-timeframe TA-analyse uit", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijvoorbeeld BTC, FET, KAS")
async def analyse(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()

    symbol = coin.upper() + "USDT"
    timeframes = ["5m", "15m", "1h", "1d"]
    results = {}
    API_URL = "http://spongebot.hopto.org:5050/api/crypto/"

    async with httpx.AsyncClient(timeout=10) as client:
        for tf in timeframes:
            try:
                url = f"{API_URL}{symbol}/{tf}"
                logger.debug(f"TA request: {url}")
                r = await client.get(url)
                data = r.json()
                results[tf] = data
            except Exception as e:
                logger.warning(f"TA-fout voor {tf}: {e}")
                results[tf] = {"error": "geen data"}

    # Bouw samenvatting
    ta_text = f"**Analyse voor {symbol} ({datetime.datetime.now().strftime('%d-%m-%Y')})**\n"
    for tf in timeframes:
        d = results[tf]
        if "error" in d:
            ta_text += f"{tf}: [GEEN DATA]\n"
            continue
        trend = "Bullish" if d["ema20"] > d["ema50"] else "Bearish" if d["ema20"] < d["ema50"] else "Neutraal"
        ta_text += f"{tf}: RSI {d['rsi']} | EMA20: {d['ema20']} | EMA50: {d['ema50']} → **{trend}**\n"

    analyse_id = f"A{str(uuid.uuid4())[:4]}"

    # AI-samenvatting
    try:
        ai_prompt = f"Geef een korte verwachting op basis van deze gegevens:\n{ta_text}"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        body = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": ai_prompt}]
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
            ai_text = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.warning(f"AI-fout: {e}")
        ai_text = "*AI-samenvatting niet beschikbaar.*"

    ta_text += f"\n**AI Samenvatting:**\n{ai_text}\n\nID: `#{analyse_id}`"
    await interaction.followup.send(ta_text)

# Start de bot
bot.run(TOKEN)
