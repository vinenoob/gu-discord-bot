import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="cogTest")
    async def cogTest(self, ctx):
        await ctx.send("Cog test successful")