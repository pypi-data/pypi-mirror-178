import discord
from discord.ext import commands


def Bot(prefix: str, case_insensitive: bool = False, intents: tuple = ("default",), activity=None, help_command=None):
    if "all" in intents:
        intent = discord.Intents.all()
    elif "default" in intents:
        intent = discord.Intents.default()
    else:
        intent = discord.Intents.default()
        if "message" in intents:
            intent.message_content = True
        if "members" in intents:
            intent.members = True
        if "presences" in intents:
            intent.presences = True

    if activity is None:
        clients = commands.Bot(command_prefix=prefix, case_insensitive=case_insensitive, intents=intent, help_command=help_command)
    else:
        clients = commands.Bot(command_prefix=prefix, case_insensitive=case_insensitive, intents=intent, activity=activity, help_command=help_command)
    return clients