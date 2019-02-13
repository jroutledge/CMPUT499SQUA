import pygame
import sys
from PIL import ImageFont
import random

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
def quit_game():
    pygame.quit()
    sys.exit()
    quit()

# this is a helper to get the current mouse location #
def get_pos():
    pos = pygame.mouse.get_pos()
    return (pos)

# this will populate the game board with words #
def createBubbles():
    global width, left, top # the width and top left corner of the game screen
    row_num = 0
    bubbleLeft = left + BUBBLE_RADIUS + 3 # the position of the leftmost bubble
    bubbleTop = top + BUBBLE_RADIUS + 3 # the position of the topmost bubble
    bubbleAreaWidth = width
    bubbleList = []

    # make a list of all the words with their associated colour
    wordColourList = []
    for i in range(0, len(WORDS)):
        main_word = WORDS.keys()[i]
        for word in WORDS[main_word]:
            colour = WORD_COLOURS[i]
            wordColourList.append((word, colour))
    #shuffle the list
    random.shuffle(wordColourList)
    #loop through the list and create the bubbles
    for wordColourPair in wordColourList:
        currentBubble = Bubble(bubbleLeft, bubbleTop, \
                        wordColourPair[0], wordColourPair[1])
        bubbleList.append(currentBubble)
        #drawWordBubble((bubbleLeft+BUBBLE_RADIUS,bubbleTop+BUBBLE_RADIUS), word, colour)
        # add radius to positions since circles draw from the middle
        bubbleLeft += (BUBBLE_RADIUS * 2)
        # if out of space for bubbles, start a new row
        if (bubbleLeft + (BUBBLE_RADIUS*2) >= (left + width)):
            row_num += 1
            bubbleLeft = left + BUBBLE_RADIUS + 3 # start at left column
            bubbleTop += (BUBBLE_RADIUS * 2) # go to the next row
            if ((row_num % 2) != 0):
                bubbleLeft += BUBBLE_RADIUS # offset every other row
                bubbleTop -= int(BUBBLE_RADIUS/3) # reduce the height so they go between the bubbles
                #TODO: math the above line, is it a third?? a quarter?? somewhere in between??
    return bubbleList

# this will shoot a bubble from its current locaiton to the position specified
def shoot(bubble, dest_pos):
    bubble.move(dest_pos)
    # load in new bubble

def drawAllBubbles(bubble_list):
    for bubble in bubble_list:
        bubble.draw()

# this is a helper function that will draw the game board in the middle of the screen #
def drawBoard():
    global width, left, top
    # initial rectagle that bounds the game region #
    top = int(DISPLAY_Y * 0.1)
    left = int(DISPLAY_X * 0.25)
    height = int(DISPLAY_Y * 0.8)
    width = int(DISPLAY_X / 2)
    pygame.draw.rect(gameDisplay, BLACK, \
        (left, top, width, height), 2)
    # starting position for the shooter #
    x = int(DISPLAY_X / 2)
    y = int(DISPLAY_Y * 4 / 5)

# funtion to add stuff around the main board space #
# it will ultimately be used for things like score #
# and varioius similar metrics #
def addToBoard():
    meme_font = pygame.font.SysFont('Comic Sans MS', 30)
    # write some memes on the sides #
    left_meme = meme_font.render('It ya boy', False, BLACK)
    right_meme = meme_font.render('DJ the ', False, BLACK)
    right_meme_pt2 = meme_font.render('incredible', False, BLACK)
    right_meme_pt3 = meme_font.render('pancake', False, BLACK) 
    gameDisplay.blit(left_meme, (int(DISPLAY_X * 0.05), int(DISPLAY_Y * 0.1)))
    gameDisplay.blit(right_meme, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.1)))
    gameDisplay.blit(right_meme_pt2, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.2)))
    gameDisplay.blit(right_meme_pt3, (int(DISPLAY_X * 0.80), int(DISPLAY_Y * 0.3)))
    
def game_loop():
    global running, gameDisplay

    pygame.init()
    pygame.font.init() # for writing text to pygame
    gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    pygame.display.set_caption('Version 0.2')
    gameDisplay.fill(BACKGROUND_COLOUR)
    clock = pygame.time.Clock()
    running = True
    
    # create a queue of bubble to be shot
    bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], 'good', LIGHT_BLUE)
    bubble.draw()
    board = Board()
    board.drawBoard()
    board.createBubbles()

    while running:
        board.drawBoard()
        board.drawAllBubbles()
        addToBoard() # this function is a shell right now
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_pos()
                shoot(bubble, pos)
            if event.type == pygame.QUIT:
                running = False

            #print(event)
        pygame.display.update()
        clock.tick(60)

    quit_game()

### START BOARD CLASS AND HELPERS ###
class Board:
    def __init__(self):
        self.top = int(DISPLAY_Y * 0.1)
        self.left = int(DISPLAY_X * 0.25)
        self.width = int(DISPLAY_X / 2)
        self.height = int(DISPLAY_Y * 0.8)
        self.board_bubbles = []
        self.future_bubbles = []

    def drawBoard(self):
        #global width, left, top
        pygame.draw.rect(gameDisplay, BLACK, \
            (self.left, self.top, self.width, self.height), 2)
        # starting position for the shooter #
        #x = int(DISPLAY_X / 2)
        #y = int(DISPLAY_Y * 4 / 5)

    def drawAllBubbles(self):
        for bubble in self.board_bubbles:
            bubble.draw()

    # this will populate the game board with words #
    def createBubbles(self):
        #global width, left, top # the width and top left corner of the game screen
        row_num = 0
        bubbleLeft = self.left + BUBBLE_RADIUS + 3 # the position of the leftmost bubble
        bubbleTop = self.top + BUBBLE_RADIUS + 3 # the position of the topmost bubble
        bubbleAreaWidth = self.width
        bubbleList = []
        # make a list of all the words with their associated colour
        wordColourList = []
        for i in range(0, len(WORDS)):
            main_word = WORDS.keys()[i]
            for word in WORDS[main_word]:
                colour = WORD_COLOURS[i]
                wordColourList.append((word, colour))
        #shuffle the list
        random.shuffle(wordColourList)
        #loop through the list and create the bubbles
        for wordColourPair in wordColourList:
            currentBubble = Bubble(bubbleLeft, bubbleTop, \
                            wordColourPair[0], wordColourPair[1])
            bubbleList.append(currentBubble)
            #drawWordBubble((bubbleLeft+BUBBLE_RADIUS,bubbleTop+BUBBLE_RADIUS), word, colour)
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
        self.board_bubbles = bubbleList

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

