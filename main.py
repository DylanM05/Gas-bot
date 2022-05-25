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

# REQUESTS THE API INFORMATION UPON COMMAND
response = requests.get("https://api.polygonscan.com/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken")
# Sets variable "gas" to 'results' from the list provided by the API response
gas = response.json()['result']
# sets variable "**_gas" to it's respective value in the "gas" variable.
fast_gas = (gas['FastGasPrice'])
moderate_gas = (gas['ProposeGasPrice'])
slow_gas = (gas['SafeGasPrice'])


# Event Listener for when the bot has switched from offline to online.
@bot.event
async def on_ready():
	print("The bot has started.")
	print(gas)


# Event listener for when a new message is sent to a channel.
@bot.event
async def on_message(message):
	# Checks if the message that was sent is equal to "!mgas".
	if message.content == "!mgas":
		# Sends back a message to the channel.
		# Refers back to the previous variables to create a message that displays gwei.
		await message.channel.send("___Current MATIC Gas in Gwei___ \n"
										"**Fast | 15 Seconds:** " + "___***" + fast_gas + "***___ \n"
										"**Moderate | 30 Seconds:** " + "___***" + moderate_gas + "***___ \n"
										"**Slow | 1 minute +:** " + "___***" + slow_gas + "***___")

# Executes the bot with the specified token.
bot.run("OTc3MzY2OTg2NzQyOTY4Mzgw.GXW4sl.oLqApr83ObBydATbbugXsUnfyBa0LWdV1gCnJQ")
