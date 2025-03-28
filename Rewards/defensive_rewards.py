def calculate_rewards(state, action, previous_state):
    """
    Calculates rewards and penalties for the left team based on the current and previous state.
    """
    reward = 0
    score, prev_score = state[95], previous_state[95]  
    ball_x = state[0]  # En un rango de 0 a 20 (bins)
    ball_owned_team, prev_ball_owned_team = state[98], previous_state[98]  
    left_team_yellow_cards, prev_left_team_yellow_cards = state[99:], previous_state[29:] 

    PASS_ACTIONS = [9, 10, 11]
    SHOOT_ACTION = 12
    DRIBBLE_ACTION = 18
    TACKLE_ACTION = 16
    
    """
    POSITIVE REWARDS
    """
    
    ## Recompensa por ganar posesión en diferentes zonas del campo
    if prev_ball_owned_team == 1 and ball_owned_team == 0:
        reward += 4  
        if ball_x < 5:  # Zona defensiva
            reward += 6  
        elif 5 <= ball_x <= 10:  # Zona media-baja
            reward += 4  
        elif 10 < ball_x <= 15:  # Zona media-alta
            reward += 3  
        if action == TACKLE_ACTION:
            reward += 7  
    
    ## Gol anotado
    if score > prev_score:
        reward += 500  

    ## Pases exitosos en diferentes zonas
    if action in PASS_ACTIONS and prev_ball_owned_team == 0 and ball_owned_team == 0:
        if ball_x < 10:
            reward += 4  # Pase en zona defensiva/media-baja
        else:
            reward += 6 if action == 9 else 3  # Pase largo (6) vs corto (3)

    ## Ganar un córner
    if state[35] == 4 and ball_owned_team == 0:
        reward += 5  

    ## Posicionamiento defensivo correcto
    if ball_owned_team == 1:
        left_team_positions = state[3:25]  
        for i in range(0, 22, 2):  
            if left_team_positions[i] < 5:  # Jugadores en zona defensiva
                reward += 1  

    ## Dribbling exitoso
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team == 0:
        reward += 6  

    ## Falta sin tarjeta amarilla
    if state[97] == 3 and prev_ball_owned_team != 0 and not any(left_team_yellow_cards):
        reward += 4  

    """
    NEGATIVE PENALTIES
    """

    ## Penalización por gol concedido
    if score < prev_score:
        reward -= 400  
    
    ## Pérdida de posesión en diferentes zonas
    if prev_ball_owned_team == 0 and ball_owned_team != 0:
        if ball_x < 5:
            reward -= 8  # Pérdida en zona defensiva
        elif ball_x < 10:
            reward -= 5  # Pérdida en zona media-baja
        else:
            reward -= 3  # Pérdida en zona ofensiva

    ## Errores defensivos
    if action == TACKLE_ACTION and ball_x < 5 and ball_owned_team != 0:
        reward -= 6  
    
    ## Disparo fallido
    if action == SHOOT_ACTION and prev_ball_owned_team == 1:
        reward -= 6  
    
    ## Tiro lejano con pérdida de posesión
    if prev_ball_owned_team == 1 and ball_owned_team == -1 and action == SHOOT_ACTION and ball_x < 5:
        reward -= 5  

    ## Penalización por tarjeta amarilla
    for i in range(len(left_team_yellow_cards)):
        if left_team_yellow_cards[i] > prev_left_team_yellow_cards[i]:
            reward -= 5  

    ## Dribbling fallido
    if action == DRIBBLE_ACTION and prev_ball_owned_team == 0 and ball_owned_team != 0:
        reward -= 6  

    return reward
