import numpy as np
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
ACTION_ADD_LINE = 1440
MAX_NEGATIVE_REWARD = -10000

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
    except:
        return False

def trans_action_id(action_id):
    """
    Convert action ID to gym format
    :param action_id: action id (0-1440)
    :return: gym format (action_type, [coordinates])
    """
    action_type = 1
    action_data = [[8, 0], [9, 0]]

    pos_id = action_id // 32
    move_id = action_id % 32
    move_dir = move_id // 8
    move_type = move_id % 8

    action_data[0][0] = pos_id // 5
    action_data[0][1] = pos_id % 5

    if action_id == ACTION_ADD_LINE:
        action_type = 3
        action_data = None
        return action_type, action_data

    if move_type == 0:
        action_type = ACTION_SWAP
        if move_dir == 0:
            action_data[1][0] =  action_data[0][0]
            action_data[1][1] =  action_data[0][1] - 1
        if move_dir == 1:
            action_data[1][0] =  action_data[0][0]
            action_data[1][1] =  action_data[0][1] + 1
        if move_dir == 2:
            action_data[1][0] =  action_data[0][0] - 1
            action_data[1][1] =  action_data[0][1]
        if move_dir == 3:
            action_data[1][0] =  action_data[0][0] + 1
            action_data[1][1] =  action_data[0][1]
    else:
        action_type = ACTION_SELECT
        action_data = [[pos_id // 5, pos_id % 5]]
        for _ in range(1, move_type+2):
            if move_dir == 0:
                action_data.append([action_data[-1][0], action_data[-1][1] - 1])
            if move_dir == 1:
                action_data.append([action_data[-1][0], action_data[-1][1] + 1])
            if move_dir == 2:
                action_data.append([action_data[-1][0] - 1, action_data[-1][1]])
            if move_dir == 3:
                action_data.append([action_data[-1][0] + 1, action_data[-1][1]])
    return action_type, action_data


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
        if action_id == 0:
            action_type = 0
            action_data = 10
        return action_type, action_data
    else:
        action_id = action.argmax()

    action_type, action_data = trans_action_id(action_id)
    return action_type, action_data
