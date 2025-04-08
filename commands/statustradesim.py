import discord
from discord.ext import commands
from discord import app_commands

class StatusTradeSim(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="statustradesim", description="Overzicht van tradesimulaties (mock)")
    async def statustradesim(self, interaction: discord.Interaction):
        await interaction.response.send_message("Mock TradeSim: 2x winst, 1x verlies, winstpercentage: 66.7%")

async def setup(bot):
    await bot.add_cog(StatusTradeSim(bot))