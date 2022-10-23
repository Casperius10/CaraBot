import os
import CaraMethods as Met
import Vars as c

# Reacts to all messages in all channels
@c.discClient.event
async def on_message(message):
    channel = message.channel
    userIsMod = True if message.channel.permissions_for(message.author).manage_messages else False
    if message.author.id == c.botUserID:
        pass
    elif message.content[:2] != c.botPrefix and message.channel.id ==c.spamChannel and message.attachments:
        for a in message.attachments:
            pass
    elif message.content[:2] == c.botPrefix:
        msg = message.content.lower()[2:].split(" ")[0]
        try:
            arg = message.content[2:].split(" ")[1]
        except:
            arg=None
        match msg:
            case "help":
                await Met.helpMsg(channel, userIsMod)
            case "spam":
                await Met.spam(channel)
            case "scrape":
                await Met.scrape(channel, userIsMod, message.author)
            case "spaminterval":
                await Met.spamInterval(channel, userIsMod, arg)
            case "changeprefix":
                await Met.changePrefix(channel, userIsMod, message[2:].content)
            case _:
                await channel.send("Unrecognized Command")

os.system('cls' if os.name == 'nt' else 'clear')
c.discClient.run(c.botToken)