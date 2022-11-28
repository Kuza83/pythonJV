# -----------------
# CONSTANT VARIABLE
# -----------------

import pygame.sprite

DARK_GREY = (50, 50, 50)
MUSTARD = (209, 206, 25)
GREEN = (0, 255, 0)
SCREEN_SIZE = (700, 500)
FPS = 60

# ----
# INIT
# ----

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Mario Like")
clock = pygame.time.Clock()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# ----
# LOAD
# ----

#player
player_image = pygame.image.load("sprites/Mario_Idle0.png")
player_x = 300
player_y = 0
player_width = 20
player_height = 35

player_speed = 0
player_acceleration = 0.2

player_on_ground = True

score = 0
lives = 3

#enemy
enemy_image = pygame.image.load("images/spike_monster.png")
enemies = [
    pygame.Rect(100, 220, 50, 26)
]

#platform
platforms = [
    #middle
    pygame.Rect(100, 300, 400, 50),
    #left
    pygame.Rect(100, 250, 50, 50),
    #right
    pygame.Rect(450, 250, 50, 50)
]

#coin
coin_image = pygame.image.load("images/coin_0.png")
coins = [
    pygame.Rect(350, 270, 23, 23),
    pygame.Rect(200, 270, 23, 23)
]

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

    new_player_x = player_x
    new_player_y = player_y

    if keys[pygame.K_LEFT]:
        new_player_x -= 2
    if keys[pygame.K_RIGHT]:
        new_player_x += 2
    if keys[pygame.K_SPACE] and player_on_ground:
        player_speed = -5

    # ------
    # UPDATE
    # ------

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

    for e in enemies:
        if e.colliderect(player_rect):
            #enemies.remove(e)
            lives -= 1
            player_x = 300
            player_y = 0

    for c in coins:
        if c.colliderect(player_rect):
            coins.remove(c)
            score += 1

    # ----
    # DRAW
    # ----

    # background
    screen.fill(DARK_GREY)

    # platform
    for p in platforms:
        pygame.draw.rect(screen, MUSTARD, p)

    # coins
    for c in coins:
        screen.blit(coin_image, (c.x, c.y))

    # enemies
    for e in enemies:
        screen.blit(enemy_image, (e.x, e.y))

    # player
    screen.blit(player_image, (player_x, player_y))

    #ui
    score_text = font.render("Score : " + str(score), True, MUSTARD, DARK_GREY)
    score_text = score_text.get_rect()

    # present screen
    pygame.display.flip()

    clock.tick(FPS)

# ----
# QUIT
# ----

pygame.quit()
