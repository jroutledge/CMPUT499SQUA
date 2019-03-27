from bubble import *
from popup import Popup

import math
import random
import pygame
from scipy.spatial import KDTree
from globe import *


def calcBoard(board):
    """ this calculates the size of the board array """
    row_num = 0
    board_len = 0
    bubbleAreaWidth = board.width
    num_bubbles = int(math.floor(bubbleAreaWidth/(BUBBLE_RADIUS * 2)))
    board_len = (num_bubbles * 3) - 1 # middle row has 1 less
    return board_len


# def createPopup(words, colour, pos_x, pos_y, gameDisplay):
#     POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
#     message = POPUP_FONT.render(words, False, colour)
#     gameDisplay.blit(message, (pos_x, pos_y))


# def erase_popup(message, pos_x, pos_y, gameDisplay):
#     POPUP_FONT = pygame.font.SysFont('Comic Sans MS', 30)
#     message = POPUP_FONT.render(message, False, WHITE)
#     gameDisplay.blit(message, (pos_x, pos_y))


class Board:
    def __init__(self,  gameDisplay):
        self.top = int(DISPLAY_Y * 0.1)
        self.left = int(DISPLAY_X * 0.12)
        self.width = int(DISPLAY_X * 0.76)
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
        self.shooting = False
        self.shoot_pos = []
        self.current_matches = []
        self.current_popups = []
        self.help_box = None    # rect object on the board
        self.gameDisplay = gameDisplay

    def shootBubble(self, dest_pos):
        """ this will shoot a bubble from its current location to the position specified """
        hit_array = []
        bubble = self.shoot_bubble

        self.shoot_pos = self.shoot_bubble.move(dest_pos, self.gameDisplay)

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

        # # move the bubble
        # while self.shooting != []:
        #     bubble.erase(self.gameDisplay)
        #     #pygame.display.update()
        #     bubble.pos = self.shooting[0]
        #     bubble.drawAsGrey(self.gameDisplay)
        #     self.shooting.pop(0)

            # TODO: make it so when shot, the match doesn't erase first, then again later

        # if self.shooting == [] and self.future_bubbles != []:
        #     # load in new bubble
        #     self.popMatches()
        #     self.shoot_bubble = Bubble(SHOOT_POSITION[0], SHOOT_POSITION[1], \
        #                                self.future_bubbles[0][0], self.future_bubbles[0][1])

        return hit_array

    def findMatches(self): # TODO: this function is bloated and is leading to problems in animating the shooting
        """
        finds matches that the bubble has made
        """
        bubble = self.shoot_bubble
        matches = [bubble]

        # find matching bubbles that are touching our bubbles
        for b in matches:
            for onBoard in self.board_bubbles:
                if (self.board_bubbles == 0):
                    pass
                if collide(b.pos, onBoard.pos) and bubble.colour == onBoard.colour: # TODO: we should NOT be comparing on colour
                    # it's matching and touching
                    if onBoard not in matches:
                        matches.append(onBoard)

        self.current_matches = matches
        return
        
    def popMatches(self):
        '''
        'pops' the matches and then displays a good job message
        '''
        bubble = self.shoot_bubble
        bubble.erase(self.gameDisplay)
        bubble.draw(self.gameDisplay)
        matches = self.current_matches
        if matches != [bubble]:
            # erase the matches
            for b in matches:
                b.erase(self.gameDisplay)
                index = self.board_bubbles.index(b)
                self.board_bubbles.pop(index)
                b.colour = WHITE
            bubble.erase(self.gameDisplay)

            # send good job message
            print("You popped bubbles!")
            self.success_popped = True
        return

    def drawBoard(self):
        # draw white board
        pygame.draw.rect(self.gameDisplay, WHITE, (HELP_X, HELP_Y, HELP_WIDTH, HELP_WIDTH), 0)
        # draw board outline
        self.board = pygame.draw.rect(self.gameDisplay, BLACK, \
                                      (self.left, self.top, self.width, self.height), 2)

        # draw help box
        self.help_box = pygame.draw.rect(self.gameDisplay, BLACK, (0, 0, 100, 40), 2)
        meme_font = pygame.font.SysFont('Comic Sans MS', 25)
        help_meme = meme_font.render('HELP', False, BLACK)
        self.gameDisplay.blit(help_meme, (20, 5))

    def drawAllBubbles(self):
        self.drawShootBubble()
        for bubble in self.board_bubbles:
            if (bubble != 0):
                bubble.draw(self.gameDisplay)

    def drawShootBubble(self):
        self.shoot_bubble.drawAsGrey(self.gameDisplay)

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
        #print(bubbleList)

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
        self.gameDisplay.blit(right_meme, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.02)))
        self.gameDisplay.blit(right_meme_pt2, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.04)))
        self.gameDisplay.blit(right_meme_pt3, (int(DISPLAY_X * 0.76), int(DISPLAY_Y * 0.06)))
        if self.won:
            # create the success popup
            success_poppup = Popup('You Won! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5), self.gameDisplay, BLUE)
            self.current_popups.append(success_poppup)
            success_poppup.create()
            # store the popup for deletion later
            # POPUP = ['Words Matched! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5)]
            # create second success popu TODO: this is a meme, remove it
            success_poppup2 = Popup('Winner, winner, chicken dinner', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.4), self.gameDisplay, BLUE)
            self.current_popups.append(success_poppup2)
            success_poppup.create()
        elif self.success_popped:
            # create the success popup
            popped_bubble = Popup('Words Matched! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5), self.gameDisplay, BLUE)
            self.current_popups.append(popped_bubble)
            popped_bubble.create()
            # start the counter
            POPUP_COUNTER += 1
            # store the popup for deletion later
            #POPUP = ['Words Matched! Good Job!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.5)]
        elif self.game_over:
            # create the game over popup
            lost_popup = Popup('Game over man, game over!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.4), self.gameDisplay, RED)
            self.current_popups.append(lost_popup)
            lost_popup.create()
            # start the counter
            POPUP_COUNTER += 1
            # store the popup for deletion later
            #POPUP = ['Game over man, game over!', int(DISPLAY_X * 0.35), int(DISPLAY_Y * 0.4)]

    def displayHelpBox(self):
        """ displays the help box for the user """
        meme_font = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.draw.rect(self.gameDisplay, WHITE, (HELP_X, HELP_Y, HELP_WIDTH, HELP_WIDTH), 0)
        pygame.draw.rect(self.gameDisplay, BLACK, (HELP_X, HELP_Y, HELP_WIDTH, HELP_WIDTH), 2)
        for i, l in enumerate(HELP_MSG):
            self.gameDisplay.blit(meme_font.render(l, 0, BLACK), (HELP_X + 5, HELP_Y + 32 * i))
            # meme_font.render(l, False, BLACK)
        pygame.display.update()

        # pause until user presses a button
        paused = True
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN:
                    paused = False
                    self.drawBoard()
                    self.drawAllBubbles()
                    self.addToBoard()
