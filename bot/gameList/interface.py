from discord.ext import commands
from gameList import logic

class GameList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addGame")
    async def addGame(self, ctx, *,game :str):
        logic.addGame(ctx.author.name,game)
        await ctx.send("Game added!")
    
    # @commands.Cog.listener()
    # async def on_message(self, ctx):
    #     print("Cog Example Listening")
    
    @commands.command(name="gameList")
    async def gameList(self, ctx, id :str):
        if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
            id = id[id.find("<@!") + len("<@!"):] #erase the first bit
            id = id[:id.find(">")] #erase the last bit
        person = self.bot.get_user(int(id))
        games = logic.gameList(person.name)
        await ctx.send(games)
    
    @commands.command(name="commonGames")
    async def commonGames(self, ctx, *, people :str):
        peopleList = people.split(",")
        nameList = []
        for id in peopleList:
            if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
                id = id[id.find("<@!") + len("<@!"):] #erase the first bit
                id = id[:id.find(">")] #erase the last bit
            person = self.bot.get_user(int(id))
            nameList.append(person.name)
        await ctx.send(logic.commonGames(nameList))