from bubble import *
from popup import Popup
from globe import *

import time
import math
import random
import pygame
from scipy.spatial import KDTree


def calcBoard(board):
    """ this calculates the size of the board array """
    row_num = 0
    board_len = 0
    bubbleAreaWidth = board.width
    num_bubbles = int(math.floor(bubbleAreaWidth/(BUBBLE_RADIUS * 2)))
    bubbles_len = (num_bubbles * 3) - 1 # middle row has 1 less
    board_len = (num_bubbles * 5) - 2 # middle and last row have 1 less
    return bubbles_len, board_len

#this is copied from bubbles, so it should be generalized
def find_collide(pos1, pos2):
    """ checks if 2 points are within x*radius of eachother """
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    dist = math.hypot(x, y)
    if dist <= 1.7 * BUBBLE_RADIUS: # this not being 2 * radius makes it easiier to "sneak" bubbles past
        # collision
        return True
    else:
        # no collision
        return False

row1 = range(0,4)
row2 = range(5,8)
row3 = range(9,13)
row4 = range(14,17)
row5 = range(18, 22)
middle = [11, 20]
right = []
edges = [0, 4, 5, 8, 9, 13, 14, 17, 18, 22]


class Board:
    def __init__(self,  gameDisplay):
        self.top = int(DISPLAY_Y * 0.1)
        self.left = int(DISPLAY_X * 0.12)
        self.width = int(DISPLAY_X * 0.76)
        self.height = int(DISPLAY_Y * 0.8)
        self.future_bubbles = []
        self.bubbles_len = calcBoard(self)[0]
        self.board_len = calcBoard(self)[1]
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
        self.num_bubbles_poopped = 0

    def drawScore(self):
        meme_font = pygame.font.SysFont('Comic Sans MS', 35)
        big_meme_font = pygame.font.SysFont('Comic Sans MS', 60)

        # erase previous number
        pygame.draw.rect(self.gameDisplay, WHITE, (20, 120, 80, 120), 0)

        # draw score
        score_meme_1 = meme_font.render("SCORE", False, BLUE)
        score_meme_2 = big_meme_font.render(str(self.num_bubbles_poopped), False, BLUE)
        self.gameDisplay.blit(score_meme_1, (2, 80))
        self.gameDisplay.blit(score_meme_2, (30, 120))

    def nearest(self, pos, flag = True):
        #calculate the shots closest neighbor
        board_cpy = [x for x in self.board_positions] # [x for x in self.board_positions if x is not 0]
        for i in range(0, len(board_cpy)):
            if self.board_bubbles[i] != 0 and flag: #TODO: maybe calling the popped bubbles 0 is sloppy
                #remake that position super far away so we never match it
                board_cpy[i] = [-1, -1]
            if self.board_bubbles[i] == 0 and not flag: #to find nearest full bubble
                board_cpy[i] = [-1, -1]
        #print(len(self.board_bubbles), len(self.board_positions), len(board_cpy))
        kdtree = KDTree(board_cpy)
        dist, indice = kdtree.query(pos)

        return dist, indice
        # this causes a bug
        # try:
        #     indice = self.board_positions.index(board_cpy[indices])
        # except ValueError:
        #     return "ValueError", None

        # return dist, indice

    def determineDirection(self, dest_pos):
        pos1 = self.shoot_bubble.pos
        pos2 = dest_pos
        dif = pos1[0] - pos2[0]
        if dif == 0:
            self.shoot_bubble.direction = "up"
        elif dif < 0:
            self.shoot_bubble.direction = "left"
        elif dif > 0:
            self.shoot_bubble.direction = "right"
        return

    def checkBelow(self, index):
        direction = self.shoot_bubble.direction
        if self.board_bubbles[index] == 0:
            return index
        if direction == "right":
            i = index + 4
        elif direction =="left" or direction == "up":
            i = index + 4
        if index not in row5 and self.board_bubbles[i] == 0:
            return i
        if index in row5:
            return index - 1 #TODO: make this an whole error
        elif index in row4:
            self.checkBelow(i)
            return i
        elif index in row3:
            self.checkBelow(i)
            return i
        elif index in row2:
            self.checkBelow(i)
            return i
        elif index in row1:
            self.checkBelow(i)
            return i
        return index

    #this is an extremely naive implementation
    def checkAbove(self, index):
        direction = self.shoot_bubble.direction
        if self.board_bubbles[index] != 0:
            return self.checkBelow(index)
        if index in edges:
            return index
        if direction == "right":
                i = index - 4
        elif direction == "left" or direction == "up":
            i = index - 4
        if index in row5:
            self.checkAbove(i)
            return i
        elif index in row4:
            self.checkAbove(i)
            return i
        elif index in row3:
            self.checkAbove(i)
            return i
        elif index in row2:
            self.checkAbove(i)
            return i
        elif index in row1:
            self.checkAbove(i)
            return i
        return index


    #WARNING: very hacky function incoming
    def fix_pos(self, a, dest, og_pos):
        #first extend destination to the edge
        # TODO: this doesn't work
        # left_edge = self.left
        # right_edge = left_edge + self.width
        # top_edge = self.top + self.height
        # x = dest[0]
        # y = dest[1]
        # x2 = og_pos[0]
        # y2 = og_pos[1]
        # difX = x - x2
        # difY = y - y2
        # dist = math.sqrt(difX**2 + difY**2)
        # num_positions = int(dist / 10)
        # c = 0
        # while left_edge < x+(difX*(c+1)/num_positions) < right_edge and \
        #         y+(difY*(c+1)/num_positions) < top_edge:
        #     c+=1
        #     x = x+(difX*(c+1)/num_positions)
        #     y = y+(difY*(c+1)/num_positions)
        #     #self.shoot_pos.append((x, y))
        # dist, m = self.nearest((x, y))# self.shoot_pos[-1]
        # dest = self.board_positions[m]
        # print(dest)
        self.shoot_pos = self.shoot_bubble.move(dest, self.gameDisplay)
        path = self.shoot_pos
        found = False
        for i in range(0, len(path)):
            dist, ind = self.nearest(path[i], False)
            near_bubble = self.board_bubbles[ind]
            if near_bubble != 0 and find_collide(near_bubble.pos, path[i]):
                found = True
                new_spot = self.nearest(path[i])[1]
                #check if newspot is in first row and full
                if new_spot > 17 and self.board_bubbles[new_spot] != 0:
                    return "Game Over"
                self.shoot_bubble.pos = og_pos
                self.shoot_pos = self.shoot_bubble.move(self.board_positions[new_spot], self.gameDisplay)
                if new_spot == i:
                    return "Game Over"
                return new_spot
        return a
        
        
    def shootBubble(self, dest_pos):
        """ this will shoot a bubble from its current location to the position specified """
        hit_array = []

        #if find_collide(SHOOT_POSITION, dest_pos):
        #    self.game_over = True

        self.determineDirection(dest_pos)
        dist, i = self.nearest(dest_pos)
        # if dist == "ValueError":
        #     print("1")
            #return "ValueError"
        #i = self.checkAbove(i)
        snapped_dest = self.board_positions[i]
        #self.shoot_pos = self.shoot_bubble.move(snapped_dest, self.gameDisplay)
        i = self.fix_pos(i, snapped_dest, SHOOT_POSITION) #this is going to be ridiculously hacky because the board should calculate a bubble's path, not the bubble itself
        if i == "Game Over":
            return i
        bubble = self.shoot_bubble

        # remove from future bubbles
        try:
            self.future_bubbles.pop(self.future_bubbles.index((bubble.word, bubble.colour)))
        except ValueError:
            print("2")
            return "ValueError"

        # add shot bubble to board
        try:
            self.board_bubbles[i] = self.shoot_bubble
        except IndexError:
            print("3")
            return "IndexError"
        #self.shoot_bubble.pos = self.board_positions[i]

        # detect matches and pop as needed
        self.findMatches()

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
                #TODO: this fix is hacky, and we shouldn't make empty bubbles zeros probably
                if onBoard != 0 and \
                    collide(b.pos, onBoard.pos) and bubble.colour == onBoard.colour:
                    # TODO: we should NOT be comparing on colour
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

            # display good job message
            good_job = Popup("You popped bubbles! Good job!.", int(DISPLAY_X * 0.25), int(DISPLAY_Y * 0.30),
                             self.gameDisplay)
            good_job.create()
            pygame.display.update()

            for b in matches:
                b.erase(self.gameDisplay)
                index = self.board_bubbles.index(b)
                self.board_bubbles[index] = 0
                #b.colour = WHITE
                self.num_bubbles_poopped += 1
            bubble.erase(self.gameDisplay)

            # send good job message
            print("You popped bubbles!")
            self.success_popped = True

            time.sleep(0.3)
            good_job.erase()

        self.drawScore()
        self.shooting = False

        self.checkToRemoveColours()

        return

    def checkToRemoveColours(self):
        """ removes colors from shooting if they are no longer on the board """
        found_colours = []
        for b in self.board_bubbles:
            if b != 0:
                found_colours.append(b.colour)

        # print(found_colours)
        index_to_pop = []
        for i in range(0, len(self.future_bubbles)):
            if self.future_bubbles[i][1] not in found_colours:
                index_to_pop.append(i)

        for j in reversed(index_to_pop):
            self.future_bubbles.pop(j)

    def drawHelp(self):
        meme_font = pygame.font.SysFont('Comic Sans MS', 50)
        # draw help box
        self.help_box = pygame.draw.rect(self.gameDisplay, BLUE, (0, 0, 160, 80), 2)
        help_meme = meme_font.render('HELP', False, BLUE)
        self.gameDisplay.blit(help_meme, (20, 5))

    def drawBoard(self):
        # draw white board
        pygame.draw.rect(self.gameDisplay, WHITE, (self.left, self.top, self.width, self.height), 0)
        # draw board outline
        self.board = pygame.draw.rect(self.gameDisplay, BLACK, \
                                      (self.left, self.top, self.width, self.height), 2)

        # draw help
        self.drawHelp()

        # draw score
        self.drawScore()

    def drawAllBubbles(self):
        self.drawShootBubble()
        for bubble, position in zip(self.board_bubbles, self.board_positions):
            #print(self.board_positions)
            if (bubble != 0):
                bubble.draw(self.gameDisplay)

    def drawShootBubble(self):
        self.shoot_bubble.drawAsGrey(self.gameDisplay)

    def createWordList(self):
        """ this will populate the game board with words """
        # we're going to make two different words to shoot with the same color
        # so we'll pop the first word of a color we see so that we can add it
        # to the main word list under the same color
        found_color = [[False, False]] * NUM_WORDS

        # make a list of all the words with their associated colour
        word_colour_list = []
        for i in range(0, len(WORDS)):
            main_word = WORDS.keys()[i]
            colour = WORD_COLOURS[i]
            self.future_bubbles.append((main_word, colour))
            for word in WORDS[main_word]:
                if not found_color[i][0]:
                    found_color[i][0] = True
                    self.future_bubbles.append((word, colour))
                elif not found_color[i][1]:
                    found_color[i][1] = True
                    self.future_bubbles.append((word, colour))
                else:
                    word_colour_list.append((word, colour))

        # shuffle the list
        random.shuffle(word_colour_list)
        # loop through the list and create the bubbles
        bubbleList = self.createBubbles(word_colour_list)
        self.board_bubbles = bubbleList
        # for i in range(0, self.board_len - self.bubbles_len):
        #     self.board_bubbles.append(0)
        self.future_bubbles += self.future_bubbles
        random.shuffle(self.future_bubbles)

    def createBubbles(self, word_colour_list):
        row_num = 0
        bubbleLeft = self.left + BUBBLE_RADIUS + 3 # the position of the leftmost bubble
        bubbleTop = self.top + BUBBLE_RADIUS + 3 # the position of the topmost bubble
        bubbleAreaWidth = self.width
        bubbleList = []
        for i in range(0, len(self.board_positions)):
            if i < self.bubbles_len and i < len(word_colour_list):
                word_colour_pair = word_colour_list[i]
                currentBubble = Bubble(bubbleLeft, bubbleTop, \
                                word_colour_pair[0], word_colour_pair[1])
                bubbleList.append(currentBubble)
            else:
                bubbleList.append(0)
            self.board_positions[i] = [bubbleLeft, bubbleTop]
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
        #print(self.board_positions)
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
            self.success_popped = False
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
        pygame.draw.rect(self.gameDisplay, WHITE, (HELP_X, HELP_Y, HELP_WIDTH, HELP_HEIGHT), 0)
        pygame.draw.rect(self.gameDisplay, BLACK, (HELP_X, HELP_Y, HELP_WIDTH, HELP_HEIGHT), 2)
        for i, l in enumerate(HELP_MSG):
            self.gameDisplay.blit(meme_font.render(l, 0, BLACK), (HELP_X + 5, HELP_Y + 32 * i))
            # meme_font.render(l, False, BLACK)
        pygame.display.update()

        # pause until user presses a button
        paused = True
        while paused:
            for ev in pygame.event.get():
                if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                    paused = False
                    self.drawBoard()
                    self.drawAllBubbles()
                    self.addToBoard()
