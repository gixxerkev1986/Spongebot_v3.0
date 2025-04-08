import discord
from discord.ext import commands
from discord import app_commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check of Spongebot leeft")
    async def ping(self, interaction: discord.Interaction):
        print("[ping] Slash command geactiveerd")
        await interaction.response.send_message("Pong! Spongebot V2 clean is online.")

async def setup(bot):
    await bot.add_cog(Ping(bot))