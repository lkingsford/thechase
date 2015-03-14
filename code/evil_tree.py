import character
import random

from data import get_asset

EVIL_TREE_HEALTH = get_asset("Config")["EVIL_TREE_HEALTH"]
EVIL_TREE_ATTACK = get_asset("Config")["EVIL_TREE_ATTACK"]
EVIL_TREE_RANGE = get_asset("Config")["EVIL_TREE_RANGE"]

class EvilTree(character.Character):
    """This is what happens when TrEeS cOmE aLiVe!
    """
    
    def __init__(self, location, game_map):	
        assets = [
            ("Tree1", "Eviltree1"),
            ("Tree2", "Eviltree2"),
            ("Tree3", "Eviltree3"),
            ("Tree4", "Eviltree4"),
            ("Tree5", "Eviltree5"),
            ("Tree6", "Eviltree6")]
        self.tree_asset = random.choice(assets)
        super().__init__(location, game_map, self.tree_asset[0],
            EVIL_TREE_HEALTH, EVIL_TREE_ATTACK)
        self.active = False
            
    
    def update(self):        
        # Activate tree if enemy gets close
        enemies = [i for i in self.game_map.characters if i.team != self.team]
        for i in enemies:
            # This may not be the best way to check for range
            if (abs(i.location[0] - self.location[0]) <= EVIL_TREE_RANGE) and \
                (abs(i.location[1] - self.location[1]) <= EVIL_TREE_RANGE):
                self.activate()
                
        super().update();
     
     
    def attack(self, target):
        # Scroll map if hits PC
        if target.team == 1:
            self.game_map.scroll();

     
    def activate(self):
        self.asset = self.tree_asset[1]
        self.active = True