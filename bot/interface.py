import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import rng

startup_extentions = ["test"]

bot_prefix = "?"
client = commands.Bot(command_prefix = bot_prefix)

@client.event
async def on_ready():
    print("Bot")

@client.command(pass_context = True)
async def randomNumber(ctx, firstNum :int): #activated by "?helloworld"
    await ctx.send(rng.randomNumber(firstNum,10))

@client.command(pass_context = True)
async def hello(ctx): #activated by "?helloworld"
    print("hello")
    await ctx.send("hello")

@client.event
async def on_message(message):
    print(message)
    await client.process_commands(message) #ensure doesn't mess with other commands

os.chdir("..")
keyFile = open("gu-discordbot\\DONTSHOW\\key.txt", "r")
key = keyFile.read()
keyFile.close()
client.run(key)