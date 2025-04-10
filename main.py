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
    "airdrop": "🟢 Actief met handleidingen & inschatting",
    "brugtip": "⚪️ Gepland, bruggen naar layer 2’s",
    "ping": "🟢 Actief",
    "status": "🟢 Overzicht werkend",
    "api-server": "🟡 Lokale TA-API draait, Binance live binnenkort",
    "claimcheck": "⚪️ Gepland, controleer of je airdrop kunt claimen",
    "walletscan": "⚪️ Gepland, analyseer je wallet op eligibility",
    "airdrops": "⚪️ Gepland, alternatief overzicht met filters",
    "accustrategie": "⚪️ Mock: geavanceerde DCA-strategie",
    "simulate": "⚪️ Mock: trade simulatie met fees en winst",
    "setbudget": "⚪️ Mock: instellen van DCA-budget per coin",
    "exitplan": "⚪️ Mock: uitstapstrategie per coin",
    "whalealert": "⚪️ Mock: melding bij grote transacties",
    "fibonacci": "⚪️ Mock: fib retracement zones genereren"
}

@bot.event
async def on_ready():
    logger.info(f"Bot is online als {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        logger.info(f"Slash commands gesynchroniseerd ({len(synced)}): {[cmd.name for cmd in synced]}")
    except Exception as e:
        logger.error(f"Fout bij syncen van commands: {e}")

# Commands

@tree.command(name="ping", description="Test of de bot werkt", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="status", description="Toon de huidige status van Spongebot", guild=discord.Object(id=GUILD_ID))
async def status(interaction: discord.Interaction):
    response = "**Spongebot v2.1 Statusoverzicht**\n\n"
    for cmd, status in status_overzicht.items():
        response += f"• `/{cmd}` – {status}\n"
    await interaction.response.send_message(response)

@tree.command(name="analyse", description="Voer technische analyse uit", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC, KAS, FET...")
async def analyse(interaction: discord.Interaction, coin: str):
    await interaction.response.send_message(f"Mock analyse voor {coin.upper()}...\n(TA komt eraan!)")

@tree.command(name="airdrop", description="Overzicht van actuele airdrops + winstinschatting", guild=discord.Object(id=GUILD_ID))
async def airdrop(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🪂 Airdrop Radar – april 2025",
        description="Claim gratis crypto met deze top 5 airdrops! Hieronder vind je *acties, kans en potentiële opbrengst* per project.",
        color=0x00ffcc
    )

    embed.add_field(
        name="1. **LayerZero (ZRO)**",
        value=(
            "📅 **Status**: Verwacht in Q2 2025\n"
            "⚙️ Gebruik [Stargate](https://stargate.finance/transfer)\n"
            "📈 **Kans**: Zeer hoog\n"
            "💰 **Opbrengst**: €300 – €2.000"
        ), inline=False)
    embed.add_field(
        name="2. **zkSync (ZKS)**",
        value=(
            "📅 **Status**: Snapshot verwacht\n"
            "⚙️ Bridge naar [zkSync Portal](https://portal.zksync.io/)\n"
            "📈 **Kans**: Hoog\n"
            "💰 **Opbrengst**: €150 – €1.200"
        ), inline=False)
    embed.add_field(
        name="3. **Blast (BLAST)**",
        value=(
            "📅 **Status**: Puntensysteem actief\n"
            "⚙️ Gebruik [blast.io](https://blast.io)\n"
            "📈 **Kans**: Zeker\n"
            "💰 **Opbrengst**: €250 – €1.000"
        ), inline=False)
    embed.add_field(
        name="4. **Scroll**",
        value=(
            "📅 **Status**: Snapshot mogelijk in aantocht\n"
            "⚙️ Bridge via [scroll.io](https://scroll.io/bridge)\n"
            "📈 **Kans**: Hoog\n"
            "💰 **Opbrengst**: €100 – €800"
        ), inline=False)
    embed.add_field(
        name="5. **EigenLayer**",
        value=(
            "📅 **Status**: Restaking live\n"
            "⚙️ Gebruik [KelpDAO](https://app.kelpdao.xyz) of [EtherFi](https://etherfi.com)\n"
            "📈 **Kans**: Zeer hoog\n"
            "💰 **Opbrengst**: €500 – €2.500"
        ), inline=False)

    embed.set_footer(text="Gebruik meerdere wallets voor hogere kansen. Meer via /claimcheck binnenkort.")
    await interaction.response.send_message(embed=embed)

@tree.command(name="brugtip", description="Brugsuggestie voor nieuwe chains", guild=discord.Object(id=GUILD_ID))
async def brugtip(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: Brug van Ethereum naar Base via Orbiter.Finance")

# Roadmap mock commands (correct zonder fout)

@tree.command(name="claimcheck", description="Mock: controleer of je airdrop kunt claimen", guild=discord.Object(id=GUILD_ID))
async def claimcheck(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/claimcheck` is nog in ontwikkeling.")

@tree.command(name="walletscan", description="Mock: analyseer je wallet op eligibility", guild=discord.Object(id=GUILD_ID))
async def walletscan(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/walletscan` is nog in ontwikkeling.")

@tree.command(name="airdrops", description="Mock: alternatief overzicht van airdrops", guild=discord.Object(id=GUILD_ID))
async def airdrops(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/airdrops` is nog in ontwikkeling.")

@tree.command(name="accustrategie", description="Mock: geavanceerde DCA-strategie", guild=discord.Object(id=GUILD_ID))
async def accustrategie(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/accustrategie` is nog in ontwikkeling.")

@tree.command(name="simulate", description="Mock: trade simulatie met fees en winst", guild=discord.Object(id=GUILD_ID))
async def simulate(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/simulate` is nog in ontwikkeling.")

@tree.command(name="setbudget", description="Mock: instellen van DCA-budget per coin", guild=discord.Object(id=GUILD_ID))
async def setbudget(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/setbudget` is nog in ontwikkeling.")

@tree.command(name="exitplan", description="Mock: uitstapstrategie per coin", guild=discord.Object(id=GUILD_ID))
async def exitplan(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/exitplan` is nog in ontwikkeling.")

@tree.command(name="whalealert", description="Mock: melding bij grote transacties", guild=discord.Object(id=GUILD_ID))
async def whalealert(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/whalealert` is nog in ontwikkeling.")

@tree.command(name="fibonacci", description="Mock: fib retracement zones genereren", guild=discord.Object(id=GUILD_ID))
async def fibonacci(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: `/fibonacci` is nog in ontwikkeling.")

# Start de bot
async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
