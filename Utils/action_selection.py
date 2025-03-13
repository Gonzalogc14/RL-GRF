import numpy as np

def epsilon_greedy_action(q_table, state, action_space, epsilon):
    if np.random.rand() < epsilon:
        action = action_space.sample() 
    else:
        action = np.argmax(q_table.get(state, np.zeros(action_space.n)))  
    return action
