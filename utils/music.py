import discord
from discord.ext import commands
from utils.playlist import *
from utils.song import *
from utils.musicyoutube import *
import youtube_dl

class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.playlist = Playlist()
        self.voice_client = None
        print('Music Extension Loaded')


    @commands.command(name='join', invoke_without_subcommand=True, aliases=['j'])
    async def __join(self, ctx: commands.Context):

        dest = ctx.author.voice.channel
        self.voice_client = await dest.connect(reconnect=True, timeout=None)

        print(f'Joined {ctx.author.voice.channel}')
        await ctx.send(f'Joined {ctx.author.voice.channel}')

    @commands.command(name='leave', invoke_without_subcommand=True, aliases=['disconnect', 'quit', 'dc'])
    async def __leave(self, ctx: commands.Context):
        await ctx.voice_client.disconnect()
        self.voice_client = None

    @commands.command(name='play', aliases=['p'])
    async def __play(self, ctx: commands.Context, *, msg: str):
        #song = self.playlist.get()
        #print("Playing: " + song.name + ' ' + song.source)
        print(msg)
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(msg, download=False)
            URL = info['formats'][0]['url']
        # voice = get(self.bot.voice_clients, guild=ctx.guild)
        print(URL)

        self.voice_client.play(discord.FFmpegPCMAudio(URL))


        '''
        song = await download_audio(msg)

        if song:
            if len(self.playlist) == 0:
                self.playlist.add(song)
                await ctx.send(f'Now playing {song.name}')
                await self.play_song()

            else:
                self.playlist.add(song)
                await ctx.send(f'{song.name} added in queue position {len(self.playlist) - 1}')
        '''
    '''async def play_song(self):
        song = self.playlist.get()
        print("Playing: " + song.name + ' ' + song.source)
        if song != None:

            source = discord.PCMVolumeTransformer((discord.FFmpegPCMAudio(song.source)))
            print('fuck')
            self.voice_client.play(source, after=lambda e: self.next_song(e))'''



    def next_song(self, e):
        coro = self.play_song()
        self.bot.loop.create_task(coro)

    @__join.before_invoke
    async def before_connect(self, ctx: commands.Context):
        if not ctx.author.voice:
            await ctx.send("You are not connected to any voice channel.")
            raise commands.CommandError("You are not connected to any voice channel.")
        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("Already connected to another voice channel.")
                raise commands.CommandError("Already connected to another voice channel.")

    @__play.before_invoke
    async def before_play(self, ctx: commands.Context):
        if not self.voice_client:
            dest = ctx.author.voice.channel
            self.voice_client = await dest.connect(reconnect=True, timeout=None)

            print(f'Joined {ctx.author.voice.channel}')
            await ctx.send(f'Joined {ctx.author.voice.channel}')
        else:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                await ctx.send("Already connected to another voice channel.")
                raise commands.CommandError("Already connected to another voice channel.")




async def setup(bot):
    await bot.add_cog(Music(bot))
