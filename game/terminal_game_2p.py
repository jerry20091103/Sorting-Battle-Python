'''
This is a interactive terminal version of the 2P game for testing.
Also serves as an example of how to use the gym in 2P mode
'''
# add include path
import sys
sys.path.append("../")
from terminal_game_util import show_game_status, get_action_from_terminal
from sorting_battle_gym.game_base import GameBase

LINE_UP = '\033[1A'

def player1_callback(game_status):
    '''
    Callback to control the player 1 from terminal.
    '''
    # show player game status
    if game_status['game_end']:
        print("###############")
        if game_status['win_flag'] == 1:
            print("player1 win!")
        elif game_status['win_flag'] == 0:
            print("player1 lose!")
        print("###############")
    print("-----------")
    print("| player1 |")
    print("-----------")
    show_game_status(False, game_status['game_end'], game_status['level'], game_status['score'], game_status['grid'], game_status['pressure'])
    print(LINE_UP * 19, end='')
    tabs = '\t\t\t\t\t'
    print(tabs, "------------")
    print(tabs, "| opponent |")
    print(tabs, "------------")
    show_game_status(True, game_status['game_end'], game_status['level'], game_status['opponent_score'], game_status['opponent_grid'], game_status['opponent_pressure'])
    # get action

    return get_action_from_terminal()

def player2_callback(game_status):
    '''
    Callback to control the player 1 from terminal.
    '''
    # show player game status
    if game_status['game_end']:
        print("###############")
        if game_status['win_flag'] == 1:
            print("player2 win!")
        elif game_status['win_flag'] == 0:
            print("player2 lose!")
        print("###############")
    print("-----------")
    print("| player2 |")
    print("-----------")
    show_game_status(False, game_status['game_end'], game_status['level'], game_status['score'], game_status['grid'], game_status['pressure'])
    print(LINE_UP * 19, end='')
    tabs = '\t\t\t\t\t'
    print(tabs, "------------")
    print(tabs, "| opponent |")
    print(tabs, "------------")
    show_game_status(True, game_status['game_end'], game_status['level'], game_status['opponent_score'], game_status['opponent_grid'], game_status['opponent_pressure'])
    # get action
    return get_action_from_terminal()

config = {
    'player_count': 2,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'player_add_new_row_delay': 50,
    'realtime': False
}
game_base = GameBase(config)
game_base.set_callback(player1_callback, 1)
game_base.set_callback(player2_callback, 2)

game_base.run_game()
