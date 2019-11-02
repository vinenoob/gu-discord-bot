import discord
from discord.ext.commands import Bot
from discord.ext import commands

client = discord.Client()

@client.event
async def on_ready():
    print("Bot")

client.run("")