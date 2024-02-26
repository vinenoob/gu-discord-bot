import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord.mentions import AllowedMentions
import smartBot.logic as logic
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType


class smartBot(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        print("smartBot initiated")
    
    @cog_ext.cog_subcommand(base = "ai", name="image", description="create an image", guild_ids=[366792929865498634, 160907545018499072])
    async def create_image(self, ctx: SlashContext, prompt):
        await ctx.send(f"Creating image based on {prompt}")
        img = logic.createImage(prompt)
        await ctx.send(img)

    @cog_ext.cog_subcommand(base = "ai", name="load", options=[create_option(name="channel", description="channel history to load", option_type=SlashCommandOptionType.CHANNEL, required=True)], description="load a chat", guild_ids=[366792929865498634, 160907545018499072])
    async def load_chat(self, ctx: SlashContext, channel: discord.TextChannel):
        history = await channel.history(limit=100).flatten()
        flattened_history = []
        message :discord.Message
        for message in history:
            if message.author.bot:
                continue
            message_time = message.created_at
            time_string = f"{message_time.month}/{message_time.day}-{message_time.hour}:{message_time.minute}"
            flattened_history.append(f"Time: {time_string}, Author: {message.author.name}, Content:{message.content}")
        logic.loadMessages(flattened_history)
        await ctx.send("Chat loaded")
        print(flattened_history)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        command = await self.bot.get_context(message)
        if command.command == None:
            if message.author is not self.bot.user and self.bot.user in message.mentions:
                messageContent: str = message.content
                if message.content.find(str(self.bot.user.id)):
                    messageContent = messageContent.replace(f"<@!{self.bot.user.id}>", "")
                if messageContent == '':
                    return
                async with command.typing():
                    await message.channel.send(logic.generateOutput(messageContent), allowed_mentions=AllowedMentions(users=False))