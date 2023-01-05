'''
This is a terminal version of the 1P random play for training
'''
import sys
sys.path.append("../")
import random
from training.utils import is_legal_action, trans_action_id

# training settings
IDLE_TIME=8
EPISODE_NUM=10

def random_player_callback(game_state):
    '''
    the model gets the current state of the game
    '''
    grid = game_state['grid']

    legal_action_space = []
    for i in range(641):
        action_type, action_data = trans_action_id(i)
        if is_legal_action(action_type, action_data, grid):
            legal_action_space.append(i)

    # if there is no legal action, idle
    if legal_action_space == []:
        action_type = 0
        action_data = IDLE_TIME
        return action_type, action_data

    action_id = random.choice(legal_action_space)
    # convert the action to the format that the gym can understand
    action_type, action_data = trans_action_id(action_id)
    return action_type, action_data
