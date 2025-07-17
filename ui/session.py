class PlaybackSession:
    def __init__(self):
        self.active_item = None
        self.playing = False

    def start(self, item):
        self.active_item = item
        self.playing = True

    def stop(self):
        self.active_item = None
        self.playing = False

    def pause(self):
        self.playing = False

    def is_active(self):
        return self.active_item is not None

SESSION = PlaybackSession()
