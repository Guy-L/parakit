

# Settings Documentation

## General Extraction Settings
Settings for reading and analyzing game states; used by both single-state and sequence extraction.
Disable extraction of entities not required for your analysis to reduce lag (especially screenshots).

| Name / Type | Description | Default |
|-|-|-|
| **`analyzer`**<br>(string) | Name of the analysis class to be ran (e.g. `'AnalysisMostBulletsFrame'`) in `analysis.py`. Sample analyses to get started and plot various entities can be found in `analysis_examples.py`.| `'AnalysisTemplate'` |
| **`requires_bullets`**<br>(bool) | If enabled, extracted states will contain bullet data. | `True` |
| **`requires_enemies`**<br>(bool) | If enabled, extracted states will contain enemy data. | `True` |
| **`requires_items`**<br>(bool) | If enabled, extracted states will contain item data. Also applies to TD spirit items and WBaWC animal tokens. | `True` |
| **`requires_lasers`**<br>(bool) | If enabled, extracted states will contain laser data. | `True` |
| **`requires_player_shots`**<br>(bool) | If enabled, extracted states will contain player shot data. | `True` |
| **`requires_screenshots`**<br>(bool) | If enabled, extracted states will contain screenshots (game window must stay active on the main monitor).| `False` |
| **`requires_side2_pvp`**<br>(bool) | If enabled, extracted states will contain P2 (right side of the screen) data in PvP danmaku games. | `True` |
| **`requires_curve_node_vels`**<br>(bool) | If enabled, non-head curvy laser nodes will also have their speed/angle extracted. Velocity is only extracted for the head node (the value is 0 for all others) and by default, the same applies to speed and angle for performance reasons. | `False` |
| **`section_sub_default_to_any`**<br>(bool) | By default, if the first section ECL sub name that can be extracted doesn't meet certain relevance criterias, section_ecl_sub will be blank. If enabled, any sub name can be used as the first. | `False` |
| **`filter_fake_enemies`**<br>(bool) | If enabled, ParaKit will filter from states non-boss enemies which don't have a sprite set (commonly used to help shoot certain patterns). | `True` |
| **`profile_performance`**<br>(bool) | If enabled, ParaKit will display information about how long it took to extract individual sections of each frame. | `False` |

## Game Interfacing Settings
Settings for the script responsible for interfacing with the game (reading, writing, inputs, screenshots...).

| Name / Type | Description | Default |
|-|-|-|
| **`termination_key`**<br>(string) | If pressed, interrupts any waiting for the next game frame and returns an error (used to terminate sequence extraction early). | `'F6'` |
| **`tiebreaker_game`**<br>(string) | Selects which game will be targetted when multiple games are open. Can be the full name, acronym, `th##` or just the game number. **Possible games**: TD, DDC, LoLK, HSiFS, WBaWC, UM, UDoALG | `''` |

## Single-State Extraction Settings
Settings for single-state extraction, in which the current state of the game is extracted and printed.
Analyses can be performed with just this one state (see any plotting example).
Performed if `ingame_duration` is unspecified or less than 2.

| Name / Type | Description | Default |
|-|-|-|
| **`show_enemy_drops`**<br>(bool) | If enabled, the enemy table will list enemy drops as a sub-line for applicable enemies. | `False` |
| **`show_enemy_thresholds`**<br>(bool) | If enabled, the enemy table will list ECL thresholds as a sub-line for bosses. Not displayed for boss-related enemies which use thresholds as the information is usually redundant. | `True` |
| **`show_player_shots`**<br>(bool) | If enabled, the player shot data table will be displayed. | `False` |
| **`list_print_limit`**<br>(int) | Maximum number of lines in an entity list to be printed before being cut off. | `30` |

## Sequence Extraction Settings 
Settings for sequence extraction, in which the state of the game is repeatedly extracted over a number of in-game frames. Analyzers can track anything they'd like over time and display their results once extraction terminates. By default, extraction will terminate if the game is closed, if the termination key is pressed (see interface settings), or if the game state indicates a non-run scenario (main menu/game over/practice mode end). You can also set custom conditions to terminate extraction based on game state by calling `terminate()` in the `step()` method of a custom analysis.

| Name / Type | Description | Default |
|-|-|-|
| **`ingame_duration`**<br>(string) | Value + Unit (f for frame, s for seconds). Value can be integer number of frames or decimal number of seconds, e.g.: `'200f'`, `'10.5s'`. If it is left unset, malformed or less than two, single-state extraction is performed. Either way, if it's specified as an argument when running `state-reader.py` in the command line, then value set here will be ignored. Can also be set to `inf` or `infinite` to keep sequence extraction going indefinitely until terminated some other way. | `''` |
| **`exact`**<br>(bool) | If enabled, slows the game down to ensure extracted frames are contiguous (see `README.md`). Can also be specified as a command-line argument to `state-reader.py` by typing `exact`. Also called *"exact mode"*. Recommended. | `False` |
| **`auto_focus`**<br>(bool) | If enabled, automatically puts the game in focus when extraction is started. | `True` |
| **`auto_unpause`**<br>(bool) | If enabled, automatically unpauses the game when extraction is started. | `False` |
| **`auto_repause`**<br>(bool) | If enabled, automatically pauses the game when extraction is finished. | `True` |
| **`need_active`**<br>(bool) | If enabled, terminates extraction when the game window goes out of focus. | `False` |

## Game-World Plotting Settings (Analysis)
Settings used by sample game world entity plotting analyses.
If you want to make your own, check how these are used.

| Name / Type | Description | Default |
|-|-|-|
| **`plot_scale`**<br>(number) | Adjusts the size of the PyPlot window. `2.0` is already really big, don't toast your PC setting this much higher.| `1.0` |
| **`bullet_factor`**<br>(number) | Makes bullets bigger than their hitbox radius in bullet scatterplots. | `7.0` |
| **`laser_factor`**<br>(number) | Makes lasers smaller than their stored width in laser scatterplots. | `0.2` |
| **`plot_velocity`**<br>(bool) | If enabled, all drawn game entities will show their current velocity as an arrow. | `False`
| **`plot_laser_circles`**<br>(bool) | If enabled, draws the head of line lasers and the tails of telegraphed lasers in their respective plots. | `True`
| **`plot_enemy_hurtbox`**<br>(bool) | If enabled, draws the outline of enemy hurtboxes on top of their hitbox in enemy scatterplots when applicable. | `True`
| **`plot_enemy_move_limits`**<br>(bool) | If enabled, draws the outline of enemy movement limits in enemy scatterplots when applicable. | `False`

## ParaKit Script Settings
Settings used by the `parakit.py` main script.

| Name / Type | Description | Default |
|-|-|-|
| **`minimize_version_checker`**<br>(bool) | Reduces the size of the automatic new-version checker's reminders to make it less annoying for users that aren't using Git. | `False` |
| **`confirm_exit`**<br>(bool) | If enabled, ParaKit will wait until user confirmation to terminate (to prevent the window from disappearing if the script was ran via double-clicking). | `True` |