import pygame

vec = pygame.math.Vector2

HEIGHT = 600
WIDTH = 800
ACC = 0.5
FRIC = -0.12
RED = (255, 0, 0)

widthSurface = 30
heightSurface = 30
centerSurface = (widthSurface / 2, heightSurface / 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((widthSurface, heightSurface))
        self.surf.fill((128, 255, 40))
        self.rect = self.surf.get_rect()
        self.surfCenter = pygame.draw.circle(self.surf, RED, centerSurface, 2.5)

        self.pos = vec(10, 385)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.nbJump = 0

        self.state = ""

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[pygame.K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH - widthSurface / 2:
            self.pos.x = WIDTH - widthSurface / 2
        if self.pos.x < widthSurface / 2:
            self.pos.x = widthSurface / 2

        self.rect.midbottom = self.pos

    def doubleJump(self):
        self.nbJump += 1
        if self.state == "DOUBLE JUMP":
            if self.nbJump <= 2:
                self.vel.y = -15

    def jump(self):
        self.vel.y = -15

    def updateCollide(self, groupsprite):
        hits = pygame.sprite.spritecollide(self, groupsprite, False)
        return hits

    def updateCollidePT(self, groupsprite):
        hitsGround = pygame.sprite.spritecollide(self, groupsprite, False)
        if hitsGround:
            self.pos.y = hitsGround[0].rect.top + 1
            self.vel.y = 0
            self.nbJump = 0
        return hitsGround
