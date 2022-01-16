import discord
from discord.ext import commands
from discord.mentions import AllowedMentions
import smartBot.logic as logic

class smartBot(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        print("smartBot initiated")
    
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