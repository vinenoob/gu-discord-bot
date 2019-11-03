import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import rng
import rolling
import dad

client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='GU\'s experimental discord bot.')

@client.event
async def on_ready():
    print("Hey Nerds")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("___________________________")

@client.command(pass_context = True)
async def randomNumber(ctx, firstNum :int):
    await ctx.send(rng.randomNumber(firstNum,10))

@client.command(pass_context=True)
async def roll(ctx, *, QuantityDSides :str):
    '''Rolls dice. Format is !roll xdy'''
    await ctx.send(rolling.roll(QuantityDSides))

@client.command(pass_context = True)
async def hello(ctx): #activated by "?helloworld"
    print("hello")
    await ctx.send("hello")

@client.command(pass_context=True)
async def say(ctx, channelid :str, *, words : str):
    '''For making the bot come out of the closet for you.
    Format is !say (channelid) (message)'''
    channel = None
    if "<#" in channelid: #see if the channel is a channel mention, ie "#but-stuff"
        channelid = channelid[channelid.find("<#") + len("<#"):] #erase the first bit
        channelid = channelid[:channelid.find(">")] #erase the last bit
    try:
        channel = client.get_channel(int(channelid))
    except:
        print("Inavlid channel")
        await ctx.send("Inavlid channel")
        return
    await channel.send(str(words))

@client.command(pass_context=True)
async def ping(ctx):
    '''For shooting the bot and waiting for a response.'''
    channel = ctx.message.channel
    await channel.send("Ow.")

@client.command(pass_context=True)
async def dadJoke(ctx):
    '''For getting a really bad joke.'''
    await ctx.send(dad.getDadJoke())

@client.event
async def on_message(message):
    if not message.author.bot:
        #START DAD
        toDad = dad.daddy(message.content)
        if(toDad[0]):
            await message.channel.send(toDad[1])
        #END DAD
    print(str(message.channel.id) + ": " + str(message.channel.name) + ": " + str(message.author.name) + ": " + str(message.content)) #print(message) gives lots of useless garbage, now streamlined
    await client.process_commands(message) #ensure doesn't mess with other commands

@client.event
async def on_message_edit(before, after): #this is useful i promise
    print(str(before.channel.id) + ": " + str(before.channel.name) + ": " + str(before.author.name) + ": " + str(before.content) + " --->>>> " + str(after.content))

keyFile = open("key.txt", "r")
key = keyFile.read()
keyFile.close()
client.run(key)