def calculate_stats(stats, action, last_obs, next_obs):
    if action in [9, 10, 11] and last_obs['ball_owned_team'] == 0:
        stats["total_passes"] += 1
        if next_obs['ball_owned_team'] != 0:
            stats["failed_passes"] += 1

    if action in [12, 13] and last_obs['ball_owned_team'] == 0:
        stats["total_shots"] += 1
        if next_obs['score'][0] > last_obs['score'][0]:
            stats["successful_shots"] += 1

    if last_obs['ball_owned_team'] == 0:
        stats["possession_time"] += 1

    if last_obs['ball_owned_team'] in [1, 2] and next_obs['ball_owned_team'] == 0:
        stats["interceptions"] += 1

    if last_obs['ball_owned_team'] in [1, 2] and next_obs['ball_owned_team'] == 0 and next_obs['ball_position'][0] > 0:
        stats["ball_recoveries"] += 1

    if action in [18, 19]:
        stats["dribbles"] += 1
        if next_obs['ball_owned_team'] == 0:
            stats["successful_dribbles"] += 1

    if action in [20, 21]:
        stats["tackles"] += 1
