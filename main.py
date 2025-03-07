import json
from Environment.env import create_environment
from Agents.sarsa_agent import SarsaAgent

def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    config = load_config('config/config.json')
    env = create_environment()
    agent = SarsaAgent(env, config)
    agent.train()
