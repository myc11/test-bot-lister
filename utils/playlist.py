from utils.log import Log
import random
class Playlist:

    def __init__(self):
        self.queue = []
        self.loop_song = False
        self.loop_queue = False
        self.loop_skip = False
        self.playing = None

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        songname = self.playing.name if self.playing is not None else 'None'
        if len(self) != 0:
            return f'Song loop: {self.loop_song}  Queue loop: {self.loop_queue}\n'+f'Playing: {songname}\n'+'\n'.join([f'{i + 1}. {song.name}'for i, song in enumerate(self.queue)])
        return f'Song loop: {self.loop_song}  Queue loop: {self.loop_queue}\n' + \
               f'Playing: {songname}\n'+'The playlist is empty'

    def loop(self):
        self.loop_song = not self.loop_song
        return self.loop_song

    def loopqueue(self):
        self.loop_queue = not self.loop_queue
        return self.loop_queue

    def add(self, song):
        Log.log('playlist', f'{song.name} added')
        self.queue.append(song)

    def shuffle(self):
        random.shuffle(self.queue)

    def get(self):
        if self.playing is not None and self.playing not in self.queue and not self.loop_song:
            self.playing.destroy()

        skip = True if self.loop_skip else False
        self.loop_skip = False

        if len(self) == 0:
            if self.playing is not None and (self.loop_song or self.loop_queue):
                return self.playing
            self.playing = None
            return None
        elif self.loop_song and self.loop_queue:
            if self.playing is None or skip:
                self.queue.append(self.playing)
                self.playing = self.queue.pop(0)
            return self.playing
        elif self.loop_song:
            if self.playing is None or skip:
                self.playing = self.queue.pop(0)
            return self.playing
        elif self.loop_queue:
            if self.playing is not None:
                self.queue.append(self.playing)
            self.playing = self.queue.pop(0)
            return self.playing
        else:
            self.playing = self.queue.pop(0)
            return self.playing

    def clear(self):
        self.queue.clear()
        self.playing = None
