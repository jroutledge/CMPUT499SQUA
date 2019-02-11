import pygame
import sys
from PIL import ImageFont

# Global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 800
DISPLAY_Y = 600
BUBBLE_RADIUS =  int((DISPLAY_X * DISPLAY_Y) / 13000)
print(BUBBLE_RADIUS)
# Gloabal variables to represent various colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

LIGHT_BLUE = (0, 100, 255)
TEXT_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (255, 255, 255)
# Globals for the thesaurus
WORDS = {'good':['nice','excellent','incredible'], 'bad':['evil','despicable','mean']}
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

# this draws a circle as the position x, y #
def drawBubble(pos, colour):
    pygame.draw.circle(gameDisplay, colour, pos, BUBBLE_RADIUS, 0)

# helper to find out how big a word will be, in pixels, given its font and size #
def getFontPixels(font, size, word):
    font = ImageFont.truetype(font, size)
    size = font.getsize(word)
    print(size)
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

# this draws a coloured circled with the specified word in it at the position x, y #
def drawWordBubble(pos, word, colour):
    drawBubble(pos, colour)
    writeToBubble(word, pos)

# this will populate the game board with words #
def createBubbles():
    global width, left, top # the width and top left corner of the game screen
    row_num = 0
    bubbleLeft = left + 3 # the position of the leftmost bubble
    bubbleTop = top + 3 # the position of the topmost bubble
    bubbleAreaWidth = width
    for i in range(0, len(WORDS)): #this will eventually get 10 words, swallow exceptions for prototyping
        try:
            main_word = WORDS.keys()[i]
            for word in WORDS[main_word]:
                print(word)
                colour = WORD_COLOURS[i]
                drawWordBubble((bubbleLeft+BUBBLE_RADIUS,bubbleTop+BUBBLE_RADIUS), word, colour)
                # add radius to positions since circles draw from the middle
                bubbleLeft += (BUBBLE_RADIUS * 2)
                # if out of space for bubbles, start a new row
                if (bubbleLeft + (BUBBLE_RADIUS*2) >= (left + width)):
                    row_num += 1
                    bubbleLeft = left + 3 # start at left column
                    bubbleTop += (BUBBLE_RADIUS * 2) # go to the next row
                    if ((row_num % 2) != 0):
                        bubbleLeft += BUBBLE_RADIUS # offset every other row
                        bubbleTop -= int(BUBBLE_RADIUS/3) # reduce the height so they go between the bubbles
                        #TODO: math the above line, is it a third?? a quarter?? somewhere in between??
        except Exception as e:
            print('Unable to initialize bubbles: ' + str(e.message)) # oh ya we error handling now

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
    pygame.draw.circle(gameDisplay, BLACK,  \
        (int(DISPLAY_X / 2), int(DISPLAY_Y * 0.8)), 24, 2)

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
    pygame.display.set_caption('Version 0.1')
    gameDisplay.fill(BACKGROUND_COLOUR)
    clock = pygame.time.Clock()
    running = True
    
    drawBoard()
    createBubbles()
    addToBoard() # this function is a shell right now

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_pos()
                drawWordBubble(pos, 'good', LIGHT_BLUE)
            if event.type == pygame.QUIT:
                running = False

            #print(event)


        pygame.display.update()
        clock.tick(60)

    quit_game()

if __name__ == '__main__':
    game_loop()

