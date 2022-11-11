class Playlist:

    def __init__(self):
        self.queue = []
        self.loop_song = False
        self.loop_queue = True

    def __len__(self):
        return len(self.queue)

    def add(self, song):
        self.queue.append(song)

    def get(self):
        if len(self) == 0:
            return None
        elif self.loop_song:
            return self.queue[0]
        elif self.loop_queue:
            res = self.queue.pop(0)
            self.queue.append(res)
            return res
        else:
            return self.queue.pop(0)