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

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Status dictionary
status_overzicht = {
    "analyse": "🟢 Werkt met echte TA + AI",
    "dagelijks": "🟡 Mock actief, TA integratie volgt",
    "signal": "🟡 Mock actief, RSI/EMA advies gepland",
    "short": "🟡 AI mock, later op basis van /analyse ID",
    "long": "🟡 AI mock, later op basis van /analyse ID",
    "accumuleer": "🟡 Mock actief, DCA-strategie in ontwikkeling",
    "alert": "🟡 Mock actief, prijsalerts worden gebouwd",
    "addcoin": "🟡 Mock actief, coinregistratie komt eraan",
    "statustradesim": "🟡 Mock actief, winstmarge overzicht later",
    "setexchange": "⚪️ Nog bouwen, exchange-specifiek systeem",
    "setfee": "⚪️ Nog bouwen, fee % per exchange/user",
    "vraag": "🟡 Mock via OpenRouter, AI live integratie volgt",
    "leermoment": "🟡 Mock actief, feedback-opslag gepland",
    "voorspeltest": "🟢 Beschikbaar in Kulleke structuur",
    "models": "🟢 Modelkeuze werkend via OpenRouter",
    "sentiment": "🟡 Mock actief, CoinGecko sentiment later",
    "trending": "🟡 Mock actief, trending coins module volgt",
    "heatmap": "⚪️ Nog niet gestart, bij sterke beweging",
    "dominantie": "⚪️ Nog niet gestart, marktdominantieanalyse",
    "airdrop": "⚪️ Gepland, met suggesties & verwachte winst",
    "brugtip": "⚪️ Gepland, bruggen naar layer 2’s",
    "ping": "🟢 Actief",
    "status": "🟢 Overzicht werkend",
    "api-server": "🟡 Lokale TA-API draait, Binance live binnenkort"
}

@bot.event
async def on_ready():
    logger.info(f"Bot is online als {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        logger.info(f"Slash commands gesynchroniseerd ({len(synced)}): {[cmd.name for cmd in synced]}")
    except Exception as e:
        logger.error(f"Fout bij syncen van commands: {e}")

# Werkende en mock commando's

@tree.command(name="ping", description="Test of de bot werkt", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    logger.info("/ping ontvangen")
    await interaction.response.send_message("Pong!")

@tree.command(name="status", description="Toon de huidige status van Spongebot", guild=discord.Object(id=GUILD_ID))
async def status(interaction: discord.Interaction):
    logger.info("/status ontvangen")
    response = "**Spongebot v2.1 Statusoverzicht**\n\n"
    for cmd, status in status_overzicht.items():
        response += f"• `/{cmd}` – {status}\n"
    await interaction.response.send_message(response)

@tree.command(name="analyse", description="Voer technische analyse uit", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC, KAS, FET...")
async def analyse(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Mock analyse voor {coin.upper()}...\n(TA komt eraan!)")

@tree.command(name="dagelijks", description="Geef dagelijkse analyse van een coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. SOL, FET, KAS...")
async def dagelijks(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Mock dagelijks overzicht voor {coin.upper()}")

@tree.command(name="signal", description="Geef koop/verkoop signaal voor een coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC, KAS, FET...")
async def signal(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Mock signal voor {coin.upper()} – advies volgt")

@tree.command(name="short", description="AI-shortadvies op basis van analyse ID", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(id="Bijv. #A123")
async def short(interaction: discord.Interaction, id: str):
    await interaction.response.send_message(f"Mock SHORT-analyse op basis van ID {id}")

@tree.command(name="long", description="AI-longadvies op basis van analyse ID", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(id="Bijv. #A123")
async def long(interaction: discord.Interaction, id: str):
    await interaction.response.send_message(f"Mock LONG-analyse op basis van ID {id}")

@tree.command(name="accumuleer", description="Mock accumulatie-analyse", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. FET, KAS...")
async def accumuleer(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Mock DCA-plan voor {coin.upper()} – analyse volgt")

@tree.command(name="alert", description="Stel prijsalert in", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC", prijs="Bijv. 0.055")
async def alert(interaction: discord.Interaction, coin: str, prijs: float):
    await interaction.response.send_message(f"Alert ingesteld voor {coin.upper()} bij prijs {prijs} – (mock)")

@tree.command(name="setexchange", description="Stel je exchange in", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(exchange="Bijv. Binance, Bitvavo...")
async def setexchange(interaction: discord.Interaction, exchange: str):
    await interaction.response.send_message(f"Mock: Exchange ingesteld op {exchange}")

@tree.command(name="setfee", description="Stel feepercentage in", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(percentage="Bijv. 0.25")
async def setfee(interaction: discord.Interaction, percentage: float):
    await interaction.response.send_message(f"Mock: Fee ingesteld op {percentage}%")

@tree.command(name="vraag", description="Stel een AI-vraag over crypto", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(tekst="Bijv. Is Solana bullish?")
async def vraag(interaction: discord.Interaction, tekst: str):
    await interaction.response.send_message(f"AI mockantwoord: interessante vraag – '{tekst}'")

@tree.command(name="leermoment", description="Geef feedback op analyse", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Coin waarop je analyse gaf", resultaat="winst/verlies")
async def leermoment(interaction: discord.Interaction, coin: str, resultaat: str):
    await interaction.response.send_message(f"Mock: Analyse van {coin.upper()} = {resultaat.upper()} opgeslagen.")

@tree.command(name="sentiment", description="Mock sentiment rond een coin", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC, FET...")
async def sentiment(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Sentiment voor {coin.upper()} = positief (mock)")

@tree.command(name="heatmap", description="Mock heatmap bij sterke marktbeweging", guild=discord.Object(id=GUILD_ID))
async def heatmap(interaction: discord.Interaction):
    await interaction.response.send_message("Mock heatmap: BTC & SOL stijgen sterk!")

@tree.command(name="dominantie", description="Mock marktdominantie-analyse", guild=discord.Object(id=GUILD_ID))
async def dominantie(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: BTC dominantie 53.2%, ETH 17.4%")

@tree.command(name="airdrop", description="Suggesties voor airdrops", guild=discord.Object(id=GUILD_ID))
async def airdrop(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: Check LayerZero, ZKSync, en Eigenlayer!")

@tree.command(name="brugtip", description="Brugsuggesties voor nieuwe chains", guild=discord.Object(id=GUILD_ID))
async def brugtip(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: Brug van Ethereum naar Base via Orbiter.Finance")

# Start de bot
async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
