import pygame
import utils
import globals


class System:
    def __init__(self):
        pass

    def check(self, entity):
        return True

    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen, inputStream, entity)

    def updateEntity(self, screen, inputStream, entity):
        pass


class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None

    def updateEntity(self, screen, inputStream, entity):
        entity.animations.animationList[entity.state].update()


class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None

    def updateEntity(self, screen, inputStream, entity):
        new_x = entity.position.rect.x
        new_y = entity.position.rect.y

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 3
                entity.direction = "left"
                entity.state = "walking"
            if entity.intention.moveRight:
                new_x += 3
                entity.direction = "right"
                entity.state = "walking"
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = "idle"
            if entity.intention.jump and entity.on_ground:
                entity.speed = -5

            new_x_rect = pygame.Rect(
                int(new_x),
                int(entity.position.rect.y),
                entity.position.rect.width,
                entity.position.rect.height)

            x_collision = False

            for platform in globals.world.platforms:
                if platform.colliderect(new_x_rect):
                    x_collision = True
                    break

            if not x_collision:
                entity.position.rect.x = new_x

            entity.speed += entity.acceleration
            new_y += entity.speed

            new_y_rect = pygame.Rect(
                int(entity.position.rect.x),
                int(new_y),
                entity.position.rect.width,
                entity.position.rect.height)

            y_collision = False
            entity.on_ground = False

            for platform in globals.world.platforms:
                if platform.colliderect(new_y_rect):
                    y_collision = True
                    entity.speed = 0
                    if platform[1] > new_y:
                        entity.position.rect.y = platform[1] - entity.position.rect.height
                        entity.on_ground = True

            if not y_collision:
                entity.position.rect.y = int(new_y)

            # reset intentions
            if entity.intention is not None:
                entity.intention.moveLeft = False
                entity.intention.moveRight = False
                entity.intention.jump = False


class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None

    def updateEntity(self, screen, inputStream, entity):
        # Jump
        if inputStream.keyboard.isKeyDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # Move Left
        if inputStream.keyboard.isKeyDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # Move Right
        if inputStream.keyboard.isKeyDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # Zoom In
        if inputStream.keyboard.isKeyDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False
        # Zoom Out
        if inputStream.keyboard.isKeyDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False


class CollectionSystem(System):
    def check(self, entity):
        return entity.type == "player" and entity.score is not None

    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == "collectable":
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.collectable.onCollide(entity, otherEntity)
                    globals.world.entities.remove(otherEntity)
                    entity.score.score += 1


class BattleSystem(System):
    def check(self, entity):
        return entity.type == "player" and entity.battle is not None

    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == "dangerous":
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    # entity.battle.onCollide(entity, otherEntity)
                    entity.battle.lives -= 1
                    # reset player position
                    entity.position.rect.x = 300
                    entity.position.rect.y = -50
                    entity.speed = 0


class CameraSystem(System):
    def check(self, entity):
        return entity.camera is not None

    def updateEntity(self, screen, inputStream, entity):

        # Zoom
        if entity.intention is not None:
            if entity.intention.zoomIn:
                entity.camera.zoomLevel += 0.01
            if entity.intention.zoomOut:
                entity.camera.zoomLevel -= 0.01

        # set clipping rectangle
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.w, cameraRect.h)
        screen.set_clip(clipRect)

        # update cam if tracking entity
        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY

            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w / 2
            targetY = trackedEntity.position.rect.y + trackedEntity.position.rect.h / 2

            entity.camera.worldX = (currentX * 0.90) + (targetX * 0.1)
            entity.camera.worldY = (currentY * 0.90) + (targetY * 0.1)

        # calculate offsets
        offsetX = cameraRect.x + cameraRect.w / 2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h / 2 - (entity.camera.worldY * entity.camera.zoomLevel)

        # fill camera background
        screen.fill(globals.BLACK)

        # Draw platforms
        for p in globals.world.platforms:
            newPosRect = pygame.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y * entity.camera.zoomLevel) + offsetY,
                p.w * entity.camera.zoomLevel,
                p.h * entity.camera.zoomLevel)
            pygame.draw.rect(screen, globals.MUSTARD, newPosRect)

        # Draw entities
        for e in globals.world.entities:
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen,
                   (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                   (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                   e.direction == "left",
                   False,
                   entity.camera.zoomLevel)

        # player HUD
        # score
        if entity.score is not None:
            screen.blit(utils.coin0, (entity.camera.rect.w - 50, entity.camera.rect.y + 10))
            utils.drawtext(screen, str(entity.score.score), entity.camera.rect.w - 20, entity.camera.rect.y + 10,
                           globals.WHITE, 0)

        # # heart
        if entity.battle is not None:
            for h in range(entity.battle.lives):
                screen.blit(utils.lives_image, (entity.camera.rect.x + 10 + (h*30), entity.camera.rect.y + 10))

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
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))


class Score:
    def __init__(self):
        self.score = 0


class Battle:
    def __init__(self):
        self.lives = 3


class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.b1 = b1
        self.b2 = b2


class Intention:
    def __init__(self):
        self.moveLeft = False
        self.moveRight = False
        self.jump = False
        self.zoomIn = False
        self.zoomOut = False


class Entity:
    def __init__(self):
        self.state = "idle"
        self.type = "normal"
        self.position = None
        self.animations = Animations()
        self.direction = "right"
        self.camera = None
        self.score = None
        self.battle = None
        self.speed = 0
        self.input = None
        self.intention = None
        self.on_ground = False
        self.acceleration = 0.2
