def calculate_rewards(state, action, previous_state):
    """
    Calculates rewards and penalties for the left team based on the current and previous state.
    """
    reward = 0
    score, prev_score = state[-4], previous_state[-4]  # Usa índice negativo para score_state
    ball_x = state[0]  
    ball_owned_team, prev_ball_owned_team = state[-2], previous_state[-2]  # Usa el penúltimo valor  
    left_team_yellow_cards, prev_left_team_yellow_cards = state[-11:], previous_state[-11:]  # Últimos 11 valores  
    
    PASS_ACTIONS = [9, 10, 11]
    SHOOT_ACTION = 12
    DRIBBLE_ACTION = 18
    TACKLE_ACTION = 16
    
    # POSITIVE REWARDS
    
    ## Rewards for possession gain
    if prev_ball_owned_team == 1 and ball_owned_team == 0:
        reward += 8  # General possession recovery reward
        if ball_x < 5:
            reward += 10  # Extra for recovering in the defensive zone
        elif 5 <= ball_x <= 10:
            reward += 6  # Extra for midfield recovery
        if action == TACKLE_ACTION:
            reward += 10  # Extra for successful tackle recovery
    
    ## Rewards for offensive plays
    if score > prev_score:
        reward += 200  # Scoring a goal
    
    if action in PASS_ACTIONS and prev_ball_owned_team == 0 and ball_owned_team == 0:
        reward += 5 if action == 9 else 3  # Long pass (5) vs short pass (3)
    
    if state[35] == 4 and ball_owned_team == 0:
        reward += 4  # Winning a corner

    
    ## Defensive positioning reward
    if ball_owned_team == 1:
        left_team_positions = state[3:25]  # Extract left team positions (11 players * 2 coordinates)
        for i in range(0, 22, 2):  # Iterate over x-coordinates of the 11 players
            if left_team_positions[i] < -0.5:
               reward += 0.1  # Defensive positioning bonus
    
    ## Rewards for dribbling success
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team == 0:
        reward += 6  # Successful dribble

        ## Reward for committing fouls without a yellow card
    if state[35] == 3 and prev_ball_owned_team != 0 and not any(left_team_yellow_cards):
        reward += 3
    
    # NEGATIVE PENALTIES
    
    ## Severe penalty for conceding a goal
    if score < prev_score:
        reward -= 200  
    
    ## Possession loss penalties
    if prev_ball_owned_team == 0 and ball_owned_team != 0:
        if ball_x < 5:
            reward -= 6  # Losing possession in the defensive zone
        if action in PASS_ACTIONS and ball_x < 5:
            reward -= 5  # Risky pass interception in the defensive zone
    
    ## Defensive errors
    if action == TACKLE_ACTION and ball_x < 5 and ball_owned_team != 0:
        reward -= 4  # Foul near the goal
    
    if action == SHOOT_ACTION and prev_ball_owned_team == 1:
        reward -= 6  # Allowing too many opponent shots
    
    if prev_ball_owned_team == 1 and ball_owned_team == -1 and action == SHOOT_ACTION and ball_x < -0.5:
        reward -= 7  # Allowing opponent shots from defensive zone
    
    ## Card penalties
    for i in range(len(left_team_yellow_cards)):
        if left_team_yellow_cards[i] > prev_left_team_yellow_cards[i]:
            reward -= 2  # Receiving a yellow card
    
    ## Penalty for failing a dribble
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team != 0:
        reward -= 4  # Failed dribble
    
    return reward

