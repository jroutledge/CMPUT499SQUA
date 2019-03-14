import pygame
import sys
import time
import bubble
from board import Board
from bubble import Bubble
from globe import *
import argparse

#TODO: look into game slowdown, and also connect frontend to back

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


def game_loop():
    global running, gameDisplay, POPUP, POPUP_COUNTER

    pygame.init()
    pygame.font.init() # for writing text to pygame
    gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
    pygame.display.set_caption('Version 1.0')
    gameDisplay.fill(BACKGROUND_COLOUR)
    clock = pygame.time.Clock()
    running = True
    
    board = Board(gameDisplay)
    board.createWordList()
    board.drawBoard()

    while running:
        board.drawBoard()
        board.drawAllBubbles()
        board.addToBoard()
        for event in pygame.event.get():
            # this section handles the erasing of a popup after 5000 ticks
            if POPUP_COUNTER >= 0:
                POPUP_COUNTER += 1
            if POPUP_COUNTER >= 20:
                POPUP_COUNTER = 0
                i = 0 #TODO: find a way for it to find the popup -> board.current_popups.index(popped_bubble)
                #board.current_popups.pop(i).erase()
                board.success_popped = False

            if board.future_bubbles == []:
                board.game_over = True
                board.future_bubbles = [(" ", WHITE)] #TODO: fix this kludge
                print("Game over, better luck next time :(")

            if board.board_bubbles == []:
                # print a win message to the screen
                board.won = True
                print("You won! Good job! :)")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = getPos()
                if board.board.collidepoint(pos):
                    # valid selection for bubble, shoot it
                    board.shootBubble(pos)

                elif board.help_box.collidepoint(pos):
                    # make help box appear
                    board.displayHelpBox()

                else:
                    # TODO: display an error
                    pass

            if event.type == pygame.QUIT:
                running = False

<<<<<<< HEAD
        if(board.shooting != []):
            board.shoot_bubble.erase(gameDisplay)
            board.shoot_bubble.pos = board.shooting[0]
            board.shoot_bubble.draw(gameDisplay)
            pygame.time.wait(1)
            board.shooting.pop(0)
            if board.shooting == []:
                # load in new bubble
                board.popMatches()
                board.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
                            board.future_bubbles[0][0], board.future_bubbles[0][1])
            #TODO: make it so when shot, the match doesn't erase first, then again later

=======
>>>>>>> refs/remotes/origin/master
        pygame.display.update()
        clock.tick(60)

    quitGame()

def main():
    parser = argparse.ArgumentParser(description='Play the game')
    parser.add_argument('grade_level', help="the grade level of the words")
    parser.add_argument('mode', help="synonym or antonym mode")
    args = parser.parse_args()
    init(args.grade_level, args.mode)
    #time.sleep(2)
    game_loop()

if __name__ == '__main__':
    main()
