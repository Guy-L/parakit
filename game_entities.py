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
    bullet_type: int
    color: int
    
@dataclass
class Enemy:
    position: Tuple[float, float]
    hurtbox: Tuple[float, float]
    hp: int
    hp_max: int

@dataclass
class Item:
    item_type: str
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    
@dataclass
class CurveNode:
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    angle: float
    speed: float

@dataclass
class LaserInner:
    pass
    
@dataclass
class LaserInnerLine(LaserInner):
    start_pos: Tuple[float, float]
    angle: float
    max_length: float
    width: float
    speed: float
    sprite: int
    color: int 
    distance: float
    
@dataclass
class LaserInnerCurve(LaserInner):
    start_pos: Tuple[float, float]
    angle: float
    width: float
    speed: float
    sprite: int
    color: int
    max_length: int 
    distance: float
    nodes: List[CurveNode] 

@dataclass 
class Laser:
    state: int
    laser_type: int
    position: Tuple[float, float]
    angle: float
    length: float
    width: float
    speed: float
    id: int
    sprite: int
    color: int
    inner: LaserInner
    
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
    bullets: Optional[List[Bullet]]
    enemies: Optional[List[Enemy]]
    items: Optional[List[Item]]
    lasers: Optional[List[Laser]]
    screen: Optional[np.ndarray]