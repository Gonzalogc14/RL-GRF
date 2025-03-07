import numpy as np

def epsilon_greedy_action(q_table, state, action_space, epsilon):
    if np.random.rand() < epsilon:
        return action_space.sample()
    return np.argmax(q_table.get(state, np.zeros(action_space.n)))
