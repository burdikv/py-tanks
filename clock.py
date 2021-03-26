import pygame


class Clock(object):
    def __init__(self, default_fps: int):
        # super(Clock, self).__init__()
        self.clock = pygame.time.Clock()
        self.defaultFps = default_fps
        self.framesCount = 0

    def frames_count(self):
        return self.framesCount

    def frame_rate(self):
        return self.defaultFps

    def tick_default(self):
        self.framesCount += 1
        return self.clock.tick(self.defaultFps)

    def tick(self, framerate = 0):
        self.framesCount += 1
        return self.clock.tick(framerate)

    def tick_busy_loop(self, framerate = 0):
        self.framesCount += 1
        return self.clock.tick_busy_loop(framerate)
