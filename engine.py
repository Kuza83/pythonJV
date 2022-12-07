import pygame


class System:
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen, entities, platforms):
        for entity in entities:
            if self.check(entity):
                self.updateEntity(screen, entity, entities, platforms)

    def updateEntity(self, screen, entity, entities, platforms):
        pass


MUSTARD = (209, 206, 25)
BLACK = (0, 0, 0)


class CameraSystem(System):
    def __init__(self):
        super(CameraSystem, self).__init__()

    def check(self, entity):
        return entity.camera is not None

    def updateEntity(self, screen, entity, entities, platforms):

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # update cam if tracking entity
        if entity.camera.entityToTrack is not None:

            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w/2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h/2

            entity.camera.worldX = (currentX * 0.90) + (targetX * 0.1)
            entity.camera.worldY = (currentY * 0.90) + (targetY * 0.1)

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w/2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h/2 - (entity.camera.worldY * entity.camera.zoomLevel)

        #fill camera background
        screen.fill(BLACK)

        # Draw platforms
        for p in platforms:
            newPosRect = pygame.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y* entity.camera.zoomLevel) + offsetY,
                p.w ,
                p.h )
            pygame.draw.rect(screen, MUSTARD, newPosRect)

        # Draw entities
        for e in entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen, e.position.rect.x + offsetX, e.position.rect.y + offsetY, e.direction == "left", False, entity.camera.zoomLevel)

        # unset clipping rectangle
        screen.set_clip(None)


class Camera:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.worldX = 0
        self.worldY = 0
        self.entityToTrack = None
        self.zoomLevel = 1

    def setWorldPos(self, x, y):
        self.worldX = x
        self.worldY = y

    def trackEntity(self, e):
        self.entityToTrack = e


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

    def draw(self, screen, x, y, flipX, flipY, zoomLevel):
        image = self.imageList[self.imageIndex]
        newWidth = image.get_rect().w * zoomLevel
        newHeight = image.get_rect().h * zoomLevel
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))


class Entity:
    def __init__(self):
        self.state = "idle"
        self.type = "normal"
        self.position = None
        self.animations = Animations()
        self.direction = "right"
        self.camera = None
