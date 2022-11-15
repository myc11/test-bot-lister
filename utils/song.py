import os
import discord

class Song:

    def __init__(self, name: str, path, source: callable=None):
        self.name = name
        self.path = path
        self.source = source

    def __str__(self):
        return f'Name: {self.name} at {self.path}'

    def destroy(self):
        if self.source == None:
            os.remove(self.path)

    def get_source(self):
        if self.source is None:
            return discord.FFmpegPCMAudio(self.path)
        else:
            return self.source(self.path)