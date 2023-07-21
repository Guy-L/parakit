from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

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
    time_in_stage: int
    input: int
    rng: int
    game_state: int
    
@dataclass 
class UntrackedStaticsOffsets:
    game_speed: int
    visual_rng: int
    replay_filename: int
    character: int
    subshot: int
    difficulty: int
    rank: int
    stage: int

@dataclass
class PlayerOffsets:
    player_pointer: int
    zPlayer_pos: int
    zPlayer_hurtbox: int
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
    zBullet_ex_delay_timer: Optional[int] #only DDC/ISC/HBM
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
    global_timer: int #frames the ascii manager has been alive: int
    
@dataclass
class SpellCardOffsets:
    spellcard_pointer: int
    zSpellcard_indicator: int #note for zero: I use this var to tell if a spellcard is active in DDC but I'm not sure what is really is. There might be a better indicator.
    zSpellcard_id: int
    zSpellcard_bonus: int
    
@dataclass
class GUIOffsets:
    gui_pointer: int
    zGui_bosstimer_s: int
    zGui_bosstimer_ms: int
    
@dataclass
class SupervisorOffsets:
    supervisor_addr: int
    game_mode: int #to relate to the ggame modes dict in Associations 
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
modern_color_coin = ['Gold', 'Silver', 'Bronze']
modern_color4 = ['Red', 'Blue', 'Green', 'Yellow']     
modern_color8 = ['Black', 'Red', 'Pink', 'Blue', 'Cyan', 'Green', 'Yellow', 'White'] 
modern_color16 = ['Black', 'Dark Red', 'Red', 'Purple', 'Pink', 'Dark Blue', 'Blue', 'Dark Cyan', 'Cyan', 'Dark Green', 'Green', 'Lime', 'Dark Yellow', 'Yellow', 'Orange', 'White'] 

modern_sprites = [('Pellet', 16), ('Pellet', 16), ('Popcorn', 16), ('Small Pellet', 16), ('Ball', 16), ('Ball', 16), ('Outline', 16), ('Outline', 16), ('Rice', 16), ('Kunai', 16), ('Shard', 16), ('Amulet', 16), ('Arrowhead', 16), ('Bullet', 16), ('Laser Head', 16), ('Bacteria', 16), ('Star', 16), ('Coin', 3), ('Mentos', 8), ('Mentos', 8), ('Jellybean', 8), ('Knife', 8), ('Butterfly', 8), ('Big Star', 8), ('Red Fireball', 0), ('Purple Fireball', 0), ('Blue Fireball', 0), ('Yellow Fireball', 0), ('Heart', 8), ('Pulsing Mentos', 8), ('Arrow', 8), ('Bubble', 4), ('Orb', 8), ('Droplet', 16), ('Spinning Rice', 16), ('Spinning Shard', 16), ('Spinning Star', 16), ('Laser', 16), ('Red Note', 0), ('Blue Note', 0), ('Green Note', 0), ('Purple Note', 0), ('Rest', 8)]
modern_curve_sprites = ['Standard', 'Thunder']

modern_item_types = {1: "Power", 2: "Point", 3:"Full Power", 4:"Life Piece", 6:"Bomb Piece", 9:"Green", 10:"Cancel"}
modern_game_states = ["Pause (/Stage Transition/Ending Sequence)", "Not in Run (Main Menu/Game Over/Practice End)", "Actively Playing"]
modern_game_modes = {4: 'Main Menu', 7: 'Game World on Screen', 15: 'Ending Sequence'}

usual_difficulties = ['Easy', 'Normal', 'Hard', 'Lunatic', 'Extra']

## The mother of all dictionaries...

offsets = {
    'th06.exe': None,
    'th07.exe': None,
    'th08.exe': None,
    'th09.exe': None,
    'th095.exe': None,
    'th10.exe': None,
    'th11.exe': None,
    'th12.exe': None,
    'th125.exe': None,
    'th128.exe': None,
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
            time_in_stage = 0xf58b0,
            input         = 0xd6a90,
            rng           = 0xdb510,
            game_state    = 0xf7ac8,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = 0xd8f58,
            visual_rng      = 0xdb508,
            replay_filename = 0xdb560,
            character       = 0xf5828,
            subshot         = 0xf582c,
            difficulty      = 0xf5834,
            rank            = 0xf583c,
            stage           = 0xf58a4,
        ),
        player = PlayerOffsets(
            player_pointer  = 0xdb67C,
            zPlayer_pos     = 0x5e0,
            zPlayer_hurtbox = 0x630,
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
            zBullet_ex_delay_timer = 0x12ec,
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
            gui_pointer       = 0xdb550,
            zGui_bosstimer_s  = 0x19c,
            zGui_bosstimer_ms = 0x1a0,
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
            sprites       = modern_sprites, 
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
        ),
        game_specific = {
            'seija_anm_pointer':  0xd8f60 + 0x1c8,
            'seija_flip_x':       0x60,
            'seija_flip_y':       0x64,
            'zPlayer_scale':      0x18308,
            'bonus_count':        0xf5894,
        }
    ),
    
    'th143.exe': None,
    'th15.exe': None,
    'th16.exe': None,
    'th165.exe': None,
    'th17.exe': None,
       
    # TOUHOU 18 -- Unconnected Marketeers ========================
    #=============================================================
    'th18.exe': Offset( 
        statics = StaticsOffsets(
            score         = None,
            graze         = None,
            piv           = None,
            power         = None,
            lives         = None,
            life_pieces   = None,
            bombs         = None,
            bomb_pieces   = None,
            time_in_stage = None,
            input         = None,
            rng           = None,
            game_state    = None,
        ),
        statics_untracked = UntrackedStaticsOffsets(
            game_speed      = None,
            visual_rng      = None,
            replay_filename = None,
            character       = None,
            subshot         = None,
            difficulty      = None,
            rank            = None,
            stage           = None,
        ),
        player = PlayerOffsets(
            player_pointer  = None,
            zPlayer_pos     = None,
            zPlayer_hurtbox = None,
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
            zBullet_ex_delay_timer = None,
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
            gui_pointer       = None,
            zGui_bosstimer_s  = None,
            zGui_bosstimer_ms = None,
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
            difficulties  = usual_difficulties,
            zEnemyFlags_is_boss    = None,
            zEnemyFlags_intangible = None,
            zEnemyFlags_no_hitbox  = None,
        ),
        game_specific = {

        }
    )
}