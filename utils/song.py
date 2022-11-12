import os


class Song:

    LOCAL = 0
    URL = 1

    def __init__(self, name: str, source: str, type):
        self.name = name
        self.source = source

    def destroy(self):
        print('Destory ' + self.source)
        os.remove(self.source)