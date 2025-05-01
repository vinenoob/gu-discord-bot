import discord
from my_discord_object_ids import *
from discord.ext import commands
import os
import asyncio
import cogs.dad



intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Logged on as', bot.user)

@bot.event
async def on_message(message):
    # don't respond to ourselves
    print(f"Message from {message.author}: {message.content} in {message.channel}")
    if message.author == bot.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')
    await bot.process_commands(message)

# on forum post creation
# @bot.event
# async def on_thread_create(post: discord.Thread):
#     print(f"Forum post created: {post.name} in {post.guild.name}")
#     await post.send("Hello!")

@bot.tree.command(name="say", guilds=[bot_testing_server])
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    """Send a message to a specific channel"""
    await channel.send(message)
    await interaction.response.send_message(f"Sent message to {channel.mention}")

@bot.hybrid_command()
async def sync(ctx):
    if ctx.author.id == my_id:
        stuff = await bot.tree.sync(guild=bot_testing_server)
        await ctx.send(f"Synced {len(stuff)} commands")



async def start_bot():
    key = ""
    try:
        key = os.environ['key']
    except:
        keyFile = open("key.txt", "r")
        key = keyFile.read()
        key = key.replace("\n", "")
        keyFile.close()
    
    async with bot:
        import cogs.dad.interface
        await bot.add_cog(cogs.dad.interface.Dad(bot))
        import cogs.heck.interface
        await bot.add_cog(cogs.heck.interface.Heck(bot))
        import cogs.poptarts.interface
        await bot.add_cog(cogs.poptarts.interface.Poptarts(bot))
        import cogs.voice.interface
        await bot.add_cog(cogs.voice.interface.Voice(bot))
        import cogs.dice.interface
        await bot.add_cog(cogs.dice.interface.Dice(bot))
        # await bot.load_extension("cogs.dad.interface")
        await bot.start(key)

if __name__ == "__main__":
    asyncio.run(start_bot())