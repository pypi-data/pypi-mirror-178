import discord
from discord.ext import commands


def getName(user: discord.User):
    return user.name


def getDescriminator(user: discord.User):
    return user.discriminator


def getCreationDate(user: discord.User):
    return user.created_at


def getID(user: discord.User):
    return user.id

def getMention(user: discord.User):
    return user.mention
