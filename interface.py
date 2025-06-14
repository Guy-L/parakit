from settings import interface_settings as _settings
from offsets import offsets
from game_entities import *
from utils import *
import pygetwindow as gw
import pyautogui
import psutil
import ctypes
import win32process
import win32api
import win32gui
import win32con
import win32com.client
import numpy as np
import cv2
import keyboard
import struct
import random
import time

# Step 1 - Find valid game processes & windows
_game_main_modules = {
    #'th06.exe':  ('6', 'th6', 'th06', 'th06.exe', 'eosd', 'teosd', 'embodiment of scarlet devil'),
    #'th07.exe':  ('7', 'th7', 'th07', 'th07.exe', 'pcb', 'perfect cherry blossom'),
    #'th08.exe':  ('8', 'th8', 'th08', 'th08.exe', 'in', 'imperishable night'),
    #'th09.exe':  ('9', 'th9', 'th09', 'th09.exe', 'pofv', 'phantasmagoria of flower view'),
    #'th095.exe': ('9.5', 'th9.5', 'th095', 'th095.exe', 'stb', 'shoot the bullet'),
    #'th10.exe':  ('10', 'th10', 'th10.exe', 'mof', 'mountain of faith'),
    #'th11.exe':  ('11', 'th11', 'th11.exe', 'sa', 'subterranean animism'),
    #'th12.exe':  ('12', 'th12', 'th12.exe', 'ufo', 'undefined fantastic object'),
    #'th125.exe': ('12.5', 'th12.5', 'th125', 'th125.exe', 'ds', 'double spoiler'),
    #'th128.exe': ('12.8', 'th12.8', 'th128', 'th128.exe', 'gfw', 'great fairy wars'),
    'th13.exe':  ('13', 'th13', 'th13.exe', 'td', 'ten desires'),
    'th14.exe':  ('14', 'th14', 'th14.exe', 'ddc', 'double dealing character'),
    #'th143.exe': ('14.3', 'th14.3', 'th143', 'th143.exe', 'isc', 'impossible spell card'),
    'th15.exe':  ('15', 'th15', 'th15.exe', 'lolk', 'legacy of lunatic kingdom'),
    'th16.exe':  ('16', 'th16', 'th16.exe', 'hsifs', 'hidden star in four seasons'),
    #'th165.exe': ('16.5', 'th16.5', 'th165', 'th165.exe', 'vd', 'violet detector'),
    'th17.exe':  ('17', 'th17', 'th17.exe', 'wbawc', 'wily beast and weakest creature'),
    'th18.exe':  ('18', 'th18', 'th18.exe', 'um', 'unconnected marketeers'),
    #'th185.exe': ('18.5', 'th18.5', 'th185.exe', 'hbm', 'hundredth bullet market'),
    'th19.exe':  ('19', 'th19', 'th19.exe', 'udoalg', 'unfinished dream of all living ghost'),
}

# Windows are found *before* knowing the game process in order to filter out zombie processes
_windows = {}
for window in gw.getAllWindows():
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(window._hWnd, ctypes.byref(pid))
    _windows[pid.value] = window

valid_game_processes = []
valid_game_windows = []
for process in psutil.process_iter(['pid', 'name', 'status']):
    if process.info['name'] and process.info['name'] in _game_main_modules.keys():
        if process.info['status'] != psutil.STATUS_ZOMBIE and process.pid in _windows:
            valid_game_processes.append(process)
            valid_game_windows.append(_windows[process.pid])

if not valid_game_processes:
    print(color("Error:", 'red'), 'No valid game process found.')
    print('Make sure the game is open.')
    exit()


# Step 2 - Select the desired game (break tie if multiple games are open)
_valid_game_i = 0
_tiebreaker = _settings['tiebreaker_game']
if len(valid_game_processes) > 1:
    if _tiebreaker and isinstance(_tiebreaker, str):
        print(color('Tie:', 'cyan'), f"Multiple games are open; {bright(_tiebreaker)} will be selected if found (otherwise will select first).")
        for i in range(len(valid_game_processes)):
            if _tiebreaker.lower().strip() in _game_main_modules[valid_game_processes[i].info['name']]:
                _valid_game_i = i
                break
    else:
        print(color('Tie:', 'cyan'), "Multiple games are open; since tiebreaker setting isn't set, first process will be selected.")

game_process = valid_game_processes[_valid_game_i]
_game_window = valid_game_windows[_valid_game_i]
_module_name = game_process.info['name']
game_id = int(_game_main_modules[_module_name][0])

print(darker(f'Found the {_module_name} game process with PID: {game_process.pid}'))
print(darker(f'Found the game window: {_game_window.title}'))


# Step 3 - Get the selected process's base address
_base_address = None
_module_handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, game_process.pid)
_module_list = win32process.EnumProcessModules(_module_handle)

for module in _module_list:
    module_info = win32process.GetModuleFileNameEx(_module_handle, module)

    if _module_name in module_info.lower():
        _base_address = module
        break

if _base_address is not None:
    print(darker(f'Base address of the process main module: {hex(_base_address)}'))
else:
    print(color("Error:", 'red'), 'Module base address not found')
    exit()


# Step 4 - Open the process handle
_PROCESS_VM_READ = 0x0010
_PROCESS_QUERY_INFORMATION = 0x0400
_process_handle = ctypes.windll.kernel32.OpenProcess(_PROCESS_VM_READ | _PROCESS_QUERY_INFORMATION, False, game_process.pid)


# ==========================================================
# Game logic groups
uses_rank = [6, 7, 8, 10, 19]
uses_pivot_angle = [14, 15, 16, 17, 18]
has_enemy_score_reward = [6, 7, 8, 9, 10, 11]
has_charging_youmu = [13, 17]
has_bullet_delay = [14, 14.3, 18.5]
has_bullet_intangible = [16, 16.5]
has_ability_cards = [18, 18.5, 19]
switch_to_player_owning_flags = 14 #first game where player flags are stored by the player, and not in static memory
switch_to_serializable_ecl = 15 #first game where enemies store sub_id + offset within the sub as opposed to instruction pointers

# Tweak graph colors here
_gold        = ('Gold',        (255, 215, 0))
_silver      = ('Silver',      (190, 190, 190))
_bronze      = ('Bronze',      (205, 130, 50))
_black       = ('Black',       (50, 50, 50))
_dark_red    = ('Dark Red',    (150, 50, 50))
_red         = ('Red',         (255, 0, 0))
_purple      = ('Purple',      (190, 70, 210))
_violet      = ('Violet',      (130, 10, 250)) #used for fireballs
_pink        = ('Pink',        (255, 75, 235))
_dark_blue   = ('Dark Blue',   (20, 0, 150))
_blue        = ('Blue',        (0, 0, 255))
_dark_cyan   = ('Dark Cyan',   (0, 200, 200))
_cyan        = ('Cyan',        (65, 255, 255))
_dark_green  = ('Dark Green',  (115, 255, 115))
_green       = ('Green',       (135, 255, 145))
_lime        = ('Lime',        (190, 255, 85))
_dark_yellow = ('Dark Yellow', (180, 200, 45))
_yellow      = ('Yellow',      (255, 255, 40))
_orange      = ('Orange',      (255, 180, 40))
_white       = ('White',       (230, 230, 230))

color_coin    = [_gold, _silver, _bronze]
color4        = [_red, _blue, _green, _yellow]
color8        = [_black, _red, _pink, _blue, _cyan, _green, _yellow, _white]
color16       = [_black, _dark_red, _red, _purple, _pink, _dark_blue, _blue, _dark_cyan, _cyan, _dark_green, _green, _lime, _dark_yellow, _yellow, _orange, _white]
curve_sprites = ['Standard', 'Thunder', 'Grapevine'] #not worth setting per-game


# ==========================================================
# Interface Method Definitions

def get_rgb_screenshot(): #Note: fails if the window is not visible!
    #screenshot = pyautogui.screenshot(region=(_game_window.left+35, _game_window.top+42, _game_window.width-44, _game_window.height-47))
    screenshot = pyautogui.screenshot(region=(_game_window.left, _game_window.top, _game_window.width, _game_window.height))
    return np.array(screenshot)

def get_greyscale_screenshot(): #Note: fails if the window is not visible!
    #screenshot = pyautogui.screenshot(region=(_game_window.left+35, _game_window.top+42, _game_window.width-44, _game_window.height-47))
    screenshot = pyautogui.screenshot(region=(_game_window.left, _game_window.top, _game_window.width, _game_window.height))
    rgb_screenshot = np.array(screenshot)
    grey_screenshot = cv2.cvtColor(rgb_screenshot, cv2.COLOR_BGR2GRAY) # can be saved with imwrite

    return np.expand_dims(grey_screenshot, axis=-1)

def save_screenshot(filename, screenshot): 
    # Swap the R and B channels to match OpenCV's BGR format (no effect for greyscale pics)
    bgr_screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, bgr_screenshot)

def read_bool(offset, rel = False):
    return bool(read_int(offset, 1, rel))

def read_int(offset, bytes = 4, rel = False, signed = False):
    return int.from_bytes(_read_memory(offset, bytes, rel), byteorder='little', signed=signed)

def read_float(offset, rel = False):
    return struct.unpack('f', _read_memory(offset, 4, rel))[0]

def read_string(offset, length, rel = False):
    return _read_memory(offset, length, rel).decode('utf-8', 'ignore').split('\x00', 1)[0]

def get_color(sprite, color):
    if bullet_types[sprite][1] == 0:
        sprite_str = bullet_types[sprite][0]

        if 'Red' in sprite_str:
            return _red
        elif 'Purple' in sprite_str:
            return _purple
        elif 'Violet' in sprite_str:
            return _violet
        elif 'Blue' in sprite_str:
            return _blue
        elif 'Yellow' in sprite_str:
            return _yellow
        elif 'Orange' in sprite_str:
            return _orange

    elif bullet_types[sprite][1] == 3:
        return color_coin[color]

    elif bullet_types[sprite][1] == 4:
        return color4[color]

    elif bullet_types[sprite][1] == 8:
        return color8[color]

    elif bullet_types[sprite][1] == 16:
        return color16[color]

def get_curve_color(sprite, color):
    if sprite == 0:
        return color16[color]
    
    elif sprite == 1:
        return _cyan
    
    elif sprite == 2:
        return _lime

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

auto_termination = False
def terminate():
    global auto_termination
    auto_termination = True

def eval_termination_conditions(need_active):
    if keyboard.is_pressed(_settings['termination_key']):
        return "User pressed termination key"
    elif auto_termination:
        return "Automatic termination triggered by analyzer"
    elif need_active and _game_window != gw.getActiveWindow():
        return "Game no longer active (need_active set to True)"

def wait_game_frame(cur_game_frame=None, need_active=False):
    if not cur_game_frame:
        cur_game_frame = read_int(zGameThread + zGameThread_stage_timer)

    while read_int(zGameThread + zGameThread_stage_timer) == cur_game_frame:
        term_ret = eval_termination_conditions(need_active)
        if term_ret:
            return term_ret
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

def pause_game(wait_for_input=False):
    if game_process.is_running() and read_int(game_screen, rel=True) == 7 and read_int(pause_state, rel=True) == 2:
        #seems to be a delay before you can pause after
        #alt tabbing (no such delay for unpausing)
        if get_focus():
            wait_global_frame(count=1)

        keyboard.stash_state()
        press_key('esc')

        while read_int(pause_state, rel=True) != 0:
            pass

        #seems to be a hardcoded 8-frame delay between 
        #when pause starts and when pause menu can take inputs
        if wait_for_input:
            wait_global_frame(count=8)

def unpause_game():
    if game_process.is_running() and read_int(game_screen, rel=True) == 7 and read_int(pause_state, rel=True) == 0:
        get_focus()
        press_key('esc')

        while read_int(pause_state, rel=True) != 2:
            pass

def get_focus():
    if _game_window == gw.getActiveWindow():
        return False #didn't have to change focus

    while _game_window != gw.getActiveWindow():
        try:
            _game_window.activate()
        except gw.PyGetWindowException as e:
            print(bright("Note:"), "Game window failed to focus (most likely because ParaKit also lost focus).")
            print("      Trying again after sending blank input.", darker("It's unknown why this works."))
            win32com.client.Dispatch("WScript.Shell").SendKeys('')
            time.sleep(0.5)
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

def print_int(offset, bytes = 4, rel = False, signed = False, name = None, format = ""):
    print(f"{hex(offset)}{' (' + name + ')' if name else ''}: {read_int(offset, bytes, rel, signed):{format}}")

def print_float(offset, rel = False, name = None):
    print(f"{hex(offset)}{' (' + name + ')' if name else ''}: {read_float(offset, rel)}")

def print_string(offset, length, rel = False, name = None):
    print(f"{hex(offset)}{' (' + name + ')' if name else ''}: {read_string(offset, length, rel)}")

# Private Method Definitions

_buffers = {} #caching helps!
_kernel32 = ctypes.windll.kernel32 # minor optimization
_byref = ctypes.byref(ctypes.c_ulonglong()) # minor optimization
def _read_memory(address, size, rel):
    if size not in _buffers:
        _buffers[size] = ctypes.create_string_buffer(size)
    buffer = _buffers[size]
    if not _kernel32.ReadProcessMemory(_process_handle, address if not rel else _base_address + address, buffer, size, _byref):
        raise RuntimeError(f"Failed to read memory at address {hex(address if not rel else _base_address + address)} with size {size}")
    return buffer.raw

# Debug Method Definitions

def _random_player():
    get_focus()

    np.set_printoptions(linewidth=np.inf)
    print(np.array(["Lives", "L.Pieces", "Bombs", "B.Pieces", "Bonus", "Power", "PIV", "Graze", "Game State", "Action", "Time in Stage"]))

    while True:            
        cur_frame = read_int(zGameThread + zGameThread_stage_timer)
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
                    read_int(pause_state, rel=True),
                    '{:08b}'.format(action),
                    cur_frame+1])))
        apply_action_int(action)

def _scan_region(offset, size):
    print("     || Int        | Signed     | Float      | String     || *Int       | *Signed    | *Float     | *String")
    for address in range(offset, offset + size, 0x4):
        desc = tabulate(hex(address - offset), 4)
        while address > _base_address and address < 0x20000000:
            desc += " || " + truncate(read_int(address), 8)
            desc += " | " + truncate(read_int(address, signed=True), 8)
            desc += " | " + truncate(read_float(address), 8)
            desc += " | " + truncate(''.join(char for char in read_string(address, 8) if ord(char) > 32), 8)
            address = read_int(address)
        print(desc)


# Step 5 - Check PE header for games with multiple supported versions (th19)
if game_id == 19:
    _pe_offset = read_int(0x3c, rel=True) #(technically this is enough to differentiate)
    _pe_timestamp = read_int(_pe_offset + 0x8, rel=True)

    if _pe_timestamp == 0x64c47c44:
        _module_name += ' (v1.00a)'

    elif _pe_timestamp == 0x668bac2a:
        _module_name += ' (v1.10c)'

    else:
        print(color("Error:", 'red'), 'Unrecognized th19 version.')
        print(bright("Please " + underline("report this error") + " to the developers!"))
        exit()


# Step 6 - Unpack offsets from selected game into namespace
for offset_category in offsets[_module_name].__dict__.values():
    for name, val in (offset_category.items() if isinstance(offset_category, dict) else vars(offset_category).items()):
        if 'zEnemyData_' in name:
            globals()[name.replace('Data', '')] = (zEnemy_data + val if val != None else val)
        elif any(classname in name for classname in ['zLaserLine_', 'zLaserInfinite_', 'zLaserCurve_', 'zLaserBeam_']):
            globals()[name] = (zLaserBaseClass_len + val if val != None else val)
        else:
            globals()[name] = val
del offsets #be kind to your namespace :)


# Step 7 - Define this here for waiting methods
global_timer += read_int(ascii_manager_ptr, rel=True)