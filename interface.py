import pygetwindow as gw
import pyautogui
import psutil
import ctypes
import win32process
import win32api
import win32con
import numpy as np
import cv2
import time #debug
import random #debug
import keyboard #debug
import struct

# Set these to select the game before training
_game_title = 'Double Dealing Character. ver 1.00b'
_module_name = 'th14.exe'
frame_rate = 60

# Offsets (public)
score = 0xF5830
lives = 0xF5864
life_pieces = 0xF5868
bombs = 0xF5870
bomb_pieces = 0xF5874
bonus_count = 0xF5894
power = 0xF5858
piv = 0xF584C
graze = 0xF5840

time_in_stage = 0x4f58b0

player_pointer = 0x4db67c 
zPlayer_pos = 0x5e0
zPlayer_iframes = 0x182c0 + 0x4
zPlayer_hurtbox = 0x630
zPlayer_focused = 0x184b0

bullet_manager_pointer = 0x4db530
zBulletManager_list = 0x7c
zBullet_pos = 0xbc0
zBullet_speed = 0xbd8
zBullet_velocity = 0xbcc
zBullet_angle = 0xbdc
zBullet_scale = 0x13bc
zBullet_hitbox_radius = 0xbe0

enemy_manager_pointer = 0x4db544
zEnemyManager_list = 0xd0
zEnemy_data = 0x11f0
zEnemy_pos = 0x44
zEnemy_hurtbox = 0x110
zEnemy_hp = 0x3f74
zEnemy_hp_max = 0x3f74 + 0x4
zEnemy_flags = 0x5244

item_manager_pointer = 0x4db660
zItemManager_array = 0x14
zItemManager_array_len = 0xddd854
zItem_len = 0xc18
zItem_state = 0xbf0 
zItem_type = 0xbf4
zItem_pos = 0xbac
zItem_vel = 0xbb8

item_types = ["Unknown 0", "Power", "Point", "Full Power", "Life Piece", "Unknown 5", "Bomb Piece", "Unknown 7", "Unknown 8", "Cancel", "Cancel"]
#game_over = 0xF9620 #always 0 on startup & 1 on the game over screen, stays at 1 after continuing unless player pauses (zun wtf)
game_state = 0xF7AC8 #seems to be: 0 = pausing/stage transition, 
                     #             1 = end of playable run (ending/practice end/game over/main menu), 
                     #             2 = actively playing

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
 
def get_normalized_greyscale_screenshot():
   return get_greyscale_screenshot().astype(np.float32) / 255.0
   
def save_screenshot(filename, screenshot): 
    # Swap the R and B channels to match OpenCV's BGR format (no effect for greyscale pics)
    bgr_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr_screenshot)

def read_int(offset):
    #return np.uint32(int.from_bytes(_read_game_memory(offset, 4), byteorder='little'))
    return int.from_bytes(_read_memory(offset, 4), byteorder='little')
    
def read_game_int(offset):
    #return np.uint32(int.from_bytes(_read_game_memory(offset, 4), byteorder='little'))
    return int.from_bytes(_read_game_memory(offset, 4), byteorder='little')
    
def read_game_float(offset):
    return struct.unpack('f', _read_game_memory(offset, 4))[0]

def read_float(offset):
    return struct.unpack('f', _read_memory(offset, 4))[0]
    
def read_byte(offset):
    return int.from_bytes(_read_memory(offset, 1), byteorder='big')
    
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
           
def wait_frame():
    _sleep(1 / frame_rate)

def wait_to_next_frame():
    _sleep(1 / frame_rate)
    
def restart_run():  
    apply_action_int(0) #ensure no residual input
    _two_frame_input('enter')
    _two_frame_input('esc')
    _two_frame_input('up')
    _two_frame_input('up')
    _two_frame_input('z')
    
def pause_game():
    if read_game_int(game_state) != 0:
        _two_frame_input('esc')
        
def unpause_game():
    if read_game_int(game_state) != 2:
        _two_frame_input('esc')
        _sleep(10 / frame_rate)
        
def enact_game_actions_bin(actions): #space-separated action binary strings
    _get_focus()
    action_array = actions.split()
    for action in action_array:
        apply_action_bin(action)
        wait_frame()
    apply_action_int(0)

def enact_game_actions_text(actions): #line-separated sets of space-seperates key press names
    _get_focus()
    action_array = actions.split('\n')
    for action in action_array:
        apply_action_str(action)
        wait_frame()
    apply_action_int(0)

# Private Method Definitions

def _read_game_memory(offset, size):
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_ulonglong()
    ctypes.windll.kernel32.ReadProcessMemory(_process_handle, _base_address + offset, buffer, size, ctypes.byref(bytesRead))
    return buffer.raw
    
def _read_memory(address, size):
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_ulonglong()
    ctypes.windll.kernel32.ReadProcessMemory(_process_handle, address, buffer, size, ctypes.byref(bytesRead))
    return buffer.raw

def _two_frame_input(key):
    keyboard.press(key)
    _sleep(1 / frame_rate)
    keyboard.release(key)
    _sleep(1 / frame_rate) #allows pressing the same key twice in a row
    
def _sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()
        
#def ???():
#    while now < end:
#        now = get_now()
    
    

# Debug Method Definitions    

def _get_focus():
    _game_window.activate()
    _sleep(0.2)
    
def _render_normalized_greyscale_screenshot(normalized_grey_screenshot):
    # Convert the normalized greyscale screenshot back to the range of 0 to 255
    grey_screenshot = (normalized_grey_screenshot * 255).astype(np.uint8)

    # Save the greyscale screenshot as an image file
    cv2.imwrite("normalized_greyscale_screenshot.png", grey_screenshot)
    
    #example where you render a 100x100 rectangle at the top left of the normalized greyscale screenshot:
    #_get_focus()
    #normalized_grey_screenshot = get_normalized_greyscale_screenshot()
    #_render_normalized_greyscale_screenshot(normalized_grey_screenshot[0:100, 0:100]) 
    
def _random_player():
    _get_focus()
    keep_running = True
    prev_step = -1

    np.set_printoptions(linewidth=np.inf)
    print(np.array(["Lives", "L.Pieces", "Bombs", "B.Pieces", "Bonus", "Power", "PIV", "Graze", "Game State", "Action", "Step Delay"]))
    
    while(keep_running):
        #user terminates the process (T press / change window)
        if keyboard.is_pressed('t') or _game_window != gw.getActiveWindow(): 
            apply_action_int(0) #un-press everything
            keep_running = False
        
        #calculate step delay
        delay = 0
        
        if prev_step != -1:
            delay = time.time() - prev_step
        else:
            prev_step = time.time()
            
        if delay < 1.0 / frame_rate: 
            continue  #synchronize action rate with framerate
            
        prev_step = time.time()
        
        #display game variables and take random actions
        action = random.randint(0, 2**len(keys))
        print(list(np.array([
                    read_game_int(lives), read_game_int(life_pieces),
                    read_game_int(bombs), read_game_int(bomb_pieces),
                    read_game_int(bonus_count), 
                    read_game_int(power), 
                    read_game_int(piv), 
                    read_game_int(graze),
                    read_game_int(game_state),
                    '{:08b}'.format(action), 
                    "{:.2f}".format(delay)])))
        apply_action_int(action)
        

# Step 5 - Optionally put the game in focus for training activities
_get_focus()