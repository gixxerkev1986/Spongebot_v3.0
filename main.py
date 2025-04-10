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

# Commands

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

# ... andere commando's (analyse, dagelijks, signal, etc.) blijven identiek ...

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
            "⚙️ **Wat te doen**:\n"
            "› Gebruik [Stargate](https://stargate.finance/transfer) om ETH/USDT te bridgen\n"
            "› Herhaal 1x/week – kleine transacties\n"
            "› Claim OmniNFT’s via [OmniZone](https://omnizone.io)\n"
            "📈 **Kans**: **Zeer hoog**\n"
            "💰 **Inschatting**: €300 – €2.000"
        ),
        inline=False
    )

    embed.add_field(
        name="2. **zkSync (ZKS)**",
        value=(
            "📅 **Status**: Snapshot nog niet genomen\n"
            "⚙️ **Wat te doen**:\n"
            "› Bridge via [zkSync Portal](https://portal.zksync.io/)\n"
            "› Swappen op [SyncSwap](https://syncswap.xyz) of [Mute.io](https://app.mute.io)\n"
            "› Gebruik meerdere dApps voor interactie\n"
            "📈 **Kans**: **Hoog**\n"
            "💰 **Inschatting**: €150 – €1.200"
        ),
        inline=False
    )

    embed.add_field(
        name="3. **Blast (BLAST)**",
        value=(
            "📅 **Status**: Puntensysteem loopt\n"
            "⚙️ **Wat te doen**:\n"
            "› Bridge ETH/USDB naar [blast.io](https://blast.io)\n"
            "› Gebruik dApps zoals Pacmoon of Juice\n"
            "› Verzamel automatisch punten = toekomstige tokens\n"
            "📈 **Kans**: **Zeker** (bevestigd)\n"
            "💰 **Inschatting**: €250 – €1.000 (afhankelijk van punten)"
        ),
        inline=False
    )

    embed.add_field(
        name="4. **Scroll**",
        value=(
            "📅 **Status**: Mainnet live, snapshot verwacht\n"
            "⚙️ **Wat te doen**:\n"
            "› Bridge via [scroll.io](https://scroll.io/bridge)\n"
            "› Swappen op DEX zoals [SyncSwap](https://syncswap.xyz)\n"
            "› Test andere apps of NFT’s\n"
            "📈 **Kans**: **Hoog**\n"
            "💰 **Inschatting**: €100 – €800"
        ),
        inline=False
    )

    embed.add_field(
        name="5. **EigenLayer (restaking)**",
        value=(
            "📅 **Status**: Pre-launch fase\n"
            "⚙️ **Wat te doen**:\n"
            "› Restake ETH via [KelpDAO](https://app.kelpdao.xyz) of [EtherFi](https://etherfi.com)\n"
            "› Verdien punten = claimpositie voor token\n"
            "📈 **Kans**: **Zeer hoog**\n"
            "💰 **Inschatting**: €500 – €2.500 (afhankelijk van inzet)"
        ),
        inline=False
    )

    embed.set_footer(text="Tip: gebruik meerdere wallets voor hogere kans (MetaMask, Rabby, Argent...)")
    await interaction.response.send_message(embed=embed)

@tree.command(name="brugtip", description="Brugsuggesties voor nieuwe chains", guild=discord.Object(id=GUILD_ID))
async def brugtip(interaction: discord.Interaction):
    await interaction.response.send_message("Mock: Brug van Ethereum naar Base via Orbiter.Finance")

# Start de bot
async def main():
    async with bot:
        await bot.start(TOKEN)

asyncio.run(main())
