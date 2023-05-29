from settings import interface_settings as _settings
import pygetwindow as gw
import pyautogui
import psutil
import ctypes
import win32process
import win32api
import win32con
import numpy as np
import cv2
import keyboard 
import struct
import random  

# Step 0 - Get the target module name and other settings
_game_main_modules = {
    ('14', 'th14', 'th14.exe', 'ddc', 'double dealing character'): 'th14.exe',
    #('15', 'th15', 'th15.exe', 'lolk', 'legacy of lunatic kingdom'): 'th15.exe',
    #('18', 'th18', 'th18.exe', 'um', 'unconnected marketeers'): 'th18.exe',
}

_game = _settings['game']
_termination_key = _settings['termination_key']

_module_name = ''
for keys, module_name in _game_main_modules.items():
    if str(_game).lower().strip() in keys:
        _module_name = module_name
        print(f"Interface: Target module '{_module_name}'.")
        break
            
if not _module_name:
    print(f"Interface error: Unknown game specifier '{_game}'.")
    exit()
    

# ==================================================
# GAME SPECIFIC STUFF -- TO BE REFACTORED ==========
# Statics
score         = 0xf5830
graze         = 0xf5840
piv           = 0xf584c
power         = 0xf5858
lives         = 0xf5864
life_pieces   = 0xf5868
bombs         = 0xf5870
bomb_pieces   = 0xf5874
bonus_count   = 0xf5894
time_in_stage = 0xf58b0
input         = 0xd6a90
rng           = 0xdb510
game_state    = 0xf7ac8

# Untracked Statics
game_speed      = 0xd8f58
visual_rng      = 0xdb508
replay_filename = 0xdb560
character       = 0xf5828
subshot         = 0xf582c
difficulty      = 0xf5834
rank            = 0xf583c 
stage           = 0xf58a4 

# Player
player_pointer  = 0xdb67c 
zPlayer_pos     = 0x5e0
zPlayer_hurtbox = 0x630
zPlayer_iframes = 0x182c4
zPlayer_focused = 0x184b0

# Bullets
bullet_manager_pointer = 0xdb530
zBulletManager_list    = 0x7c
zBullet_iframes        = 0x24
zBullet_pos            = 0xbc0
zBullet_velocity       = 0xbcc
zBullet_speed          = 0xbd8
zBullet_angle          = 0xbdc
zBullet_hitbox_radius  = 0xbe0
zBullet_ex_delay_timer = 0x12ec #only DDC/ISC/HBM
zBullet_scale          = 0x13bc
zBullet_type           = 0x13ec
zBullet_color          = 0x13ee

# Enemies
enemy_manager_pointer = 0xdb544
zEnemyManager_list    = 0xd0
zEnemy_data           = 0x11f0
zEnemy_pos            = zEnemy_data + 0x44
zEnemy_hurtbox        = zEnemy_data + 0x110
zEnemy_hitbox         = zEnemy_data + 0x118
zEnemy_rotation       = zEnemy_data + 0x120
zEnemy_time           = zEnemy_data + 0x2bc + 0x4
zEnemy_score_reward   = zEnemy_data + 0x3f70
zEnemy_hp             = zEnemy_data + 0x3f74
zEnemy_hp_max         = zEnemy_data + 0x3f78
zEnemy_iframes        = zEnemy_data + 0x3ff0
zEnemy_flags          = zEnemy_data + 0x4054 #"flags_low" contains the useful stuff
zEnemy_subboss_id     = zEnemy_data + 0x4064

zEnemyFlags_is_boss    = 0x800000
#zEnemyFlags_timeout    = 0x10000 not needed
zEnemyFlags_intangible = 0x20
zEnemyFlags_no_hitbox  = 0x2 

# Items
item_manager_pointer   = 0xdb660
zItemManager_array     = 0x14
zItemManager_array_len = 0xddd854
zItem_len              = 0xc18
zItem_state            = 0xbf0 
zItem_type             = 0xbf4
zItem_pos              = 0xbac
zItem_vel              = 0xbb8

# Laser (Base)
laser_manager_pointer   = 0xdb664
zLaserManager_list      = 0x5d0
zLaserBaseClass_next    = 0x4
zLaserBaseClass_state   = 0x10    
zLaserBaseClass_type    = 0x14     
zLaserBaseClass_timer   = 0x1c
zLaserBaseClass_offset  = 0x54
zLaserBaseClass_angle   = 0x6c
zLaserBaseClass_length  = 0x70
zLaserBaseClass_width   = 0x74
zLaserBaseClass_speed   = 0x78
zLaserBaseClass_id      = 0x80     
zLaserBaseClass_iframes = 0x5b4     
zLaserBaseClass_sprite  = 0x5b8  
zLaserBaseClass_color   = 0x5bc

# Laser (Line)
zLaserLine_start_pos    = 0x5c0 
zLaserLine_mgr_angle    = 0x5cc    
zLaserLine_max_length   = 0x5d0 
#zLaserLine_mgr_width    = 0x5dc  storing manager value is redundant  
zLaserLine_mgr_speed    = 0x5e0   
#zLaserLine_mgr_sprite   = 0x5e4  storing manager value is redundant
#zLaserLine_mgr_color    = 0x5e8  storing manager value is redundant
zLaserLine_distance     = 0x5ec

# Laser (Infinite)
zLaserInfinite_start_pos    = 0x5c0
zLaserInfinite_velocity     = 0x5cc
zLaserInfinite_mgr_angle    = 0x5d8
zLaserInfinite_angle_vel    = 0x5dc
zLaserInfinite_final_len    = 0x5e0
zLaserInfinite_mgr_len      = 0x5e4
zLaserInfinite_final_width  = 0x5e8
zLaserInfinite_mgr_speed    = 0x5ec
zLaserInfinite_start_time   = 0x5f0
zLaserInfinite_expand_time  = 0x5f4
zLaserInfinite_active_time  = 0x5f8
zLaserInfinite_shrink_time  = 0x5fc
zLaserInfinite_mgr_distance = 0x60c
#zLaserInfinite_mgr_sprite   = 0x610  storing manager value is redundant
#zLaserInfinite_mgr_color    = 0x614  storing manager value is redundant

# Laser (Curve)
#zLaserCurve_start_pos  = 0x5c0  storing value is redundant          
#zLaserCurve_angle      = 0x5cc  storing manager value is redundant
#zLaserCurve_width      = 0x5d0  storing manager value is redundant
#zLaserCurve_speed      = 0x5d4  storing manager value is redundant
#zLaserCurve_sprite     = 0x5d8  storing manager value is redundant
#zLaserCurve_color      = 0x5dc  storing manager value is redundant
zLaserCurve_max_length = 0x5e0
zLaserCurve_distance   = 0x5e4
zLaserCurve_array      = 0x14ac

# Curve Node
zLaserCurveNode_pos   = 0x0 
zLaserCurveNode_vel   = 0xc 
zLaserCurveNode_angle = 0x18
zLaserCurveNode_speed = 0x1c
zLaserCurveNode_size  = 0x20

# Ascii
ascii_manager_pointer = 0xdb520
global_timer          = 0x191e0 #frames the ascii manager has been alive = global frame counter (it never dies)

# Spell Card
spellcard_pointer     = 0xdb534
zSpellcard_indicator  = 0x20 #note: since I don't know what this var is, this is a hack (any better indicator?)
zSpellcard_id         = 0x78
zSpellcard_bonus      = 0x80

# GUI
gui_pointer       = 0xdb550
zGui_bosstimer_s  = 0x19c
zGui_bosstimer_ms = 0x1a0

# Supervisor
supervisor_addr = 0xd8f60
game_mode       = supervisor_addr + 0x6e8 #4 = anywhere in main menu, 7 = anywhere the game world is on screen, 15 = credits/endings
rng_seed        = supervisor_addr + 0x728 #based on time when game was launched; never changes

# DDC-specific
seija_anm_pointer = supervisor_addr + 0x1c8
seija_flip_x      = 0x60 #goes from 1 to -1 smoothly during Spell 1 & instantly during Spell 4
seija_flip_y      = 0x64 #goes from 1 to -1 smoothly during Spell 2 & instantly during Spell 4
zPlayer_scale     = 0x18308

# Meaning Arrays
color_coin = ['Gold', 'Silver', 'Bronze']       #color type '3'
color4 = ['Red', 'Blue', 'Green', 'Yellow']     
color8 = ['Black', 'Red', 'Pink', 'Blue', 'Cyan', 'Green', 'Yellow', 'White'] 
color16 = ['Black', 'Dark Red', 'Red', 'Purple', 'Pink', 'Dark Blue', 'Blue', 'Dark Cyan', 'Cyan', 'Dark Green', 'Green', 'Lime', 'Dark Yellow', 'Yellow', 'Orange', 'White'] 

sprites = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Star', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Blue Fireball', 0), ('Yellow Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Spinning Star', 16), ('Laser', 16), ('Red Note', 0), ('Blue Note', 0), ('Green Note', 0), ('Purple Note', 0), ('Rest', 8)]
curve_sprites = ['Standard', 'Thunder']

item_types = {1: "Power", 2: "Point", 3:"Full Power", 4:"Life Piece", 6:"Bomb Piece", 9:"Green", 10:"Cancel"}
game_states = ["Pause (/Stage Transition/Ending Sequence)", "Not in Run (Main Menu/Game Over/Practice End)", "Actively Playing"]
game_modes = {4: 'Main Menu', 7: 'Game World on Screen', 15: 'Ending Sequence'}

characters = ['Reimu', 'Marisa', 'Sakuya']
subshots = ['A', 'B']
difficulties = ['Easy', 'Normal', 'Hard', 'Lunatic', 'Extra']

# GAME SPECIFIC STUFF -- TO BE REFACTORED ==========
# ==================================================

# Step 1 - Get the game process
game_process = None

for process in psutil.process_iter(['pid', 'name']):
    if process.info['name'] and process.info['name'].lower() == _module_name:
        game_process = process
        break

if game_process:
    print(f'Found the {_module_name} game process with PID: {game_process.pid}')
else:
    print('Interface error: Game process not found')
    exit()

# Step 2 - Get the process's base address
_base_address = None
_module_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, game_process.pid)
_module_list = win32process.EnumProcessModules(_module_handle)

for module in _module_list:
    module_info = win32process.GetModuleFileNameEx(_module_handle, module)

    if _module_name in module_info.lower():
        _base_address = module
        break

if _base_address is not None:
    print(f'Base address of the process main module: {hex(_base_address)}')
else:
    print('Interface error: Module base address not found')
    exit()

# Step 3 - Open a process handle
_PROCESS_VM_READ = 0x0010
_PROCESS_QUERY_INFORMATION = 0x0400
_process_handle = ctypes.windll.kernel32.OpenProcess(_PROCESS_VM_READ | _PROCESS_QUERY_INFORMATION, False, game_process.pid)

# Step 4 - Get the game window
_game_window = None

for window in gw.getAllWindows():
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(window._hWnd, ctypes.byref(pid))
    
    if pid.value == game_process.pid:
        _game_window = window
        break

if _game_window:
    print(f'Found the game window: {_game_window}')
else:
    print('Interface error: Game window not found')
    exit()


# Interface Method Definitions

def get_rgb_screenshot(): #Note: fails if the window is inactive!    
    # Take a screenshot of the game window with a predetermined crop (note that there's 3 extra pixels on every side of the screenshot by default)
    screenshot = pyautogui.screenshot(region=(_game_window.left+35, _game_window.top+42, _game_window.width-44, _game_window.height-47))

    # Convert the PIL image to a NumPy array
    return np.array(screenshot)

def get_greyscale_screenshot(): #Note: fails if the window is inactive!    
    # Take a screenshot of the game window with a predetermined crop (note that there's 3 extra pixels on every side of the screenshot by default)
    screenshot = pyautogui.screenshot(region=(_game_window.left+35, _game_window.top+42, _game_window.width-44, _game_window.height-47))

    # Convert the PIL image to a NumPy array
    rgb_screenshot = np.array(screenshot)

    # Convert the RGB image to a greyscale image
    grey_screenshot = cv2.cvtColor(rgb_screenshot, cv2.COLOR_BGR2GRAY) # can be saved with imwrite
    
    # Add a channel dimension to the greyscale image    
    return np.expand_dims(grey_screenshot, axis=-1)
   
def save_screenshot(filename, screenshot): 
    # Swap the R and B channels to match OpenCV's BGR format (no effect for greyscale pics)
    bgr_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr_screenshot)

def read_int(offset, bytes = 4, rel = False):
    #return np.uint32(int.from_bytes(_read_memory(offset, 4, rel), byteorder='little'))
    return int.from_bytes(_read_memory(offset, bytes, rel), byteorder='little')

def read_float(offset, rel = False):
    return struct.unpack('f', _read_memory(offset, 4, rel))[0]
    
def read_string(offset, length, rel = False):
    return _read_memory(offset, length, rel).decode('utf-8').rstrip('\x00')
        
def read_zList(offset):
    return {"entry": read_int(offset), "next": read_int(offset + 0x4)}
        
def get_item_type(item_type):
    if item_type in item_types.keys() :
        return item_types[item_type]
    else:
        #return "Unknown " + str(item_type) #(no need to display this, all item types should be known)
        return None
        
def get_color(sprite, color):
    if sprites[sprite][1] == 0:
        return "N/A"
        
    elif sprites[sprite][1] == 3:
        return color_coin[color]
        
    elif sprites[sprite][1] == 4:
        return color4[color]
        
    elif sprites[sprite][1] == 8:
        return color8[color]
        
    elif sprites[sprite][1] == 16:
        return color16[color]

# Ordered set of available keys
_keys = ['shift', 'z', 'left', 'right', 'up', 'down', 'x']

def apply_action_int(action_int):
    # Iterate through the list of keys and hold/release keys depending on the bit value
    for index, key in enumerate(reversed(_keys)):
        # Check if the bit at the current position is set (1) or not (0)
        bit_set = (action_int >> index) & 1
        
        if bit_set:
            keyboard.press(key)
        else:
            keyboard.release(key)
            
def apply_action_bin(action_binstr):
    # Iterate through the list of keys and hold/release keys depending on the bit value
    for index, key in enumerate(_keys):
        # Check if the bit at the current position is set (1) or not (0)
        bit_set = (action_binstr[index] == '1')
        
        if bit_set:
            keyboard.press(key)
        else:
            keyboard.release(key)
            
def apply_action_str(action_text):
    key_presses = action_text.split()
    for key in _keys:
        if key in key_presses:
            keyboard.press(key)
        else:
            keyboard.release(key)
           
def wait_global_frame(cur_global_frame=None, count=0):
    if not cur_global_frame:
        cur_global_frame = read_int(global_timer)
        
    while read_int(global_timer) <= cur_global_frame + count:
        pass
    
def wait_game_frame(cur_game_frame=None, need_active=False):
    if not cur_game_frame:
        cur_game_frame = read_int(time_in_stage, rel=True)

    while read_int(time_in_stage, rel=True) == cur_game_frame: 
        if read_int(game_state, rel=True) == 1:
            return "Non-run game state detected"
        elif not game_process.is_running():
            return "Game was closed"  #bugged, but not worth fixing (edge case)
        elif keyboard.is_pressed(_termination_key):
            return "User pressed termination key"
        elif need_active and _game_window != gw.getActiveWindow():
            return "Game no longer active (need_active set to True)"
    return None

def press_key(key):
    keyboard.press(key)
    wait_global_frame()
    keyboard.release(key)
    wait_global_frame()
    
def restart_run():  
    apply_action_int(0) #ensure no residual input
    press_key('enter')
    press_key('esc')
    press_key('up')
    press_key('up')
    press_key('z')
    
def pause_game():
    if get_focus() and read_int(game_state, rel=True) == 2:
        press_key('esc')
        
        while read_int(game_state, rel=True) != 0:
            pass
        
        #seems to be a hardcoded 8-frame delay between 
        #when pause starts and when pause menu can take inputs
        wait_global_frame(count=8)
        
def unpause_game():
    if get_focus() and read_int(game_state, rel=True) == 0:
        press_key('esc')
        
        while read_int(game_state, rel=True) != 2:
            pass

def get_focus():
    if not game_process.is_running():
        return False

    if _game_window != gw.getActiveWindow():
        _game_window.activate()
        while _game_window != gw.getActiveWindow():
            pass
    return True
    
def enact_game_actions_bin(actions): #space-separated action binary strings
    get_focus()
    action_array = actions.split()
    for action in action_array:
        apply_action_bin(action)
        wait_game_frame(need_active=True)
    apply_action_int(0)

def enact_game_actions_text(actions): #line-separated sets of space-seperates key press names
    get_focus()
    action_array = actions.split('\n')
    for action in action_array:
        apply_action_str(action)
        wait_game_frame(need_active=True)
    apply_action_int(0)


# Private Method Definitions

_buffers = {} #caching helps!
_kernel32 = ctypes.windll.kernel32 # minor optimization
_byref = ctypes.byref(ctypes.c_ulonglong()) # minor optimization
def _read_memory(address, size, rel):
    if size not in _buffers:
        _buffers[size] = ctypes.create_string_buffer(size)
    buffer = _buffers[size]
    _kernel32.ReadProcessMemory(_process_handle, address if not rel else _base_address + address, buffer, size, _byref)
    return buffer.raw


# Debug Method Definitions

def _random_player():
    get_focus()

    np.set_printoptions(linewidth=np.inf)
    print(np.array(["Lives", "L.Pieces", "Bombs", "B.Pieces", "Bonus", "Power", "PIV", "Graze", "Game State", "Action", "Time in Stage"]))
    
    while True:            
        cur_frame = read_int(time_in_stage, rel=True)
        if wait_game_frame(cur_frame, True):
            apply_action_int(0) #un-press everything
            return
        
        #display game variables and take random actions
        action = random.randint(0, 2**len(_keys))
        print(list(np.array([
                    read_int(lives, rel=True), read_int(life_pieces, rel=True),
                    read_int(bombs, rel=True), read_int(bomb_pieces, rel=True),
                    read_int(bonus_count, rel=True), 
                    read_int(power, rel=True), 
                    read_int(piv, rel=True), 
                    read_int(graze, rel=True),
                    read_int(game_state, rel=True),
                    '{:08b}'.format(action),
                    cur_frame+1])))
        apply_action_int(action)

# Step 5 - Read the address of the ascii manager here so timing methods work
global_timer += read_int(ascii_manager_pointer, rel=True)