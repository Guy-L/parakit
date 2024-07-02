# General Extraction Settings
extraction_settings = {

    # Name of an analysis class (e.g. 'AnalysisMostBulletsFrame') in analysis.py.
    # Sample analyses to get started and plot various entities can be found in analysis_examples.py.
    'analyzer': 'AnalysisTemplate',

    # Disable extraction of entities not required for your analysis to reduce lag
    'requires_bullets': True,
    'requires_enemies': True,
    'requires_items':   True,
    'requires_lasers':  True,
    'requires_player_shots': True,
    'requires_screenshots': False,
    'requires_side2_pvp': True,

    # See settings.md for more info.
    'requires_curve_node_vels': False,
    'section_sub_default_to_any': False,
    'filter_fake_enemies': True,
    'profile_performance': False,
}

# Game Interfacing Settings
# See settings.md for more info.
interface_settings = {
    'termination_key': 'F6',
    'tiebreaker_game': '',
}

# Single-State Extraction Settings
singlext_settings = {
    'show_enemy_drops': False,
    'show_boss_thresholds': True,
    'show_player_shots': False,
    'list_print_limit': 30,
}

# Sequence Extraction Settings 
# See settings.md for more info.
seqext_settings = {
    'ingame_duration': '', #e.g. '520f', '12.4s', etc. or 'infinite', 'inf'
    'exact':        False,
    'auto_focus':   True,
    'auto_unpause': False,
    'auto_repause': True,
    'need_active':  False,
}

# Game-World Plotting Settings (Analysis)
# See settings.md for more info.
pyplot_settings = {
    'plot_scale':    1.0,
    'bullet_factor': 7.0,
    'laser_factor':  0.2,
    'plot_velocity': False,
    'plot_laser_circles': True,
    'plot_enemy_hurtbox': True,
    'plot_enemy_move_limits': False,
}

# ParaKit Script Settings
# See settings.md for more info.
parakit_settings = {
    'minimize_version_checker': False,
    'confirm_exit': True,
}
