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

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
sceneManager.push(mainMenu)

inputStream = input.InputStream()

# create player
globals.player1 = utils.makePlayer(300, 0)
globals.player1.camera = engine.Camera(10, 10, 400, 400)
globals.player1.camera.setWorldPos(300, 0)
globals.player1.camera.trackEntity(globals.player1)
globals.player1.input = engine.Input(pygame.K_SPACE, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_z, pygame.K_d)


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
