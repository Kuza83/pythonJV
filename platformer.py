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
game_state = "playing"

# ----
# LOAD
# ----


entities = []

# player
player_acceleration = 0.2

player_on_ground = True

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

    if game_state == "playing":

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        if keys[pygame.K_SPACE] and player_on_ground:
            player.speed = -6
        elif keys[pygame.K_LEFT]:
            new_player_x -= 3
            player.direction = "left"
            player.state = "walking"
        elif keys[pygame.K_RIGHT]:
            new_player_x += 3
            player.direction = "right"
            player.state = "walking"
        else:
            player.state = "idle"
        # zoom control
        # zoom in
        if keys[pygame.K_z]:
            player.camera.zoomLevel += 0.01

        if keys[pygame.K_d]:
            player.camera.zoomLevel -= 0.01

        # ------
        # UPDATE
        # ------

    if game_state == "playing":

        # update animations
        for entity in globals.world.entities:
            entity.animations.animationList[entity.state].update()

        # platform collision
        new_player_rect = pygame.Rect(int(new_player_x), int(player.position.rect.y), player.position.rect.width,
                                      player.position.rect.height)
        x_collision = False

        for p in globals.world.platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if not x_collision:
            player.position.rect.x = new_player_x

        player.speed += player_acceleration
        new_player_y += player.speed

        new_player_rect = pygame.Rect(int(player.position.rect.x), int(new_player_y), player.position.rect.width,
                                      player.position.rect.height)

        y_collision = False
        player_on_ground = False

        for p in globals.world.platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player.speed = 0
                if p[1] > new_player_y:
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True

        if not y_collision:
            player.position.rect.y = new_player_y

        if player.position.rect.y > 500:
            player.position.rect.x = 300
            player.position.rect.y = -50
            player.battle.lives -= 1
            player.speed = 0

    clock.tick(globals.FPS)

# ----
# QUIT
# ----

pygame.quit()
