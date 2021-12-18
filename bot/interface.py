import typing
import discord
import os
from discord import voice_client
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import sleep_until
import rng
from gtts import gTTS
from discord_slash import SlashCommand, SlashContext
#import rolling
import dad.interface
import cogExample.cogTest
import gameList.interface
import cogDice.cogDice
import heck.interface
import magic8.interface
import smartBot.interface
import slashbot


import voice.interface
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('?'), description='GU\'s experimental discord ')
slash = SlashCommand(client, override_type=True, sync_commands=True)

client.add_cog(smartBot.interface.smartBot(client))
client.add_cog(dad.interface.Dad(client))
client.add_cog(cogExample.cogTest.Greetings(client))
client.add_cog(gameList.interface.GameList(client))
client.add_cog(cogDice.cogDice.Dice(client))
client.add_cog(heck.interface.Heck(client))
client.add_cog(magic8.interface.Magic8(client))
client.add_cog(voice.interface.Voice(client))
client.add_cog(slashbot.Slash(client))

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
async def hello(ctx): 
    print("hello")
    await ctx.send("hello")

#TODO: Repeat unable to voice
# join when john joins and calls him nerd
#https://gtts.readthedocs.io/en/latest/module.html#module-gtts.tts
#https://www.youtube.com/watch?v=ml-5tXRmmFk&ab_channel=RoboticNation



@client.command(pass_context=True)
async def say(ctx: commands.Context, channel :typing.Optional[discord.TextChannel] = None, *, words : str):
    '''For making the bot come out of the closet for you.
    Format is !say (channelid) (message)'''
    if channel == None:
        await ctx.send("Invalid channel")
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

@client.event
async def on_message(message: discord.Message):
    print(str(message.channel.id) + ": " + str(message.channel.name) + ": " + str(message.author.name) + ": " + str(message.content)) #print(message) gives lots of useless garbage, now streamlined
    context = await client.get_context(message)
    if context.command != None:
        await client.process_commands(message) #ensure doesn't mess with other commands

# @slash.slash(name="test2", description="non-cog slashing", guild_ids=[366792929865498634])
# async def _test(ctx: SlashContext):
#     embed = discord.Embed(title="embed test not!!!")
#     await ctx.send(content="test", embeds=[embed])

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

# @client.command(pass_context=True)
# async def dadJoke(ctx):
#     '''For getting a really bad joke.'''
#     await ctx.send(dad.getDadJoke())

# @client.command(pass_context=True)
# async def turnDaddyOn(ctx):
#     '''For turning daddy on'''
#     dad.turnDaddyOn()
#     await ctx.send("Thank you for turning daddy on ;)")

# @client.command(pass_context=True)
# async def turnDaddyOff(ctx):
#     '''For turning daddy off :('''
#     dad.turnDaddyOff()
#     await ctx.send("Daddy has been turned off :(")

#TODO: add these to their modules
# @client.event
# async def on_message_edit(before, after): #this is useful i promise
#     if not after.author.bot:
#         #START DAD
#         toDad = dad.daddy(after.content)
#         if(toDad[0]):
#             await after.channel.send(toDad[1])
#         #END DAD
#         toHeck = heck.logic.heckin(after.content)
#         if(toHeck[0]):
#             await after.channel.send(toHeck[1])
#     print(str(before.channel.id) + ": " + str(before.channel.name) + ": " + str(before.author.name) + ": " + str(before.content) + " --->>>> " + str(after.content))
