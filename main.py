# Import discord.py. Allows Access to discord's API
import discord
from discord.ext import tasks
import os
# Import requests for APIs
import requests
# Import LOAD_DOTENV function from DOTENV MODULE.
from dotenv import load_dotenv
# Loads The .ENV file that resides on the same level as the script.
load_dotenv("bot.env")
# Grab the API token from the .ENV file.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
# Gets the client object from DISCORD.PY. Client is synonymous with bot.
bot = discord.Client()


@bot.event
async def on_ready():
	print("Bot is running")
	# starts the loops for the presence updater process.
	matic_loop.start()
	eth_loop.start()


# Event listener for when a new message is sent to a channel.
@bot.event
async def on_message(message):
	# Checks if the message that was sent is equal to "!commands"
	if message.content == "!commands":
		# makes a variable with an embedded message
		embed = discord.Embed(title="Commands", description="**!egas - Retrieves ETH gas cost \n "
															"\n !mgas - Retrieves MATIC gas cost**")
		# Sends the embedded message from the variable
		await message.channel.send(embed=embed)

		# looks for the message "!mgas
	if message.content == "!mgas":
		# Requests a response from the API, and makes it into a variable
		response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=P8HUN8TU54KBQ7YNZPU7XGAI1KJ5IVEV9N")
		# Sets variable "gas" to 'results' from the list provided by the API response
		gas = response.json()['result']
		# sets variable "**_gas" to it's respective value in the "gas" variable.
		m_gas = round(float(gas['FastGasPrice'])), round(float(gas['ProposeGasPrice'])), round(float(gas['SafeGasPrice']))
	#	moderate_gas = round(float(gas['ProposeGasPrice']))
	#	slow_gas = round(float(gas['SafeGasPrice']))
		# Creates an embedded message inside a variable.
		embed = discord.Embed(title="__*Current MATIC Gas*__")
		embed.add_field(name="**Fast :banana: |  15 Seconds**  ", value=str(m_gas[0]) + " Gwei", inline=False)
		embed.add_field(name="**Moderate :orangutan: |  30 Seconds** ", value=str(m_gas[1]) + " Gwei", inline=False)
		embed.add_field(name="**Slow :see_no_evil: |  1 minute +** ", value=str(m_gas[2]) + " Gwei", inline=False)
		# Sets the thumbnail image
		embed.set_thumbnail(url='https://images.exchangerates.org.uk/uploads/polygon-1.jpg')
		embed.set_footer(text="Data grabbed in real time from Polygonscan.")
		# Sends the embedded message
		await message.channel.send(embed=embed)

	if message.content == "!egas":
		response_eth = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=T663YBZDIEV5KAK2T84BFNRS93B4UJPHVJ")
		eth_gas = response_eth.json()['result']
		e_gas = int(eth_gas['FastGasPrice']), int(eth_gas['ProposeGasPrice']), int(eth_gas['SafeGasPrice'])
#		fast_eth_gas = eth_gas['FastGasPrice']
#		moderate_eth_gas = eth_gas['ProposeGasPrice']
#		slow_eth_gas = eth_gas['SafeGasPrice']
		embed = discord.Embed(title="__*Current ETH Gas*__")
		embed.add_field(name="**Fast :banana: |  30 Seconds**  ", value=str(e_gas[0]) + " Gwei", inline=False)
		embed.add_field(name="**Moderate :orangutan: | 3 Minutes** ", value=str(e_gas[1]) + " Gwei", inline=False)
		embed.add_field(name="**Slow :see_no_evil: |  10 Minutes** ", value=str(e_gas[2]) + " Gwei", inline=False)
		embed.set_thumbnail(url='https://crypto-money.io/wp-content/uploads/2019/10/Ethereum.jpg')
		embed.set_footer(text="Data grabbed in real time from Etherscan.")
		await message.channel.send(embed=embed)


# defines a loop for every 10 seconds
@tasks.loop(seconds=5)
async def matic_loop():
	resp = requests.post("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=P8HUN8TU54KBQ7YNZPU7XGAI1KJ5IVEV9N")
	gs = resp.json()['result']
	m_gs = round(float(gs['FastGasPrice'])), round(float(gs['ProposeGasPrice'])), round(float(gs['SafeGasPrice']))
#	fast_gs = round(float(gs['FastGasPrice']))
#	moderate_gs = round(float(gs['ProposeGasPrice']))
#	slow_gs = round(float(gs['SafeGasPrice']))
	# Sets presence as Matic 'fast_gs' | 'moderate_gs' | slow_gs
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="MATIC " + str(m_gs[0]) + " | " + str(m_gs[1]) + " | " + str(m_gs[2])))


# Defines a loop for every 20 seconds (alternating 10 seconds with the previous loop)
@tasks.loop(seconds=10)
async def eth_loop():
	resp_eth = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=T663YBZDIEV5KAK2T84BFNRS93B4UJPHVJ")
	eth_gs = resp_eth.json()['result']
	e_gs = int(eth_gs['FastGasPrice']), int(eth_gs['ProposeGasPrice']), int(eth_gs['SafeGasPrice'])
#	fast_e_gas = e_gas['FastGasPrice']
#	moderate_e_gas = e_gas['ProposeGasPrice']
#	slow_e_gas = e_gas['SafeGasPrice']
	# Sets presence as ETH 'fast_e_gas' | 'moderate_e_gas' | slow_e_gas
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ETH " + str(e_gs[0]) + " | " + str(e_gs[1]) + " | " + str(e_gs[2])))


bot.run(DISCORD_TOKEN)
