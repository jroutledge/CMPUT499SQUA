import pygame
import sys
from PIL import ImageFont
from scipy.spatial import KDTree
import random
import math

# Global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 800
DISPLAY_Y = 600
BUBBLE_RADIUS =  int((DISPLAY_X * DISPLAY_Y) / 13000)
SHOOT_POSITION = (int(DISPLAY_X / 2), int(DISPLAY_Y * 0.8))
# Gloabal variables to represent various colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

LIGHT_BLUE = (0, 100, 255)
TEXT_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (255, 255, 255)
# Globals for the thesaurus TODO: make this a thesaurus library
WORDS = {
        'good':['nice','excellent','exceptional', 'wonderful', 'positive'], \
        'bad':['awful', 'evil','despicable','mean'], \
        'well':['strong', 'together']
        }
WORD_COLOURS = [RED, GREEN, BLUE] #there should be 10, this will be the list of colours for the different words for the current session

# this is a helper to quit the game #
def quitGame():
    pygame.quit()
    sys.exit()
    quit()

# this is a helper to get the current mouse location #
def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)
 
# this is a helper to check if a click is inbounds #
def checkInbound(pos, board):
    min_x = board.left
    max_x = board.left + board.width
    min_y = board.top
    max_y = board.top + board.height
    x = pos[0]
    y = pos[1]
    if not (min_x < x < max_x):
        return False
    if not (min_y < y < max_y):
        return False
    return True

def game_loop():
    global running, gameDisplay

    pygame.init()
    pygame.font.init() # for writing text to pygame
    gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    pygame.display.set_caption('Version 0.2')
    gameDisplay.fill(BACKGROUND_COLOUR)
    clock = pygame.time.Clock()
    running = True
    
    board = Board()
    board.createWordList()
    board.drawBoard()

    while running:
        board.drawBoard()
        board.drawAllBubbles()
        board.addToBoard() # this function is a shell right now
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = getPos()
                if (checkInbound(pos, board) == True):
                    board.shootBubble(pos)
                else:
                    #TODO: display an error
                    pass
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(60)

    quitGame()

### START BOARD CLASS AND HELPERS ###
# this calculates the size of the board array #
def calcBoard(board):
        row_num = 0
        board_len = 0
        bubbleAreaWidth = board.width
        num_bubbles = int(math.floor(bubbleAreaWidth/(BUBBLE_RADIUS * 2)))
        board_len = (num_bubbles * 3) - 1 # middle row has 1 less
        return board_len

class Board:
    def __init__(self):
        self.top = int(DISPLAY_Y * 0.1)
        self.left = int(DISPLAY_X * 0.25)
        self.width = int(DISPLAY_X / 2)
        self.height = int(DISPLAY_Y * 0.8)
        self.future_bubbles = []
        self.board_len = calcBoard(self)
        self.board_bubbles = [0] * self.board_len
        self.board_positions = [0] * self.board_len
        self.createWordList()
        self.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
                            self.future_bubbles[0][0], self.future_bubbles[0][1])

    # this will shoot a bubble from its current locaiton to the position specified
    def shootBubble(self, dest_pos):
        hit_array = []
        bubble = self.shoot_bubble
        # remove from future bubbles
        self.future_bubbles.pop(self.future_bubbles.index((bubble.word, bubble.colour)))
        #calculate the shots closest neighbor
        board_cpy = [x for x in self.board_positions if x is not 0]
        pos_cpy = [dest_pos[0], dest_pos[1]]
        kdtree = KDTree(board_cpy)
        dist, indices = kdtree.query(dest_pos)
        # add shot bubble to board
        self.board_bubbles.insert(indices, bubble)
        # load in new bubble
        self.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
                            self.future_bubbles[0][0], self.future_bubbles[0][1])
        self.shoot_bubble.draw()
        # TODO: THIS ISN'T WORKING
        return hit_array

    def drawBoard(self):
        pygame.draw.rect(gameDisplay, BLACK, \
            (self.left, self.top, self.width, self.height), 2)

    def drawAllBubbles(self):
        self.shoot_bubble.draw()
        for bubble in self.board_bubbles:
            bubble.draw()

    # this will populate the game board with words #
    def createWordList(self):
        # make a list of all the words with their associated colour
        word_colour_list = []
        for i in range(0, len(WORDS)):
            main_word = WORDS.keys()[i]
            colour = WORD_COLOURS[i]
            self.future_bubbles.append((main_word, colour))
            for word in WORDS[main_word]:
                word_colour_list.append((word, colour))
        #shuffle the list
        random.shuffle(word_colour_list)
        #loop through the list and create the bubbles
        bubbleList = self.createBubbles(word_colour_list)
        self.board_bubbles = bubbleList

    def createBubbles(self, word_colour_list):
        row_num = 0
        bubbleLeft = self.left + BUBBLE_RADIUS + 3 # the position of the leftmost bubble
        bubbleTop = self.top + BUBBLE_RADIUS + 3 # the position of the topmost bubble
        bubbleAreaWidth = self.width
        bubbleList = []
        for i in range(0, len(self.board_positions)):
            if i < len(word_colour_list):
                word_colour_pair = word_colour_list[i]
                currentBubble = Bubble(bubbleLeft, bubbleTop, \
                                word_colour_pair[0], word_colour_pair[1])
                bubbleList.append(currentBubble)
            # add radius to positions since circles draw from the middle
            bubbleLeft += (BUBBLE_RADIUS * 2)
            # if out of space for bubbles, start a new row
            if (bubbleLeft + (BUBBLE_RADIUS*2) >= (self.left + self.width)):
                row_num += 1
                bubbleLeft = self.left + BUBBLE_RADIUS + 3 # start at left column
                bubbleTop += (BUBBLE_RADIUS * 2) # go to the next row
                if ((row_num % 2) != 0):
                    bubbleLeft += BUBBLE_RADIUS # offset every other row
                    bubbleTop -= int(BUBBLE_RADIUS/3) # reduce the height so they go between the bubbles
                    #TODO: math the above line, is it a third?? a quarter?? somewhere in between??
            self.board_positions[i] = [bubbleLeft, bubbleTop]
        return bubbleList

    # funtion to add stuff around the main board space #
    # it will ultimately be used for things like score #
    # and varioius similar metrics #
    def addToBoard(self):
        meme_font = pygame.font.SysFont('Comic Sans MS', 30)
        # write some memes on the sides #
        left_meme = meme_font.render('It ya boi', False, BLACK)
        right_meme = meme_font.render('DJ the ', False, BLACK)
        right_meme_pt2 = meme_font.render('incredible', False, BLACK)
        right_meme_pt3 = meme_font.render('pancake', False, BLACK) 
        gameDisplay.blit(left_meme, (int(DISPLAY_X * 0.05), int(DISPLAY_Y * 0.1)))
        gameDisplay.blit(right_meme, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.1)))
        gameDisplay.blit(right_meme_pt2, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.2)))
        gameDisplay.blit(right_meme_pt3, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.3)))

### END BOARD CLASS AND HELPERS ###

### START BUBBLE CLASS AND HELPERS ###
# helper to find out how big a word will be, in pixels, given its font and size #
def getFontPixels(font, size, word):
    font = ImageFont.truetype(font, size)
    size = font.getsize(word)
    return size

# this writes the text to the middle of a bubble #
def writeToBubble(word, pos):
    fontSize = int(2*(BUBBLE_RADIUS)/(len(word)*0.5)) # scale the font size bases on bubble radius and word length
    font = 'Arial'
    pixelFontSize = getFontPixels(font, fontSize, word)
    horizontalMiddle = int(pixelFontSize[0]/3) # dividing by 2 wasn't working?? TODO: essplain
    vertMiddle = int(pixelFontSize[1]/3)
    wordFont = pygame.font.SysFont(font, fontSize)
    wordBubble = wordFont.render(word, False, BLACK)
    gameDisplay.blit(wordBubble, (int(pos[0]-horizontalMiddle), pos[1]-vertMiddle))

# this draws a circle as the position x, y #
def drawBubble(pos, colour):
    pygame.draw.circle(gameDisplay, colour, pos, BUBBLE_RADIUS, 0)

# TODO: put this in an appropriate other file
class Bubble:
    def __init__(self, pos_x, pos_y, word, colour):
        self.pos = (pos_x, pos_y)   # tuple that represents the bubbles position
        self.word = word            # word that will be in the buble
        self.colour = colour        # the colour that the bubble will be
        return

    #TODO: this function should move a bubble around the screen
    def move(self, targetPosition):
        self.erase()
        self.pos = targetPosition
        self.draw()
        return

    def draw(self):
        drawBubble(self.pos, self.colour)
        writeToBubble(self.word, self.pos)
        return

    def erase(self):
        drawBubble(self.pos, WHITE)
        return

# TODO: put this in an appropriate other file
#class Board:

if __name__ == '__main__':
    print(BUBBLE_RADIUS)
    game_loop()

