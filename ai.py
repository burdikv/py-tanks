import random
import math


class AI(object):
    def __init__(self, game):
        self.timer = 20
        self.game = game
        self.tank = None
        self.visionRadius = 500
        self.target = None
        self.prevTarget = None
        self.targetDistance = 0

    def set_tank(self, tank):
        self.tank = tank

    def control(self):
        vision_radius_sqr = self.visionRadius ** 2
        if self.target is not None:
            if self.target.isDead or vision_radius_sqr < (self.target.x - self.tank.x) ** 2 + (self.target.y - self.tank.y) ** 2:
                self.prevTarget = self.target
                self.target = None
        if self.target is None:
            potential_targets = [self.game.player]
            for e in self.game.enemies:
                if e != self.tank and not e.isDead:
                    potential_targets.append(e)
            min_distance_sqr = vision_radius_sqr
            target_ref = None
            for i, t in enumerate(potential_targets):
                d_sqr = (t.x - self.tank.x) ** 2 + (t.y - self.tank.y) ** 2
                if vision_radius_sqr < d_sqr:
                    potential_targets.pop(i)
                elif d_sqr < min_distance_sqr:
                    min_distance_sqr = d_sqr
                    target_ref = t
            if target_ref is not None:
                self.target = target_ref
                self.targetDistance = math.sqrt(min_distance_sqr)
        if self.target is None:
            self.move(self.tank)
        else:
            self.full_stop()
            target_angle = math.degrees(math.atan2(self.target.y - self.tank.y, self.target.x - self.tank.x)) % 360
            aim_angle = (self.tank.angle + self.tank.turretAngle) % 360
            if math.fabs(target_angle - aim_angle) > 180:
                if aim_angle < target_angle:
                    aim_angle += 360
                else:
                    target_angle += 360
            half_cone_angle = math.degrees(math.atan2(self.target.width * self.target.scaleFactor / 2, self.targetDistance))
            if math.fabs(target_angle - aim_angle) <= half_cone_angle:
                self.aim_stop()
                self.tank.keyShoot = True
            elif target_angle > aim_angle:
                self.aim_right()
            elif target_angle < aim_angle:
                self.aim_left()
            # print(target_angle, aim_angle, half_cone_angle)

    def aim_left(self):
        self.tank.keyTurnTurretLeft = True
        self.tank.keyTurnTurretRight = False

    def aim_right(self):
        self.tank.keyTurnTurretLeft = False
        self.tank.keyTurnTurretRight = True

    def aim_stop(self):
        self.tank.keyTurnTurretLeft = False
        self.tank.keyTurnTurretRight = False

    def full_stop(self):
        self.tank.keyTurnRight = False
        self.tank.keyTurnLeft = False
        self.tank.keyDriveForward = False
        self.tank.keyDriveBackward = False
        self.tank.keyTurnTurretLeft = False
        self.tank.keyTurnTurretRight = False
        self.tank.keyShoot = False

    def move(self, tank):
        tank.keyTurnTurretRight = True
        tank.keyDriveForward = True
        tank.keyShoot = True

        self.timer -= 1

        if self.timer <= 0:
            self.timer = random.randint(10, 60)

            self.do_random(tank)

    def do_random(self, tank):
        a = random.randint(0, 5)
        if a == 0:
            tank.keyTurnTurretRight = True
            tank.keyTurnTurretLeft = False
        elif a == 1:
            tank.keyTurnTurretRight = False
            tank.keyTurnTurretLeft = True
        elif a == 2:
            tank.keyTurnRight = True
            tank.keyTurnLeft = False
        elif a == 3:
            tank.keyTurnRight = False
            tank.keyTurnLeft = True
        elif a == 4:
            tank.keyTurnRight = False
            tank.keyTurnLeft = False
