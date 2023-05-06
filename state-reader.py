from interface import *
from analysis import *
from game_entities import *
import sys
import math
import atexit

requiresBullets = True
requiresEnemies = True
requiresItems = True
requiresScreenshots = False

zPlayer        = read_int(player_pointer)
zBulletManager = read_int(bullet_manager_pointer)
zEnemyManager  = read_int(enemy_manager_pointer)
zItemManager   = read_int(item_manager_pointer)
        
def tabulate(str, min_size=10):
    to_append = min_size - len(str)
    return str + " "*to_append

def extract_bullets():
    bullets = []
    current_bullet_list = read_zList(zBulletManager + zBulletManager_list)
        
    while current_bullet_list["next"]:
        current_bullet_list = read_zList(current_bullet_list["next"]) 
            
        zBullet       = current_bullet_list["entry"]
        bullet_x      = round(read_float(zBullet + zBullet_pos), 1)
        bullet_y      = round(read_float(zBullet + zBullet_pos + 0x4), 1)
        bullet_vel_x  = round(read_float(zBullet + zBullet_velocity), 1)
        bullet_vel_y  = round(read_float(zBullet + zBullet_velocity + 0x4), 1)
        bullet_speed = round(read_float(zBullet + zBullet_speed), 1)
        bullet_angle = round(read_float(zBullet + zBullet_angle), 1)
        bullet_scale = round(read_float(zBullet + zBullet_scale), 1)
        bullet_radius = round(read_float(zBullet + zBullet_hitbox_radius), 1)
        
        bullets.append(Bullet(
            position      = (bullet_x, bullet_y), 
            velocity      = (bullet_vel_x, bullet_vel_y), 
            speed = bullet_speed,
            angle = bullet_angle,
            scale = bullet_scale,
            hitbox_radius = bullet_radius
        ))
        
    return bullets
    
def extract_enemies():
    enemies = []
    current_enemy_list = {"entry": 0, "next": read_int(zEnemyManager + zEnemyManager_list)}
        
    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"]) 
        
        zEnemy       = current_enemy_list["entry"]
        enemy_x      = round(read_float(zEnemy + zEnemy_data + zEnemy_pos), 1)
        enemy_y      = round(read_float(zEnemy + zEnemy_data + zEnemy_pos + 0x4), 1)
        enemy_hp     = read_int(zEnemy + zEnemy_data + zEnemy_hp)
        enemy_hp_max = read_int(zEnemy + zEnemy_data + zEnemy_hp_max)
        enemy_hurtbox_x = round(read_float(zEnemy + zEnemy_data + zEnemy_hurtbox), 1)
        enemy_hurtbox_y = round(read_float(zEnemy + zEnemy_data + zEnemy_hurtbox + 0x4), 1)
               
        if read_byte(zEnemy + zEnemy_flags) & 0x31 != 0:
            continue
                    
        enemies.append(Enemy(
            position = (enemy_x, enemy_y), 
            hurtbox = (enemy_hurtbox_x, enemy_hurtbox_y), 
            hp       = enemy_hp, 
            hp_max   = enemy_hp_max
        ))
    
    return enemies
    
def extract_items():
    items = []
    current_item = zItemManager + zItemManager_array
    
    while current_item < zItemManager + zItemManager_array_len:
        current_item += zItem_len
        
        if read_int(current_item + zItem_state) == 0:
            continue
            
        item_type = get_item_type(read_int(current_item + zItem_type))
        
        item_x     = round(read_float(current_item + zItem_pos), 1)
        item_y     = round(read_float(current_item + zItem_pos + 0x4), 1)
        item_vel_x = round(read_float(current_item + zItem_vel), 1)
        item_vel_y = round(read_float(current_item + zItem_vel + 0x4), 1)
        
        items.append(Item(
            item_type = item_type, 
            position  = (item_x, item_y), 
            velocity  = (item_vel_x, item_vel_y)
        ))
    
    return items
    
def extract_game_state():        
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
        player_position = (round(read_float(zPlayer + zPlayer_pos), 1), round(read_float(zPlayer + zPlayer_pos + 0x4), 1)),
        player_iframes  = read_int(zPlayer + zPlayer_iframes),
        player_focused  = read_int(zPlayer + zPlayer_focused) == 1,
        bullets         = extract_bullets() if requiresBullets else None,
        enemies         = extract_enemies() if requiresEnemies else None,
        items           = extract_items() if requiresItems else None,
        screen          = get_rgb_screenshot() if requiresScreenshots else None
    )
    
    return gs

def print_game_state(gs: GameState):
    print(f"[Frame #{gs.frame_id}] SCORE: {gs.score}")
    print(f"| {gs.lives} lives ({gs.life_pieces}/3 pieces), {gs.bombs} bombs ({gs.bomb_pieces}/8 pieces), {gs.power/100} power, {gs.piv} PIV, {gs.graze} graze")
    print(f"| Player at {gs.player_position} with {gs.player_iframes} invulnerability frames {'(focused movement)' if gs.player_focused else '(unfocused movement)'}")

    if gs.bullets:
        print("\nList of on-screen bullets:")
        print("  Position        Velocity         Hitbox Radius")
        for bullet in gs.bullets:
            print(f"• {tabulate(str(bullet.position), 16)}{tabulate(str(bullet.velocity), 16)} {bullet.hitbox_radius}")
        
    if gs.enemies:
        print("\nList of on-screen enemies:")
        print("  Position         HP / Max HP")
        for enemy in gs.enemies:
            print(f"• {tabulate(str(enemy.position), 16)} {enemy.hp} / {enemy.hp_max}")
    
    if gs.items:
        print("\nList of on-screen items:")
        print("  Type            Position         Velocity")
        for item in gs.items:
            print(f"• {tabulate(item.item_type + ' Item', 16)}{tabulate(str(item.position), 16)} {item.velocity}")    
        
def on_exit():
    game_process.resume() #just in case!!

atexit.register(on_exit)
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
    
    #unpause_game()
    print("(unpause the game to begin)")
    analysis = Analysis()
    end_of_play = False
    
    for i in range(frame_count):
        if end_of_play:
            break
            
        frame_timestamp = read_int(time_in_stage)
        print(f"Extracting frame #{i+1} (in-stage: #{frame_timestamp})")
        
        if exact:
            game_process.suspend()
        
        state = extract_game_state()
        analysis.step(state)
        
        if exact:
            game_process.resume()
            
        #busy wait for next frame
        while read_int(time_in_stage) == frame_timestamp: 
            if read_game_int(game_state) == 1:
                print("End of play detected; terminating now")
                end_of_play = True
                break
            
    pause_game()
        
    print("================================")
    analysis.done(requiresScreenshots)