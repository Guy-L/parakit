from dataclasses import dataclass
from abc import ABC
from typing import List, Tuple, Optional, Dict, Any, Union
from numpy import ndarray
from time import struct_time

# ================================================
# All-game entities ==============================
# ================================================
# Note: IDs are unique numbers you can use to track
#  an entity during its lifetime.

@dataclass
class Bullet:
    id: int
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    speed: float
    angle: float
    scale: float #set to 1 in pre-DDC for convenience
    hitbox_radius: float
    iframes: int
    is_active: bool #true if not in spawn/despawn anim
    is_grazeable: bool
    alive_timer: int
    type: int #meaning: bullet_types[type][0]
    color: int #meaning: get_color(type, color)[0]

@dataclass #a rectangle, used by bosses
class EnemyMovementLimit:
    center: Tuple[float, float]
    width: float
    height: float

@dataclass
class Enemy:
    id: int
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    hurtbox: Tuple[float, float]
    hitbox: Tuple[float, float]
    move_limit: Optional[EnemyMovementLimit]
    no_hurtbox: bool
    no_hitbox: bool
    invincible: bool
    intangible: bool
    is_grazeable: bool
    is_rectangle: bool
    is_boss: bool
    is_fake: bool #always False if filter_fake_enemies is True
    subboss_id: int
    health_threshold: Tuple[int, str] #if health <= int, run ECL sub str, only used by bosses
    time_threshold: Tuple[int, str] #if ecl timer > int, run ECL sub str, only used by bosses
    rotation: float
    pivot_angle: float #used to rotate rectangle enemies in DDC-UM in janky way (see AnalysisPlotEnemies); 0 in other games
    anm_page: int #usually: 0 for bosses sprites, 1 for stage enemy sprites, 2 for custom enemy sprites
    anm_id: int #id of the sprite within the page
    ecl_sub_name: str #name of the ecl subroutine ran by the enemy. useful to tell apart stage enemies
    ecl_sub_timer: int
    alive_timer: int
    health: int
    health_max: int
    revenge_ecl_sub: str #name of the ecl subroutine ran when the enemy dies (revenge bullets)
    drops: Dict[int, int] #key: item type, value: count
    iframes: int

@dataclass
class Item:
    id: int
    state: int #compare again zItemState_autocollect & zItemState_attracted
    item_type: int #meaning: item_types[item_type]
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    alive_timer: int

@dataclass 
class Laser:
    id: int
    state: int #if telegraph: telegraph=3, expand=4, active=2, shrink=5
    laser_type: int #line=0, telegraph=1, curve=2, beam=3
    alive_timer: int
    position: Tuple[float, float]
    angle: float
    length: float
    width: float
    speed: float
    iframes: int
    sprite: int #meaning: bullet_types[sprite][0] for line/infinite, curve_sprites[sprite] for curve
    color: int #meaning: get_color(sprite, color)[0]

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
    id: int
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
class Bomb:
    state: int #active if non-zero (usually 1)

@dataclass
class PlayerShot:
    id: int
    array_id: int #[0, player_shot_array_len - 1]; functionally the same as id
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    hitbox: Tuple[float, float]
    speed: float
    angle: float
    damage: int
    alive_timer: int

@dataclass
class Player:
    position: Tuple[float, float]
    hitbox_rad: float
    iframes: int
    focused: bool
    options_pos: List[Tuple[float, float]]
    shots: List[PlayerShot]
    deathbomb_f: int #starts at deathbomb_window_frames (usually 8) on hit and goes down to 0, can db if non-0
    can_shoot: bool

@dataclass
class SpellCard:
    spell_id: int
    capture_bonus: int

# ================================================
# Environment data ===============================
# ================================================
@dataclass
class ExtractionStatus:
    frame_counter: int #frames extracted so far
    sequence_counter: int #increases each time the game world is loaded (resets/stage transition/loads from menu)
    work_time: float #excludes time in menus
    total_time: float #includes time in menus
    system_time: struct_time #converted to local time
    system_input: List[int] #pressed keyboard scancodes

# Note: RunEnvironment variables are only extracted
# once per game world load in sequence extraction.
@dataclass
class RunEnvironment:
    difficulty: int #meaning: difficulties[difficulty]
    character: int #meaning: characters[character]
    subshot: int #meaning: subshots[subshot]
    stage: int

@dataclass
class GameConstants:
    deathbomb_window_frames: int #can change in UM
    poc_line_height: int #can change in UM
    life_piece_req: int #can change in TD
    bomb_piece_req: int
    world_width: int
    world_height: int
    game_id: int

# ================================================
# Game specific environment data =================
# ================================================
@dataclass
class RunEnvironmentUDoALG(RunEnvironment):
    card_count: int
    charge_attack_threshold: int #to compare against gauge_charge; c1
    charge_skill_threshold: int #to compare against gauge_charge; c2
    ex_attack_threshold: int #to compare against gauge_charge; c3
    boss_attack_threshold: int #to compare against gauge_charge; c4

# ================================================
# Game specific game entities ====================
# ================================================

# EoSD / PCB / IN / PoFV / MoF / SA
@dataclass
class ScoreRewardEnemy(Enemy):
    score_reward: int

# Ten Desires
@dataclass
class RectangleEcho:
    left_x: float
    right_x: float
    top_y: float
    bottom_y: float

@dataclass
class CircleEcho:
    position: Tuple[float, float]
    radius: float

@dataclass
class SpiritDroppingEnemy(Enemy):
    speedkill_cur_drop_amt: int
    speedkill_time_left_for_amt: int

# Double Dealing Character
@dataclass
class ScalablePlayer(Player):
    scale: float #[1, 3]

# DDC / ISC / HBM
@dataclass
class ShowDelayBullet(Bullet):
    show_delay: int

# Legacy of Lunatic Kingdom
@dataclass
class GrazeTimerBullet(Bullet):
    graze_timer: int

# HSiFS / VD
@dataclass
class CanIntangibleBullet(Bullet):
    is_intangible: bool

@dataclass
class WeightedEnemy(Enemy):
    shootdown_weight: int

# Hidden Star in Four Seasons
@dataclass
class SeasonDroppingEnemy(Enemy):
    speedkill_cur_drop_amt: int
    speedkill_time_left_for_amt: int
    season_drop_timer: int
    season_drop_max_time: int
    season_drop_min_count: int
    damage_per_season_drop: int
    damage_taken_for_season_drops: int

# Unconnected Marketeers & (TODO) UDoALG
@dataclass
class SpeedkillDropEnemy(Enemy):
    speedkill_cur_drop_amt: int #gold only, to make it work with AnalysisPlotEnemiesSpeedkillDrops (this sucks)
    speedkill_time_left_for_amt: int #gold only, to make it work with AnalysisPlotEnemiesSpeedkillDrops (this sucks)
    speedkill_drops_max_cnt: Dict[int, int] #key: item type, value: count
    speedkill_drops_max_time: int
    speedkill_drops_timer: int

# Unfinished Dream of All Living Ghost
@dataclass
class CanGenItemsTimerBullet(Bullet):
    can_gen_items_timer: int #set to 0 when grazed/scoped, ticks up otherwise
    #bullet can be grazed/scoped for items again at 60f (stored in bullet.is_grazeable)

@dataclass
class StunnableShieldPlayer(Player):
    hitstunned: bool
    shield_up: bool

# ================================================
# Game specific objects ==========================
# ================================================

# Ten Desires
@dataclass
class SpiritItem:
    id: int
    state: int #1 = idle, 2 = attracted, 4 = reimu trance PoC
    spirit_type: int #meaning: spirit_types[spirit_type]
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    alive_timer: int #[1, 522] frames alive

# Wily Beast & Weakest Creature
@dataclass
class AnimalToken:
    id: int
    type: int #meaning: token_types[type]
    position: Tuple[float, float]
    base_velocity: Tuple[float, float] #wont reflect slowdown by player proximity
    being_grabbed: bool
    can_switch: bool
    slowed_by_player: bool
    switch_timer: int #ticks down from 180f, token starts blinking at 60f; when it hits 0, resets to 180f and type = type++ % 3
    alive_timer: int #ticks up; token becomes transparent after 7800f, can leave field after 8400f

@dataclass
class RoaringHyper:
    type: int #meaning: hyper_types[type]
    duration: int
    time_remaining: int #extra beasts appear 120f (2s) after timer expires
    reward_mode: int #0 = regular, 2 = cow, 3 = chick, 1 and >5 = jelly & others
    token_grab_time_bonus: int #first grab adds 180f, then 120f, 80f, 53f then always 23f
    otter_shield_angles: List[float] #length 3 for otter hyper, 0 otherwise
    currently_breaking: bool #used for ST6 secret token

# Unconnected Marketeers
@dataclass
class ActiveCard:
    type: int #meaning: card_nicknames[type]
    charge: int #[0, charge_max], set to 0 upon use (or 20% of max if Scroll equipped), ticks up every frame once no longer in use
    charge_max: int #depends purely on the type of card
    internal_name: str
    selected: bool
    in_use: bool

# Unfinished Dream of All Living Ghost
@dataclass
class P2Side:
    lives: int
    lives_max: int
    bombs: int
    bomb_pieces: int
    power: int
    graze: int
    boss_timer_shown: float
    boss_timer_real: float
    section_ecl_sub: str
    spell_card: Optional[SpellCard]
    input: int
    player: Player
    bomb: Bomb
    bullets: List[Bullet]
    enemies: List[Enemy]
    items: List[Item]
    lasers: List[Laser]
    last_combo_hits: int
    current_combo_hits: int
    current_combo_chain: int
    enemy_pattern_count: int
    gauge_charging: bool
    gauge_charge: int
    gauge_fill: int
    ex_attack_level: int
    boss_attack_level: int
    pvp_wins: int
    env: RunEnvironmentUDoALG


# ================================================
# General `state` schema =========================
# ================================================

@dataclass
class GameState:
    stage_frame: int
    global_frame: int
    score: int
    lives: int
    life_pieces: int #set to 0 in pre-SA + UDoALG for convenience
    bombs: int
    bomb_pieces: int
    power: int
    piv: int
    graze: int
    spell_card: Optional[SpellCard]
    rank: int
    input: int
    rng: int
    continues: int
    stage_chapter: int
    boss_timer_shown: float #capped at 99.99, truncated to 2 decimals
    boss_timer_real: float #not capped, not truncated
    section_ecl_sub: str #use this to tell apart stage/boss sections
    game_speed: float #usually 1 (always 1 in pause menu)
    fps: float
    player: Player
    bomb: Bomb
    bullets: List[Bullet]
    enemies: List[Enemy]
    items: List[Item]
    lasers: List[Laser]
    screen: Optional[ndarray]
    constants: GameConstants
    env: RunEnvironment
    pk: ExtractionStatus


# ================================================
# Game specific state extensions =================
# ================================================

# Ten Desires
@dataclass
class GameStateTD(GameState):
    trance_active: bool
    trance_meter: int #[0, 600], doubles as remaining frame counter for trances (600 frames = 10s)
    chain_timer: int #[0, 60] frames
    chain_counter: int #>9 greys spawn
    spirit_items: List[SpiritItem]
    spawned_spirit_count: int #next spirit spawns to the left if odd, to the right otherwise; applies to all spirits
    kyouko_echo: Union[RectangleEcho, CircleEcho]
    youmu_charge_timer: int #focus shot on release if >60f, negative for 40f cooldown
    miko_final_logic_active: bool

# Double Dealing Character
@dataclass
class GameStateDDC(GameState):
    bonus_count: int #increases with non-2.0 bonuses, life piece at every multiple of 5
    seija_flip: Tuple[float, float] #[0, 1] for x and y (0 = normal, 1 = fully flipped)
    sukuna_penult_logic_active: bool

# Legacy of Lunatic Kingdom
@dataclass
class GameStateLoLK(GameState):
    item_graze_slowdown_factor: float
    reisen_bomb_shields: int
    time_in_chapter: int
    chapter_graze: int
    chapter_enemy_weight_spawned: int
    chapter_enemy_weight_destroyed: int
    in_pointdevice: bool
    pointdevice_resets_total: int
    pointdevice_resets_chapter: int
    graze_inferno_logic_active: bool

# Hidden Star in Four Seasons
@dataclass
class GameStateHSiFS(GameState):
    next_extend_score: int
    season_level: int
    season_power: int #increments with each season item grabbed
    next_level_season_power: int #season power required for next level
    season_delay_post_use: int #[0, 45], ticks down from 45 after release deactivates
    release_active: bool
    season_disabled: bool
    snowman_logic_active: bool

# Wily Beast & Weakest Creature
@dataclass
class GameStateWBaWC(GameState):
    held_tokens: List[int] #length [0, 5], meaning: token_types[token]
    field_tokens: List[AnimalToken]
    roaring_hyper: Optional[RoaringHyper]
    extra_token_spawn_delay_timer: int #[0, 120], ticks up, only resets when Extra Beasts Appear! delay starts
    youmu_charge_timer: int #focus shot on release if >60f, negative for 40f cooldown
    yacchie_recent_graze: int #sum of graze gains over last 20 frames

# Unconnected Marketeers
@dataclass
class GameStateUM(GameState):
    funds: int
    total_cards: int
    total_actives: int
    total_equipmt: int
    total_passive: int
    cancel_counter: int #increments with bullet cancels that spawn items, used by Mallet for item conversion
    lily_counter: Optional[int] #increments with uses of the Lily card, determines difficulty
    centipede_multiplier: Optional[float] #[1.0, 1.8]
    active_cards: List[ActiveCard]
    asylum_logic_active: bool
    sakuya_knives_angle: float #[~0.79, ~2.34] (higher = farther left, lower = farther right, 1.57 = middle)
    sakuya_knives_spread: float #[~-0.3, ~1.03] (lower = more concentrated, higher = more spread)

# Unfinished Dream of All Living Ghost
@dataclass
class GameStateUDoALG(GameState):
    lives_max: int
    last_combo_hits: int
    current_combo_hits: int
    current_combo_chain: int
    enemy_pattern_count: int
    gauge_charging: bool
    gauge_charge: int
    gauge_fill: int
    ex_attack_level: int
    boss_attack_level: int
    side2: Optional[P2Side]
    story_boss_difficulty: int
    story_fight_phase: Optional[int]     #important for story mode AI fight progress, both are None if not in story mode
    story_progress_meter: Optional[int]  #more info: https://docs.google.com/document/d/1HCCxLkN9KAW4tOu1196CA40S2tugd3DCPUh-pT4Nr8c
    pvp_timer_start: int
    pvp_timer: int
    pvp_wins: int
    rank_max: int