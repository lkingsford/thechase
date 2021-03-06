import state
import game
import about
import controls

import pygame

from pygame.locals import *
from data import *

class MainMenu(state.State):
    """The Main Menu"""
    def __init__(self):
        super().__init__()
        self.state = None
        self.to_exit = False;
        # Create menu options
        # In format:
        #   Text, Code to run, Physical rect on screen
        self.menu = [("Start Game", self.start_game, None),
                     ("How To Play", self.controls, None),
                     ("About", self.about, None),
                     ("Exit", self.exit, None)]
        self.selected = 0;
    
    def draw(self, surface):
        """Draw the state to the surface
        Keyword arguments:
            surface - PyGame surface to draw to
        Returns:
            none
        """
        if self.state != None:
            self.state.draw(surface);
        else:
            surface.fill((255,255,255))
            # Draw title
            title_text = get_asset("TitleFont").render("The Chase", True,
                (0, 0, 0)) 
            title_position = \
                (((surface.get_width() - title_text.get_width()) / 2), 100)
            surface.blit(title_text, title_position)       
            item_font = get_asset("MenuFont");            
            # Draw menu items
            for item_number, item in enumerate(self.menu):
                if self.selected == item_number:
                    item_color = (0, 143, 193)
                else:
                    item_color = (0, 0, 0)
                item_text = item_font.render(item[0], True, item_color);
                item_position = \
                (((surface.get_width() - item_text.get_width()) / 2), 
                    400 + (item_text.get_height() + 10) * item_number)
                surface.blit(item_text, item_position);
                
                # If there is no rect (for mouse) set, then set one
                if (item[2] == None):
                    self.menu[item_number] = (item[0], item[1], 
                        pygame.Rect(item_position, item_text.get_size()))
                    
    
    def take_input(self, event):
       """Accept and process any input
        Keyword arguments:
            event - the event to process
        Returns:
            none
        """
       if self.state != None:
            self.state.take_input(event)
            return
       
       if event.type == KEYDOWN:
           if event.key == pygame.K_DOWN:
               self.selected += 1
               self.selected = self.selected % len(self.menu)
               
           if event.key == pygame.K_UP:
               self.selected -= 1
               self.selected = self.selected % len(self.menu)
           
           if event.key == pygame.K_RETURN or\
               event.key == pygame.K_SPACE or\
               event.key == pygame.K_KP_ENTER:               
               self.menu[self.selected][1]()
       
       if event.type == MOUSEMOTION:
           for item_number, item in enumerate(self.menu):
               if item[2] != None:
                   if item[2].collidepoint(event.pos):
                       self.selected = item_number
                       break;
                       
       if event.type == MOUSEBUTTONDOWN:
           for item_number, item in enumerate(self.menu):
               if item[2] != None:
                   if item[2].collidepoint(event.pos):
                       self.selected = item_number
                       self.menu[self.selected][1]()
                       break;
                       

    def update(self):
        """Process the next frame
        Keyword arguments:
            none
        Returns:
            True if still running, False if finished
        """

        if self.state != None:
            if self.state.update():
                return not(self.to_exit)
            else:
                self.state = None;
                
        return not(self.to_exit)
        
        
    def start_game(self):
        """ Start the game state
        Keyword arguments:
            none
        Returns:
            none
        """
        
        # Set the state to a new game object
        self.state = game.Game();
        
    def exit(self):
        """ Exit the menu (and hence the game)
        Keyword arguments:
            none
        Returns:
            none
        """
        
        self.to_exit = True;
        
    def about(self):
        """ Go to the About screen
        Keyword arguments:
            none
        Returns:
            none
        """
        self.state = about.About();
        
    def controls(self):
        """ Go to the Control screen
        Keyword arguments:
            none
        Returns:
            none
        """
        self.state = controls.Controls();
