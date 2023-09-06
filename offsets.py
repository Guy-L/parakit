from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

# offsets & game_entities: Guidelines for Game-Specific Data
# if shared by a majority of windows games (>= 10)
    # offsets.py: defined Optional for all offset objects, set to None when absent
    # game_entities: defined Optional for all game state objects, set to None if offset is None
    
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
    score: int
    graze: int
    piv: int
    power: int
    lives: int
    life_pieces: int
    bombs: int
    bomb_pieces: int
    stage_chapter: int
    time_in_stage: int
    input: int
    rng: int
    game_state: int
    
@dataclass 
class UntrackedStaticsOffsets:
    game_speed: int
    visual_rng: int
    character: int
    subshot: int
    difficulty: int
    rank: int
    stage: int

@dataclass
class PlayerOffsets:
    player_pointer: int
    zPlayer_pos: int
    zPlayer_hit_rad: int
    zPlayer_iframes: int
    zPlayer_focused: int
    
@dataclass 
class BulletOffsets:
    bullet_manager_pointer: int
    zBulletManager_list: int
    zBullet_iframes: int
    zBullet_pos: int
    zBullet_velocity: int
    zBullet_speed: int
    zBullet_angle: int
    zBullet_hitbox_radius: int
    zBullet_scale: int
    zBullet_type: int
    zBullet_color: int
    
@dataclass
class EnemyOffsets:
    enemy_manager_pointer: int
    zEnemyManager_list: int
    zEnemy_data: int
    zEnemy_pos: int
    zEnemy_hurtbox: int
    zEnemy_hitbox: int
    zEnemy_rotation: int
    zEnemy_time: int
    zEnemy_score_reward: int
    zEnemy_hp: int
    zEnemy_hp_max: int
    zEnemy_iframes: int
    zEnemy_flags: int   #"flags_low" contains the useful stuff
    zEnemy_subboss_id: int
    
@dataclass
class ItemOffsets:
    item_manager_pointer: int
    zItemManager_array: int
    zItemManager_array_len: int
    zItem_len: int
    zItem_state: int
    zItem_type: int
    zItem_pos: int
    zItem_vel: int
    
@dataclass
class LaserBaseOffsets:
    laser_manager_pointer: int
    zLaserManager_list: int
    zLaserBaseClass_next: int
    zLaserBaseClass_state: int
    zLaserBaseClass_type: int
    zLaserBaseClass_timer: int
    zLaserBaseClass_offset: int
    zLaserBaseClass_angle: int
    zLaserBaseClass_length: int
    zLaserBaseClass_width: int
    zLaserBaseClass_speed: int
    zLaserBaseClass_id: int
    zLaserBaseClass_iframes: int
    zLaserBaseClass_sprite: int
    zLaserBaseClass_color: int
    
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
class SupervisorOffsets:
    supervisor_addr: int
    game_mode: int #to relate to the game modes dict in Associations 
    rng_seed: int #based on time when game was launched; never changes
    
@dataclass
class Associations:
    color_coin: List[str] #color type '3'
    color4: List[str]
    color8: List[str]
    color16: List[str]
    sprites: List[Tuple[str, int]]
    curve_sprites: List[str]
    item_types: Dict[int, str]
    game_states: List[str]
    game_modes: Dict[int, str]
    characters: List[str]
    subshots: List[str]
    difficulties: List[str]
    zEnemyFlags_is_boss: int
    zEnemyFlags_intangible: int
    zEnemyFlags_no_hitbox: int
    life_piece_req: int
    bomb_piece_req: int
    
@dataclass
class Offset:
    statics: StaticsOffsets
    statics_untracked: UntrackedStaticsOffsets
    player: PlayerOffsets
    bullets: BulletOffsets
    enemies: EnemyOffsets
    items: ItemOffsets
    laser_base: LaserBaseOffsets
    laser_line: LaserLineOffsets
    laser_infinite: LaserInfiniteOffsets
    laser_curve: LaserCurveOffsets
    laser_curve_node: LaserCurveNodeOffsets
    ascii: AsciiOffsets
    spell_card: SpellCardOffsets
    gui: GUIOffsets
    supervisor: SupervisorOffsets
    associations: Associations
    game_specific: Optional[Dict[str, any]]






## Association arrays that are shared between games.
# Assuming these are the same between UM and DDC until proven otherwise 
# If proven otherwise then just define it seperately in both instances
# If any of these don't change at all in any game, remove from offset class
modern_color_coin = ['Gold', 'Silver', 'Bronze']
modern_color4 = ['Red', 'Blue', 'Green', 'Yellow']     
modern_color8 = ['Black', 'Red', 'Pink', 'Blue', 'Cyan', 'Green', 'Yellow', 'White'] 
modern_color16 = ['Black', 'Dark Red', 'Red', 'Purple', 'Pink', 'Dark Blue', 'Blue', 'Dark Cyan', 'Cyan', 'Dark Green', 'Green', 'Lime', 'Dark Yellow', 'Yellow', 'Orange', 'White'] 


#re-evaluate when adding new modern games.
modern_sprites_pre_lolk = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Small Star CW', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Violet Fireball', 0), ('Yellow Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Small Star CCW', 16), ('Laser', 16), ('Red Note', 0), ('Blue Note', 0), ('Yellow Note', 0), ('Purple Note', 0), ('Rest', 8)] #assuming the second spinning star came with lolk
modern_sprites_post_lolk = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Small Star CW', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star CW', 8), ('Big Star CCW', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Violet Fireball', 0), ('Yellow Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Small Star CCW', 16), ('Laser', 16), ('Red Note', 0), ('Blue Note', 0), ('Yellow Note', 0), ('Purple Note', 0), ('Rest', 8)] #if yin-yangs stay, define another for post-UM
modern_curve_sprites = ['Standard', 'Thunder']

modern_item_types = {1: "Power", 2: "Point", 3:"Full Power", 4:"Life Piece", 6:"Bomb Piece", 9:"Green", 10:"Cancel"} #if this is only DDC, move it to DDC
modern_game_states = ["Pause (/Stage Transition/Ending Sequence)", "Not in Run (Main Menu/Game Over/Practice End)", "Actively Playing"]
modern_game_modes = {4: 'Main Menu', 7: 'Game World on Screen', 15: 'Ending Sequence'}

usual_difficulties = ['Easy', 'Normal', 'Hard', 'Lunatic', 'Extra']

## The mother of all dictionaries...

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
    'th13.exe': None,

    # TOUHOU 14 -- Double Dealing Character ======================
    #=============================================================
    'th14.exe': Offset( 
        statics = StaticsOffsets(
            score         = 0xf5830,
            graze         = 0xf5840,
            piv           = 0xf584C,
            power         = 0xf5858,
            lives         = 0xf5864,
            life_pieces   = 0xf5868,
            bombs         = 0xf5870,
            bomb_pieces   = 0xf5874,
            stage_chapter = 0xf58ac,
            time_in_stage = 0xf58b0,
            input         = 0xd6a90,
            rng           = 0xdb510,
            game_state    = 0xf7ac8,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = 0xd8f58,
            visual_rng      = 0xdb508,
            character       = 0xf5828,
            subshot         = 0xf582c,
            difficulty      = 0xf5834,
            rank            = 0xf583c,
            stage           = 0xf58a4,
        ),
        player = PlayerOffsets(
            player_pointer  = 0xdb67C,
            zPlayer_pos     = 0x5e0,
            zPlayer_hit_rad = 0x648,
            zPlayer_iframes = 0x182c4,
            zPlayer_focused = 0x184b0,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xdb530,
            zBulletManager_list    = 0x7c,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0xbc0,
            zBullet_velocity       = 0xbcc,
            zBullet_speed          = 0xbd8,
            zBullet_angle          = 0xbdc,
            zBullet_hitbox_radius  = 0xbe0,
            zBullet_scale          = 0x13bc,
            zBullet_type           = 0x13ec,
            zBullet_color          = 0x13ee,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer = 0xdb544,
            zEnemyManager_list    = 0xd0,
            zEnemy_data           = 0x11f0,
            zEnemy_pos            = 0x11f0 + 0x44,
            zEnemy_hurtbox        = 0x11f0 + 0x110,
            zEnemy_hitbox         = 0x11f0 + 0x118,
            zEnemy_rotation       = 0x11f0 + 0x120,
            zEnemy_time           = 0x11f0 + 0x2bc + 0x4,
            zEnemy_score_reward   = 0x11f0 + 0x3f70,
            zEnemy_hp             = 0x11f0 + 0x3f74,
            zEnemy_hp_max         = 0x11f0 + 0x3f78,
            zEnemy_iframes        = 0x11f0 + 0x3ff0,
            zEnemy_flags          = 0x11f0 + 0x4054,
            zEnemy_subboss_id     = 0x11f0 + 0x4064,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xdb660,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0xddd854,
            zItem_len              = 0xc18,
            zItem_state            = 0xbf0,
            zItem_type             = 0xbf4,
            zItem_pos              = 0xbac,
            zItem_vel              = 0xbb8,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xdb664,
            zLaserManager_list      = 0x5d0,
            zLaserBaseClass_next    = 0x4,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1c,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6c,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_id      = 0x80,
            zLaserBaseClass_iframes = 0x5b4,
            zLaserBaseClass_sprite  = 0x5b8,
            zLaserBaseClass_color   = 0x5bc,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x5c0,
            zLaserLine_mgr_angle  = 0x5cc,
            zLaserLine_max_length = 0x5d0,
            zLaserLine_mgr_speed  = 0x5e0,
            zLaserLine_distance   = 0x5ec,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x5c0,
            zLaserInfinite_velocity     = 0x5cc,
            zLaserInfinite_mgr_angle    = 0x5d8,
            zLaserInfinite_angle_vel    = 0x5dc,
            zLaserInfinite_final_len    = 0x5e0,
            zLaserInfinite_mgr_len      = 0x5e4,
            zLaserInfinite_final_width  = 0x5e8,
            zLaserInfinite_mgr_speed    = 0x5ec,
            zLaserInfinite_start_time   = 0x5f0,
            zLaserInfinite_expand_time  = 0x5f4,
            zLaserInfinite_active_time  = 0x5f8,
            zLaserInfinite_shrink_time  = 0x5fc,
            zLaserInfinite_mgr_distance = 0x60c,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x5e0,
            zLaserCurve_distance   = 0x5e4,
            zLaserCurve_array      = 0x14ac,
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
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xd8f60,
            game_mode       = 0xd8f60 + 0x6e8,
            rng_seed        = 0xd8f60 + 0x728
        ),
        associations = Associations(
            color_coin    = modern_color_coin, 
            color4        = modern_color4, 
            color8        = modern_color8, 
            color16       = modern_color16, 
            sprites       = modern_sprites_pre_lolk, 
            curve_sprites = modern_curve_sprites, 
            item_types    = modern_item_types, 
            game_states   = modern_game_states,
            game_modes    = modern_game_modes, 
            characters    = ['Reimu', 'Marisa', 'Sakuya'],
            subshots      = ['A', 'B'],
            difficulties  = usual_difficulties,
            zEnemyFlags_is_boss    = 0x800000,
            zEnemyFlags_intangible = 0x20,
            zEnemyFlags_no_hitbox  = 0x2,
            life_piece_req = 3,
            bomb_piece_req = 8,
        ),
        game_specific = {
            'zBullet_ex_delay_timer': 0x12ec,
            'seija_anm_pointer':  0xd8f60 + 0x1c8,
            'seija_flip_x':       0x60,
            'seija_flip_y':       0x64,
            'zPlayer_scale':      0x18308,
            'bonus_count':        0xf5894,
        }
    ),
    
    # TOUHOU 14.3 -- Impossible Spell Card =======================
    #=============================================================
    'th143.exe': None,
    
    # TOUHOU 15 -- Legacy of Lunatic Kingdom =====================
    #=============================================================
    'th15.exe': Offset(
        statics = StaticsOffsets(
            score         = None,
            graze         = None,
            piv           = None,
            power         = None,
            lives         = None,
            life_pieces   = None,
            bombs         = None,
            bomb_pieces   = None,
            stage_chapter = None,
            time_in_stage = None,
            input         = None,
            rng           = None,
            game_state    = None,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = None,
            visual_rng      = None,
            character       = None,
            subshot         = None,
            difficulty      = None,
            rank            = None,
            stage           = None,
        ),
        player = PlayerOffsets(
            player_pointer  = None,
            zPlayer_pos     = None,
            zPlayer_hit_rad = None,
            zPlayer_iframes = None,
            zPlayer_focused = None,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = None,
            zBulletManager_list    = None,
            zBullet_iframes        = None,
            zBullet_pos            = None,
            zBullet_velocity       = None,
            zBullet_speed          = None,
            zBullet_angle          = None,
            zBullet_hitbox_radius  = None,
            zBullet_scale          = None,
            zBullet_type           = None,
            zBullet_color          = None,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer = None,
            zEnemyManager_list    = None,
            zEnemy_data           = None,
            zEnemy_pos            = None,
            zEnemy_hurtbox        = None,
            zEnemy_hitbox         = None,
            zEnemy_rotation       = None,
            zEnemy_time           = None,
            zEnemy_score_reward   = None,
            zEnemy_hp             = None,
            zEnemy_hp_max         = None,
            zEnemy_iframes        = None,
            zEnemy_flags          = None,
            zEnemy_subboss_id     = None,
        ),
        items = ItemOffsets(
            item_manager_pointer   = None,
            zItemManager_array     = None,
            zItemManager_array_len = None,
            zItem_len              = None,
            zItem_state            = None,
            zItem_type             = None,
            zItem_pos              = None,
            zItem_vel              = None,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = None,
            zLaserManager_list      = None,
            zLaserBaseClass_next    = None,
            zLaserBaseClass_state   = None,
            zLaserBaseClass_type    = None,
            zLaserBaseClass_timer   = None,
            zLaserBaseClass_offset  = None,
            zLaserBaseClass_angle   = None,
            zLaserBaseClass_length  = None,
            zLaserBaseClass_width   = None,
            zLaserBaseClass_speed   = None,
            zLaserBaseClass_id      = None,
            zLaserBaseClass_iframes = None,
            zLaserBaseClass_sprite  = None,
            zLaserBaseClass_color   = None,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = None,
            zLaserLine_mgr_angle  = None,
            zLaserLine_max_length = None,
            zLaserLine_mgr_speed  = None,
            zLaserLine_distance   = None,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = None,
            zLaserInfinite_velocity     = None,
            zLaserInfinite_mgr_angle    = None,
            zLaserInfinite_angle_vel    = None,
            zLaserInfinite_final_len    = None,
            zLaserInfinite_mgr_len      = None,
            zLaserInfinite_final_width  = None,
            zLaserInfinite_mgr_speed    = None,
            zLaserInfinite_start_time   = None,
            zLaserInfinite_expand_time  = None,
            zLaserInfinite_active_time  = None,
            zLaserInfinite_shrink_time  = None,
            zLaserInfinite_mgr_distance = None,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = None,
            zLaserCurve_distance   = None,
            zLaserCurve_array      = None,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = None,
            zLaserCurveNode_vel   = None,
            zLaserCurveNode_angle = None,
            zLaserCurveNode_speed = None,
            zLaserCurveNode_size  = None,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = None,
            global_timer          = None,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = None,
            zSpellcard_indicator = None,
            zSpellcard_id        = None,
            zSpellcard_bonus     = None,
        ),
        gui = GUIOffsets(
            gui_pointer          = None,
            zGui_bosstimer_s     = None,
            zGui_bosstimer_ms    = None,
            zGui_bosstimer_drawn = None,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = None,
            game_mode       = None,
            rng_seed        = None,
        ),
        associations = Associations(
            color_coin    = None,
            color4        = None,
            color8        = None,
            color16       = None,
            sprites       = None,
            curve_sprites = None,
            item_types    = None,
            game_states   = None,
            game_modes    = None,
            characters    = None,
            subshots      = None,
            difficulties  = None,
            zEnemyFlags_is_boss    = None,
            zEnemyFlags_intangible = None,
            zEnemyFlags_no_hitbox  = None,
            life_piece_req = None,
            bomb_piece_req = None,
        ),
        game_specific = { }
    ),
    
    # TOUHOU 16 -- Hidden Star in Four Seasons ===================
    #=============================================================
    'th16.exe': None,
    
    # TOUHOU 16.5 -- Violet Detector =============================
    #=============================================================
    'th165.exe': None,
    
    # TOUHOU 17 -- Wily Beast & Weakest Creature =================
    #=============================================================
    'th17.exe': None,
       
    # TOUHOU 18 -- Unconnected Marketeers ========================
    #=============================================================
    'th18.exe': Offset( 
        statics = StaticsOffsets(
            score         = 0xCCCFC,
            graze         = 0xCCD0C,
            piv           = 0xCCD24,
            power         = 0xCCD38,
            lives         = 0xCCD48,
            life_pieces   = 0xCCD4C,
            bombs         = 0xCCD58,
            bomb_pieces   = 0xCCD5C,
            stage_chapter = 0xCCCE4,
            time_in_stage = 0xCCCE8, #to verify
            input         = 0xCA428,
            rng           = 0xDB510,
            game_state    = 0x16AD00,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = 0xCCBF0,
            visual_rng      = 0xDB508,
            character       = 0xCCCF4,
            subshot         = 0xCCCF8,
            difficulty      = 0xCCD00,
            rank            = 0xCCD08,
            stage           = 0xCCCDC,
        ),
        player = PlayerOffsets(
            player_pointer  = 0xCF410,
            zPlayer_pos     = 0x620,
            zPlayer_hit_rad = 0x4799C,
            zPlayer_iframes = 0x47778,
            zPlayer_focused = 0x476CC,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = 0xCF2BC,
            zBulletManager_list    = 0xBC,
            zBullet_iframes        = 0x24,
            zBullet_pos            = 0x638,
            zBullet_velocity       = 0x644,
            zBullet_speed          = 0x650,
            zBullet_angle          = 0x654,
            zBullet_hitbox_radius  = 0x658,
            zBullet_scale          = 0xF38,
            zBullet_type           = 0xF98,
            zBullet_color          = 0xF9A,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer = 0xCF2D0,
            zEnemyManager_list    = 0x18C,
            zEnemy_data           = 0x122C,
            zEnemy_pos            = 0x122C + 0x44,
            zEnemy_hurtbox        = 0x122C + 0x110,
            zEnemy_hitbox         = 0x122C + 0x118,
            zEnemy_rotation       = 0x122C + 0x120,
            zEnemy_time           = 0x122C + 0x2C0,
            zEnemy_score_reward   = 0x122C + 0x4FF0,
            zEnemy_hp             = 0x122C + 0x4FF4,
            zEnemy_hp_max         = 0x122C + 0x4FF8,
            zEnemy_iframes        = 0x122C + 0x50F4,
            zEnemy_flags          = 0x122C + 0x5130,
            zEnemy_subboss_id     = 0x122C + 0x5140,
        ),
        items = ItemOffsets(
            item_manager_pointer   = 0xCF2EC,
            zItemManager_array     = 0x14,
            zItemManager_array_len = 0xE6BAF4,
            zItem_len              = 0xC94,
            zItem_state            = 0xC74,
            zItem_type             = 0xC78,
            zItem_pos              = 0xC2C,
            zItem_vel              = 0xC38,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = 0xCF3F4,
            zLaserManager_list      = 0x794,
            zLaserBaseClass_next    = 0x4,
            zLaserBaseClass_state   = 0x10,
            zLaserBaseClass_type    = 0x14,
            zLaserBaseClass_timer   = 0x1C,
            zLaserBaseClass_offset  = 0x54,
            zLaserBaseClass_angle   = 0x6C,
            zLaserBaseClass_length  = 0x70,
            zLaserBaseClass_width   = 0x74,
            zLaserBaseClass_speed   = 0x78,
            zLaserBaseClass_id      = 0x80,
            zLaserBaseClass_iframes = 0x77C,
            zLaserBaseClass_sprite  = 0x780,
            zLaserBaseClass_color   = 0x784,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = 0x788,
            zLaserLine_mgr_angle  = 0x794,
            zLaserLine_max_length = 0x798,
            zLaserLine_mgr_speed  = 0x7A8,
            zLaserLine_distance   = 0x7B4,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = 0x788,
            zLaserInfinite_velocity     = 0x794,
            zLaserInfinite_mgr_angle    = 0x7A0,
            zLaserInfinite_angle_vel    = 0x7A4,
            zLaserInfinite_final_len    = 0x7A8,
            zLaserInfinite_mgr_len      = 0x7AC,
            zLaserInfinite_final_width  = 0x7B0,
            zLaserInfinite_mgr_speed    = 0x7B4,
            zLaserInfinite_start_time   = 0x7B8,
            zLaserInfinite_expand_time  = 0x7BC,
            zLaserInfinite_active_time  = 0x7C0,
            zLaserInfinite_shrink_time  = 0x7C4,
            zLaserInfinite_mgr_distance = 0x7D4,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = 0x7A8,
            zLaserCurve_distance   = 0x7AC,
            zLaserCurve_array      = 0x1800,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = 0x0,
            zLaserCurveNode_vel   = 0xC,
            zLaserCurveNode_angle = 0x18,
            zLaserCurveNode_speed = 0x1C,
            zLaserCurveNode_size  = 0x20,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = 0xCF2AC,
            global_timer          = 0x1925C,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = 0xCF2C0,
            zSpellcard_indicator = 0x1c, #game code seem to use 0x78, to check (cf. instruction @ 0x423756 in PseudoC)
            zSpellcard_id        = 0x74,
            zSpellcard_bonus     = 0x7C,
        ),
        gui = GUIOffsets(
            gui_pointer          = 0xCF2E0,
            zGui_bosstimer_s     = 0x1B8,
            zGui_bosstimer_ms    = 0x1BC,
            zGui_bosstimer_drawn = 0x1C4,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = 0xCCDF0,
            game_mode       = 0xCCDF0 + 0x7F4,
            rng_seed        = 0xCCDF0 + 0x838,
        ),
        associations = Associations(
            color_coin    = modern_color_coin,
            color4        = modern_color4,
            color8        = modern_color8,
            color16       = modern_color16,
            sprites       = modern_sprites_post_lolk + [('Yin-Yang CW', 8), ('Yin-Yang CCW', 8), ('Big Yin-Yang CW', 4), ('Big Yin-Yang CCW', 4)],
            curve_sprites = modern_curve_sprites,
            item_types    = {1: "Power", 2: "Gold", 3: "Full Power", 4: "Life Piece", 6: "Bomb Piece", 9: "Green", 16: "LifeP. Card", 17: "BombP. Card", 18: "Gold Card", 19: "Power Card"}, 
            game_states   = modern_game_states,
            game_modes    = modern_game_modes,
            characters    = ['Reimu', 'Marisa', 'Sakuya', 'Sanae'],
            subshots      = ['N/A'],
            difficulties  = usual_difficulties,
            zEnemyFlags_is_boss    = 0x800000,
            zEnemyFlags_intangible = 0x20,
            zEnemyFlags_no_hitbox  = 0x2,
            life_piece_req = 3,
            bomb_piece_req = 3,
        ),
        game_specific = {
            'funds': 0xCCD34,
            'card_nicknames': {41: "Gap", 42: "Mallet", 43: "Keystone", 44: "Moon", 45: "Miko", 46: "Fang", 47: "Sun", 48: "Lily", 49: "Drum", 50: "Sumireko", 52: "Bottle", 53: "Rice"},
            'ability_manager_pointer': 0xCF298,
            'zAbilityManager_list': 0x18,
            'zAbilityManager_total_cards': 0x28,
            'zAbilityManager_total_actives': 0x2C,
            'zAbilityManager_total_equipmt': 0x30,
            'zAbilityManager_total_passive': 0x34,
            'zAbilityManager_selected_active': 0x38,
            'zCard_id': 0x4,
            'zCard_charge': 0x38,
            'zCard_charge_max': 0x48,
            'zCard_name_pointer_pointer': 0x4C,
            'zCard_counter': 0x54, #used by Centipede & Lily
        }
    ),
    
    # TOUHOU 19 -- Unfinished Dream of All Living Ghost ==========
    #=============================================================
    'th19.exe': Offset( 
        statics = StaticsOffsets(
            score         = None,
            graze         = None,
            piv           = None,
            power         = None,
            lives         = None,
            life_pieces   = None,
            bombs         = None,
            bomb_pieces   = None,
            stage_chapter = None,
            time_in_stage = None,
            input         = None,
            rng           = None,
            game_state    = None,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = None,
            visual_rng      = None,
            character       = None,
            subshot         = None,
            difficulty      = None,
            rank            = None,
            stage           = None,
        ),
        player = PlayerOffsets(
            player_pointer  = None,
            zPlayer_pos     = None,
            zPlayer_hit_rad = None,
            zPlayer_iframes = None,
            zPlayer_focused = None,
        ),
        bullets = BulletOffsets(
            bullet_manager_pointer = None,
            zBulletManager_list    = None,
            zBullet_iframes        = None,
            zBullet_pos            = None,
            zBullet_velocity       = None,
            zBullet_speed          = None,
            zBullet_angle          = None,
            zBullet_hitbox_radius  = None,
            zBullet_scale          = None,
            zBullet_type           = None,
            zBullet_color          = None,
        ),
        enemies = EnemyOffsets(
            enemy_manager_pointer = None,
            zEnemyManager_list    = None,
            zEnemy_data           = None,
            zEnemy_pos            = None,
            zEnemy_hurtbox        = None,
            zEnemy_hitbox         = None,
            zEnemy_rotation       = None,
            zEnemy_time           = None,
            zEnemy_score_reward   = None,
            zEnemy_hp             = None,
            zEnemy_hp_max         = None,
            zEnemy_iframes        = None,
            zEnemy_flags          = None,
            zEnemy_subboss_id     = None,
        ),
        items = ItemOffsets(
            item_manager_pointer   = None,
            zItemManager_array     = None,
            zItemManager_array_len = None,
            zItem_len              = None,
            zItem_state            = None,
            zItem_type             = None,
            zItem_pos              = None,
            zItem_vel              = None,
        ),
        laser_base = LaserBaseOffsets(
            laser_manager_pointer   = None,
            zLaserManager_list      = None,
            zLaserBaseClass_next    = None,
            zLaserBaseClass_state   = None,
            zLaserBaseClass_type    = None,
            zLaserBaseClass_timer   = None,
            zLaserBaseClass_offset  = None,
            zLaserBaseClass_angle   = None,
            zLaserBaseClass_length  = None,
            zLaserBaseClass_width   = None,
            zLaserBaseClass_speed   = None,
            zLaserBaseClass_id      = None,
            zLaserBaseClass_iframes = None,
            zLaserBaseClass_sprite  = None,
            zLaserBaseClass_color   = None,
        ),
        laser_line = LaserLineOffsets(
            zLaserLine_start_pos  = None,
            zLaserLine_mgr_angle  = None,
            zLaserLine_max_length = None,
            zLaserLine_mgr_speed  = None,
            zLaserLine_distance   = None,
        ),
        laser_infinite = LaserInfiniteOffsets(
            zLaserInfinite_start_pos    = None,
            zLaserInfinite_velocity     = None,
            zLaserInfinite_mgr_angle    = None,
            zLaserInfinite_angle_vel    = None,
            zLaserInfinite_final_len    = None,
            zLaserInfinite_mgr_len      = None,
            zLaserInfinite_final_width  = None,
            zLaserInfinite_mgr_speed    = None,
            zLaserInfinite_start_time   = None,
            zLaserInfinite_expand_time  = None,
            zLaserInfinite_active_time  = None,
            zLaserInfinite_shrink_time  = None,
            zLaserInfinite_mgr_distance = None,
        ),
        laser_curve = LaserCurveOffsets(
            zLaserCurve_max_length = None,
            zLaserCurve_distance   = None,
            zLaserCurve_array      = None,
        ),
        laser_curve_node = LaserCurveNodeOffsets(
            zLaserCurveNode_pos   = None,
            zLaserCurveNode_vel   = None,
            zLaserCurveNode_angle = None,
            zLaserCurveNode_speed = None,
            zLaserCurveNode_size  = None,
        ),
        ascii = AsciiOffsets(
            ascii_manager_pointer = None,
            global_timer          = None,
        ),
        spell_card = SpellCardOffsets(
            spellcard_pointer    = None,
            zSpellcard_indicator = None,
            zSpellcard_id        = None,
            zSpellcard_bonus     = None,
        ),
        gui = GUIOffsets(
            gui_pointer          = None,
            zGui_bosstimer_s     = None,
            zGui_bosstimer_ms    = None,
            zGui_bosstimer_drawn = None,
        ),
        supervisor = SupervisorOffsets(
            supervisor_addr = None,
            game_mode       = None,
            rng_seed        = None,
        ),
        associations = Associations(
            color_coin    = None,
            color4        = None,
            color8        = None,
            color16       = None,
            sprites       = None,
            curve_sprites = None,
            item_types    = None,
            game_states   = None,
            game_modes    = None,
            characters    = None,
            subshots      = None,
            difficulties  = None,
            zEnemyFlags_is_boss    = None,
            zEnemyFlags_intangible = None,
            zEnemyFlags_no_hitbox  = None,
            life_piece_req = None,
            bomb_piece_req = None,
        ),
        game_specific = { }
    ),
}

# Template as of post-UM support
# ==============================
# 
#    'thXX.exe': Offset(
#        statics = StaticsOffsets(
#            score         = None,
#            graze         = None,
#            piv           = None,
#            power         = None,
#            lives         = None,
#            life_pieces   = None,
#            bombs         = None,
#            bomb_pieces   = None,
#            stage_chapter = None,
#            time_in_stage = None,
#            input         = None,
#            rng           = None,
#            game_state    = None,
#        ),
#        statics_untracked = UntrackedStaticsOffsets(
#            game_speed      = None,
#            visual_rng      = None,
#            character       = None,
#            subshot         = None,
#            difficulty      = None,
#            rank            = None,
#            stage           = None,
#        ),
#        player = PlayerOffsets(
#            player_pointer  = None,
#            zPlayer_pos     = None,
#            zPlayer_hit_rad = None,
#            zPlayer_iframes = None,
#            zPlayer_focused = None,
#        ),
#        bullets = BulletOffsets(
#            bullet_manager_pointer = None,
#            zBulletManager_list    = None,
#            zBullet_iframes        = None,
#            zBullet_pos            = None,
#            zBullet_velocity       = None,
#            zBullet_speed          = None,
#            zBullet_angle          = None,
#            zBullet_hitbox_radius  = None,
#            zBullet_scale          = None,
#            zBullet_type           = None,
#            zBullet_color          = None,
#        ),
#        enemies = EnemyOffsets(
#            enemy_manager_pointer = None,
#            zEnemyManager_list    = None,
#            zEnemy_data           = None,
#            zEnemy_pos            = None,
#            zEnemy_hurtbox        = None,
#            zEnemy_hitbox         = None,
#            zEnemy_rotation       = None,
#            zEnemy_time           = None,
#            zEnemy_score_reward   = None,
#            zEnemy_hp             = None,
#            zEnemy_hp_max         = None,
#            zEnemy_iframes        = None,
#            zEnemy_flags          = None,
#            zEnemy_subboss_id     = None,
#        ),
#        items = ItemOffsets(
#            item_manager_pointer   = None,
#            zItemManager_array     = None,
#            zItemManager_array_len = None,
#            zItem_len              = None,
#            zItem_state            = None,
#            zItem_type             = None,
#            zItem_pos              = None,
#            zItem_vel              = None,
#        ),
#        laser_base = LaserBaseOffsets(
#            laser_manager_pointer   = None,
#            zLaserManager_list      = None,
#            zLaserBaseClass_next    = None,
#            zLaserBaseClass_state   = None,
#            zLaserBaseClass_type    = None,
#            zLaserBaseClass_timer   = None,
#            zLaserBaseClass_offset  = None,
#            zLaserBaseClass_angle   = None,
#            zLaserBaseClass_length  = None,
#            zLaserBaseClass_width   = None,
#            zLaserBaseClass_speed   = None,
#            zLaserBaseClass_id      = None,
#            zLaserBaseClass_iframes = None,
#            zLaserBaseClass_sprite  = None,
#            zLaserBaseClass_color   = None,
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
#        supervisor = SupervisorOffsets(
#            supervisor_addr = None,
#            game_mode       = None,
#            rng_seed        = None,
#        ),
#        associations = Associations(
#            color_coin    = None,
#            color4        = None,
#            color8        = None,
#            color16       = None,
#            sprites       = None,
#            curve_sprites = None,
#            item_types    = None,
#            game_states   = None,
#            game_modes    = None,
#            characters    = None,
#            subshots      = None,
#            difficulties  = None,
#            zEnemyFlags_is_boss    = None,
#            zEnemyFlags_intangible = None,
#            zEnemyFlags_no_hitbox  = None,
#            life_piece_req = None,
#            bomb_piece_req = None,
#        ),
#        game_specific = { }
#    ),