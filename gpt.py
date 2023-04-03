from interface import *
from gpt4_prompt import *
from le_secrets import openai_api_key #make your own secrets (don't call it secrets.py tho that makes numpy act up lol)
import datetime
import openai

openai.api_key = openai_api_key
zPlayer = read_int(player_pointer)
zBulletManager = read_int(bullet_manager_pointer)
zEnemyManager = read_int(enemy_manager_pointer)
zItemManager = read_int(item_manager_pointer)

def read_zList(offset):
    return {"entry": read_int(offset), "next": read_int(offset + 0x4)}
    
def get_item_type(item_type):
    if(item_type < len(item_types)):
        return item_types[item_type]
    else:
        return item_type

def print_game_state():
    #print("--------------------------------------------------------------")
    #Player
    result = ""
    
    player_x = '%g'%(round(read_float(zPlayer + zPlayer_pos), 1))
    player_y = '%g'%(round(read_float(zPlayer + zPlayer_pos + 0x4), 1))
    player_iframes = read_int(zPlayer + zPlayer_iframes)
    player_focused = read_int(zPlayer + zPlayer_focused)
    #player_hurtbox_1 = '%g'%(round(read_float(zPlayer + zPlayer_hurtbox), 1))
    #player_hurtbox_2 = '%g'%(round(read_float(zPlayer + zPlayer_hurtbox + 0xc), 1))
    
    result += f"SCORE: {read_game_int(score)*10}\n"
    result += f"| {read_game_int(lives)} lives ({read_game_int(life_pieces)}/3 pieces), {read_game_int(bombs)} bombs ({read_game_int(bomb_pieces)}/8 pieces), {read_game_int(power)/100} power, {int(read_game_int(piv)/100)} score per point item, grazed bullets {read_game_int(graze)} total times\n"
    result += f"| Player at ({player_x}, {player_y}) with {player_iframes} invulnerability frames {'(focused movement)' if player_focused == 1 else '(unfocused movement)'}\n"
        
    # Bullets
    current_bullet_list = read_zList(zBulletManager + zBulletManager_list)
    
    #if current_bullet_list["next"]:
    result += "| List of on-screen bullets:\n"
    bullet_counter = 0
        
    while current_bullet_list["next"] and bullet_counter < 200: #head bullet is a placeholder/ignored
        current_bullet_list = read_zList(current_bullet_list["next"]) 
        bullet_counter = bullet_counter + 1 # release the 32k context model already ree
            
        zBullet = current_bullet_list["entry"]
        bullet_x = '%g'%(round(read_float(zBullet + zBullet_pos), 1))
        bullet_y = '%g'%(round(read_float(zBullet + zBullet_pos + 0x4), 1))
        bullet_speed = '%g'%(round(read_float(zBullet + zBullet_speed), 1))
        bullet_angle = '%g'%(round(read_float(zBullet + zBullet_angle), 1))
        bullet_scale = '%g'%(round(read_float(zBullet + zBullet_scale), 1))
        bullet_vel_x = '%g'%(round(read_float(zBullet + zBullet_velocity), 1))
        bullet_vel_y = '%g'%(round(read_float(zBullet + zBullet_velocity + 0x4), 1))
        bullet_radius = '%g'%(round(read_float(zBullet + zBullet_hitbox_radius), 1))
        #print(f"• ({bullet_x}, {bullet_y}), speed {bullet_speed} & angle {bullet_angle} (vel. {bullet_vel_x}, {bullet_vel_y}), hitbox size {bullet_radius}")
        result += f"• ({bullet_x}, {bullet_y}), ({bullet_vel_x}, {bullet_vel_y}), {bullet_radius}\n"

    # Enemies
    current_enemy_list = {"entry": 0, "next": read_int(zEnemyManager + zEnemyManager_list)}
    
    #if current_enemy_list["next"]:
    result += "| List of on-screen enemies:\n"
        
    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"]) 
        
        zEnemy = current_enemy_list["entry"]
        enemy_x = '%g'%(round(read_float(zEnemy + zEnemy_data + zEnemy_pos), 1))
        enemy_y = '%g'%(round(read_float(zEnemy + zEnemy_data + zEnemy_pos + 0x4), 1))
        #enemy_hurtbox_x = round(read_float(zEnemy + zEnemy_data + zEnemy_hurtbox), 1)
        #enemy_hurtbox_y = round(read_float(zEnemy + zEnemy_data + zEnemy_hurtbox + 0x4), 1)
        enemy_hp = read_int(zEnemy + zEnemy_data + zEnemy_hp)
        enemy_hp_max = read_int(zEnemy + zEnemy_data + zEnemy_hp_max)
               
        if read_byte(zEnemy + zEnemy_flags) & 0x31 != 0:
            continue
                    
        result += f"• ({enemy_x}, {enemy_y}), {enemy_hp} / {enemy_hp_max}\n"
    
    # Items
    current_item = zItemManager + zItemManager_array
    
    result += "| List of on-screen items:\n"
    while current_item < zItemManager + zItemManager_array_len:
        current_item += zItem_len
        
        if read_int(current_item + zItem_state) == 0:
            continue
            
        item_type = get_item_type(read_int(current_item + zItem_type))
        
        if item_type == "Cancel":
            continue
        
        item_x = '%g'%(round(read_float(current_item + zItem_pos), 1))
        item_y = '%g'%(round(read_float(current_item + zItem_pos + 0x4), 1))
        item_vel_x = '%g'%(round(read_float(current_item + zItem_vel), 1))
        item_vel_y = '%g'%(round(read_float(current_item + zItem_vel + 0x4), 1))
        
        result += f"• {item_type} Item @ ({item_x}, {item_y}) vel. ({item_vel_x}, {item_vel_y})\n"
    
    return result

while(True):
    game_state = print_game_state()
    
    print(game_state)
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=300,
        #temperature=1.2,
        messages = [{"role": "system", "content": system_prompt + boss_fight}, {"role": "user", "content": game_state + boss_fight}]
    )
    
    gpt_actions = response.choices[0].message.content
    print(gpt_actions)
    
    if(gpt_actions):
        unpause_game()
        enact_game_actions_text(gpt_actions)
        pause_game()
        
    else:
        print("Bank account succesfully drained")
        exit()
