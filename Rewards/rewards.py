def calculate_rewards(state, action, previous_state):
    """
    Calculates rewards and penalties for the left team based on the current and previous state.
    """
    reward = 0
    score, prev_score = state['score'], previous_state['score']
    ball_x, ball_owned_team = state['ball'][0], state['ball_owned_team']
    prev_ball_owned_team = previous_state['ball_owned_team']

    PASS_ACTIONS = [9, 10, 11]
    SHOOT_ACTION = 12
    DRIBBLE_ACTION = 18
    TACKLE_ACTION = 16

    """
    POSITIVE REWARDS
    """

    """
    Reward for scoring a goal.
    - Points are awarded based on the previous score.
    - If already winning, the reward is lower.
    - If the match was tied or losing, the reward is higher.
    """
   
    if (score[0] - prev_score[0]) == 1:
        if prev_score[0] > prev_score[1]:  
            reward += 8  
        elif prev_score[0] < prev_score[1]:  
            reward += 10  
        else:  
            reward += 9  
 

    """
    Reward for a successful pass.
    - Given if the left team maintains possession after a pass.
    - No reward if the pass results in offside.
    """
    if action in PASS_ACTIONS and prev_ball_owned_team == 0 and ball_owned_team == 0 and not state.get('offside', False):
        reward += 2  

    """
    Reward for an assist.
    - Given if a pass directly leads to a goal.
    """
    if action in PASS_ACTIONS and score[0] > prev_score[0]:  
        reward += 5  

    """
    Reward for an interception.
    - Given if the left team steals the ball from the opposing team.
    """
    if prev_ball_owned_team == 1 and ball_owned_team == 0:
        reward += 3  

    """
    Reward for a blocked shot.
    - Given if the left team shoots, and the goalkeeper or defense gains possession.
    """
    if action == SHOOT_ACTION and prev_ball_owned_team == 0 and ball_owned_team == 1:
        reward += 3  

    """
    Reward for a successful dribble.
    - Given if the player maintains possession after attempting to dribble.
    """
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team == 0:
        reward += 3  

    """
    Reward for recovering the ball with a sliding tackle.
    - Given if the left team regains possession after a tackle.
    """
    if action == TACKLE_ACTION and prev_ball_owned_team == 1 and ball_owned_team == 0:
        reward += 3  

    """
    Reward for recovering the ball in the attacking third.
    - Given if the left team steals the ball near the opponent's area.
    """
    if prev_ball_owned_team == 1 and ball_owned_team == 0 and ball_x > 0.5:
        reward += 4  

    """
    NEGATIVE PENALTIES
    """

    """
    Penalty for conceding a goal.
    - A higher penalty is applied if the team was tied or losing.
    - A lower penalty is applied if the team was already winning.
    """
    if (score[1] - prev_score[1]) == 1:  # Opponent just scored
        if prev_score[0] > prev_score[1]:  # You were winning before
            reward -= 5  
        elif prev_score[0] < prev_score[1]:  # You were already losing
            reward -= 6  
        else:  # It was tied before
            reward -= 8  

    """
    Penalty for losing possession in the defensive third.
    - Applied if the team loses the ball near their own goal area.
    """
    if prev_ball_owned_team == 0 and ball_owned_team != 0 and ball_x < -0.5:
        reward -= 3  

    """
    Penalty for a failed pass.
    - Applied if the team loses possession immediately after a pass.
    """
    if action in PASS_ACTIONS and prev_ball_owned_team == 0 and ball_owned_team != 0:
        reward -= 2  

    """
    Penalty for committing a foul in the defensive third.
    - Applied if the team commits a foul in their own half.
    """
    if action == TACKLE_ACTION and ball_x < -0.5 and ball_owned_team != 0:
        reward -= 3  

    """
    Penalty for a shot that misses the target.
    - Applied if a shot goes out of bounds without being saved.
    """
    if action == SHOOT_ACTION and ball_owned_team == -1:  
        reward -= 2  

    """
    Penalty for a failed dribble.
    - Applied if the player loses possession after attempting to dribble.
    """
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team != 0:
        reward -= 2  

    """
    Penalty for being offside.
    - Applied if the left team commits an offside offense after a pass.
    - Possession changes to the opponent's team.
    """
    if action in PASS_ACTIONS and state.get('offside', False):
        reward -= 2  

    """
    Penalty for receiving a red card.
    - A higher penalty is applied if the team is losing.
    - A lower penalty is applied if the team is winning.
    """
    if 'red_card' in state and state['red_card'] > previous_state.get('red_card', 0):  
        if prev_score[0] > prev_score[1]:  
            reward -= 5  
        else:  
            reward -= 7  

    """
    Penalty for losing possession in the midfield third.
    - Applied if the team loses the ball in the central area of the field.
    """
    if prev_ball_owned_team == 0 and ball_owned_team != 0 and -0.5 <= ball_x <= 0.5:
        reward -= 2  

    return reward
