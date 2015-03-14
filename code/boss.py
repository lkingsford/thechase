import character
import player_character

from data import get_asset

BOSS_HEALTH = get_asset("Config")["BOSS_HEALTH"]
BOSS_ATTACK = get_asset("Config")["BOSS_ATTACK"]

class Boss(character.Character):
    def __init__(self, location, game_map):	
        super().__init__(location, game_map, "Boss", BOSS_HEALTH)
        self.attack_strength = BOSS_ATTACK
        
    def attacked(self, damage, attacker):
        killed = super().attacked(damage, attacker)
        if killed:
            # Attacker will be PC otherwise this will go badly
            attacker.game_end_state = player_character.GameEndState.won_killed
            
