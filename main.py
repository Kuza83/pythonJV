import sys

import pygame
from pygame.locals import *

import item
import platform
import player
import scene


# ----
# LOAD
# ----

pygame.init()

HEIGHT = 600
WIDTH = 800
FPS = 60

RED = (255, 0, 0)
BLACK = (0, 0, 0)

FramePerSec = pygame.time.Clock()

displaySurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

PT1 = platform.Platform()
P1 = player.Player()
IT1 = item.Item()

allSprites = pygame.sprite.Group()
allSprites.add(P1)
allSprites.add(PT1)
allSprites.add(IT1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

items = pygame.sprite.Group()
items.add(IT1)

running = True

sceneManager = scene.SceneManager()
mainMenu = scene.MainMenuScene()
level1 = scene.GameScene()
sceneManager.push(mainMenu)


# ---------
# GAME LOOP
# ---------

while running:

    sceneManager.input()
    sceneManager.update()
    sceneManager.draw()

    # -----
    # INPUT
    # -----

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and player.Player.updateCollidePT(P1, platforms):
                P1.jump()
            if event.key == pygame.K_SPACE and P1.state == "DOUBLE JUMP":
                P1.doubleJump()

    # ------
    # UPDATE
    # ------

    P1.move()
    IT1.update()

    player.Player.updateCollidePT(P1, platforms)

    if player.Player.updateCollide(P1, items):
        P1.state = "DOUBLE JUMP"

    # ----
    # DRAW
    # ----

    displaySurface.fill(BLACK)

    for entity in allSprites:
        displaySurface.blit(entity.surf, entity.rect)

    font = pygame.font.SysFont("Arial", 20)
    score = font.render(str(P1.nbJump), True, RED)
    displaySurface.blit(score, (10, 10))

    posP1x = font.render(str(int(P1.pos.x)), True, RED)
    posP1y = font.render(str(int(P1.pos.y)), True, RED)
    displaySurface.blit(posP1x, (10, 50))
    displaySurface.blit(posP1y, (10, 70))

    playerState = font.render(P1.state, True, RED)
    displaySurface.blit(playerState, (10, 90))

    pygame.display.update()
    FramePerSec.tick(FPS)


pygame.quit()
sys.exit()
