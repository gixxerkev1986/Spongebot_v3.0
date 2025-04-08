import discord
from discord.ext import commands
from discord import app_commands

class Analyse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyse", description="Mock technische analyse van een coin")
    @app_commands.describe(coin="Bijv. kaspa, fet, link")
    async def analyse(self, interaction: discord.Interaction, coin: str):
        await interaction.response.send_message(f"Mock TA voor {coin.upper()}: RSI 47, lichte bullish trend.")

async def setup(bot):
    await bot.add_cog(Analyse(bot))