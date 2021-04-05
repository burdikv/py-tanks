import pygame
import os


class Sprites(object):
    def __init__(self):
        self.sprites = {}
        self.sprites["player.tank.body"] = pygame.image.load(os.path.join("Sprites", "Hulls_Color_B", "Hull_01.png")).convert()
        self.sprites["player.tank.turret"] = pygame.image.load(os.path.join("Sprites", "Weapon_Color_B", "Gun_01.png")).convert()
        pathTracks = os.path.join("Sprites", "Tracks")
        self.sprites["player.tank.track.a"] = pygame.image.load(os.path.join(pathTracks, "Track_2_A.png")).convert()
        self.sprites["player.tank.track.b"] = pygame.image.load(os.path.join(pathTracks, "Track_2_B.png")).convert()
        path = os.path.join("Sprites", "Hulls_Color_D")
        self.sprites["enemy.tank.body"] = pygame.image.load(os.path.join("Sprites", "Hulls_Color_D", "Hull_01.png")).convert()
        self.sprites["enemy.tank.turret"] = pygame.image.load(os.path.join("Sprites", "Weapon_Color_D", "Gun_01.png")).convert()
        self.sprites["enemy.tank.track.a"] = pygame.image.load(os.path.join(pathTracks, "Track_2_A.png")).convert()
        self.sprites["enemy.tank.track.b"] = pygame.image.load(os.path.join(pathTracks, "Track_2_B.png")).convert()
        path = os.path.join("Sprites", "Effects")
        self.sprites["shell.medium"] = pygame.image.load(os.path.join(path, "Medium_Shell.png")).convert()
        path2 = os.path.join(path, "Sprites")
        for i in range(9):
            self.sprites["explosion." + str(i)] = pygame.image.load(os.path.join(path2, f"Sprite_Effects_Explosion_00{i}.png")).convert()
        for i in range(4):
            self.sprites["shot.flame.a." + str(i)] = pygame.image.load(os.path.join(path2, f"Sprite_Fire_Shots_Shot_A_00{i}.png")).convert()
        for i in range(4):
            self.sprites["shot.hit.a." + str(i)] = pygame.image.load(os.path.join(path2, f"Sprite_Fire_Shots_Impact_A_00{i}.png")).convert()

        # this is true for current sprites, if other sprites appear in future, they might need another transparency color
        for name in self.sprites:
            self.sprites[name].set_colorkey((0, 0, 0), pygame.RLEACCEL)

        # special transparency for these sprites is needed
        self.sprites["any.tank.energyshield"] = pygame.image.load(os.path.join(path, "shield.png")).convert_alpha()
        self.sprites["any.tank.energyshield.a"] = pygame.image.load(os.path.join(path, "spr_shield.png")).convert_alpha()

    def get_sprite(self, name):
        if name in self.sprites:
            return self.sprites[name]
        else:
            return None


class PivotSprite(pygame.sprite.Sprite):
    @staticmethod
    def surface_rotate(image, pos, origin_pos, angle):
        # calculate the axis aligned bounding box of the rotated image
        w, h = image.get_size()
        box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot
        pivot = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = (
            pos[0] - origin_pos[0] + min_box[0] - pivot_move[0], pos[1] - origin_pos[1] - max_box[1] + pivot_move[1])

        # get a rotated image
        rotated_image = pygame.transform.rotate(image, angle)

        return rotated_image, origin
