import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands

bot_prefix = "?"
client = commands.Bot(command_prefix = bot_prefix)

@client.event
async def on_ready():
    print("Bot")

@client.command()
async def helloworld(): #activated by "?helloworld"
    print("hello world")

@client.event
async def on_message(message):
    print(message)
    await client.process_commands(message) #ensure doesn't mess with other commands


os.chdir("..")
keyFile = open("gu-discordbot\\DONTSHOW\\key.txt", "r")
key = keyFile.read()
keyFile.close()
client.run(key)