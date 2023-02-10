# -----------------
# CONSTANT VARIABLE
# -----------------

import pygame
import engine
import utils
import level
import scene
import globals
import input


# ----
# INIT
# ----

pygame.init()
screen = pygame.display.set_mode(globals.SCREEN_SIZE)
pygame.display.set_caption("Mario Like")
clock = pygame.time.Clock()

# ----
# LOAD
# ----

entities = []

# player

player = utils.makePlayer(300, 0)

player.camera = engine.Camera(10, 10, 400, 400)
player.camera.setWorldPos(300, 0)
player.camera.trackEntity(player)

player.score = engine.Score()
player.battle = engine.Battle()

player.input = engine.Input(pygame.K_SPACE, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_z, pygame.K_d)
player.intention = engine.Intention()

# enemy
enemy = utils.makeEnemy(100, 220)
enemy.camera = engine.Camera(420, 10, 200, 200)
enemy.camera.setWorldPos(150, 250)

# coin
coin1 = utils.makeCoin(350, 270)
coin2 = utils.makeCoin(250, 270)
coin3 = utils.makeCoin(280, 270)
entities.append(coin1)
entities.append(coin2)

# camera
cameraSys = engine.CameraSystem()


def lostLevel(levels):
    for entity in levels.entities:
        if entity.type == "player":
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    return True


def wonLevel(levels):
    for entity in levels.entities:
        if entity.type == "player":
            if entity.score.score is not None:
                if entity.score.score == 3:
                    return True
    return False


globals.levels[1] = level.Level(
    platforms=[
        # middle
        pygame.Rect(100, 300, 400, 50),
        # left
        pygame.Rect(100, 250, 50, 50),
        # right
        pygame.Rect(450, 250, 50, 50)
    ],
    entities=[
        player, enemy, coin1, coin2, coin3
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)

globals.levels[2] = level.Level(
    platforms=[
        # middle
        pygame.Rect(100, 300, 400, 50)
    ],
    entities=[
        player, coin1, coin2, coin3
    ],
    winFunc=wonLevel,
    loseFunc=lostLevel
)


globals.world = globals.levels[1]

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = input.InputStream()

running = True

# ---------
# GAME LOOP
# ---------

while running:

    inputStream.processInput()

    if sceneManager.isEmpty():
        running = False

    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    # -----
    # INPUT
    # -----

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
        running = False

    clock.tick(globals.FPS)

# ----
# QUIT
# ----

pygame.quit()
