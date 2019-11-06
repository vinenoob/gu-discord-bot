from discord.ext import commands
from gameList import logic

class GameList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addGame")
    async def addGame(self, ctx, *,game :str):
        '''Add a game to your game list'''
        logic.addGame(ctx.author.name,game)
        await ctx.send("Game added!")

    @commands.command(name="addGames")
    async def addGames(self, ctx, *, games:str):
        '''Add some games to your game list'''
        for game in games.split(", "):
            logic.addGame(ctx.author.name,game)
        await ctx.send("Games added!")
    
    # @commands.Cog.listener()
    # async def on_message(self, ctx):
    #     print("Cog Example Listening")
    
    @commands.command(name="gameList")
    async def gameList(self, ctx, id :str):
        '''Find out what games someone has on their list'''
        if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
            id = id[id.find("<@!") + len("<@!"):] #erase the first bit
            id = id[:id.find(">")] #erase the last bit
        person = self.bot.get_user(int(id))
        games = logic.gameList(person.name)
        await ctx.send(games)
    
    @commands.command(name="commonGames")
    async def commonGames(self, ctx, *, people :str):
        '''Find common games among multiple peoples games list'''
        peopleList = people.split(",")
        nameList = []
        for id in peopleList:
            if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
                id = id[id.find("<@!") + len("<@!"):] #erase the first bit
                id = id[:id.find(">")] #erase the last bit
            person = self.bot.get_user(int(id))
            nameList.append(person.name)
        await ctx.send(logic.commonGames(nameList))