from sprites import PivotSprite
import pygame

DEBUG_MODE = False


# blitRotate(screen, image, pos, (w / 2 - 20, h / 2), angle)
class Flash(PivotSprite):
    def __init__(self, x, y, angle, game):
        super().__init__()
        self.x = x
        self.y = y
        self.angle = angle
        self.scaleFactor = game.scaleFactor
        self.screen = game.screen
        self.clock = game.clock
        self.spriteIndex = 0
        self.sprites = []
        self.spriteNames = []
        self.init_sprites(game.sprites)
        self.isFinished = False
        self.lastTic = self.clock.frames_count()
        # adjust these vars to fit animation
        self.ticCount = 0
        self.adjustX = 0
        self.adjustY = 0

    def init_sprites(self, sprites):
        self.spriteNames = self.get_sprite_names()
        for name in self.spriteNames:
            sprite = sprites.get_sprite(name)
            if sprite is not None:
                self.sprites.append(sprite)

    def render(self):
        if self.isFinished or len(self.sprites) == 0:
            return
        tic = self.clock.frames_count()
        original_image = self.sprites[self.spriteIndex]
        w, h = original_image.get_width(), original_image.get_height()
        scaled_image = pygame.transform.scale(original_image,
                                              (int(round(w * self.scaleFactor)), int(round(h * self.scaleFactor))))
        pos = scaled_image.get_rect()
        pos.center = (self.x, self.y)
        rot_image = pygame.transform.rotate(scaled_image, -90 - self.angle)
        rect = rot_image.get_rect()
        rect.center = pos.center
        self.screen.blit(rot_image, rect)
        """
        imageMode(CENTER)
        noTint()
        pushMatrix()
        translate(self.x, self.y)
        scale(self.scaleFactor)
        rotate(PI/2+self.angleR)
        translate(self.adjustX, self.adjustY)
        image(self.sprites[self.spriteIndex], 0, 0)
        popMatrix()
        """
        if self.ticCount >= 0:
            if tic - self.lastTic > self.ticCount:
                self.spriteIndex += 1
                self.lastTic = tic
        if self.spriteIndex >= len(self.sprites):
            self.isFinished = True

    # override this method to provide real sprite names
    def get_sprite_names(self):
        return []

    # override for proper work of descendants
    def get_type(self):
        return "Flash"


class FlashA(Flash):
    def __init__(self, x, y, angle, game):
        super().__init__(x, y, angle, game)
        self.ticCount = 6
        self.adjustX = 0
        self.adjustY = -10

    def get_sprite_names(self):
        names = []
        for i in range(4):
            names.append("shot.flame.a." + str(i))
        return names


class HitA(Flash):
    def __init__(self, x, y, angle, game):
        super().__init__(x, y, angle, game)
        self.ticCount = 4

    def get_sprite_names(self):
        names = []
        for i in range(4):
            names.append("shot.hit.a." + str(i))
        return names

    def get_type(self):
        return "FlashA"


class Explosion(Flash):
    def __init__(self, x, y, game):
        super().__init__(x, y, 0, game)
        self.ticCount = 3

    def get_sprite_names(self):
        names = []
        for i in range(9):
            names.append("explosion." + str(i))
        return names

    def get_type(self):
        return "Explosion"


class EnergyShield(Flash):
    def __init__(self, duration, tank, game):
        super().__init__(tank.x, tank.y, 0, game)
        self.radius = 195
        self.adjustFactor = 1.5
        self.scaleFactor *= self.adjustFactor
        self.ticCount = self.clock.frame_rate() * duration
        self.tank = tank
        self.healthBarOffsetModifier = 50
        self.ui = game.ui
        self.sounds = game.sounds
        self.lastState = self.ui.gameplay
        self.delta = 0
        self.backupTicCount = self.ticCount

    def get_sprite_names(self):
        return ["any.tank.energyshield"]

    def get_type(self):
        return "EnergyShield"

    def render(self):
        if self.isFinished:
            return
        if self.ui.state != self.lastState:
            if self.lastState == self.ui.gameplay:
                self.delta = self.clock.frames_count() - self.lastTic
                self.ticCount = -1
            elif self.ui.state == self.ui.gameplay:
                self.lastTic = self.clock.frames_count() - self.delta
                self.ticCount = self.backupTicCount
            self.lastState = self.ui.state
        super().render()
        if DEBUG_MODE:
            pygame.draw.circle(self.screen, (0, 0, 0), (self.x, self.y),
                               self.radius * self.scaleFactor / self.adjustFactor, 1)

    def update(self):
        if self.isFinished:
            self.undo()
            return
        self.x = self.tank.x
        self.y = self.tank.y

    def apply(self):
        for effect in self.tank.containedEffects:
            if effect.get_type() == self.get_type() and effect != self:
                effect.isFinished = True
                effect.update()
                break
        self.tank.healthBarOffset += self.healthBarOffsetModifier
        self.tank.isShielded = True

    def undo(self):
        self.tank.healthBarOffset -= self.healthBarOffsetModifier
        self.tank.isShielded = False
        self.tank.containedEffects.remove(self)

    def check_hit(self, bullet):
        d2 = (self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2
        col_d = self.radius * self.scaleFactor / self.adjustFactor
        if d2 <= col_d ** 2:
            return True
        return False

    def hit(self, bullet):
        self.tank.hit(bullet)
        self.sounds.play("sound.hit.shield")


class EnergyShieldA(EnergyShield):
    def __init__(self, duration, tank, game):
        super().__init__(duration, tank, game)
        self.adjustFactor = 0.75
        self.scaleFactor = tank.scaleFactor * self.adjustFactor

    def get_sprite_names(self):
        return ["any.tank.energyshield.a"]

    def get_type(self):
        return "EnergyShield"
