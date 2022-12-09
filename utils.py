
import pygame
import engine


MUSTARD = (209, 206, 25)
BLACK = (0, 0, 0)
DARK_GREY = (50, 50, 50)

pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 24)

# lives
lives_image = pygame.image.load("images/heart.png")


def drawtext(screen, t, x, y):
    text = font.render(t, True, MUSTARD)
    text_rect = text.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text, text_rect)


coin0 = pygame.image.load("images/coin_0.png")
coin1 = pygame.image.load("images/coin_1.png")
coin2 = pygame.image.load("images/coin_2.png")
coin3 = pygame.image.load("images/coin_3.png")
coin4 = pygame.image.load("images/coin_4.png")
coin5 = pygame.image.load("images/coin_5.png")


def makeCoin(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 23, 23)
    entityAnimation = engine.Animation([coin0, coin1, coin2, coin3, coin4, coin5])
    entity.animations.add("idle", entityAnimation)
    entity.type = "collectable"
    return entity


enemy0 = pygame.image.load("images/spike_monster.png")


def makeEnemy(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 50, 26)
    entityAnimation = engine.Animation([enemy0])
    entity.animations.add("idle", entityAnimation)
    entity.type = "dangerous"
    return entity


idle0 = pygame.image.load("sprites/Mario_Idle0.png")
idle1 = pygame.image.load("sprites/Mario_Idle1.png")
idle2 = pygame.image.load("sprites/Mario_Idle2.png")
idle3 = pygame.image.load("sprites/Mario_Idle3.png")

walking0 = pygame.image.load("sprites/Mario_Run0.png")
walking1 = pygame.image.load("sprites/Mario_Run1.png")
walking2 = pygame.image.load("sprites/Mario_Run2.png")
walking3 = pygame.image.load("sprites/Mario_Run3.png")
walking4 = pygame.image.load("sprites/Mario_Run4.png")
walking5 = pygame.image.load("sprites/Mario_Run5.png")
walking6 = pygame.image.load("sprites/Mario_Run6.png")
walking7 = pygame.image.load("sprites/Mario_Run7.png")


def makePlayer(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 40, 70)
    entityIdleAnimation = engine.Animation([idle0, idle1, idle2, idle3])
    entityWalkingAnimation = engine.Animation([walking0, walking1, walking2, walking3, walking4, walking5, walking6, walking7])
    entity.animations.add("idle", entityIdleAnimation)
    entity.animations.add("walking", entityWalkingAnimation)
    entity.type = "player"
    return entity
