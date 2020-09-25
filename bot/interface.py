import discord
import os
from discord.ext.commands import Bot
from discord.ext import commands
import rng
#import rolling
import dad
import cogExample.cogTest
import gameList.interface
import cogDice.cogDice
#small change for checking stuff
client = commands.Bot(command_prefix=commands.when_mentioned_or('?'), description='GU\'s experimental discord ')

client.add_cog(cogExample.cogTest.Greetings(client))
client.add_cog(gameList.interface.GameList(client))
client.add_cog(cogDice.cogDice.Dice(client))

@client.event
async def on_ready():
    print("Hey Nerds")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))
    print("___________________________")

@client.command(pass_context = True)
async def randomNumber(ctx, firstNum :int, secondNum :int):
    '''Generate random number between x and y'''
    try:
        num = rng.randomNumber(firstNum,secondNum)
        await ctx.send(num)
    except:
        await ctx.send("Failed")

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
    channel = client.get_channel(int(channelid))
    if channel is None: #see if a channel was successfully found
        print("Inavlid channel")
        await ctx.send("Inavlid channel")
        return
    try:
        await channel.send(str(words))
    except discord.Forbidden:
        err = "Can't send there. Missing perms?"
        print(err)
        await ctx.send(err)

@client.command(pass_context=True)
async def ping(ctx):
    '''For shooting the bot and waiting for a response.'''
    channel = ctx.message.channel
    await channel.send("Ow.")

@client.command(pass_context=True)
async def dadJoke(ctx):
    '''For getting a really bad joke.'''
    await ctx.send(dad.getDadJoke())

@client.command(pass_context=True)
async def turnDaddyOn(ctx):
    '''For turning daddy on'''
    dad.turnDaddyOn()
    await ctx.send("Thank you for turning daddy on ;)")

@client.command(pass_context=True)
async def turnDaddyOff(ctx):
    '''For turning daddy off :('''
    dad.turnDaddyOff()
    await ctx.send("Daddy has been turned off :(")

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
    if not after.author.bot:
        #START DAD
        toDad = dad.daddy(after.content)
        if(toDad[0]):
            await after.channel.send(toDad[1])
        #END DAD
    print(str(before.channel.id) + ": " + str(before.channel.name) + ": " + str(before.author.name) + ": " + str(before.content) + " --->>>> " + str(after.content))

def start_bot():
    key = ""
    try:
        key = os.environ['key']
    except:
        keyFile = open("key.txt", "r")
        key = keyFile.read()
        key = key.replace("\n", "")
        keyFile.close()
        
    client.run(key)

if __name__ == '__main__':
    start_bot()