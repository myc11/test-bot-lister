import os


class Song:

    def __init__(self, name: str, source, local_path=None):
        self.name = name
        self.source = source
        self.local_path = local_path

    def __str__(self):
        if self.local_path is not None:
            return f'Name: {self.name} at {self.local_path}'
        else:
            return f'Name: {self.name} from url'

    def destroy(self):
        if self.local_path is not None:
            os.remove(self.local_path)