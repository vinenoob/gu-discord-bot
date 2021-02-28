from logging import error, log
from shlex import join
import typing
import discord
from discord import guild
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.core import command
from discord.ext import commands
from discord.utils import get
import voice.logic as logic

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot: AutoShardedBot = bot
        self.watch: discord.TextChannel = None
        print("Voice Initiated")

    @commands.command(name = "join")
    async def join(self, ctx: commands.Context):
        '''Joins the voice channel the user is in'''
        try:
            voice_channel = ctx.author.voice.channel
            if in_voice(ctx):
                await ctx.voice_client.disconnect() #if the bot is alread in a channel, leave it
            await voice_channel.connect()
        except AttributeError:
            await ctx.send("You aren't in a voice channel")

    @commands.command(name = "leave")
    async def leave(self, ctx: commands.Context):
        '''Leaves the voice channel the bot is currently in'''
        print(ctx.voice_client)
        if in_voice(ctx):
            await ctx.voice_client.disconnect()

    @commands.command(name="speak")
    async def speak(self, ctx: commands.Context, *, whatToSay: str):
        '''Makes the bot speak. Will join voice if not in already'''
        if not in_voice(ctx):
            await self.join(ctx)
        logic.generateTTS(whatToSay, "speach.mp3")
        ctx.voice_client.play(discord.FFmpegPCMAudio("speach.mp3"))

    @commands.command(name = "repeat")
    async def repeat(self, ctx: commands.Context, channel: typing.Optional[discord.TextChannel]):
        '''The bot will repeat in voice whatever is said in the specified channel'''
        if channel != None:
            await ctx.send("Repeating " + channel.name)
            await self.join(ctx)
            self.watch = channel
        else:
            await ctx.send("Could not find the specified channel")

    @commands.command(name= "stop_repeat")
    async def stop_repeat(self, ctx: commands.Context):
        '''Stops the bot from repeating a text channel'''
        await ctx.send("No longer repeating channel " + self.watch.name)
        self.watch = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot and not "stop_repeat" in message.content:
            if message.channel == self.watch:
                try:
                    voice_channel: discord.VoiceClient = get(self.bot.voice_clients, guild= message.guild)
                    logic.generateTTS(message.content, "watch.mp3")
                    voice_channel.play(discord.FFmpegPCMAudio("watch.mp3"))
                except AttributeError:
                    await self.stop_repeat()
                except AssertionError as error: #I know this is really generic
                    print(error)
                except Exception as error:
                    print(error)
        pass

def in_voice(ctx: commands.Context):
    if ctx.voice_client != None:
        return True
    return False