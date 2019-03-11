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
    d = {}
    #TODO: error handle incorrect args
    if mode == 'Synonym':
        table2 = 'SynWords'
    elif mode == 'Antonym':
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
    print(WORDS)

# def dict_factory(cursor, row):
#     d = {}
#     print(cursor.fetchall())
#     for idx, col in enumerate(cursor.fetchall()):
#         if col
#         d[col[idx]] = row[idx]
#     return d

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
