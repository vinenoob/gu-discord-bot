import asyncio
import random
import time
import discord
from discord.ext import commands
from discord import app_commands
import my_discord_object_ids


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")
# Text this many characters or shorter is too little to guess from
MIN_MESSAGE_LENGTH = 10
# How long fetched channel history is reused before it's fetched again
CACHE_SECONDS = 10 * 60
# Channels with message history and an id to cache it under (plain Messageable has no id)
HistorySource = (discord.TextChannel | discord.Thread | discord.VoiceChannel | discord.StageChannel
                 | discord.DMChannel | discord.GroupChannel | discord.PartialMessageable)


def image_url(message: discord.Message) -> str | None:
    '''URL of the first image attached to the message, if any'''
    for attachment in message.attachments:
        # Older attachments may not have a content type, fall back to the file extension
        if (attachment.content_type or "").startswith("image/") or attachment.filename.lower().endswith(IMAGE_EXTENSIONS):
            return attachment.url
    return None


def is_usable(message: discord.Message, allow_images: bool) -> bool:
    '''Whether the message is a human's, with enough text (or an image, if allowed) to guess from'''
    if message.author.bot:
        return False
    # Short messages are only usable for their image
    has_image = allow_images and image_url(message) is not None
    if not has_image:
        if len(message.content) <= MIN_MESSAGE_LENGTH:
            return False
    return True


def channel_error(channel: discord.TextChannel | discord.VoiceChannel | discord.Thread | None, user: discord.User | discord.Member) -> str | None:
    '''Why the user can't pull messages from the channel they picked, or None if they can'''
    # No channel picked means the one the command was run in, which they can already read
    if channel is None:
        return None
    # Thread permissions come from the parent channel, which doesn't prove they're in a private thread
    if isinstance(channel, discord.Thread) and channel.is_private():
        return "Private threads can't be used."
    if not isinstance(user, discord.Member) or not channel.permissions_for(user).read_message_history:
        return "You can't read messages in that channel."
    return None


class GuessButton(discord.ui.Button):
    def __init__(self, member: discord.User | discord.Member):
        super().__init__(label=member.display_name[:80], style=discord.ButtonStyle.primary)
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        view = self.view
        if not isinstance(view, GuessView):
            return
        if interaction.user.id in view.guesses:
            await interaction.response.send_message("You already guessed!", ephemeral=True)
            return
        view.guesses[interaction.user.id] = (self.member.id, time.perf_counter() - view.started_at)
        await interaction.response.send_message(f"You guessed {self.member.display_name}", ephemeral=True)


class GuessView(discord.ui.View):
    def __init__(self, author: discord.User | discord.Member, options: list[discord.User | discord.Member]):
        # No view timeout: it resets on every click, so the command ends the round itself with end_round()
        super().__init__(timeout=None)
        self.author = author
        # guesser id -> (guessed member id, seconds after the round started), in the order guesses came in
        self.guesses: dict[int, tuple[int, float]] = {}
        self.started_at = time.perf_counter()
        for member in options:
            self.add_item(GuessButton(member))

    def end_round(self) -> str:
        '''Disable the buttons, highlight the answer and summarize who got it right'''
        # Stop listening for clicks so no guesses land after the deadline
        self.stop()
        for item in self.children:
            if not isinstance(item, GuessButton):
                continue
            item.disabled = True
            if item.member.id == self.author.id:
                item.style = discord.ButtonStyle.success
        if not self.guesses:
            return "Nobody played."
        # Guesses are in the order they came in, so the fastest correct guess is first
        winners = ", ".join(f"<@{uid}> ({seconds:.1f}s)" for uid, (guess, seconds) in self.guesses.items()
                            if guess == self.author.id) or "nobody"
        played = len(self.guesses)
        return f"{played} {'person' if played == 1 else 'people'} played, {winners} got it right."


class GuessWho(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.tree.add_command(GuessWhoGroup())
        print("GuessWho Initiated")


class GuessWhoGroup(app_commands.Group):
    def __init__(self):
        super().__init__(
            name="guesswho",
            description="Guess who sent a message",
            guild_ids=[my_discord_object_ids.bot_testing_server_id, my_discord_object_ids.gamers_united_server_id],
        )
        # channel id -> (time fetched, history count fetched, messages newest first)
        self.history_cache: dict[int, tuple[float, int, list[discord.Message]]] = {}

    async def get_history(self, source: HistorySource, limit: int) -> list[discord.Message]:
        '''The newest `limit` messages in the channel, from the cache if it covers them'''
        cached = self.history_cache.get(source.id)
        if cached is None:
            return await self.fetch_history(source, limit)
        fetched_at, fetched_limit, messages = cached
        if time.time() - fetched_at >= CACHE_SECONDS:
            return await self.fetch_history(source, limit)
        # A smaller fetch can't cover a bigger one
        if fetched_limit < limit:
            return await self.fetch_history(source, limit)
        # History comes newest first, so slicing keeps the most recent messages
        return messages[:limit]

    async def fetch_history(self, source: HistorySource, limit: int) -> list[discord.Message]:
        '''Fetch the newest `limit` messages from Discord and cache them'''
        start = time.perf_counter()
        messages = [m async for m in source.history(limit=limit)]
        print(f"GuessWho: fetched {len(messages)} messages from Discord in {time.perf_counter() - start:.2f}s")
        self.history_cache[source.id] = (time.time(), limit, messages)
        return messages

    @app_commands.command(name="play", description="Guess who sent a random message")
    @app_commands.describe(
        seconds="How long players have to guess (default 30)",
        choices="How many names to pick from (default 5)",
        history="How many recent messages to pick from (default 500)",
        channel="Channel, voice channel, thread or forum post to pull the message from (default this channel)",
        images="Include messages with images (default off)",
    )
    async def play(
        self,
        interaction: discord.Interaction,
        # Max 5 minutes: the reveal edit has to happen within the 15 minute interaction window
        seconds: app_commands.Range[int, 10, 300] = 30,
        choices: app_commands.Range[int, 2, 25] = 5,
        history: app_commands.Range[int, 100, 2000] = 500,
        # Forum posts are threads, so this covers them too. Voice channels have their own text chat
        channel: discord.TextChannel | discord.VoiceChannel | discord.Thread | None = None,
        images: bool = False,
    ):
        source = channel or interaction.channel
        if not isinstance(source, discord.abc.Messageable):
            await interaction.response.send_message("I can't read messages in this channel.", ephemeral=True)
            return
        # Don't let people pull messages from channels they can't read themselves
        error = channel_error(channel, interaction.user)
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return
        # Reading history can take longer than the 3 second slash command limit
        await interaction.response.defer()
        # Pick a random usable message from recent channel history
        fetched = await self.get_history(source, history)
        messages = [m for m in fetched if is_usable(m, images)]
        print(f"GuessWho: {len(messages)} of {len(fetched)} messages usable")
        if not messages:
            await interaction.followup.send("Couldn't find any messages to use.")
            return
        picked = random.choice(messages)
        author = picked.author

        # Real author plus other people up to the requested count, shuffled
        others = list({m.author.id: m.author for m in messages if m.author.id != author.id}.values())
        options = random.sample(others, min(choices - 1, len(others))) + [author]
        random.shuffle(options)

        # Channel mentions render as a clickable #name and never ping anyone
        question = f"Who said this in <#{picked.channel.id}>?"
        if picked.content:
            # Quote every line, "> " only covers the line it's on
            question += "\n" + "\n".join(f"> {line}" for line in picked.content.splitlines())
        url = image_url(picked) if images else None
        if url:
            # Discord shows the image under the message from the bare link
            question += f"\n{url}"
        view = GuessView(author, options)
        # Discord renders this as a live "in X seconds" countdown on each viewer's client
        ends = int(time.time()) + seconds
        # The quoted message may contain mentions, don't ping anyone with them
        message = await interaction.followup.send(
            f"{question}\n\nEnds <t:{ends}:R>",
            view=view,
            wait=True,
            allowed_mentions=discord.AllowedMentions.none(),
        )
        # Wait until the countdown hits zero, however many guesses come in
        await asyncio.sleep(max(0, ends - time.time()))
        summary = view.end_round()
        await message.edit(
            content=f"{question}\n\nIt was **{author.display_name}**! {summary}\n[Original message]({picked.jump_url})",
            view=view,
            allowed_mentions=discord.AllowedMentions.none(),
        )
