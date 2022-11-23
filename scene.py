import pygame
from pygame.locals import *


class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self, sm):
        pass

    def update(self, sm):
        pass

    def draw(self, sm):
        pass


class MainMenuScene(Scene):
    def onEnter(self):
        print("entre dans le main menu")

    def onExit(self):
        print("sort du main menu")

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(LevelSelectScene())
        if keys[pygame.K_q]:
            sm.pop()

    def update(self, sm):
        print("main menu update")

    def draw(self, sm):
        print("main menu draw")


class LevelSelectScene(Scene):
    def onEnter(self):
        print("entre dans la selection lvl")

    def onExit(self):
        print("sort de la selection lvl")

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            sm.push(GameScene())
        if keys[pygame.K_2]:
            sm.push(GameScene())
        if keys[pygame.K_LSHIFT]:
            sm.pop()

    def update(self, sm):
        print("lvl select update")

    def draw(self, sm):
        print("lvl select draw")


class GameScene(Scene):
    def onEnter(self):
        print("entre dans la game scene")

    def onExit(self):
        print("sort de la game scene")

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sm.pop()

    def update(self, sm):
        print("game scene update")

    def draw(self, sm):
        print("game scene draw")


class SceneManager:
    def __init__(self):
        self.scenes = []

    def isEmpty(self):
        return len(self.scenes) == 0

    def enterScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()

    def exitScene(self):
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()

    def input(self):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self)

    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)

    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self)
        # present screen
        pygame.display.flip()

    def push(self, scene):
        self.exitScene()
        self.scenes.append(scene)
        self.enterScene()

    def pop(self):
        self.exitScene()
        self.scenes.pop()
        self.enterScene()

    def set(self, scene):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scenes
        for s in scene:
            self.push(s)
