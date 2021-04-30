import random
import typing

import discord
from discord import User
from discord.ext import commands
from discord.ext.commands.converter import Converter, MemberConverter
from discord.ext.commands.core import command
from discord_slash import cog_ext, SlashContext
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option

import gameList.logic as logic



class GameList(commands.Cog):
    GAME_LIST_SLASH_BASE = "Gamelist"
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_subcommand(base = GAME_LIST_SLASH_BASE, name="add", description="Add a game to your list", guild_ids=[366792929865498634, 160907545018499072])
    async def _addGame(self, ctx: SlashContext, game: str):
        _, message = logic.addGame(ctx.author.name, game)
        await ctx.send(message)

    @commands.command(name="addGame")
    async def addGame(self, ctx, *,game :str):
        '''Add a game to your game list'''
        _, message = logic.addGame(ctx.author.name, game)
        await ctx.send(message)

    @commands.command(name="addGames")
    async def addGames(self, ctx, *, games:str):
        '''Add some games to your game list'''
        gamesAdded = ""
        for game in games.split(", "):
            _, message = logic.addGame(ctx.author.name,game)
            gamesAdded += message + "\n"
        await ctx.send(gamesAdded)
        await ctx.send("Games added!")
    
    @cog_ext.cog_subcommand(base = GAME_LIST_SLASH_BASE, name="remove", description="Remove a game to your list", guild_ids=[366792929865498634, 160907545018499072])
    async def _removeGame(self, ctx: SlashContext, game: str):
        found = logic.removeGame(ctx.author.name, game)
        if found:
            await ctx.send(game + " deleted")
        else:
            await ctx.send("Couldn't find " + game)

    @commands.command(name="removeGame")
    async def removeGame(self, ctx, *, game:str):
        found = logic.removeGame(ctx.author.name, game)
        if found:
            await ctx.send(game + " deleted")
        else:
            await ctx.send("Couldn't find " + game)
    

    gamesOptions = [
        create_option(
            name="user",
            description="The user who's games to get",
            option_type=SlashCommandOptionType.USER,
            required=False,
        )
    ]
    @cog_ext.cog_subcommand(base = GAME_LIST_SLASH_BASE, name="games", description="Shows games of a user", options = gamesOptions, guild_ids=[366792929865498634, 160907545018499072])
    async def _gameList(self, ctx: SlashContext, user = 0):
        print(user)
        if user == 0:
            user = ctx.author
        games = logic.gameList(user.name)
        if games == '':
            games = "Person not found in database"
        await ctx.send(games)

    @commands.command(name="gameList")
    async def gameList(self, ctx, *, usr :typing.Optional[User] = 0):
        '''Find out what games someone has on their list'''
        if usr == 0:
            usr = ctx.author
        games = logic.gameList(usr.name)
        if games == '':
            games = "Person not found in database"
        await ctx.send(games)
    
    commonOptions = [
        create_option(name = "user1",description = "User 1",option_type = SlashCommandOptionType.USER, required=True,),
        create_option(name = "user2",description = "User 2",option_type = SlashCommandOptionType.USER, required=True,),
        create_option(name = "user3",description = "User 3",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user4",description = "User 4",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user5",description = "User 5",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user6",description = "User 6",option_type = SlashCommandOptionType.USER, required=False,),
    ]
    @cog_ext.cog_subcommand(base = GAME_LIST_SLASH_BASE, name="common", description="Shows games common to both users", options = commonOptions, guild_ids=[366792929865498634, 160907545018499072])
    async def _commonGames(self, ctx: SlashContext, user1 = None, user2 = None, user3 = None, user4 = None, user5 = None, user6 = None):
        people: typing.List[discord.User] = []
        if user1:
            people.append(user1)
        if user2:
            people.append(user1)
        if user3:
            people.append(user3)
        if user4:
            people.append(user4)
        if user5:
            people.append(user5)
        if user6:
            people.append(user6)
        nameList: typing.List[str] = []
        user: discord.User
        for user in people:
            nameList.append(user.name)
        await ctx.send(str(logic.commonGames(nameList)))


    @commands.command(name="commonGames")
    async def commonGames(self, ctx: commands.Context, *people :discord.User ):
        '''Find common games among multiple peoples games list'''
        nameList: typing.List[str] = []
        user: discord.User
        for user in people:
            nameList.append(user.name)
        await ctx.send(logic.commonGames(nameList))

    pickOptions = [
        create_option(name = "user1",description = "User 1",option_type = SlashCommandOptionType.USER, required=True,),
        create_option(name = "user2",description = "User 2",option_type = SlashCommandOptionType.USER, required=True,),
        create_option(name = "user3",description = "User 3",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user4",description = "User 4",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user5",description = "User 5",option_type = SlashCommandOptionType.USER, required=False,),
        create_option(name = "user6",description = "User 6",option_type = SlashCommandOptionType.USER, required=False,),
    ]
    @cog_ext.cog_subcommand(base = GAME_LIST_SLASH_BASE, name="pick", description="Pick a game common to all players", options = pickOptions, guild_ids=[366792929865498634, 160907545018499072])
    async def _pickGame(self, ctx: SlashContext, user1 = None, user2 = None, user3 = None, user4 = None, user5 = None, user6 = None):
        people: typing.List[discord.User] = []
        if user1:
            people.append(user1)
        if user2:
            people.append(user1)
        if user3:
            people.append(user3)
        if user4:
            people.append(user4)
        if user5:
            people.append(user5)
        if user6:
            people.append(user6)
        nameList: typing.List[str] = []
        user: discord.User
        for user in people:
            nameList.append(user.name)
        await ctx.send(random.choice(logic.commonGames(nameList)))

    @commands.command(name="pickGame")
    async def pickGame(self, ctx, *, people :str):
        '''Find common games among multiple peoples games list'''
        peopleList = people.split(" ")
        nameList = []
        for id in peopleList:
            if "<@!" in id: #see if the channel is a channel mention, ie "#but-stuff"
                id = id[id.find("<@!") + len("<@!"):] #erase the first bit
                id = id[:id.find(">")] #erase the last bit
            person = self.bot.get_user(int(id))
            nameList.append(person.name)
        await ctx.send(random.choice(logic.commonGames(nameList)))
