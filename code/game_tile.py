class GameTile:
    """ A tile on a GameMap """
    def __init__(self, 
                 floor_tile, 
                 wall_tile = None,
                 walkable = True,
                 on_walk_event = None):
        """ Create a new game tile
        Keyword arguments:
            floor_tile - Which floor asset to use
            walk_tile - Which wall asset to use
            walkable - Whether the tile can be walked on
            on_walk_event - Called when the player walks on the tile
        """
        self.floor_tile_ = floor_tile;
        self.wall_tile_ = wall_tile;
        self.walkable_ = walkable;
        self.on_walk_event_ = on_walk_event;
    
    def floor_tile(self):
        return self.floor_tile_
    
    def wall_tile(self):
        return self.wall_tile_
    
    def walkable(self):
        return self.walkable_        
