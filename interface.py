import pygetwindow as gw
import pyautogui
import psutil
import ctypes
import win32process
import win32api
import win32con
import cv2
import numpy as np
import time #debug
import random #debug
import keyboard #debug

# Set these to select the game before training
_game_title = 'Double Dealing Character. ver 1.00b'
_module_name = 'th14.exe'
_frame_rate = 60

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

def get_greyscale_screenshot(): #Note: fails if the window is inactive!    
    # Take a screenshot of the game window with a predetermined crop (note that there's 3 extra pixels on every side of the screenshot by default)
    screenshot = pyautogui.screenshot(region=(_game_window.left+35, _game_window.top+42, _game_window.width-44, _game_window.height-47))

    # Convert the PIL image to a NumPy array
    rgb_screenshot = np.array(screenshot)

    # Convert the RGB image to a greyscale image
    grey_screenshot = cv2.cvtColor(rgb_screenshot, cv2.COLOR_BGR2GRAY) # can be saved with imwrite
    
    # Add a channel dimension to the greyscale image    
    return np.expand_dims(grey_screenshot, axis=-1)
 
def get_normalized_greyscale_screenshot(): #apparently not needed
   return get_greyscale_screenshot().astype(np.float32) / 255.0
    
def read_game_int(offset):
    return np.uint32(int.from_bytes(_read_game_memory(offset, 4), byteorder='little'))

def apply_action(action_flag):
    # Iterate through the list of keys and hold/release keys depending on the bit value
    for index, key in enumerate(keys):
        # Check if the bit at the current position is set (1) or not (0)
        bit_set = (action_flag >> index) & 1

        if bit_set:
            keyboard.press(key)
        else:
            keyboard.release(key)

def restart_run():  
    apply_action(0) #ensure no residual input
    _two_frame_input('enter')
    _two_frame_input('esc')
    _two_frame_input('up')
    _two_frame_input('up')
    _two_frame_input('z')

    
# Private Method Definitions

def _read_game_memory(offset, size):
    buffer = ctypes.create_string_buffer(size)
    bytesRead = ctypes.c_ulonglong()
    ctypes.windll.kernel32.ReadProcessMemory(_process_handle, _base_address + offset, buffer, size, ctypes.byref(bytesRead))
    return buffer.raw

def _two_frame_input(key):
    keyboard.press(key)
    time.sleep(1 / _frame_rate)
    keyboard.release(key)
    time.sleep(1 / _frame_rate) #allows pressing the same key twice in a row
    
    

# Debug Method Definitions    

def _get_focus():
    _game_window.activate()
    time.sleep(0.2)
    
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
            apply_action(0) #un-press everything
            keep_running = False
        
        #calculate step delay
        delay = 0
        
        if prev_step != -1:
            delay = time.time() - prev_step
        else:
            prev_step = time.time()
            
        if delay < 1.0 / _frame_rate: 
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
        apply_action(action)
        

# Step 5 - Optionally put the game in focus for training activities
_get_focus()