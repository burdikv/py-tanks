import random


class AI(object):
    def __init__(self):
        self.timer = 20

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
