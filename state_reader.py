from settings import extraction_settings, singlext_settings, seqext_settings
from utils import *
import sys
import math
import atexit
import traceback

try:
    print(italics(darker("Setting up extraction interface...")), clear(), end='\r')
    from interface import *
    print(italics(darker("Importing analyzers...")), clear(), end='\r')
    import analysis_examples as analysis #(includes analysis.py analyzers)
    print(italics(darker("Starting extraction...")), clear(), end='\r')
except KeyboardInterrupt:
    print("Extraction setup interrupted by user.")
    exit()

#For quick access
analyzer, requires_bullets, requires_enemies, requires_items, requires_lasers, requires_player_shots, requires_screenshots, requires_side2_pvp = extraction_settings.values()
exact = seqext_settings['exact']
need_active = seqext_settings['need_active']

def extract_bullets(bullet_manager = zBulletManager):
    bullets = []
    current_bullet_list = read_zList(bullet_manager + zBulletManager_list)

    #may need logic group if multiple games have pointer as tick list head
    if game_id == 19:
        if current_bullet_list["entry"] == 0:
            return bullets
        current_bullet_list = read_zList(current_bullet_list["entry"])

    while current_bullet_list["next"]:
        current_bullet_list = read_zList(current_bullet_list["next"])
        zBullet = current_bullet_list["entry"]

        bullet_type = read_int(zBullet + zBullet_type, 2)
        bullet_color = read_int(zBullet + zBullet_color, 2)
        bullet_hitbox_rad = read_float(zBullet + zBullet_hitbox_radius)
        bullet_is_intangible = False

        #fallback for intangible bullets (radius set to 0) in HSiFS
        #note: bullet flag 2**1 seems to have the same effect, though I've not seen it used yet
        if not bullet_hitbox_rad and game_id in has_bullet_intangible:
            bullet_hitbox_rad = read_float(bullet_typedefs_radius + bullet_typedef_len * bullet_type, rel=True)
            bullet_is_intangible = True
            bullet_color = 0 #all intangible bullets use the dark render mode

        bullet = {
            'id':            zBullet,
            'position':     (read_float(zBullet + zBullet_pos), read_float(zBullet + zBullet_pos + 0x4)),
            'velocity':     (read_float(zBullet + zBullet_velocity), read_float(zBullet + zBullet_velocity + 0x4)),
            'speed':         read_float(zBullet + zBullet_speed),
            'angle':         read_float(zBullet + zBullet_angle),
            'scale':         read_float(zBullet + zBullet_scale) if zBullet_scale else 1,
            'hitbox_radius': bullet_hitbox_rad,
            'iframes':       read_int(zBullet + zBullet_iframes),
            'is_active':     read_int(zBullet + zBullet_state, 2) == 1,
            'is_grazeable':  read_int(zBullet + zBullet_flags) & zBulletFlags_grazed == 0,
            'alive_timer':   read_int(zBullet + zBullet_timer),
            'type':          bullet_type,
            'color':         bullet_color,
        }

        #Game-specific attributes
        if game_id in has_bullet_delay:
            bullet['show_delay'] = read_int(zBullet + zBullet_ex_delay_timer)
            bullets.append(ShowDelayBullet(**bullet))

        elif game_id in has_bullet_intangible:
            bullet['is_intangible'] = bullet_is_intangible
            bullets.append(CanIntangibleBullet(**bullet))

        elif game_id == 15:
            bullet['graze_timer'] = read_int(zBullet + zBullet_graze_timer)
            bullets.append(GrazeTimerBullet(**bullet))

        elif game_id == 19:
            bullet['can_gen_items_timer'] = read_int(zBullet + zBullet_can_gen_items_timer)
            bullet['is_grazeable'] = read_int(zBullet + zBullet_can_gen_items) == 1
            bullets.append(CanGenItemsTimerBullet(**bullet))

        else:
            bullets.append(Bullet(**bullet))

    return bullets

def extract_enemy_movement_limit(movement_bounds, flags):
    if flags & zEnemyFlags_has_move_limit:
        return EnemyMovementLimit(
            center = (read_float(movement_bounds), read_float(movement_bounds + 0x4)),
            width = read_float(movement_bounds + 0x8),
            height = read_float(movement_bounds + 0xc),
        )

def extract_enemy_ecl_sub_name(ecl_ref):
    if game_id >= switch_to_serializable_ecl:
        enemy_sub_id = read_int(ecl_ref) #may be -1 for spawning enemies

        if enemy_sub_id in range(len(ecl_sub_names)):
            return ecl_sub_names[enemy_sub_id]

    else:
        cur_instr_addr = read_int(ecl_ref)
        enemy_sub_id = None
        for sub_id in range(len(ecl_sub_starts)):
            if ecl_sub_starts[sub_id] <= cur_instr_addr:
                if not enemy_sub_id or ecl_sub_starts[sub_id] > ecl_sub_starts[enemy_sub_id] :
                    enemy_sub_id = sub_id

        if enemy_sub_id:
            return ecl_sub_names[enemy_sub_id]

def extract_enemy_thresholds(interrupts):
    zEnemyHealthThreshold = None
    zEnemyTimeThreshold = None

    interrupts_end = interrupts + zEnemyInterrupt_len * zEnemy_interrupts_arr_len

    for interrupt in range(interrupts, interrupts_end, zEnemyInterrupt_len):
        interrupt_hp = read_int(interrupt + zEnemyInterrupt_hp, signed=True)

        if interrupt_hp >= 0:
            if not zEnemyHealthThreshold:
                #grab health threshold from first interrupt with valid health
                interrupt_hp_sub_addr = interrupt + zEnemyInterrupt_hp_sub

                if game_id < switch_to_serializable_ecl: #seems its a pointer in older games
                    interrupt_hp_sub_addr = read_int(interrupt_hp_sub_addr)

                zEnemyHealthThreshold = (interrupt_hp, read_string(interrupt_hp_sub_addr, 64))

            interrupt_time = read_int(interrupt + zEnemyInterrupt_time, signed=True)
            if interrupt_time > 0:
                #grab time threshold from first interrupt with BOTH valid health and time
                interrupt_time_sub_addr = interrupt + zEnemyInterrupt_time_sub

                if game_id < switch_to_serializable_ecl: #seems its a pointer in older games
                    interrupt_time_sub_addr = read_int(interrupt_time_sub_addr)

                zEnemyTimeThreshold = (interrupt_time, read_string(interrupt_time_sub_addr, 64))
                break

    return (zEnemyHealthThreshold, zEnemyTimeThreshold)

def extract_enemy_drops(enemy_drops):
    drops = {}

    for item_id in item_types:
        drop_count = read_int(enemy_drops + 0x4*item_id)
        if drop_count:
            drops[item_id] = drop_count

    main_drop_id = read_int(enemy_drops)
    if main_drop_id:
        if main_drop_id in drops:
            drops[main_drop_id] += 1
        else:
            drops[main_drop_id] = 1

    return drops

def extract_enemies(enemy_manager = zEnemyManager):
    enemies = []
    current_enemy_list = {"entry": 0, "next": read_int(enemy_manager + zEnemyManager_list)}
    ecl_sub_names, ecl_sub_starts = ecl_sub_arrs[enemy_manager]

    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"])

        zEnemy = current_enemy_list["entry"]
        zEnemyFlags = (read_int(zEnemy + zEnemy_flags + 0x4) << 32) | read_int(zEnemy + zEnemy_flags)

        if enemy_manager != zEnemyManager: #udoalg p2
            zEnemyAnmVM = find_anm_vm_by_id(read_int(zEnemy + zEnemy_anm_vm_id), zAnmManager_list_p2)
        else:
            zEnemyAnmVM = find_anm_vm_by_id(read_int(zEnemy + zEnemy_anm_vm_id))

        # Filter invisible enemies
        if not zEnemyAnmVM:
            continue

        enemy = {
            'id':               zEnemy,
            'position':         (read_float(zEnemy + zEnemy_pos), read_float(zEnemy + zEnemy_pos + 0x4)),
            'velocity':         (read_float(zEnemy + zEnemy_vel), read_float(zEnemy + zEnemy_vel + 0x4)),
            'hurtbox':          (read_float(zEnemy + zEnemy_hurtbox), read_float(zEnemy + zEnemy_hurtbox + 0x4)),
            'hitbox':           (read_float(zEnemy + zEnemy_hitbox), read_float(zEnemy + zEnemy_hitbox + 0x4)),
            'move_limit':       extract_enemy_movement_limit(zEnemy + zEnemy_movement_bounds, zEnemyFlags),
            'no_hurtbox':       zEnemyFlags & zEnemyFlags_no_hurtbox != 0,
            'no_hitbox':        zEnemyFlags & zEnemyFlags_no_hitbox != 0,
            'invincible':       zEnemyFlags & zEnemyFlags_invincible != 0,
            'intangible':       zEnemyFlags & zEnemyFlags_intangible != 0,
            'is_grazeable':     zEnemyFlags & zEnemyFlags_is_grazeable != 0,
            'is_rectangle':     zEnemyFlags & zEnemyFlags_is_rectangle != 0,
            'is_boss':          zEnemyFlags & zEnemyFlags_is_boss != 0,
            'subboss_id':       read_int(zEnemy + zEnemy_subboss_id, signed=True),
            'health_threshold': None, #only checked for boss & boss-related enemies
            'time_threshold':   None, #only checked for boss & boss-related enemies
            'rotation':         read_float(zEnemy + zEnemy_rotation) if game_id != 13 else read_float(zEnemyAnmVM + zAnmVm_rotation_z),
            'pivot_angle':      read_float(zEnemyAnmVM + zAnmVm_rotation_z) if game_id in uses_pivot_angle else 0,
            'anm_page':         read_int(zEnemy + zEnemy_anm_page),
            'anm_id':           read_int(zEnemy + zEnemy_anm_id),
            'ecl_sub_name':     extract_enemy_ecl_sub_name(zEnemy + zEnemy_ecl_ref),
            'ecl_sub_timer':    read_int(zEnemy + zEnemy_ecl_timer),
            'alive_timer':      read_int(zEnemy + zEnemy_alive_timer),
            'health':           read_int(zEnemy + zEnemy_hp),
            'health_max':       read_int(zEnemy + zEnemy_hp_max),
            'drops':            extract_enemy_drops(zEnemy + zEnemy_drops),
            'iframes':          read_int(zEnemy + zEnemy_iframes),
        }

        # Checking thresholds for boss & boss-related enemies
        if enemy['is_boss'] or enemy['anm_page'] == 0 or enemy['anm_page'] > 2:
            enemy['health_threshold'], enemy['time_threshold'] = extract_enemy_thresholds(zEnemy + zEnemy_interrupts_arr)

        # Game-specific extensions
        if game_id in has_enemy_score_reward:
            enemy['score_reward'] = read_int(zEnemy + zEnemy_score_reward)
            enemies.append(ScoreRewardEnemy(**enemy))

        if game_id == 13:
            spirit_time_max  = read_int(zEnemy + zEnemy_spirit_time_max)
            remaining_frames = spirit_time_max - enemy['alive_timer']

            if remaining_frames >= 0:
                interval_size = spirit_time_max // read_int(zEnemy + zEnemy_max_spirit_count)
                enemy['speedkill_cur_drop_amt'] = (remaining_frames // interval_size) + (2 if difficulty >= 2 else 1)
                enemy['speedkill_time_left_for_amt'] = remaining_frames - (remaining_frames // interval_size) * interval_size + 1

            else:
                enemy['speedkill_cur_drop_amt'] = 0
                enemy['speedkill_time_left_for_amt'] = 0

            enemies.append(SpiritDroppingEnemy(**enemy))

        elif game_id == 15:
            enemy['shootdown_weight'] = read_int(zEnemy + zEnemy_weight, signed=True)
            enemies.append(WeightedEnemy(**enemy))

        elif game_id == 16:
            bonus_timer = read_int(zEnemy + zEnemy_season_drop + zSeasonDrop_timer)
            max_time = read_int(zEnemy + zEnemy_season_drop + zSeasonDrop_max_time)
            min_count = read_int(zEnemy + zEnemy_season_drop + zSeasonDrop_min_count)

            if enemy['drops'] and not enemy['no_hurtbox']:
                base_season_drop_count = enemy['drops'][16]
                enemy['speedkill_cur_drop_amt'] = min_count + ((base_season_drop_count - min_count) * bonus_timer) // max_time

                if enemy['speedkill_cur_drop_amt'] == min_count:
                    enemy['speedkill_time_left_for_amt'] = 0

                else:
                    frames_left = 1 #bruteforce because interval size for above formula is NOT regular, too hard
                    while min_count + ((base_season_drop_count - min_count) * (bonus_timer-frames_left)) // max_time == enemy['speedkill_cur_drop_amt']:
                        frames_left += 1

                    enemy['speedkill_time_left_for_amt'] = frames_left

            else:
                enemy['speedkill_cur_drop_amt'] = 0
                enemy['speedkill_time_left_for_amt'] = 0

            enemy['season_drop_timer'] = bonus_timer
            enemy['season_drop_max_time'] = max_time
            enemy['season_drop_min_count'] = min_count
            enemy['damage_per_season_drop'] = read_int(zEnemy + zEnemy_season_drop + zSeasonDrop_damage_for_drop)
            enemy['damage_taken_for_season_drops'] = read_int(zEnemy + zEnemy_season_drop + zSeasonDrop_total_damage)

            enemies.append(SeasonDroppingEnemy(**enemy))

        else:
            enemies.append(Enemy(**enemy))

    return enemies

#used to get special state info contained by the boss, like kyouko echo, okina season disable...
def find_special_enemy_addr(special_func, enemy_manager = zEnemyManager):
    current_enemy_list = {"entry": 0, "next": read_int(enemy_manager + zEnemyManager_list)}

    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"])

        zEnemy = current_enemy_list["entry"]
        if read_int(zEnemy + zEnemy_special_func) == special_func:
            return zEnemy

#used to get the (uncapped) boss timer from extracted enemies
def get_boss_timer(enemies):
    #boss timer GUI updates off last boss enemy with valid time threshold
    for enemy in reversed(enemies):
        if enemy.time_threshold and enemy.is_boss:

            #note: + 1 accounts for extra frame from time > threshold comparison (instead of >=)
            return (enemy.time_threshold[0] + 1 - enemy.ecl_sub_timer)/60

def extract_items(item_manager = zItemManager):
    items = []
    item_array_start = item_manager + zItemManager_array
    item_array_end   = item_array_start + zItemManager_array_len * zItem_len

    for item in range(item_array_start, item_array_end, zItem_len):
        item_state = read_int(item + zItem_state)
        if item_state == 0:
            continue

        item_type = read_int(item + zItem_type)
        if item_type not in item_types:
            if item_type < 50:
                print(f"Found and skipped unknown item with type ID {item_type}. If this is a real in-game item, please report it to the developper!")
            continue

        items.append(Item(
            id          = item,
            state       = item_state,
            item_type   = item_type,
            position    = (read_float(item + zItem_pos), read_float(item + zItem_pos + 0x4)),
            velocity    = (read_float(item + zItem_vel), read_float(item + zItem_vel + 0x4)),
            alive_timer = read_int(item + zItem_timer) + 1,
        ))

    return items

# Ten Desires only
def extract_spirit_items():
    spirit_items = []
    spirit_array_start = zSpiritManager + zSpiritManager_array
    spirit_array_end   = spirit_array_start + zSpiritManager_array_len * zSpiritItem_len

    for spirit_item in range(spirit_array_start, spirit_array_end, zSpiritItem_len):
        if read_int(spirit_item + zSpiritItem_state) != 0:
            spirit_items.append(SpiritItem(
                id          = spirit_item,
                state       = read_int(spirit_item),
                spirit_type = read_int(spirit_item + zSpiritItem_type),
                position    = (read_float(spirit_item + zSpiritItem_pos), read_float(spirit_item + zSpiritItem_pos + 0x4)),
                velocity    = (read_float(spirit_item + zSpiritItem_vel), read_float(spirit_item + zSpiritItem_vel + 0x4)),
                alive_timer = read_int(spirit_item + zSpiritItem_timer) + 1,
            ))

    return spirit_items

# Wily Beast & Weakest Creature only
def extract_animal_tokens():
    animal_tokens = []

    current_token_list = {"entry": 0, "next": read_int(zTokenManager + zTokenManager_list)}

    while current_token_list["next"]:
        current_token_list = read_zList(current_token_list["next"])
        zToken = current_token_list["entry"]
        token_flags = read_int(zToken + zToken_flags)

        animal_tokens.append(AnimalToken(
            id = zToken,
            type             = read_int(zToken + zToken_type),
            position         = (read_float(zToken + zToken_pos), read_float(zToken + zToken_pos + 0x4)),
            base_velocity    = (read_float(zToken + zToken_base_vel), read_float(zToken + zToken_base_vel + 0x4)),
            being_grabbed    = token_flags & 2**0 != 0,
            can_switch       = token_flags & 2**1 != 0,
            slowed_by_player = token_flags & 2**2 != 0,
            switch_timer     = read_int(zToken + zToken_switch_timer),
            alive_timer      = read_int(zToken + zToken_alive_timer),
        ))

    return animal_tokens

def extract_lasers(laser_manager = zLaserManager):
    lasers = []
    current_laser_ptr = read_int(laser_manager + zLaserManager_list) #pointer to head laser 

    #UDoALG uses a ZUNlist for lasers with a dummy head node (skipped here) and no dummy tail node
    #prior games use ZUNlist-like pointers in lasers with a dummy tail laser (skipped here)
    next_laser_ptr = current_laser_ptr if game_id == 19 else read_int(current_laser_ptr + 0x4)
    while next_laser_ptr:

        if game_id == 19: #may need logic group if multiple games use ZUNlists for lasers
            current_laser_ptr = read_int(next_laser_ptr)

        laser_state = read_int(current_laser_ptr + zLaserBaseClass_state)
        laser_type  = read_int(current_laser_ptr + zLaserBaseClass_type)

        laser_base = {
            'id':          current_laser_ptr,
            'state':       laser_state,
            'laser_type':  laser_type,
            'alive_timer': read_int(current_laser_ptr + zLaserBaseClass_timer),
            'position':   (read_float(current_laser_ptr + zLaserBaseClass_offset), read_float(current_laser_ptr + zLaserBaseClass_offset + 0x4)),
            'angle':       read_float(current_laser_ptr + zLaserBaseClass_angle),
            'length':      read_float(current_laser_ptr + zLaserBaseClass_length),
            'width':       read_float(current_laser_ptr + zLaserBaseClass_width),
            'speed':       read_float(current_laser_ptr + zLaserBaseClass_speed),
            'iframes':     read_int(current_laser_ptr + zLaserBaseClass_iframes),
            'sprite':      read_int(current_laser_ptr + zLaserBaseClass_sprite),
            'color':       read_int(current_laser_ptr + zLaserBaseClass_color),
        }

        if laser_type == 0: #LINE
            lasers.append(LineLaser(
                **laser_base,
                **extract_line_laser(current_laser_ptr)
            ))

        elif laser_type == 1: #INFINITE
            lasers.append(InfiniteLaser(
                **laser_base,
                **extract_infinite_laser(current_laser_ptr)
            ))

        elif laser_type == 2: #CURVE
            lasers.append(CurveLaser(
                **laser_base,
                **extract_curve_laser(current_laser_ptr)
            ))

        elif laser_type == 3: #BEAM 
            lasers.append(Laser(**laser_base))

        current_laser_ptr = next_laser_ptr
        next_laser_ptr = read_int(current_laser_ptr + 0x4)

    return lasers

def extract_line_laser(laser_ptr):
    line_start_pos_x = read_float(laser_ptr + zLaserLine_start_pos)
    line_start_pos_y = read_float(laser_ptr + zLaserLine_start_pos + 0x4)
    line_init_angle  = read_float(laser_ptr + zLaserLine_mgr_angle)
    line_max_length  = read_float(laser_ptr + zLaserLine_max_length)
    line_init_speed  = read_float(laser_ptr + zLaserLine_mgr_speed)
    line_distance    = read_float(laser_ptr + zLaserLine_distance)

    return {
        'start_pos': (line_start_pos_x, line_start_pos_y),
        'init_angle': line_init_angle,
        'max_length': line_max_length,
        'init_speed': line_init_speed, 
        'distance': line_distance,
    }

def extract_infinite_laser(laser_ptr):
    infinite_start_pos_x   = read_float(laser_ptr + zLaserInfinite_start_pos)
    infinite_start_pos_y   = read_float(laser_ptr + zLaserInfinite_start_pos + 0x4)
    infinite_origin_vel_x  = read_float(laser_ptr + zLaserInfinite_velocity)
    infinite_origin_vel_y  = read_float(laser_ptr + zLaserInfinite_velocity + 0x4)
    infinite_default_angle = read_float(laser_ptr + zLaserInfinite_mgr_angle)
    infinite_angular_vel   = read_float(laser_ptr + zLaserInfinite_angle_vel)
    infinite_init_length   = read_float(laser_ptr + zLaserInfinite_mgr_len)
    infinite_max_length    = read_float(laser_ptr + zLaserInfinite_final_len)
    infinite_max_width     = read_float(laser_ptr + zLaserInfinite_final_width)
    infinite_default_speed = read_float(laser_ptr + zLaserInfinite_mgr_speed)
    infinite_start_time    = read_int(laser_ptr + zLaserInfinite_start_time)
    infinite_expand_time   = read_int(laser_ptr + zLaserInfinite_expand_time)
    infinite_active_time   = read_int(laser_ptr + zLaserInfinite_active_time)
    infinite_shrink_time   = read_int(laser_ptr + zLaserInfinite_shrink_time)
    infinite_distance      = read_float(laser_ptr + zLaserInfinite_mgr_distance)

    return {
        'start_pos': (infinite_start_pos_x, infinite_start_pos_y),
        'origin_vel': (infinite_origin_vel_x, infinite_origin_vel_y),
        'default_angle': infinite_default_angle,
        'angular_vel': infinite_angular_vel,
        'init_length': infinite_init_length,
        'max_length': infinite_max_length,
        'max_width': infinite_max_width,
        'default_speed': infinite_default_speed,
        'start_time': infinite_start_time,
        'expand_time': infinite_expand_time,
        'active_time': infinite_active_time,
        'shrink_time': infinite_shrink_time,
        'distance': infinite_distance,
    }

def extract_curve_laser(laser_ptr):
    curve_max_length  = read_int(laser_ptr + zLaserCurve_max_length)
    curve_distance    = read_float(laser_ptr + zLaserCurve_distance)

    curve_nodes = []
    current_node_ptr = read_int(laser_ptr + zLaserCurve_array)
    for i in range(0, curve_max_length):
        node_pos_x = read_float(current_node_ptr + zLaserCurveNode_pos)
        node_pos_y = read_float(current_node_ptr + zLaserCurveNode_pos + 0x4)
        node_vel_x = None
        node_vel_y = None
        node_angle = None
        node_speed = None

        if i == 0 or False: #(bool literal marks a removed setting; useless data for non-head nodes afaik)
            node_angle = read_float(current_node_ptr + zLaserCurveNode_angle)
            node_speed = read_float(current_node_ptr + zLaserCurveNode_speed)
            node_vel_x = read_float(current_node_ptr + zLaserCurveNode_vel)
            node_vel_y = read_float(current_node_ptr + zLaserCurveNode_vel + 0x4)

        curve_nodes.append(CurveNode(
            id = current_node_ptr,
            position = (node_pos_x, node_pos_y),
            velocity = (node_vel_x, node_vel_y),
            angle = node_angle,
            speed = node_speed,
        ))

        current_node_ptr += zLaserCurveNode_size

    return {
        'max_length': curve_max_length,
        'distance': curve_distance,
        'nodes': curve_nodes,
    }

def find_anm_vm_by_id(anm_id, list_offset=zAnmManager_list):
    current_anm_vm_list = {"entry": 0, "next": read_int(zAnmManager + list_offset)}

    while current_anm_vm_list['next']:
        current_anm_vm_list = read_zList(current_anm_vm_list['next'])
        zAnmVm = current_anm_vm_list['entry']

        if read_int(zAnmVm + zAnmVm_id) == anm_id:
            return zAnmVm

def extract_player_option_positions(player = zPlayer):
    player_option_positions = []
    player_option_array_start = player + zPlayer_option_array
    player_option_array_end   = player_option_array_start + zPlayer_option_array_len * zPlayerOption_len

    for player_option in range(player_option_array_start, player_option_array_end, zPlayerOption_len):
        if read_int(player_option + zPlayerOption_active) != 0:
            option_vm = None

            if player != zPlayer:
                option_vm = find_anm_vm_by_id(read_int(player_option + zPlayerOption_anm_id), zAnmManager_list_p2)
            else:
                option_vm = find_anm_vm_by_id(read_int(player_option + zPlayerOption_anm_id))

            if option_vm:
                player_option_positions.append((read_float(option_vm + zAnmVm_entity_pos), read_float(option_vm + zAnmVm_entity_pos + 0x4)))

    return player_option_positions

def extract_player_shots(player = zPlayer):
    player_shots = []
    player_shot_array_start = player + zPlayer_shots_array
    player_shot_array_end   = player_shot_array_start + zPlayer_shots_array_len * zPlayerShot_len

    for player_shot in range(player_shot_array_start, player_shot_array_end, zPlayerShot_len):
        if read_int(player_shot + zPlayerShot_state) == 1: #0 = inactive, 1 = active, 2 = destroy anim

            player_shots.append(PlayerShot(
                id          = player_shot,
                position    = (read_float(player_shot + zPlayerShot_pos),    read_float(player_shot + zPlayerShot_pos + 0x4)),
                velocity    = (read_float(player_shot + zPlayerShot_vel),    read_float(player_shot + zPlayerShot_vel + 0x4)),
                hitbox      = (read_float(player_shot + zPlayerShot_hitbox), read_float(player_shot + zPlayerShot_hitbox + 0x4)),
                speed       = read_float(player_shot + zPlayerShot_speed),
                angle       = read_float(player_shot + zPlayerShot_angle),
                damage      = read_int(player_shot + zPlayerShot_damage),
                alive_timer = read_int(player_shot + zPlayerShot_timer) + 1,
            ))

    return player_shots

def extract_spellcard(spellcard = zSpellCard):
    if read_int(spellcard + zSpellcard_indicator) == 0:
        return None

    spell_id = read_int(spellcard + zSpellcard_id)
    spell_capture_bonus = read_int(spellcard + zSpellcard_bonus, signed=True)

    return Spellcard(
        spell_id = spell_id,
        capture_bonus = spell_capture_bonus,
    )

def extract_game_state(frame_id = 0, real_time = 0):
    if game_id == 13:
        game_constants.life_piece_req = life_piece_reqs[read_int(extend_count, rel=True)]
    elif game_id == 18:
        game_constants.deathbomb_window_frames = read_int(zPlayer + zPlayer_deathbomb_window)
        game_constants.poc_line_height = read_int(zPlayer + zPlayer_poc_line_height)

    state_base = {
        'frame_stage':        read_int(stage_timer),
        'frame_global':       read_int(global_timer),
        'stage_chapter':      read_int(stage_chapter, rel=True),
        'seq_frame_id':       frame_id,
        'seq_real_time':      real_time,
        'boss_timer_shown':   None, #need to extract enemies
        'boss_timer_real':    None, #need to extract enemies
        'pause_state':        read_int(pause_state, rel=True),
        'game_mode':          read_int(game_mode, rel=True),
        'game_speed':         read_float(game_speed, rel=True),
        'score':              read_int(score, rel=True) * 10,
        'lives':              read_int(lives, rel=True, signed=True),
        'life_pieces':        read_int(life_pieces, rel=True) if life_pieces else 0,
        'bombs':              read_int(bombs, rel=True),
        'bomb_pieces':        read_int(bomb_pieces, rel=True),
        'power':              read_int(power, rel=True),
        'piv':                int(read_int(piv, rel=True) / 100),
        'graze':              read_int(graze, rel=True),
        'spellcard':          extract_spellcard(),
        'rank':               read_int(rank, rel=True),
        'input':              read_int(input, rel=True),
        'rng':                read_int(replay_rng, rel=True),
        'continues':          read_int(continues, rel=True),
        'player_position':    (read_float(zPlayer + zPlayer_pos), read_float(zPlayer + zPlayer_pos + 0x4)),
        'player_hitbox_rad':  read_float(zPlayer + zPlayer_hit_rad),
        'player_iframes':     read_int(zPlayer + zPlayer_iframes),
        'player_focused':     read_int(zPlayer + zPlayer_focused) == 1,
        'player_options_pos': extract_player_option_positions(),
        'player_shots':       extract_player_shots() if requires_player_shots else [],
        'player_deathbomb_f': max(0, game_constants.deathbomb_window_frames - read_int(zPlayer + zPlayer_db_timer)) if read_int(zPlayer + zPlayer_state) == 4 else 0,
        'bomb_state':         read_int(zBomb + zBomb_state),
        'bullets':            extract_bullets() if requires_bullets else [],
        'enemies':            extract_enemies() if requires_enemies else [],
        'items':              extract_items() if requires_items else [],
        'lasers':             extract_lasers() if requires_lasers else [],
        'screen':             get_rgb_screenshot() if requires_screenshots else None,
        'constants':          game_constants,
        'env':                run_environment,
    }

    boss_timer = get_boss_timer(state_base['enemies'])
    if boss_timer:
        state_base['boss_timer_real'] = boss_timer
        state_base['boss_timer_shown'] = min(99.99, round_down(boss_timer, 2))

    if game_id == 13:
        kyouko = None
        echo_func = 0x0
        for kyouko_echo_func in (square_echo_func, inv_square_echo_func, circle_echo_func):
            kyouko = find_special_enemy_addr(kyouko_echo_func)
            if kyouko:
                echo_func = kyouko_echo_func
                break

        kyouko_echo = None
        if kyouko:
            if echo_func == square_echo_func:
                kyouko_echo = RectangleEcho(
                    left_x   = read_float(kyouko + zEnemy_pos)       + read_float(kyouko + zEnemy_f0_echo_x1),
                    right_x  = read_float(kyouko + zEnemy_pos)       + read_float(kyouko + zEnemy_f1_echo_x2),
                    top_y    = read_float(kyouko + zEnemy_pos + 0x4) + read_float(kyouko + zEnemy_f2_echo_y1),
                    bottom_y = read_float(kyouko + zEnemy_pos + 0x4) + read_float(kyouko + zEnemy_f3_echo_y2),
                )

            elif echo_func == inv_square_echo_func:
                kyouko_echo = RectangleEcho(
                    left_x   = read_float(kyouko + zEnemy_f0_echo_x1),
                    right_x  = read_float(kyouko + zEnemy_f1_echo_x2),
                    top_y    = read_float(kyouko + zEnemy_f2_echo_y1),
                    bottom_y = read_float(kyouko + zEnemy_f3_echo_y2),
                )

            elif echo_func == circle_echo_func:
                kyouko_echo = CircleEcho(
                    position = (read_float(kyouko + zEnemy_f1_echo_x2), read_float(kyouko + zEnemy_f2_echo_y1)),
                    radius   = read_float(kyouko + zEnemy_f0_echo_x1),
                )

        return GameStateTD(
            **state_base,
            trance_active           = read_int(trance_state, rel=True) != 0,
            trance_meter            = read_int(trance_meter, rel=True),
            spawned_spirit_count    = read_int(zSpiritManager + zSpiritManager_spawn_total),
            chain_timer             = read_int(zSpiritManager + zSpiritManager_chain_timer),
            chain_counter           = read_int(zSpiritManager + zSpiritManager_chain_counter),
            spirit_items            = extract_spirit_items() if requires_items else [],
            kyouko_echo             = kyouko_echo,
            youmu_charge_timer      = read_int(zPlayer + zPlayer_youmu_charge_timer, signed=True),
            miko_final_logic_active = bool(find_special_enemy_addr(miko_final_func))
        )

    elif game_id == 14:
        return GameStateDDC(
            **state_base,
            bonus_count  = read_int(bonus_count, rel=True),
            player_scale = read_float(zPlayer + zPlayer_scale),
            seija_flip   = ((-read_float(ddcSeijaAnm + seija_flip_x) + 1)/2, (-read_float(ddcSeijaAnm + seija_flip_y) + 1)/2),
            sukuna_penult_logic_active = bool(find_special_enemy_addr(sukuna_penult_func)),
        )

    elif game_id == 15:
        return GameStateLoLK(
            **state_base,
            item_graze_slowdown_factor     = read_float(zItemManager + zItemManager_graze_slowdown_factor),
            reisen_bomb_shields            = read_int(zBomb + zBomb_reisen_shields),
            time_in_chapter                = read_int(time_in_chapter, rel=True),
            chapter_graze                  = read_int(chapter_graze, rel=True),
            chapter_enemy_weight_spawned   = read_int(chapter_enemy_weight_spawned, rel=True),
            chapter_enemy_weight_destroyed = read_int(chapter_enemy_weight_destroyed, rel=True),
            in_pointdevice                 = read_int(modeflags, rel=True) & 2**8 != 0,
            pointdevice_resets_total       = read_int(pointdevice_resets_total, rel=True),
            pointdevice_resets_chapter     = read_int(pointdevice_resets_chapter, rel=True),
            graze_inferno_logic_active     = bool(find_special_enemy_addr(graze_inferno_func))
        )

    elif game_id == 16:
        player_season_level = read_int(zPlayer + zPlayer_season_level)
        season_bomb_timer = read_int(zSeasomBomb + zBomb_timer, signed=True)

        return GameStateHSiFS(
            **state_base,
            next_extend_score = 10 * read_int((extend_scores_extra if difficulty == 4 else extend_scores_maingame) + read_int(next_extend_score_index, rel=True) * 0x4, rel=True),
            season_level = player_season_level,
            season_power = read_int(season_power, rel=True),
            next_level_season_power = read_int(season_power_thresholds + player_season_level * 0x4, rel=True),
            season_delay_post_use = -season_bomb_timer if season_bomb_timer < 0 else 0,
            release_active = read_int(zSeasomBomb + zBomb_state),
            season_disabled = bool(find_special_enemy_addr(season_disable_func)),
            snowman_logic_active = bool(find_special_enemy_addr(snowman_func)),
        )

    elif game_id == 17:
        held_tokens = []

        for token_slot in range(held_token_array, held_token_array + 0x14, 0x4):
            held_token = read_int(token_slot, rel=True)
            if held_token:
                held_tokens.append(held_token)

        hyper = None
        roaring_hyper_flags = read_int(hyper_flags, bytes = 1, rel=True)

        if roaring_hyper_flags & 2**1 != 0:
            cur_hyper_type = read_int(hyper_type, rel=True)
            otter_shield_angles = []

            if cur_hyper_type == 2:
                for otter_vm_i in range(3):
                    otter_vm = find_anm_vm_by_id(read_int(zTokenManager + zTokenManager_otter_anm_ids + otter_vm_i * 0x4))
                    if otter_vm:
                        otter_shield_angles.append(read_float(otter_vm + zAnmVm_rotation) - (math.pi/9)) #game does this subtraction

            hyper = RoaringHyper(
                type                   = read_int(hyper_type, rel=True),
                duration               = read_int(hyper_duration, rel=True),
                time_remaining         = read_int(hyper_time_remaining, rel=True),
                reward_mode            = roaring_hyper_flags >> 4,
                token_grab_time_bonus  = read_int(hyper_token_time_bonus, rel=True),
                otter_shield_angles    = otter_shield_angles,
                currently_breaking     = roaring_hyper_flags & 2**2 != 0,
            )

        return GameStateWBaWC(
            **state_base,
            held_tokens                   = held_tokens,
            field_tokens                  = extract_animal_tokens() if requires_items else [],
            roaring_hyper                 = hyper,
            extra_token_spawn_delay_timer = read_int(hyper_token_spawn_delay, rel=True),
            youmu_charge_timer            = read_int(zPlayer + zPlayer_youmu_charge_timer, signed=True),
            yacchie_recent_graze          = sum(read_int(zBulletManager + zBulletManager_recent_graze_gains + 0x4 * i) for i in range(20)),
        )

    elif game_id == 18:
        selected_active = read_int(zAbilityManager + zAbilityManager_selected_active)
        lily_counter = None
        centipede_multiplier = None
        active_cards = []

        current_active_list = read_zList(zAbilityManager + zAbilityManager_list)

        while current_active_list["next"]:
            current_active_list = read_zList(current_active_list["next"])

            zCard                  = current_active_list["entry"]
            card_type              = read_int(zCard + zCard_type)
            card_charge_max        = read_int(zCard + zCard_charge_max) #the first 20% of the cooldown time is always skipped
            card_charge            = card_charge_max - read_int(zCard + zCard_charge) #game counts down rather than up, but up is more intuitive

            if card_type == 48: #Lily
                lily_counter = read_int(zCard + zCard_counter)

            if card_type not in card_nicknames.keys():
                if card_type == 54: #Centipede
                    centipede_multiplier = 1 + 0.00005 * min(16000, read_int(zCard + zCard_counter))

                continue #skip non-actives

            active_cards.append(ActiveCard(
                type          = card_type,
                charge        = card_charge, 
                charge_max    = card_charge_max,
                internal_name = read_string(read_int(read_int(zCard + zCard_name_ptr_ptr)), 15),
                selected      = zCard == selected_active,
                in_use        = read_int(zCard + zCard_flags) & 2**5 != 0,
            ))

        return GameStateUM(
            **state_base,
            funds                = read_int(funds, rel=True),
            total_cards          = read_int(zAbilityManager + zAbilityManager_total_cards),
            total_actives        = read_int(zAbilityManager + zAbilityManager_total_actives),
            total_equipmt        = read_int(zAbilityManager + zAbilityManager_total_equipmt),
            total_passive        = read_int(zAbilityManager + zAbilityManager_total_passive),
            cancel_counter       = read_int(zBulletManager + zBulletManager_cancel_counter),
            lily_counter         = lily_counter,
            centipede_multiplier = centipede_multiplier,
            active_cards         = active_cards,
            asylum_logic_active  = bool(find_special_enemy_addr(asylum_func)),
            sakuya_knives_angle  = -read_float(zPlayer + zPlayer_sakuya_knives_angle),
            sakuya_knives_spread = read_float(zPlayer + zPlayer_sakuya_knives_spread),
        )

    elif game_id == 19:
        side2 = None

        #technically side2, but important singleplayer info so stored at the root of the state
        story_fight_phase, story_progress_meter = None, None
        if zAiP2:
            zStoryAi = read_int(zAiP2 + zAi_story_mode_pointer)
            if zStoryAi:
                story_fight_phase = read_int(zStoryAi + zStoryAi_fight_phase)
                story_progress_meter = read_int(zStoryAi + zStoryAi_progress_meter)

        if requires_side2_pvp:
            side2 = P2Side(
                lives               = read_int(p2_lives, rel=True),
                lives_max           = read_int(p2_lives_max, rel=True),
                bombs               = read_int(p2_bombs, rel=True),
                bomb_pieces         = read_int(p2_bomb_pieces, rel=True),
                power               = read_int(p2_power, rel=True),
                graze               = read_int(p2_graze, rel=True),
                boss_timer_shown    = None, #need to extract enemies
                boss_timer_real     = None, #need to extract enemies
                spellcard           = extract_spellcard(zSpellCardP2),
                input               = read_int(p2_input, rel=True),
                player_position     = (read_float(zPlayerP2 + zPlayer_pos), read_float(zPlayerP2 + zPlayer_pos + 0x4)),
                player_hitbox_rad   = read_float(zPlayerP2 + zPlayer_hit_rad),
                player_iframes      = read_int(zPlayerP2 + zPlayer_iframes),
                player_focused      = read_int(zPlayerP2 + zPlayer_focused) == 1,
                player_options_pos  = extract_player_option_positions(zPlayerP2),
                player_shots        = extract_player_shots(zPlayerP2) if requires_player_shots else [],
                player_deathbomb_f  = max(0, game_constants.deathbomb_window_frames - read_int(zPlayerP2 + zPlayer_db_timer)) if read_int(zPlayerP2 + zPlayer_state) == 4 else 0,
                bomb_state          = read_int(zBombP2 + zBomb_state),
                bullets             = extract_bullets(zBulletManagerP2) if requires_bullets else [],
                enemies             = extract_enemies(zEnemyManagerP2) if requires_enemies else [],
                items               = extract_items(zItemManagerP2) if requires_items else [],
                lasers              = extract_lasers(zLaserManagerP2) if requires_lasers else [],
                hitstun_status      = read_int(zPlayerP2 + zPlayer_hitstun_status),
                shield_status       = read_int(zPlayerP2 + zPlayer_shield_status),
                last_combo_hits     = read_int(zPlayerP2 + zPlayer_last_combo_hits),
                current_combo_hits  = read_int(zPlayerP2 + zPlayer_current_combo_hits),
                current_combo_chain = read_int(zPlayerP2 + zPlayer_current_combo_chain),
                enemy_pattern_count = read_int(zEnemyManagerP2 + zEnemyManager_pattern_count),
                item_spawn_total    = read_int(zItemManagerP2 + zItemManager_spawn_total),
                gauge_charging      = read_int(zGaugeManagerP2 + zGaugeManager_charging_bool) == 1,
                gauge_charge        = read_int(zGaugeManagerP2 + zGaugeManager_gauge_charge),
                gauge_fill          = read_int(zGaugeManagerP2 + zGaugeManager_gauge_fill),
                ex_attack_level     = read_int(p2_ex_attack_level, rel=True),
                boss_attack_level   = read_int(p2_boss_attack_level, rel=True),
                pvp_wins            = read_int(p2_pvp_wins, rel=True),
                env                 = p2_run_environment,
            )

            boss_timer_p2 = get_boss_timer(side2.enemies)
            if boss_timer_p2:
                side2.boss_timer_real = boss_timer_p2
                side2.boss_timer_shown = min(99.99, round_down(boss_timer_p2, 2))

        return GameStateUDoALG(
            **state_base,
            lives_max            = read_int(lives_max, rel=True),
            hitstun_status       = read_int(zPlayer + zPlayer_hitstun_status),
            shield_status        = read_int(zPlayer + zPlayer_shield_status),
            last_combo_hits      = read_int(zPlayer + zPlayer_last_combo_hits),
            current_combo_hits   = read_int(zPlayer + zPlayer_current_combo_hits),
            current_combo_chain  = read_int(zPlayer + zPlayer_current_combo_chain),
            enemy_pattern_count  = read_int(zEnemyManager + zEnemyManager_pattern_count),
            item_spawn_total     = read_int(zItemManager + zItemManager_spawn_total),
            gauge_charging       = read_int(zGaugeManager + zGaugeManager_charging_bool) == 1,
            gauge_charge         = read_int(zGaugeManager + zGaugeManager_gauge_charge),
            gauge_fill           = read_int(zGaugeManager + zGaugeManager_gauge_fill),
            ex_attack_level      = read_int(ex_attack_level, rel=True),
            boss_attack_level    = read_int(boss_attack_level, rel=True),
            pvp_timer_start      = read_int(pvp_timer_start, rel=True),
            pvp_timer            = read_int(pvp_timer, rel=True),
            pvp_wins             = read_int(pvp_wins, rel=True),
            story_fight_phase    = story_fight_phase,
            story_progress_meter = story_progress_meter,
            side2                = side2,
        )

def print_game_state(gs: GameState):
    #======================================
    # Consistent prints ===================
    bar = bright(color("|", 'green'))

    shottype = characters[gs.env.character] + ('' if subshots[gs.env.subshot] == 'N/A' else "-" + subshots[gs.env.subshot])
    print(bright(f"[Global Frame #{gs.frame_global} | Stage Frame #{gs.frame_stage} | {shottype} {difficulties[gs.env.difficulty]} Stage {gs.env.stage}] Score:"), f"{gs.score:,}")

    # Player status
    print(bar, bright("Player status:" ), f"Player at ({round(gs.player_position[0], 2)}, {round(gs.player_position[1], 2)}); hitbox radius {gs.player_hitbox_rad}; {gs.player_iframes} iframes; {'un' if not gs.player_focused else ''}focused movement")

    # Basic resources
    basic_resources = bar + bright(" Resources: ") + f"{gs.lives} lives"
    if gs.constants.life_piece_req != None:
        basic_resources += f" ({gs.life_pieces}/{gs.constants.life_piece_req} pieces)"
    basic_resources += f"; {gs.bombs} bombs"
    if gs.constants.bomb_piece_req != None:
        basic_resources += f" ({gs.bomb_pieces}/{gs.constants.bomb_piece_req} pieces)"
    print(basic_resources + f"; {gs.power/100:.2f} power; {gs.piv:,} PIV; {gs.graze:,} graze")

    # Useful internals
    print(bar, bright("Game state:" ), f"{pause_states[gs.pause_state]} ({game_modes[gs.game_mode]})")
    print(bar, bright("Input bitflag:" ), f"{gs.input:08b}")
    print(bar, bright("RNG value:" ), f"{gs.rng}")

    if game_id in uses_rank:
        print(bar, bright("Rank value:" ), f"{gs.rank}")

    #======================================
    # Situational prints ==================
    bar = bright(color("|", 'cyan'))

    if gs.boss_timer_shown:
        print(bar, bright("Boss timer:" ), f"{gs.boss_timer_shown:.2f}", darker(f"({round(gs.boss_timer_real, 3)}s)") if round(gs.boss_timer_real, 3) != gs.boss_timer_shown else '')

    if gs.spellcard:
        print(bar, bright(f"Spell #{gs.spellcard.spell_id+1}; SCB:"), f"{gs.spellcard.capture_bonus:,}" if gs.spellcard.capture_bonus > 0 else 'Failed')

    if gs.game_speed != 1:
        print(bar, bright("Game speed:" ), f"{gs.game_speed}x")

    if gs.player_deathbomb_f:
        print(bar, bright("Deathbomb window:" ), f"{gs.player_deathbomb_f} frames left")

    if gs.bomb_state:
        print(bar, bright("Bomb active" ), f"(state: {gs.bomb_state})")

    #======================================
    # Game-specific prints ================
    bar = color("|", 'yellow')

    if game_id == 13: #TD
        print(bar, f"TD Trance Meter: {round(gs.trance_meter/200, 2)} / 3.0")

        if gs.trance_active:
            print(bar, f"TD Active Trance: {gs.trance_meter/60:.2f}s")

        if gs.chain_counter:
            print(bar, f"TD Chain {'Active' if gs.chain_counter > 9 else 'Starting (no greys)'}: {gs.chain_counter} blues spawned; {gs.chain_timer}f left")

        if gs.miko_final_logic_active:
            print(bar, "TD Miko Final: Orbs will stop and aim towards player if player distance <= 48")

        if gs.spirit_items:
            counter = 0

            print(bright(underline("\nList of spirit items:")))
            print(bright("  Type       Position         Velocity         Frames Left"))
            for spirit in gs.spirit_items:
                description = bp + " "
                description += tabulate(spirit_types[spirit.spirit_type], 11)
                description += tabulate(f"({round(spirit.position[0], 1)}, {round(spirit.position[1], 1)})", 17)
                description += tabulate(f"({round(spirit.velocity[0], 1)}, {round(spirit.velocity[1], 1)})", 17)
                description += tabulate(523 - spirit.alive_timer, 12)

                if spirit.state == 2:
                    description += " (Attracted)"
                elif spirit.state == 4:
                    description += " (Auto-collecting)"

                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(gs.spirit_items)} spirit item total]'))
                    break

    elif game_id == 14: #DDC
        bonus_cycle_desc = ""
        if gs.bonus_count % 5 == 4:
            bonus_cycle_desc = " (life piece for next bonus < 2.0)"
        else:
            bonus_cycle_desc = " (bomb piece for next bonus < 2.0)"
        print(bar, f"DDC Bonus Cycle: {gs.bonus_count%5}{bonus_cycle_desc}")

        if gs.seija_flip[0]:
            print(bar, f"DDC Seija Horizontal Flip: {round(100*gs.seija_flip[0], 2)}%")

        if gs.seija_flip[1]:
            print(bar, f"DDC Seija Vertical Flip: {round(100*gs.seija_flip[1], 2)}%")

        if gs.player_scale > 1:
            print(bar, f"DDC Player Scale: grew {round(gs.player_scale, 2)}x bigger! (hitbox radius: {round(gs.player_hitbox_rad * gs.player_scale, 2)})")

        if gs.sukuna_penult_logic_active:
            print(bar, "DDC Sukuna Penult: Orbs will start homing if player distance < 64, will stop when player distance >= 128")

    elif game_id == 15: #LoLK
        chapter = "Chapter"
        if gs.stage_chapter:
            chapter = f"S{read_int(stage, rel=True)}C{gs.stage_chapter+1}"

        chapter_desc = f"{gs.chapter_graze} graze; "
        chapter_desc += f"shootdown {gs.chapter_enemy_weight_destroyed}/{gs.chapter_enemy_weight_spawned}"
        if gs.chapter_enemy_weight_spawned > 0:
            chapter_desc += f" ({round(100*gs.chapter_enemy_weight_destroyed/gs.chapter_enemy_weight_spawned,1)}%)"
        chapter_desc += f"; frame #{gs.time_in_chapter}"
        print(bar, f"LoLK {chapter}: {chapter_desc}")

        if gs.in_pointdevice:
            print(bar, f"LoLK Pointdevice: {gs.pointdevice_resets_chapter} chapter resets / {gs.pointdevice_resets_total} total resets")

        if gs.item_graze_slowdown_factor < 1:
            print(bar, f"LoLK Item Graze Slowdown: {round(gs.item_graze_slowdown_factor,1)}x")

        if gs.reisen_bomb_shields > 0:
            print(bar, f"LoLK Reisen Bomb Shields: {gs.reisen_bomb_shields}")

        if gs.graze_inferno_logic_active:
            print(bar, f"LoLK Graze Inferno: Fireballs will slow down when player distance <= {math.sqrt(1800):.3f}")

    elif game_id == 16: #HSiFS
        print(bar, f"HSiFS Next Score Extend Threshold: {gs.next_extend_score:,}")

        if gs.season_disabled:
            print(bar, f"HSiFS Season Gauge: Disabled by Okina final")

        else:
            remaining_charge_desc = ""
            if gs.next_level_season_power - gs.season_power:
                remaining_charge_desc = f" for level {gs.season_level+1}"

            releasability_desc = " (can't release)"
            if gs.season_level and not gs.bomb_state and not gs.release_active:
                if gs.season_delay_post_use:
                    releasability_desc = f" (can release in {gs.season_delay_post_use}f)"
                else:
                    releasability_desc = " (can release)"

            print(bar, f"HSiFS Season Gauge: level {gs.season_level}, {gs.season_power}/{gs.next_level_season_power} season items{remaining_charge_desc}{releasability_desc}")

    elif game_id == 17: #WBaWC
        if gs.held_tokens:
            token_stock = ""
            for held_token in gs.held_tokens:
                if token_stock:
                    token_stock += ", "
                token_stock += token_types[held_token-1]
            print(bar, f"WBaWC Held Tokens ({len(gs.held_tokens)}/5): {token_stock}")

        if gs.roaring_hyper:
            hyper = gs.roaring_hyper
            hyper_extend_desc = f"(+{hyper.token_grab_time_bonus}f for grabbing a token)" if not hyper.currently_breaking else "(broken)"
            print(bar, f"WBaWC {hyper_types[hyper.type]} Hyper Timer: {hyper.time_remaining}f / {hyper.duration}f {hyper_extend_desc}")

            hyper_rewards_desc = "1 Life Piece, 4 Random Animals"
            if hyper.reward_mode == 0:
                hyper_rewards_desc = "2 Random Animals"
            elif hyper.reward_mode == 2:
                hyper_rewards_desc = "1 Bomb Piece, 1 Life Piece, 3 Random Animals"
            elif hyper.reward_mode == 3:
                hyper_rewards_desc = "2 Bomb Piece, 1 Life Piece, 1 Power Item, 1 Point Item"

            if not hyper.currently_breaking:
                print(bar, f"WBaWC {hyper_types[hyper.type]} Hyper Token Rewards: {hyper_rewards_desc}")

            if hyper.type == 2:
                print(bar, f"WBaWC Otter Hyper Shield Angles: {round(hyper.otter_shield_angles[0], 3)}, {round(hyper.otter_shield_angles[1], 3)}, {round(hyper.otter_shield_angles[2], 3)}")

        if gs.youmu_charge_timer:
            print(bar, f"WBaWC Youmu Charge Timer: {gs.youmu_charge_timer}f / 60f")

        if gs.field_tokens:
            counter = 0

            print(bright(underline("\nList of animal tokens:")))
            print(bright("  Position         Base Velocity    Type        Timer"))
            for token in gs.field_tokens:
                description = bp + " "
                description += tabulate(f"({round(token.position[0], 1)}, {round(token.position[1], 1)})", 17)
                description += tabulate(f"({round(token.base_velocity[0], 1)}, {round(token.base_velocity[1], 1)})", 17)
                description += tabulate(token_types[token.type-1], 12)
                description += tabulate(f"{token.alive_timer}", 11)

                if token.alive_timer >= 7800:
                    description += f" (can leave{' in ' + str(8400 - token.alive_timer) + 'f' if token.alive_timer < 8400 else '!'})"

                if token.being_grabbed:
                    description += " (being grabbed)"
                elif token.slowed_by_player:
                    description += " (slowed by player)"

                if token.can_switch:
                    description += f" (switches in {token.switch_timer}f)"

                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(gs.field_tokens)} animal tokens total]'))
                    break

    elif game_id == 18: #UM
        print(bar, f"UM Funds: {gs.funds:,}")

        cards_breakdown = ""
        if gs.total_cards > 0:
            cards_breakdown += " ("
            if gs.total_actives > 0:
                cards_breakdown += f"{gs.total_actives} active"
            if gs.total_equipmt > 0:
                if cards_breakdown != " (":
                    cards_breakdown += ", "
                cards_breakdown += f"{gs.total_equipmt} equipment"
            if gs.total_passive > 0:
                if cards_breakdown != " (":
                    cards_breakdown += ", "
                cards_breakdown += f"{gs.total_passive} passive"
            cards_breakdown += ")"

        print(bar, f"UM Cards: {gs.total_cards}" + cards_breakdown)

        if gs.centipede_multiplier:
            print(bar, f"UM Centipede Multiplier: {gs.centipede_multiplier:.3f}x")

        if gs.lily_counter != None:
            print(bar, f"UM Lily Use Count: {gs.lily_counter} (" + ('next Lily drops Life Piece' if gs.lily_counter % 3 == 2 else 'next Lily drops Bomb Piece') + ")")

        if gs.asylum_logic_active:
            print(bar, "UM Asylum of Danmaku: Droplets will transform if player distance <= 128")

        if gs.active_cards:
            print(bright(underline("\nList of active cards:")))
            print(bright("  ID   Internal Name   Nickname    Charge / Max     %"))
            for card in gs.active_cards:
                description = bp + " "
                description += tabulate(card.type, 5)
                description += tabulate(card.internal_name, 16)
                description += tabulate(card_nicknames[card.type], 12)
                description += tabulate(card.charge, 6) + " / "
                description += tabulate(card.charge_max, 8)
                description += tabulate(f"{round(100*card.charge / card.charge_max, 2):.3g}%", 6)

                if card.selected:
                    description += " (selected)"
                if card.in_use:
                    description += " (in use)"

                print(description.strip())

    elif game_id == 19: #UDoALG
        print(bar, f"UDoALG Shield: {'Active' if gs.shield_status == 1 else 'Broken'}; Max Lives: {gs.lives_max}")
        print(bar, f"UDoALG Combo Hits: {gs.current_combo_hits}")
        print(bar, f"UDoALG Item Spawn Total: {gs.item_spawn_total}")

        thresholds = [gs.env.charge_attack_threshold, gs.env.charge_skill_threshold, gs.env.ex_attack_threshold, gs.env.boss_attack_threshold]
        names = ["attack", "skill", "ex", "boss"]
        charge_met = ""
        fill_met = ""

        for t in range(len(thresholds)):
            if gs.gauge_charge >= thresholds[t]:
                charge_met = names[t]
            if gs.gauge_fill >= thresholds[t]:
                fill_met += names[t] + ", "

        if charge_met:
            charge_met = f"(release will send {charge_met})"
        if fill_met:
            fill_met = f"(can send {fill_met.rstrip(', ')})"

        if gs.gauge_charging:
            print(bar, f"UDoALG Gauge Charge: {gs.gauge_charge} / {gs.gauge_fill} {charge_met}")

        print(bar, f"UDoALG Gauge Fill: {gs.gauge_fill} / 2500 {fill_met}")
        print(bar, f"UDoALG Gauge Thresholds: attack @ {thresholds[0]}, skill @ {thresholds[1]}, ex @ {thresholds[2]} (Lv{gs.ex_attack_level + 1}), boss @ {thresholds[3]} (Lv{gs.boss_attack_level + 1})")

        if gs.pvp_timer_start:
            print(bar, f"UDoALG PvP Timer: {round(gs.pvp_timer/60)} / {round(gs.pvp_timer_start/60)}")

        if gs.story_fight_phase != None and gs.story_progress_meter != None:
            print(bar, f"UDoALG Story Mode Fight Phase {gs.story_fight_phase} Progress Meter: {gs.story_progress_meter}")

        if gs.side2:
            print(bar, f"UDoALG P2 ({characters[gs.side2.env.character]}) side data included in state.")

    #======================================
    # Game entity prints (all optional) ===
    if gs.bullets and any(bullet.is_active for bullet in gs.bullets): #Bullets
        counter = 0

        print(bright(underline("\nList of bullets:")))
        print(bright("  Position         Velocity         Speed   Angle   Radius  Timer  Color        Type"))
        for bullet in gs.bullets:
            if not bullet.is_active:
                continue

            description = bp + " "
            description += tabulate(f"({round(bullet.position[0], 1)}, {round(bullet.position[1], 1)})", 17)
            description += tabulate(f"({round(bullet.velocity[0], 1)}, {round(bullet.velocity[1], 1)})", 17)
            description += tabulate(round(bullet.speed, 1), 8)
            description += tabulate(round(bullet.angle, 2), 8)
            description += tabulate(round(bullet.hitbox_radius, 1), 8)
            description += tabulate(bullet.alive_timer, 7)
            description += tabulate(get_color(bullet.type, bullet.color)[0], 13)

            #account for mono-color sprites
            bullet_type = bullet_types[bullet.type][0]
            if bullet_types[bullet.type][1] == 0:
                bullet_type = bullet_type.split(' ')[1]

            description += tabulate(bullet_type, 15)

            #not in table since rare
            if bullet.iframes > 0:
                description += f" ({bullet.iframes} iframes)"

            if hasattr(bullet, 'show_delay') and bullet.show_delay > 0:
                description += f" ({bullet.show_delay} invis. frames)"

            if hasattr(bullet, 'graze_timer') and bullet.graze_timer > 0:
                description += f" (grazed {bullet.graze_timer}f)"

            if bullet.scale != 1:
                description += f" (scale: {round(bullet.scale, 2)}x)"

            if hasattr(bullet, 'is_intangible') and bullet.is_intangible:
                description += f" (intangible)"

            print(description.strip())

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(bp, darker(f'... [{len(gs.bullets)} active bullets total]'))
                break

    if gs.lasers: #Lasers
        line_lasers = [laser for laser in gs.lasers if laser.laser_type == 0]
        infinite_lasers = [laser for laser in gs.lasers if laser.laser_type == 1]
        curve_lasers = [laser for laser in gs.lasers if laser.laser_type == 2]
        beam_lasers = [laser for laser in gs.lasers if laser.laser_type == 3]

        if line_lasers:
            counter = 0

            print(bright(underline("\nList of segment (\"line\") lasers:")))
            print(bright("  Tail Position    Speed   Angle   Length / Max     Width   Color   Sprite"))
            for laser in line_lasers:
                description = bp + " "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(round(laser.speed, 1), 8)
                description += tabulate(round(laser.angle, 2), 8)
                description += tabulate(round(laser.length, 1), 6) + " / "
                description += tabulate(round(laser.max_length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(bullet_types[laser.sprite][0], 8)
                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(line_lasers)} line lasers total]'))
                    break

        if infinite_lasers:
            counter = 0

            print(bright(underline("\nList of telegraphed (\"infinite\") lasers:")))
            print(bright("  Origin Position  Origin Velocity  Angle (Vel)    Length (%)    Width (%)     Color   State (#frames left)"))
            for laser in infinite_lasers:
                description = bp + " "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(f"({round(laser.origin_vel[0], 1)}, {round(laser.origin_vel[1], 1)})", 17)
                description += tabulate(round(laser.angle, 2), 6)
                description += tabulate(f"({format(laser.angular_vel, '.3f').rstrip('0').rstrip('.')})", 9)
                description += tabulate(f"{round(laser.length, 1)} ({int(100*laser.length/laser.max_length)}%)", 14)
                description += tabulate(f"{round(laser.width, 1)} ({int(100*laser.width/laser.max_width)}%)", 14)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)

                if laser.state == 3:
                    description += f"Telegraph ({laser.start_time - laser.alive_timer}f)"
                elif laser.state == 4:
                    description += f"Expand ({laser.expand_time - laser.alive_timer}f)"
                elif laser.state == 2:
                    description += f"Active ({laser.active_time - laser.alive_timer}f)"
                elif laser.state == 5:
                    description += f"Shrink ({laser.shrink_time - laser.alive_timer}f)"
                else:
                    description += "Unknown"

                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(infinite_lasers)} telegraphed lasers total]'))
                    break

        if curve_lasers:
            counter = 0

            print(bright(underline("\nList of curvy lasers:")))
            print(bright("  Spawn Position  Head Position     Head Velocity   HSpeed  HAngle  #Nodes  Width   Color   Sprite"))
            for laser in curve_lasers:
                description = bp + " "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 16)
                description += tabulate(f"({round(laser.nodes[0].position[0], 1)}, {round(laser.nodes[0].position[1], 1)})", 18)
                description += tabulate(f"({round(laser.nodes[0].velocity[0], 1)}, {round(laser.nodes[0].velocity[1], 1)})", 16)
                description += tabulate(round(laser.nodes[0].speed, 1), 8)
                description += tabulate(round(laser.nodes[0].angle, 2), 8)
                description += tabulate(round(laser.max_length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_curve_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(curve_sprites[laser.sprite], 10)
                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(curve_lasers)} curvy lasers total]'))
                    break

        if beam_lasers:
            counter = 0

            print(bright(underline("\nList of beam lasers:")))
            print(darker("Note: Beam lasers are not fully supported; data may be inaccurate."))
            print(bright("  Position         Speed   Angle   Length  Width   Color   Sprite"))
            for laser in beam_lasers:
                description = bp + " "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(round(laser.speed, 1), 8)
                description += tabulate(round(laser.angle, 2), 8)
                description += tabulate(round(laser.length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(bullet_types[laser.sprite][0], 8)
                print(description.strip())

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(bp, darker(f'... [{len(beam_lasers)} beam lasers total]'))
                    break

    if gs.enemies: #Enemies
        counter = 0

        print(bright(underline("\nList of enemies:")))
        print(bright("  Position        Hurtbox         Hitbox          Timer  HP / Max HP     ECL Sub         Type"))
        for enemy in gs.enemies:
            is_bosslike = enemy.is_boss or enemy.anm_page == 0 or enemy.anm_page > 2

            description = bp + " "
            description += tabulate(f"({round(enemy.position[0], 1)}, {round(enemy.position[1], 1)})", 16)
            description += tabulate(f"({round(enemy.hurtbox[0], 1)}, {round(enemy.hurtbox[1], 1)})", 16)
            description += tabulate(f"({round(enemy.hitbox[0], 1)}, {round(enemy.hitbox[1], 1)})", 16)
            description += tabulate(enemy.ecl_sub_timer if is_bosslike else enemy.alive_timer, 7) #so enemies don't all have a 0 timer when thprac timelock is on
            description += tabulate(f"{enemy.health} / {enemy.health_max}", 16)
            description += truncate(enemy.ecl_sub_name, 14)

            type = ""
            if enemy.anm_page == 2:
                if enemy.anm_id in enemy_anms:
                    type = enemy_anms[enemy.anm_id]
                else:
                    type = f"Unknown #{enemy.anm_id}"
            elif is_bosslike:
                if enemy.is_boss:
                    if enemy.subboss_id == 0:
                        type = "Boss"
                    else:
                        type = f"Sub-boss #{enemy.subboss_id}"
                else:
                    type = "Boss-specific"
            else:
                type = f"Unknown {enemy.anm_page}/{enemy.anm_id}"
            description += truncate(type, 18, 1)

            #not in table since rare
            if enemy.no_hurtbox:
                description += " (Hurtbox Off)"
            if enemy.no_hitbox:
                description += " (Hitbox Off)"
            if enemy.invincible:
                description += " (Invincible)"
            if enemy.intangible:
                description += " (Intangible)"
            if enemy.is_grazeable:
                description += " (Grazeable)"
            if enemy.iframes:
                description += f" ({enemy.iframes} iframes)"
            if hasattr(enemy, 'shootdown_weight') and enemy.shootdown_weight != 1:
                description += f" ({enemy.shootdown_weight} weight)"

            description = description.strip()

            #note: boss drops are never properly set prior to the frame they're instructed to drop
            if singlext_settings['show_enemy_drops'] and enemy.drops and not enemy.is_boss:
                description += "\n  " + bp + " Drops: " + ", ".join(f"{enemy.drops[drop]} {item_types[drop]}" for drop in enemy.drops)
                if game_id == 13 and enemy.speedkill_cur_drop_amt:
                    description += f" (+ {enemy.speedkill_cur_drop_amt} Blue Spirit; will be {enemy.speedkill_cur_drop_amt-1} in {enemy.speedkill_time_left_for_amt}f)"

                elif game_id == 16 and enemy.drops[16] > enemy.speedkill_cur_drop_amt:
                    description += f" (reduced to {enemy.speedkill_cur_drop_amt} Season"
                    if enemy.speedkill_time_left_for_amt:
                        description += f"; will be {enemy.speedkill_cur_drop_amt-1} in {enemy.speedkill_time_left_for_amt}f"
                    description += ")"

            if singlext_settings['show_boss_thresholds'] and enemy.is_boss:
                max_sub_len = -2
                max_thresh_len = -3
                max_cur_len = -11
                if enemy.health_threshold and enemy.time_threshold:
                    max_sub_len = max(len(enemy.health_threshold[1]), len(enemy.time_threshold[1]))
                    max_thresh_len = max(len(str(enemy.health_threshold[0]))+3, len(str(enemy.time_threshold[0]))+1)
                    max_cur_len = max(len(str(enemy.health))+3, len(str(enemy.ecl_sub_timer))+1)

                if enemy.health_threshold:
                    description += f"\n  {bp} Boss Health Threshold: Sub "
                    description += tabulate(f"'{enemy.health_threshold[1]}'", max_sub_len + 2)
                    description += tabulate(f" @ {enemy.health_threshold[0]} HP", max_thresh_len + 3)
                    description += tabulate(f" (current: {enemy.health} HP", max_cur_len + 11)
                    description += f" → {(100*(enemy.health_max - enemy.health))//(enemy.health_max - enemy.health_threshold[0])}%)"

                if enemy.time_threshold:
                    description += f"\n  {bp} Boss Time Threshold:   Sub "
                    description += tabulate(f"'{enemy.time_threshold[1]}'", max_sub_len + 2)
                    description += tabulate(f" @ {enemy.time_threshold[0]}f", max_thresh_len + 3)
                    description += tabulate(f" (current: {enemy.ecl_sub_timer}f", max_cur_len + 11)
                    description += f" → {(100*enemy.ecl_sub_timer)//enemy.time_threshold[0]}%)"

            print(description)

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(bp, darker(f'... [{len(gs.enemies)} enemies total]'))
                break

    if gs.items: #Items
        counter = 0

        print(bright(underline("\nList of items:")))
        print(bright("  Position         Velocity         Timer   Type"))
        for item in gs.items:
            description = bp + " "
            description += tabulate(f"({round(item.position[0], 1)}, {round(item.position[1], 1)})", 17)
            description += tabulate(f"({round(item.velocity[0], 1)}, {round(item.velocity[1], 1)})", 17)
            description += tabulate(item.alive_timer, 8)
            description += tabulate(item_types[item.item_type], 14)

            if item.state == zItemState_autocollect:
                description += " (Auto-collecting)"
            elif item.state == zItemState_attracted:
                description += " (Attracted)"

            print(description.strip())

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(bp, darker(f'... [{len(gs.items)} items total]'))
                break

    if gs.player_shots and singlext_settings['show_player_shots']:
        counter = 0

        print(bright(underline("\nList of player shots:")))
        print(bright("  Position         Velocity         Hitbox          Speed   Angle   Damage  Timer"))
        for shot in gs.player_shots:
            description = bp + " "
            description += tabulate(f"({round(shot.position[0], 1)}, {round(shot.position[1], 1)})", 17)
            description += tabulate(f"({round(shot.velocity[0], 1)}, {round(shot.velocity[1], 1)})", 17)
            description += tabulate(f"({round(shot.hitbox[0], 1)}, {round(shot.hitbox[1], 1)})", 16)
            description += tabulate(round(shot.speed, 1), 8)
            description += tabulate(round(shot.angle, 2), 8)
            description += tabulate(shot.damage, 8)
            description += tabulate(shot.alive_timer, 8)

            print(description.strip())

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(bp, darker(f'... [{len(gs.player_shots)} shots total]'))
                break

def on_exit():
    if game_process.is_running:
        game_process.resume()
atexit.register(on_exit)

def parse_frame_count(expr):
    if not expr or expr[-1].lower() not in "fs":
        return None

    try:
        if expr[-1].lower() == "f": #frames
            return int(expr[:-1])
        else: #seconds
            return math.floor(float(expr[:-1]) * 60)

    except ValueError:
        return None

print(separator.replace('\n',''))


# Extraction parameters processing
# Get extraction params from settings.py
printed_warning = False
if seqext_settings['ingame_duration'].lower() in ['inf', 'infinite', 'endless', 'forever']:
    frame_duration = -1
else:
    frame_duration = parse_frame_count(seqext_settings['ingame_duration'])
#(analyzer & exact defined via import)

# Overwrite settings with supplied arguments
if len(sys.argv) > 4:
    print(color("Warning:", 'orange'), f"More arguments were supplied than exist settings for ({bright(len(sys.argv)-1)} > 3).")
    printed_warning = True

for arg in sys.argv[1:]:
    if arg.lower() == 'exact':
        exact = True
    elif arg.lower() == 'inexact':
        exact = False
    elif arg.lower() in ['inf', 'infinite', 'endless', 'forever']:
        frame_duration = -1
    elif parse_frame_count(arg.lower()):
        frame_duration = parse_frame_count(arg.lower())
    elif hasattr(analysis, arg):
        analyzer = arg
    else:
        print(color("Warning:", 'orange'), f"Unrecognized argument '{bright(arg)}'.")
        printed_warning = True

# Warn & use default value if using unparseable settings
if not frame_duration:
    if seqext_settings['ingame_duration']:
        print(color("Warning:", 'orange'), f"Couldn't parse duration '{bright(seqext_settings['ingame_duration'])}'; remember to include a unit (e.g. '150f', '12.4s', 'infinite', etc.).")
        print("         Defaulting to single-state extraction.")
        printed_warning = True
    frame_duration = 1

if not hasattr(analysis, analyzer):
    print(color("Warning:", 'orange'), f"Unrecognized analyzer '{bright(analyzer)}'; defaulting to template.")
    printed_warning = True
    analyzer = 'AnalysisTemplate'

if printed_warning:
    print()


# Single-State Extraction
if frame_duration in [0, 1]:
    analysis = getattr(analysis, analyzer)()

    if requires_screenshots:
        get_focus()

    state = extract_game_state()
    print_game_state(state)

    try:
        print(separator)
        set_status(f"Running {bright(analyzer)}...")
        status_start()
        analysis.step(state)
        analysis.done()

    except KeyboardInterrupt:
        print(f"{bright(analyzer)} interrupted by user.", clear())

    except Exception as e:
        status_stop()
        print(color(f"{analyzer} error:", 'red'), str(e), darker(), clear())
        traceback.print_exc()
        print(default())

    finally:
        status_stop()


# Sequence Extraction
else:
    if frame_duration < 0:
        print(f"Extracting until termination triggered by user or analyzer {bright(analyzer)}{' (exact mode)' if exact else ''}.")
    else:
        print(bright(f"Extracting for {frame_duration} frames{' (exact mode)' if exact else ''}."))

    if seqext_settings['auto_unpause']:
        unpause_game()
    elif seqext_settings['auto_focus']:
        get_focus()

    analysis = getattr(analysis, analyzer)()

    try:
        start_time = time.perf_counter()
        terminated = False
        frame_counter = 0

        status_start()
        while frame_duration < 0 or frame_counter < frame_duration:
            if terminated:
                break

            frame_timestamp = read_int(stage_timer)
            percent = ""
            if frame_duration > 0:
                percent = bright(f"[{int(100*frame_counter/frame_duration)}%] ")
            set_status(percent + f"Extracting from frame #{frame_counter+1} (in-stage: #{frame_timestamp})")

            if exact:
                game_process.suspend()

            current_time = time.perf_counter()
            state = extract_game_state(frame_counter, current_time - start_time)
            analysis.step(state)
            frame_counter += 1

            if exact:
                game_process.resume()

            #busy wait for new frame
            pause_time = 0
            while True: #(do...while, ensuring term conditions evaluated at least once)
                current_pause_state = read_int(pause_state, rel=True)
                term_return = eval_termination_conditions(current_pause_state, need_active)

                if term_return:
                    print(f"{term_return}; terminating now.", clear())
                    terminated = True
                    break

                if read_int(stage_timer) != frame_timestamp:
                    break
                elif current_pause_state == 0:
                    pause_time = time.perf_counter() - current_time
                    set_status(percent + "(Unpause the game to continue extraction)")
            start_time += pause_time

        if not terminated:
            print(f"{bright('[100%] ') if frame_duration > 0 else ''}Finished extraction in { round(time.perf_counter() - start_time, 2) } seconds.", clear())

    except KeyboardInterrupt:
        print("User interrupted extraction; terminating now.", clear())

    except Exception as e:
        status_stop()
        print(color("Error:", 'red'), str(e) + "; terminating now.", darker(), clear())
        traceback.print_exc()
        print(default())

    finally:
        game_process.resume()

    if seqext_settings['auto_repause']:
        pause_game()

    set_status(f"Running {bright(analyzer)}.done()...")
    print(separator, clear())

    try:
        analysis.done()
    except KeyboardInterrupt:
        print(f"{bright(analyzer)} interrupted by user.", clear())
    except Exception as e:
        status_stop()
        print(color(f"{analyzer} error:", 'red'), str(e), darker(), clear())
        traceback.print_exc()
        print(default())
    finally:
        status_stop()