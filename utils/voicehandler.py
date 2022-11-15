import traceback

import discord
from discord.ext import commands
from utils.playlist import Playlist
from utils.musicyoutube import *
from utils.musicbilibili import *
from utils.log import *

voicehandlers = {}

class VoiceHandler:

    def __init__(self, bot, ctx: commands.Context):
        self.bot = bot
        self.playlist = Playlist()
        self.txtchannel = ctx.channel
        self.voice_client = ctx.voice_client

        Log.log('VoiceHandler.__init__', "New handler: "+str(ctx.guild))

        voicehandlers[hash(ctx.guild)] = self

    @classmethod
    async def get_voicehandler_from_guild(cls, guild: discord.Guild):
        if hash(guild) in voicehandlers:
            return voicehandlers[hash(guild)]
        return None

    @classmethod
    async def get_voicehandler(cls, ctx: commands.Context, connect=True):
        if hash(ctx.guild) in voicehandlers:
            voicehandler = voicehandlers[hash(ctx.guild)]
            # Rebind channel
            if voicehandler.txtchannel != ctx.channel:
                voicehandler.txtchannel = ctx.channel
            if connect:
                # If is connected
                if voicehandler.voice_state():
                    return voicehandler

                await voicehandler.connect(ctx)
                return voicehandler

            elif not connect:
                return voicehandler
        else:
            if ctx.author.voice:
                if connect:
                    voicehandler = VoiceHandler(ctx.bot, ctx)
                    await voicehandler.connect(ctx)

                    return voicehandler

                return VoiceHandler(ctx.bot, ctx)

    async def connect(self, ctx):
        try:
            if ctx.author.voice:
                dest = ctx.author.voice.channel
                await dest.connect(timeout=60)
                self.bot = ctx.bot
                self.txtchannel = ctx.channel
                self.voice_client = ctx.voice_client

                Log.log('get_voicehandler', f"Connected to {ctx.guild}: {ctx.channel}")
        except Exception as e:
            Log.log('Connect Error', e)

    def get_info(self):
        return f"Connected to {str(self.voice_client.guild)}: {self.voice_client.channel}\n" \
               f"Connected: {self.voice_state()} \n" \
               f"Paused: {self.voice_client.is_paused()} \n" \
               f"Playing: {self.voice_client.is_playing()}"

    async def check_channel_members(self):
        try:
            if self.voice_state():
                members = self.voice_client.channel.members
                Log.log('check_channel_members', self.voice_client.channel.members)
                if len(members) == 1:
                    await self._disconnect()
        except:
            traceback.print_exc()


    async def disconnect(self, ctx):
        if self.voice_state():
            await self._disconnect()
        else:
            await ctx.send("Not connected to voice channel")
        # voicehandlers.pop(hash(ctx.guild))
        # Clean play list
        self.playlist.clear()

    async def _disconnect(self):
        if self.voice_state():
            await self.txtchannel.send(f'Disconnected from {self.voice_client.channel}')
            await self.voice_client.disconnect()
            Log.log('Disconnect', f'{self.voice_client.guild}: {self.voice_client.channel}')
            self.playlist.clear()

    async def skip(self, ctx):
        if not self.voice_state():
            await ctx.send("Not connected to voice channel")
        elif self.voice_client.is_playing():
            await ctx.send(f'{self.playlist.playing.name} skipped')
            self.playlist.loop_skip = True
            self.voice_client.stop()
        else:
            await ctx.send(f'No song is playing')


    def voice_state(self):
        # Check if is connected to voice channel
        return self.voice_client is not None and self.voice_client.is_connected()

    async def play_song(self):
        if not self.voice_state():
            Log.log('play_song', 'VOICE_STATE ERROR')
            return

        song = self.playlist.get()

        try:
            if song is not None:
                Log.log("play_song", 'Playing '+ str(song))
                source = song.get_source()
                await self.txtchannel.send(f'Now playing {song.name}')
                self.voice_client.play(source, after=lambda err: self.next_song(err))
            else:
                await self.txtchannel.send(f'No more songs to play')
        except Exception as e:
            traceback.print_exc()

    def next_song(self, err):
        Log.log('next_song', 'Ended with: '+str(err))
        if err is not None:
            traceback.print_exc()
            self.txtchannel.send('An error occured: ' + str(err))

        coro = self.play_song()
        self.bot.loop.create_task(coro)

    async def load_song_youtube(self, ctx, msg):
        await ctx.send('Searching YouTube...')
        async with self.txtchannel.typing():

            song = preprocess_youtube(msg)

            if song is not None:
                Log.log('load_song_youtube', f' {song.name}')
                self.playlist.add(song)
                if self.playlist.playing is None:
                    await self.play_song()
                else:
                    await ctx.send(f'{song.name} added in queue position {len(self.playlist)}')

            else:
                Log.log('ERROR: load_song_youtube', msg)
                await ctx.send(f'ERROR: load_song_youtube {msg}')

    async def load_song_bilibili(self, ctx, msg):
        await ctx.send('Searching Bilibili...')
        async with self.txtchannel.typing():

            song = preprocess_bili(msg)

            if song is not None:
                Log.log('load_song_bilibili', f'Load {song.name} success')
                self.playlist.add(song)
                if self.playlist.playing is None:
                    await self.play_song()
                else:
                    await ctx.send(f'{song.name} added in queue position {len(self.playlist)}')

            else:
                Log.log('ERROR: load_song_bilibili', msg)
                await ctx.send(f'ERROR: load_song_bilibili {msg}')
