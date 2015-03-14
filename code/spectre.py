import character

from data import get_asset
from character import Action

SPECTRE_HEALTH = get_asset("Config")["SPECTRE_HEALTH"]
SPECTRE_ATTACK = get_asset("Config")["SPECTRE_ATTACK"]

class Spectre(character.Character):
    def __init__(self, location, game_map):	
        super().__init__(location, 
            game_map, 
            "Spectre",
            SPECTRE_HEALTH,
            SPECTRE_ATTACK)
        
        
    def update(self):
        """Make character move/perform current action"""
        if self.active:
            # Find Enemy (ie player)
            # This would normally be nearest, but there's only
            # going to be one enemy in the whole darn game - so simplified

            enemies = \
                [i for i in self.game_map.characters if i.team != self.team]
            if len(enemies) > 0:
                enemy = enemies[0]
                desired_location = \
                    (self.location[0] - \
                        change_direction(self.location[0], enemy.location[0]),
                    self.location[1] - \
                        change_direction(self.location[1], enemy.location[1]))                     
                self.move_to_location(desired_location)           
            else:
                self.move(Action.wait)


    def move_to_location(self, desired_location):
        """ Move to desired_location. It replaces the other as can move
        through trees.
        If there's somebody there - stop (if friendly) or attack (if not)"""
        # This should be refactored into GameMap        
        characters_on_tile = [i for i in self.game_map.characters \
                              if i.location[:2] == desired_location[:2]]
                              # Those ':2's are there as there may be more 
                              # then two in the tuplet, as fed from the
                              # pathfinding
        
        if len(characters_on_tile) > 0:
            for i in characters_on_tile:
                if i.team == self.team:
                    # Just making behaviour explicit. Does nothing if friends.
                    pass 
                else:
                    self.attack(i)
                
        else:        
            self.location = desired_location


def change_direction(current, next):
    """ Convenience function that returns
            1 if next < current,
            0 if next == current,
            -1 if next > current
    """
    if next > current:
        return -1
    elif next == current:
        return 0
    else:
        return 1