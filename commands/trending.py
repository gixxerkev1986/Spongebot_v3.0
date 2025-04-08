import discord
from discord.ext import commands
from discord import app_commands

class Trending(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="trending", description="Toon trending coins (mock)")
    async def trending(self, interaction: discord.Interaction):
        await interaction.response.send_message("Mock Trending Coins: KAS, FET, LINK, TAO, JOE")

async def setup(bot):
    await bot.add_cog(Trending(bot))