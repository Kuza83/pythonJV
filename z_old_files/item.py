import pygame

import player

vec = pygame.math.Vector2

heightItem = 10
widthItem = 10

BLUE = (0, 0, 255)


class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((widthItem, heightItem))
        self.surf.fill(BLUE)
        self.rect = self.surf.get_rect()

        self.rect.x = 300
        self.rect.y = 565
