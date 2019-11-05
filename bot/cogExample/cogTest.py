import discord
from cogExample import cogLogic #this shows an error for me but works -Jonathan
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cogTest")
    async def cogTest(self, ctx):
        await ctx.send(cogLogic.hi())
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        print("Cog Example Listening")