# Import discord.py. Allows Access to discord's API
import asyncio
import discord
from discord.ext import tasks, commands
import os
# Import requests for APIs
import requests
# Import LOAD_DOTENV function from DOTENV MODULE.
from dotenv import load_dotenv
import ccxt
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from ta import add_all_ta_features
from ta.volume import MFIIndicator

# Loads The .ENV file that resides on the same level as the script.
load_dotenv("bot.env")
# Grab the API token from the .ENV file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Gets the client object from DISCORD.PY. Client is synonymous with bot.
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents) 


binance = ccxt.binance()


def pull_quotes(pair, since, time_bucket):
    # Load OHLCV (open/high/low/close/volume) data with 1-day resolution
    ohlcv = binance.fetch_ohlcv(pair, time_bucket, since=since)

    # Get closing prices for each day
    prices = [x[4] for x in ohlcv]
    vol = [x[5] for x in ohlcv]

    # Convert Unix timestamps to Python dates
    dates = [datetime.fromtimestamp(x[0] // 1000) for x in ohlcv]

    # Prepare a Pandas series object
    data = pd.Series(prices, dates)

    return data, ohlcv


@bot.event
async def on_ready():
    print("Bot is running")
    # starts the loops for the presence updater process.
    activity_loop.start()


# Event listener for when a new message is sent to a channel.
@bot.event
async def on_message(message):
    # Checks if the message that was sent is equal to "!commands"
    if message.content == "!gashelp":
        # makes a variable with an embedded message
        embed = discord.Embed(title="Commands", description="**!egas - Retrieves ETH gas cost \n"
                                                            "\n !mgas - Retrieves MATIC gas cost**")
        # Sends the embedded message from the variable
        await message.channel.send(embed=embed)
    if message.content == "!matichelp":
        since = round(datetime.today().timestamp() * 1000 - 9000000)
        eth_data, eth_ohlcv = pull_quotes('ETH/USDT', since, '1m')
        btc_data, btc_ohlcv = pull_quotes('BTC/USDT', since, '1m')
        matic_data, matic_ohlcv = pull_quotes('MATIC/USDT', since, '1m')

        df_data = pd.DataFrame(matic_ohlcv, columns=['ts', 'open', 'high', 'low', 'adjclose', 'volume'])
        data = add_all_ta_features(df_data, open="open", high="high", low="low", close="adjclose", volume="volume")

        fig, axis = plt.subplots(2)
        plt.xlabel('Matic and BTC in Matic price')
        axis[0].plot(matic_data)
        axis[1].plot(btc_data / matic_data)
        fig.savefig('matichelp.png')
        file = discord.File("matichelp.png")  # an image in the same folder as the main bot file

        # makes a variable with an embedded message
        embed = discord.Embed(title="Price Info", description="ETH - in the past 3 hours prices ranged from " + str(
            min(eth_data)) + " and " + str(max(eth_data)) + "\n"
                                                            "\n BTC - in the past 3 hours prices ranged from " + str(
            min(btc_data)) + " and " + str(max(btc_data)) + "\n"
                                                            "\n MATIC - in the past 3 hours prices ranged from " + str(
            min(matic_data)) + " and " + str(max(matic_data))

                              )
        # embed.set_image(url="attachment://testplot.png")
        # Sends the embedded message from the variable
        await message.channel.send(embed=embed, file=file)

    if message.content == "!tradehelp":
        since = round(datetime.today().timestamp() * 1000 - 9000000)
        eth_data, eth_ohlcv = pull_quotes('ETH/USDT', since, '1m')
        btc_data, btc_ohlcv = pull_quotes('BTC/USDT', since, '1m')
        matic_data, matic_ohlcv = pull_quotes('MATIC/USDT', since, '1m')

        df_data = pd.DataFrame(eth_ohlcv, columns=['ts', 'open', 'high', 'low', 'adjclose', 'volume'])
        data = add_all_ta_features(df_data, open="open", high="high", low="low", close="adjclose", volume="volume")

        mfi = MFIIndicator(data['high'], data['low'], data['adjclose'], data['volume'], window=15)

        fig, axis = plt.subplots(2)
        plt.xlabel('ETH and MFI score')
        axis[0].plot(eth_data)
        axis[1].plot(mfi.money_flow_index())
        fig.savefig('tradehelp.png')
        file = discord.File("tradehelp.png")  # an image in the same folder as the main bot file

        # makes a variable with an embedded message
        embed = discord.Embed(title="Price Info", description="ETH - in the past 3 hours prices ranged from " + str(
            min(eth_data)) + " and " + str(max(eth_data)) + "\n"
                                                            "\n BTC - in the past 3 hours prices ranged from " + str(
            min(btc_data)) + " and " + str(max(btc_data)) + "\n"
                                                            "\n MATIC - in the past 3 hours prices ranged from " + str(
            min(matic_data)) + " and " + str(max(matic_data))

                              )
        # embed.set_image(url="attachment://testplot.png")
        # Sends the embedded message from the variable
        await message.channel.send(embed=embed, file=file)

    # looks for the message "!mgas"
    if message.content == "!mgas":
        # Requests a response from the API, and makes it into a variable
        response = requests.get(
            "https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=P8HUN8TU54KBQ7YNZPU7XGAI1KJ5IVEV9N")
        # Sets variable "gas" to 'results' from the list provided by the API response
        gas = response.json()['result']
        # sets variable "**_gas" to it's respective value in the "gas" variable.
        m_gas = round(float(gas['FastGasPrice'])), round(float(gas['ProposeGasPrice'])), round(
            float(gas['SafeGasPrice']))
        # Creates an embedded message inside a variable.
        embed = discord.Embed(colour=0x6A0DAD, title="__*Current MATIC Gas*__")
        embed.add_field(name="**Fast :banana: |  15 Seconds**  ", value=str(m_gas[0]) + " Gwei", inline=False)
        embed.add_field(name="**Moderate :orangutan: |  30 Seconds** ", value=str(m_gas[1]) + " Gwei", inline=False)
        embed.add_field(name="**Slow :see_no_evil: |  1 minute +** ", value=str(m_gas[2]) + " Gwei", inline=False)
        # Sets the thumbnail image
        embed.set_thumbnail(url='https://images.exchangerates.org.uk/uploads/polygon-1.jpg')
        embed.set_footer(text="Data grabbed in real time from Polygonscan."
                              "\n!gashelp for a list of commands")
        # Sends the embedded message
        await message.channel.send(embed=embed)

    if message.content == "!egas":
        response_eth = requests.get(
            "https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=T663YBZDIEV5KAK2T84BFNRS93B4UJPHVJ")
        eth_gas = response_eth.json()['result']
        e_gas = int(eth_gas['FastGasPrice']), int(eth_gas['ProposeGasPrice']), int(eth_gas['SafeGasPrice'])
        embed = discord.Embed(colour=0x0000FF, title="__*Current ETH Gas*__")
        embed.add_field(name="**Fast :banana: |  30 Seconds**  ", value=str(e_gas[0]) + " Gwei", inline=False)
        embed.add_field(name="**Moderate :orangutan: | 3 Minutes** ", value=str(e_gas[1]) + " Gwei", inline=False)
        embed.add_field(name="**Slow :see_no_evil: |  10 Minutes** ", value=str(e_gas[2]) + " Gwei", inline=False)
        embed.set_thumbnail(url='https://crypto-money.io/wp-content/uploads/2019/10/Ethereum.jpg')
        embed.set_footer(text="Data grabbed in real time from Etherscan.\n"
                              "!gashelp for a list of commands")
        await message.channel.send(embed=embed)

    if message.content == "!startactivity":
        activity_loop.start()
        print("Starting the Gas Activity loop.")

# defines a loop called activity_loop for every 14 seconds
@tasks.loop(seconds=10, reconnect=True)
async def activity_loop():
    # defines the matic_loop to set the activity
    async def matic_loop():
        resp = requests.post("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=A5R243GPHH3P5V5KC67SGJ7QHHFU2BJBXZ") #Second API key to avoid overloading, Testing Key: 1BUE342DTEZCG251WXSFTK4QM45ZZ7W2J5 Active Key: A5R243GPHH3P5V5KC67SGJ7QHHFU2BJBXZ
        gs = resp.json()['result']
        m_gs = int(round(float(gs['FastGasPrice']))), int(round(float(gs['ProposeGasPrice']))), int(round(float(gs['SafeGasPrice'])))
        # Sets presence as MATIC 'FastGasPrice' | 'ProposeGasPrice' | 'SafeGasPrice
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name="MATIC 🍌" + str(m_gs[0]) + " | " + str(m_gs[1]) + " | " + str(m_gs[2])))

    # launches the matic_loop as defined above
    await matic_loop()
    # Waits 7 seconds before starting the next action
    await asyncio.sleep(5)

    # defines the eth loop to set the activity

    async def eth_loop():
        resp_eth = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=VASE6Z47G6NWVKGWT9FSGEQ5V186H7C6KN") #Second API key to avoid overloading, Testing key : 8QBXWKRM63JYX1H25Z5IG5UK1X92R5M5RR Active key: VASE6Z47G6NWVKGWT9FSGEQ5V186H7C6KN 
        eth_gs = resp_eth.json()['result']
        e_gs = int(eth_gs['FastGasPrice']), int(eth_gs['ProposeGasPrice']), int(eth_gs['SafeGasPrice'])
        # Sets presence as ETH 'FastGasPrice' | 'ProposeGasPrice' | 'SafeGasPrice
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                            name="ETH 🦍" + str(e_gs[0]) + " | " + str(e_gs[1]) + " | " + str(e_gs[2])))

    # launches the eth_loop as defined above after waiting 5 seconds
    await eth_loop()


bot.run(DISCORD_TOKEN)