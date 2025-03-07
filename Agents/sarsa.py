import numpy as np
import csv
from Utils.discretizer import discretize_observation
from Utils.action_selection import epsilon_greedy_action
from Rewards.rewards import calculate_rewards

class SarsaAgent:
    def __init__(self, env, config):
        self.env = env
        self.alpha = config["alpha"]
        self.gamma = config["gamma"]
        self.epsilon = config["epsilon"]
        self.num_episodes = config["num_episodes"]
        self.q_table = {}
        self.config = config
        self.results_file = 'Results/sarsa_results.csv'

        with open(self.results_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "Total Reward", "Final Score"])

    def train(self):
        for episode in range(1, self.num_episodes + 1):
            obs = self.env.reset()
            state = discretize_observation(obs[0], self.config)
            action = epsilon_greedy_action(self.q_table, state, self.env.action_space, self.epsilon)
            total_reward = 0
            done = False
            last_obs = obs[0]

            while not done:
                next_obs, _, done, _ = self.env.step(action)
                next_state = discretize_observation(next_obs[0], self.config)
                next_action = epsilon_greedy_action(self.q_table, next_state, self.env.action_space, self.epsilon)

                reward = calculate_rewards(next_obs[0], action, last_obs)
                total_reward += reward

                if state not in self.q_table:
                    self.q_table[state] = np.zeros(self.env.action_space.n)
                if next_state not in self.q_table:
                    self.q_table[next_state] = np.zeros(self.env.action_space.n)

                self.q_table[state][action] += self.alpha * (
                    reward + self.gamma * self.q_table[next_state][next_action] - self.q_table[state][action]
                )

                state, action, last_obs = next_state, next_action, next_obs[0]

            final_score = f"{last_obs['score'][0]} - {last_obs['score'][1]}"
            print(f"Episode {episode}: Total Reward = {total_reward} | Score: {final_score}")
            
            with open(self.results_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([episode, total_reward, final_score])
