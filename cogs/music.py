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


    @commands.command(name='join', invoke_without_subcommand=True, aliases=['j'])
    async def __join(self, ctx: commands.Context):
        await VoiceHandler.get_voicehandler(ctx)

    @commands.command(name='leave', invoke_without_subcommand=True, aliases=['disconnect', 'quit', 'dc'])
    async def __leave(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()
        self.voice_client = None

    @commands.command(name='play', aliases=['p'])
    async def __play(self, ctx: commands.Context, *, msg: str):

        voicehandler = await VoiceHandler.get_voicehandler(ctx)
        await voicehandler.load_song_youtube(ctx, msg)



    @__join.before_invoke
    @__play.before_invoke
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
