

# Settings Documentation

## Game Interfacing Settings
Settings for the script responsible for interfacing with the game (reading, writing, inputs, screenshots...).

| Name / Type | Description | Default |
|-|-|-|
| **`termination_key`**<br>(string) | If pressed, interrupts any waiting for the next game frame and returns an error (used to terminate sequence extraction early). | `'F6'` |
| **`game`**<br>(string) | Select the game here; can be the full name, acronym, `th##` or just the game number. **Fully supported games**: TD, DDC, LoLK, WBaWC, UM, UDoALG | `'No game selected'` |

## General Extraction Settings
Settings for reading and analyzing game states; used by both single-state and sequence extraction.
Disable extraction of entities not required for your analysis to reduce lag (especially screenshots).

| Name / Type | Description | Default |
|-|-|-|
| **`analyzer`**<br>(string) | Name of an analysis class (e.g. `'AnalysisMostBulletsFrame'`) in `analysis.py`. Sample analyses to get started and plot various entities can be found in `analysis_examples.py`.| `'AnalysisTemplate'` |
| **`requires_bullets`**<br>(bool) | If enabled, extracted states will contain bullet data. | `True` |
| **`requires_enemies`**<br>(bool) | If enabled, extracted states will contain enemy data. | `True` |
| **`requires_items`**<br>(bool) | If enabled, extracted states will contain item data. | `True` |
| **`requires_lasers`**<br>(bool) | If enabled, extracted states will contain laser data. | `True` |
| **`requires_screenshots`**<br>(bool) | If enabled, extracted states will contain screenshots (game window must stay active on the main monitor).| `False` |
| **`requires_side2_pvp`**<br>(bool) | If enabled, extracted states will contain P2 (right side of the screen) data in PvP danmaku games. | `True` |
| **`only_game_world`**<br>(bool) | If enabled, prevents accidentally starting extraction when there is no loaded game world. Also affects sequence extraction, but "not in game world" is one of its termination conditions anyways. | `True` |

## Single-State Extraction Settings
Settings for single-state extraction, in which the current state of the game is extracted and printed.
Analyses can be performed with just this one state (see any plotting example).
Performed if `ingame_duration` is unspecified or less than 2.

| Name / Type | Description | Default |
|-|-|-|
| **`show_untracked`**<br>(bool) | If enabled, prints additional state data (difficulty, character, visual RNG...) deemed not worth tracking for sequence extraction due to either not changing often or being irrelevant. | `False` |
| **`show_enemy_drops`**<br>(bool) | If enabled, a second line listing enemy drops will be added to enemy lines (when applicable). | `False` |
| **`list_print_limit`**<br>(int) | Maximum number of lines in an entity list to be printed before being cut off. | `30` |

## Sequence Extraction Settings 
Settings for sequence extraction, in which the state of the game is repeatedly extracted over a number of in-game frames. Analyzers can track anything they'd like over time and display their results once extraction terminates. By default, extraction will terminate if the game is closed, if the termination key is pressed (see interface settings), or if the game state indicates a non-run scenario (main menu/game over/practice mode end). You can also set custom conditions to terminate extraction based on game state by calling `terminate()` in the `step()` method of a custom analysis.

| Name / Type | Description | Default |
|-|-|-|
| **`ingame_duration`**<br>(string) | Value + Unit (f for frame, s for seconds). Value can be integer number of frames or decimal number of seconds, e.g.: `'200f'`, `'10.5s'`. If it is left unset, malformed or less than two, single-state extraction is performed. Either way, if it's specified as an argument when running `state-reader.py` in the command line, then value set here will be ignored. Can also be set to `inf` or `infinite` to keep sequence extraction going indefinitely until terminated some other way. | `''` |
| **`exact`**<br>(bool) | If enabled, slows the game down to ensure extracted frames are contiguous (see `README.md`). Can also be specified as a command-line argument to `state-reader.py` by typing `exact`. Also called *"exact mode"*. Recommended. | `True` |
| **`auto_focus`**<br>(bool) | If enabled, automatically puts the game in focus when extraction is started. | `True` |
| **`auto_unpause`**<br>(bool) | If enabled, automatically unpauses the game when extraction is started. | `False` |
| **`auto_repause`**<br>(bool) | If enabled, automatically pauses the game when extraction is finished. | `True` |
| **`need_active`**<br>(bool) | If enabled, terminates extraction when the game window goes out of focus. | `False` |
| **`infinite_print_updates`**<br>(bool) | If enabled, per-frame extraction update lines will be printed during infinite extraction. **Note**: When disabled, it may look like the program is unresponsive on the terminal unless you add your own printing in your analyzer's `step` method. | `True` |

## Game-World Plotting Settings (Analysis)
Settings used by sample game world entity plotting analyses.
If you want to make your own, check how these are used.

| Name / Type | Description | Default |
|-|-|-|
| **`plot_scale`**<br>(number) | Adjusts the size of the PyPlot window. `2.0` is already really big, don't toast your PC setting this much higher.| `1.0` |
| **`pyplot_factor`**<br>(number) | Converts sizes in game units to pyplot point/line sizes; seems accurate but may be tweaked. | `0.2` |
| **`bullet_factor`**<br>(number) | Makes bullets bigger than their hitbox radius in bullet scatterplots. | `35` |
| **`enemy_factor`**<br>(number) | Makes enemies bigger than their hitbox radius in enemy scatterplots. | `3` |
| **`plot_laser_circles`**<br>(bool) | If enabled, draws the head of line lasers and the tails of telegraphed lasers in their respective plots. | `True`
| **`plot_enemy_hurtbox`**<br>(bool) | If enabled, draws the outline of enemy hurtboxes on top of their hitbox in enemy scatterplots. | `False`

## ParaKit Script Settings
Settings used by the `parakit.py` main script.

| Name / Type | Description | Default |
|-|-|-|
| **`minimize_version_checker`**<br>(bool) | Reduces the size of the automatic new-version checker's reminders to make it less annoying for users that aren't using Git. | `False` |
