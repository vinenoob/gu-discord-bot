from math import log
import magic8.logic as logic
import discord
from discord.ext import commands

class Magic8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Magic8 Initiated")
    
    @commands.command(name="magic8")
    async def magic8(self, ctx):
        '''Magic8 ball'''
        response = logic.magic8()
        await ctx.send(response)
