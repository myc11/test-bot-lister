import json
import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot('!', intents=intents)

extensions = [
    'utils.music',
    'utils.events'
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

async def main():
    token = json.load(open('settings.json', 'r', encoding='utf-8'))['TOKEN']
    for ext in extensions:
        await bot.load_extension(ext)
    await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())