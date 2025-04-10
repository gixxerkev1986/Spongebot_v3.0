import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import requests

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
    "airdrop": "🟢 Live via DeFiLlama API",
    "status": "🟢 Overzicht werkend",
    "ping": "🟢 Actief",
    "claimcheck": "⚪️ Gepland",
    "walletscan": "⚪️ Gepland",
    "airdrops": "⚪️ Gepland",
    "accustrategie": "⚪️ Gepland",
    "simulate": "⚪️ Gepland",
    "setbudget": "⚪️ Gepland",
    "exitplan": "⚪️ Gepland",
    "whalealert": "⚪️ Gepland",
    "fibonacci": "⚪️ Gepland"
}

@bot.event
async def on_ready():
    logger.info(f"Bot is online als {bot.user}")
    try:
        synced = await tree.sync(guild=discord.Object(id=GUILD_ID))
        logger.info(f"Slash commands gesynchroniseerd ({len(synced)}): {[cmd.name for cmd in synced]}")
    except Exception as e:
        logger.error(f"Fout bij syncen van commands: {e}")

@tree.command(name="ping", description="Test of de bot werkt", guild=discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="status", description="Toon de huidige status van Spongebot", guild=discord.Object(id=GUILD_ID))
async def status(interaction: discord.Interaction):
    response = "**Spongebot v2.1 Statusoverzicht**\n\n"
    for cmd, stat in status_overzicht.items():
        response += f"• `/{cmd}` – {stat}\n"
    await interaction.response.send_message(response)

@tree.command(name="analyse", description="Voer technische analyse uit", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(coin="Bijv. BTC, KAS, FET...")
async def analyse(interaction: discord.Interaction, coin: str):
    await interaction.response.defer()
    try:
        symbol = f"{coin.upper()}USDT"
        url = f"http://spongebot.hopto.org:5050/api/crypto/{symbol}/1d"
        res = requests.get(url, timeout=10)
        data = res.json()
        logger.debug(f"Analyse API response: {data}")
        latest = data.get("result", [])[-1] if data.get("result") else None

        if latest is None:
            raise ValueError("Geen analysegegevens ontvangen.")

        close = float(latest.get("close", 0))
        rsi = float(latest.get("rsi", 0))
        ema20 = float(latest.get("ema20", 0))
        ema50 = float(latest.get("ema50", 0))

        trend = "📈 Opwaarts" if ema20 > ema50 else "📉 Neerwaarts" if ema20 < ema50 else "➡️ Zijwaarts"
        advies = "Kans op herstel" if rsi < 40 else "Oververhit" if rsi > 70 else "Neutraal"

        response = (
            f"**Technische Analyse – {coin.upper()} (1D)**\n"
            f"• Sluitprijs: ${close:,.2f}\n"
            f"• RSI: {rsi:.2f}\n"
            f"• EMA20: {ema20:.2f}\n"
            f"• EMA50: {ema50:.2f}\n"
            f"• Trend: {trend}\n"
            f"**Advies:** {advies}"
        )
        await interaction.followup.send(response)
    except Exception as e:
        logger.error(f"Fout bij analyse: {e}")
        await interaction.followup.send("Er ging iets mis bij het ophalen van de analyse.")

@tree.command(name="airdrop", description="Live overzicht van potentiële airdrops (DeFiLlama)", guild=discord.Object(id=GUILD_ID))
async def airdrop(interaction: discord.Interaction):
    try:
        res = requests.get("https://api.llama.fi/airdrop")
        data = res.json()
        embed = discord.Embed(title="🪂 Live Airdrop Radar (via DeFiLlama)", color=0x00ffcc)
        count = 0
        for project in data:
            if not project.get("hasToken") and count < 5:
                name = project.get("name", "Onbekend")
                chains = ", ".join(project.get("chains", [])) or "Onbekend"
                url = project.get("url", "https://defillama.com")
                tvl = project.get("tvl", 0)
                description = f"🌐 **Chains**: {chains}\n💰 **TVL**: ${int(tvl):,}\n🔗 [Bezoek project]({url})"
                embed.add_field(name=f"{count+1}. {name}", value=description, inline=False)
                count += 1

        if count == 0:
            embed.description = "Geen nieuwe airdrops gevonden zonder token."
        embed.set_footer(text="Data van DefiLlama.com – realtime update bij elke oproep")
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        logger.error(f"Fout bij ophalen airdrops: {e}")
        await interaction.response.send_message("Er ging iets mis bij het ophalen van de airdrops.")

# Start de bot
async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
