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
    screen: Optional[np.ndarray]