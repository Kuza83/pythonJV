import pygame
import utils
import globals
import engine


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

    def draw(self, sm, screen):
        pass


class MainMenuScene(Scene):
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            sm.push(FadeTransitionScene(self, LevelSelectScene()))
        if keys[pygame.K_q]:
            sm.pop()

    def draw(self, sm, screen):
        # background
        screen.fill(globals.DARK_GREY)
        utils.drawtext(screen, "Main Menu. [Return=Levels, Q=Quit]", 10, 50)


class LevelSelectScene(Scene):
    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            # set level to 1
            globals.world = globals.levels[1]
            sm.push(FadeTransitionScene(self, GameScene()))
        if keys[pygame.K_2]:
            # set level to 2
            globals.world = globals.levels[2]
            sm.push(FadeTransitionScene(self, GameScene()))
        if keys[pygame.K_LSHIFT]:
            sm.pop()
            sm.push(FadeTransitionScene(self, None))

    def draw(self, sm, screen):
        # background
        screen.fill(globals.DARK_GREY)
        utils.drawtext(screen, "Level Select. [1/2=Level, ShiftL=Return Main Menu]", 10, 50)


class GameScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()

    def input(self, sm):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            sm.pop()
            sm.push(FadeTransitionScene(self, None))
        if globals.world.isWon():
            sm.push(WinScene())
            sm.push(FadeTransitionScene(self, None))
        if globals.world.isLost():
            sm.push(LoseScene())
            sm.push(FadeTransitionScene(self, None))

    def draw(self, sm, screen):
        # background
        screen.fill(globals.DARK_GREY)
        self.cameraSystem.update(screen)


class WinScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()

    def input(self, sm):
        pass

    def draw(self, sm, screen):
        utils.drawtext(screen, "YOU WIN !!!!!", 10, 50)


class LoseScene(Scene):
    def __init__(self):
        self.cameraSystem = engine.CameraSystem()

    def input(self, sm):
        pass

    def draw(self, sm, screen):
        utils.drawtext(screen, "YOU LOSE !!!!!", 10, 50)


class TransitionScene(Scene):
    def __init__(self, fromScene, toScene):
        super().__init__()
        self.currentPercentage = 0
        self.fromScene = fromScene
        self.toScene = toScene

    def update(self, sm):
        self.currentPercentage += 2
        if self.currentPercentage >= 100:
            sm.pop()
            if self.toScene is not None:
                sm.push(self.toScene)


class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            self.fromScene.draw(sm, screen)
        else:
            if self.toScene is None:
                sm.scenes[-2].draw(sm, screen)
            else:
                self.toScene.draw(sm, screen)
        # fade overlay
        overlay = pygame.Surface(globals.SCREEN_SIZE)
        alpha = int(abs((255-((255/50) * self.currentPercentage))))
        overlay.set_alpha(255 - alpha)
        overlay.fill(globals.BLACK)
        screen.blit(overlay, (0, 0))


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

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
        utils.drawtext(screen, str(len(self.scenes)), 0, 0)
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
