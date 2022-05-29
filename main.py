# Import discord.py. Allows Access to discord's API
import discord
# Import the OS module.
import os
# Import requests for APIs
import requests
# Import LOAD_DOTENV function from DOTENV MODULE.
from dotenv import load_dotenv

# Loads The .ENV file that resides on the same level as the script.
load_dotenv()

# Grab the API token from the .ENV file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Gets the client object from DISCORD.PY. Client is synonymous with bot.
bot = discord.Client()


@bot.event
async def on_ready():
	print("Bot is running")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="bananas grow", afk=False))


# Event listener for when a new message is sent to a channel.
@bot.event
async def on_message(message):
	# Checks if the message that was sent is equal to "!commands"
	if message.content == "!commands":
		# makes a variable with an embedded message
		embed = discord.Embed(title="Commands", description="**!gas - Retrieves ETH gas cost \n "
															"\n !mgas - Retrieves MATIC gas cost**")
		# Sends the embedded message from the variable
		await message.channel.send(embed=embed)
		# looks for the message "!mgas
	if message.content == "!mgas":
		# Requests a response from the API, and makes it into a variable
		response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken")
		# Sets variable "gas" to 'results' from the list provided by the API response
		gas = response.json()['result']
		# sets variable "**_gas" to it's respective value in the "gas" variable.
		fast_gas = (gas['FastGasPrice'])
		moderate_gas = (gas['ProposeGasPrice'])
		slow_gas = (gas['SafeGasPrice'])
		# Creates an embedded message inside a variable.
		embed = discord.Embed(title="__*Current MATIC Gas in Gwei*__")
		embed.add_field(name="**Fast :banana: |  15 Seconds**  ", value=fast_gas + " Gwei", inline=False)
		embed.add_field(name="**Moderate :orangutan: |  30 Seconds** ", value=moderate_gas + " Gwei", inline=False)
		embed.add_field(name="**Slow :see_no_evil: |  1 minute +** ", value=slow_gas + " Gwei", inline=False)
		# Sets the thumbnail image
		embed.set_thumbnail(url='https://images.exchangerates.org.uk/uploads/polygon-1.jpg')
		embed.set_footer(text="Data grabbed in real time from Polygonscan.")
		# Sends the embedded message
		await message.channel.send(embed=embed)

	if message.content == "!gas":
		# REQUESTS THE API INFORMATION UPON COMMAND
		response_eth = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken")
		# Sets variable "gas" to 'results' from the list provided by the API response
		eth_gas = response_eth.json()['result']
		# sets variable "**_eth_gas" to it's respective value in the "eth_gas" variable.
		fast_eth_gas = (eth_gas['FastGasPrice'])
		moderate_eth_gas = (eth_gas['ProposeGasPrice'])
		slow_eth_gas = (eth_gas['SafeGasPrice'])
		# Creates an embedded message inside a variable.
		embed = discord.Embed(title="__*Current ETH Gas in Gwei*__")
		embed.add_field(name="**Fast :banana: |  30 Seconds**  ", value=fast_eth_gas + " Gwei", inline=False)
		embed.add_field(name="**Moderate :orangutan: | 3 Minutes** ", value=moderate_eth_gas + " Gwei", inline=False)
		embed.add_field(name="**Slow :see_no_evil: |  10 Minutes** ", value=slow_eth_gas + " Gwei", inline=False)
		embed.set_thumbnail(url='https://crypto-money.io/wp-content/uploads/2019/10/Ethereum.jpg')
		embed.set_footer(text="Data grabbed in real time from Etherscan.")
		# Sends the embedded message
		await message.channel.send(embed=embed)

bot.run("OTczMzQ1MzIxMDIxMjE4ODM3.GHSJv5.LoeDJDxUXTrNE35BrWpWUnD98YYKBgv3nSxCsk")
