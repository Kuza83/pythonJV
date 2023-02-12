import globals
import utils
import pygame


class Level:
    def __init__(self, platforms=None, entities=None, winFunc=None, loseFunc=None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc

    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)

    def isLost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)


def lostLevel(levels):
    for entity in levels.entities:
        if entity.type == "player":
            if entity.battle is not None:
                if entity.battle.lives > 0:
                    return False
    return True


def wonLevel(levels):
    for entity in levels.entities:
        if entity.type == "player":
            if entity.score.score is not None:
                if entity.score.score == 3:
                    return True
    return False


def loadLevel(levelNumber):
    if levelNumber == 1:
        globals.world = Level(
            platforms=[
                # middle
                pygame.Rect(100, 300, 400, 50),
                # left
                pygame.Rect(100, 250, 50, 50),
                # right
                pygame.Rect(450, 250, 50, 50)
            ],
            entities=[
                utils.makeCoin(350, 270),
                utils.makeCoin(250, 270),
                utils.makeEnemy(100, 220),
                globals.player1
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel
        )
    if levelNumber == 2:
        globals.world = Level(
            platforms=[
                # middle
                pygame.Rect(100, 300, 400, 50),
            ],
            entities=[
                utils.makeCoin(350, 270),
                globals.player1
            ],
            winFunc=wonLevel,
            loseFunc=lostLevel
        )