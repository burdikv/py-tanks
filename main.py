import gc
import pygame
from game import Game
from tank import Player
from tank import Enemy
from clock import Clock
from effects import EnergyShield

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FRAME_RATE = 60
SCALE_FACTOR = 0.25

global _game

pygame.mixer.init()
pygame.init()
clock = Clock(FRAME_RATE)
programIcon = pygame.image.load('battle-tank.png')
pygame.display.set_icon(programIcon)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tanks")
width = screen.get_width()
height = screen.get_height()


def setup():
    global _game
    _game = Game(screen, clock, SCALE_FACTOR)
    _game.player = Player(width / 2, height / 2, -90, _game)
    _game.enemies.append(Enemy(width / 4, height / 2, 180, _game))
    _game.enemies.append(Enemy(3 * width / 4, height / 2, 0, _game))

    _game.player.apply_power_up(EnergyShield(-1, _game.player, _game))


def restart():
    global _game
    del _game
    gc.collect()
    setup()


setup()
running = True
while running:
    key = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYDOWN:
            key = event.key

    pressed_keys = pygame.key.get_pressed()
    if _game.ui.state == _game.ui.gameplay:
        _game.player.keyShoot = pressed_keys[pygame.K_SPACE]
        _game.player.keyTurnLeft = pressed_keys[pygame.K_a]
        _game.player.keyTurnRight = pressed_keys[pygame.K_d]
        _game.player.keyDriveForward = pressed_keys[pygame.K_w]
        _game.player.keyDriveBackward = pressed_keys[pygame.K_s]
        _game.player.keyTurnTurretLeft = pressed_keys[pygame.K_LEFT]
        _game.player.keyTurnTurretRight = pressed_keys[pygame.K_RIGHT]

    if _game.ui.state == _game.ui.gamestart:
        if key == pygame.K_SPACE:
            _game.ui.state = _game.ui.gameplay
    elif _game.ui.state == _game.ui.gameplay:
        if key == pygame.K_p:
            _game.ui.state = _game.ui.pause
    elif _game.ui.state == _game.ui.pause:
        if key == pygame.K_p or key == pygame.K_SPACE:
            _game.ui.state = _game.ui.gameplay
        if key == pygame.K_r:
            _game.ui.state = _game.ui.gamestart
            restart()
            continue
    elif _game.ui.state == _game.ui.gameover or _game.ui.state == _game.ui.gamewin:
        if key == pygame.K_r:
            _game.ui.state = _game.ui.gamestart
            restart()
            continue

    screen.fill((255, 255, 255))

    # tank
    if _game.ui.state == _game.ui.gameplay:
        _game.player.move(_game.enemies)
    _game.player.render()
    # enemies
    enemiesCount = len(_game.enemies)
    for enemy in _game.enemies:
        if _game.ui.state == _game.ui.gameplay:
            otherTanks = [_game.player]
            for e in _game.enemies:
                if e != enemy:
                    otherTanks.append(e)
            if _game.ui.state == _game.ui.gameplay:
                _game.ai.move(enemy)
            enemy.move(otherTanks)
        enemy.render()
        if enemy.isDead:
            enemiesCount -= 1
    if enemiesCount <= 0:
        _game.ui.state = _game.ui.gamewin
    # bullets
    for i, bullet in enumerate(_game.bullets):
        destroy = False
        if bullet.x < 0 or bullet.x >= width or bullet.y < 0 or bullet.y >= height:
            destroy = True
        else:
            allTanks = [_game.player]
            for e in _game.enemies:
                allTanks.append(e)
            for t in allTanks:
                if bullet.tank == t:
                    continue
                shield = t.get_shield()
                if shield is not None:
                    if shield.check_hit(bullet):
                        shield.hit(bullet)
                        destroy = True
                        break
                elif t.check_hit(bullet):
                    t.hit(bullet)
                    if _game.player.isDead:
                        _game.ui.state = _game.ui.gameover
                    destroy = True
                    break
        if destroy:
            bullet.isDestroyed = True
            _game.bullets.pop(i)
        if _game.ui.state == _game.ui.gameplay:
            bullet.update()
        bullet.render()
    # effects
    effectCount = len(_game.effects)
    while effectCount > 0:
        effect = _game.effects[effectCount - 1]
        effect.render()
        if effect.isFinished:
            _game.effects.remove(effect)
        effectCount -= 1
    # ui
    _game.ui.render()

    pygame.display.flip()
    clock.tick_default()

pygame.mixer.quit()
pygame.quit()
