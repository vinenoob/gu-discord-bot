import discord
import cogs.dad.logic as logic
from discord.ext import commands
from discord import app_commands
import my_discord_object_ids

class DadGroup(app_commands.Group):
    def __init__(self):
        super().__init__(name="daddy", description="Daddy commands", guild_ids=[my_discord_object_ids.bot_testing_server_id])
        print("DadGroup Initiated")
    
    @app_commands.command(name="dadjoke", description="get a dad joke")
    async def _dadjoke(self, interaction: discord.Interaction):
        await interaction.response.send_message(logic.getDadJoke())

    @app_commands.command(name="on", description="turn daddy on")
    async def _turnDaddyOn(self, interaction: discord.Interaction):
        logic.turnDaddyOn()
        await interaction.response.send_message("Daddy turned on ;)")

    @app_commands.command(name="off", description="turn daddy off")
    async def _turnDaddyOff(self, interaction: discord.Interaction):
        logic.turnDaddyOff()
        await interaction.response.send_message("Daddy has been forcibly turned off :(")

class Dad(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot= bot
        self.bot.tree.add_command(DadGroup())
        print("Dad Initiated")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            toDad = logic.daddy(message.content)
            if(toDad[0]):
                await message.channel.send(toDad[1])