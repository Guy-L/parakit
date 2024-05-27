from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# offsets & game_entities: Guidelines for Game-Specific Data
# if shared by a majority of windows games (>= 10)
    # offsets.py: defined Optional for all offset objects, set to None when absent
    # game_entities: defined Optional for all game state objects, set to None if offset is None
        #OR (preferred): non-optional in game states & set to default value if offset is None

# object properties: if not shared by a majority of windows games (<10)
    # offsets.py: defined only in game_specifc dict
    # game_entities: defined Optional for all game state objects, set to None if offset not in namespace

# globals & systems used by only a few games (ie cards)
    # offsets.py: defined only in game_specifc dict
    # game_entities: in game_specific game state member, set in extract_game_state based on game number or game-logic grouping

#rationale for offsets.py rules:
#1. don't want massive amount of Nones for all game offset objects due to differences
#2. dataclasses are used in favor of dicts for consistency AND convenience; defining new dataclasses for all possible shared game-specific data is not convenient so dicts it is

#rationale for game_entities.py rules:
#1. data that's shared by more than a few games should be writeable/accessible without the game-specific dict for speed and convenience
#2. want to minimize the use of dicts in general here; game_specifc dicts may eventually be switched to a family of game specific dataclasses
#3. extraction method assumes given offset is not None for efficiency reasons; call must be conditional

# to decide in the future: how to account for major differences like laser data types in older windows games

@dataclass
class StaticsOffsets:
    game_speed: int
    score: int
    continues: int
    graze: int
    piv: int
    power: int
    lives: int
    life_pieces: Optional[int] #absent in pre-SA & UDoALG
    bombs: int
    bomb_pieces: int
    stage_chapter: int
    rank: int
    input: int
    visual_rng: int #not extracted
    replay_rng: int
    pause_state: int

@dataclass
class EnvironmentOffsets:
    character: int
    subshot: int
    difficulty: int
    stage: int

@dataclass
class PlayerOffsets:
    player_pointer: int
    zPlayer_pos: int
    zPlayer_db_timer: int
    zPlayer_state: int
    zPlayer_hit_rad: int
    zPlayer_iframes: int
    zPlayer_focused: int
    zPlayer_option_array: int
    zPlayer_option_array_len: int
    zPlayer_shots_array: int
    zPlayer_shots_array_len: int

@dataclass
class PlayerOptionOffsets:
    zPlayerOption_active: int
    zPlayerOption_anm_id: int #(IDs of VMs)
    zPlayerOption_len: int

@dataclass
class PlayerShotOffsets:
    zPlayerShot_timer: int
    zPlayerShot_pos: int
    zPlayerShot_speed: int
    zPlayerShot_angle: int
    zPlayerShot_vel: int
    zPlayerShot_state: int
    zPlayerShot_damage: int
    zPlayerShot_hitbox: int
    zPlayerShot_len: int

@dataclass
class BombOffsets:
    bomb_pointer: int
    zBomb_state: int

@dataclass
class BulletOffsets:
    bullet_manager_pointer: int
    zBulletManager_list: int
    zBullet_flags: int
    zBullet_iframes: int
    zBullet_pos: int
    zBullet_velocity: int
    zBullet_speed: int
    zBullet_angle: int
    zBullet_hitbox_radius: int
    zBullet_scale: Optional[int] #absent in pre-DDC
    zBullet_state: int
    zBullet_timer: int
    zBullet_type: int
    zBullet_color: int

@dataclass
class EnemyOffsets:
    enemy_manager_pointer: int
    zEnemyManager_ecl_file: int
    zEnemyManager_list: int
    zEclFile_sub_count: int
    zEclFile_subroutines: int
    zEnemy_ecl_ref: int #sub id for games >= lolk, otherwise cur instruction ptr
    zEnemy_data: int
    zEnemyData_pos: int #from "final_pos"
    zEnemyData_vel: int #from "final_pos"
    zEnemyData_hurtbox: int
    zEnemyData_hitbox: int
    zEnemyData_rotation: int
    zEnemyData_anm_vm_id: int #"anm_vm_ids"
    zEnemyData_anm_page: int #"anm_slot_0_index"
    zEnemyData_anm_id: int #"anm_slot_0_script"
    zEnemyData_timer: int
    zEnemyData_movement_bounds: int
    zEnemyData_score_reward: int
    zEnemyData_hp: int
    zEnemyData_hp_max: int
    zEnemyData_drops: int
    zEnemyData_iframes: int
    zEnemyData_flags: int #"flags_low"
    zEnemyData_subboss_id: int
    zEnemyData_special_func: int

@dataclass
class ItemOffsets:
    item_manager_pointer: int
    zItemManager_array: int
    zItemManager_array_len: int
    zItem_state: int
    zItem_type: int
    zItem_pos: int
    zItem_vel: int
    zItem_timer: int
    zItem_len: int

@dataclass
class LaserBaseOffsets:
    laser_manager_pointer: int
    zLaserManager_list: int
    zLaserBaseClass_state: int
    zLaserBaseClass_type: int
    zLaserBaseClass_timer: int
    zLaserBaseClass_offset: int
    zLaserBaseClass_angle: int
    zLaserBaseClass_length: int
    zLaserBaseClass_width: int
    zLaserBaseClass_speed: int
    zLaserBaseClass_iframes: int
    zLaserBaseClass_sprite: int
    zLaserBaseClass_color: int
    zLaserBaseClass_len: int

@dataclass
class LaserLineOffsets:
    zLaserLine_start_pos: int
    zLaserLine_mgr_angle: int
    zLaserLine_max_length: int
    zLaserLine_mgr_speed: int
    zLaserLine_distance: int

@dataclass
class LaserInfiniteOffsets:
    zLaserInfinite_start_pos: int
    zLaserInfinite_velocity: int
    zLaserInfinite_mgr_angle: int
    zLaserInfinite_angle_vel: int
    zLaserInfinite_final_len: int
    zLaserInfinite_mgr_len: int
    zLaserInfinite_final_width: int
    zLaserInfinite_mgr_speed: int
    zLaserInfinite_start_time: int
    zLaserInfinite_expand_time: int
    zLaserInfinite_active_time: int
    zLaserInfinite_shrink_time: int
    zLaserInfinite_mgr_distance: int

@dataclass
class LaserCurveOffsets:
    zLaserCurve_max_length: int
    zLaserCurve_distance: int
    zLaserCurve_array: int

@dataclass
class LaserCurveNodeOffsets:
    zLaserCurveNode_pos: int
    zLaserCurveNode_vel: int
    zLaserCurveNode_angle: int
    zLaserCurveNode_speed: int
    zLaserCurveNode_size: int

@dataclass
class AsciiOffsets:
    ascii_manager_pointer: int
    global_timer: int #frames the ascii manager has been alive (never destroyed)

@dataclass
class AnmOffsets:
    anm_manager_pointer: int
    zAnmManager_list: int
    zAnmVm_rotation_z : int
    zAnmVm_id: int
    zAnmVm_entity_pos: int

@dataclass
class SpellCardOffsets:
    spellcard_pointer: int
    zSpellcard_indicator: int
    zSpellcard_id: int
    zSpellcard_bonus: int

@dataclass
class GUIOffsets:
    gui_pointer: int
    zGui_bosstimer_s: int
    zGui_bosstimer_ms: int
    zGui_bosstimer_drawn: int

@dataclass
class GameThreadOffsets:
    game_thread_pointer: int
    stage_timer: int

@dataclass
class SupervisorOffsets:
    supervisor_addr: int
    zSupervisor_game_mode: int #to relate to the game modes dict in Associations
    zSupervisor_rng_seed: int #based on time when game was launched; never changes; not extracted

@dataclass
class Associations:
    bullet_types: List[Tuple[str, int]]
    enemy_anms: Dict[int, str]
    item_types: Dict[int, str]
    pause_states: List[str]
    game_modes: Dict[int, str]
    characters: List[str]
    subshots: List[str]
    difficulties: List[str]
    zBulletFlags_grazed: int
    zEnemyFlags_no_hurtbox: int
    zEnemyFlags_no_hitbox: int
    zEnemyFlags_invincible: int
    zEnemyFlags_intangible: int
    zEnemyFlags_is_grazeable: int
    zEnemyFlags_is_rectangle: int
    zEnemyFlags_has_move_limit: int
    zEnemyFlags_is_boss: int
    zItemState_autocollect: int
    zItemState_attracted: int
    deathbomb_window_frames: int
    marisa_lower_poc_line: int
    life_piece_req: int
    bomb_piece_req: int
    world_width: int
    world_height: int

@dataclass
class Offset:
    statics: StaticsOffsets
    environment: EnvironmentOffsets
    player: PlayerOffsets
    player_options: PlayerOptionOffsets
    player_shots: PlayerShotOffsets
    bomb: BombOffsets
    bullets: BulletOffsets
    enemies: EnemyOffsets
    items: ItemOffsets
    laser_base: LaserBaseOffsets
    laser_line: LaserLineOffsets
    laser_infinite: LaserInfiniteOffsets
    laser_curve: LaserCurveOffsets
    laser_curve_node: LaserCurveNodeOffsets
    ascii: AsciiOffsets
    anm: AnmOffsets
    spell_card: SpellCardOffsets
    gui: GUIOffsets
    game_thread: GameThreadOffsets
    supervisor: SupervisorOffsets
    associations: Associations
    game_specific: Optional[Dict[str, any]]






## Maps & properties shared between games
# Always re-evaluate when adding new games
bullet_types_post_td = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Small Star CW', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star CW', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Violet Fireball', 0), ('Orange Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Small Star CCW', 16), ('Laser', 16)] #TD only?
bullet_types_post_ddc = bullet_types_post_td + [('Red Note', 0), ('Blue Note', 0), ('Yellow Note', 0), ('Purple Note', 0), ('Rest', 8)] #DDC/ISC
bullet_types_post_lolk = bullet_types_post_ddc[:24] + [('Big Star CCW', 8)] + bullet_types_post_ddc[24:] #LoLK-WBaWC
bullet_types_post_um = bullet_types_post_lolk + [('Yin-Yang CW', 8), ('Yin-Yang CCW', 8), ('Big Yin-Yang CW', 4), ('Big Yin-Yang CCW', 4)] #UM/HBM(?)/UDoALG

enemy_anms_base = {0: "Blue Fairy", 5: "Red Fairy", 10: "Green Fairy", 15: "Yellow Fairy", 20: "Blue Flower Fairy", 25: "Red Flower Fairy", 30: "Maroon Fairy", 35: "Teal Fairy", 40: "Sunflower Fairy"}
enemy_anms_pre_ddc = {**enemy_anms_base, 53: "Red Yin-Yang", 56: "Green Yin-Yang", 59: "Blue Yin-Yang", 62: "Purple Yin-Yang", 65: "Red Yin-Yang", 68: "Green Yin-Yang", 71: "Blue Yin-Yang", 74: "Purple Yin-Yang", 78: "Red Spirit", 79:"Red Spirit", 80: "Green Spirit", 82: "Blue Spirit", 83: "Green Spirit", 87: "Blue Spirit", 91: "Yellow Spirit", 106: "Yellow Spirit", 147: "Blue Hell Fairy", 152: "Red Hell Fairy", 157: "Yellow Hell Fairy", 162: "Purple Fairy", 167: "Hellflower Fairy"}
enemy_anms_post_ddc = {**enemy_anms_pre_ddc, 80: "Red Inverted Spirit", 84: "Green Inverted Spirit", 88: "Blue Inverted Spirit", 92: "Yellow Inverted Spirit"}
enemy_anms_post_wbawc = {**enemy_anms_post_ddc, 172: "Glowing Blue Fairy", 177: "Glowing Red Fairy", 202: "Glowing Maroon Fairy", 212: "Glowing Sunflower Fairy"}
enemy_anms_post_um = {**enemy_anms_post_wbawc, 77: "Red Yin-Yang", 80: "Green Yin-Yang", 91: "Red Spirit", 99: "Blue Spirit", 184: "Blue Glowing Fairy", 189: "Red Glowing Fairy", 214: "Maroon Glowing Fairy", 224: "Glowing Sunflower Fairy"}

item_types_td = {1: "Power", 2: "Point", 3:"Big Power", 4:"Big Point", 5:"Bomb Piece", 6: "Life", 7: "Bomb", 8: "Full Power", 9: "Cancel", 10: "LifeP. Spirit", 11: "Blue Spirit", 12: "BombP. Spirit", 13: "Grey Spirit", 14: "Blue Spirit"} #TD
item_types_post_ddc = {1: "Power", 2: "Point", 3:"Big Power", 4:"Life Piece", 5:"Life", 6:"Bomb Piece", 7:"Bomb", 8:"Full Power", 9:"Green", 10:"Cancel", 11:"Big Cancel", 12:"Undiff. Piece"} #shared DDC-LoLK
item_types_post_hsifs = {**item_types_post_ddc, 10:"Green++", 11:"Cancel", 12:"Cancel++", 13:"Big Cancel", 14:"Big Cancel++", 15:"Bomb Piece"} #shared HSiFS-WBaWC
item_types_post_um = {**item_types_post_hsifs, 2:"Gold"} #shared UM/HBM(?)/UDoALG

modern_pause_states = ["Pause (/Stage Transition/Ending Sequence)", "Not in Run (Main Menu/Game Over/Practice End)", "Actively Playing"]
modern_game_modes = {4: 'Main Menu', 7: 'Game World on Screen', 15: 'Ending Sequence'}

usual_difficulties = ['Easy', 'Normal', 'Hard', 'Lunatic', 'Extra']
difficulties_pre_td = usual_difficulties + ['Phantasm']
difficulties_post_td = usual_difficulties + ['Overdrive']

usual_world_width = 384
usual_world_height = 448

offsets = {

    # TOUHOU 6 -- Embodiment of Scarlet Devil ====================
    #=============================================================
    'th06.exe': None,

    # TOUHOU 7 -- Perfect Cherry Blossom =========================
    #=============================================================
    'th07.exe': None,

    # TOUHOU 8 -- Imperishable Night =============================
    #=============================================================
    'th08.exe': None,

    # TOUHOU 9 -- Phantasmagoria of Flower View ==================
    #=============================================================
    'th09.exe': None,

    # TOUHOU 9.5 -- Shoot the Bullet =============================
    #=============================================================
    'th095.exe': None,

    # TOUHOU 10 -- Mountain of Faith =============================
    #=============================================================
    'th10.exe': None,

    # TOUHOU 11 -- Subterranean Animism ==========================
    #=============================================================
    'th11.exe': None,

    # TOUHOU 12 -- Undefined Fantastic Object ====================
    #=============================================================
    'th12.exe': None,

    # TOUHOU 12.5 -- Double Spoiler ==============================
    #=============================================================
    'th125.exe': None,

    # TOUHOU 12.8 -- Great Fairy Wars ============================
    #=============================================================
    'th128.exe': None,

    # TOUHOU 13 -- Ten Desires ===================================
    #=============================================================
    'th13.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xc0a28,
            score         = 0xbe7c0,
            continues     = 0xbe7c8,
            graze         = 0xbe7d0,
            piv           = 0xbe7dc,
            power         = 0xbe7e8,
            lives         = 0xbe7f4,
            life_pieces   = 0xbe7f8,
            bombs         = 0xbe800,
            bomb_pieces   = 0xbe804,
            stage_chapter = 0xbe824,
            rank          = 0xbe7cc,
            input         = 0xe4c08,
            visual_rng    = 0xdc31c,
            replay_rng    = 0xdc324,
            pause_state   = 0xdf120,
        ),
        environment = EnvironmentOffsets(
            character       = 0xbe7b8,
            subshot         = 0xbe7bc,
            difficulty      = 0xbe7c4,
            stage           = 0xbe81c,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xc22c4,
            zPlayer_pos      = 0x5b8,
            zPlayer_db_timer = 0x668,
            zPlayer_state    = 0x65c,
            zPlayer_hit_rad  = 0x620,
            zPlayer_iframes  = 0x14688,
            zPlayer_focused  = 0x14840,
            zPlayer_option_array     = 0xa2b8,
            zPlayer_option_array_len = 0x8,
            zPlayer_shots_array      = 0x6a0,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xe4,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x1c,
            zPlayerShot_pos    = 0x2c,
            zPlayerShot_speed  = 0x44,
            zPlayerShot_angle  = 0x48,
            zPlayerShot_vel    = 0x60,
            zPlayerShot_state  = 0x70,
            zPlayerShot_damage = 0x84,
            zPlayerShot_hitbox = 0x88,
            zPlayerShot_len    = 0x9c,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xc2170,
            zBomb_state  = 0x40,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xc2174,
            zBulletManager_list    = 0x80,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0xb70,
            zBullet_velocity       = 0xb7c,
            zBullet_speed          = 0xb88,
            zBullet_angle          = 0xb8c,
            zBullet_hitbox_radius  = 0xb90,
            zBullet_scale          = None,
            zBullet_state          = 0xbbe,
            zBullet_timer          = 0x132c,
            zBullet_type           = 0x1354,
            zBullet_color          = 0x1356,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xc2188,
            zEnemyManager_ecl_file = 0xac,
            zEnemyManager_list     = 0xb0,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0xc,
            zEnemy_data            = 0x11ec,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = None, #stored in ANM VM z-rotation
            zEnemyData_anm_vm_id       = 0x120,
            zEnemyData_anm_page        = 0x264,
            zEnemyData_anm_id          = 0x268,
            zEnemyData_timer           = 0x2bc,
            zEnemyData_movement_bounds = 0x3f38,
            zEnemyData_score_reward    = 0x3f48,
            zEnemyData_hp              = 0x3f4c,
            zEnemyData_hp_max          = 0x3f50,
            zEnemyData_drops           = 0x3f68,
            zEnemyData_iframes         = 0x3fd0,
            zEnemyData_flags           = 0x4030,
            zEnemyData_subboss_id      = 0x4040,
            zEnemyData_special_func    = 0x40e8,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xc229c,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0xa58,
            zItem_state = 0xba0,
            zItem_type  = 0xba4,
            zItem_pos   = 0xb5c,
            zItem_vel   = 0xb68,
            zItem_timer = 0xb7c,
            zItem_len   = 0xbc8,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xc22a0,
            zLaserManager_list      = 0x5d0,
            zLaserBaseClass_state   = 0xc,
            zLaserBaseClass_type    = 0x10,
            zLaserBaseClass_timer   = 0x18,
            zLaserBaseClass_offset  = 0x50,
            zLaserBaseClass_angle   = 0x68,
            zLaserBaseClass_length  = 0x6c,
            zLaserBaseClass_width   = 0x70,
            zLaserBaseClass_speed   = 0x74,
            zLaserBaseClass_iframes = 0x5b4,
            zLaserBaseClass_sprite  = 0x5b8,
            zLaserBaseClass_color   = 0x5bc,
            zLaserBaseClass_len     = 0x5c0,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0xe9c,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xc2160,
            global_timer          = 0x19190,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0xdc688,
            zAnmManager_list    = 0xf48208,
            zAnmVm_rotation_z   = 0x50,
            zAnmVm_id           = 0x530,
            zAnmVm_entity_pos   = 0x574,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xc2178,
            zSpellcard_indicator = 0x20,
            zSpellcard_id        = 0x78,
            zSpellcard_bonus     = 0x80,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xc2190,
            zGui_bosstimer_s     = 0x1a0,
            zGui_bosstimer_ms    = 0x1a4,
            zGui_bosstimer_drawn = 0x1ac,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xc2194,
            stage_timer = 0x14,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xdc6a0,
            zSupervisor_game_mode = 0x580,
            zSupervisor_rng_seed  = 0x5c0,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_td,
            enemy_anms    = enemy_anms_pre_ddc,
            item_types    = item_types_td,
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sanae', 'Youmu'],
            subshots      = ['N/A'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2,
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**15,
            zEnemyFlags_has_move_limit = 2**18,
            zEnemyFlags_is_boss        = 2**24,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = False,
            life_piece_req = None, #changes based on extend_count
            bomb_piece_req = 8,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'trance_meter': 0xbe808,
            'trance_state': 0xbe80c,
            'extend_count': 0xbe7fc,
            'life_piece_reqs': [8, 10, 12, 15, 18, 20, 25],
            'spirit_types': ['LifeP.', 'Blue', 'BombP.', 'Gray'],
            'spirit_manager_pointer': 0xc22a4,
            'zSpiritManager_array': 0x14,
            'zSpiritManager_array_len': 0x100,
            'zSpiritManager_spawn_total': 0x8820,
            'zSpiritManager_chain_timer': 0x8828,
            'zSpiritManager_chain_counter': 0x8838,
            'zSpiritItem_state': 0x0, #0 = free, 1 = used/active
            'zSpiritItem_type': 0x4,
            'zSpiritItem_pos': 0x14,
            'zSpiritItem_vel': 0x48,
            'zSpiritItem_timer': 0x60,
            'zSpiritItem_len': 0x88,
            'square_echo_func': 0x422150,
            'inv_square_echo_func': 0x4224b0,
            'circle_echo_func': 0x4228b0,
            'miko_final_func': 0x422d60,
            'zPlayer_youmu_charge_timer': 0x146a4,
            'zEnemyData_f0_echo_x1': 0x298, #if useful in multiple games, add to Enemy offset spec
            'zEnemyData_f1_echo_x2': 0x29c, #if useful in multiple games, add to Enemy offset spec
            'zEnemyData_f2_echo_y1': 0x2a0, #if useful in multiple games, add to Enemy offset spec
            'zEnemyData_f3_echo_y2': 0x2a4, #if useful in multiple games, add to Enemy offset spec
            'zEnemyData_spirit_time_max': 0x3ff4,
            'zEnemyData_max_spirit_count': 0x3ff8,
        }
    ),

    # TOUHOU 14 -- Double Dealing Character ======================
    #=============================================================
    'th14.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xd8f58,
            score         = 0xf5830,
            continues     = 0xf5838,
            graze         = 0xf5840,
            piv           = 0xf584c,
            power         = 0xf5858,
            lives         = 0xf5864,
            life_pieces   = 0xf5868,
            bombs         = 0xf5870,
            bomb_pieces   = 0xf5874,
            stage_chapter = 0xf58ac,
            rank          = 0xf583c,
            input         = 0xd6a90,
            visual_rng    = 0xdb508,
            replay_rng    = 0xdb510,
            pause_state   = 0xf7ac8,
        ),
        environment = EnvironmentOffsets(
            character       = 0xf5828,
            subshot         = 0xf582c,
            difficulty      = 0xf5834,
            stage           = 0xf58a4,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xdb67c,
            zPlayer_pos      = 0x5e0,
            zPlayer_db_timer = 0x690,
            zPlayer_state    = 0x684,
            zPlayer_hit_rad  = 0x648,
            zPlayer_iframes  = 0x182c4,
            zPlayer_focused  = 0x184b0,
            zPlayer_option_array     = 0xd6ec,
            zPlayer_option_array_len = 0x8,
            zPlayer_shots_array      = 0x6c8,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xe4,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x1c,
            zPlayerShot_pos    = 0x54,
            zPlayerShot_speed  = 0x6c,
            zPlayerShot_angle  = 0x70,
            zPlayerShot_vel    = 0x88,
            zPlayerShot_state  = 0x98,
            zPlayerShot_damage = 0xac,
            zPlayerShot_hitbox = 0xb0,
            zPlayerShot_len    = 0xd0,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xdb52c,
            zBomb_state  = 0x40,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xdb530,
            zBulletManager_list    = 0x7c,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0xbc0,
            zBullet_velocity       = 0xbcc,
            zBullet_speed          = 0xbd8,
            zBullet_angle          = 0xbdc,
            zBullet_hitbox_radius  = 0xbe0,
            zBullet_scale          = 0x13bc,
            zBullet_state          = 0xc0e,
            zBullet_timer          = 0x13c4,
            zBullet_type           = 0x13ec,
            zBullet_color          = 0x13ee,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xdb544,
            zEnemyManager_ecl_file = 0xcc,
            zEnemyManager_list     = 0xd0,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0xc,
            zEnemy_data            = 0x11f0,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = 0x120,
            zEnemyData_anm_vm_id       = 0x124,
            zEnemyData_anm_page        = 0x268,
            zEnemyData_anm_id          = 0x26c,
            zEnemyData_timer           = 0x2c0,
            zEnemyData_movement_bounds = 0x3f60,
            zEnemyData_score_reward    = 0x3f70,
            zEnemyData_hp              = 0x3f74,
            zEnemyData_hp_max          = 0x3f78,
            zEnemyData_drops           = 0x3f90,
            zEnemyData_iframes         = 0x3ff0,
            zEnemyData_flags           = 0x4054,
            zEnemyData_subboss_id      = 0x4064,
            zEnemyData_special_func    = 0x410c,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xdb660,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0x1258,
            zItem_state = 0xbf0,
            zItem_type  = 0xbf4,
            zItem_pos   = 0xbac,
            zItem_vel   = 0xbb8,
            zItem_timer = 0xbcc,
            zItem_len   = 0xc18,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xdb664,
            zLaserManager_list      = 0x5d0,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_iframes = 0x5b4,
            zLaserBaseClass_sprite  = 0x5b8,
            zLaserBaseClass_color   = 0x5bc,
            zLaserBaseClass_len     = 0x5c0,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0xeec,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xdb520,
            global_timer          = 0x191e0,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0xf56cc,
            zAnmManager_list    = 0xfe8208,
            zAnmVm_rotation_z   = 0x50,
            zAnmVm_id           = 0x540,
            zAnmVm_entity_pos   = 0x59c,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xdb534,
            zSpellcard_indicator = 0x20,
            zSpellcard_id        = 0x78,
            zSpellcard_bonus     = 0x80,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xdb550,
            zGui_bosstimer_s     = 0x19c,
            zGui_bosstimer_ms    = 0x1a0,
            zGui_bosstimer_drawn = 0x1a8,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xdb558,
            stage_timer = 0x14,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xd8f60,
            zSupervisor_game_mode = 0x6e8,
            zSupervisor_rng_seed  = 0x728,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_ddc,
            enemy_anms    = enemy_anms_post_ddc,
            item_types    = item_types_post_ddc,
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sakuya'],
            subshots      = ['A', 'B'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2,
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**17,
            zEnemyFlags_is_boss        = 2**23,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = True,
            life_piece_req = 3,
            bomb_piece_req = 8,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'zBullet_ex_delay_timer': 0x12ec,
            'seija_anm_pointer': 0xd9128,
            'seija_flip_x': 0x60,
            'seija_flip_y': 0x64,
            'zPlayer_scale': 0x18308,
            'bonus_count': 0xf5894,
            'sukuna_penult_func': 0x42cb00,
        }
    ),

    # TOUHOU 14.3 -- Impossible Spell Card =======================
    #=============================================================
    'th143.exe': None,

    # TOUHOU 15 -- Legacy of Lunatic Kingdom =====================
    #=============================================================
    'th15.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xe73e8,
            score         = 0xe740c,
            continues     = 0xe7414,
            graze         = 0xe741c,
            piv           = 0xe7434,
            power         = 0xe7440,
            lives         = 0xe7450,
            life_pieces   = 0xe7454,
            bombs         = 0xe745c,
            bomb_pieces   = 0xe7460,
            stage_chapter = 0xe73f8,
            rank          = 0xe7418,
            input         = 0xe6f28,
            replay_rng    = 0xe9a48,
            visual_rng    = 0xe9a40,
            pause_state   = 0x11bc60,
        ),
        environment = EnvironmentOffsets(
            character       = 0xe7404,
            subshot         = 0xe7408,
            difficulty      = 0xe7410,
            stage           = 0xe73f0,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xe9bb8,
            zPlayer_pos      = 0x618,
            zPlayer_db_timer = 0x630,
            zPlayer_state    = 0x16220,
            zPlayer_hit_rad  = 0x2bfc8,
            zPlayer_iframes  = 0x16284,
            zPlayer_focused  = 0x16240,
            zPlayer_option_array     = 0x668,
            zPlayer_option_array_len = 0x8,
            zPlayer_shots_array      = 0xd88,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xe4,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x10,
            zPlayerShot_pos    = 0x48,
            zPlayerShot_speed  = 0x60,
            zPlayerShot_angle  = 0x64,
            zPlayerShot_vel    = 0x7c,
            zPlayerShot_state  = 0x8c,
            zPlayerShot_damage = 0x9c,
            zPlayerShot_hitbox = 0xa0,
            zPlayerShot_len    = 0xc0,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xe9a68,
            zBomb_state  = 0x24,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xe9a6c,
            zBulletManager_list    = 0x68,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0xc38,
            zBullet_velocity       = 0xc44,
            zBullet_speed          = 0xc50,
            zBullet_angle          = 0xc54,
            zBullet_hitbox_radius  = 0xc58,
            zBullet_scale          = 0x1438,
            zBullet_state          = 0xc8a,
            zBullet_timer          = 0x146c,
            zBullet_type           = 0x1490,
            zBullet_color          = 0x1492,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xe9a80,
            zEnemyManager_ecl_file = 0x17c,
            zEnemyManager_list     = 0x180,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0x14,
            zEnemy_data            = 0x120c,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = 0x120,
            zEnemyData_anm_vm_id       = 0x124,
            zEnemyData_anm_page        = 0x268,
            zEnemyData_anm_id          = 0x26c,
            zEnemyData_timer           = 0x2c0,
            zEnemyData_movement_bounds = 0x3f60,
            zEnemyData_score_reward    = 0x3f70,
            zEnemyData_hp              = 0x3f74,
            zEnemyData_hp_max          = 0x3f78,
            zEnemyData_drops           = 0x3f90,
            zEnemyData_iframes         = 0x3ffc,
            zEnemyData_flags           = 0x4060,
            zEnemyData_subboss_id      = 0x4070,
            zEnemyData_special_func    = 0x4518,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xe9a9c,
            zItemManager_array     = 0x0,
            zItemManager_array_len = 0x1258,
            zItem_state = 0xc74,
            zItem_type  = 0xc78,
            zItem_pos   = 0xc30,
            zItem_vel   = 0xc3c,
            zItem_timer = 0xc50,
            zItem_len   = 0xc88,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xe9ba0,
            zLaserManager_list      = 0x5e0,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_iframes = 0x5c8,
            zLaserBaseClass_sprite  = 0x5cc,
            zLaserBaseClass_color   = 0x5d0,
            zLaserBaseClass_len     = 0x5d4,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0xf68,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xe9a58,
            global_timer          = 0x19254,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0x103c18,
            zAnmManager_list    = 0xdc,
            zAnmVm_rotation_z   = 0x4c,
            zAnmVm_id           = 0x544,
            zAnmVm_entity_pos   = 0x5ec,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xe9a70,
            zSpellcard_indicator = 0x1c,
            zSpellcard_id        = 0x74,
            zSpellcard_bonus     = 0x7c,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xe9a8c,
            zGui_bosstimer_s     = 0x1c0,
            zGui_bosstimer_ms    = 0x1c4,
            zGui_bosstimer_drawn = 0x1cc,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xe9a94,
            stage_timer = 0x10,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xe77d0,
            zSupervisor_game_mode = 0x6f8,
            zSupervisor_rng_seed  = 0x73c,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_lolk,
            enemy_anms    = enemy_anms_post_ddc,
            item_types    = {**item_types_post_ddc, 13:"Graze"},
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sanae', 'Reisen'],
            subshots      = ['N/A'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2, #note: unused
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**17,
            zEnemyFlags_is_boss        = 2**23,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = True,
            life_piece_req = 3,
            bomb_piece_req = 5,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'time_in_chapter': 0xe7400,
            'chapter_graze': 0xe7420,
            'chapter_enemy_weight_spawned': 0xe7484,
            'chapter_enemy_weight_destroyed': 0xe7488,
            'pointdevice_resets_total': 0xe7594,
            'pointdevice_resets_chapter': 0xe75b8,
            'modeflags': 0xe7794,
            'zBomb_reisen_shields': 0x60,
            'zEnemyData_weight': 0x452c,
            'zBullet_graze_timer': 0x1454,
            'zItemManager_graze_slowdown_factor': 0xe5def0,
            'graze_inferno_func': 0x4318a0,
        }
    ),

    # TOUHOU 16 -- Hidden Star in Four Seasons ===================
    #=============================================================
    'th16.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xa5788,
            score         = 0xa57b0,
            continues     = 0xa57b8,
            graze         = 0xa57c0,
            piv           = 0xa57d8,
            power         = 0xa57e4,
            lives         = 0xa57f4,
            life_pieces   = 0xa57f8,
            bombs         = 0xa5800,
            bomb_pieces   = 0xa5804,
            stage_chapter = 0xa5798,
            rank          = 0xa57bc,
            input         = 0xa52c8,
            visual_rng    = 0xa6d80,
            replay_rng    = 0xa6d88,
            pause_state   = 0xd9d90,
        ),
        environment = EnvironmentOffsets(
            character       = 0xa57a4,
            subshot         = 0xa57ac,
            difficulty      = 0xa57b4,
            stage           = 0xa5790,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xa6ef8,
            zPlayer_pos      = 0x610,
            zPlayer_db_timer = 0x628,
            zPlayer_state    = 0x165a8,
            zPlayer_hit_rad  = 0x2c748,
            zPlayer_iframes  = 0x1663c,
            zPlayer_focused  = 0x165c8,
            zPlayer_option_array     = 0x660,
            zPlayer_option_array_len = 0xc,
            zPlayer_shots_array      = 0x1110,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xe4,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x10,
            zPlayerShot_pos    = 0x48,
            zPlayerShot_speed  = 0x60,
            zPlayerShot_angle  = 0x64,
            zPlayerShot_vel    = 0x7c,
            zPlayerShot_state  = 0x8c,
            zPlayerShot_damage = 0x9c,
            zPlayerShot_hitbox = 0xa0,
            zPlayerShot_len    = 0xc0,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xa6da8,
            zBomb_state  = 0x30,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xa6dac,
            zBulletManager_list    = 0x6c,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0xc20,
            zBullet_velocity       = 0xc2c,
            zBullet_speed          = 0xc38,
            zBullet_angle          = 0xc3c,
            zBullet_hitbox_radius  = 0xc40,
            zBullet_scale          = 0x141c,
            zBullet_state          = 0xc72,
            zBullet_timer          = 0x1450,
            zBullet_type           = 0x1474,
            zBullet_color          = 0x1476,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xa6dc0,
            zEnemyManager_ecl_file = 0x17c,
            zEnemyManager_list     = 0x180,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0x14,
            zEnemy_data            = 0x120c,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = 0x120,
            zEnemyData_anm_vm_id       = 0x124,
            zEnemyData_anm_page        = 0x268,
            zEnemyData_anm_id          = 0x26c,
            zEnemyData_timer           = 0x2d4,
            zEnemyData_movement_bounds = 0x3f60,
            zEnemyData_score_reward    = 0x3f70,
            zEnemyData_hp              = 0x3f74,
            zEnemyData_hp_max          = 0x3f78,
            zEnemyData_drops           = 0x3f90,
            zEnemyData_iframes         = 0x4000,
            zEnemyData_flags           = 0x4060,
            zEnemyData_subboss_id      = 0x4070,
            zEnemyData_special_func    = 0x4518,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xa6ddc,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0x1258,
            zItem_state = 0xc50,
            zItem_type  = 0xc54,
            zItem_pos   = 0xc08,
            zItem_vel   = 0xc14,
            zItem_timer = 0xc2c,
            zItem_len   = 0xc78,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xa6ee0,
            zLaserManager_list      = 0x5e0,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_iframes = 0x5c8,
            zLaserBaseClass_sprite  = 0x5cc,
            zLaserBaseClass_color   = 0x5d0,
            zLaserBaseClass_len     = 0x5d4,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0xf50,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xa6d98,
            global_timer          = 0x1923c,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0xc0f48,
            zAnmManager_list    = 0xdc,
            zAnmVm_rotation_z   = 0x40,
            zAnmVm_id           = 0x538,
            zAnmVm_entity_pos   = 0x5e0,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xa6db0,
            zSpellcard_indicator = 0x1c,
            zSpellcard_id        = 0x74,
            zSpellcard_bonus     = 0x7c,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xa6dcc,
            zGui_bosstimer_s     = 0x1d0,
            zGui_bosstimer_ms    = 0x1d4,
            zGui_bosstimer_drawn = 0x1dc,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xa6dd4,
            stage_timer = 0x10,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xc10d0,
            zSupervisor_game_mode = 0x6f0,
            zSupervisor_rng_seed  = 0x734,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_lolk,
            enemy_anms    = enemy_anms_post_ddc,
            item_types    = {**item_types_post_hsifs, 16:"Season"},
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Cirno', 'Aya', 'Marisa'],
            subshots      = ['Spring', 'Summer', 'Autumn', 'Winter', 'Full'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2,
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**17,
            zEnemyFlags_is_boss        = 2**23,
            zItemState_autocollect  = 4,
            zItemState_attracted    = 5,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = True,
            life_piece_req = None, #note: not in this game
            bomb_piece_req = 5,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'next_extend_score_index': 0xa57fc,
            'extend_scores_maingame': 0x91880,
            'extend_scores_extra': 0x917c4,
            'bullet_typedefs_radius': 0x9f3e4,
            'bullet_typedef_len': 0x114,
            'zEnemyData_season_drop': 0x403c,
            'zSeasonDrop_timer': 0x4,
            'zSeasonDrop_max_time': 0x14,
            'zSeasonDrop_min_count': 0x18,
            'zSeasonDrop_damage_for_drop': 0x1c,
            'zSeasonDrop_total_damage': 0x20,
            'snowman_func': 0x4252d0, #note: snowman state at offset 0xc4c of bullets
            'zPlayer_season_level': 0x1669c,
            'season_power': 0xa5808,
            'season_power_thresholds': 0xa583c,
            'season_disable_func': 0x4253b0,
            'season_bomb_ptr': 0xa6da4,
            'zBomb_timer': 0x38,
        }
    ),

    # TOUHOU 16.5 -- Violet Detector =============================
    #=============================================================
    'th165.exe': None,

    # TOUHOU 17 -- Wily Beast & Weakest Creature =================
    #=============================================================
    'th17.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xb5918,
            score         = 0xb59fc,
            continues     = 0xb5a04,
            graze         = 0xb5a0c,
            piv           = 0xb5a24,
            power         = 0xb5a30,
            lives         = 0xb5a40,
            life_pieces   = 0xb5a44,
            bombs         = 0xb5a4c,
            bomb_pieces   = 0xb5a50,
            stage_chapter = 0xb59e4,
            rank          = 0xb5a08,
            input         = 0xb3448,
            visual_rng    = 0xb7660,
            replay_rng    = 0xb7668,
            pause_state   = 0x124778,
        ),
        environment = EnvironmentOffsets(
            character       = 0xb59f4,
            subshot         = 0xb59f8,
            difficulty      = 0xb5a00,
            stage           = 0xb59dc,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xb77d0,
            zPlayer_pos      = 0x610,
            zPlayer_db_timer = 0x628,
            zPlayer_state    = 0x18db0,
            zPlayer_hit_rad  = 0x18ffc,
            zPlayer_iframes  = 0x18e7c,
            zPlayer_focused  = 0x18dd0,
            zPlayer_option_array     = 0x660,
            zPlayer_option_array_len = 0xc,
            zPlayer_shots_array      = 0x1110,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xe4,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x10,
            zPlayerShot_pos    = 0x48,
            zPlayerShot_speed  = 0x60,
            zPlayerShot_angle  = 0x64,
            zPlayerShot_vel    = 0x7c,
            zPlayerShot_state  = 0x8c,
            zPlayerShot_damage = 0x9c,
            zPlayerShot_hitbox = 0xa0,
            zPlayerShot_len    = 0xe0,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xb7688,
            zBomb_state  = 0x30,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xb768c,
            zBulletManager_list    = 0xbc,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0x62c,
            zBullet_velocity       = 0x638,
            zBullet_speed          = 0x644,
            zBullet_angle          = 0x648,
            zBullet_hitbox_radius  = 0x64c,
            zBullet_scale          = 0xe20,
            zBullet_state          = 0xe50,
            zBullet_timer          = 0xe58,
            zBullet_type           = 0xe80,
            zBullet_color          = 0xe82,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xb76a0,
            zEnemyManager_ecl_file = 0x17c,
            zEnemyManager_list     = 0x180,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0x14,
            zEnemy_data            = 0x120c,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = 0x120,
            zEnemyData_anm_vm_id       = 0x124,
            zEnemyData_anm_page        = 0x268,
            zEnemyData_anm_id          = 0x26c,
            zEnemyData_timer           = 0x2d4,
            zEnemyData_movement_bounds = 0x3f60,
            zEnemyData_score_reward    = 0x3f70,
            zEnemyData_hp              = 0x3f74,
            zEnemyData_hp_max          = 0x3f78,
            zEnemyData_drops           = 0x3f90,
            zEnemyData_iframes         = 0x4044,
            zEnemyData_flags           = 0x4080,
            zEnemyData_subboss_id      = 0x4090,
            zEnemyData_special_func    = 0x4538,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xb76b8,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0x1258,
            zItem_state = 0xc58,
            zItem_type  = 0xc5c,
            zItem_pos   = 0xc10,
            zItem_vel   = 0xc1c,
            zItem_timer = 0xc34,
            zItem_len   = 0xc78,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xb76bc,
            zLaserManager_list      = 0x5e0,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_iframes = 0x5c8,
            zLaserBaseClass_sprite  = 0x5cc,
            zLaserBaseClass_color   = 0x5d0,
            zLaserBaseClass_len     = 0x5d4,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0xf58,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xb7678,
            global_timer          = 0x19244,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0x109a20,
            zAnmManager_list    = 0x6dc,
            zAnmVm_rotation_z   = 0x40,
            zAnmVm_id           = 0x538,
            zAnmVm_entity_pos   = 0x5e4,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xb7690,
            zSpellcard_indicator = 0x1c,
            zSpellcard_id        = 0x74,
            zSpellcard_bonus     = 0x7c,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xb76ac,
            zGui_bosstimer_s     = 0x1c8,
            zGui_bosstimer_ms    = 0x1cc,
            zGui_bosstimer_drawn = 0x1d4,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xb76b0,
            stage_timer = 0x10,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xb5ae0,
            zSupervisor_game_mode = 0x6f0,
            zSupervisor_rng_seed  = 0x734,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_lolk,
            enemy_anms    = enemy_anms_post_wbawc,
            item_types    = {**item_types_post_hsifs, 16:"Stable Wolf Spirit", 17:"Stable Otter Spirit", 18:"Stable Eagle Spirit", 19:"Bomb Spirit", 20:"Life Spirit", 21:"Power Spirit", 22:"Point Spirit", 23:"Jellyfish Spirit", 24:"Cow Spirit", 25:"Chick Spirit", 26:"Tortoise Spirit", 27:"Haniwa Spirit", 28:"Haniwa Horse Spirit", 29:"Chick Trio Spirit", 30:"Wolf Spirit", 31:"Otter Spirit", 32:"Eagle Spirit", 33:"Random Spirit"},
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Youmu'],
            subshots      = ['Wolf', 'Otter', 'Eagle'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2,
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**17,
            zEnemyFlags_is_boss        = 2**23,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = True,
            life_piece_req = 3,
            bomb_piece_req = 3,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'token_types': ["Wolf", "Otter", "Eagle", "Bomb Piece", "Life Piece", "Power Item", "Point Item", "Jellyfish", "Cow", "Chick", "Tortoise", "Haniwa", "Horse", "Chick Trio"],
            'held_token_array': 0xb5a64,
            'token_manager_pointer': 0xb7684,
            'zTokenManager_list': 0x18,
            'zTokenManager_otter_anm_ids': 0x44,
            'zToken_type': 0x14,
            'zToken_pos': 0x18,
            'zToken_base_vel': 0x24,
            'zToken_alive_timer': 0x34,
            'zToken_switch_timer': 0x5c,
            'zToken_flags': 0x6c,

            'hyper_types': ["N/A", "Wolf", "Otter", "Eagle", "Neutral"],
            'hyper_token_spawn_delay': 0xb5a94,
            'hyper_time_remaining': 0xb5aa8,
            'hyper_duration': 0xb5ab8,
            'hyper_type': 0xb5abc,
            'hyper_token_time_bonus': 0xb5ac0,
            'hyper_flags': 0xb5ac4,

            'zAnmVm_rotation': 0x40,
            'zPlayer_youmu_charge_timer': 0x19084,
            'zBulletManager_recent_graze_gains': 0x58,
        }
    ),

    # TOUHOU 18 -- Unconnected Marketeers ========================
    #=============================================================
    'th18.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0xccbf0,
            score         = 0xcccfc,
            continues     = 0xccd04,
            graze         = 0xccd0c,
            piv           = 0xccd24,
            power         = 0xccd38,
            lives         = 0xccd48,
            life_pieces   = 0xccd4c,
            bombs         = 0xccd58,
            bomb_pieces   = 0xccd5c,
            stage_chapter = 0xccce4,
            rank          = 0xccd08,
            input         = 0xca428,
            visual_rng    = 0xcf280,
            replay_rng    = 0xcf288,
            pause_state   = 0x16ad00,
        ),
        environment = EnvironmentOffsets(
            character       = 0xcccf4,
            subshot         = 0xcccf8,
            difficulty      = 0xccd00,
            stage           = 0xcccdc,
        ),
        player = PlayerOffsets(
            player_pointer   = 0xcf410,
            zPlayer_pos      = 0x620,
            zPlayer_db_timer = 0x638,
            zPlayer_state    = 0x476ac,
            zPlayer_hit_rad  = 0x4799c,
            zPlayer_iframes  = 0x47778,
            zPlayer_focused  = 0x476cc,
            zPlayer_option_array     = 0x670,
            zPlayer_option_array_len = 0x10,
            zPlayer_shots_array      = 0x1570,
            zPlayer_shots_array_len  = 0x200,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xb0,
            zPlayerOption_len    = 0xf0,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x10,
            zPlayerShot_pos    = 0x48,
            zPlayerShot_speed  = 0x60,
            zPlayerShot_angle  = 0x64,
            zPlayerShot_vel    = 0x7c,
            zPlayerShot_state  = 0x8c,
            zPlayerShot_damage = 0x9c,
            zPlayerShot_hitbox = 0xa0,
            zPlayerShot_len    = 0xf8,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0xcf2b8,
            zBomb_state  = 0x30,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xcf2bc,
            zBulletManager_list    = 0xbc,
            zBullet_flags          = 0x20,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0x638,
            zBullet_velocity       = 0x644,
            zBullet_speed          = 0x650,
            zBullet_angle          = 0x654,
            zBullet_hitbox_radius  = 0x658,
            zBullet_scale          = 0xf38,
            zBullet_state          = 0xf68,
            zBullet_timer          = 0xf70,
            zBullet_type           = 0xf98,
            zBullet_color          = 0xf9a,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0xcf2d0,
            zEnemyManager_ecl_file = 0x188,
            zEnemyManager_list     = 0x18c,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x8c,
            zEnemy_ecl_ref         = 0x14,
            zEnemy_data            = 0x122c,
            zEnemyData_pos             = 0x44,
            zEnemyData_vel             = 0x78,
            zEnemyData_hurtbox         = 0x110,
            zEnemyData_hitbox          = 0x118,
            zEnemyData_rotation        = 0x120,
            zEnemyData_anm_vm_id       = 0x124,
            zEnemyData_anm_page        = 0x268,
            zEnemyData_anm_id          = 0x26c,
            zEnemyData_timer           = 0x2d4,
            zEnemyData_movement_bounds = 0x4fe0,
            zEnemyData_score_reward    = 0x4ff0,
            zEnemyData_hp              = 0x4ff4,
            zEnemyData_hp_max          = 0x4ff8,
            zEnemyData_drops           = 0x5010,
            zEnemyData_iframes         = 0x50f4,
            zEnemyData_flags           = 0x5130,
            zEnemyData_subboss_id      = 0x5140,
            zEnemyData_special_func    = 0x55e8,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xcf2ec,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0x1258,
            zItem_state = 0xc74,
            zItem_type  = 0xc78,
            zItem_pos   = 0xc2c,
            zItem_vel   = 0xc38,
            zItem_timer = 0xc50,
            zItem_len   = 0xc94,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xcf3f4,
            zLaserManager_list      = 0x794,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_iframes = 0x77c,
            zLaserBaseClass_sprite  = 0x780,
            zLaserBaseClass_color   = 0x784,
            zLaserBaseClass_len     = 0x788,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0x1078,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xcf2ac,
            global_timer          = 0x1925c,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0x11f65c,
            zAnmManager_list    = 0x6f0,
            zAnmVm_rotation_z   = 0x44,
            zAnmVm_id           = 0x544,
            zAnmVm_entity_pos   = 0x5f0,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xcf2c0,
            zSpellcard_indicator = 0x1c,
            zSpellcard_id        = 0x74,
            zSpellcard_bonus     = 0x7c,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xcf2e0,
            zGui_bosstimer_s     = 0x1b8,
            zGui_bosstimer_ms    = 0x1bc,
            zGui_bosstimer_drawn = 0x1c4,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0xcf2e4,
            stage_timer = 0x10,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xccdf0,
            zSupervisor_game_mode = 0x7f4,
            zSupervisor_rng_seed  = 0x838,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_um,
            enemy_anms    = {**enemy_anms_post_um, 229: "Lily", 251: "Jimbo"},
            item_types    = {**item_types_post_um, 16: "LifeP. Card", 17: "BombP. Card", 18: "Gold Card", 19: "Power Card"},
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sakuya', 'Sanae'],
            subshots      = ['N/A'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2,
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**17,
            zEnemyFlags_is_boss        = 2**23,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = None, #changes, see zPlayer_deathbomb_window
            marisa_lower_poc_line   = False,
            life_piece_req = 3,
            bomb_piece_req = 3,
            world_width    = usual_world_width,
            world_height   = usual_world_height,
        ),
        game_specific = {
            'funds': 0xccd34,
            'card_nicknames': {41: "Gap", 42: "Mallet", 43: "Keystone", 44: "Moon", 45: "Miko", 46: "Fang", 47: "Sun", 48: "Lily", 49: "Drum", 50: "Sumireko", 52: "Bottle", 53: "Rice"},
            'zBulletManager_cancel_counter': 0x7a41d0,
            'ability_manager_pointer': 0xcf298,
            'zAbilityManager_list': 0x18,
            'zAbilityManager_total_cards': 0x28,
            'zAbilityManager_total_actives': 0x2c,
            'zAbilityManager_total_equipmt': 0x30,
            'zAbilityManager_total_passive': 0x34,
            'zAbilityManager_selected_active': 0x38,
            'zCard_type': 0x4,
            'zCard_charge': 0x38,
            'zCard_charge_max': 0x48,
            'zCard_name_ptr_ptr': 0x4c,
            'zCard_flags': 0x50,
            'zCard_counter': 0x54, #used by Centipede & Lily
            'zPlayer_deathbomb_window': 0x47908, #15 with Tewi card, 8 otherwise
            'zPlayer_poc_line_height': 0x47998, #224 with Kanako card, 128 otherwise
            'zPlayer_sakuya_knives_angle': 0x4790c,
            'zPlayer_sakuya_knives_spread': 0x47910,
            'asylum_func': 0x438d90,
        }
    ),

    # TOUHOU 19 -- Unfinished Dream of All Living Ghost ==========
    #=============================================================
    'th19.exe': Offset(
        statics = StaticsOffsets(
            game_speed    = 0x1a356c,
            score         = 0x207910,
            continues     = 0x207a9c,
            graze         = 0x20798c,
            piv           = 0x207918, #note: unsure, should always be 0
            power         = 0x207924,
            lives         = 0x207960,
            life_pieces   = None,     #note: not in this game
            bombs         = 0x207974,
            bomb_pieces   = 0x207978,
            stage_chapter = 0x2082cc,
            rank          = 0x207aa0,
            input         = 0x200aec,
            visual_rng    = 0x1ae410,
            replay_rng    = 0x1ae420,
            pause_state   = 0x20b210,
        ),
        environment = EnvironmentOffsets(
            character       = 0x20791c,
            subshot         = 0x207920,
            difficulty      = 0x207a90,
            stage           = 0x2082c0,
        ),
        player = PlayerOffsets(
            player_pointer   = 0x1ae474,
            zPlayer_pos      = 0x68c,
            zPlayer_db_timer = 0x6b8,
            zPlayer_state    = 0x10,
            zPlayer_hit_rad  = 0x20c4,
            zPlayer_iframes  = 0x2078,
            zPlayer_focused  = 0x2070,
            zPlayer_option_array     = 0x700,
            zPlayer_option_array_len = 0x16,
            zPlayer_shots_array      = 0x22f8,
            zPlayer_shots_array_len  = 0x100,
        ),
        player_options = PlayerOptionOffsets(
            zPlayerOption_active = 0x0,
            zPlayerOption_anm_id = 0xdc,
            zPlayerOption_len    = 0x128,
        ),
        player_shots = PlayerShotOffsets(
            zPlayerShot_timer  = 0x1c,
            zPlayerShot_pos    = 0x54,
            zPlayerShot_speed  = 0x6c,
            zPlayerShot_angle  = 0x70,
            zPlayerShot_vel    = 0x8c,
            zPlayerShot_state  = 0x9c,
            zPlayerShot_damage = 0xac,
            zPlayerShot_hitbox = 0xb0,
            zPlayerShot_len    = 0x128,
        ),
        bomb = BombOffsets(
            bomb_pointer = 0x1ae48c,
            zBomb_state  = 0x18,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0x1ae470,
            zBulletManager_list    = 0x8156e0,
            zBullet_flags          = 0x10,
            zBullet_iframes        = 0x14,
            zBullet_pos            = 0x650,
            zBullet_velocity       = 0x65c,
            zBullet_speed          = 0x668,
            zBullet_angle          = 0x670,
            zBullet_hitbox_radius  = 0x674,
            zBullet_scale          = 0xfd4,
            zBullet_state          = 0x1044,
            zBullet_timer          = 0x104c,
            zBullet_type           = 0x1078,
            zBullet_color          = 0x107a,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer  = 0x1ae478,
            zEnemyManager_ecl_file = 0x4b48,
            zEnemyManager_list     = 0x4b50,
            zEclFile_sub_count     = 0x8,
            zEclFile_subroutines   = 0x20c,
            zEnemy_ecl_ref         = 0x14,
            zEnemy_data            = 0x1230,
            zEnemyData_pos             = 0x48,
            zEnemyData_vel             = 0x80,
            zEnemyData_hurtbox         = 0x120,
            zEnemyData_hitbox          = 0x128,
            zEnemyData_rotation        = 0x130,
            zEnemyData_anm_vm_id       = 0x134,
            zEnemyData_anm_page        = 0x278,
            zEnemyData_anm_id          = 0x27c,
            zEnemyData_timer           = 0x2e4,
            zEnemyData_movement_bounds = 0x4ff4,
            zEnemyData_score_reward    = 0x5004,
            zEnemyData_hp              = 0x5008,
            zEnemyData_hp_max          = 0x500c,
            zEnemyData_drops           = 0x5028,
            zEnemyData_iframes         = 0x512c,
            zEnemyData_flags           = 0x516c,
            zEnemyData_subboss_id      = 0x5180,
            zEnemyData_special_func    = 0x5648,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0x1ae47c,
            zItemManager_array     = 0x18,
            zItemManager_array_len = 0x13c,
            zItem_state = 0xcc8,
            zItem_type  = 0xccc,
            zItem_pos   = 0xc80,
            zItem_vel   = 0xc8c,
            zItem_timer = 0xca4,
            zItem_len   = 0xcf0,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0x1ae484,
            zLaserManager_list      = 0x14,
            zLaserBaseClass_state   = 0x1c,
            zLaserBaseClass_type    = 0x20,
            zLaserBaseClass_timer   = 0x28,
            zLaserBaseClass_offset  = 0x60,
            zLaserBaseClass_angle   = 0x78,
            zLaserBaseClass_length  = 0x7c,
            zLaserBaseClass_width   = 0x80,
            zLaserBaseClass_speed   = 0x84,
            zLaserBaseClass_iframes = 0x85c,
            zLaserBaseClass_sprite  = 0x874,
            zLaserBaseClass_color   = 0x878,
            zLaserBaseClass_len     = 0x888,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x0,
            zLaserLine_mgr_angle  = 0xc,
            zLaserLine_max_length = 0x10,
            zLaserLine_mgr_speed  = 0x20,
            zLaserLine_distance   = 0x2c,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x0,
            zLaserInfinite_velocity     = 0xc,
            zLaserInfinite_mgr_angle    = 0x18,
            zLaserInfinite_angle_vel    = 0x1c,
            zLaserInfinite_final_len    = 0x20,
            zLaserInfinite_mgr_len      = 0x24,
            zLaserInfinite_final_width  = 0x28,
            zLaserInfinite_mgr_speed    = 0x2c,
            zLaserInfinite_start_time   = 0x30,
            zLaserInfinite_expand_time  = 0x34,
            zLaserInfinite_active_time  = 0x38,
            zLaserInfinite_shrink_time  = 0x3c,
            zLaserInfinite_mgr_distance = 0x4c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x20,
            zLaserCurve_distance   = 0x24,
            zLaserCurve_array      = 0x10e0,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xc,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1c,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0x1ae444,
            global_timer          = 0x197b4,
        ),
        anm = AnmOffsets(
            anm_manager_pointer = 0x1ae3ac,
            zAnmManager_list    = 0x724,
            zAnmVm_rotation_z   = 0x44,
            zAnmVm_id           = 0x4d8,
            zAnmVm_entity_pos   = 0x614,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0x1ae480,
            zSpellcard_indicator = 0x10,
            zSpellcard_id        = 0x78,
            zSpellcard_bonus     = 0x80,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0x1ae460,
            zGui_bosstimer_s     = 0x68,
            zGui_bosstimer_ms    = 0x6c,
            zGui_bosstimer_drawn = 0x60,
        ),
        game_thread = GameThreadOffsets(
            game_thread_pointer = 0x1ae464,
            stage_timer = 0x14,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0x208380,
            zSupervisor_game_mode = 0x90c,
            zSupervisor_rng_seed  = 0x950,
        ),
        associations = Associations(
            bullet_types  = bullet_types_post_um,
            enemy_anms    = {**enemy_anms_post_um, 265: "Wolf Spirit", 266: "Otter Spirit", 267: "Eagle Spirit", 268: "Tamed Wolf Spirit", 269: "Tamed Otter Spirit", 270: "Tamed Eagle Spirit"},
            item_types    = {**item_types_post_um, 9: "Spirit Power"}, #technically more changes in HBM/UDoALG with bigger-sized spirit power items, but never used afaik
            pause_states  = modern_pause_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sanae', 'Ran', 'Aunn', 'Nazrin', 'Seiran', 'Rin', 'Tsukasa', 'Mamizou', 'Yachie', 'Saki', 'Yuuma', 'Suika', 'Biten', 'Enoko', 'Chiyari', 'Hisami', 'Zanmu'],
            subshots      = ['N/A'],
            difficulties  = difficulties_post_td,
            zBulletFlags_grazed        = 2**2, #note: unused
            zEnemyFlags_no_hurtbox     = 2**0,
            zEnemyFlags_no_hitbox      = 2**1,
            zEnemyFlags_invincible     = 2**4,
            zEnemyFlags_intangible     = 2**5,
            zEnemyFlags_is_grazeable   = 2**9,
            zEnemyFlags_is_rectangle   = 2**12,
            zEnemyFlags_has_move_limit = 2**33,
            zEnemyFlags_is_boss        = 2**6,
            zItemState_autocollect  = 3,
            zItemState_attracted    = 4,
            deathbomb_window_frames = 8,
            marisa_lower_poc_line   = False,
            life_piece_req = None, #note: not in this game
            bomb_piece_req = 3,
            world_width    = 296,
            world_height   = usual_world_height,
        ),
        game_specific = {
            #Struct Members
            'zPlayer_hitstun_status': 0x10,
            'zPlayer_shield_status': 0x18,
            'zPlayer_last_combo_hits': 0x22b4,
            'zPlayer_current_combo_hits': 0x22b8,
            'zPlayer_current_combo_chain': 0x22bc,
            'zBullet_can_gen_items_timer': 0x1004,
            'zBullet_can_gen_items': 0x1018,
            'zEnemyManager_pattern_count': 0x42ac,
            'zItemManager_spawn_total': 0xff8d8,
            'zGaugeManager_charging_bool': 0x2c,
            'zGaugeManager_gauge_charge': 0x94,
            'zGaugeManager_gauge_fill': 0xa4,
            'zAbilityManager_total_cards': 0x2c, #untracked
            'zAnmManager_list_p2': 0x744,
            'zGui_p2_bosstimer_s': 0xd4,
            'zGui_p2_bosstimer_ms': 0xd8,
            'zGui_p2_bosstimer_drawn': 0xcc,
            'zAi_story_mode_pointer': 0x34,
            'zStoryAi_fight_phase': 0x4,
            'zStoryAi_progress_meter': 0x8,

            #P1 Struct Pointers
            'gauge_manager_pointer': 0x1ae488,
            'ability_manager_pointer': 0x1ae490,

            #P2 Struct Pointers
            'p2_bullet_manager_pointer': 0x1ae4ac,
            'p2_player_pointer': 0x1ae4b0,
            'p2_bomb_pointer': 0x1ae4c8,
            'p2_enemy_manager_pointer': 0x1ae4b4,
            'p2_item_manager_pointer': 0x1ae4b8,
            'p2_spellcard_pointer': 0x1ae4bc,
            'p2_laser_manager_pointer': 0x1ae4c0,
            'p2_gauge_manager_pointer': 0x1ae4c4,
            'p2_ability_manager_pointer': 0x1ae4cc,
            'p2_ai_pointer': 0x1ae4e0,

            #P1 (Remaining) Globals
            'charge_attack_threshold': 0x207934, #untracked
            'skill_attack_threshold': 0x207938, #untracked
            'ex_attack_threshold': 0x20793c, #untracked
            'boss_attack_threshold': 0x207940, #untracked
            'ex_attack_level': 0x207944,
            'boss_attack_level': 0x207948,
            'lives_max': 0x207964,
            'pvp_wins': 0x2079c8,

            #P2 Globals
            'p2_input': 0x2018b0,
            'p2_shottype': 0x2079dc, #untracked
            'p2_power': 0x2079e4,
            'p2_charge_attack_threshold': 0x2079f4, #untracked
            'p2_skill_attack_threshold': 0x2079f8, #untracked
            'p2_ex_attack_threshold': 0x2079fc, #untracked
            'p2_boss_attack_threshold': 0x207a00, #untracked
            'p2_ex_attack_level': 0x207a04,
            'p2_boss_attack_level': 0x207a08,
            'p2_lives': 0x207a20,
            'p2_lives_max': 0x207a24,
            'p2_bombs': 0x207a34,
            'p2_bomb_pieces': 0x207a38,
            'p2_graze': 0x207a4c,
            'p2_pvp_wins': 0x207a88,

            #Shared Globals
            'pvp_timer_start': 0x20835c,
            'pvp_timer': 0x208360,
            'rank_max': 0x207aa8,
        }
    ),
}

# Template as of post-HSiFS support
# ==============================
#
#    'thXX.exe': Offset(
#        statics = StaticsOffsets(
#            game_speed    = None,
#            score         = None,
#            continues     = None,
#            graze         = None,
#            piv           = None,
#            power         = None,
#            lives         = None,
#            life_pieces   = None,
#            bombs         = None,
#            bomb_pieces   = None,
#            stage_chapter = None,
#            rank          = None,
#            input         = None,
#            visual_rng    = None,
#            replay_rng    = None,
#            pause_state   = None,
#        ),
#        environment = EnvironmentOffsets(
#            character       = None,
#            subshot         = None,
#            difficulty      = None,
#            stage           = None,
#        ),
#        player = PlayerOffsets(
#            player_pointer   = None,
#            zPlayer_pos      = None,
#            zPlayer_db_timer = None,
#            zPlayer_state    = None,
#            zPlayer_hit_rad  = None,
#            zPlayer_iframes  = None,
#            zPlayer_focused  = None,
#            zPlayer_option_array     = None,
#            zPlayer_option_array_len = None,
#            zPlayer_shots_array      = None,
#            zPlayer_shots_array_len  = None,
#        ),
#        player_options = PlayerOptionOffsets(
#            zPlayerOption_active = None,
#            zPlayerOption_anm_id = None,
#            zPlayerOption_len    = None,
#        ),
#        player_shots = PlayerShotOffsets(
#            zPlayerShot_timer  = None,
#            zPlayerShot_pos    = None,
#            zPlayerShot_speed  = None,
#            zPlayerShot_angle  = None,
#            zPlayerShot_vel    = None,
#            zPlayerShot_state  = None,
#            zPlayerShot_damage = None,
#            zPlayerShot_hitbox = None,
#            zPlayerShot_len    = None,
#        ),
#        bomb = BombOffsets(
#            bomb_pointer = None,
#            zBomb_state  = None,
#        ),
#        bullets = BulletOffsets(
#            bullet_manager_pointer = None,
#            zBulletManager_list    = None,
#            zBullet_flags          = None,
#            zBullet_iframes        = None,
#            zBullet_pos            = None,
#            zBullet_velocity       = None,
#            zBullet_speed          = None,
#            zBullet_angle          = None,
#            zBullet_hitbox_radius  = None,
#            zBullet_scale          = None,
#            zBullet_state          = None,
#            zBullet_timer          = None,
#            zBullet_type           = None,
#            zBullet_color          = None,
#        ),
#        enemies = EnemyOffsets(
#            enemy_manager_pointer  = None,
#            zEnemyManager_ecl_file = None,
#            zEnemyManager_list     = None,
#            zEclFile_sub_count     = None,
#            zEclFile_subroutines   = None,
#            zEnemy_ecl_ref         = None,
#            zEnemy_data            = None,
#            zEnemyData_pos             = None,
#            zEnemyData_vel             = None,
#            zEnemyData_hurtbox         = None,
#            zEnemyData_hitbox          = None,
#            zEnemyData_rotation        = None,
#            zEnemyData_anm_vm_id       = None,
#            zEnemyData_anm_page        = None,
#            zEnemyData_anm_id          = None,
#            zEnemyData_timer           = None,
#            zEnemyData_movement_bounds = None,
#            zEnemyData_score_reward    = None,
#            zEnemyData_hp              = None,
#            zEnemyData_hp_max          = None,
#            zEnemyData_drops           = None,
#            zEnemyData_iframes         = None,
#            zEnemyData_flags           = None,
#            zEnemyData_subboss_id      = None,
#        ),
#        items = ItemOffsets(
#            item_manager_pointer   = None,
#            zItemManager_array     = None,
#            zItemManager_array_len = None,
#            zItem_state = None,
#            zItem_type  = None,
#            zItem_pos   = None,
#            zItem_vel   = None,
#            zItem_timer = None,
#            zItem_len   = None,
#        ),
#        laser_base = LaserBaseOffsets(
#            laser_manager_pointer   = None,
#            zLaserManager_list      = None,
#            zLaserBaseClass_state   = None,
#            zLaserBaseClass_type    = None,
#            zLaserBaseClass_timer   = None,
#            zLaserBaseClass_offset  = None,
#            zLaserBaseClass_angle   = None,
#            zLaserBaseClass_length  = None,
#            zLaserBaseClass_width   = None,
#            zLaserBaseClass_speed   = None,
#            zLaserBaseClass_iframes = None,
#            zLaserBaseClass_sprite  = None,
#            zLaserBaseClass_color   = None,
#            zLaserBaseClass_len     = None,
#        ),
#        laser_line = LaserLineOffsets(
#            zLaserLine_start_pos  = None,
#            zLaserLine_mgr_angle  = None,
#            zLaserLine_max_length = None,
#            zLaserLine_mgr_speed  = None,
#            zLaserLine_distance   = None,
#        ),
#        laser_infinite = LaserInfiniteOffsets(
#            zLaserInfinite_start_pos    = None,
#            zLaserInfinite_velocity     = None,
#            zLaserInfinite_mgr_angle    = None,
#            zLaserInfinite_angle_vel    = None,
#            zLaserInfinite_final_len    = None,
#            zLaserInfinite_mgr_len      = None,
#            zLaserInfinite_final_width  = None,
#            zLaserInfinite_mgr_speed    = None,
#            zLaserInfinite_start_time   = None,
#            zLaserInfinite_expand_time  = None,
#            zLaserInfinite_active_time  = None,
#            zLaserInfinite_shrink_time  = None,
#            zLaserInfinite_mgr_distance = None,
#        ),
#        laser_curve = LaserCurveOffsets(
#            zLaserCurve_max_length = None,
#            zLaserCurve_distance   = None,
#            zLaserCurve_array      = None,
#        ),
#        laser_curve_node = LaserCurveNodeOffsets(
#            zLaserCurveNode_pos   = None,
#            zLaserCurveNode_vel   = None,
#            zLaserCurveNode_angle = None,
#            zLaserCurveNode_speed = None,
#            zLaserCurveNode_size  = None,
#        ),
#        ascii = AsciiOffsets(
#            ascii_manager_pointer = None,
#            global_timer          = None,
#        ),
#        anm = AnmOffsets(
#            anm_manager_pointer = None,
#            zAnmManager_list    = None,
#            zAnmVm_rotation_z   = None,
#            zAnmVm_id           = None,
#            zAnmVm_entity_pos   = None,
#        ),
#        spell_card = SpellCardOffsets(
#            spellcard_pointer    = None,
#            zSpellcard_indicator = None,
#            zSpellcard_id        = None,
#            zSpellcard_bonus     = None,
#        ),
#        gui = GUIOffsets(
#            gui_pointer          = None,
#            zGui_bosstimer_s     = None,
#            zGui_bosstimer_ms    = None,
#            zGui_bosstimer_drawn = None,
#        ),
#        game_thread = GameThreadOffsets(
#            game_thread_pointer = None,
#            stage_timer = None,
#        ),
#        supervisor = SupervisorOffsets(
#            supervisor_addr = None,
#            zSupervisor_game_mode = None,
#            zSupervisor_rng_seed  = None,
#        ),
#        associations = Associations(
#            bullet_types  = None,
#            enemy_anms    = None,
#            item_types    = None,
#            pause_states  = None,
#            game_modes    = None,
#            characters    = None,
#            subshots      = None,
#            difficulties  = None,
#            zBulletFlags_grazed        = None,
#            zEnemyFlags_no_hurtbox     = None,
#            zEnemyFlags_no_hitbox      = None,
#            zEnemyFlags_invincible     = None,
#            zEnemyFlags_intangible     = None,
#            zEnemyFlags_is_grazeable   = None,
#            zEnemyFlags_is_rectangle   = None,
#            zEnemyFlags_has_move_limit = None,
#            zEnemyFlags_is_boss        = None,
#            zItemState_autocollect  = None,
#            zItemState_attracted    = None,
#            deathbomb_window_frames = None,
#            marisa_lower_poc_line   = None,
#            life_piece_req = None,
#            bomb_piece_req = None,
#            world_width    = None,
#            world_height   = None,
#        ),
#        game_specific = { }
#    ),