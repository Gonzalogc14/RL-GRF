import numpy as np

def discretize(value, min_val, max_val, bins):
    return np.digitize(value, np.linspace(min_val, max_val, bins))

def discretize_observation(obs, config):
    ball_x = discretize(obs['ball'][0], -1.2, 1.2, config["ball_bins"][0])
    ball_y = discretize(obs['ball'][1], -1.0, 1.0, config["ball_bins"][1])
    ball_z = discretize(obs['ball'][2], 0.0, 1.0, config["ball_bins"][2])

    ball_dir_x = discretize(obs['ball_direction'][0], -1.5, 1.5, config["ball_dir_bins"][0])
    ball_dir_y = discretize(obs['ball_direction'][1], -1.5, 1.5, config["ball_dir_bins"][1])
    ball_dir_z = discretize(obs['ball_direction'][2], -1.5, 1.5, config["ball_dir_bins"][2])

    left_team = [
        (discretize(p[0], -1.2, 1.2, config["player_bins"][0]),
         discretize(p[1], -1.0, 1.0, config["player_bins"][1]))
        for p in obs['left_team']
    ]

    left_team_dir = [
        (discretize(v[0], -1.0, 1.0, config["player_dir_bins"][0]),
         discretize(v[1], -1.0, 1.0, config["player_dir_bins"][1]))
        for v in obs['left_team_direction']
    ]

    right_team = [
        (discretize(p[0], -1.2, 1.2, config["player_bins"][0]),
         discretize(p[1], -1.0, 1.0, config["player_bins"][1]))
        for p in obs['right_team']
    ]

    right_team_dir = [
        (discretize(v[0], -1.0, 1.0, config["player_dir_bins"][0]),
         discretize(v[1], -1.0, 1.0, config["player_dir_bins"][1]))
        for v in obs['right_team_direction']
    ]

    ball_owned_player = obs['ball_owned_player'] if obs['ball_owned_player'] != -1 else 11

    score_diff = obs['score'][0] - obs['score'][1]
    steps_state = discretize(obs['steps_left'], 0, config["max_steps"], config["time_bins"])
    game_mode = obs['game_mode']
    possession = 0 if obs['ball_owned_team'] == 0 else 1

    left_team_yellow = [1 if card else 0 for card in obs['left_team_yellow_card']]

    return tuple(
        [ball_x, ball_y, ball_z, ball_dir_x, ball_dir_y, ball_dir_z] +
        [coord for player in left_team for coord in player] +
        [coord for player in left_team_dir for coord in player] +
        [coord for player in right_team for coord in player] +
        [coord for player in right_team_dir for coord in player] +
        [ball_owned_player, score_diff, steps_state, game_mode, possession] +
        left_team_yellow
    )
