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
WORDS = {
    'good':['nice','excellent','exceptional', 'wonderful', 'positive'], \
    'bad':['awful', 'evil','despicable', 'mean'], \
    'easy':['accessible', 'clear', 'effortless', 'obvious'], \
    'hard':['arduous', 'heavy', 'rough', 'tough'], \
    'cold':['chilled', 'cool', 'icy', 'snowy'], \
    'warm':['hot', 'balmy', 'heated', 'sunny']
}
WORD_COLOURS = [RED, GREEN, BLUE, YELLOW, PURPLE, TURQUOISE] #TODO: add colours as needed
