import cogs.dice.logic as logic
from discord.ext import commands
from discord import app_commands
import discord
import my_discord_object_ids


class Dice(commands.Cog):
    """Cog for rolling dice."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Register the command group
        bot.tree.add_command(DiceGroup())
        print("Dice Cog loaded.")


class DiceGroup(app_commands.Group):
    """Group of commands for rolling dice."""

    def __init__(self):
        super().__init__(
            name="dice",
            description="Dice commands",
            guild_ids=[my_discord_object_ids.bot_testing_server_id, my_discord_object_ids.gamers_united_server_id],
        )
        print("DiceGroup initiated")

    @app_commands.command(name="roll", description="Roll dice in the format XdY")
    async def roll(self, interaction: discord.Interaction, notation: str):
        """Roll dice in the format XdY."""
        try:
            rolls, total = logic.roll_and_sum(notation)
            await interaction.response.send_message(f"Rolls: {rolls}, Total: {total}")
        except logic.DiceParseError as e:
            await interaction.response.send_message(f"Error parsing dice notation: {e}")
        except ValueError as e:
            await interaction.response.send_message(f"Error: {e}")
        except Exception as e:
            await interaction.response.send_message(f"An unexpected error occurred: {e}")