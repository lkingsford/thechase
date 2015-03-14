import pathfinding

from enum import Enum

class Character:
    """A character in the game
    """
    def __init__(self,
        location,
        game_map,
        asset,
        health = 3,
        attack_strength = 1,
        team = 0):
        self.location = location
        self.game_map = game_map
        self.asset = asset        
        self.health = health
        self.max_health = health
        self.team = team
        game_map.characters.append(self)
        self.active = True
        self.attack_strength = attack_strength        
        
        
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
                next_step = pathfinding.get_route(self.game_map,
                    self.location, enemy.location)
                if len(next_step) > 0:
                    self.move_to_location(next_step[1])           
            else:
                self.move(Action.wait)
           
    def move(self, action):
        """ Move in the direction indicated by action"""
        if action == Action.n:
            desired_location = self.location[0], self.location[1] - 1
        if action == Action.ne:
            desired_location = self.location[0] + 1, self.location[1] - 1
        if action == Action.e:
            desired_location = self.location[0] + 1, self.location[1] 
        if action == Action.se:
            desired_location = self.location[0] + 1, self.location[1] + 1
        if action == Action.s:
            desired_location = self.location[0], self.location[1] + 1
        if action == Action.sw:
            desired_location = self.location[0] - 1, self.location[1] + 1
        if action == Action.w:
            desired_location = self.location[0] - 1, self.location[1]
        if action == Action.nw:
            desired_location = self.location[0] - 1, self.location[1] - 1
        if action == Action.wait:
            desired_location = self.location[0], self.location[1]                        
        
        self.move_to_location(desired_location)
    
    
    def move_to_location(self, desired_location):
        """ Move to desired_location. Checks walkable, not distance.
        If there's somebody there - stop (if friendly) or attack (if not)"""
        # This should be refactored into GameMap
        walkable = self.game_map.inner_map[desired_location[0]]\
                    [desired_location[1]].walkable()
        
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
            if walkable:
                self.location = desired_location


    def attack(self, target):
        killed = target.attacked(self.attack_strength, self)


    def attacked(self, damage, attacker):
        """ Attacks the creature. Returns True if they were killed. """
        self.health -= damage
        if self.health <= 0:
            return True
        else:
            return False
            
    
    def alive(self):
        return self.health > 0


class Action(Enum):
    n = 0
    ne = 1
    e = 2
    se = 3
    s = 4
    sw = 5
    w = 6
    nw = 7
    wait = 8
    teleport = 9
    shoot = 10
