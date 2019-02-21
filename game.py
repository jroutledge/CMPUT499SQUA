import pygame
import sys
from PIL import ImageFont
from scipy.spatial import KDTree
import random
import math
import time

# Global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 800
DISPLAY_Y = 600
BUBBLE_RADIUS =  int((DISPLAY_X * DISPLAY_Y) / 13000)
SHOOT_POSITION = (int(DISPLAY_X / 2), int(DISPLAY_Y * 0.8))
# Global variables for controlling the duration of popups
POPUP_COUNTER = 0
POPUP = None
POPUP_FONT = None # TODO: find a way to make this global
# Gloabal variables to represent various colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255 ,0)
PURPLE = (255, 0, 255)
TURQUOISE = (0, 255, 255)
WHITE = (255, 255, 255)
LIGHT_BLUE = (0, 100, 255)
TEXT_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (255, 255, 255)
# Globals for the thesaurus TODO: make this a thesaurus library and dynamically generate
WORDS = {
        'good':['nice','excellent','exceptional', 'wonderful', 'positive'], \
        'bad':['awful', 'evil','despicable', 'mean'], \
        'easy':['accessible', 'clear', 'effortless', 'obvious'], \
        'hard':['arduous', 'heavy', 'rough', 'tough'], \
        'cold':['chilled', 'cool', 'icy', 'snowy'], \
        'warm':['hot', 'balmy', 'heated', 'sunny']
        }
WORD_COLOURS = [RED, GREEN, BLUE, YELLOW, PURPLE, TURQUOISE] #TODO: add colours as needed


def quitGame():
    """ this is a helper to quit the game """
    pygame.quit()
    sys.exit()
    quit()


def getPos():
    """ this is a helper to get the current mouse location """
    pos = pygame.mouse.get_pos()
    return (pos)
 

def checkInbound(pos, board):
    """ this is a helper to check if a click is inbounds """
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

def createPopup(words, colour, pos_x, pos_y):
    POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
    message = POPUP_FONT.render(words, False, colour)
    gameDisplay.blit(message, (pos_x, pos_y))


def erase_popup(message, pos_x, pos_y):
    POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
    message = POPUP_FONT.render(message, False, WHITE)
    gameDisplay.blit(message, (pos_x, pos_y))


def game_loop():
    global running, gameDisplay, POPUP, POPUP_COUNTER

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

    num_loops = 0
    while running:
        num_loops += 1
        board.drawBoard()
        board.drawAllBubbles()
        board.addToBoard()
        for event in pygame.event.get():
            # this section handles the erasing of a popup after 5000 ticks
            if POPUP_COUNTER >= 1:
                POPUP_COUNTER += 1
            if POPUP_COUNTER >= 50:
                POPUP_COUNTER = 0
                erase_popup(POPUP[0], POPUP[1], POPUP[2])
                board.success_popped = False

            if board.future_bubbles == []:
                board.game_over = True
                print("You lost!")

            if board.board_bubbles == []:
                # print a win message to the screen
                board.won = True
                print("You won!")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = getPos()
                # if (checkInbound(pos, board) == True):
                if board.board.collidepoint(pos):
                    #print(board.future_bubbles)
                    board.shootBubble(pos)
                else:
                    #TODO: display an error
                    pass

            if event.type == pygame.QUIT:
                running = False

        if(board.shooting != []):
            if(num_loops%50 == 0):
                board.shoot_bubble.erase()
            board.shoot_bubble.pos = board.shooting[0]
            board.shooting.pop(0)

        pygame.display.update()
        clock.tick(60)

    quitGame()

### START BOARD CLASS AND HELPERS ###
def calcBoard(board):
    """ this calculates the size of the board array """
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
        self.board_bubbles = [0] * self.board_len       # list of bubbles on the board
        self.board_positions = [0] * self.board_len     # list if coords for centers of bubble
        self.createWordList()
        self.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
                            self.future_bubbles[0][0], self.future_bubbles[0][1])   # bubble to shoot
        self.board = None       # rect object of the board
        self.success_popped = False
        self.won = False
        self.game_over = False
        self.shooting = []


    def shootBubble(self, dest_pos):
        """ this will shoot a bubble from its current location to the position specified """
        hit_array = []
        bubble = self.shoot_bubble

        self.shooting = self.shoot_bubble.move(dest_pos)

        # remove from future bubbles
        self.future_bubbles.pop(self.future_bubbles.index((bubble.word, bubble.colour)))

        #calculate the shots closest neighbor
        board_cpy = [x for x in self.board_positions if x is not 0]
        pos_cpy = [dest_pos[0], dest_pos[1]]
        kdtree = KDTree(board_cpy)
        dist, indices = kdtree.query(dest_pos)

        # add shot bubble to board
        self.board_bubbles.insert(indices, bubble)
        self.shoot_bubble.pos = self.board_positions[indices]

        # detect matches and pop as needed
        self.findMatches()

        # load in new bubble
        self.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
                            self.future_bubbles[0][0], self.future_bubbles[0][1])
        # self.shoot_bubble.draw(BLACK)
        # TODO: THIS ISN'T WORKING

        return hit_array


    def findMatches(self):
        """
        finds matches that the bubble has made
        'pops' the matches and then displays a good job message
        """
        bubble = self.shoot_bubble
        matches = [bubble]

        # find matching bubbles that are touching our bubbles
        for b in matches:
            for onBoard in self.board_bubbles:
                if (self.board_bubbles == 0):
                    pass
                if collide(b.pos, onBoard.pos) and bubble.colour == onBoard.colour:
                    # it's matching and touching
                    if onBoard not in matches:
                        matches.append(onBoard)

        #print(matches)
        if matches != [bubble]:
            # erase the matches
            for b in matches:
                b.erase()
                index = self.board_bubbles.index(b)
                self.board_bubbles.pop(index)
                b.colour = WHITE
            bubble.erase()

            # send good job message
            print("You popped bubbles!")
            self.success_popped = True
        return


    def drawBoard(self):
        self.board = pygame.draw.rect(gameDisplay, BLACK, \
                                      (self.left, self.top, self.width, self.height), 2)


    def drawAllBubbles(self):
        self.shoot_bubble.draw()
        for bubble in self.board_bubbles:
            if (bubble != 0):
                bubble.draw()


    def createWordList(self):
        """ this will populate the game board with words """
        # make a list of all the words with their associated colour
        word_colour_list = []
        for i in range(0, len(WORDS)):
            main_word = WORDS.keys()[i]
            colour = WORD_COLOURS[i]
            self.future_bubbles.append((main_word, colour))
            for word in WORDS[main_word]:
                word_colour_list.append((word, colour))
        # shuffle the list
        random.shuffle(word_colour_list)
        # loop through the list and create the bubbles
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
                    bubbleTop -= int(BUBBLE_RADIUS/3.5) # reduce the height so they go between the bubbles
                    #TODO: math the above line, is it a third?? a quarter?? somewhere in between??
            self.board_positions[i] = [bubbleLeft, bubbleTop]
        return bubbleList


    def addToBoard(self):
        global POPUP_COUNTER, POPUP
        """
        funtion to add stuff around the main board space
        it will ultimately be used for things like score
        and varioius similar metrics
        """
        meme_font = pygame.font.SysFont('Comic Sans MS', 25)
        # write some memes on the sides #
        # left_meme = meme_font.render('It ya boi', False, BLACK)
        right_meme = meme_font.render('To play click', False, BLACK)
        right_meme_pt2 = meme_font.render('where you want', False, BLACK)
        right_meme_pt3 = meme_font.render('the bubble to go', False, BLACK)
        # gameDisplay.blit(left_meme, (int(DISPLAY_X * 0.05), int(DISPLAY_Y * 0.1)))
        gameDisplay.blit(right_meme, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.1)))
        gameDisplay.blit(right_meme_pt2, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.2)))
        gameDisplay.blit(right_meme_pt3, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.3)))
        if self.won:
            # create the success popup
            createPopup('You Won! Good Job!', BLUE, int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5))
            # store the popup for deletion later
            POPUP = ['Words Matched! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5)]
            # create second success popu TODO: this is a meme, remove it
            createPopup('Winner, winner, chicken dinner', BLUE, int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.4))
        elif self.success_popped:
            # create the success popup
            createPopup('Words Matched! Good Job!', BLUE, int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5))
            # start the counter
            POPUP_COUNTER += 1
            # store the popup for deletion later
            POPUP = ['Words Matched! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5)]
        elif self.game_over:
            # create the game over popup
            createPopup('Game over man, game over!', RED, int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.4))
            # start the counter
            POPUP_COUNTER += 1
            # store the popup for deletion later
            POPUP = ['Game over man, game over!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5)]

### END BOARD CLASS AND HELPERS ###

### START BUBBLE CLASS AND HELPERS ###
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


def writeToBubble(word, pos, color):
    """ this writes the text to the middle of a bubble """
    fontSize = int(2*(BUBBLE_RADIUS)/(len(word)*0.5)) # scale the font size bases on bubble radius and word length
    font = 'Arial'
    pixelFontSize = getFontPixels(font, fontSize, word)
    horizontalMiddle = int(pixelFontSize[0]/3) # dividing by 2 wasn't working?? TODO: essplain
    vertMiddle = int(pixelFontSize[1]/3)
    wordFont = pygame.font.SysFont(font, fontSize)
    wordBubble = wordFont.render(word, False, color)
    gameDisplay.blit(wordBubble, (int(pos[0]-horizontalMiddle), pos[1]-vertMiddle))


def drawBubble(pos, colour):
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
    def move(self, target_position):
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

        self.erase()
        self.pos = target_position
        return intermediate_positions

    def draw(self):
        drawBubble(self.pos, self.colour)
        writeToBubble(self.word, self.pos, BLACK)
        return

    def erase(self):
        drawBubble(self.pos, WHITE)
        writeToBubble(self.word, self.pos, WHITE)
        return


if __name__ == '__main__':
    print(BUBBLE_RADIUS)
    game_loop()

