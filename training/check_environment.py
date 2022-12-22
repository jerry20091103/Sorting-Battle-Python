from stable_baselines3.common.env_checker import check_env
from sorting_battle_env import SortingBattleEnv

env = SortingBattleEnv()
check_env(env)