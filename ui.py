import pygame


class UI(object):
    def __init__(self, screen, clock, draw_fps=False):
        self.gamestart = 0
        self.gameplay = 1
        self.gameover = 2
        self.gamewin = 3
        self.pause = 4
        self.state = self.gamestart
        self.drawFps = draw_fps
        self.screen = screen
        self.clock = clock
        self.surf = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.surfRect = self.surf.get_rect()
        self.surfRect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        self.fontBold = pygame.font.Font("Fonts\\Roboto\\Roboto-Bold.ttf", 60)
        self.fontNormal = pygame.font.Font("Fonts\\Roboto\\Roboto-Regular.ttf", 20)

    def draw_background(self):
        # pass
        self.surf.fill((0, 0, 0, 100))
        self.screen.blit(self.surf, (0, 0))

    def text_centered(self, message):
        text = self.fontBold.render(message, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = self.surfRect.center
        self.screen.blit(text, text_rect)
        return text_rect

    def text(self, pos, color, message, centered=False):
        text = self.fontNormal.render(message, True, color)
        text_rect = text.get_rect()
        if centered:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        self.screen.blit(text, text_rect)
        return text_rect

    def render(self):
        if self.state == self.gameover:
            self.draw_background()
            r = self.text_centered("Game Over")
            p = (r.centerx, r.centery + r.height)
            self.text(p, (255, 255, 255), "Press <R> to restart...", True)
        elif self.state == self.gamewin:
            self.draw_background()
            r = self.text_centered("You Win")
            p = (r.centerx, r.centery + r.height)
            self.text(p, (255, 255, 255), "Press <R> to restart...", True)
        elif self.state == self.pause:
            self.draw_background()
            r = self.text_centered("Press <SPACE> to resume...")
            p = (r.centerx, r.centery + r.height)
            self.text(p, (255, 255, 255), "or <R> to restart...", True)
        elif self.state == self.gamestart:
            self.draw_background()
            self.text_centered("Press <SPACE> to start...")
        if self.drawFps:
            self.text((20, 20), (255, 0, 0), f"FPS: {int(round(self.clock.get_fps()))}")
