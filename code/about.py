import state
import game
import pygame

from pygame.locals import *
from data import *

class About(state.State):
    """The Main Menu"""
    def __init__(self):
        super().__init__()
        self.state = None
        self.to_exit = False; 
    
    
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
            version_text = item_font.render(get_asset("Version")[:-1], False,
                (0, 0, 0))
            version_position = (100, 400)
            surface.blit(version_text, version_position)               

            for item_number, item in enumerate(get_asset("AboutText")):
                item_text = item_font.render(item[:-1],False, (0,0,0));
                item_position = \
                (((surface.get_width() - item_text.get_width()) / 2), 
                    460 + (item_text.get_height() + 10) * item_number)
                surface.blit(item_text, item_position);
                    
    
    def take_input(self, event):
       """Close window on any mouse or key input
        Keyword arguments:
            event - the event to process
        Returns:
            none
        """
       if self.state != None:
            self.state.take_input(event);    
            return;
       
       if event.type == KEYDOWN:
           self.to_exit = True
                       
       if event.type == MOUSEBUTTONDOWN:
           self.to_exit = True
           
           
    def update(self):
        """Process the next frame
        Keyword arguments:
            none
        Returns:
            True if still running, False if finished
        """

        if self.state != None:
            self.state.update();
                
        return not(self.to_exit);           
