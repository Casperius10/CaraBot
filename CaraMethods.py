import asyncio
import os
import random
from time import sleep
import Vars as c
newline = "\n"
import imgurpython

# 
#  ---------- @EVERYONE METHODS ----------
#  Commands anyone can execute
# 

# Displays All commands available to the user
# Arguments:
    # Channel channel, output channel
    # Boolean userIsMod, determines extra output
async def helpMsg(channel, userIsMod):
    helpMsg = (
        "\n**CaraBot Commands**\n"+
        f"Command prefix: {c.botPrefix}"
        "\n\n"+
        "• Help: This command! Shows all available commands and their descriptions\n"+
        f"• Spam: Only usable in <#{c.spamChannel}>. Sends pictures of cats every few seconds")
    # Only displays if user is mod
    if userIsMod:
        helpMsg += (
            "\n\nMOD COMMANDS"+
            "• Scrape: Runs through the past 10,000 messages in the active channel and downloads all images to an Imgur album for use with the Spam command\n"+
            "• SpamInterval [seconds]: Changes the interval at which images are sent using the Spam command\n"+
            "• ChangePrefix [newPrefix]: Changes the bot's command prefix"
        )
    await channel.send(helpMsg)

# Randomizes Imgur album, then sends images at a given interval
# Arguments:
    # Channel channel, output channel
async def spam(channel):
    if channel.id != c.spamChannel:
        await channel.send(f"You can only use this command in <#{c.spamChannel}>")
        return
    album = retrieveAlbumLinks()
    random.shuffle(album)
    for img in album:
        await channel.send(img)
        sleep(c.spamInterval)
    await channel.send("End of album")




# 
#  ---------- MOD-ONLY METHODS ----------
#  Commands only mods can execute
#  (Determined by existence of 'manage messages' permissions)
# 

# Scrapes the channel for all image attachments and loads them to an imgur album
# Arguments:
    # Channel channel, output channel
    # Boolean userIsMod, determines whether function will execute
    # Member author, for pinging when complete
async def scrape(channel, userIsMod, author):
    try:
        counter = 1
        if not userIsMod:
            await channel.send("Sorry, you don't have permission to use that command")
            return
        await channel.send("Starting scrape...")
        async for m in channel.history(limit=10000):
            if counter >= 50:
                print("upload limit reached. Pausing for one hour...")
                await asyncio.sleep(3600)
                counter = 0
            if (m.author.id != c.botUserID):
                for a in m.attachments:
                    await imgurUpload(a)
                    counter+=1
                
        await channel.send(author.mention + " Scraping Complete!")
    except imgurpython.helpers.error.ImgurClientRateLimitError as e:
        print("upload limit exceeded. Quitting scrape.")
        os.remove("images/"+a.filename)


# Changes the interval of spam()
# Arguments: 
    # Channel channel, output channel
    # String arg, interval in seconds
    # Boolean userIsMod, user allowance
async def spamInterval(channel, userIsMod, arg):
    if not userIsMod:
        await channel.send("Sorry, you don't have permission to use that command")
        return
    if arg == None:
        await channel.send(f"The current spam interval is {c.spamInterval}")
        return
    try:
        arg = int(arg)
        if arg>120 or arg <3:
            raise ValueError
        c.spamInterval = arg
        await channel.send(f"New spam interval set to {arg} seconds")
    except ValueError as e:
        await channel.send("The argument for that command needs to be a number of seconds between 3 and 120")
        return

# Changes the bot's prefix
# Arguments:
    # Channel channel, output channel
    # Boolean userIsMod, user allowance
async def changePrefix(channel, userIsMod, message):
    if not userIsMod:
        await channel.send("Sorry, you don't have permission to use that command")
        return
    if len(message.split(" ")) > 2:
        await channel.send("Please do not include any spaces in the new prefix")
        return
    c.botPrefix = message.content[2:].split(" ")[1]
    await channel.send(f"New command prefix set to {c.botPrefix}")




# 
#  ---------- HELPER METHODS ----------
#  Methods only utilized by other methods
# 

# Helper function for spam(), Generates list of all image links from imgur album
def retrieveAlbumLinks():
    linkList = []
    items = c.imgClient.get_album_images(c.ALBUMID)
    for item in items:
        linkList.append(item.link)
    return linkList

async def imgurUpload(a):
    if a.content_type in ('image/jpeg', 'image/jpg', 'image/png'):
        await a.save(fp="images/"+a.filename)
        print(f"uploading {a.filename}")
        c.imgClient.upload_from_path(path="images/"+a.filename, config={'album':c.ALBUMID}, anon=False)
        os.remove("images/"+a.filename)
