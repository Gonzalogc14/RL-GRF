def calculate_stats(stats, action, last_obs, next_obs):
    ball_position = next_obs.get('ball_position', None)

    if action in [9, 10, 11] and last_obs['ball_owned_team'] == 0:
        stats["total_passes"] += 1
        if next_obs['ball_owned_team'] != 0:
            stats["failed_passes"] += 1

    if action in [12] and last_obs['ball_owned_team'] == 0:
        stats["total_shots"] += 1
        if next_obs['score'][0] > last_obs['score'][0]:
            stats["successful_shots"] += 1

    if last_obs['ball_owned_team'] == 0:
        stats["possession_time"] += 1

    if action in [18]:  
        stats["dribbles"] += 1
        if next_obs['ball_owned_team'] == 0:
            stats["successful_dribbles"] += 1

    if action == 16:  
        stats["tackles"] += 1
    
    if action in [12] and last_obs['ball_owned_team'] == 1:
        stats["opponent_shots"] += 1

