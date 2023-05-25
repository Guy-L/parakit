from game_entities import GameState
from abc import ABC, abstractmethod

#Base class (abstract)
class Analysis(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def step(self, state):
        pass

    @abstractmethod
    def done(self):
        pass

#Feel free to duplicate and implement to make your own! (make sure to rename them)
class AnalysisTemplate(Analysis):
    #Called right before extraction starts
    def __init__(self):
        #Your initialization code here
        pass

    #Called for each extracted frame 
    def step(self, state):
        #Your analysis code here
        pass

    #Called after extraction finishes
    def done(self):
        print("(Template) Analysis results go here.")
        #Your printing code here
   
   
   
   
#useful stuff, see analysis_examples.py for usages
#(note: if your analysis is above these lines, you can't use 'em)
from settings import pyplot_settings
from interface import save_screenshot, get_color, color16, np
import matplotlib.pyplot as plt
import math

#cursed pyplot stuff, idem
def pyplot_color(color_str):
    if color_str == 'White':
        return 'lightgrey'
    elif color_str == 'Dark Yellow':
        return 'olive'
    elif color_str == 'Bronze':
        return 'sienna'
    elif color_str == 'N/A':
        return 'black'
    else:
        return color_str.replace(" ", "")
        
def item_color(item_type):
    if item_type == 'Power' or item_type == 'Full Power':
        return 'red'
    elif item_type == 'Point':
        return 'blue'
    elif item_type == 'Life Piece':
        return 'fuchsia'
    elif item_type == 'Bomb Piece':
        return 'lime'
    elif item_type == 'Green':
        return 'green'
    elif item_type == 'Cancel':
        return 'olive'
    else:
        return 'black'
        
plot_scale, pyplot_factor, bullet_factor, enemy_factor, plot_laser_circles = pyplot_settings.values()
