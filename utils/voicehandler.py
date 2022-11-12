import discord

from discord.ext import commands
from utils.playlist import Playlist
from utils.musicyoutube import *

voicehandlers = {}

class VoiceHandler:

    def __init__(self, bot, voice_client: commands.Context.voice_client):
        self.bot = bot
        self.voice_client = voice_client
        self.initial_channel = voice_client.channel
        self.playlist = Playlist()

        if not self.voice_client.is_connected():
            raise

        voicehandlers[hash(voice_client.guild)] = self

    @classmethod
    async def get_voicehandler(cls, ctx: commands.Context):
        if hash(ctx.guild) in voicehandlers and voicehandlers[hash(ctx.guild)].voice_client.is_connected():
            return voicehandlers[hash(ctx.guild)]

        else:
            dest = ctx.author.voice.channel
            voice_client = await dest.connect(timeout=60)

            print(f"Connected to {voice_client.channel}")

            return VoiceHandler(ctx.bot, voice_client)

    def get_info(self):
        return f"Connected to {str(self.voice_client.guild)}: {self.voice_client.channel}\n" \
               f"Connected: {self.voice_client.is_connected()} \n" \
               f"Paused: {self.voice_client.is_paused()} \n" \
               f"Playing: {self.voice_client.is_playing()}"


    async def voice_state(self):
        # Check if is connected to voice channel
        if not self.voice_client.is_connected():
            # Try to reconnect to the initial_channel
            print("Warning: Trying to reconnect to " + str(self.initial_channel))
            await self.initial_channel.connect(timeout=60)


    async def play_song(self):
        await self.voice_state()

        if self.voice_client.is_playing():
            self.voice_client.pause()

        song = self.playlist.get()
        print("Playing: " + song.name + ' ' + song.source)

        if song:
            source = discord.FFmpegPCMAudio(song.source)
            self.voice_client.play(source, after=lambda e: self.play_next(e))

    def next_song(self, e):
        print('next_song: Ended with ' + e)
        coro = self.play_song()
        self.bot.loop.create_task(coro)

    async def load_song_youtube(self, ctx, msg):
        song = download_audio_global(msg)
        print(song.name, song.source)
        if song != None:
            if self.playlist.playing == None:
                self.playlist.add(song)
                await ctx.send(f'Now playing {song.name}')
                await self.play_song()
            else:
                self.playlist.add(song)
                await ctx.send(f'{song.name} added in queue position {len(self.playlist) - 1}')

        else:
            print('ERROR: load_song_youtube')
