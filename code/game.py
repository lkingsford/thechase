import state
import pygame
import game_map
import random
import player_character

from pygame.locals import *
from data import *
from character import Action
from player_character import GameEndState

TILE_WIDTH = get_asset("Config")["TILE_WIDTH"]
TILE_HEIGHT = get_asset("Config")["TILE_HEIGHT"]
MAP_WIDTH = get_asset("Config")["MAP_WIDTH"]
MAP_HEIGHT = get_asset("Config")["MAP_HEIGHT"]
HUD_HEIGHT = get_asset("Config")["HUD_HEIGHT"]
UNDER_HUD_HEIGHT = get_asset("Config")["UNDER_HUD_HEIGHT"]
ACTIVE_WIDTH = get_asset("Config")["ACTIVE_WIDTH"]
ACTIVE_HEIGHT = get_asset("Config")["ACTIVE_HEIGHT"]
EXTRA_MAP_WIDTH = get_asset("Config")["EXTRA_MAP_WIDTH"]
HEALTH_PIP_OFFSET = get_asset("Config")["HEALTH_PIP_OFFSET"]
GAME_DISTANCE = get_asset("Config")["GAME_DISTANCE"]
PROGRESS_OFFSET = get_asset("Config")["PROGRESS_OFFSET"]

class Game(state.State):
    """The Main Game of The Chase"""
    def __init__(self):
        super().__init__()
        self.state = None;
        self.to_exit = False;
        self.game_map = game_map.GameMap( \
            (ACTIVE_WIDTH, ACTIVE_HEIGHT), EXTRA_MAP_WIDTH, \
            GAME_DISTANCE)    
    
        # Assets that are used for the Black
        self.black_assets = [\
            "Black1",
            "Black2",
            "Black3",
            "Black4"]

        # Assets used for the health symbol
        # From most to least health
        self.heart_assets = [\
            "Heart1",
            "Heart2",
            "Heart3",
            "Heart4",
            "Heart5",
            "Heart6",
            "Heart7",
            "Heart8",
            "Heart9"]

        # Create the player character
        self.player_character = \
            player_character.PlayerCharacter((20, 5), self.game_map)
         
        # Whether the next turn is ready to update
        self.next_turn = False 
        
        self.game_done = False
        
        # Do the first turn
        self.process_turn()
        
        # Show the initial chunk of story        
        self.show_story(get_asset("StartStory"))
        
    
    def draw(self, surface):
        """Draw the state to the surface
        Keyword arguments:
            surface     PyGame surface to draw to
        Returns:
            none
        """
        if self.state != None:
            self.state.draw(surface)
            return
        
        # Start with black screen
        surface.fill((0, 0, 0))
        
        # Draw map
        # New surface for scaling
        playfield_surface = pygame.Surface((TILE_WIDTH * MAP_WIDTH, 
            TILE_HEIGHT * MAP_HEIGHT))
        # Draw floors and walls
        for ix, column in enumerate(self.game_map.inner_map):
            for iy, item in enumerate(column):
                location = (ix * TILE_WIDTH, iy * TILE_HEIGHT)
                if (item.floor_tile() != None):
                    playfield_surface.blit(get_asset(item.floor_tile()),
                        location)
                if (item.wall_tile() != None):
                    playfield_surface.blit(get_asset(item.wall_tile()),
                        location)                   
        
        # For drawing health pips - for speeds sake
        pip_width = get_asset("HealthPip").get_width();
        
        # Draw the characters
        for i in self.game_map.characters:
            location = i.location[0] * TILE_WIDTH, i.location[1] * TILE_HEIGHT
            playfield_surface.blit(get_asset(i.asset), location)
            # Draw health pips
            if i.team != 1 and i.active: # If not PC, and not hidden tree          
                for j in range(i.health):
                    pos = (TILE_WIDTH // 2 + i.location[0] * TILE_WIDTH -\
                        (i.health * pip_width) // 2 \
                        + j * pip_width,
                        i.location[1] * TILE_HEIGHT + HEALTH_PIP_OFFSET)
                    playfield_surface.blit(get_asset("HealthPip"), pos)                                                       

        # Draw Health Packs
        for i in self.game_map.health_packs:
            location = i.location[0] * TILE_WIDTH , i.location[1] * TILE_HEIGHT
            playfield_surface.blit(get_asset("HealthPack"), location)

        # Draw the BLACK
        for iy in range(ACTIVE_HEIGHT):
            location = (0, iy * TILE_HEIGHT)
            playfield_surface.blit(get_asset(self.black_tiles[iy]), location)
            
        # Darken tiles
        for ix in range(ACTIVE_WIDTH):
            for iy in range(ACTIVE_HEIGHT):
                # b stands for brightness here
                b = self.tile_brightness[ix][iy]
                playfield_surface.fill((b,b,b), 
                    (ix * TILE_WIDTH, iy * TILE_HEIGHT,
                        TILE_WIDTH, TILE_HEIGHT), BLEND_RGBA_MULT)
        
        # Scale playfield to screen size
        scale_amount = surface.get_width() / playfield_surface.get_width();
        scaled_surface = pygame.transform.scale(playfield_surface, 
            (round(scale_amount * playfield_surface.get_width()),
             round(scale_amount * playfield_surface.get_height())))
        
        # Draw scaled map        
        map_height = (surface.get_height() - scaled_surface.get_height()) / 2
        surface.blit(scaled_surface,(0, map_height))                  
        
        # Draw HUD
        # HUD will be above the map, scaled the same
        hud_surface = pygame.Surface((playfield_surface.get_width(), 
            HUD_HEIGHT))
        
        # Draw players current health        
        health_ratio = min(max(0, 1 - \
            (self.player_character.health / self.player_character.max_health)),
            1)
        heart_element = round(health_ratio * (len(self.heart_assets) - 1))
        heart_asset = get_asset(self.heart_assets[heart_element])
        hud_surface.blit(heart_asset, (50, 
            (HUD_HEIGHT - heart_asset.get_height()) // 2))
        
        # Draw bullets
        bullet_full_asset = get_asset("BulletFull")
        bullet_spent_asset = get_asset("BulletSpent")
        bullet_width = bullet_full_asset.get_width()
        bullet_dx = 80 
        for i in range(self.player_character.bullets):
            hud_surface.blit(bullet_full_asset, (bullet_dx, 
                (HUD_HEIGHT - bullet_full_asset.get_height()) // 2))
            bullet_dx += bullet_width
        for i in range(self.player_character.bullets + 1, 
            self.player_character.max_bullets + 1):
            hud_surface.blit(bullet_spent_asset, (bullet_dx, 
                (HUD_HEIGHT - bullet_full_asset.get_height()) // 2))
            bullet_dx += bullet_width
        
        # Draw teleports
        teleport_full_asset = get_asset("TeleportFull")
        teleport_spent_asset = get_asset("TeleportSpent")
        teleport_width = teleport_full_asset.get_width()
        teleport_dx = 160
        for i in range(self.player_character.teleports):
            hud_surface.blit(teleport_full_asset, (teleport_dx, 
                (HUD_HEIGHT - teleport_full_asset.get_height()) // 2))
            teleport_dx += teleport_width
        for i in range(self.player_character.teleports + 1, 
            self.player_character.max_teleports + 1):
            hud_surface.blit(teleport_spent_asset, (teleport_dx, 
                (HUD_HEIGHT - teleport_full_asset.get_height()) // 2))
            teleport_dx += teleport_width
        
        # Draw attack
        attack_asset = get_asset("Attack")
        for i in range (self.player_character.attack_strength):
            hud_surface.blit(attack_asset, 
                (240 + 6 * i, (HUD_HEIGHT - attack_asset.get_height()) // 2))
        
        # Draw XP Bar (under attack)
        hud_surface.blit(get_asset("XPBarEmpty"), (240, 
            (HUD_HEIGHT - attack_asset.get_height()) // 2 + \
            attack_asset.get_height() + 4))
        
        hud_surface.blit(get_asset("XPBarFull"), (240, 
            (HUD_HEIGHT - attack_asset.get_height()) // 2 + \
            attack_asset.get_height() + 4),
            (0, 0, 
                int(self.player_character.xp / \
                    self.player_character.next_level * \
                    get_asset("XPBarFull").get_width()),
                get_asset("XPBarFull").get_height())
            )

        # Draw HUD surface to screen
        scaled_surface = pygame.transform.scale(hud_surface, 
            (round(scale_amount * hud_surface.get_width()),
             round(scale_amount * hud_surface.get_height())))                       
        surface.blit(scaled_surface,(0, map_height - HUD_HEIGHT * scale_amount)) 

        # Draw lower HUD
        under_hud_surface = pygame.Surface((playfield_surface.get_width(), 
            UNDER_HUD_HEIGHT))
        
        # Draw game progress    
        pb_width = get_asset("GameProgressBar").get_width()
        under_hud_surface.blit(get_asset("GameProgressBar"), \
            (under_hud_surface.get_width() // 2 - pb_width // 2, 
            PROGRESS_OFFSET))
        
        # Ugly, unmaintainable, hacky but rushed and working    
        tick_width = get_asset("GameProgressTick").get_width()
        under_hud_surface.blit(get_asset("GameProgressTick"),
            (int(under_hud_surface.get_width() // 2 - pb_width // 2) -\
                (int(tick_width) // 2) + \
                int((pb_width + tick_width) * \
                (self.player_character.location[0] +\
                    self.game_map.total_offset) / GAME_DISTANCE)
                , PROGRESS_OFFSET))
                                       
        scaled_surface = pygame.transform.scale(under_hud_surface, 
            (round(scale_amount * under_hud_surface.get_width()),
             round(scale_amount * under_hud_surface.get_height())))                       
        surface.blit(scaled_surface,(0, map_height + ACTIVE_HEIGHT *\
            TILE_HEIGHT * scale_amount))
        
        if self.show_story_active:
            story_surface = pygame.Surface((get_asset("StoryBox").get_width(), \
                get_asset("StoryBox").get_height()))
            story_surface.blit(get_asset("StoryBox"), (0, 0))
            line_font = get_asset("StoryFont")
            for line_number, line in enumerate(self.story):
                line_text = line_font.render(line[:-1], False, (255, 255, 255))
                line_position = (5, 3 + (line_text.get_height() + 3) * line_number)
                story_surface.blit(line_text, line_position)
            scaled_surface = pygame.transform.scale(story_surface, 
                (round(scale_amount * story_surface.get_width()),
                    round(scale_amount * story_surface.get_height())))   
            surface.blit(scaled_surface,(surface.get_width() // 2 - scaled_surface.get_width() // 2,
                surface.get_height() // 2 - scaled_surface.get_height() // 2))
        
        
    def take_input(self, event):
        """Accept and process any input
        Keyword arguments:
            event - the event to process
        Returns:
            none
        """
        if self.state != None:
           self.state.take_input(event)  
           return
        
        if not(self.show_story_active):
            if event.type == KEYDOWN:
                if event.key == K_UP or event.key == K_KP8 or event.key == K_q:
                     self.player_character.do(Action.n)
                     self.next_turn = True
                if event.key == K_KP9 or event.key == K_e:
                    self.player_character.do(Action.ne)
                    self.next_turn = True
                if event.key == K_RIGHT or event.key ==  K_KP6 or event.key == K_d:
                    self.player_character.do(Action.e)
                    self.next_turn = True
                if event.key == K_KP3 or event.key == K_c:
                    self.player_character.do(Action.se)
                    self.next_turn = True
                if event.key == K_DOWN or event.key ==  K_KP2 or event.key == K_x:
                    self.player_character.do(Action.s)
                    self.next_turn = True
                if event.key == K_KP1:
                    self.player_character.do(Action.sw)
                    self.next_turn = True                
                if event.key == K_LEFT or event.key ==  K_KP4 or event.key == K_a:
                    self.player_character.do(Action.w)
                    self.next_turn = True
                if event.key == K_KP7 or event.key == K_q:
                    self.player_character.do(Action.nw)
                    self.next_turn = True
                if event.key == K_KP5 or event.key == K_s:
                    self.player_character.do(Action.wait)
                    self.next_turn = True                
                if event.key == K_SPACE or event.key == K_KP0:
                    self.player_character.do(Action.shoot)
                    self.next_turn = True
                if event.key == K_RETURN or event.key == K_KP_ENTER:
                    self.player_character.do(Action.teleport)
                    self.next_turn = True
                if event.key == K_ESCAPE:                 
                    self.to_exit = True    
        
        if (self.show_story_active):
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                self.show_story_active = False
   
   
    def update(self):
        """Process the next frame
        Keyword arguments:
            none
        Returns:
            True if still running, False if finished
        """

        if self.state != None:
            if self.state.update():
                return not(self.to_exit)
            else:
                self.state = None;
                        
        if self.next_turn:
            self.process_turn()
            self.next_turn = None
        
        self.to_exit = \
            (self.game_done) and not(self.show_story_active)
        
        if self.show_story_active:        
            return True            
        else:            
            return not(self.game_done)
        
    
    def process_turn(self):
        """Process the turn
        Keyword arguments:
            none
        Returns:
            none
        """
        
        # Update/Move Characters
        for i in self.game_map.characters:
            i.update()
            
        # Kill any character engulfed by the black
        for i in self.game_map.characters:
            if i.location[0] == 0:
                i.attacked(i.health, None)
    
        # Delete dead characters
        self.game_map.characters = \
            [i for i in self.game_map.characters if i.alive()] 
    
        # Scroll map
        self.game_map.scroll()
    
        # Change the BLACK tiles
        self.black_tiles = \
            [random.choice(self.black_assets) for iy in range(TILE_HEIGHT)]
                
        # Update brightness 
        # Brightness is multiplied by that tile
        self.tile_brightness = [[0 for y in range(ACTIVE_HEIGHT)] \
            for x in range(ACTIVE_WIDTH)]
        for ix in range(ACTIVE_WIDTH):
            for iy in range(ACTIVE_HEIGHT):
                dx = abs(ix - self.player_character.location[0])
                dy = abs(iy - self.player_character.location[1])
                 
                brightness = 60 + random.randint(0, 5)*3 + 15 * max(0, 8 - dx - dy)   
                if dx + dy < 4:
                    brightness = (200 + brightness) // 2;
                self.tile_brightness[ix][iy] = brightness
        
        if self.player_character.game_end_state == GameEndState.dead:
            self.state = self.show_story(get_asset("DeadStory"))
            self.game_done = True
        if ((self.player_character.game_end_state == GameEndState.consumed) or
            (self.player_character.location[0] <= 0)):
            self.state = self.show_story(get_asset("ConsumedStory"))
            self.game_done = True            
        if self.player_character.game_end_state == GameEndState.won_killed:
            self.state = self.show_story(get_asset("WonKilledStory"))
            self.game_done = True          
        if ((self.player_character.game_end_state == GameEndState.won_escaped)\
            or (self.player_character.location[0] +\
            self.game_map.total_offset) >= \
                get_asset("Config")["GAME_DISTANCE"]):
            self.state = self.show_story(get_asset("WonEscapedStory"))
            self.game_done = True          
            
    
    def show_story(self, story):
        self.show_story_active = True
        self.story = story
