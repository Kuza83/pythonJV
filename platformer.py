# -----------------
# CONSTANT VARIABLE
# -----------------

import pygame
import engine
import utils
import level

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
FPS = 60

# ----
# INIT
# ----

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Mario Like")
clock = pygame.time.Clock()


game_state = "playing"

# ----
# LOAD
# ----


entities = []

# player
player_speed = 0
player_acceleration = 0.2

player_on_ground = True

player = utils.makePlayer(300, 0)
entities.append(player)

player.camera = engine.Camera(10, 10, 400, 400)
player.camera.setWorldPos(300, 0)
player.camera.trackEntity(player)

player.score = engine.Score()
player.battle = engine.Battle()

# enemy
enemy = utils.makeEnemy(100, 220)
enemy.camera = engine.Camera(420, 10, 200, 200)
enemy.camera.setWorldPos(150, 250)
entities.append(enemy)

# platform
# platforms = [
#     #middle
#     pygame.Rect(100, 300, 400, 50),
#     #left
#     pygame.Rect(100, 250, 50, 50),
#     #right
#     pygame.Rect(450, 250, 50, 50)
# ]

# coin
entities.append(utils.makeCoin(350, 270))
entities.append(utils.makeCoin(250, 270))

# camera
cameraSys = engine.CameraSystem()

level1 = level.Level(
    platforms=[
        # middle
        pygame.Rect(100, 300, 400, 50),
        # left
        pygame.Rect(100, 250, 50, 50),
        # right
        pygame.Rect(450, 250, 50, 50)
    ],
    entities=[
        player, enemy
    ]
)

world = level1

running = True

# ---------
# GAME LOOP
# ---------

while running:

    # -----
    # INPUT
    # -----

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_ESCAPE]:
        running = False

    if game_state == "playing":

        new_player_x = player.position.rect.x
        new_player_y = player.position.rect.y

        if keys[pygame.K_SPACE] and player_on_ground:
            player_speed = -6
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
        for entity in world.entities:
            entity.animations.animationList[entity.state].update()

        # platform collision
        new_player_rect = pygame.Rect(int(new_player_x), int(player.position.rect.y), player.position.rect.width, player.position.rect.height)
        x_collision = False

        for p in world.platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if not x_collision:
            player.position.rect.x = new_player_x

        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(int(player.position.rect.x), int(new_player_y), player.position.rect.width, player.position.rect.height)

        y_collision = False
        player_on_ground = False

        for p in world.platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                if p[1] > new_player_y:
                    player.position.rect.y = p[1] - player.position.rect.height
                    player_on_ground = True

        if not y_collision:
            player.position.rect.y = new_player_y

        player_rect = pygame.Rect(int(player.position.rect.x), int(player.position.rect.y), player.position.rect.width, player.position.rect.height)

        if player.position.rect.y > 500:
            player.position.rect.x = 300
            player.position.rect.y = -50
            player.battle.lives -= 1
            player_speed = 0

        # alive ?
        if player.battle.lives <= 0:
            game_state = "lose"

        # collectible system
        for entity in world.entities:
            if entity.type == "collectable":
                if entity.position.rect.colliderect(player_rect):
                    world.entities.remove(entity)
                    player.score.score += 1
                    if player.score.score >= 3:
                        game_state = "win"

        # enemy system
        for entity in world.entities:
            if entity.type == "dangerous":
                if entity.position.rect.colliderect(player_rect):
                    player.battle.lives -= 1
                    player.position.rect.x = 300
                    player.position.rect.y = -50
                    player_speed = 0

    # ----
    # DRAW
    # ----

    # background
    screen.fill(utils.DARK_GREY)

    cameraSys.update(screen, world.entities, world.platforms)
    #
    # if game_state == "win":
    #     drawtext("You win !!", 10, 10)
    #
    # if game_state == "lose":
    #     drawtext("You lose !!", 10, 10)

    # present screen
    pygame.display.flip()
    clock.tick(FPS)

# ----
# QUIT
# ----

pygame.quit()
