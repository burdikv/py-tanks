from ai import AI
from ui import UI
from sprites import Sprites
from sounds import Sounds


class Game(object):
    def __init__(self, screen, clock, scale_factor):
        self.screen = screen
        self.clock = clock
        self.scaleFactor = scale_factor
        self.bullets = []
        self.effects = []
        self.enemies = []
        self.player = None
        self.sprites = Sprites()
        # draw_fps=True in UI
        self.ui = UI(self.screen, self.clock, True)
        self.sounds = Sounds()
