import asyncio
from logging import log
import discord
from discord import message
from discord.ext.commands.core import command
import dad.logic as logic
from discord.ext import commands

class Dad(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dontWatch = [] #TODO: Implement
        print("Dad Initiated")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.author.name in self.dontWatch:
            toDad = logic.daddy(message.content)
            if(toDad[0]):
                await message.channel.send(toDad[1])
    
    @commands.command(name="dadJoke")
    async def dadJoke(self, ctx :commands.context.Context):
        '''Get a dad joke'''
        await ctx.trigger_typing()
        await ctx.send(logic.getDadJoke())
        

    @commands.command(name="turnDaddyOn")
    async def turnDaddyOn(self, ctx):
        '''Stops daddy from watching you'''
        logic.turnDaddyOn()
        await ctx.send("Daddy turned on ;)")
    
    @commands.command(name="turnDaddyOff")
    async def turnDaddyOff(self, ctx):
        '''Daddy watches you'''
        logic.turnDaddyOff()
        await ctx.send("Daddy has been forcibly turned off :(")