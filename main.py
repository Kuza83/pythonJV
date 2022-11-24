import pygame


# -----------------
# CONSTANT VARIABLE
# -----------------

DARK_GREY = (50, 50, 50)
MUSTARD = (209, 206, 25)
SCREEN_SIZE = (700, 500)

# ----
# INIT
# ----

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Mario Like")

player_image = pygame.image.load("sprites/Mario_Idle0.png")

middle_platform = pygame.Rect(100, 300, 400, 50)
left_platform = pygame.Rect(100, 250, 50, 50)
right_platform = pygame.Rect(450, 250, 50, 50)

running = True

# ---------
# GAME LOOP
# ---------

while running:

    # -----
    # INPUT
    # -----

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ------
    # UPDATE
    # ------


    # ----
    # DRAW
    # ----

    # background
    screen.fill(DARK_GREY)

    # platform
    pygame.draw.rect(screen, MUSTARD, middle_platform)
    pygame.draw.rect(screen, MUSTARD, left_platform)
    pygame.draw.rect(screen, MUSTARD, right_platform)


    # player
    screen.blit(player_image, (300, 100))

    # present screen
    pygame.display.flip()

# ----
# QUIT
# ----

pygame.quit()
