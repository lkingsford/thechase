import state
import game
import pygame

from pygame.locals import *
from data import *

class Controls(state.State):
    """The Control Screen"""
    def __init__(self):
        super().__init__()
        self.state = None
        self.to_exit = False; 
        self.current_screen = 0       
    
    
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
            if self.current_screen == 0:            
                screen_to_draw = get_asset("ControlsScreen")
                surface.blit(screen_to_draw, (0,0))                
            if self.current_screen == 1:
                # item_font = get_asset("MenuFont");     
                # for item_number, item in enumerate(get_asset("HowToPlay")):
                    # item_text = item_font.render(item, True, (0,0,0));
                    # item_position = \
                    # (((surface.get_width() - item_text.get_width()) / 2), 
                        # 50 + (item_text.get_height() + 10) * item_number)
                    # surface.blit(item_text, item_position);
                screen_to_draw = get_asset("ControlsScreen2")
                surface.blit(screen_to_draw, (0,0))                                
    # 
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
           if self.current_screen == 1:
               self.to_exit = True
           else:
               self.current_screen += 1
                       
       if event.type == MOUSEBUTTONDOWN:
           if self.current_screen == 1:
               self.to_exit = True
           else:
               self.current_screen += 1           
           
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
