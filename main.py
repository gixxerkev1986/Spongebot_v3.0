import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import asyncio
import requests
import httpx

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)8s] %(name)s: %(message)s')
logger = logging.getLogger("spongebot")

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Status dictionary
status_overzicht = {
    "analyse": "🟢 Werkt met echte TA + AI",
    "airdrop": "🟢 Live via DeFiLlama API",
    "status": "🟢 Overzicht werkend",
    "ping": "🟢 Actief"
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
    try:
        await interaction.response.defer()
        symbol = coin.upper() + "USDT"
        timeframes = ["5m", "15m", "1h", "1d"]
        resultaten = []

        for tf in timeframes:
            url = f"http://spongebot.hopto.org:5050/api/crypto/{symbol}/{tf}"
            r = requests.get(url)
            bron = "Binance"

            if r.status_code != 200 or "result" not in r.json():
                # fallback
                url = f"http://spongebot.hopto.org:5050/api/fallback/{coin.upper()}/{tf}"
                r = requests.get(url)
                bron = "CoinGecko"

            if r.status_code != 200:
                raise Exception("Geen data voor analyse")

            data = r.json()
            laatste = data["result"][-1]
            prijs = laatste["close"]
            rsi = laatste["rsi"]
            ema20 = laatste["ema20"]
            ema50 = laatste["ema50"]

            trend = "📈 Uptrend" if ema20 > ema50 else "📉 Downtrend"
            advies = "🟢 DCA instap" if rsi < 30 else ("⚪️ Houden" if rsi < 70 else "🔴 Exit zone")

            resultaten.append({
                "tf": tf,
                "prijs": prijs,
                "rsi": rsi,
                "trend": trend,
                "advies": advies,
                "bron": bron
            })

        output = f"🔍 Analyse voor: `{coin.upper()}`\n\n"
        for r in resultaten:
            output += (
                f"⏱️ {r['tf']}  \n"
                f"• Prijs: `${r['prijs']:,}`  \n"
                f"• RSI: {r['rsi']:.1f}  \n"
                f"• Trend: {r['trend']}  \n"
                f"• Advies: {r['advies']}  \n"
                f"• Bron: {r['bron']}  \n\n"
            )

        prompt = f"Geef een korte en duidelijke samenvatting van deze analyse (coin: {coin}):\n"
        for r in resultaten:
            prompt += f"{r['tf']}: prijs {r['prijs']}, rsi {r['rsi']:.1f}, trend {r['trend']}, advies {r['advies']}. "

        # AI-samenvatting via OpenRouter
        ai_tekst = ""
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            res = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            if res.status_code == 200:
                ai_tekst = res.json()["choices"][0]["message"]["content"]
            else:
                ai_tekst = "_AI-samenvatting niet beschikbaar._"

        output += f"🧠 **AI Samenvatting**:\n{ai_tekst}"
        await interaction.followup.send(output)

    except Exception as e:
        logger.error(f"Fout bij analyse: {e}")
        await interaction.followup.send("Er ging iets mis tijdens de analyse.")

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
