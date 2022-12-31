'''
This is a terminal version of the 1P random play for training
'''
import sys
sys.path.append("../")
import random
from sorting_battle_gym.game_base import GameBase
from training.utils import is_legal_action, trans_action_id


# training settings
IDLE_TIME=8
EPISODE_NUM=10

def random_playcallback(game_state):
    # show_game_status(False, game_state['game_end'], game_state['level'], game_state['score'], game_state['grid'])

    # the model gets the current state of the game
    # the model takes action according to current state of the game
    grid=game_state['grid']

    legal_action_space = []
    for i in range(641):
        action_type, action_data = trans_action_id(i)
        if is_legal_action(action_type, action_data, grid):
            legal_action_space.append(i)

    # if there is no legal action, idle
    if legal_action_space == []:
        action_type = 0
        action_data = IDLE_TIME
        print(f'In Random, action_type: {action_type}, action_data: {action_data}')
        return action_type, action_data

    action_id = random.choice(legal_action_space)
    # convert the action to the format that the gym can understand
    action_type, action_data = trans_action_id(action_id)

    print(f'In Random, action_type: {action_type}, action_data: {action_data}')
    return action_type, action_data

config = {
    'player_count': 1,
    'player_swap_delay': 40,
    'player_select_delay': 50,
    'player_add_new_row_delay': 10,
    'realtime': False
}

ACCUMULATED_SCORE = 0
for i in range(EPISODE_NUM):
    game_base = GameBase(config)
    # set the callback function
    game_base.set_callback(random_playcallback, 1)
    # run the game
    game_base.run_game()

    print("=================================================")
    print("EPISODE_NUM: " + str(i))
    print("score: " + str(game_base.game_state.game_board_state.game_score_state.total_score))
    print("=================================================")
print("Average score: " + str(ACCUMULATED_SCORE / EPISODE_NUM))
