import sys
'''
This module contains common utility functions for training.
'''
import numpy as np
sys.path.append("../")
from sorting_battle_gym.game_board_state import GameBoardState
from training.action_table import ACTION_TABLE

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
ACTION_SIZE = 640

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
    return ACTION_TABLE[action_id]


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

        # if there is no legal action, idle
        if np.max(legal_action_space) == MAX_NEGATIVE_REWARD:
            action_type, action_data = 0, 10
        return action_type, action_data
    else:
        action_id = action.argmax()

    return trans_action_id(action_id)
