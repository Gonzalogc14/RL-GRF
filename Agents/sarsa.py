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

        self.epsilon_start = config.get("epsilon_start", 1.0)
        self.epsilon_min = config.get("epsilon_min", 0.05)
        self.epsilon_decay = config.get("epsilon_decay", 0.995)
        self.epsilon = self.epsilon_start

        self.num_episodes = config["num_episodes"]
        self.q_table = {}
        self.config = config

        self.results_file = 'Results/sarsa_results.csv'
        self.q_values_file = 'Results/q_values.csv' 
        self.actions_file = 'Results/sarsa_actions.csv'

        with open(self.results_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "Total Reward", "Final Score", "Total Passes", "Failed Passes"])

        with open(self.q_values_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "State", "Action", "Q-value"])
        
        with open(self.actions_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "Step", "Action", "Reward"])

    def train(self):
        rewards_per_episode = []  

        for episode in range(1, self.num_episodes + 1):
            obs = self.env.reset()
            state = discretize_observation(obs[0], self.config)
            action = epsilon_greedy_action(self.q_table, state, self.env.action_space, self.epsilon)
            
            total_reward = 0
            total_passes = 0
            failed_passes = 0
            done = False
            last_obs = obs[0]
            step = 0

            while not done:
                next_obs, _, done, _ = self.env.step(action)
                next_state = discretize_observation(next_obs[0], self.config)
                next_action = epsilon_greedy_action(self.q_table, next_state, self.env.action_space, self.epsilon)

                reward = calculate_rewards(next_obs[0], action, last_obs)
                total_reward += reward

                if action in [9, 10, 11] and last_obs['ball_owned_team'] == 0:
                    total_passes += 1
                    if next_obs[0]['ball_owned_team'] != 0:
                        failed_passes += 1  # Si no mantiene posesión, cuenta como fallo

                if state not in self.q_table:
                    self.q_table[state] = np.ones(self.env.action_space.n) * 1.0  
                if next_state not in self.q_table:
                    self.q_table[next_state] = np.ones(self.env.action_space.n) * 1.0

                self.q_table[state][action] += self.alpha * (
                    reward + self.gamma * self.q_table[next_state][next_action] - self.q_table[state][action]
                )

                with open(self.actions_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([episode, step, action, reward])
                
                step += 1
                state, action, last_obs = next_state, next_action, next_obs[0]

            final_score = f"{last_obs['score'][0]} - {last_obs['score'][1]}"
            rewards_per_episode.append(total_reward)

            with open(self.results_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([episode, total_reward, final_score, total_passes, failed_passes])

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

        return rewards_per_episode
