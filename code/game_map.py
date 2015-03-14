import random
import game_tile
import evil_tree
import cultist
import spectre
import flame
import health_pack
import boss
import teleporter
import player_character

from enum import Enum
from data import get_asset

TYPES_OF_WALLS = 6;
TYPES_OF_FLOORS = 6;
ENEMY_CHANCE = get_asset("Config")["ENEMY_CHANCE"];

class GameMap:
    """ The main game map.
    This is not a generically useful map for any roguelike game as it does
    some things in slower then usual ways in order to facilitate the horizontal
    scrolling.
    Make a game not an engine amirite?!
    
    The map has floors and walls. Floors are an integer saying which floor
    (in reality - 0 to 5 are different grasses). Walls are 0 if no wall, 
    otherwise 1-6 saying which type of tree
    """
    def __init__(self, active_size, extra_width, win_point):
        """ Initialise the map
        Keyword arguments:
            active_size - (width, height) of the play area
            extra_width - amount of columns to prepare beyond active_size
            win_point - x value at which wins
        Returns:
            none
        """       
        self.active_size = active_size
        
        # Initialise asset lists
        self.GrassAssets = [\
            "Grass1",
            "Grass2",
            "Grass3",
            "Grass4",
            "Grass5",
            "Grass6"]
        
        self.TreeAssets = [\
            "Tree1",
            "Tree2",
            "Tree3",
            "Tree4",
            "Tree5",
            "Tree6"]
            
        self.inner_map = []
                    
        self.characters = []
        self.health_packs = []
        
        self.win_point = win_point

        # How far across the map is
        # The magic number is the starting position of the player character
        # Should be a constant
        # I'll let future me worry about it
        # Maybe
        self.total_offset = -20

        # A region sets the amount of trees and types of enemies
        # Next Region is when the next one starts
        # Value forces it to initialse when first started
        self.next_region = -1

            
        # Corrodor thickness that the endzone starts at 
        self.corrodor = get_asset("Config")["END_ZONE_START_THICK"]

        # Create initial map        
        for i in range(active_size[0] + extra_width):
            self.add_column();        
                    
    
    def scroll(self):
        """ Scroll the map to the left
            Keyword arguments:
                none
            Returns:
                none
        """    
        # Remove leftmost colum
        self.inner_map.pop(0)
        
        # Update characters locations
        for i in self.characters:
            i.location = i.location[0] - 1, i.location[1]            
            # Remove characters who are no longer active
            if (i.location[0] < 1):
                i.game_end_state = player_character.GameEndState.consumed
                self.characters.remove(i)                
        
        for i in self.health_packs:
            i.location = i.location[0] - 1, i.location[1]     
            if (i.location[0] < 1):
                self.health_packs.remove(i)
        
        # Create new column
        self.add_column()
        
        # Adjust total offset to reflect absolute position
        # Absolute character position  x is the position + total_offset
        self.total_offset += 1
        
        
    def add_column(self):
        """ Add another column of map to the right
            Keyword arguments:
                blocked_amount - chance that any square will be blocked
            Returns:
                none
        """
        self.next_region -= 1
        
        if self.next_region <= 0:
            self.next_region = random.randint(20, 40)
            self.new_trees = random.random() * 0.2 + 0.1
            self.keep_tree_adjacent = random.random() * 0.5 + 0.2
            self.keep_tree_diagonal = random.random() * 0.5 + 0.2            
        
        new_column = []        
        
        # If in the normal area
        if ((self.active_size[0] + self.total_offset) < \
            (get_asset("Config")["GAME_DISTANCE"] - \
            get_asset("Config")["END_ZONE"])):  

            last_column = []
            if len(self.inner_map) > 0:
                last_column = self.inner_map[-1]
            else:            
                for i in range(self.active_size[1]):
                    last_column.append(None)
                    
            for i in range(self.active_size[1]):
                # Check if blocked
                blocked_new = random.random() < self.new_trees
                blocked_adj = last_column[i] == None and \
                              random.random() < self.keep_tree_adjacent;
                blocked_diag = False
                
                blocked = blocked_new or blocked_adj or blocked_diag;
                
                # Force blocked if first or last tile
                if (i == 0) or (i == (self.active_size[1] - 1)):
                    blocked = True
                # Pick a type of floor
                floor_asset = random.choice(self.GrassAssets)
                # If blocked, pick type of walls
                if blocked:
                    wall_asset = random.choice(self.TreeAssets)
                else:
                    wall_asset = None;
                    
                new_column.append(game_tile.GameTile(floor_asset,
                    wall_asset, not(blocked)))
            
            # Maybe add an enemy
            new_enemy = random.random() < ENEMY_CHANCE
            if new_enemy:
                y = random.randint(0, self.active_size[1] - 1)
                tries = 0
                failed = False
                while (not(new_column[y].walkable())):
                    tries += 1
                    y = random.randint(0, self.active_size[1] - 1)
                    if tries > 10:
                        failed = True
                        break
                if not(failed):
                    monster = random.choice ([
                        flame.Flame,
                        evil_tree.EvilTree,
                        cultist.Cultist,
                        spectre.Spectre
                        ])((len(self.inner_map), y), self)
            
            # Maybe add a health pack
            add_health_pack = random.random() < \
                get_asset("Config")["HEALTH_PACK_CHANCE"]
            if add_health_pack:
                y = random.randint(0, self.active_size[1] - 1)
                tries = 0
                failed = False
                while (not(new_column[y].walkable())):
                    tries += 1
                    y = random.randint(0, self.active_size[1] - 1)
                    if tries > 10:
                        failed = True
                        break
                if (not(failed)):
                    self.health_packs.append( \
                        health_pack.HealthPack((len(self.inner_map), y)))      
            
        # If in the end zone
        elif ((self.active_size[0]) + self.total_offset < \
            get_asset("Config")["GAME_DISTANCE"]):
            height = get_asset("Config")["MAP_HEIGHT"]
            self.corrodor = max(2, min(get_asset("Config")["MAP_HEIGHT"]-2,
                self.corrodor + random.randint(-1,1)))
            corrodor = self.corrodor
            tree_thickness = (height - corrodor) // 2
            blocked = []
            for i in range(tree_thickness):
                blocked.append(True)
            for i in range(corrodor):
                blocked.append(False)
            for i in range(tree_thickness):
                blocked.append(True)
            if (len(blocked) < self.active_size[1]):
                blocked.append(True)            
            for i in blocked:
                # Pick a type of floor
                floor_asset = random.choice(self.GrassAssets)
                # If blocked, pick type of walls
                if i:
                    wall_asset = random.choice(self.TreeAssets)
                else:
                    wall_asset = None;
                    
                new_column.append(game_tile.GameTile(floor_asset,
                    wall_asset, not(i)))       
                
            if (self.active_size[0]) + self.total_offset == \
                get_asset("Config")["GAME_DISTANCE"] - \
                get_asset("Config")["END_ZONE"] + \
                get_asset("Config")["BOSS_DISTANCE"]:
                    # CREATE DA BOSS!
                    boss.Boss((len(self.inner_map), height // 2), self)
            
        # It at the end
        else:             
            height = get_asset("Config")["MAP_HEIGHT"]
            corrodor = 4
            tree_thickness = (height - corrodor) // 2
            blocked = []
            for i in range(tree_thickness):
                blocked.append(True)
            for i in range(corrodor):
                blocked.append(False)
            for i in range(tree_thickness):
                blocked.append(True)
            if (len(blocked) < self.active_size[1]):
                blocked.append(True)            
            for i in blocked:
                # Pick a type of floor
                floor_asset = random.choice(self.GrassAssets)
                # If blocked, pick type of walls
                if i:
                    wall_asset = random.choice(self.TreeAssets)
                else:
                    wall_asset = None;
                    
                new_column.append(game_tile.GameTile(floor_asset,
                    wall_asset, not(i)))

        if (self.active_size[0]) + self.total_offset == \
            get_asset("Config")["GAME_DISTANCE"]:
            car = game_tile.GameTile(floor_asset, "Car1", False)
            new_column[height // 2] = car

        if (self.active_size[0]) + self.total_offset == \
            (get_asset("Config")["GAME_DISTANCE"] + 1):
            car = game_tile.GameTile(floor_asset, "Car2", False)
            new_column[height // 2] = car
                        
        self.inner_map.append(new_column)
         
        
    
    def walkable(self, location):
        # This is ugly, but I'm running out of time
        try:
            if (0 <= location[0] < self.active_size[0]) and \
                (0 <= location[1] < self.active_size[1]):
                return self.inner_map[location[0]][location[1]].walkable()
            else:
                return False
        except IndexError:
            return False
