from discord.ext import commands
from discord import app_commands
import discord
import my_discord_object_ids


class Overwatch(commands.Cog):
    """Cog for Overwatch commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.tree.add_command(OverwatchGroup())
        print("Overwatch Cog loaded.")


class OverwatchGroup(app_commands.Group):
    """Group of commands for Overwatch."""

    def __init__(self):
        super().__init__(
            name="overwatch",
            description="Overwatch commands",
            guild_ids=[my_discord_object_ids.bot_testing_server_id, my_discord_object_ids.gamers_united_server_id],
        )
        print("OverwatchGroup initiated")

    @app_commands.command(name="move", description="Move everyone from one voice channel to another")
    async def move(self, interaction: discord.Interaction, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel):
        """Move everyone from one voice channel to another."""
        await move_members(interaction, from_channel, to_channel)

    @app_commands.command(name="movehere", description="Move everyone from a voice channel to your voice channel")
    async def movehere(self, interaction: discord.Interaction, from_channel: discord.VoiceChannel):
        """Move everyone from a voice channel to the author's voice channel."""
        voice = interaction.user.voice if isinstance(interaction.user, discord.Member) else None
        if voice is None or voice.channel is None:
            await interaction.response.send_message("You need to be in a voice channel to use this", ephemeral=True)
            return
        await move_members(interaction, from_channel, voice.channel)


async def move_members(interaction: discord.Interaction, from_channel: discord.VoiceChannel, to_channel: discord.VoiceChannel | discord.StageChannel):
    """Move everyone in from_channel to to_channel and report the result."""
    members = list(from_channel.members)
    if not members:
        await interaction.response.send_message(f"Nobody is in {from_channel.mention}")
        return

    # moving many members can take longer than the 3 second response window
    await interaction.response.defer()
    failed = []
    for member in members:
        try:
            await member.move_to(to_channel)
        except discord.HTTPException:
            failed.append(member.display_name)

    moved = len(members) - len(failed)
    message = f"Moved {moved} member(s) from {from_channel.mention} to {to_channel.mention}"
    if failed:
        message += f"\nCouldn't move: {', '.join(failed)}"
    await interaction.followup.send(message)
