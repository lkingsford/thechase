import character

from data import get_asset
from character import Action
from enum import Enum

HERO_HEALTH = get_asset("Config")["HERO_HEALTH"]
START_BULLETS = get_asset("Config")["START_BULLETS"]
START_TELEPORTS = get_asset("Config")["START_TELEPORTS"]
START_INITIAL_XP_REQUIRED = get_asset("Config")["START_INITIAL_XP_REQUIRED"]
XP_LEVELLING_MULTIPLIER = get_asset("Config")["XP_LEVELLING_MULTIPLIER"]
MAX_HEALTH_PER_LEVEL = get_asset("Config")["MAX_HEALTH_PER_LEVEL"]

class PlayerCharacter(character.Character):
    """The player character"""
    def __init__(self, location, game_map):
        super().__init__(location,
            game_map,
            "Hero",
            health = HERO_HEALTH,
            attack_strength = 1,
            team = 1)
        self.next_action = None
        self.bullets = START_BULLETS
        self.max_bullets = START_BULLETS
        self.teleports = START_TELEPORTS
        self.max_teleports = START_TELEPORTS
        self.xp = 0
        self.next_level = 12                
        self.game_end_state = GameEndState.still_going
        
     
    def update(self):
        """ Make character move/perform current action
            Keyword arguments:
                none
            Returns:
                none
        """
        if self.next_action == None:
            return

        if 0 <= self.next_action.value <= 8:
            self.move(self.next_action)
            health_packs = [i for i in self.game_map.health_packs if
                            i.location == self.location]
            for i in health_packs:
                self.game_map.health_packs.remove(i)
                self.health = self.max_health;
        
        if self.next_action == Action.shoot:
            self.shoot()
        
        if self.next_action == Action.teleport:
            self.teleport()
        
        self.next_action = None
        

    def attack(self, target):
        self.attack_with_damage(target, self.attack_strength)


    def attack_with_damage(self, target, damage):
        killed = target.attacked(damage, self)
        # Add XP
        # If over max, go up a level
        if killed:
            self.xp += target.max_health + target.attack_strength
            if self.xp > self.next_level:
                self.level_up()
    
    
    def level_up(self):
        self.xp -= self.next_level
        self.attack_strength += 1
        self.next_level = self.next_level * XP_LEVELLING_MULTIPLIER
        self.health += MAX_HEALTH_PER_LEVEL
        self.max_health += MAX_HEALTH_PER_LEVEL
        

    def do(self, action):
        """Perform an action
            Keyword arguments:
                action - action to perform
            Returns:
                none
        """
        self.next_action = action
        
     
    def shoot(self):
        """ Shoot directly in front of player 
            Shooting removes all health from an enemy
        """
        if (self.bullets > 0):
            self.bullets -= 1
            for fx in range(self.location[0], self.game_map.active_size[0]):
                enemy_hit = [i for i in self.game_map.characters \
                             if i.location == (fx, self.location[1]) and \
                             i.team != self.team ]
                if len(enemy_hit) > 0:
                    for i in enemy_hit:
                        self.attack_with_damage(i, i.health)                
                    break;
        # Get a free move to the right
        self.move(Action.e)
  
  
    def teleport(self):
        """ Teleport forward 2 spaces, and keep going forward if blocked by
            trees
        """
        if (self.teleports > 0):
            desired_location = (self.location[0] + 2, self.location[1])
            if desired_location[0] <= self.game_map.active_size[0]:
                while (not self.game_map.walkable(desired_location)):
                    desired_location = (desired_location[0] + 1,
                        self.location[1])   
                    if desired_location[0] > self.game_map.active_size[0]:
                        return;
                self.location = desired_location[0], self.location[1]
                self.teleports -= 1
                # Telefrag if somebody there
                enemy_hit = [i for i in self.game_map.characters \
                             if i.location == self.location and \
                             i.team != self.team ]
                if len(enemy_hit) > 0:
                    for i in enemy_hit:
                        self.attack_with_damage(i, i.health)


    def attacked(self, damage, attacker):        
        self.health -= damage
        if self.health <= 0:
            self.game_end_state = GameEndState.dead
            return True
        else:
            return False


class GameEndState(Enum):
    still_going = 0
    dead = 1
    consumed = 2
    won_killed = 3
    won_escaped = 4
                        
                        
                        
