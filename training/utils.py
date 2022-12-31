import sys
import copy
'''
This module contains common utility functions for training.
'''
import numpy as np
sys.path.append("../")
from sorting_battle_gym.game_board_state import GameBoardState
from training.action_table import ACTION_TABLE
import matplotlib.pyplot as plt

game_board_config = {
  'seed' : None,
  'row_count' : 10,
  'column_count' : 5,
  'number_upper_bound' : 10,
  'minimum_sorted_length' : 3,
  'base_remove_score' : 50,
  'remove_length_bonus' : 25,
  'max_effective_combo' : 10,
  'combo_score_step' : 2,
}

ACTION_SWAP = 1
ACTION_SELECT = 2
ACTION_ADD = 3
MAX_NEGATIVE_REWARD = -10000
ACTION_SIZE = 641
MAX_GRID = 9
MIN_GRID = -2

def normalize_game_state(game_state):
    """
    Normalize grid values to 0-1
    :param game_state: 2d list, value = -2 ~ 9
    :return: normalized 2d list, value = 0 ~ 1
    """
    new_game_state = dict()
    for key in game_state.keys():
        if key == 'grid':
            new_grid = np.array(game_state[key])
            new_grid = (new_grid - MIN_GRID)/(MAX_GRID - MIN_GRID)
            new_grid = list([list(row) for row in new_grid])
            new_game_state[key] = new_grid
        else:
            new_game_state[key] = game_state[key]
    return new_game_state

def is_legal_action(action_type, action_data, game_state_grid):
    """
    Check if the action is legal
    :param action_type: swap, select
    :param action_data: (x, y) or a list of (x, y)
    :param game_state_grid: current board state
    :return: bool
    """
    game_board_state = GameBoardState(game_board_config)
    game_board_state.game_grid_state.load_grid(game_state_grid)
    try:
        if action_type == ACTION_SELECT:
            return game_board_state.game_controller_state.select(action_data)[0] > 0
        elif action_type == ACTION_SWAP:
            return game_board_state.game_controller_state.swap(action_data)
        elif action_type == ACTION_ADD:
            return True
    except:
        return False

def trans_action_id(action_id):
    """
    Convert action ID to gym format
    :param action_id: action id (0-1800)
    :return: gym format (action_type, (list of)[coordinates])
    """
    return copy.deepcopy(ACTION_TABLE[action_id][0]), copy.deepcopy(ACTION_TABLE[action_id][1])

def select_act(action, grid, choose_legal=True):
    """
    Select action from network output
    :param action: all actions in action space
    :param grid: current board
    :param choose_legal: whether to mask illegal actions
    :return: selected action in gym format
    """
    if choose_legal:
        legal_action_space = []
        for _, act in enumerate(action):
            action_type, action_data = trans_action_id(_)
            if is_legal_action(action_type, action_data, grid):
                legal_action_space.append(act)
            else:
                # make sure won't be selected
                legal_action_space.append(MAX_NEGATIVE_REWARD)

        legal_action_space = np.array(legal_action_space)
        action_id = legal_action_space.argmax()
    else:
        action_id = action.argmax()

    return trans_action_id(action_id)

# testing
# game_state = [[1, 2, 3, 9], [-2, -1, 0, 8], [4, 5, 6, 7]]
# print(normalize_game_state(game_state))

def plot_curve(train_rewards, filename):
    plt.xlabel('episode')
    plt.ylabel('reward')

    x1 = np.arange(0, EPISODE_NUM)
    plt.plot(x1, train_rewards, c='blue', label='train')

    leg = plt.legend(loc='upper left')
    plt.title(filename)
    plt.savefig(filename + ".jpg")