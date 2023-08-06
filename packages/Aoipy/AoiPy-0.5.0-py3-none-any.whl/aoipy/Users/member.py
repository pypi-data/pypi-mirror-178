import discord


def getNick(member: discord.Member):
    return member.display_name


def getRoles(member: discord.Member):
    return member.roles


def getJoinDate(member: discord.Member):
    return member.joined_at


def sendMessage(user: discord.User, message, embed: bool = False):
    if embed:
        user.send(embed=message)
    else:
        user.send(message)