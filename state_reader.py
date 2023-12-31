from settings import extraction_settings, singlext_settings, seqext_settings
from interface import *
from game_entities import *
import analysis_examples as analysis #(includes analysis.py analyzers)
import sys
import math
import time
import atexit

#For quick access
analyzer, requires_bullets, requires_enemies, requires_items, requires_lasers, requires_screenshots, requires_side2_pvp, only_game_world = extraction_settings.values()
exact = seqext_settings['exact']
need_active = seqext_settings['need_active']
infinite_print_updates = seqext_settings['infinite_print_updates']

zPlayer        = read_int(player_pointer, rel=True)
zBomb          = read_int(bomb_pointer, rel=True)
zBulletManager = read_int(bullet_manager_pointer, rel=True)
zEnemyManager  = read_int(enemy_manager_pointer, rel=True)
zItemManager   = read_int(item_manager_pointer, rel=True)
zLaserManager  = read_int(laser_manager_pointer, rel=True)
zSpellCard     = read_int(spellcard_pointer, rel=True)
zGui           = read_int(gui_pointer, rel=True)

if game_id == 13:
    zSpiritManager = read_int(spirit_manager_pointer, rel=True)

elif game_id == 14:
    ddcSeijaAnm = read_int(seija_anm_pointer, rel=True)

elif game_id == 19:
    zGaugeManager = read_int(gauge_manager_pointer, rel=True)

    if requires_side2_pvp:
        zPlayerP2         = read_int(p2_player_pointer, rel=True)
        zBombP2           = read_int(p2_bomb_pointer, rel=True)
        zBulletManagerP2  = read_int(p2_bullet_manager_pointer, rel=True)
        zEnemyManagerP2   = read_int(p2_enemy_manager_pointer, rel=True)
        zItemManagerP2    = read_int(p2_item_manager_pointer, rel=True)
        zLaserManagerP2   = read_int(p2_laser_manager_pointer, rel=True)
        zSpellCardP2      = read_int(p2_spellcard_pointer, rel=True)
        zGaugeManagerP2   = read_int(p2_gauge_manager_pointer, rel=True)
        zAbilityManagerP2 = read_int(p2_ability_manager_pointer, rel=True)

if game_id in has_ability_cards:
    zAbilityManager = read_int(ability_manager_pointer, rel=True)

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

        bullet = {
            'id':           zBullet,
            'position':     (read_float(zBullet + zBullet_pos), read_float(zBullet + zBullet_pos + 0x4)),
            'velocity':     (read_float(zBullet + zBullet_velocity), read_float(zBullet + zBullet_velocity + 0x4)),
            'speed':         read_float(zBullet + zBullet_speed),
            'angle':         read_float(zBullet + zBullet_angle),
            'scale':         read_float(zBullet + zBullet_scale) if zBullet_scale else 1,
            'hitbox_radius': read_float(zBullet + zBullet_hitbox_radius),
            'iframes':       read_int(zBullet + zBullet_iframes),
            'is_active':     read_int(zBullet + zBullet_state, 2) == 1,
            'bullet_type':   read_int(zBullet + zBullet_type, 2),
            'color':         read_int(zBullet + zBullet_color, 2),
        }

        #Game-specific attributes
        if game_id in has_bullet_delay:
            bullet['show_delay'] = read_int(zBullet + zBullet_ex_delay_timer)
            bullets.append(ShowDelayBullet(**bullet))

        elif game_id == 15:
            bullet['graze_timer'] = read_int(zBullet + zBullet_graze_timer)
            bullets.append(GrazeTimerBullet(**bullet))

        else:
            bullets.append(Bullet(**bullet))

    return bullets

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

    while current_enemy_list["next"]:
        current_enemy_list = read_zList(current_enemy_list["next"])

        zEnemy = current_enemy_list["entry"]
        zEnemyFlags = read_int(zEnemy + zEnemy_flags)

        if zEnemyFlags & zEnemyFlags_intangible != 0:
            continue

        enemy = {
            'id':           zEnemy,
            'position':     (read_float(zEnemy + zEnemy_pos), read_float(zEnemy + zEnemy_pos + 0x4)),
            'hurtbox':      (read_float(zEnemy + zEnemy_hurtbox), read_float(zEnemy + zEnemy_hurtbox + 0x4)),
            'hitbox':       (read_float(zEnemy + zEnemy_hitbox), read_float(zEnemy + zEnemy_hitbox + 0x4)),
            'no_hurtbox':   zEnemyFlags & zEnemyFlags_no_hurtbox != 0,
            'no_hitbox':    zEnemyFlags & zEnemyFlags_no_hitbox != 0,
            'invincible':   zEnemyFlags & zEnemyFlags_invincible != 0,
            'is_rectangle': zEnemyFlags & zEnemyFlags_is_rectangle != 0,
            'is_boss':      zEnemyFlags & zEnemyFlags_is_boss != 0,
            'subboss_id':   read_int(zEnemy + zEnemy_subboss_id, signed=True),
            'rotation':     read_float(zEnemy + zEnemy_rotation),
            'anm_page':     read_int(zEnemy + zEnemy_anm_page),
            'anm_id':       read_int(zEnemy + zEnemy_anm_id),
            'score_reward': read_int(zEnemy + zEnemy_score_reward),
            'hp':           read_int(zEnemy + zEnemy_hp),
            'hp_max':       read_int(zEnemy + zEnemy_hp_max),
            'drops':        extract_enemy_drops(zEnemy + zEnemy_drops),
            'iframes':      read_int(zEnemy + zEnemy_iframes),
        }

        if game_id == 13:
            spirit_time_max  = read_int(zEnemy + zEnemy_spirit_time_max)
            remaining_frames =  spirit_time_max - read_int(zEnemy + zEnemy_timer)

            if remaining_frames >= 0:
                interval_size = spirit_time_max // read_int(zEnemy + zEnemy_max_spirit_count)
                enemy['speedkill_blue_drops'] = (remaining_frames // interval_size) + (2 if difficulty >= 2 else 1)
                enemy['speedkill_time_left_for_amt'] = remaining_frames - (remaining_frames // interval_size) * interval_size + 1

            else:
                enemy['speedkill_blue_drops'] = 0
                enemy['speedkill_time_left_for_amt'] = 0

            kyouko_echo = None
            special_func = read_int(zEnemy + zEnemy_special_func)
            if special_func == square_echo_func:
                kyouko_echo = RectangleEcho(
                    left_x   = enemy['position'][0] + read_float(zEnemy + zEnemy_f0_echo_x1),
                    right_x  = enemy['position'][0] + read_float(zEnemy + zEnemy_f1_echo_x2),
                    top_y    = enemy['position'][1] + read_float(zEnemy + zEnemy_f2_echo_y1),
                    bottom_y = enemy['position'][1] + read_float(zEnemy + zEnemy_f3_echo_y2),
                )

            elif special_func == inv_square_echo_func:
                kyouko_echo = RectangleEcho(
                    left_x   = read_float(zEnemy + zEnemy_f0_echo_x1),
                    right_x  = read_float(zEnemy + zEnemy_f1_echo_x2),
                    top_y    = read_float(zEnemy + zEnemy_f2_echo_y1),
                    bottom_y = read_float(zEnemy + zEnemy_f3_echo_y2),
                )

            elif special_func == circle_echo_func:
                kyouko_echo = CircleEcho(
                    position = (read_float(zEnemy + zEnemy_f1_echo_x2), read_float(zEnemy + zEnemy_f2_echo_y1)),
                    radius   = read_float(zEnemy + zEnemy_f0_echo_x1),
                )

            enemy['kyouko_echo'] = kyouko_echo
            enemies.append(TDEnemy(**enemy))

        elif game_id == 15:
            enemy['shootdown_weight'] = read_int(zEnemy + zEnemy_weight, signed=True)
            enemies.append(WeightedEnemy(**enemy))

        else:
            enemies.append(Enemy(**enemy))

    return enemies

def extract_items(item_manager = zItemManager):
    items = []
    item_array_start = item_manager + zItemManager_array
    item_array_end   = item_array_start + zItemManager_array_len * zItem_len

    for item in range(item_array_start, item_array_end, zItem_len):
        item_state = read_int(item + zItem_state)
        if item_state == 0:
            continue

        item_type = read_int(item + zItem_type)
        if not get_item_type(item_type):
            if item_type < 50:
                print(f"Found and skipped unknown item with type ID {item_type}. If this is a real in-game item, please report it to the developper!")
            continue

        item_x     = read_float(item + zItem_pos)
        item_y     = read_float(item + zItem_pos + 0x4)
        item_vel_x = read_float(item + zItem_vel)
        item_vel_y = read_float(item + zItem_vel + 0x4)

        items.append(Item(
            id        = item,
            state     = item_state,
            item_type = item_type,
            position  = (item_x, item_y), 
            velocity  = (item_vel_x, item_vel_y),
        ))

    return items

# Ten Desires only
def extract_spirit_items():
    spirit_items = []
    spirit_array_start = zSpiritManager + zSpiritManager_array
    spirit_array_end   = spirit_array_start + zSpiritManager_array_len * zSpiritItem_len

    for spirit_item in range(spirit_array_start, spirit_array_end, zSpiritItem_len):
        if read_int(spirit_item + zSpiritItem_state) != 0:
            spirit_item_type  = read_int(spirit_item + zSpiritItem_type)
            spirit_item_x     = read_float(spirit_item + zSpiritItem_pos)
            spirit_item_y     = read_float(spirit_item + zSpiritItem_pos + 0x4)
            spirit_item_vel_x = read_float(spirit_item + zSpiritItem_vel)
            spirit_item_vel_y = read_float(spirit_item + zSpiritItem_vel + 0x4)
            spirit_item_timer = read_int(spirit_item + zSpiritItem_timer)

            spirit_items.append(SpiritItem(
                id          = spirit_item,
                spirit_type = spirit_item_type,
                position    = (spirit_item_x, spirit_item_y),
                velocity    = (spirit_item_vel_x, spirit_item_vel_y),
                timer       = spirit_item_timer,
            ))

    return spirit_items

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
            'id':         current_laser_ptr,
            'state':      laser_state,
            'laser_type': laser_type,
            'timer':      read_int(current_laser_ptr + zLaserBaseClass_timer),
            'position':  (read_float(current_laser_ptr + zLaserBaseClass_offset), read_float(current_laser_ptr + zLaserBaseClass_offset + 0x4)),
            'angle':      read_float(current_laser_ptr + zLaserBaseClass_angle),
            'length':     read_float(current_laser_ptr + zLaserBaseClass_length),
            'width':      read_float(current_laser_ptr + zLaserBaseClass_width),
            'speed':      read_float(current_laser_ptr + zLaserBaseClass_speed),
            'iframes':    read_int(current_laser_ptr + zLaserBaseClass_iframes),
            'sprite':     read_int(current_laser_ptr + zLaserBaseClass_sprite),
            'color':      read_int(current_laser_ptr + zLaserBaseClass_color),
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

        if i == 0:
            node_angle = read_float(current_node_ptr + zLaserCurveNode_angle)
            node_speed = read_float(current_node_ptr + zLaserCurveNode_speed)

            if i == 0:
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

def extract_spellcard(spellcard = zSpellCard):
    if read_int(spellcard + zSpellcard_indicator) == 0:
        return None

    spell_id = read_int(spellcard + zSpellcard_id)
    spell_capture_bonus = read_int(spellcard + zSpellcard_bonus, signed=True)

    return Spellcard(
        spell_id = spell_id,
        capture_bonus = spell_capture_bonus,
    )

def extract_game_state(frame_id = None, real_time = None):
    game_specific = None

    if game_id == 13:
        global life_piece_req
        life_piece_reqs = [8, 10, 12, 15, 18, 20, 25]
        life_piece_req = life_piece_reqs[read_int(extend_count, rel=True)]

        game_specific = GameSpecificTD(
            life_piece_req = life_piece_req,
            trance_active  = read_int(trance_state, rel=True) != 0,
            trance_meter   = read_int(trance_meter, rel=True),
            chain_timer    = read_int(zSpiritManager + zSpiritManager_chain_timer),
            chain_counter  = read_int(zSpiritManager + zSpiritManager_chain_counter),
            spirit_items   = extract_spirit_items() if requires_items else [],
        )

    elif game_id == 14:
        game_specific = GameSpecificDDC(
            bonus_count  = read_int(bonus_count, rel=True),
            player_scale = read_float(zPlayer + zPlayer_scale),
            seija_flip   = (read_float(ddcSeijaAnm + seija_flip_x), read_float(ddcSeijaAnm + seija_flip_y)),
        )

    elif game_id == 15:
        game_specific = GameSpecificLoLK(
            item_graze_slowdown_factor     = read_float(zItemManager + zItemManager_graze_slowdown_factor),
            reisen_bomb_shields            = read_int(zBomb + zBomb_reisen_shields),
            time_in_chapter                = read_int(time_in_chapter, rel=True),
            chapter_graze                  = read_int(chapter_graze, rel=True),
            chapter_enemy_weight_spawned   = read_int(chapter_enemy_weight_spawned, rel=True),
            chapter_enemy_weight_destroyed = read_int(chapter_enemy_weight_destroyed, rel=True),
            in_pointdevice                 = read_int(modeflags, rel=True) & 2**8 != 0,
            pointdevice_resets_total       = read_int(pointdevice_resets_total, rel=True),
            pointdevice_resets_chapter     = read_int(pointdevice_resets_chapter, rel=True),
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
            card_id                = read_int(zCard + zCard_id)
            card_charge_max        = int(read_int(zCard + zCard_charge_max)) #the first 20% of the cooldown time is always skipped
            card_charge            = card_charge_max - read_int(zCard + zCard_charge) #game counts down rather than up, but up is more intuitive

            card_name = read_string(read_int(read_int(zCard + zCard_name)), 15)

            #uncomment to see other internal card names and uses of counter 
            #(some actives use it temporarily, out of bounds address for most passives)
            #print(f"{card_name} ({card_id}): {read_int(zCard + zCard_counter)}")

            if card_id == 48: #Lily
                lily_counter = read_int(zCard + zCard_counter)

            if card_id not in card_nicknames.keys():
                if card_id == 54: #Centipede
                    centipede_multiplier = 1 + 0.00005 * min(16000, read_int(zCard + zCard_counter))

                continue #skip non-actives

            active_cards.append(ActiveCard(
                id            = card_id,
                charge        = card_charge, 
                charge_max    = card_charge_max,
                internal_name = card_name,
                selected      = zCard == selected_active
            ))

        game_specific = GameSpecificUM(
            funds                = read_int(funds, rel=True),
            total_cards          = read_int(zAbilityManager + zAbilityManager_total_cards),
            total_actives        = read_int(zAbilityManager + zAbilityManager_total_actives),
            total_equipmt        = read_int(zAbilityManager + zAbilityManager_total_equipmt),
            total_passive        = read_int(zAbilityManager + zAbilityManager_total_passive),
            cancel_counter       = read_int(zBulletManager + zBulletManager_cancel_counter),
            lily_counter         = lily_counter,
            centipede_multiplier = centipede_multiplier,
            active_cards         = active_cards,
        )

    elif game_id == 19:
        side2 = None

        if requires_side2_pvp:
            side2 = P2Side(
                lives               = read_int(p2_lives, rel=True),
                lives_max           = read_int(p2_lives_max, rel=True),
                bombs               = read_int(p2_bombs, rel=True),
                bomb_pieces         = read_int(p2_bomb_pieces, rel=True),
                power               = read_int(p2_power, rel=True),
                graze               = read_int(p2_graze, rel=True),
                boss_timer          = float(f"{read_int(zGui+zGui_p2_bosstimer_s)}.{read_int(zGui+zGui_p2_bosstimer_ms)}") if read_int(zGui+zGui_p2_bosstimer_drawn) == 0 else -1,
                spellcard           = extract_spellcard(zSpellCardP2),
                input               = read_int(p2_input, rel=True),
                player_position     = (read_float(zPlayerP2 + zPlayer_pos), read_float(zPlayerP2 + zPlayer_pos + 0x4)),
                player_hitbox_rad   = read_float(zPlayerP2 + zPlayer_hit_rad),
                player_iframes      = read_int(zPlayerP2 + zPlayer_iframes),
                player_focused      = read_int(zPlayerP2 + zPlayer_focused) == 1,
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
            )

        game_specific = GameSpecificUDoALG(
            lives_max =           read_int(lives_max, rel=True),
            hitstun_status =      read_int(zPlayer + zPlayer_hitstun_status),
            shield_status =       read_int(zPlayer + zPlayer_shield_status),
            last_combo_hits =     read_int(zPlayer + zPlayer_last_combo_hits),
            current_combo_hits =  read_int(zPlayer + zPlayer_current_combo_hits),
            current_combo_chain = read_int(zPlayer + zPlayer_current_combo_chain),
            enemy_pattern_count = read_int(zEnemyManager + zEnemyManager_pattern_count),
            item_spawn_total =    read_int(zItemManager + zItemManager_spawn_total),
            gauge_charging =      read_int(zGaugeManager + zGaugeManager_charging_bool) == 1,
            gauge_charge =        read_int(zGaugeManager + zGaugeManager_gauge_charge),
            gauge_fill =          read_int(zGaugeManager + zGaugeManager_gauge_fill),
            ex_attack_level =     read_int(ex_attack_level, rel=True),
            boss_attack_level =   read_int(boss_attack_level, rel=True),
            pvp_wins =            read_int(pvp_wins, rel=True),
            side2 =               side2,
            pvp_timer_start =     read_int(pvp_timer_start, rel=True),
            pvp_timer =           read_int(pvp_timer, rel=True),
        )

    boss_timer = -1
    if (game_id in has_boss_timer_drawn_if_indic_zero) == (read_int(zGui+zGui_bosstimer_drawn) == 0):
        boss_timer = float(f"{read_int(zGui+zGui_bosstimer_s)}.{read_int(zGui+zGui_bosstimer_ms)}")

    gs = GameState(
        frame_stage         = read_int(stage_timer),
        frame_global        = read_int(global_timer),
        stage_chapter       = read_int(stage_chapter, rel=True),
        seq_frame_id        = frame_id,
        seq_real_time       = real_time,
        pause_state         = read_int(pause_state, rel=True),
        game_mode           = read_int(game_mode, rel=True),
        score               = read_int(score, rel=True) * 10,
        lives               = read_int(lives, rel=True, signed=True),
        life_pieces         = read_int(life_pieces, rel=True) if life_pieces else 0,
        bombs               = read_int(bombs, rel=True),
        bomb_pieces         = read_int(bomb_pieces, rel=True),
        power               = read_int(power, rel=True),
        piv                 = int(read_int(piv, rel=True) / 100),
        graze               = read_int(graze, rel=True),
        boss_timer          = boss_timer,
        spellcard           = extract_spellcard(),
        rank                = read_int(rank, rel=True),
        input               = read_int(input, rel=True),
        rng                 = read_int(rng, rel=True),
        player_position     = (read_float(zPlayer + zPlayer_pos), read_float(zPlayer + zPlayer_pos + 0x4)),
        player_hitbox_rad   = read_float(zPlayer + zPlayer_hit_rad),
        player_iframes      = read_int(zPlayer + zPlayer_iframes),
        player_focused      = read_int(zPlayer + zPlayer_focused) == 1,
        bomb_state          = read_int(zBomb + zBomb_state),
        bullets             = extract_bullets() if requires_bullets else [],
        enemies             = extract_enemies() if requires_enemies else [],
        items               = extract_items() if requires_items else [],
        lasers              = extract_lasers() if requires_lasers else [],
        screen              = get_rgb_screenshot() if requires_screenshots else None,
        game_specific       = game_specific,
    )
    
    return gs

def print_game_state(gs: GameState):
    #======================================
    # Consistent prints ===================
    print(f"[Stage Frame #{gs.frame_stage} | Global Frame #{gs.frame_global}] Score: {gs.score:,}")

    # Basic resources
    basic_resources = f"| {gs.lives} lives"
    if life_piece_req != None:
        basic_resources += f" ({gs.life_pieces}/{life_piece_req} pieces)"
    basic_resources += f"; {gs.bombs} bombs"
    if bomb_piece_req != None:
        basic_resources += f" ({gs.bomb_pieces}/{bomb_piece_req} pieces)"
    print(basic_resources + f"; {gs.power/100:.2f} power; {gs.piv:,} PIV; {gs.graze:,} graze")

    # Player status
    print(f"| Player at ({round(gs.player_position[0], 2)}, {round(gs.player_position[1], 2)}); hitbox radius {gs.player_hitbox_rad}; {gs.player_iframes} iframes; {'un' if not gs.player_focused else ''}focused movement")

    # Useful internals
    print(f"| Game state: {pause_states[gs.pause_state]} ({game_modes[gs.game_mode]})")
    print(f"| Input bitflag: {gs.input:08b}")
    print(f"| RNG value: {gs.rng}")

    if game_id in uses_rank:
        print(f"| Rank value: {gs.rank}")

    #======================================
    # Situational prints ==================
    if gs.boss_timer != -1:
        print(f"| Boss timer: {gs.boss_timer:.2f}")

    if gs.spellcard:
        print(f"| Spell #{gs.spellcard.spell_id+1}; SCB: {gs.spellcard.capture_bonus if gs.spellcard.capture_bonus > 0 else 'Failed'}")

    if gs.bomb_state > 0:
        print(f"| Bomb active (state: {gs.bomb_state})")

    #======================================
    # Game-specific prints ================
    if game_id == 13: #TD
        print(f"| TD Trance Meter: {round(gs.game_specific.trance_meter/200, 2)} / 3.0")

        if gs.game_specific.trance_active:
            print(f"| TD Active Trance: {gs.game_specific.trance_meter/60:.2f}s")

        if gs.game_specific.chain_counter:
            print(f"| TD Chain {'Active' if gs.game_specific.chain_counter > 9 else 'Starting (no greys)'}: {gs.game_specific.chain_counter} blues spawned; {gs.game_specific.chain_timer}f left")

        if gs.game_specific.spirit_items:
            counter = 0

            print("\nList of spirit items:")
            print("  Type       Position         Velocity         Frames Left")
            for spirit in gs.game_specific.spirit_items:
                description = "• "
                description += tabulate(spirit_types[spirit.spirit_type], 11)
                description += tabulate(f"({round(spirit.position[0], 1)}, {round(spirit.position[1], 1)})", 17)
                description += tabulate(f"({round(spirit.velocity[0], 1)}, {round(spirit.velocity[1], 1)})", 17)
                description += str(522 - spirit.timer)
                print(description)

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(f'• ... [{len(gs.game_specific.spirit_items)} spirit item total]')
                    break

    elif game_id == 14: #DDC
        print(f"| DDC Bonus Count: {gs.game_specific.bonus_count}")

        if gs.game_specific.seija_flip[0] != 1:
            print(f"| DDC Seija Horizontal Flip: {round(100*(-gs.game_specific.seija_flip[0]+1)/2, 2)}%")

        if gs.game_specific.seija_flip[1] != 1:
            print(f"| DDC Seija Vertical Flip: {round(100*(-gs.game_specific.seija_flip[1]+1)/2, 2)}%")

        if gs.game_specific.player_scale > 1:
            print(f"| DDC Player Scale: grew {round(gs.game_specific.player_scale, 2)}x bigger! (hitbox radius: {round(gs.player_hitbox_rad * gs.game_specific.player_scale, 2)})")

    elif game_id == 15: #LoLK
        chapter = "Chapter"
        if gs.stage_chapter:
            chapter = f"S{read_int(stage, rel=True)}C{gs.stage_chapter+1}"

        chapter_desc = f"{gs.game_specific.chapter_graze} graze; "
        chapter_desc += f"shootdown {gs.game_specific.chapter_enemy_weight_destroyed}/{gs.game_specific.chapter_enemy_weight_spawned}"
        if gs.game_specific.chapter_enemy_weight_spawned > 0:
            chapter_desc += f" ({round(100*gs.game_specific.chapter_enemy_weight_destroyed/gs.game_specific.chapter_enemy_weight_spawned,1)}%)"
        chapter_desc += f"; frame #{gs.game_specific.time_in_chapter}"
        print(f"| LoLK {chapter}: {chapter_desc}")

        if gs.game_specific.in_pointdevice:
            print(f"| LoLK Pointdevice: {gs.game_specific.pointdevice_resets_chapter} chapter resets / {gs.game_specific.pointdevice_resets_total} total resets")

        if gs.game_specific.item_graze_slowdown_factor < 1:
            print(f"| LoLK Item Graze Slowdown: {round(gs.game_specific.item_graze_slowdown_factor,1)}x")

        if gs.game_specific.reisen_bomb_shields > 0:
            print(f"| LoLK Reisen Bomb Shields: {gs.game_specific.reisen_bomb_shields}")

    elif game_id == 18: #UM
        print(f"| UM Funds: {gs.game_specific.funds:,}")

        cards_breakdown = ""
        if gs.game_specific.total_cards > 0:
            cards_breakdown += " ("
            if gs.game_specific.total_actives > 0:
                cards_breakdown += f"{gs.game_specific.total_actives} active"
            if gs.game_specific.total_equipmt > 0:
                if cards_breakdown != " (":
                    cards_breakdown += ", "
                cards_breakdown += f"{gs.game_specific.total_equipmt} equipment"
            if gs.game_specific.total_passive > 0:
                if cards_breakdown != " (":
                    cards_breakdown += ", "
                cards_breakdown += f"{gs.game_specific.total_passive} passive"
            cards_breakdown += ")"

        print(f"| UM Cards: {gs.game_specific.total_cards}" + cards_breakdown)

        if gs.game_specific.centipede_multiplier:
            print(f"| UM Centipede Multiplier: {gs.game_specific.centipede_multiplier:.3f}x")

        if gs.game_specific.lily_counter != None:
            print(f"| UM Lily Use Count: {gs.game_specific.lily_counter} (" + ('next Lily drops Life Piece' if gs.game_specific.lily_counter % 3 == 2 else 'next Lily drops Bomb Piece') + ")")

        if gs.game_specific.active_cards:
            print("\nList of active cards:")
            print("  ID   Internal Name   Nickname    Charge / Max     %")
            for card in gs.game_specific.active_cards:
                description = "• "
                description += tabulate(card.id, 5)
                description += tabulate(card.internal_name, 16)
                description += tabulate(card_nicknames[card.id], 12)
                description += tabulate(card.charge, 6) + " / "
                description += tabulate(card.charge_max, 8)
                description += tabulate(f"{round(100*card.charge / card.charge_max, 2):.3g}%", 6)

                if card.selected:
                    description += " (selected)"

                print(description)

    elif game_id == 19: #UDoALG
        print(f"| UDoALG Shield: {'Active' if gs.game_specific.shield_status == 1 else 'Broken'}; Max Lives: {gs.game_specific.lives_max}")
        print(f"| UDoALG Combo Hits: {gs.game_specific.current_combo_hits}")
        print(f"| UDoALG Item Spawn Total: {gs.game_specific.item_spawn_total}")

        if gs.game_specific.gauge_charging:
            print(f"| UDoALG Gauge Charge: {gs.game_specific.gauge_charge} / {gs.game_specific.gauge_fill}")
        print(f"| UDoALG Gauge Fill: {gs.game_specific.gauge_fill} / 2500")
        print(f"| UDoALG Attack Levels: Lv{gs.game_specific.ex_attack_level + 1} Ex, Lv{gs.game_specific.boss_attack_level + 1} Boss")

        if gs.game_specific.pvp_timer_start:
            print(f"| UDoALG PvP Timer: {round(gs.game_specific.pvp_timer/60)} / {round(gs.game_specific.pvp_timer_start/60)}")

        if gs.game_specific.side2:
            print("| UDoALG P2 side data included in state.")

    #======================================
    # Game entity prints (all optional) ===
    if gs.bullets and any(bullet.is_active for bullet in gs.bullets): #Bullets
        counter = 0

        print("\nList of bullets:")
        print("  Position         Velocity         Speed   Angle   Radius  Color        Type")
        for bullet in gs.bullets:
            if not bullet.is_active:
                continue

            description = "• "
            description += tabulate(f"({round(bullet.position[0], 1)}, {round(bullet.position[1], 1)})", 17)
            description += tabulate(f"({round(bullet.velocity[0], 1)}, {round(bullet.velocity[1], 1)})", 17)
            description += tabulate(round(bullet.speed, 1), 8)
            description += tabulate(round(bullet.angle, 2), 8)
            description += tabulate(round(bullet.hitbox_radius, 1), 8)
            description += tabulate(get_color(bullet.bullet_type, bullet.color)[0], 13)

            #account for mono-color sprites
            bullet_type = sprites[bullet.bullet_type][0]
            if sprites[bullet.bullet_type][1] == 0:
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

            print(description)

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(f'• ... [{len(gs.bullets)} active bullets total]')
                break

    if gs.lasers: #Lasers
        line_lasers = [laser for laser in gs.lasers if laser.laser_type == 0]
        infinite_lasers = [laser for laser in gs.lasers if laser.laser_type == 1]
        curve_lasers = [laser for laser in gs.lasers if laser.laser_type == 2]
        beam_lasers = [laser for laser in gs.lasers if laser.laser_type == 3]

        if line_lasers:
            counter = 0

            print("\nList of segment (\"line\") lasers:")
            print("  Tail Position    Speed   Angle   Length / Max     Width   Color   Sprite")
            for laser in line_lasers:
                description = "• "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(round(laser.speed, 1), 8)
                description += tabulate(round(laser.angle, 2), 8)
                description += tabulate(round(laser.length, 1), 6) + " / "
                description += tabulate(round(laser.max_length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(sprites[laser.sprite][0], 8)
                print(description)

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(f'• ... [{len(line_lasers)} line lasers total]')
                    break

        if infinite_lasers:
            counter = 0

            print("\nList of telegraphed (\"infinite\") lasers:")
            print("  Origin Position  Origin Velocity  Angle (Vel)    Length (%)    Width (%)     Color   State (#frames left)")
            for laser in infinite_lasers:
                description = "• "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(f"({round(laser.origin_vel[0], 1)}, {round(laser.origin_vel[1], 1)})", 17)
                description += tabulate(round(laser.angle, 2), 6)
                description += tabulate(f"({format(laser.angular_vel, '.3f').rstrip('0').rstrip('.')})", 9)
                description += tabulate(f"{round(laser.length, 1)} ({int(100*laser.length/laser.max_length)}%)", 14)
                description += tabulate(f"{round(laser.width, 1)} ({int(100*laser.width/laser.max_width)}%)", 14)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)

                if laser.state == 3:
                    description += f"Telegraph ({laser.start_time - laser.timer}f)"
                elif laser.state == 4:
                    description += f"Expand ({laser.expand_time - laser.timer}f)"
                elif laser.state == 2:
                    description += f"Active ({laser.active_time - laser.timer}f)"
                elif laser.state == 5:
                    description += f"Shrink ({laser.shrink_time - laser.timer}f)"
                else:
                    description += "Unknown"

                print(description)

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(f'• ... [{len(infinite_lasers)} telegraphed lasers total]')
                    break

        if curve_lasers:
            counter = 0

            print("\nList of curvy lasers:")
            print("  Spawn Position  Head Position     Head Velocity   HSpeed  HAngle  #Nodes  Width   Color   Sprite")
            for laser in curve_lasers:
                description = "• "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 16)
                description += tabulate(f"({round(laser.nodes[0].position[0], 1)}, {round(laser.nodes[0].position[1], 1)})", 18)
                description += tabulate(f"({round(laser.nodes[0].velocity[0], 1)}, {round(laser.nodes[0].velocity[1], 1)})", 16)
                description += tabulate(round(laser.nodes[0].speed, 1), 8)
                description += tabulate(round(laser.nodes[0].angle, 2), 8)
                description += tabulate(round(laser.max_length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_curve_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(curve_sprites[laser.sprite], 10)
                print(description)

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(f'• ... [{len(curve_lasers)} curvy lasers total]')
                    break

        if beam_lasers:
            counter = 0

            print("\nList of beam lasers:")
            print("Note: Beam lasers are not fully supported; data may be inaccurate.")
            print("  Position         Speed   Angle   Length  Width   Color   Sprite")
            for laser in beam_lasers:
                description = "• "
                description += tabulate(f"({round(laser.position[0], 1)}, {round(laser.position[1], 1)})", 17)
                description += tabulate(round(laser.speed, 1), 8)
                description += tabulate(round(laser.angle, 2), 8)
                description += tabulate(round(laser.length, 1), 8)
                description += tabulate(round(laser.width, 1), 8)
                description += tabulate(get_color(laser.sprite, laser.color)[0], 8)
                description += tabulate(sprites[laser.sprite][0], 8)
                print(description)

                counter += 1
                if counter >= singlext_settings['list_print_limit']:
                    print(f'• ... [{len(beam_lasers)} beam lasers total]')
                    break

    if gs.enemies: #Enemies
        counter = 0

        print("\nList of enemies:")
        print("  Position        Hurtbox         Hitbox          Rotation  IFrames  HP / Max HP     Type")
        for enemy in gs.enemies:
            description = "• "
            description += tabulate(f"({round(enemy.position[0], 1)}, {round(enemy.position[1], 1)})", 16)
            description += tabulate(f"({round(enemy.hurtbox[0], 1)}, {round(enemy.hurtbox[1], 1)})", 16)
            description += tabulate(f"({round(enemy.hitbox[0], 1)}, {round(enemy.hitbox[1], 1)})", 16)
            description += tabulate(round(enemy.rotation, 2), 10)
            description += tabulate(enemy.iframes, 9)
            description += tabulate(f"{enemy.hp} / {enemy.hp_max}", 16)

            type = ""
            if enemy.anm_page == 2:
                if enemy.anm_id in enemy_anms:
                    type = enemy_anms[enemy.anm_id]
                else:
                    type = f"Unknown #{enemy.anm_id}"
            elif enemy.anm_page == 0 or enemy.anm_page > 2:
                if enemy.is_boss:
                    if enemy.subboss_id == 0:
                        type = "Boss"
                    else:
                        type = f"Sub-boss #{enemy.subboss_id}"
                else:
                    type = "Boss-specific"
            else:
                type = f"Unknown {enemy.anm_page}/{enemy.anm_id}"
            description += tabulate(type, 16)

            #not in table since rare
            if enemy.no_hurtbox:
                description += " (Hurtbox Off)"
            if enemy.no_hitbox:
                description += " (Hitbox Off)"
            if enemy.invincible:
                description += " (Invincible)"
            if hasattr(enemy, 'kyouko_echo') and enemy.kyouko_echo:
                description += f" (Echoing)"
            if hasattr(enemy, 'shootdown_weight') and enemy.shootdown_weight != 1:
                description += f" ({enemy.shootdown_weight} weight)"

            #note: boss drops are never properly set prior to the frame they're instructed to drop
            if singlext_settings['show_enemy_drops'] and enemy.drops and not enemy.is_boss:
                description += "\n  • Drops: " + ", ".join(f"{enemy.drops[drop]} {item_types[drop]}" for drop in enemy.drops)
                if game_id == 13 and enemy.speedkill_blue_drops:
                    description += f" (+ {enemy.speedkill_blue_drops} Blue Spirit; will be {enemy.speedkill_blue_drops-1} in {enemy.speedkill_time_left_for_amt}f)"

            print(description)

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(f'• ... [{len(gs.enemies)} enemies total]')
                break

    if gs.game_mode == 7 and gs.items: #Items
        counter = 0

        print("\nList of items:")
        print("  Position         Velocity         Type")
        for item in gs.items:
            description = "• "
            description += tabulate(f"({round(item.position[0], 1)}, {round(item.position[1], 1)})", 17)
            description += tabulate(f"({round(item.velocity[0], 1)}, {round(item.velocity[1], 1)})", 17)
            description += tabulate(get_item_type(item.item_type), 14)

            #not in table since rare
            if item.state == zItemState_autocollect:
                description += " (Auto-collecting)"
            elif item.state == zItemState_attracted:
                description += " (Attracted)"

            print(description)

            counter += 1
            if counter >= singlext_settings['list_print_limit']:
                print(f'• ... [{len(gs.items)} items total]')
                break

def print_untracked_vars():
    print("[Bonus] Untracked values:")
    print(f"| RNG Seed: {read_int(rng_seed, rel=True)}")
    print(f"| Game Speed: {read_float(game_speed, rel=True)}")
    print(f"| Visual RNG: {read_int(visual_rng, rel=True)}")
    print(f"| Character: {characters[read_int(character, rel=True)]}")

    if 'p2_shottype' in globals():
        print(f"| P2 Character: {characters[read_int(p2_shottype, rel=True)]}")
    else:
        print(f"| Sub-Shot: {subshots[read_int(subshot, rel=True)]}")

    print(f"| Difficulty: {difficulties[difficulty]}")
    print(f"| Stage #: {read_int(stage, rel=True)}")
    print(f"| Continues: {read_int(continues, rel=True)}")

    if game_id == 19:
        print(f"| UDoALG Max Rank: {read_int(rank_max, rel=True)}")

        print(f"\n| UDoALG P1 Card Count: {read_int(zAbilityManager + zAbilityManager_total_cards)}")
        print(f"| UDoALG P1 Charge Attack Threshold: {read_int(charge_attack_threshold, rel=True)}")
        print(f"| UDoALG P1 Charge Skill Threshold: {read_int(skill_attack_threshold, rel=True)}")
        print(f"| UDoALG P1 Ex Attack Threshold: {read_int(ex_attack_threshold, rel=True)}")
        print(f"| UDoALG P1 Boss Attack Threshold: {read_int(boss_attack_threshold, rel=True)}")

        print(f"\n| UDoALG P2 Card Count: {read_int(zAbilityManagerP2 + zAbilityManager_total_cards)}")
        print(f"| UDoALG P2 Charge Attack Threshold: {read_int(p2_charge_attack_threshold, rel=True)}")
        print(f"| UDoALG P2 Charge Skill Threshold: {read_int(p2_skill_attack_threshold, rel=True)}")
        print(f"| UDoALG P2 Ex Attack Threshold: {read_int(p2_ex_attack_threshold, rel=True)}")
        print(f"| UDoALG P2 Boss Attack Threshold: {read_int(p2_boss_attack_threshold, rel=True)}")

def on_exit():
    if game_process.is_running:
        game_process.resume()

def parse_frame_count(expr):
    unit = expr[-1:]
    if unit.lower() not in "fs":
        return None

    frame_count = 0
    if unit == "s":
        try:
            frame_count = math.floor(float(expr[:-1]) * 60)
        except ValueError:
            return None
    else:
        try:
            frame_count = int(expr[:-1])
        except ValueError:
            return None

    return frame_count

atexit.register(on_exit)

print("================================")

if only_game_world and read_int(game_mode, rel=True) != 7:
    print("Error: Game world not loaded (only_game_world set to True).")
    exit()

infinite = False
frame_count = 0
if seqext_settings['ingame_duration']:
    if seqext_settings['ingame_duration'].lower() in ['inf', 'infinite', 'endless', 'forever']:
        infinite = True

    else:
        parsed_frame_count = parse_frame_count(seqext_settings['ingame_duration'])

        if parsed_frame_count:
            frame_count = parsed_frame_count
        else:
            print(f"Error: Couldn't parse duration '{seqext_settings['ingame_duration']}'; remember to include a unit (e.g. 150f / 12.4s).")
            print("Defaulting to single-state extraction.\n")

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        parsed_frame_count = parse_frame_count(arg)

        if parsed_frame_count:
            frame_count = parsed_frame_count

        elif arg in ['inf', 'infinite', 'endless', 'forever']:
            infinite = True

        elif arg == 'exact':
            exact = True #overwrites options

        else:
            print(f"Error: Unrecognized argument '{arg}'.")
            exit()

if not hasattr(analysis, analyzer):
    print(f"Error: Unrecognized analyzer {analyzer}; defaulting to template.")
    analyzer = 'AnalysisTemplate'

if frame_count < 2 and not infinite: #Single-State Extraction
    analysis = getattr(analysis, analyzer)()

    if requires_screenshots:
        get_focus()

    state = extract_game_state()
    analysis.step(state)
    print_game_state(state)

    print("================================")
    analysis.done()

    if singlext_settings['show_untracked']:
        print("\n================================")
        print_untracked_vars()

else: #State Sequence Extraction
    if infinite:
        print(f"Extracting frames until termination (infinite mode){' (exact mode)' if exact else ''}.")
    else:
        print(f"Extracting {frame_count} frames{' (exact mode)' if exact else ''}.")

    if seqext_settings['auto_unpause']:
        unpause_game()
    else:
        if seqext_settings['auto_focus']:
            get_focus()
        print("(Unpause the game to begin extraction)")

    analysis = getattr(analysis, analyzer)()
    start_time = time.perf_counter()
    terminated = False
    frame_counter = 0

    while infinite or frame_counter < frame_count:
        if terminated:
            break

        frame_timestamp = read_int(stage_timer)
        if infinite:
            if infinite_print_updates:
                print(f"Extracting frame #{frame_counter+1} (in-stage: #{frame_timestamp})")
        else:
            print(f"[{int(100*frame_counter/frame_count)}%] Extracting frame #{frame_counter+1} (in-stage: #{frame_timestamp})")

        if exact:
            game_process.suspend()

        state = extract_game_state(frame_counter, time.perf_counter() - start_time)
        analysis.step(state)
        frame_counter += 1

        if exact:
            game_process.resume()

        #busy wait for new frame
        while True: #(do...while, ensuring term conditions evaluated at least once)
            term_return = eval_termination_conditions(need_active)
            if term_return:
                print(f"{term_return}; terminating now.")
                terminated = True
                break

            if read_int(stage_timer) != frame_timestamp:
                break

    if not terminated:
        print(f"{'[100%] ' if infinite else ''}Finished extraction in { round(time.perf_counter() - start_time, 2) } seconds.")

    if seqext_settings['auto_repause']:
        pause_game()

    print("================================")
    analysis.done()