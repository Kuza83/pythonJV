import pygame
from pygame.locals import *


class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class MainMenuScene(Scene):
    def onEnter(self):
        print("entre dans le main menu")

    def onExit(self):
        print("sort du main menu")

    def input(self):
        print("main menu input")

    def update(self):
        print("main menu update")

    def draw(self):
        print("main menu draw")


class LevelSelectScene(Scene):
    def onEnter(self):
        print("entre dans la selection lvl")

    def onExit(self):
        print("sort de la selection lvl")

    def input(self):
        print("lvl select input")

    def update(self):
        print("lvl select update")

    def draw(self):
        print("lvl select draw")


class GameScene(Scene):
    def onEnter(self):
        print("entre dans la game scene")

    def onExit(self):
        print("sort de la game scene")

    def input(self):
        print("game scene input")

    def update(self):
        print("game scene update")

    def draw(self):
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
            self.scenes[-1].input()

    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update()

    def draw(self):
        if len(self.scenes) > 0:
            self.scenes[-1].draw()
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

    def set(self, scenes):
        # pop all scenes
        while len(self.scenes) > 0:
            self.pop()
        # add new scenes
        for s in scenes:
            self.push(s)
