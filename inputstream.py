import pygame


class Keyboard:
    def __init__(self):
        self.currentKeyStates = None
        self.previousKeyStates = None

    def processInput(self):
        self.previousKeyStates = self.currentKeyStates
        self.currentKeyStates = pygame.key.get_pressed()

    def isKeyDown(self, keyCode):
        return self.currentKeyStates[keyCode] == True

    def isKeyPressed(self, keyCode):
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False

    def isKeyRealesed(self, keyCode):
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True


class InputStream:
    def __init__(self):
        self.keyboard = Keyboard()
        # self.mouse
        # self.controllers

    def processInput(self):
        self.keyboard.processInput()
