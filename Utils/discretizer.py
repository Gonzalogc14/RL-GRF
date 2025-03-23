import numpy as np

def discretize(value, min_val, max_val, bins):
    return np.digitize(value, np.linspace(min_val, max_val, bins))

def discretize_observation(obs, config):
    ball_x = discretize(obs['ball'][0], -1.2, 1.2, config["ball_bins"][0])
    ball_y = discretize(obs['ball'][1], -1.0, 1.0, config["ball_bins"][1])
    ball_z = discretize(obs['ball'][2], 0.0, 1.0, config["ball_bins"][2])

    left_team = [
        (discretize(p[0], -1.2, 1.2, config["player_bins"][0]),
         discretize(p[1], -1.0, 1.0, config["player_bins"][1]))
        for p in obs['left_team']
    ]

    # Guardar diferencia de goles sin bins
    score_diff = obs['score'][0] - obs['score'][1]
    
    steps_state = discretize(obs['steps_left'], 0, config["max_steps"], config["time_bins"])
    game_mode = obs['game_mode']
    
    # Cambiar posesión: 0 si el equipo izquierdo tiene el balón, 1 si no lo tiene
    possession = 0 if obs['ball_owned_team'] == 0 else 1
    
    left_team_yellow = [1 if card else 0 for card in obs['left_team_yellow_card']]
    
    return tuple(
        [ball_x, ball_y, ball_z] +
        [coord for player in left_team for coord in player] +
        [score_diff, steps_state, game_mode, possession] +
        left_team_yellow
    )

