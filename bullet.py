import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle, tank):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.tank = tank
        self.screen = screen
        self.speed = 50
        self.shell = None
        self.spriteNames = []
        self.init_sprites(self.tank.sprites)
        self.isDestroyed = False

    def init_sprites(self, sprites):
        self.spriteNames = self.get_sprite_names()
        if len(self.spriteNames) > 0:
            self.shell = sprites.get_sprite(self.spriteNames[0])

    def update(self):
        if self.isDestroyed:
            return
        x = self.x + self.speed * math.cos(math.radians(self.angle)) * self.tank.scaleFactor
        y = self.y + self.speed * math.sin(math.radians(self.angle)) * self.tank.scaleFactor
        self.x = int(round(x))
        self.y = int(round(y))

    def render(self):
        if self.isDestroyed or self.shell is None:
            return
        w, h = self.shell.get_width(), self.shell.get_height()
        scaled_shell = pygame.transform.scale(self.shell, (int(round(w * self.tank.scaleFactor)), int(round(h * self.tank.scaleFactor))))
        old_rect = scaled_shell.get_rect()
        old_rect.center = (self.x, self.y)
        shell = pygame.transform.rotate(scaled_shell, -90 - self.angle)
        rect = shell.get_rect()
        rect.center = old_rect.center
        self.screen.blit(shell, rect)

    # override this method to provide real sprite names
    def get_sprite_names(self):
        return []


class MediumShell(Bullet):
    def get_sprite_names(self):
        return ["shell.medium"]
