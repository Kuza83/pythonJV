import pygame
import utils
import globals
import engine
import ui


class Scene:
    def __init__(self):
        pass

    def onEnter(self):
        pass

    def onExit(self):
        pass

    def input(self, sm, inputStream):
        pass

    def update(self, sm, inputStream):
        pass

    def draw(self, sm, screen):
        pass


class MainMenuScene(Scene):
    def __init__(self):
        self.enter = ui.ButtonUI(pygame.K_RETURN, "[Enter = next]", 50, 200)
        self.esc = ui.ButtonUI(pygame.K_RETURN, "[Q or Esc = quit]", 50, 230)
        self.c = ui.ButtonUI(pygame.K_c, "[C = test]", 50, 260)

    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_q):
            sm.pop()

    def update(self, sm, inputStream):
        self.c.update(inputStream)

    def draw(self, sm, screen):
        screen.fill(globals.BLACK)
        utils.drawtext(screen, "Main Menu", 10, 50, globals.WHITE, 255)
        self.enter.draw(screen)
        self.esc.draw(screen)
        self.c.draw(screen)


class LevelSelectScene(Scene):
    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_1):
            # set level to 1
            globals.world = globals.levels[1]
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_2):
            # set level to 2
            globals.world = globals.levels[2]
            sm.push(FadeTransitionScene([self], [GameScene()]))
        if inputStream.keyboard.isKeyPressed(pygame.K_LSHIFT):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))

    def draw(self, sm, screen):
        # background
        screen.fill(globals.BLACK)
        utils.drawtext(screen, "Level Select", 10, 50, globals.WHITE, 255)


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.cameraSystem = engine.CameraSystem()

    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_q):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        if globals.world.isWon():
            sm.set([WinScene()])
        if globals.world.isLost():
            sm.set([LoseScene()])

    def draw(self, sm, screen):
        # background
        screen.fill(globals.BLACK)
        self.cameraSystem.update(screen)


class WinScene(Scene):
    def __init__(self):
        super().__init__()
        self.alpha = 0

    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)

    def input(self, sm, inputStream):
        if inputStream.keyboard.isKeyPressed(pygame.K_x):
            sm.set([FadeTransitionScene([self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        bgSurf = pygame.Surface((700, 500))
        bgSurf.fill(globals.BLACK)
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawtext(screen, "YOU WIN !!!!!", 150, 150, globals.WHITE, self.alpha)


class LoseScene(Scene):
    def __init__(self):
        self.alpha = 0

    def update(self, sm, inputStream):
        self.alpha = min(255, self.alpha + 10)

    def input(self, sm, inputStream):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            sm.set([FadeTransitionScene([self], [MainMenuScene(), LevelSelectScene()])])

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        bgSurf = pygame.Surface((700, 500))
        bgSurf.fill(globals.BLACK)
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawtext(screen, "YOU LOSE !!!!!", 150, 150, globals.WHITE, self.alpha)


class TransitionScene(Scene):
    def __init__(self, fromScenes, toScenes):
        super().__init__()
        self.currentPercentage = 0
        self.fromScenes = fromScenes
        self.toScenes = toScenes

    def update(self, sm, inputStream):
        self.currentPercentage += 2
        if self.currentPercentage >= 100:
            sm.pop()
            for s in self.toScenes:
                sm.push(s)


class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm, screen)
            else:
                for s in self.toScenes:
                    s.draw(sm, screen)
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

    def input(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].input(self, inputStream)

    def update(self, inputStream):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, inputStream)

    def draw(self, screen):
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
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
