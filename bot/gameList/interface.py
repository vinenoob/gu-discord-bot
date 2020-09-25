from discord.ext import commands
from discord import User
import gameList.logic as logic
import random
import typing
class GameList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="addGame")
    async def addGame(self, ctx, *,game :str):
        '''Add a game to your game list'''
        _, message = logic.addGame(ctx.author.name,game)
        await ctx.send(message)

    @commands.command(name="addGames")
    async def addGames(self, ctx, *, games:str):
        '''Add some games to your game list'''
        for game in games.split(", "):
            _, message = logic.addGame(ctx.author.name,game)
            await ctx.send(message)
        await ctx.send("Games added!")
    
    @commands.command(name="removeGame")
    async def removeGame(self, ctx, *, game:str):
        found = logic.removeGame(ctx.author.name, game)
        if found:
            await ctx.send(game + " deleted")
        else:
            await ctx.send("Couldn't find " + game)
    
    @commands.command(name="gameList")
    async def gameList(self, ctx, *, usr :typing.Optional[User] = 0):
        '''Find out what games someone has on their list'''
        if usr == 0:
            usr = ctx.author
        games = logic.gameList(usr.name)
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

    @commands.command(name="pickGame")
    async def pickGame(self, ctx, *, people :str):
        '''Find common games among multiple peoples games list'''
        peopleList = people.split(",")
        nameList = []
        for id in peopleList:
            if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
                id = id[id.find("<@!") + len("<@!"):] #erase the first bit
                id = id[:id.find(">")] #erase the last bit
            person = self.bot.get_user(int(id))
            nameList.append(person.name)
        await ctx.send(random.choice(logic.commonGames(nameList)))