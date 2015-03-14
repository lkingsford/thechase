class State:
    """A generic state.  """
    def __init__(self):
        """Initialise the state """
        pass;
        
        
    def draw(self, surface):
        """Draw the state to the surface
        Keyword arguments:
            surface     PyGame surface to draw to
        Returns:
            none
        """
        pass;
        
        
    def take_input(self, event):
       """Accept and process any input
        Keyword arguments:
            event - the event to process
        Returns:
            none
        """
       pass
        
   
    def update(self):
        """Process the next frame
        Keyword arguments:
            none
        Returns:
            True if still running, False if finished
        """
        return False
        
    
