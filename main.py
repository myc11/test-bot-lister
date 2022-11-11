import discord
from discord.ext import commands



intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run('MTA0MDUwMzQ3MjEwNzI5MDY4NA.Gv__IO.hmG5_zrcZG7qPkX8pdNmkWkAdsWgVf6ZZ314Uk')


