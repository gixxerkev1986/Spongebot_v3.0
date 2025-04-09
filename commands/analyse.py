import discord
from discord import app_commands
from discord.ext import commands
import httpx
import uuid
import os
import datetime
import logging

logger = logging.getLogger("spongebot")

API_URL = "http://spongebot.hopto.org:5050/api/crypto/"
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")
GUILD_ID = int(os.getenv("GUILD_ID"))

class Analyse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyse", description="Voer een multi-timeframe analyse uit")
    @app_commands.describe(coin="Bijvoorbeeld BTC, FET, KAS")
    async def analyse(self, interaction: discord.Interaction, coin: str):
        await interaction.response.defer()
        symbol = coin.upper() + "USDT"
        timeframes = ["5m", "15m", "1h", "1d"]
        results = {}

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
            ta_text += f"{tf}: RSI {d['rsi']} | EMA20: {d['ema20']} | EMA50: {d['ema50']} â†’ **{trend}**\n"

        # Analyse-ID
        analyse_id = f"A{str(uuid.uuid4())[:4]}"

        # Vraag AI om samenvatting
        try:
            ai_prompt = f"Geef een korte samenvatting en verwachting voor de volgende coin op basis van RSI/EMA gegevens:\n{ta_text}"
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
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

async def setup(bot):
    await bot.add_cog(Analyse(bot))
