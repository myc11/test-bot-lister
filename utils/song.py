import os


class Song:

    def __init__(self, name: str, source: str):
        self.name = name
        self.source = source

    def __del__(self):
        print('Destory ' + self.source)
        os.remove(self.source)