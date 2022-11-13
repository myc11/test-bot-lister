import discord
from discord.ext import commands
from utils.playlist import *
from utils.song import *
from utils.musicyoutube import *
from utils.voicehandler import VoiceHandler

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        print('Music Extension Loaded')

    @commands.command(name='queue', invoke_without_subcommand=True, aliases=['q'])
    async def __queue(self, ctx: commands.Context):
        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        print(str(voicehandler.playlist))
        await ctx.send(str(voicehandler.playlist))

    @commands.command(name='join', invoke_without_subcommand=True, aliases=['j'])
    async def __join(self, ctx: commands.Context):
        await VoiceHandler.get_voicehandler(ctx)

    @commands.command(name='leave', invoke_without_subcommand=True, aliases=['disconnect', 'quit', 'dc'])
    async def __leave(self, ctx: commands.Context):
        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        if voicehandler is not None:
            await voicehandler.disconnect(ctx)

    @commands.command(name='play', aliases=['p'])
    async def __play(self, ctx: commands.Context, *, msg: str):
        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        if 'www.bilibili.com' in msg:
            await ctx.send('Searching Bilibili...')
            await voicehandler.load_song_bilibili(ctx, msg)
        else:
            await ctx.send('Searching YouTube...')
            await voicehandler.load_song_youtube(ctx, msg)


    @commands.command(name='playy', aliases=['playyoutube', 'y'])
    async def __playyoutube(self, ctx: commands.Context, *, msg: str):

        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        await voicehandler.load_song_youtube(ctx, msg)

    @commands.command(name='playb', aliases=['playbili', 'b'])
    async def __playbili(self, ctx: commands.Context, *, msg: str):

        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        await voicehandler.load_song_bilibili(ctx, msg)


    @__join.before_invoke
    @__playyoutube.before_invoke
    @__playbili.before_invoke
    async def before_connect(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            raise commands.CommandError("You are not connected to any voice channel.")
        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("Already connected to another voice channel.")
                raise commands.CommandError("Already connected to another voice channel.")



async def setup(bot):
    await bot.add_cog(Music(bot))
