'''
This is a interactive terminal version of the 2P game for testing.
Also serves as an example of how to use the gym in 2P mode
'''
# add include path
import sys
sys.path.append("../")
from sorting_battle_gym.game_base import GameBase
from terminal_game_util import *

def player1_callback(game_status):
    '''
    Callback to control the player 1 from terminal.
    '''
    # show player game status
    print("-----------")
    print("| player1 |")
    print("-----------")
    show_game_status(game_status['game_end'], game_status['level'], game_status['score'], game_status['grid'])
    print("------------")
    print("| opponent |")
    print("------------")
    show_game_status(game_status['game_end'], game_status['level'], game_status['opponent_score'], game_status['opponent_grid'])
    # get action
    return get_action_from_terminal()

def player2_callback(game_status):
    '''
    Callback to control the player 1 from terminal.
    '''
    # show player game status
    print("-----------")
    print("| player2 |")
    print("-----------")
    show_game_status(game_status['game_end'], game_status['level'], game_status['score'], game_status['grid'])
    print("------------")
    print("| opponent |")
    print("------------")
    show_game_status(game_status['game_end'], game_status['level'], game_status['opponent_score'], game_status['opponent_grid'])
    # get action
    return get_action_from_terminal()

config = {
    'player_count': 2,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'realtime': False
}
game_base = GameBase(config)
game_base.set_callback(player1_callback, 1)
game_base.set_callback(player2_callback, 2)

game_base.run_game()
