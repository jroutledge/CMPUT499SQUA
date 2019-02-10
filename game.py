import pygame
import sys

# Global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 800
DISPLAY_Y = 600
# Gloabal variables to represent various colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)
BACKGROUND_COLOUR = (255, 255, 255)
# Globals for the thesaurus
words = {'good':['nice','excellent','incredible']}

# this is a helper to quit the game
def quit_game():
    pygame.quit()
    sys.exit()
    quit()

# this is a helper to get the current mouse location
def get_pos():
    pos = pygame.mouse.get_pos()
    print(pos)
    return (pos)

# this draws a circle as the position x, y
def drawBubble(pos, colour):
    pygame.draw.circle(gameDisplay, colour, pos, 20, 0)

# this is a helper function that will draw the game board in the middle of the screen #
def drawBoard():
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

# funtion to add stuff on to the main board space
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
    addToBoard()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = get_pos()
                drawBubble(pos, BLUE)
            if event.type == pygame.QUIT:
                running = False

            print(event)


        pygame.display.update()
        clock.tick(60)

    quit_game()

if __name__ == '__main__':
    game_loop()

