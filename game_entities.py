from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
import numpy as np

@dataclass
class Bullet:
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    is_active: bool
    speed: float
    angle: float
    scale: float
    hitbox_radius: float
    iframes: int
    bullet_type: int
    color: int

@dataclass
class Enemy:
    position: Tuple[float, float]
    hurtbox: Tuple[float, float]
    hitbox: Tuple[float, float]
    no_hurtbox: bool
    no_hitbox: bool
    invincible: bool
    is_rectangle: bool
    is_boss: bool
    subboss_id: int
    rotation: float
    anm_page: int
    anm_id: int
    score_reward: int
    hp: int
    hp_max: int
    iframes: int

@dataclass
class Item:
    item_type: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    
@dataclass 
class Laser:
    state: int
    laser_type: int
    timer: int
    position: Tuple[float, float]
    angle: float
    length: float
    width: float
    speed: float
    id: int
    iframes: int
    sprite: int
    color: int
    
@dataclass
class LineLaser(Laser):
    start_pos: Tuple[float, float]
    init_angle: float
    max_length: float
    init_speed: float
    distance: float

@dataclass
class InfiniteLaser(Laser):
    start_pos: Tuple[float, float]
    origin_vel: Tuple[float, float]
    default_angle: float
    angular_vel: float
    init_length: float
    max_length: float
    max_width: float
    default_speed: float
    start_time: int
    expand_time: int
    active_time: int
    shrink_time: int
    distance: float

@dataclass
class CurveNode:
    position: Tuple[float, float]
    velocity: Optional[Tuple[float, float]]
    angle: Optional[float]
    speed: Optional[float]
    
@dataclass
class CurveLaser(Laser):
    #start_pos: stored as laser pos
    max_length: int 
    distance: float
    nodes: List[CurveNode]   

@dataclass
class Spellcard:
    spell_id: int
    capture_bonus: int
    
@dataclass
class GameState:
    frame_stage: int
    frame_global: int
    stage_chapter: int
    seq_frame_id: Optional[int]   
    seq_real_time: Optional[float]
    state: int
    mode: int
    score: int
    lives: int
    life_pieces: Optional[int] #game-specific: absent in pre-SA & UDoALG
    bombs: int
    bomb_pieces: int
    power: int
    piv: int
    graze: int
    boss_timer: float
    spellcard: Optional[Spellcard]
    rank: int
    input: int
    rng: int
    player_position: Tuple[float, float]
    player_hitbox_rad: float
    player_iframes: int
    player_focused: bool
    bomb_state: int
    bullets: Optional[List[Bullet]]
    enemies: Optional[List[Enemy]]
    items: Optional[List[Item]]
    lasers: Optional[List[Laser]]
    screen: Optional[np.ndarray]
    game_specific: Optional[Dict[str, Any]]

# ======================
# Game specific entities

# DDC / ISC / HBM
@dataclass
class ShowDelayBullet(Bullet):
    show_delay: int

# Legacy of Lunatic Kingdom
@dataclass
class GrazeTimerBullet(Bullet):
    graze_timer: int

@dataclass
class WeightedEnemy(Enemy):
    shootdown_weight: int

# Unconnected Marketeers
@dataclass
class ActiveCard:
    id: int
    charge: int
    charge_max: int
    internal_name: str
    selected: bool

# Unfinished Dream of All Living Ghost
@dataclass
class P2Side:
    lives: int
    lives_max: int
    bombs: int
    bomb_pieces: int
    power: int
    graze: int
    boss_timer: float
    spellcard: Optional[Spellcard]
    input: int
    player_position: Tuple[float, float]
    player_hitbox_rad: float
    player_iframes: int
    player_focused: bool
    bomb_state: int
    bullets: Optional[List[Bullet]]
    enemies: Optional[List[Enemy]]
    items: Optional[List[Item]]
    lasers: Optional[List[Laser]]
    hitstun_status: int
    shield_status: int
    last_combo_hits: int
    current_combo_hits: int
    current_combo_chain: int
    enemy_pattern_count: int
    item_spawn_total: int
    gauge_charging: bool
    gauge_charge: int
    gauge_fill: int
    ex_attack_level: int
    boss_attack_level: int
    pvp_wins: int