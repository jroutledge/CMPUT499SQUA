WORDS = {}
# Global values from our database
def init(grade_level, mode):
    import sqlite3
    import os
    from random import randint
    import numpy as np
    global WORDS, NUM_WORDS

    path, f = os.path.split(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/words.db')

    print(path)

    d = {}
    #TODO: error handle incorrect args
    if mode.lower() == 'synonym':
        table2 = 'SynWords'
    elif mode.lower() == 'antonym':
        table2 = 'AntWords'
    else:
        table2 = 'error'
    #conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute('SELECT w.word, s.syn \
               FROM StartWords w, {0} s \
               WHERE w.grade_level = {1} \
               AND w.word = s.word'.format(table2, grade_level))
    all_rows = c.fetchall()
    for i in all_rows:
        word = str(i[0].encode("utf-8"))
        similar = str(i[1].encode("utf-8"))
        if word in d.keys():
            d[word].append(similar)
        else:
            d[word] = [similar]

    word_indexes = []
    for i in range(0, NUM_WORDS):
        word_indexes.append(randint(0, len(d.keys()) - 1))
    
    for i in word_indexes:
        key = d.keys()[i]
        val = d[key]
        WORDS[key] = val
    #print(WORDS)

# Global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 1000#800
DISPLAY_Y = 1000#600
BUBBLE_RADIUS =  int((DISPLAY_X * DISPLAY_Y) / 15000)
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
# WORDS = {
#     'good':['nice','excellent','exceptional', 'wonderful', 'positive'], \
#     'bad':['awful', 'evil','despicable', 'mean'], \
#     'easy':['accessible', 'clear', 'effortless', 'obvious'], \
#     'hard':['arduous', 'heavy', 'rough', 'tough'], \
#     'cold':['chilled', 'cool', 'icy', 'snowy'], \
#     'warm':['hot', 'balmy', 'heated', 'sunny']
# }
WORD_COLOURS = [RED, GREEN, BLUE, YELLOW, PURPLE, TURQUOISE] #TODO: add colours as needed
NUM_WORDS = len(WORD_COLOURS)

# Globals for helpp message
HELP_MSG = ["Game Instructions and Help: ", "",
            "To play game, try and match the words according to ",
            "their meanings. If playing on synonym mode, this ",
            "means matching words like 'big' and 'huge' together.",
            "If playing on antonym mode, this means matching ",
            "words like 'big' and 'small' together. Shoot the ",
            "bubble at the word you think it matches. You can do ",
            "this by clicking where you want the bubble to go on ",
            "the board. If it's a match it will pop, otherwise it ",
            "will stay. If you pop all the bubbles you win! ",
            "", "To exit this menu, press any key."]
HELP_X = int(DISPLAY_X * 0.12)
HELP_Y = int(DISPLAY_Y * 0.1)
HELP_WIDTH = int(DISPLAY_X * 0.76)
HELP_HEIGHT = int(DISPLAY_Y * 0.8)
