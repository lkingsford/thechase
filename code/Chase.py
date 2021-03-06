import pygame
import main_menu

from pygame.locals import *

# Initialise Pygame
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('The Chase')
surface = pygame.Surface((1280, 720))
pygame.font.init()
fullscreen = False

# Chase.py is structured as a nested state machine. Any states beyond the
# root state are passed down to children - hence, the Main Menu state
# holds the Game state and passes the draw or input down the line.
# This may not make sense for a larger project, but I consider that it
# does here.

start_state = main_menu.MainMenu()  # The initial state
running = True                      # Set to false if close button

while (start_state.update() & running):
    start_state.draw(surface)
    screen.blit(surface, (0, 0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        else:
            start_state.take_input(event)

# Close Pygame
pygame.quit()
