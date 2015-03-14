""" Common procedures to access files
    Also contains the list of asset file names 
    """
import os
import pygame
import enum
import sys
import json

from enum import Enum


def find_data_file(filename):
    """ Return the correct location of a file regardless of OS and whether
        frozen or not.
        Named Arguments:
            filename - filename to get
        Returns:
            String containing correct path
    """
    
    # if getattr(sys, 'frozen', False):
        # # The application is frozen
        # datadir = os.path.dirname(sys.executable + "\\assets\\")
    # else:
        # The application is not frozen
        # I'm unsure if this is the best approach
    
    datadir = os.path.dirname(os.path.dirname(__file__) + "\\..\\assets\\")
    
    return os.path.join(datadir, filename)


class AssetType(Enum):
    image = 1           # A PyGame image
    font = 2            # A PyGame font
    text_slab = 3       # Text as a single string
    text_lines = 4      # Text as a list of lines
    json = 5            # A JSON file, stored as a dict


def get_asset(asset):
    """ Return the requested asset from memory or disk 
        Named Arguments:
            asset - asset to get
        Returns:
            Object in format for that asset
    """
    if not(asset in assets_in_memory):
        # If asset no loaded, get its type and use the correct loader
        required_type = asset_file_names[asset][1]
        if (required_type == AssetType.image):
            assets_in_memory[asset] = \
                pygame.image.load(find_data_file(asset_file_names[asset][0]))
        elif (required_type == AssetType.font):
            assets_in_memory[asset] = \
                pygame.font.Font(find_data_file(asset_file_names[asset][0]),
                    asset_file_names[asset][2])
        elif (required_type == AssetType.text_slab):
            f = open(find_data_file(asset_file_names[asset][0]), "r")            
            assets_in_memory[asset] = f.read()
            f.close
        elif (required_type == AssetType.text_lines):
            f = open(find_data_file(asset_file_names[asset][0]), "r")
            assets_in_memory[asset] = f.readlines()                
        elif (required_type == AssetType.json):
            f = open(find_data_file(asset_file_names[asset][0]), "r")        
            assets_in_memory[asset] = json.load(f)
    
    # Return asset
    return assets_in_memory[asset]
                
    
assets_in_memory = {};

# This is the list of all the assets. They're in a dict with the key being
# a string of the assets name, and the value being:
#   ( file_name, file_type, additional_data).
# File Name is a filename with extension, without path
# File Type is an AssetType (Enum - declared above)
# Additional info contains type specific information. Namely:
#    AssetType.Font - Contains Font Size

asset_file_names = \
    {
    "Config" : ("config.json", AssetType.json),
    "TitleFont" : ("leaguespartan-bold.ttf", AssetType.font, 240),
    "MenuFont" : ("volter.ttf", AssetType.font, 24),
    "StoryFont" : ("volter.ttf", AssetType.font, 9),
    "AboutText" : ("about", AssetType.text_lines),
    "StoryBox" : ("story_box.png", AssetType.image),
    "Version" : ("version", AssetType.text_slab),
    "Grass1" : ("grass1.png", AssetType.image),
    "Grass2" : ("grass2.png", AssetType.image),
    "Grass3" : ("grass3.png", AssetType.image),
    "Grass4" : ("grass4.png", AssetType.image),
    "Grass5" : ("grass5.png", AssetType.image),
    "Grass6" : ("grass6.png", AssetType.image),
    "Tree1" : ("tree1.png", AssetType.image),
    "Tree2" : ("tree2.png", AssetType.image),
    "Tree3" : ("tree3.png", AssetType.image),
    "Tree4" : ("tree4.png", AssetType.image),
    "Tree5" : ("tree5.png", AssetType.image),
    "Tree6" : ("tree6.png", AssetType.image),
    "Black1" : ("black1.png", AssetType.image),
    "Black2" : ("black2.png", AssetType.image),
    "Black3" : ("black3.png", AssetType.image),
    "Black4" : ("black4.png", AssetType.image),
    "Hero" : ("hero.png", AssetType.image),
    "Heart1" : ("heart1.png", AssetType.image),
    "Heart2" : ("heart2.png", AssetType.image),
    "Heart3" : ("heart3.png", AssetType.image),
    "Heart4" : ("heart4.png", AssetType.image),
    "Heart5" : ("heart5.png", AssetType.image),
    "Heart6" : ("heart6.png", AssetType.image),
    "Heart7" : ("heart7.png", AssetType.image),
    "Heart8" : ("heart8.png", AssetType.image),
    "Heart9" : ("heart9.png", AssetType.image),
    "Eviltree1" : ("eviltree1.png", AssetType.image),
    "Eviltree2" : ("eviltree2.png", AssetType.image),
    "Eviltree3" : ("eviltree3.png", AssetType.image),
    "Eviltree4" : ("eviltree4.png", AssetType.image),
    "Eviltree5" : ("eviltree5.png", AssetType.image),
    "Eviltree6" : ("eviltree6.png", AssetType.image),
    "Cultist" : ("cultist.png", AssetType.image),
    "Flame" : ("flame.png", AssetType.image),
    "Spectre" : ("spectre.png", AssetType.image),
    "Boss" : ("boss.png", AssetType.image),
    "BulletFull" : ("bullet_full.png", AssetType.image),
    "BulletSpent" : ("bullet_spent.png", AssetType.image),
    "TeleportFull" : ("teleport_full.png", AssetType.image),
    "TeleportSpent" : ("teleport_spent.png", AssetType.image),
    "Attack" : ("attack.png", AssetType.image),
    "HealthPip" : ("health_pip.png", AssetType.image),
    "ControlsScreen" : ("controls.png", AssetType.image),
    "ControlsScreen2" : ("controls2.png", AssetType.image),
    "XPBarFull" : ("xp_full.png", AssetType.image),
    "XPBarEmpty" : ("xp_empty.png", AssetType.image),    
    "GameProgressBar" : ("game_progress_bar.png", AssetType.image),
    "GameProgressTick" : ("game_progress_tick.png", AssetType.image), 
    "StartStory": ("start_story", AssetType.text_lines),
    "DeadStory": ("dead_story", AssetType.text_lines),
    "ConsumedStory": ("consumed_story", AssetType.text_lines),
    "WonKilledStory": ("won_killed_story", AssetType.text_lines),
    "WonEscapedStory": ("won_escaped_story", AssetType.text_lines),
    "HealthPack" : ("health_pack.png", AssetType.image),
    "Car1" : ("car1.png", AssetType.image),
    "Car2" : ("car2.png", AssetType.image),
    "dummy" : None
    }
