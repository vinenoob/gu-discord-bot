# cog.py
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from dad import logic

class Slash(commands.Cog):
    def __init__(self, bot):
        print("Slash Initiated")
        self.bot = bot

    @cog_ext.cog_slash(name="test", description="cog slashing", guild_ids=[366792929865498634, 160907545018499072])
    async def _test(self, ctx: SlashContext):
        embed = discord.Embed(title="yoooooo", description=logic.getDadJoke())
        await ctx.send(content="test", embeds=[embed])

def setup(bot):
    bot.add_cog(Slash(bot))