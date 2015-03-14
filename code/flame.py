import character

from data import get_asset

FLAME_HEALTH = get_asset("Config")["FLAME_HEALTH"]
FLAME_ATTACK = get_asset("Config")["FLAME_ATTACK"]

class Flame(character.Character):
    def __init__(self, location, game_map):	
        super().__init__(location,
            game_map,
            "Flame",
            FLAME_HEALTH,
            FLAME_ATTACK)