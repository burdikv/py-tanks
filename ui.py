import pygame


class UI(object):
    def __init__(self, screen):
        self.gamestart = 0
        self.gameplay = 1
        self.gameover = 2
        self.gamewin = 3
        self.pause = 4
        self.state = self.gamestart
        self.screen = screen
        self.surf = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.surfRect = self.surf.get_rect()
        self.surfRect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.fontBold = pygame.font.Font("Fonts\\Roboto\\Roboto-Bold.ttf", 60)
        self.fontNormal = pygame.font.Font("Fonts\\Roboto\\Roboto-Regular.ttf", 60)

    def draw_background(self):
        # pass
        self.surf.fill((0, 0, 0, 100))
        self.screen.blit(self.surf, (0, 0))

    def text_centered(self, message):
        text = self.fontBold.render(message, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.surfRect.center
        self.screen.blit(text, text_rect)

    def render(self):
        if self.state == self.gameover:
            self.draw_background()
            self.text_centered("Game Over")
        elif self.state == self.gamewin:
            self.draw_background()
            self.text_centered("You Win")
        elif self.state == self.pause:
            self.draw_background()
            self.text_centered("Press <SPACE> to resume...")
        elif self.state == self.gamestart:
            self.draw_background()
            self.text_centered("Press <SPACE> to start...")
