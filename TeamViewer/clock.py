class Clock():
    def __init__(self, FPS):
        self.fps = FPS
        self.seconds = 0
        self.frames = 0
    
    def tick(self):
        if self.frames == self.fps - 1:
            self.frames = 0
            self.seconds += 1
        else:
            self.frames += 1

    @property
    def time(self):
        secs = str(self.seconds % 60).zfill(2)
        mins = str(int(self.seconds / 60)).zfill(2)

        return "{}:{}".format(mins, secs)