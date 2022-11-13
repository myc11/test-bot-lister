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
    async def get_voicehandler(cls, ctx: commands.Context, connect=True):
        if hash(ctx.guild) in voicehandlers:
            if connect:
                if voicehandlers[hash(ctx.guild)].voice_state():
                    return voicehandlers[hash(ctx.guild)]

                await voicehandlers[hash(ctx.guild)].connect(ctx)
                return voicehandlers[hash(ctx.guild)]

            elif not connect:
                return voicehandlers[hash(ctx.guild)]
        else:
            if ctx.author.voice:
                if connect:
                    voicehandler = VoiceHandler(ctx.bot, ctx)
                    await voicehandler.connect(ctx)

                    return voicehandler

                return VoiceHandler(ctx.bot, ctx)

        return None

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

    async def disconnect(self, ctx):
        if self.voice_state():
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Not connected to voice channel")
        voicehandlers.pop(hash(ctx.guild))
        # Clean play list
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

    def download_source(self, url):
        if 'www.bilibili.com' in url:
            return download_bili_audio(url)
        elif 'www.youtube.com' in url:
            return download_audio_global(url)
        else:
            Log.log('download_url', "ERROR")

    async def play_song(self):
        if not self.voice_state():
            Log.log('play_song', 'VOICE_STATE ERROR')

        song = self.playlist.get()

        try:
            if song is not None:
                Log.log("play_song", 'Playing '+ str(song))
                source = self.download_source(song.path)
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
        await ctx.send('Searching Bilibili...')
        async with self.txtchannel.typing():
            song = preprocess_bili(msg)
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
