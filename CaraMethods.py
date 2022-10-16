import os
import random
from time import sleep
import CaraBot as Bot
newline = "\n"




# 
#  ---------- @EVERYONE METHODS ----------
#  Commands anyone can execute
# 

# Displays All commands available to the user ()
# Arguments:
    # Channel channel, output channel
    # Boolean userIsMod, determines extra output
async def helpMsg(channel, userIsMod):
    helpMsg = (
        "\n**CaraBot Commands**\n"+
        f"Command prefix: {Bot.botPrefix}"
        "\n\n"+
        "• Help: This command! Shows all available commands and their descriptions\n"+
        f"• Spam: Only usable in <#{Bot.spamChannel}>. Sends pictures of cats every few seconds")
    # Only displays if user is mod
    if userIsMod:
        helpMsg += (
            "\n\nMOD COMMANDS"+
            "• Scrape: Runs through the past 10,000 messages in the active channel and downloads all images to an Imgur album for use with the Spam command"+
            "• SpamInterval [seconds]: Changes the interval at which images are sent using the Spam command"+
            "• ChangePrefix [newPrefix]: Changes the bot's command prefix"
        )
    await channel.send(helpMsg)

# Randomizes Imgur album, then sends images at a given interval
# Arguments:
    # Channel channel, output channel
async def spam(channel):
    if channel.id != Bot.spamChannel:
        await channel.send(f"You can only use this command in <#{Bot.spamChannel}>")
        return
    album = retrieveAlbumLinks()
    random.shuffle(album)
    for img in album:
        await channel.send(img)
        sleep(Bot.spamInterval)




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
    if not userIsMod:
        await channel.send("Sorry, you don't have permission to use that command")
        return
    await channel.send("Starting scrape...")
    async for m in channel.history(limit=10000):
        if (m.author.id != Bot.botUserID):
            for a in m.attachments:
                print (a.content_type)
                if a.content_type in ('image/jpeg', 'image/jpg', 'image/png'):
                    filename = "images/" +a.filename
                    await a.save(fp="images/"+a.filename)
                    Bot.imgClient.upload_from_path(path="images/"+a.filename, config={'album':Bot.ALBUMID}, anon=False)
                    os.remove(filename)
    await channel.send(author.mention + "Scraping Complete!")

# Changes the interval of spam()
# Arguments: 
    # Channel channel, output channel
    # String arg, interval in seconds
    # Boolean userIsMod, user allowance
async def spamInterval(channel, arg, userIsMod):
    if not userIsMod:
        await channel.send("Sorry, you don't have permission to use that command")
        return
    try:
        arg = int(arg)
        if arg>120 or arg <10:
            raise ValueError
        Bot.spamInterval = arg
        await channel.send(f"New spam interval set to {arg} seconds")
    except ValueError as e:
        await channel.send("The argument for that command needs to be a number between 10 and 120")
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
    Bot.botPrefix = message.content[2:].split(" ")[1]
    await channel.send(f"New command prefix set to {Bot.botPrefix}")




# 
#  ---------- HELPER METHODS ----------
#  Methods only utilized by other methods
# 

# Helper function for spam(), Generates list of all image links from imgur album
def retrieveAlbumLinks():
    linkList = []
    items = Bot.imgClient.get_album_images(Bot.ALBUMID)
    for item in items:
        linkList.append(item.link)
    return linkList

