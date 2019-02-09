import pygame

# global values for the display size
# (we will always multiply these so that we can scale the resolution)
DISPLAY_X = 800
DISPLAY_Y = 600

pygame.init()

gameDisplay = pygame.display.set_mode((DISPLAY_X, DISPLAY_Y))
pygame.display.set_caption('Version 0.1')

clock = pygame.time.Clock()

crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()
    clock.tick(60)

