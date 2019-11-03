import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import rng

startup_extentions = ["test"]

client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='GU\'s experimental discord bot.')

#import roll

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
    print(str(message.channel.id) + ": " + str(message.channel.name) + ": " + str(message.author.name) + ": " + str(message.content)) #print(message) gives lots of useless garbage, now streamlined
    await client.process_commands(message) #ensure doesn't mess with other commands

@client.event
async def on_message_edit(before, after): #this is usefull i promise
    print(str(before.channel.id) + ": " + str(before.channel.name) + ": " + str(before.author.name) + ": " + str(before.content) + " --->>>> " + str(after.content))

keyFile = open("key.txt", "r")
key = keyFile.read()
keyFile.close()
client.run(key)