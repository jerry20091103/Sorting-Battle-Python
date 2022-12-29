import sys
'''
This module contains common utility functions for training.
'''
import numpy as np
sys.path.append("../")
from sorting_battle_gym.game_board_state import GameBoardState

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
ID_ADD_LINE = 1800
MAX_NEGATIVE_REWARD = -10000
ACTION_DIRECTIONS = {0: (0, -1), 1: (0, 1), 2: (-1, 0), 3: (1, 0)}

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

def swap_converter(move_dir, pos_id):
    """
    Handle convertion of action type = swap
    :param move_dir: direction of swapping, left/right/down/up
    :param pos_id: starting point
    :return: action_type, [start_xy, end_xy]
    """
    action_type = ACTION_SWAP
    direction = ACTION_DIRECTIONS[move_dir]
    action_data = [[-1, -1], [-1, -1]]
    action_data[0] = [pos_id // 5, pos_id % 5]
    action_data[1] = [action_data[0][0] + direction[0], action_data[0][1] + direction[1]]
    return action_type, action_data

def select_converter(move_dir, pos_id, move_type):
    """
    Handle convertion of action type = select
    :param move_dir: direction of eliminating, left/right/down/up
    :param pos_id: starting point
    :param move_type: num. of squares to eliminate (including starting point)
    :return: action_type, [start_xy, ..., end_xy]
    """
    action_type = ACTION_SELECT
    direction = ACTION_DIRECTIONS[move_dir]
    action_data = []
    action_data.append([pos_id // 5, pos_id % 5])
    for _ in range(move_type + 1):
        action_data.append([action_data[-1][0] + direction[0], action_data[-1][1] + direction[1]])
    return action_type, action_data

def trans_action_id(action_id):
    """
    Convert action ID to gym format
    :param action_id: action id (0-1800)
    :return: gym format (action_type, (list of)[coordinates])
    """
    if action_id == ID_ADD_LINE:
        return ACTION_ADD, None

    pos_id = action_id // 36
    move_id = action_id % 36
    move_dir = move_id // 9
    move_type = move_id % 9 # 0:swap, 1-8: select 3-10 squares (including starting pnt)

    if move_type == 0:
        return swap_converter(move_dir, pos_id)
    return select_converter(move_dir, pos_id, move_type)


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
