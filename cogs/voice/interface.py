import asyncio
import cogs.voice.logic as logic
import discord
from discord import app_commands
from discord.ext import commands
import my_discord_object_ids

class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # default listen channel (can be None until set)
        self.listen_channel_id: int | None = None
        bot.tree.add_command(VoiceGroup())
        print("Voice Cog loaded.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # only process messages in the configured channel
        if (
            message.author.bot
            or self.listen_channel_id is None
            or message.channel.id != self.listen_channel_id
        ):
            return

        vc: discord.VoiceClient | None = message.guild.voice_client
        if vc is None or not vc.is_connected():
            return  # or auto-join here

        filename = f"tts.mp3"
        to_say = message.content
        #replace mentions with their names
        for mention in message.mentions:
            to_say = to_say.replace(mention.mention, mention.nick or mention.name)
        for mention in message.role_mentions:
            to_say = to_say.replace(mention.mention, mention.name)
        for mention in message.channel_mentions:
            to_say = to_say.replace(mention.mention, mention.name)

        logic.generateTTS(to_say, filename)

        audio_src = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
        if vc.is_playing():
            vc.stop()
        vc.play(audio_src, after=lambda e: print(f"TTS error: {e}") if e else None)

        # wait for playback to finish before continuing
        while vc.is_playing():
            await asyncio.sleep(0.5)

class VoiceGroup(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="voice",
            description="Voice commands",
            guild_ids=[my_discord_object_ids.bot_testing_server_id],
        )
        print("VoiceGroup Initiated")

    @app_commands.command(name="join", description="Join your voice channel")
    async def _join(self, interaction: discord.Interaction):
        try:
            await interaction.user.voice.channel.connect()
            await interaction.response.send_message(f"Joined {interaction.user.voice.channel.name}")
        except Exception as e:
            await interaction.response.send_message(f"Error joining voice channel: {e}")

    @app_commands.command(name="leave", description="Leave voice channel")
    async def _leave(self, interaction: discord.Interaction):
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message("Left the voice channel")

    @app_commands.command(
        name="say",
        description="Say a one‑off message in voice"
    )
    async def _say(self, interaction: discord.Interaction, message: str):
        vc = interaction.guild.voice_client
        if not vc:
            await interaction.user.voice.channel.connect()
            vc = interaction.guild.voice_client
        filename = "tts.mp3"
        logic.generateTTS(message, filename)
        src = discord.FFmpegPCMAudio(executable="ffmpeg", source=filename)
        if vc.is_playing():
            vc.stop()
        await interaction.response.send_message(f"🔊 Playing: {message}")
        vc.play(src, after=lambda e: print(f"TTS error: {e}") if e else None)

    @app_commands.command(
        name="listen", 
        description="Configure which text channel I should auto‑TTS"
    )
    @app_commands.describe(channel="The text channel I should read from")
    async def _listen(
        self, 
        interaction: discord.Interaction, 
        channel: discord.TextChannel
    ):
        # grab the Voice cog and update its listen_channel_id
        voice_cog: Voice = interaction.client.get_cog("Voice")  # type: ignore
        voice_cog.listen_channel_id = channel.id

        await interaction.user.voice.channel.connect()

        await interaction.response.send_message(
            f"✅ I will now TTS anything posted in {channel.mention}.",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Voice(bot))
