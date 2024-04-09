import discord
from discord.ext import commands, tasks
import os
import requests
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv("bot.env")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
ETHERSCAN_TOKEN = os.getenv("ETHERSCAN_TOKEN")
POLYGONSCAN_TOKEN = os.getenv("POLYGONSCAN_TOKEN")

# Ensure the token is loaded correctly
if DISCORD_TOKEN is None:
    print("Error: Discord token not found in bot.env file")
    raise ValueError("Discord token not found in bot.env file")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents) 

# Override the default check for the process_commands function
def custom_check(ctx):
    return True

bot.check = custom_check

@bot.event
async def on_ready():
    print("Bot is running")
    matic_loop.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "!mgas":
        await mgas(message.channel)
    elif message.content.lower() == "!egas":
        await egas(message.channel)
    else:
        await bot.process_commands(message)

async def mgas(channel):
    response = requests.get(POLYGONSCAN_TOKEN)
    gas = response.json()['result']
    m_gas = round(float(gas['FastGasPrice'])), round(float(gas['ProposeGasPrice'])), round(float(gas['SafeGasPrice']))
    embed = discord.Embed(title="__*Current MATIC Gas*__")
    embed.add_field(name="**Fast :banana: |  15 Seconds**  ", value=str(m_gas[0]) + " Gwei", inline=False)
    embed.add_field(name="**Moderate :orangutan: |  30 Seconds** ", value=str(m_gas[1]) + " Gwei", inline=False)
    embed.add_field(name="**Slow :see_no_evil: |  1 minute +** ", value=str(m_gas[2]) + " Gwei", inline=False)
    embed.set_thumbnail(url='https://images.exchangerates.org.uk/uploads/polygon-1.jpg')
    embed.set_footer(text="Data grabbed in real time from Polygonscan.")
    await channel.send(embed=embed)

async def egas(channel):
    response_eth = requests.get(ETHERSCAN_TOKEN)
    eth_gas = response_eth.json()['result']
    e_gas = int(eth_gas['FastGasPrice']), int(eth_gas['ProposeGasPrice']), int(eth_gas['SafeGasPrice'])
    embed = discord.Embed(title="__*Current ETH Gas*__")
    embed.add_field(name="**Fast :banana: |  30 Seconds**  ", value=str(e_gas[0]) + " Gwei", inline=False)
    embed.add_field(name="**Moderate :orangutan: | 3 Minutes** ", value=str(e_gas[1]) + " Gwei", inline=False)
    embed.add_field(name="**Slow :see_no_evil: |  10 Minutes** ", value=str(e_gas[2]) + " Gwei", inline=False)
    embed.set_thumbnail(url='https://crypto-money.io/wp-content/uploads/2019/10/Ethereum.jpg')
    embed.set_footer(text="Data grabbed in real time from Etherscan.")
    await channel.send(embed=embed)

@tasks.loop(seconds=10)
async def matic_loop():
    try:
        resp = requests.post(POLYGONSCAN_TOKEN)
        resp.raise_for_status()  
    except requests.RequestException as e:
        print(f"Failed to get MATIC gas prices: {e}")
        return

    gs = resp.json()['result']
    m_gs = round(float(gs['FastGasPrice'])), round(float(gs['ProposeGasPrice'])), round(float(gs['SafeGasPrice']))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="MATIC " + str(m_gs[0]) + " | " + str(m_gs[1]) + " | " + str(m_gs[2])))
    await asyncio.sleep(5)

    try:
        resp_eth = requests.get(ETHERSCAN_TOKEN)
        resp_eth.raise_for_status() 
    except requests.RequestException as e:
        print(f"Failed to get ETH gas prices: {e}")
        return

    eth_gs = resp_eth.json()['result']
    e_gs = int(eth_gs['FastGasPrice']), int(eth_gs['ProposeGasPrice']), int(eth_gs['SafeGasPrice'])
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ETH " + str(e_gs[0]) + " | " + str(e_gs[1]) + " | " + str(e_gs[2])))
    await asyncio.sleep(5) 

bot.run(DISCORD_TOKEN)
