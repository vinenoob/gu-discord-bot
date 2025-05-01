import cogs.heck.logic as logic
from discord.ext import commands

class Heck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Heck Initiated")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            do, response = logic.heckin(message.content)
            if do:
                await message.channel.send(response)

            do, response = logic.your(message.content)
            if do:
                await message.channel.send(response)