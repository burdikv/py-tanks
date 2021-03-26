import pygame
import math
from sprites import PivotSprite
from bullet import MediumShell
from effects import FlashA
from effects import HitA
from effects import Explosion


class Tank(PivotSprite):
    def __init__(self, x, y, angle, game):
        super().__init__()
        self.screen = game.screen
        self.clock = game.clock
        self.game = game
        self.x = x
        self.y = y
        self.scaleFactor = game.scaleFactor
        self.angle = angle
        self.turretAngle = 0
        self.tankBody = None
        self.turret = None
        self.tracks = []
        self.trackIndex = 0
        self.tracksSideShift = 80
        self.tracksBackShift = 5
        self.turretAngleStep = 2
        self.turretShift = 48
        self.barrelLength = 165
        self.angleStep = 2
        self.speed = 10
        self.isMoving = False
        self.isRotating = False
        self.width = 200
        self.height = 240

        self.keyTurnLeft = False
        self.keyTurnRight = False
        self.keyDriveForward = False
        self.keyDriveBackward = False
        self.keyTurnTurretLeft = False
        self.keyTurnTurretRight = False
        self.keyShoot = False

        self.shootDelay = 30
        self.shootCurrent = 0
        self.maxHealth = 5
        self.health = self.maxHealth
        self.healthBarWidth = 200
        self.healthBarHeight = 20
        self.healthBarOffset = self.height // 2 + 50
        self.isDead = False
        self.bullets = game.bullets
        self.effects = game.effects
        self.sprites = game.sprites
        self.sounds = game.sounds
        self.moveSound = self.sounds.clone_sound("sound.tank")
        self.containedEffects = []
        self.isShielded = False

    def render(self):
        if self.tankBody is None or self.turret is None or len(self.tracks) == 0:
            return
        if self.isMoving or self.isRotating:
            self.trackIndex = int(self.clock.frames_count() / 6) % 2
        # health bar
        if not self.isDead:
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (self.x - self.healthBarWidth * self.scaleFactor / 2,
                              self.y - (self.healthBarHeight + self.healthBarOffset) * self.scaleFactor,
                              self.healthBarWidth * self.scaleFactor, self.healthBarHeight * self.scaleFactor))
            pygame.draw.rect(self.screen, (255, 0, 0),
                             (self.x - self.healthBarWidth * self.scaleFactor / 2,
                              self.y - (self.healthBarHeight + self.healthBarOffset) * self.scaleFactor,
                              int(round(self.healthBarWidth * self.scaleFactor * self.health / self.maxHealth)),
                              self.healthBarHeight * self.scaleFactor))
        # tank
        t1 = (self.x - self.tracksBackShift * self.scaleFactor, self.y - self.tracksSideShift * self.scaleFactor)
        t2 = (self.x - self.tracksBackShift * self.scaleFactor, self.y + self.tracksSideShift * self.scaleFactor)
        phi = math.radians(self.angle)
        t1 = (int(round(self.x + (t1[0] - self.x) * math.cos(phi) - (t1[1] - self.y) * math.sin(phi))),
              int(round(self.y + (t1[0] - self.x) * math.sin(phi) + (t1[1] - self.y) * math.cos(phi))))
        t2 = (int(round(self.x + (t2[0] - self.x) * math.cos(phi) - (t2[1] - self.y) * math.sin(phi))),
              int(round(self.y + (t2[0] - self.x) * math.sin(phi) + (t2[1] - self.y) * math.cos(phi))))
        t1_image = self.tracks[self.trackIndex]
        w, h = t1_image.get_width(), t1_image.get_height()
        t1_scaled = pygame.transform.scale(t1_image,
                                           (int(round(w * self.scaleFactor)), int(round(h * self.scaleFactor))))
        if self.isDead:
            t1_scaled.fill((150, 150, 150, 100), special_flags=pygame.BLEND_MULT)
        pos = t1_scaled.get_rect()
        pos.center = t1
        t1_rot = pygame.transform.rotate(t1_scaled, -90 - self.angle)
        rect = t1_rot.get_rect()
        rect.center = pos.center
        self.screen.blit(t1_rot, rect)
        i = self.trackIndex
        if self.isRotating:
            i = 1 - self.trackIndex
        t2_image = self.tracks[i]
        w, h = t2_image.get_width(), t2_image.get_height()
        t2_scaled = pygame.transform.scale(t2_image,
                                           (int(round(w * self.scaleFactor)), int(round(h * self.scaleFactor))))
        if self.isDead:
            t2_scaled.fill((150, 150, 150, 100), special_flags=pygame.BLEND_MULT)
        pos = t2_scaled.get_rect()
        pos.center = t2
        t2_rot = pygame.transform.rotate(t2_scaled, -90 - self.angle)
        rect = t2_rot.get_rect()
        rect.center = pos.center
        self.screen.blit(t2_rot, rect)
        # image(self.tankBody, 0, 0)
        w, h = self.tankBody.get_width(), self.tankBody.get_height()
        scaled_body = pygame.transform.scale(self.tankBody,
                                             (int(round(w * self.scaleFactor)), int(round(h * self.scaleFactor))))
        if self.isDead:
            scaled_body.fill((150, 150, 150, 100), special_flags=pygame.BLEND_MULT)
        pos = scaled_body.get_rect()
        pos.center = (self.x, self.y)
        rot_body = pygame.transform.rotate(scaled_body, -90 - self.angle)
        rect = rot_body.get_rect()
        rect.center = pos.center
        # rot_body, rect = self.surface_rotate(scaled_body, (self.x, self.y), (w * self.scaleFactor // 2, h * self.scaleFactor // 2), self.angle - 90)
        self.screen.blit(rot_body, rect)
        if not self.isDead:
            w, h = self.turret.get_width(), self.turret.get_height()
            scaled_turret = pygame.transform.scale(self.turret,
                                                   (int(round(w * self.scaleFactor)), int(round(h * self.scaleFactor))))
            pos = scaled_turret.get_rect()
            pos.center = (self.x, self.y)
            rot_turret = pygame.transform.rotate(scaled_turret, -90 - self.angle - self.turretAngle)
            rect = rot_turret.get_rect()
            rect.center = pos.center
            pivot = (self.x - self.turretShift * self.scaleFactor, self.y)
            turret_pivot = pivot
            phi = math.radians(self.angle)
            pivot = (int(round(self.x + (pivot[0] - self.x) * math.cos(phi) - (pivot[1] - self.y) * math.sin(phi))),
                     int(round(self.y + (pivot[0] - self.x) * math.sin(phi) + (pivot[1] - self.y) * math.cos(phi))))
            phi = math.radians(self.angle + self.turretAngle)
            turret_pivot = (int(round(
                self.x + (turret_pivot[0] - self.x) * math.cos(phi) - (turret_pivot[1] - self.y) * math.sin(phi))),
                            int(round(self.y + (turret_pivot[0] - self.x) * math.sin(phi) + (
                                        turret_pivot[1] - self.y) * math.cos(phi))))
            rect.center = (rect.center[0] + pivot[0] - turret_pivot[0], rect.center[1] + pivot[1] - turret_pivot[1])
            self.screen.blit(rot_turret, rect)

    def move(self, other_tanks):
        if self.isDead:
            self.isMoving = False
            self.isRotating = False
            """
            if self.moveSound is not None:
                if self.moveSound.isPlaying():
                    self.moveSound.stop()
            """
            return
        turn_direction = -self.keyTurnLeft + self.keyTurnRight
        self.angle += turn_direction * self.angleStep
        self.angle %= 360
        turret_direction = -self.keyTurnTurretLeft + self.keyTurnTurretRight
        self.turretAngle += turret_direction * self.turretAngleStep
        self.turretAngle %= 360
        drive_direction = -self.keyDriveBackward + self.keyDriveForward
        old_x = self.x
        old_y = self.y
        self.x += drive_direction * self.speed * math.cos(math.radians(self.angle)) * self.scaleFactor
        self.y += drive_direction * self.speed * math.sin(math.radians(self.angle)) * self.scaleFactor
        if self.x < self.height * self.scaleFactor / 2:
            self.x = self.height * self.scaleFactor / 2
        if self.x > self.screen.get_width() - self.height * self.scaleFactor / 2:
            self.x = self.screen.get_width() - self.height * self.scaleFactor / 2
        if self.y < self.height * self.scaleFactor / 2:
            self.y = self.height * self.scaleFactor / 2
        if self.y > self.screen.get_height() - self.height * self.scaleFactor / 2:
            self.y = self.screen.get_height() - self.height * self.scaleFactor / 2
        self.x = int(round(self.x))
        self.y = int(round(self.y))
        for tank in other_tanks:
            d2 = (self.x - tank.x) ** 2 + (self.y - tank.y) ** 2
            col_d = (self.height + tank.height) * self.scaleFactor / 2
            if d2 < col_d ** 2:
                self.x = old_x
                self.y = old_y
                break
        for effect in self.containedEffects:
            effect.update()
        self.isMoving = drive_direction != 0
        self.isRotating = turn_direction != 0 and drive_direction == 0
        """
        if (self.isMoving or self.isRotating) and self.moveSound is not None:
            if not self.moveSound.isPlaying():
                self.moveSound.loop()
        elif self.moveSound is not None:
            if self.moveSound.isPlaying():
                self.moveSound.pause()
        """
        if self.shootCurrent > 0:
            self.shootCurrent -= 1
        if self.shootCurrent == 0 and self.keyShoot:
            self.shoot()

    def shoot(self):
        bullet_angle = self.angle + self.turretAngle
        bullet_x = int(round(
            self.x - self.turretShift * math.cos(
                math.radians(self.angle)) * self.scaleFactor + self.barrelLength * math.cos(
                math.radians(bullet_angle)) * self.scaleFactor))
        bullet_y = int(round(
            self.y - self.turretShift * math.sin(
                math.radians(self.angle)) * self.scaleFactor + self.barrelLength * math.sin(
                math.radians(bullet_angle)) * self.scaleFactor))
        self.bullets.append(MediumShell(self.screen, bullet_x, bullet_y, bullet_angle, self))
        self.effects.append(FlashA(bullet_x, bullet_y, bullet_angle, self.game))
        self.sounds.play("sound.shoot")
        self.shootCurrent = self.shootDelay

    def check_hit(self, bullet):
        phi = -1 * math.radians(self.angle)
        bullet_x1 = int(round(self.x + (bullet.x - self.x) * math.cos(phi) - (bullet.y - self.y) * math.sin(phi)))
        bullet_y1 = int(round(self.y + (bullet.x - self.x) * math.sin(phi) + (bullet.y - self.y) * math.cos(phi)))
        return self.x - self.height * self.scaleFactor / 2 <= bullet_x1 <= self.x + self.height * self.scaleFactor / 2 \
            and self.y - self.width * self.scaleFactor / 2 <= bullet_y1 <= self.y + self.width * self.scaleFactor / 2

    def hit(self, bullet):
        just_exploded = False
        if self.health > 0 and not self.isShielded:
            self.health -= 1
            if self.health == 0:
                self.effects.append(Explosion(self.x, self.y, self.game))
                self.sounds.play("sound.explosion")
                just_exploded = True
        if self.health == 0:
            self.isDead = True
        self.effects.append(HitA(bullet.x, bullet.y, bullet.angle + 90, self.game))
        if not just_exploded and not self.isShielded:
            self.sounds.play("sound.hit")

    def apply_power_up(self, effect):
        self.effects.append(effect)
        self.containedEffects.append(effect)
        effect.apply()

    def get_shield(self):
        if self.isShielded:
            for effect in self.containedEffects:
                if effect.get_type() == "EnergyShield":
                    return effect
        return None


class Player(Tank):
    def __init__(self, x, y, angle, game):
        super().__init__(x, y, angle, game)
        self.tankBody = game.sprites.get_sprite("player.tank.body")
        self.turret = game.sprites.get_sprite("player.tank.turret")
        self.tracks.append(game.sprites.get_sprite("player.tank.track.a"))
        self.tracks.append(game.sprites.get_sprite("player.tank.track.b"))


class Enemy(Tank):
    def __init__(self, x, y, angle, game):
        super().__init__(x, y, angle, game)
        self.tankBody = game.sprites.get_sprite("enemy.tank.body")
        self.turret = game.sprites.get_sprite("enemy.tank.turret")
        self.tracks.append(game.sprites.get_sprite("enemy.tank.track.a"))
        self.tracks.append(game.sprites.get_sprite("enemy.tank.track.b"))
