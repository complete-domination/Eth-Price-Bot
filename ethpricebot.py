import discord
from discord.ext import commands, tasks
import requests
import asyncio

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
CHANNEL_ID = 123456789012345678  # Replace with your channel ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_eth_data():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "ethereum",
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    response = requests.get(url, params=params).json()
    eth_price = response["ethereum"]["usd"]
    eth_change = response["ethereum"]["usd_24h_change"]
    return eth_price, eth_change

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    update_price.start()

@tasks.loop(minutes=5)
async def update_price():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        eth_price, eth_change = get_eth_data()
        color = 0x2ECC71 if eth_change >= 0 else 0xE74C3C
        change_symbol = "🟢" if eth_change >= 0 else "🔴"

        embed = discord.Embed(
            title=f"💠 Ethereum (ETH)",
            description=f"**${eth_price:,.2f}** {change_symbol}\n24h change: `{eth_change:+.2f}%`",
            color=color
        )
        embed.set_footer(text="Data from CoinGecko")
        await channel.send(embed=embed)
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"ETH ${eth_price:,.2f} ({eth_change:+.2f}%)"
            )
        )

@bot.command()
async def eth(ctx):
    eth_price, eth_change = get_eth_data()
    color = 0x2ECC71 if eth_change >= 0 else 0xE74C3C
    change_symbol = "🟢" if eth_change >= 0 else "🔴"

    embed = discord.Embed(
        title=f"💠 Ethereum (ETH)",
        description=f"**${eth_price:,.2f}** {change_symbol}\n24h change: `{eth_change:+.2f}%`",
        color=color
    )
    embed.set_footer(text="Data from CoinGecko")
    await ctx.send(embed=embed)

bot.run(TOKEN)
