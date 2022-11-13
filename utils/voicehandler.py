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
        if not self.voice_client.is_connected():
            raise

        voicehandlers[hash(ctx.guild)] = self

    @classmethod
    async def get_voicehandler(cls, ctx: commands.Context):
        if hash(ctx.guild) in voicehandlers and voicehandlers[hash(ctx.guild)].voice_client.is_connected():
            return voicehandlers[hash(ctx.guild)]

        else:
            if ctx.author.voice:
                dest = ctx.author.voice.channel
                voice_client = await dest.connect(timeout=60)

                Log.log('get_voicehandler', f"Connected to {ctx.guild}: {voice_client.channel}")

                return VoiceHandler(ctx.bot, ctx)
            return None

    def get_info(self):
        return f"Connected to {str(self.voice_client.guild)}: {self.voice_client.channel}\n" \
               f"Connected: {self.voice_client.is_connected()} \n" \
               f"Paused: {self.voice_client.is_paused()} \n" \
               f"Playing: {self.voice_client.is_playing()}"

    async def disconnect(self, ctx):
        if self.voice_client.is_playing():
            self.voice_client.stop()
        await ctx.voice_client.disconnect()
        voicehandlers.pop(hash(ctx.guild))
        # Clean play list
        self.playlist.clear()

    async def skip(self, ctx):
        if self.voice_client.is_playing():
            await ctx.send(f'{self.playlist.playing.name} skipped')
            self.voice_client.stop()
        else:
            await ctx.send(f'No song is playing')


    async def voice_state(self):
        # Check if is connected to voice channel
        if not self.voice_client.is_connected():
            Log.log('ERROR', 'NOT CONNECTED TO VOICE CHANNEL')
            raise


    async def play_song(self):
        await self.voice_state()


        song = self.playlist.get()

        if song is not None:
            Log.log("play_song", 'Playing '+song.name)
            await self.txtchannel.send(f'Now playing {song.name}')
            self.voice_client.play(song.source, after=lambda err: self.next_song())
        else:
            await self.txtchannel.send(f'No more songs to play')

    def next_song(self):
        Log.log('next_song', '_')
        coro = self.play_song()
        self.bot.loop.create_task(coro)

    async def load_song_youtube(self, ctx, msg):
        async with self.txtchannel.typing():
            song = download_audio_global(msg)

            if song is not None:
                Log.log('', f'load_song_youtube {song.name}')
                if self.playlist.playing is None:
                    self.playlist.add(song)
                    await self.play_song()
                else:
                    self.playlist.add(song)
                    await ctx.send(f'{song.name} added in queue position {len(self.playlist)}')

            else:
                Log.log('ERROR: load_song_youtube', msg)
                await ctx.send(f'ERROR: load_song_youtube {msg}')

    async def load_song_bilibili(self, ctx, msg):
        async with self.txtchannel.typing():
            song = download_bili_audio(msg)
            if song is not None:
                Log.log('', f'load_song_bilibili {song.name}')
                if self.playlist.playing is None:
                    self.playlist.add(song)
                    await self.play_song()
                else:
                    self.playlist.add(song)
                    await ctx.send(f'{song.name} added in queue position {len(self.playlist)}')

            else:
                Log.log('ERROR: load_song_bilibili', msg)
                await ctx.send(f'ERROR: load_song_bilibili {msg}')
