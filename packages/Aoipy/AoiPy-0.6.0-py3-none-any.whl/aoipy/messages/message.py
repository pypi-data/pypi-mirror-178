import discord


async def deleteMessage(message: discord.Message, delay: int or float = None):
    if delay is None:
        return await message.delete()
    else:
        return await message.delete(delay=delay)


def getMessageID(message: discord.Message):
    return message.id


def getMessageContent(message: discord.Message):
    return message.content


def getMessageChannelName(message: discord.Message):
    return message.channel.name


def getMessageChannelID(message: discord.Message):
    return message.channel.id

