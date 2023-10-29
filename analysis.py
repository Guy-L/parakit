from game_entities import GameState
from abc import ABC, abstractmethod
from interface import game_id

#Base class (abstract), shouldn't be touched
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

#Feel free to duplicate and implement to make your own! (make sure to rename the class)
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
#(note: put your custom analysis under these lines so you can use 'em)
from settings import pyplot_settings
from interface import save_screenshot, terminate, get_color, get_curve_color
from interface import enemy_anms, world_width, world_height, color16, np
from scipy.ndimage import uniform_filter
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse, Circle, Rectangle
import math

#cursed pyplot stuff, idem
def pyplot_color(color_str):
    if color_str == 'White':
        return 'lightgrey'
    elif color_str == 'Dark Yellow':
        return 'olive'
    elif color_str == 'Bronze':
        return 'sienna'
    else:
        return color_str.replace(" ", "")

def enemy_color(anm_page, anm_id):
    if anm_page != 2 or anm_id not in enemy_anms:
        return 'C0'

    type_str = enemy_anms[anm_id]

    if mcolors.is_color_like(type_str.split(' ')[0]):
        return type_str.split(' ')[0]
    elif 'Sunflower Fairy' in type_str:
        return 'gold'
    elif 'Wolf Spirit' in type_str:
        return 'red'
    elif 'Otter Spirit' in type_str:
        return 'green'
    elif 'Eagle Spirit' in type_str:
        return 'blue'
    else:
        return 'C0'

def item_color(item_type):
    if item_type == 'Power' or item_type == 'Full Power' or item_type == 'Power Card':
        return 'red'
    elif item_type == 'Point':
        return 'blue'
    elif item_type == 'Life Piece' or item_type == 'LifeP. Card':
        return 'fuchsia'
    elif item_type == 'Bomb Piece' or item_type == 'BombP. Card':
        return 'lime'
    elif item_type == 'Green':
        return 'green'
    elif item_type == 'Cancel':
        return 'olive'
    elif item_type == 'Gold' or item_type == 'Gold Card':
        return 'gold'
    elif item_type == 'Spirit Power':
        return (0.3, 0.3, 0.45, 0.5)
    else:
        return 'black'

plot_scale, pyplot_factor, bullet_factor, enemy_factor, plot_laser_circles = pyplot_settings.values()
DONT_PLOT = -1
HIDE_P2 = -2