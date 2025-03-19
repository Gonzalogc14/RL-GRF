import json
from Agents.sarsa import SarsaAgent
from Environment.env import create_environment

def load_config(path):
    with open(path, 'r') as file:
        return json.load(file)

if __name__ == "__main__":
    config = load_config('Config/config.json')
    env = create_environment()
    agent = SarsaAgent(env, config)
    agent.train()
