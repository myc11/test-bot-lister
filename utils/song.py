import os


class Song:

    LOCAL = 0
    BILI = 1
    YOUTUBE = 2

    def __init__(self, name: str, path, source=None):
        self.name = name
        self.path = path
        self.source = source

    def __str__(self):
        return f'Name: {self.name} at {self.path}'

    def destroy(self):
        if self.source == Song.LOCAL:
            os.remove(self.path)