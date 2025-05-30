from discord.ext import commands
from discord.member import Member
from discord.ext.commands import AutoShardedBot
from discord import Activity, ActivityType

class Poptarts(commands.Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        print("Poptarts Initiated")

    @commands.command(name="poptart", aliases=["poptarts"])
    async def poptart(self, ctx):
        '''Get a poptart'''
        await ctx.send("https://www.youtube.com/watch?v=1Q9Ug2qZ2dI")
    
    # print when a user is updates their status
    @commands.Cog.listener()
    async def on_presence_update(self, before: Member, after: Member):
        if before.bot or after.bot:
            return
        
        if before.id != 287697603607658496 and before.id != 160907412205862913:
            # not ben or jonathan
            return
        
        if before.activity == None or after.activity == None:
            return
        if before.activity != after.activity:
            before_activity = before.activity.name if before.activities else None
            after_activity = after.activity.name if after.activities else None
            # check if they both have a number at the beginning
            before_activity_split = before_activity.split(" ")
            after_activity_split = after_activity.split(" ")
            if len(before_activity_split) == 0 or len(after_activity_split) == 0:
                return
            if not before_activity_split[0].isnumeric():
                return
            if not after_activity_split[0].isnumeric():
                return
            after_number = int(after_activity_split[0])
            await self.bot.change_presence(activity=Activity(name=f"{384-after_number} poptarts being eaten", type=ActivityType.listening))
            # from discord import Game
            # from discord import Status
            # activity = Game(name="with someone else!")
            # await self.bot.change_presence(status=Status.online, activity=activity)
            print(f"{before.name} changed from {before_activity} to {after_activity}")