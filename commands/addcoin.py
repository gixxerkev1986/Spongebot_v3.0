import discord
from discord.ext import commands
from discord import app_commands

class AddCoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="addcoin", description="Voeg coin toe aan je portfolio (mock)")
    async def addcoin(self, interaction: discord.Interaction):
        await interaction.response.send_message("Coin succesvol toegevoegd aan mock portfolio.")

async def setup(bot):
    await bot.add_cog(AddCoin(bot))