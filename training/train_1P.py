import sys
sys.path.append("../")

from game.terminal_game_util import show_game_status
from sorting_battle_gym.game_base import GameBase
from training.training_model_1P import NeuralNetwork
from training.training_model_1P import Buffer
from training.training_model_1P import ppo_agent
import numpy as np
import torch

model_save_name = 'model/training_model_1P.pt'
path = f"{model_save_name}" 

# save model
# torch.save(model_player1, path)

# load model
model_player1 = torch.load(path)

# define the callback function
def player1_callback(game_state):
    # show_game_status(False, game_state['game_end'], game_state['level'], game_state['score'], game_state['grid'])
    
    # the model gets the current state of the game
    # the model takes action according to current state of the game
    action, log_prob = model_player1.act(game_state)
    # the current state is stored to replay memory for future learning
    # model_player1.store_state(current_state)
    model_player1.buffer.states.append([item for sublist in game_state["grid"] for item in sublist])
    model_player1.buffer.actions.append(action)
    model_player1.buffer.log_probs.append(log_prob)
    # convert the action to the format that the gym can understand
    # action_type, action_data = trans_act(action)
    action_type, action_data = trans_act(action, game_state["grid"])
    
    if is_legal_action(action_type, action_data, game_state["grid"]):
      model_player1.buffer.episode_rewards.append(game_state["score"])
    else:
      model_player1.buffer.episode_rewards.append(-10000)
      action_data = 10 if action_type == ACTION_SWAP else 50 
      action_type = 0 
      
    if model_player1.counter > UPDATE_INTERVAL:
        # print('update')
        model_player1.buffer.rewards.append(model_player1.buffer.episode_rewards)
        model_player1.buffer.episode_rewards = []
        # print('model_player1.buffer.rewards:', model_player1.buffer.rewards)
        model_player1.update_network()
      
    # give the action to the gym
    print(f'action_type: {action_type}, action_data: {action_data}')
    return action_type, action_data

# initialize the gym
config = {
    'player_count': 1,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}

# check performance
game_base = GameBase(config)
# set the callback function
game_base.set_callback(player1_callback, 1)
# run the game
game_base.run_game()
print("=================================================")
print("score: " + str(game_base.game_state.game_board_state.game_score_state.total_score))
