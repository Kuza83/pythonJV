import pygame


class System:
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def _update(self, screen, entity, entities, platforms):
        for entity in entities:
            if self.check(entity):
                self.update(screen, entity, entities, platforms)

    def update(self, screen, entity, entities, platforms):
        pass


MUSTARD = (209, 206, 25)


class CameraSystem(System):
    def __init__(self):
        super(CameraSystem, self).__init__()

    def check(self, entity):
        return entity.camera is not None

    def update(self, screen, entity, entities, platforms):
        for p in platforms:
            pygame.draw.rect(screen, MUSTARD, p)


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class Position:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class Animations:
    def __init__(self):
        self.animationList = {}

    def add(self, state, animation):
        self.animationList[state] = animation


class Animation:
    def __init__(self, imageList):
        self.imageList = imageList
        self.imageIndex = 0
        self.animationTimer = 0
        self.animationSpeed = 5

    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:
            self.animationTimer = 0
            self.imageIndex += 1
            if self.imageIndex > len(self.imageList) - 1:
                self.imageIndex = 0

    def draw(self, screen, x, y, flipX, flipY):
        screen.blit(pygame.transform.flip(self.imageList[self.imageIndex], flipX, flipY), (x, y))


class Entity:
    def __init__(self):
        self.state = "idle"
        self.type = "normal"
        self.position = None
        self.animations = Animations()
        self.direction = "right"
        self.camera = None
