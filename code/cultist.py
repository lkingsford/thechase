import character

from data import get_asset

CULTIST_HEALTH = get_asset("Config")["CULTIST_HEALTH"]
CULTIST_ATTACK = get_asset("Config")["CULTIST_ATTACK"]

class Cultist(character.Character):
    def __init__(self, location, game_map):	
        super().__init__(location, game_map, "Cultist", CULTIST_HEALTH)
        self.attack_strength = CULTIST_ATTACK