import discord
import heck.logic as logic
from discord.ext import commands

class Heck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dontWatch = []
        print("Heck Initiated")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and not message.author.name in self.dontWatch:
            toHeck = logic.heckin(message.content)
            if(toHeck[0]):
                await message.channel.send(toHeck[1])


    