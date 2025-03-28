def calculate_rewards(state, action, previous_state):
    """
    Calculates rewards and penalties for the left team based on the current and previous state.
    """
    reward = 0
    score, prev_score = state[25], previous_state[25]  
    ball_x = state[0]  
    ball_owned_team, prev_ball_owned_team = state[28], previous_state[28]  
    left_team_yellow_cards, prev_left_team_yellow_cards = state[29:], previous_state[29:] 

    PASS_ACTIONS = [9, 10, 11]
    SHOOT_ACTION = 12
    DRIBBLE_ACTION = 18
    TACKLE_ACTION = 16
    
    """
    POSITIVE REWARDS
    """
    
    ## Rewards for possession gain
    #
    if prev_ball_owned_team == 1 and ball_owned_team == 0:
        reward += 4  
        if ball_x < 5:
           reward += 4  
        elif 5 <= ball_x <= 10:
           reward += 4 
        if action == TACKLE_ACTION:
           reward += 7 
    
    if score > prev_score:
       reward += 500  # Scoring a goal
    
    if action in PASS_ACTIONS and prev_ball_owned_team == 0 and ball_owned_team == 0:
        reward += 6 if action == 9 else 3  # Long pass (5) vs short pass (3)
    
    if state[35] == 4 and ball_owned_team == 0:
       reward += 5  # Winning a corner

    
    ## Defensive positioning reward
    if ball_owned_team == 1:
        left_team_positions = state[3:25]  
        for i in range(0, 22, 2):  
            if left_team_positions[i] < -0.5:
               reward += 1  
    
    ## Rewards for dribbling success
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team == 0:
       reward += 6  

    ## Reward for committing fouls without a yellow card
    if state[35] == 3 and prev_ball_owned_team != 0 and not any(left_team_yellow_cards):
        reward += 4

    """
    NEGATIVE PENALTIES
    """

    ## Severe penalty for conceding a goal
    if score < prev_score:
        reward -= 400  
    
    ## Possession loss penalties
    if prev_ball_owned_team == 0 and ball_owned_team != 0:
        if ball_x < 5:
            reward -= 6 
        if action in PASS_ACTIONS and ball_x < 5:
            reward -= 5  
    
    ## Defensive errors
    if action == TACKLE_ACTION and ball_x < 5 and ball_owned_team != 0:
        reward -= 6 
    
    if action == SHOOT_ACTION and prev_ball_owned_team == 1:
        reward -= 6  
    
    if prev_ball_owned_team == 1 and ball_owned_team == -1 and action == SHOOT_ACTION and ball_x < -0.5:
        reward -= 5  
    
    ## Card penalties
    for i in range(len(left_team_yellow_cards)):
        if left_team_yellow_cards[i] > prev_left_team_yellow_cards[i]:
            reward -= 5  
    
    ## Penalty for failing a dribble
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team != 0:
        reward -= 6 
    
    return reward

