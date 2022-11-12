import discord

from discord.ext import commands
from playlist import Playlist

voicehandlers = {}

class VoiceHandler:

    def __init__(self, voice_client: commands.Context.voice_client):
        self.voice_client = voice_client
        self.initial_channel = voice_client.channel
        self.playlist = Playlist()

        if not self.voice_client.is_connected():
            raise


    def get_info(self):
        return f"Connected to {str(self.voice_client.guild)}: {self.voice_client.channel}\n" \
               f"Connected: {self.voice_client.is_connected()} \n" \
               f"Paused: {self.voice_client.is_paused()} \n" \
               f"Playing: {self.voice_client.is_playing()}"


    def voice_state(self):
        # Check if is connected to voice channel
        if not self.voice_client.is_connected():

    async def play_song(self):
        pass

    def play_next(self):
        pass

