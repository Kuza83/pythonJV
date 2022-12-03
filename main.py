# -----------------
# CONSTANT VARIABLE
# -----------------

import pygame
import engine


def drawtext(t, x, y):
    text = font.render(t, True, MUSTARD, DARK_GREY)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


DARK_GREY = (50, 50, 50)
MUSTARD = (209, 206, 25)
GREEN = (0, 255, 0)
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
font = pygame.font.Font(pygame.font.get_default_font(), 24)

game_state = "playing"

# ----
# LOAD
# ----

# player
player_image = pygame.image.load("sprites/Mario_Idle0.png")
player_x = 300
player_y = 0
player_width = 40
player_height = 70

player_speed = 0
player_acceleration = 0.2
player_direction = ""
player_state = ""

player_on_ground = True

player_animation = engine.Animation([
    pygame.image.load("sprites/Mario_Idle0.png"),
    pygame.image.load("sprites/Mario_Idle1.png"),
    pygame.image.load("sprites/Mario_Idle2.png"),
    pygame.image.load("sprites/Mario_Idle3.png")
])

# UI
score = 0

# enemy
enemy_image = pygame.image.load("images/spike_monster.png")
enemies = [
    pygame.Rect(100, 220, 50, 26)
]

# platform
platforms = [
    #middle
    pygame.Rect(100, 300, 400, 50),
    #left
    pygame.Rect(100, 250, 50, 50),
    #right
    pygame.Rect(450, 250, 50, 50)
]

# coin
coin_image = pygame.image.load("images/coin_0.png")
coin_animation = engine.Animation([
    pygame.image.load("images/coin_0.png"),
    pygame.image.load("images/coin_1.png"),
    pygame.image.load("images/coin_2.png"),
    pygame.image.load("images/coin_3.png"),
    pygame.image.load("images/coin_4.png"),
    pygame.image.load("images/coin_5.png")
])
coins = [
    pygame.Rect(350, 270, 23, 23),
    pygame.Rect(200, 270, 23, 23)
]

# lives
lives_image = pygame.image.load("images/heart.png")
lives = 3

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

        new_player_x = player_x
        new_player_y = player_y

        if keys[pygame.K_LEFT]:
            new_player_x -= 3
            player_direction = "left"
        if keys[pygame.K_RIGHT]:
            new_player_x += 3
            player_direction = "right"
        if keys[pygame.K_SPACE] and player_on_ground:
            player_speed = -6

        # ------
        # UPDATE
        # ------

    if game_state == "playing":

        # platform collision
        new_player_rect = pygame.Rect(new_player_x, player_y, player_width, player_height)
        x_collision = False

        for p in platforms:
            if p.colliderect(new_player_rect):
                x_collision = True
                break

        if not x_collision:
            player_x = new_player_x

        player_speed += player_acceleration
        new_player_y += player_speed

        new_player_rect = pygame.Rect(player_x, new_player_y, player_width, player_height)

        y_collision = False
        player_on_ground = False

        for p in platforms:
            if p.colliderect(new_player_rect):
                y_collision = True
                player_speed = 0
                if p[1] > new_player_y:
                    player_y = p[1] - player_height
                    player_on_ground = True

        if not y_collision:
            player_y = new_player_y

        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        if player_y > 500:
            player_x = 300
            player_y = -50
            lives -= 1
            player_speed = 0

        # enemies collision
        for e in enemies:
            if e.colliderect(player_rect):
                #enemies.remove(e)
                lives -= 1
                player_x = 300
                player_y = -50
                player_speed = 0

        # alive ?
        if lives <= 0:
            game_state = "lose"

        # coin collect
        for c in coins:
            if c.colliderect(player_rect):
                coins.remove(c)
                score += 1
                if score >= 2:
                    game_state = "win"

        coin_animation.update(10)
        player_animation.update(12)

    # ----
    # DRAW
    # ----

    # background
    screen.fill(DARK_GREY)

    if game_state == "playing":

        # platform
        for p in platforms:
            pygame.draw.rect(screen, MUSTARD, p)

        # coins
        for c in coins:
            coin_animation.draw(screen, c.x, c.y)

        # enemies
        for e in enemies:
            screen.blit(enemy_image, (e.x, e.y))

        # player
        if player_direction == "":
            player_animation.draw(screen, player_x, player_y)
        elif player_direction == "right":
            screen.blit(player_image, (player_x, player_y))
        elif player_direction == "left":
            screen.blit(pygame.transform.flip(player_image, True, False), (player_x, player_y))

        # score
        screen.blit(coin_image, (600, 10))
        drawtext(str(score), 633, 10)

        # heart
        for h in range(lives):
            screen.blit(lives_image, (10 + (h*30), 10))

    if game_state == "win":
        drawtext("You win !!", 10, 10)

    if game_state == "lose":
        drawtext("You lose !!", 10, 10)

    # present screen
    pygame.display.flip()

    clock.tick(FPS)


# ----
# QUIT
# ----

pygame.quit()
