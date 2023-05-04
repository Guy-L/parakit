from interface import *
import sys
import math
from dataclasses import dataclass
from typing import List, Tuple

zPlayer        = read_int(player_pointer)
zBulletManager = read_int(bullet_manager_pointer)
zEnemyManager  = read_int(enemy_manager_pointer)
zItemManager   = read_int(item_manager_pointer)

def read_zList(offset):
    return {"entry": read_int(offset), "next": read_int(offset + 0x4)}
    
def get_item_type(item_type):
    if(item_type < len(item_types)):
        return item_types[item_type]
    else:
        return item_type
        
def tabulate(str, min_size=10):
    to_append = min_size - len(str)
    return str + " "*to_append
    
    
@dataclass
class Bullet:
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    hitbox_radius: float
    
@dataclass
class Enemy:
    position: Tuple[float, float]
    hp: int
    hp_max: int

@dataclass
class Item:
    item_type: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    
@dataclass
class GameState:
    frame_id: int
    score: int
    lives: int
    life_pieces: int
    bombs: int
    bomb_pieces: int
    power: int
    piv: int
    graze: int
    player_position: Tuple[float, float]
    player_iframes: int
    player_focused: bool
    bullets: List[Bullet]
    enemies: List[Enemy]
    items: List[Item]

def extract_game_state():
    # Player
    player_x = round(read_float(zPlayer + zPlayer_pos), 1)
    player_y = round(read_float(zPlayer + zPlayer_pos + 0x4), 1)
    
    # Bullets
    bullets = []
    current_bullet_list = read_zList(zBulletManager + zBulletManager_list)
    bullet_counter = 0
        
    while current_bullet_list["next"] and bullet_counter < 200:
        current_bullet_list = read_zList(current_bullet_list["next"]) 
        bullet_counter = bullet_counter + 1
            
        zBullet       = current_bullet_list["entry"]
        bullet_x      = round(read_float(zBullet + zBullet_pos), 1)
        bullet_y      = round(read_float(zBullet + zBullet_pos + 0x4), 1)
        bullet_vel_x  = round(read_float(zBullet + zBullet_velocity), 1)
        bullet_vel_y  = round(read_float(zBullet + zBullet_velocity + 0x4), 1)
        bullet_radius = round(read_float(zBullet + zBullet_hitbox_radius), 1)
        
        bullets.append(Bullet(
            position      = (bullet_x, bullet_y), 
            velocity      = (bullet_vel_x, bullet_vel_y), 
            hitbox_radius = bullet_radius)
        )
        
    # Enemies
    enemies = []
    current_enemy_list = {"entry": 0, "next": read_int(zEnemyManager + zEnemyManager_list)}
        
    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"]) 
        
        zEnemy       = current_enemy_list["entry"]
        enemy_x      = round(read_float(zEnemy + zEnemy_data + zEnemy_pos), 1)
        enemy_y      = round(read_float(zEnemy + zEnemy_data + zEnemy_pos + 0x4), 1)
        enemy_hp     = read_int(zEnemy + zEnemy_data + zEnemy_hp)
        enemy_hp_max = read_int(zEnemy + zEnemy_data + zEnemy_hp_max)
               
        if read_byte(zEnemy + zEnemy_flags) & 0x31 != 0:
            continue
                    
        enemies.append(Enemy(
            position = (enemy_x, enemy_y), 
            hp       = enemy_hp, 
            hp_max   = enemy_hp_max)
        )
    
    # Items
    items = []
    current_item = zItemManager + zItemManager_array
    
    while current_item < zItemManager + zItemManager_array_len:
        current_item += zItem_len
        
        if read_int(current_item + zItem_state) == 0:
            continue
            
        item_type = get_item_type(read_int(current_item + zItem_type))
        
        if item_type == "Cancel":
            continue
        
        item_x     = round(read_float(current_item + zItem_pos), 1)
        item_y     = round(read_float(current_item + zItem_pos + 0x4), 1)
        item_vel_x = round(read_float(current_item + zItem_vel), 1)
        item_vel_y = round(read_float(current_item + zItem_vel + 0x4), 1)
        
        items.append(Item(
            item_type = item_type, 
            position  = (item_x, item_y), 
            velocity  = (item_vel_x, item_vel_y))
        )    
        
    gs = GameState(
        frame_id        = read_int(time_in_stage),
        score           = read_game_int(score) * 10,
        lives           = read_game_int(lives),
        life_pieces     = read_game_int(life_pieces),
        bombs           = read_game_int(bombs),
        bomb_pieces     = read_game_int(bomb_pieces),
        power           = read_game_int(power),
        piv             = int(read_game_int(piv) / 100),
        graze           = read_game_int(graze),
        player_position = (player_x, player_y),
        player_iframes  = read_int(zPlayer + zPlayer_iframes),
        player_focused  = read_int(zPlayer + zPlayer_focused) == 1,
        bullets         = bullets,
        enemies         = enemies,
        items           = items
    )
    
    return gs

def print_game_state(gs: GameState):
    print(f"[Frame #{gs.frame_id}] SCORE: {gs.score}")
    print(f"| {gs.lives} lives ({gs.life_pieces}/3 pieces), {gs.bombs} bombs ({gs.bomb_pieces}/8 pieces), {gs.power/100} power, {gs.piv} PIV, {gs.graze} graze")
    print(f"| Player at {gs.player_position} with {gs.player_iframes} invulnerability frames {'(focused movement)' if gs.player_focused else '(unfocused movement)'}")

    print("\nList of on-screen bullets:")
    print("  Position        Velocity         Hitbox Radius")
    for bullet in gs.bullets:
        print(f"• {tabulate(str(bullet.position), 16)}{tabulate(str(bullet.velocity), 16)} {bullet.hitbox_radius}")
        
    print("\nList of on-screen enemies:")
    print("  Position         HP / Max HP")
    for enemy in gs.enemies:
        print(f"• {tabulate(str(enemy.position), 16)} {enemy.hp} / {enemy.hp_max}")
    
    print("\nList of on-screen items:")
    print("  Type            Position         Velocity")
    for item in gs.items:
        print(f"• {tabulate(item.item_type + ' Item', 16)}{tabulate(str(item.position), 16)} {item.velocity}")    

print("================================")

if len(sys.argv) <= 1:
    print_game_state(extract_game_state())

elif len(sys.argv) > 3:
    print("Too many arguments!")
    
elif len(sys.argv) == 3 and sys.argv[2].lower() != "exact":
    print(f"Unrecognized second argument {sys.argv[2]} (should be \"exact\", won't proceed)")
    
else:    
    units = sys.argv[1][-1:]
    if units.lower() not in "fs":
        print("Could not parse time unit")
        exit()
    
    frame_count = 0
    if units == "s":
        try:
            frame_count = math.floor(float(sys.argv[1][:-1]) * frame_rate)
        except ValueError:
            print("Could not parse second count")
            exit()
    else:
        try:
            frame_count = int(sys.argv[1][:-1])
        except ValueError:
            print("Could not parse frame count")
            exit()
            
    print(f"Extracting for {frame_count} frames")
    exact = (len(sys.argv) == 3)
    
    unpause_game()
    
    #Initialize analysis vars here
    
    for i in range(frame_count):
        frame_timestamp = read_int(time_in_stage)
        print(f"Extracting frame #{i+1} (in-stage: #{frame_timestamp})")
        
        if exact:
            game_process.suspend()
        
        state = extract_game_state()
        #YOUR ANALYSIS HERE!
        
        if exact:
            game_process.resume()
            
        while read_int(time_in_stage) == frame_timestamp:
            pass
            
    pause_game()
        
    print("================================")
    print("Analysis results: (your print code here)")