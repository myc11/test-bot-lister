import json
import asyncio
import discord
from discord.ext import commands

from utils.log import Log
from utils.voicehandler import *

intents = discord.Intents.all()
bot = commands.Bot('$', intents=intents)

extensions = [
    'cogs.music',
    'cogs.events'
]

@bot.command()
async def load(ctx, extension):
    try:
        await bot.load_extension(f'{extension}')
        await ctx.send(f"Loaded {extension}")
    except FileExistsError:
        await ctx.send(f"No Extension names {extension}")

@bot.command()
async def unload(ctx, extension):
    try:
        await bot.unload_extension(f'{extension}')
        await ctx.send(f"Unloaded {extension}")
    except FileExistsError:
        await ctx.send(f"No Extension names {extension}")

@bot.command()
async def reload(ctx, extension):
    try:
        await bot.reload_extension(f'{extension}')
        await ctx.send(f"Re - Loaded {extension}")
    except FileExistsError:
        await ctx.send(f"No Extension names {extension}")

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # Channel changed
    Log.log('on_voice_state_update', member)
    if before.channel is not None and before.channel != after.channel:
        voicehandler =  await VoiceHandler.get_voicehandler_from_guild(before.channel.guild)
        if voicehandler is not None:
            await voicehandler.check_channel_members()

async def main():
    token = json.load(open('settings.json', 'r', encoding='utf-8'))['TOKEN']
    for ext in extensions:
        await bot.load_extension(ext)
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())