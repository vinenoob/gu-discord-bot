import asyncio
import random
import time
import discord
from discord.ext import commands
from discord import app_commands
import my_discord_object_ids


IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".webp")


def image_url(message: discord.Message) -> str | None:
    '''URL of the first image attached to the message, if any'''
    for attachment in message.attachments:
        # Older attachments may not have a content type, fall back to the file extension
        if (attachment.content_type or "").startswith("image/") or attachment.filename.lower().endswith(IMAGE_EXTENSIONS):
            return attachment.url
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
        view.guesses[interaction.user.id] = self.member.id
        view.guess_times[interaction.user.id] = time.perf_counter() - view.started_at
        await interaction.response.send_message(f"You guessed {self.member.display_name}", ephemeral=True)


class GuessView(discord.ui.View):
    def __init__(self, question: str, author: discord.User | discord.Member, choices: list[discord.User | discord.Member], jump_url: str):
        # No view timeout: it resets on every click, so the command ends the round itself with end_round()
        super().__init__(timeout=None)
        self.question = question
        self.author = author
        self.jump_url = jump_url  # link to the original message, shown once the answer is revealed
        self.guesses: dict[int, int] = {}  # guesser id -> guessed member id
        self.guess_times: dict[int, float] = {}  # guesser id -> seconds after the round started
        self.started_at = time.perf_counter()
        self.message: discord.Message | None = None
        for member in choices:
            self.add_item(GuessButton(member))

    async def end_round(self):
        # Stop listening for clicks so no guesses land after the deadline
        self.stop()
        for item in self.children:
            if not isinstance(item, GuessButton):
                continue
            item.disabled = True
            if item.member.id == self.author.id:
                item.style = discord.ButtonStyle.success
        # Fastest correct guess first
        winner_ids = sorted((uid for uid, guess in self.guesses.items() if guess == self.author.id),
                            key=lambda uid: self.guess_times[uid])
        winners = [f"<@{uid}> ({self.guess_times[uid]:.1f}s)" for uid in winner_ids]
        result = ", ".join(winners) if winners else "nobody"
        played = len(self.guesses)
        if played == 0:
            summary = "Nobody played."
        else:
            summary = f"{played} {'person' if played == 1 else 'people'} played, {result} got it right."
        if self.message is None:
            return
        await self.message.edit(
            content=f"{self.question}\n\nIt was **{self.author.display_name}**! {summary}\n[Original message]({self.jump_url})",
            view=self,
            allowed_mentions=discord.AllowedMentions.none(),
        )


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

    @app_commands.command(name="play", description="Guess who sent a random message")
    @app_commands.describe(
        seconds="How long players have to guess (default 30)",
        choices="How many names to pick from (default 5)",
        history="How many recent messages to pick from (default 500)",
        channel="Channel, thread or forum post to pull the message from (default this channel)",
        images="Include messages with images (default off)",
    )
    async def play(
        self,
        interaction: discord.Interaction,
        # Max 5 minutes: the reveal edit has to happen within the 15 minute interaction window
        seconds: app_commands.Range[int, 10, 300] = 30,
        choices: app_commands.Range[int, 2, 25] = 5,
        history: app_commands.Range[int, 100, 2000] = 500,
        # Forum posts are threads, so this covers them too
        channel: discord.TextChannel | discord.Thread | None = None,
        images: bool = False,
    ):
        source = channel or interaction.channel
        if not isinstance(source, discord.abc.Messageable):
            await interaction.response.send_message("I can't read messages in this channel.", ephemeral=True)
            return
        # Don't let people pull messages from channels they can't read themselves
        if channel is not None:
            # Thread permissions come from the parent channel, which doesn't prove they're in a private thread
            if isinstance(channel, discord.Thread) and channel.is_private():
                await interaction.response.send_message("Private threads can't be used.", ephemeral=True)
                return
            if not isinstance(interaction.user, discord.Member) or not channel.permissions_for(interaction.user).read_message_history:
                await interaction.response.send_message("You can't read messages in that channel.", ephemeral=True)
                return
        # Reading history can take longer than the 3 second slash command limit
        await interaction.response.defer()
        # Pick a random human message with some text (or an image, if allowed) from recent channel history
        history_start = time.perf_counter()
        fetched = [m async for m in source.history(limit=history)]
        history_seconds = time.perf_counter() - history_start
        messages = [m for m in fetched
                    if not m.author.bot and not m.content.startswith("!")
                    and (len(m.content) > 10 or (images and image_url(m)))]
        print(f"GuessWho: fetched {len(fetched)} messages in {history_seconds:.2f}s, {len(messages)} usable")
        if not messages:
            await interaction.followup.send("Couldn't find any messages to use.")
            return
        picked = random.choice(messages)
        author = picked.author

        # Real author plus other people up to the requested count, shuffled
        others = list({m.author.id: m.author for m in messages if m.author.id != author.id}.values())
        options = random.sample(others, min(choices - 1, len(others))) + [author]
        random.shuffle(options)

        question = "Who said this?"
        if picked.content:
            # Quote every line, "> " only covers the line it's on
            question += "\n" + "\n".join(f"> {line}" for line in picked.content.splitlines())
        url = image_url(picked) if images else None
        if url:
            # Discord shows the image under the message from the bare link
            question += f"\n{url}"
        view = GuessView(question, author, options, picked.jump_url)
        # Discord renders this as a live "in X seconds" countdown on each viewer's client
        ends = int(time.time()) + seconds
        # The quoted message may contain mentions, don't ping anyone with them
        view.message = await interaction.followup.send(
            f"{question}\n\nEnds <t:{ends}:R>",
            view=view,
            wait=True,
            allowed_mentions=discord.AllowedMentions.none(),
        )
        # Wait until the countdown hits zero, however many guesses come in
        await asyncio.sleep(max(0, ends - time.time()))
        await view.end_round()
