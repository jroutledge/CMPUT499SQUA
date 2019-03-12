import pygame
from globe import *

class Popup():
    def __init__(self, text, pos_x, pos_y, gameDisplay, colour=BLACK):
        self.text = text
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.gameDisplay = gameDisplay
        self.colour = colour
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def create(self):
        #POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
        message = self.font.render(self.text, False, self.colour)
        self.gameDisplay.blit(message, (self.pos_x, self.pos_y))


    def erase(self):
        #POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
        message = self.font.render(self.text, False, WHITE)
        self.gameDisplay.blit(message, (self.pos_x, self.pos_y))