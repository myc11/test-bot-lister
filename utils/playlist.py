class Playlist:

    def __init__(self):
        self.queue = []
        self.loop_song = False
        self.loop_queue = False

        self.playing = None

    def __len__(self):
        return len(self.queue)

    def __str__(self):
        return f'Song loop: {self.loop_song}  Queue loop: {self.loop_queue}\n'+'\n'.join([f'{i}. {song.name}'for i, song in enumerate(self.queue)])

    def add(self, song):
        self.queue.append(song)

    def get(self):
        if self.playing is not None and self.playing not in self.queue:
            self.playing.destroy()

        self.playing = None

        if len(self) == 0:
            return None
        elif self.loop_song:
            self.playing = self.queue[0]
            return self.playing
        elif self.loop_queue:
            self.playing = self.queue.pop(0)
            self.queue.append(self.playing)
            return self.playing
        else:
            self.playing = self.queue.pop(0)
            return self.playing

    def clear(self):
        self.queue.clear()
        self.playing = None