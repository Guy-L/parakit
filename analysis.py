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
from interface import save_screenshot, terminate, get_color, get_curve_color, get_item_type
from interface import enemy_anms, world_width, world_height, color16, np
from interface import zItemState_autocollect, zItemState_attracted
from scipy.ndimage import uniform_filter
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Ellipse, Circle, Rectangle
import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore
from PyQt5.QtWidgets import QApplication
import os
os.environ['QT_LOGGING_RULES'] = '*=false;*.critical=true;*.fatal=true'
import traceback

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
    elif 'Hellflower Fairy' in type_str:
        return 'darkred'
    elif 'Wolf Spirit' in type_str:
        return 'red'
    elif 'Otter Spirit' in type_str:
        return 'green'
    elif 'Eagle Spirit' in type_str:
        return 'blue'
    else:
        return 'C0'

def item_color(item_type):
    if 'Full Power' in item_type:
        return 'yellow'
    elif 'Spirit Power' in item_type:
        return (0.3, 0.3, 0.45, 0.5)
    elif 'Power' in item_type:
        return 'red'
    elif 'Point' in item_type:
        return 'blue'
    elif 'Life' in item_type:
        return 'fuchsia'
    elif 'Bomb' in item_type:
        return 'lime'
    elif 'Green' in item_type or 'Graze' in item_type:
        return 'green'
    elif 'Cancel' in item_type:
        return 'olive'
    elif 'Gold' in item_type:
        return 'gold'
    else:
        return 'black'

def item_size(item_type):
    if item_type == 'Full Power':
        return 150

    for word in ['Life', 'Bomb', 'Big', 'Card']:
        if word in item_type:
            return 100

    for type in ['Green', 'Graze', 'Spirit Power']:
        if item_type == type:
            return 10

    if item_type == 'Cancel':
        return 25

    return 50

plot_scale, pyplot_factor, bullet_factor, enemy_factor, plot_laser_circles, plot_enemy_hurtbox = pyplot_settings.values()
DONT_PLOT = -1
HIDE_P2 = -2