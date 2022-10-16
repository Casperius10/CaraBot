import discord
from imgurpython import ImgurClient
import myCreds
import os
import CaraMethods as Met

# Mutable vars
spamChannel = "1030525792280653855"
spamInterval = 15
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
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
discClient = discord.Client(intents = intents)
guild = discord.Guild
botUserID = 1030552352442286111
botToken = myCreds.botToken

# Reacts to all messages in all channels
@discClient.event
async def on_message(message):
    channel = message.channel
    userIsMod = True if message.channel.permissions_for(message.author).manage_messages else False
    if message.author.id == botUserID or message.content[:2] != botPrefix:
        pass
    else:
        msg = message.content.lower()[2:].split(" ")[0]
        arg = message.content[2:].split(" ")[1]
        match msg:
            case "help":
                await Met.helpMsg(channel, userIsMod)

            case "spam":
                Met.spam(channel)

            case "scrape":
                await Met.scrape(channel, userIsMod, message.author)

            case "spaminterval":
                spamInterval(channel, arg)

            case "changeprefix":
                if userIsMod:
                    Met.changePrefix(channel, userIsMod, message[2:].content)

            case _:
                await channel.send("Unrecognized Command")
                
os.system('cls' if os.name == 'nt' else 'clear')
discClient.run(botToken)