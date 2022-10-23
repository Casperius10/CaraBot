import myCreds
import discord
import myCreds
from imgurpython import ImgurClient

# Mutable vars
spamChannel = 1030525792280653855
spamInterval = 10
botPrefix = "/\\"

# Imgur client setup
ALBUMID = "HndnqTX"
client_id = myCreds.client_id
client_secret = myCreds.client_secret
access_token = myCreds.access_token
refresh_token = myCreds.refresh_token
imgClient = ImgurClient(client_id, client_secret, refresh_token)
imgClient.set_user_auth(access_token, refresh_token)

# Discord Client Setup
# Bot invite link: https://discordapp.com/api/oauth2/authorize?client_id=1030552352442286111&permissions=8&scope=bot
intents = discord.Intents.all()
discClient = discord.Client(intents = intents)
guild = discord.Guild
botUserID = 1030552352442286111
botToken = myCreds.botToken