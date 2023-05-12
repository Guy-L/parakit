from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np

@dataclass
class Bullet:
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    speed: float
    angle: float
    scale: float
    hitbox_radius: float
    show_delay: int
    iframes: int
    bullet_type: int
    color: int
    
@dataclass
class Enemy:
    position: Tuple[float, float]
    hurtbox: Tuple[float, float]
    hitbox: Tuple[float, float]
    rotation: float
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
class GameState:
    frame_id: int
    state: int
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
    bullets: Optional[List[Bullet]]
    enemies: Optional[List[Enemy]]
    items: Optional[List[Item]]
    lasers: Optional[List[Laser]]
    screen: Optional[np.ndarray]