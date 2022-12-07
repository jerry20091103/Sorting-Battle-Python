from sorting_battle_gym.game_state import GameState

def print_callback(input_ticks):
    print("outside callback, current tick:", input_ticks)
    return 10
def print_callback2(input_ticks):
    print("outside callback2, current tick:", input_ticks)
    return 20

def agent_callback(grid, score, level):
    # do stuff
    return action_type, coord_list

config = {'swap_delay': 1, 'remove_delay': 1}
game_state = GameState(config)
# game_state.set_player_callback(print_callback, 1)
# game_state.set_player_callback(print_callback2, 2)
game_state.run_game()
