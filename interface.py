from options import game, thcrap_enabled, termination_key
import pygetwindow as gw
import pyautogui
import psutil
import ctypes
import win32process
import win32api
import win32con
import numpy as np
import cv2
import random   #debug
import keyboard 
import struct

# Set these to select the game before training
_game_title = '“Œ•û‹Pjé@` Double Dealing Character. ver 1.00b'
_module_name = 'th14.exe'

# Offsets
score         = 0xf5830
lives         = 0xf5864
life_pieces   = 0xf5868
bombs         = 0xf5870
bomb_pieces   = 0xf5874
bonus_count   = 0xf5894
power         = 0xf5858
piv           = 0xf584c
graze         = 0xf5840
time_in_stage = 0xf58b0

player_pointer  = 0xdb67c 
zPlayer_pos     = 0x5e0
zPlayer_hurtbox = 0x630
zPlayer_iframes = 0x182c4
zPlayer_focused = 0x184b0

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

enemy_manager_pointer = 0xdb544
zEnemyManager_list    = 0xd0
zEnemy_data           = 0x11f0
zEnemy_pos            = zEnemy_data + 0x44
zEnemy_hurtbox        = zEnemy_data + 0x110
zEnemy_hitbox         = zEnemy_data + 0x118
zEnemy_rotation       = zEnemy_data + 0x120
zEnemy_score_reward   = zEnemy_data + 0x3f70
zEnemy_hp             = zEnemy_data + 0x3f74
zEnemy_hp_max         = zEnemy_data + 0x3f78
zEnemy_iframes        = zEnemy_data + 0x3ff0
zEnemy_flags          = 0x5244

item_manager_pointer   = 0xdb660
zItemManager_array     = 0x14
zItemManager_array_len = 0xddd854
zItem_len              = 0xc18
zItem_state            = 0xbf0 
zItem_type             = 0xbf4
zItem_pos              = 0xbac
zItem_vel              = 0xbb8

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

zLaserLine_start_pos    = 0x5c0 
zLaserLine_mgr_angle    = 0x5cc    
zLaserLine_max_length   = 0x5d0 
#zLaserLine_mgr_width    = 0x5dc  storing manager value is redundant  
zLaserLine_mgr_speed    = 0x5e0   
#zLaserLine_mgr_sprite   = 0x5e4  storing manager value is redundant
#zLaserLine_mgr_color    = 0x5e8  storing manager value is redundant
zLaserLine_distance     = 0x5ec

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

#zLaserCurve_start_pos  = 0x5c0  storing value is redundant          
#zLaserCurve_angle      = 0x5cc  storing manager value is redundant
#zLaserCurve_width      = 0x5d0  storing manager value is redundant
#zLaserCurve_speed      = 0x5d4  storing manager value is redundant
#zLaserCurve_sprite     = 0x5d8  storing manager value is redundant
#zLaserCurve_color      = 0x5dc  storing manager value is redundant
zLaserCurve_max_length = 0x5e0
zLaserCurve_distance   = 0x5e4
zLaserCurve_array      = 0x14ac

zLaserCurveNode_pos   = 0x0 
zLaserCurveNode_vel   = 0xc 
zLaserCurveNode_angle = 0x18
zLaserCurveNode_speed = 0x1c
zLaserCurveNode_size  = 0x20

ascii_manager_pointer = 0xdb520
global_timer          = 0x191e0 #frames the ascii manager has been alive = global frame counter (it never dies)

supervisor_addr      = 0xd8f60
zSupervisor_gamemode = 0x6e8 #4 = anywhere in main menu, 7 = anywhere the game world is on screen, 15 = credits/endings
zSupervisor_rng_seed = 0x728

game_state = 0xF7AC8

color_coin = ['Gold', 'Silver', 'Bronze']       #color type '3'
color4 = ['Red', 'Blue', 'Green', 'Yellow']     
color8 = ['Black', 'Red', 'Pink', 'Blue', 'Cyan', 'Green', 'Yellow', 'White'] 
color16 = ['Black', 'Dark Red', 'Red', 'Purple', 'Pink', 'Dark Blue', 'Blue', 'Dark Cyan', 'Cyan', 'Dark Green', 'Green', 'Lime', 'Dark Yellow', 'Yellow', 'Orange', 'White'] 

sprites = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Star', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Blue Fireball', 0), ('Yellow Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Spinning Star', 16), ('Laser', 16), ('Red Note', 0), ('Blue Note', 0), ('Green Note', 0), ('Purple Note', 0), ('Rest', 8)]
curve_sprites = ['Standard', 'Thunder']

item_types = ["Unknown 0", "Power", "Point", "Full Power", "Life Piece", "Unknown 5", "Bomb Piece", "Unknown 7", "Unknown 8", "Green", "Cancel"]
game_states = ["Pause (/Stage Transition/Ending Sequence)", "Not in Run (Main Menu/Game Over/Practice End)", "Actively Playing"]
game_modes = {4: 'Main Menu', 7: 'Game World on Screen', 15: 'Ending Sequence'}

# Ordered set of available keys (public)
keys = ['shift', 'z', 'left', 'right', 'up', 'down', 'x']

# Step 1 - Get the game window
_game_windows = gw.getWindowsWithTitle(_game_title)

if len(_game_windows) == 1:
    print(f'Found the game window: {_game_windows[0]}')
else:
    print('Game window not found (' + _game_title + ')')
    exit()
    
_game_window = _game_windows[0]

# Step 2 - Get the process ID
_hWnd = _game_window._hWnd  # Get the window handle
_pid = ctypes.c_ulong()
ctypes.windll.user32.GetWindowThreadProcessId(_hWnd, ctypes.byref(_pid))  # Get the process ID

_game_pid = _pid.value

if _game_pid is not None:
    print(f'Found the game process with PID: {_game_pid}')
else:
    print('Game process not found')
    exit()
    
#for suspending/resuming
game_process = psutil.Process(_game_pid)

# Step 3 - Get the process's base address
_base_address = None
_module_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, _game_pid)
_module_list = win32process.EnumProcessModules(_module_handle)

for module in _module_list:
    module_info = win32process.GetModuleFileNameEx(_module_handle, module)
    
    if _module_name.lower() in module_info.lower():
        _base_address =  module
        break

if _base_address is not None:
    print(f'Base address of the process main module: {hex(_base_address)}')
else:
    print('Module base address not found')
    exit()
    
# Step 4 - Open a process handle
_PROCESS_VM_READ = 0x0010
_PROCESS_QUERY_INFORMATION = 0x0400
_process_handle = ctypes.windll.kernel32.OpenProcess(_PROCESS_VM_READ | _PROCESS_QUERY_INFORMATION, False, _game_pid)



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
    
def read_byte(offset, rel = False):
    return int.from_bytes(_read_memory(offset, 1, rel), byteorder='big')
    
def read_zList(offset):
    return {"entry": read_int(offset), "next": read_int(offset + 0x4)}
        
def get_item_type(item_type):
    if item_type < len(item_types) :
        return item_types[item_type]
    else:
        return "Unknown " + str(item_type)
        
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
    
def apply_action_int(action_int):
    # Iterate through the list of keys and hold/release keys depending on the bit value
    for index, key in enumerate(reversed(keys)):
        # Check if the bit at the current position is set (1) or not (0)
        bit_set = (action_int >> index) & 1
        
        if bit_set:
            keyboard.press(key)
        else:
            keyboard.release(key)
            
def apply_action_bin(action_binstr):
    # Iterate through the list of keys and hold/release keys depending on the bit value
    for index, key in enumerate(keys):
        # Check if the bit at the current position is set (1) or not (0)
        bit_set = (action_binstr[index] == '1')
        
        if bit_set:
            keyboard.press(key)
        else:
            keyboard.release(key)
            
def apply_action_str(action_text):
    key_presses = action_text.split()
    for key in keys:
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
        elif keyboard.is_pressed(termination_key):
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
        action = random.randint(0, 2**len(keys))
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