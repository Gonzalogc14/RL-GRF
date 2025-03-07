import gfootball.env as football_env

def create_environment():
    return football_env.create_environment(
        env_name='11_vs_11_stochastic',
        representation='raw'
    )
