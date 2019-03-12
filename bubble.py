import pygame
import math
from PIL import ImageFont
from globe import *

def collide(pos1, pos2):
    """ checks if 2 points are within 2.5*radius of eachother """
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    dist = math.hypot(x, y)
    if dist <= 2.5*BUBBLE_RADIUS:
        # collision
        return True
    else:
        # no collision
        return False

def getFontPixels(font, size, word):
    """ helper to find out how big a word will be, in pixels, given its font and size """
    font = ImageFont.truetype(font, size)
    size = font.getsize(word)
    return size


def writeToBubble(word, pos, color, gameDisplay):
    """ this writes the text to the middle of a bubble """
    fontSize = int(2*(BUBBLE_RADIUS)/(len(word)*0.5)) # scale the font size bases on bubble radius and word length
    #TODO: make this catch divide by zero errors
    font = 'Arial'
    pixelFontSize = getFontPixels(font, fontSize, word)
    horizontalMiddle = int(pixelFontSize[0]/3) # dividing by 2 wasn't working?? TODO: essplain
    vertMiddle = int(pixelFontSize[1]/3)
    wordFont = pygame.font.SysFont(font, fontSize)
    wordBubble = wordFont.render(word, False, color)
    gameDisplay.blit(wordBubble, (int(pos[0]-horizontalMiddle), pos[1]-vertMiddle))


def drawBubble(pos, colour, gameDisplay):
    """ this draws a circle as the position x, y """
    return pygame.draw.circle(gameDisplay, colour, pos, BUBBLE_RADIUS, 0)

# TODO: put this in an appropriate other file
class Bubble:
    def __init__(self, pos_x, pos_y, word, colour):
        self.pos = (pos_x, pos_y)   # tuple that represents the bubbles position
        self.word = word            # word that will be in the buble
        self.colour = colour        # the colour that the bubble will be
        return

    # TODO: this function should move a bubble around the screen
    def move(self, target_position, gameDisplay):
        """this part is going to animate the bubble moving"""
        x1 = self.pos[0]
        y1 = self.pos[1]
        x2 = target_position[0]
        y2 = target_position[1]
        difX = x2 - x1
        difY = y2 - y1
        print(difX, difY)
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        num_positions = int(dist / 10)
        intermediate_positions = [(0,0)] * num_positions
        for i in range(0, len(intermediate_positions)):
            xPos = x1+(difX*(i+1)/num_positions)
            yPos = y1+(difY*(i+1)/num_positions)
            intermediate_positions[i] = (xPos, yPos)
        # for i in intermediate_positions:
        #     self.erase()
        #     print(self.pos, i)
        #     pygame.time.wait(10)
        #     self.pos = i
        #     self.draw()
        #     pygame.time.wait(10)

        self.erase(gameDisplay)
        self.pos = target_position
        return intermediate_positions

    def draw(self, gameDisplay):
        drawBubble(self.pos, self.colour, gameDisplay)
        writeToBubble(self.word, self.pos, BLACK, gameDisplay)
        return

    def erase(self, gameDisplay):
        drawBubble(self.pos, WHITE, gameDisplay)
        writeToBubble(self.word, self.pos, WHITE, gameDisplay)
        return