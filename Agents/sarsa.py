import numpy as np
import csv
from Utils.discretizer import discretize_observation
from Utils.action_selection import epsilon_greedy_action
from Rewards.defensive_rewards import calculate_rewards
from Utils.calculate_stats import calculate_stats

class SarsaAgent:
    def __init__(self, env, config):
        self.env = env
        self.alpha = config["alpha"]
        self.gamma = config["gamma"]
        self.epsilon = config.get("epsilon_start", 1.0)
        self.epsilon_min = config.get("epsilon_min", 0.05)
        self.epsilon_decay = config.get("epsilon_decay", 0.995)
        self.num_episodes = config["num_episodes"]
        self.q_table = {}
        self.config = config
        self.results_file = 'Results/sarsa_summary.csv'

        with open(self.results_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Episode", "Total Reward", "Final Score", "Total Passes", "Failed Passes", "Total Shots", "Successful Shots", "Opponent Shots", "Possession Time", "Interceptions", "Dribbles", "Successful Dribbles", "Tackles"])

    def train(self):
        rewards_per_episode = []  

        for episode in range(1, self.num_episodes + 1):
            obs = self.env.reset()
            state = discretize_observation(obs[0], self.config)
            action = epsilon_greedy_action(self.q_table, state, self.env.action_space, self.epsilon)
            
            total_reward = 0
            game_stats = {
                "total_passes": 0, "failed_passes": 0, "total_shots": 0, "successful_shots": 0,
                "opponent_shots": 0, "possession_time": 0, "interceptions": 0, "dribbles": 0,
                "successful_dribbles": 0, "tackles": 0
            }
            done = False
            last_obs = obs[0]

            while not done:
                next_obs, _, done, _ = self.env.step(action)
                next_state = discretize_observation(next_obs[0], self.config)
                next_action = epsilon_greedy_action(self.q_table, next_state, self.env.action_space, self.epsilon)

                reward = calculate_rewards(state, action, next_state)
                total_reward += reward

                calculate_stats(game_stats, action, last_obs, next_obs[0])
                
                self.q_table.setdefault(state, np.ones(self.env.action_space.n) * 1.0)
                self.q_table.setdefault(next_state, np.ones(self.env.action_space.n) * 1.0)

                self.q_table[state][action] += self.alpha * (
                    reward + self.gamma * self.q_table[next_state][next_action] - self.q_table[state][action]
                )
                
                state, action, last_obs = next_state, next_action, next_obs[0]

            final_score = f"{last_obs['score'][0]} - {last_obs['score'][1]}"
            rewards_per_episode.append(total_reward)

            with open(self.results_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([episode, total_reward, final_score, *game_stats.values()])

            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

        return rewards_per_episode

