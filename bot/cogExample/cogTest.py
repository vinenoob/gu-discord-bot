import discord
#import bot.cogExample.cogLogic #this shows an error for me but works -Jonathan
import cogExample.cogLogic as cogLogic
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cogTest")
    async def cogTest(self, ctx):
        await ctx.send(cogLogic.hi())
    
    @commands.Cog.listener()
    async def on_message(self, message):
        pass
        # print("Cog Example Listening")