from settings import interface_settings as _settings
from offsets import offsets
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
    #('6', 'th6', 'th06', 'th06.exe', 'eosd', 'teosd', 'embodiment of scarlet devil'): 'th06.exe',
    #('7', 'th7', 'th07', 'th07.exe', 'pcb', 'perfect cherry blossom'): 'th07.exe',
    #('8', 'th8', 'th08', 'th08.exe', 'in', 'imperishable night'): 'th08.exe',
    #('9', 'th9', 'th09', 'th09.exe', 'pofv', 'phantasmagoria of flower view'): 'th09.exe',
    #('9.5', 'th9.5', 'th095', 'th095.exe', 'stb', 'shoot the bullet'): 'th095.exe',
    #('10', 'th10', 'th10.exe', 'mof', 'mountain of faith'): 'th10.exe',
    #('11', 'th11', 'th11.exe', 'sa', 'subterranean animism'): 'th11.exe',
    #('12', 'th12', 'th12.exe', 'ufo', 'undefined fantastic object'): 'th12.exe',
    #('12.5', 'th12.5', 'th125', 'th125.exe', 'ds', 'double spoiler'): 'th125.exe',
    #('12.8', 'th12.8', 'th128', 'th128.exe', 'gfw', 'great fairy wars'): 'th128.exe',
    #('13', 'th13', 'th13.exe', 'td', 'ten desires'): 'th13.exe',
    ('14', 'th14', 'th14.exe', 'ddc', 'double dealing character'): 'th14.exe',
    #('14.3', 'th14.3', 'th143', 'th143.exe', 'isc', 'impossible spell card'): 'th143.exe',
    #('15', 'th15', 'th15.exe', 'lolk', 'legacy of lunatic kingdom'): 'th15.exe',
    ('16', 'th16', 'th16.exe', 'hsifs', 'hidden star in four seasons'): 'th16.exe',
    #('16.3', 'th16.3', 'th163', 'th163.exe', 'vd', 'violet detector'): 'th163.exe',
    #('17', 'th17', 'th17.exe', 'wbawc', 'wily beast and weakest creature'): 'th17.exe',
    ('18', 'th18', 'th18.exe', 'um', 'unconnected marketeers'): 'th18.exe',
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
    

# ==========================================================
# GAME SPECIFIC STUFF -- TO BE REFACTORED FURTHER ==========

# Statics
score         = offsets[_module_name].statics.score
graze         = offsets[_module_name].statics.graze
piv           = offsets[_module_name].statics.piv
power         = offsets[_module_name].statics.power
lives         = offsets[_module_name].statics.lives
life_pieces   = offsets[_module_name].statics.life_pieces
bombs         = offsets[_module_name].statics.bombs
bomb_pieces   = offsets[_module_name].statics.bomb_pieces
time_in_stage = offsets[_module_name].statics.time_in_stage
input         = offsets[_module_name].statics.input
rng           = offsets[_module_name].statics.rng
game_state    = offsets[_module_name].statics.game_state

# Untracked Statics
game_speed      = offsets[_module_name].statics_untracked.game_speed
visual_rng      = offsets[_module_name].statics_untracked.visual_rng
replay_filename = offsets[_module_name].statics_untracked.replay_filename
character       = offsets[_module_name].statics_untracked.character
subshot         = offsets[_module_name].statics_untracked.subshot
difficulty      = offsets[_module_name].statics_untracked.difficulty
rank            = offsets[_module_name].statics_untracked.rank
stage           = offsets[_module_name].statics_untracked.stage

# Player
player_pointer  = offsets[_module_name].player.player_pointer
zPlayer_pos     = offsets[_module_name].player.zPlayer_pos
zPlayer_hurtbox = offsets[_module_name].player.zPlayer_hurtbox
zPlayer_iframes = offsets[_module_name].player.zPlayer_iframes
zPlayer_focused = offsets[_module_name].player.zPlayer_focused

# Bullets
bullet_manager_pointer = offsets[_module_name].bullets.bullet_manager_pointer
zBulletManager_list    = offsets[_module_name].bullets.zBulletManager_list
zBullet_iframes        = offsets[_module_name].bullets.zBullet_iframes
zBullet_pos            = offsets[_module_name].bullets.zBullet_pos
zBullet_velocity       = offsets[_module_name].bullets.zBullet_velocity
zBullet_speed          = offsets[_module_name].bullets.zBullet_speed
zBullet_angle          = offsets[_module_name].bullets.zBullet_angle
zBullet_hitbox_radius  = offsets[_module_name].bullets.zBullet_hitbox_radius
zBullet_ex_delay_timer = offsets[_module_name].bullets.zBullet_ex_delay_timer
zBullet_scale          = offsets[_module_name].bullets.zBullet_scale
zBullet_type           = offsets[_module_name].bullets.zBullet_type
zBullet_color          = offsets[_module_name].bullets.zBullet_color

# Enemies
enemy_manager_pointer = offsets[_module_name].enemies.enemy_manager_pointer
zEnemyManager_list    = offsets[_module_name].enemies.zEnemyManager_list
zEnemy_data           = offsets[_module_name].enemies.zEnemy_data
zEnemyManager_list    = offsets[_module_name].enemies.zEnemyManager_list
zEnemy_pos            = offsets[_module_name].enemies.zEnemy_pos
zEnemy_hurtbox        = offsets[_module_name].enemies.zEnemy_hurtbox
zEnemy_hitbox         = offsets[_module_name].enemies.zEnemy_hitbox
zEnemy_rotation       = offsets[_module_name].enemies.zEnemy_rotation
zEnemy_time           = offsets[_module_name].enemies.zEnemy_time
zEnemy_score_reward   = offsets[_module_name].enemies.zEnemy_score_reward
zEnemy_hp             = offsets[_module_name].enemies.zEnemy_hp
zEnemy_hp_max         = offsets[_module_name].enemies.zEnemy_hp_max
zEnemy_iframes        = offsets[_module_name].enemies.zEnemy_iframes
zEnemy_flags          = offsets[_module_name].enemies.zEnemy_flags
zEnemy_subboss_id     = offsets[_module_name].enemies.zEnemy_subboss_id

zEnemyFlags_is_boss    = offsets[_module_name].associations.zEnemyFlags_is_boss
zEnemyFlags_intangible = offsets[_module_name].associations.zEnemyFlags_intangible
zEnemyFlags_no_hitbox  = offsets[_module_name].associations.zEnemyFlags_no_hitbox

# Items
item_manager_pointer   = offsets[_module_name].items.item_manager_pointer
zItemManager_array     = offsets[_module_name].items.zItemManager_array
zItemManager_array_len = offsets[_module_name].items.zItemManager_array_len
zItem_len              = offsets[_module_name].items.zItem_len
zItem_state            = offsets[_module_name].items.zItem_state
zItem_type             = offsets[_module_name].items.zItem_type
zItem_pos              = offsets[_module_name].items.zItem_pos
zItem_vel              = offsets[_module_name].items.zItem_vel

# Laser (Base)
laser_manager_pointer   = offsets[_module_name].laser_base.laser_manager_pointer
zLaserManager_list      = offsets[_module_name].laser_base.zLaserManager_list
zLaserBaseClass_next    = offsets[_module_name].laser_base.zLaserBaseClass_next
zLaserBaseClass_state   = offsets[_module_name].laser_base.zLaserBaseClass_state
zLaserBaseClass_type    = offsets[_module_name].laser_base.zLaserBaseClass_type
zLaserBaseClass_timer   = offsets[_module_name].laser_base.zLaserBaseClass_timer
zLaserBaseClass_offset  = offsets[_module_name].laser_base.zLaserBaseClass_offset
zLaserBaseClass_angle   = offsets[_module_name].laser_base.zLaserBaseClass_angle
zLaserBaseClass_length  = offsets[_module_name].laser_base.zLaserBaseClass_length
zLaserBaseClass_width   = offsets[_module_name].laser_base.zLaserBaseClass_width
zLaserBaseClass_speed   = offsets[_module_name].laser_base.zLaserBaseClass_speed
zLaserBaseClass_id      = offsets[_module_name].laser_base.zLaserBaseClass_id
zLaserBaseClass_iframes = offsets[_module_name].laser_base.zLaserBaseClass_iframes
zLaserBaseClass_sprite  = offsets[_module_name].laser_base.zLaserBaseClass_sprite
zLaserBaseClass_color   = offsets[_module_name].laser_base.zLaserBaseClass_color

# Laser (Line)
zLaserLine_start_pos  = offsets[_module_name].laser_line.zLaserLine_start_pos
zLaserLine_mgr_angle  = offsets[_module_name].laser_line.zLaserLine_mgr_angle
zLaserLine_max_length = offsets[_module_name].laser_line.zLaserLine_max_length
zLaserLine_mgr_speed  = offsets[_module_name].laser_line.zLaserLine_mgr_speed
zLaserLine_distance   = offsets[_module_name].laser_line.zLaserLine_distance

# Laser (Infinite)
zLaserInfinite_start_pos    = offsets[_module_name].laser_infinite.zLaserInfinite_start_pos
zLaserInfinite_velocity     = offsets[_module_name].laser_infinite.zLaserInfinite_velocity
zLaserInfinite_mgr_angle    = offsets[_module_name].laser_infinite.zLaserInfinite_mgr_angle
zLaserInfinite_angle_vel    = offsets[_module_name].laser_infinite.zLaserInfinite_angle_vel
zLaserInfinite_final_len    = offsets[_module_name].laser_infinite.zLaserInfinite_final_len
zLaserInfinite_mgr_len      = offsets[_module_name].laser_infinite.zLaserInfinite_mgr_len
zLaserInfinite_final_width  = offsets[_module_name].laser_infinite.zLaserInfinite_final_width
zLaserInfinite_mgr_speed    = offsets[_module_name].laser_infinite.zLaserInfinite_mgr_speed
zLaserInfinite_start_time   = offsets[_module_name].laser_infinite.zLaserInfinite_start_time
zLaserInfinite_expand_time  = offsets[_module_name].laser_infinite.zLaserInfinite_expand_time
zLaserInfinite_active_time  = offsets[_module_name].laser_infinite.zLaserInfinite_active_time
zLaserInfinite_shrink_time  = offsets[_module_name].laser_infinite.zLaserInfinite_shrink_time
zLaserInfinite_mgr_distance = offsets[_module_name].laser_infinite.zLaserInfinite_mgr_distance

# Laser (Curve)
zLaserCurve_max_length = offsets[_module_name].laser_curve.zLaserCurve_max_length
zLaserCurve_distance   = offsets[_module_name].laser_curve.zLaserCurve_distance
zLaserCurve_array      = offsets[_module_name].laser_curve.zLaserCurve_array

# Curve Node
zLaserCurveNode_pos   = offsets[_module_name].laser_curve_node.zLaserCurveNode_pos
zLaserCurveNode_vel   = offsets[_module_name].laser_curve_node.zLaserCurveNode_vel
zLaserCurveNode_angle = offsets[_module_name].laser_curve_node.zLaserCurveNode_angle
zLaserCurveNode_speed = offsets[_module_name].laser_curve_node.zLaserCurveNode_speed
zLaserCurveNode_size  = offsets[_module_name].laser_curve_node.zLaserCurveNode_size

# Ascii 
ascii_manager_pointer = offsets[_module_name].ascii.ascii_manager_pointer
global_timer          = offsets[_module_name].ascii.global_timer

# Spell Card
spellcard_pointer    = offsets[_module_name].spell_card.spellcard_pointer
zSpellcard_indicator = offsets[_module_name].spell_card.zSpellcard_indicator
zSpellcard_id        = offsets[_module_name].spell_card.zSpellcard_id
zSpellcard_bonus     = offsets[_module_name].spell_card.zSpellcard_bonus

# GUI
gui_pointer       = offsets[_module_name].gui.gui_pointer
zGui_bosstimer_s  = offsets[_module_name].gui.zGui_bosstimer_s
zGui_bosstimer_ms = offsets[_module_name].gui.zGui_bosstimer_ms

# Supervisor
supervisor_addr = offsets[_module_name].supervisor.supervisor_addr
game_mode = offsets[_module_name].supervisor.game_mode
rng_seed = offsets[_module_name].supervisor.rng_seed

# DDC-specific
bonus_count       = offsets[_module_name].game_specific['bonus_count']
seija_anm_pointer = offsets[_module_name].game_specific['seija_anm_pointer']
seija_flip_x      = offsets[_module_name].game_specific['seija_flip_x']
seija_flip_y      = offsets[_module_name].game_specific['seija_flip_y']
zPlayer_scale     = offsets[_module_name].game_specific['zPlayer_scale']

# Meaning Arrays
color_coin    = offsets[_module_name].associations.color_coin
color4        = offsets[_module_name].associations.color4
color8        = offsets[_module_name].associations.color8
color16       = offsets[_module_name].associations.color16
sprites       = offsets[_module_name].associations.sprites
curve_sprites = offsets[_module_name].associations.curve_sprites
item_types    = offsets[_module_name].associations.item_types
game_states   = offsets[_module_name].associations.game_states
game_modes    = offsets[_module_name].associations.game_modes
characters    = offsets[_module_name].associations.characters
subshots      = offsets[_module_name].associations.subshots
difficulties  = offsets[_module_name].associations.difficulties

# GAME SPECIFIC STUFF -- TO BE REFACTORED FURTHER ==========
# ==========================================================

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
        return sprites[sprite][0].split(' ')[0]
        
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