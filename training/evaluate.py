'''
This script is used to evaluate the performance of 2P models
'''
import sys
sys.path.append("../")
from training.utils import select_act, normalize_game_state, ACTION_SIZE
from training.random_play import random_player_callback
from sorting_battle_gym.game_base import GameBase
from sorting_battle_gym.game_board_state import GameBoardState
from training.ppo_agent import PPOAgent

N_GAMES = 100
config = {
    'player_count': 2,
    'player_swap_delay': 30,
    'player_select_delay': 50,
    'player_add_new_row_delay': 20,
    'realtime': False
}
agent = {'A': 'random agent', 'a': 'random agent',
         'B': 'ppo agent', 'b': 'ppo agent'}
def player1_callback(game_state):
    """
    Player1's callback function
    :param game_state: current game state
    :return: the action player1's going to act
    """
    # the model takes action according to current state of the game
    action= model_player1.act(normalize_game_state(game_state))[0]

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])
    return action_type, action_data
def player2_callback(game_state):
    """
    Player2's callback function
    :param game_state: current game state
    :return: the action player2's going to act
    """
    # the model takes action according to current state of the game
    action= model_player2.act(normalize_game_state(game_state))[0]

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])
    return action_type, action_data

player1, player2 = '', ''
policy_path_1, value_path_1 = '', ''
policy_path_2, value_path_2 = '', ''

print('============================================')
print('A. random agent')
print('B. ppo agent')
while True:
    player1 = input('choose player 1 (A/B): ')
    if player1 in agent.keys():
        player1 = agent[player1]
        break
    print('input "A" or "B", lowercase is also acceptable')
if player1 == 'ppo agent':
    SUCCESS = False
    while not SUCCESS:
        policy_path_1 = input('player1\'s policy network path: ')
        value_path_1 = input('player1\'s value network path: ')
        try:
            model_player1 = PPOAgent(50, ACTION_SIZE, policy_path_1, value_path_1)
            model_player1.set_evaluation_mode()
            SUCCESS = True
        except:
            print('please try again...')
print('============================================')
print('A. random agent')
print('B. ppo agent')
while True:
    player2 = input('choose player 2 (A/B): ')
    if player2 in agent.keys():
        player2 = agent[player2]
        break
    print('input "A" or "B", lowercase is also acceptable')
if player2 == 'ppo agent':
    SUCCESS = False
    while not SUCCESS:
        policy_path_2 = input('player2\'s policy network path: ')
        value_path_2 = input('player2\'s value network path: ')
        try:
            model_player2 = PPOAgent(100, ACTION_SIZE, policy_path_2, value_path_2)
            model_player2.set_evaluation_mode()
            SUCCESS = True
        except Exception as e:
            print(e)
            print('please try again...')
print('============================================')

print('Evaluation Info:')
print(f'player1: {player1}')
if policy_path_1 and value_path_1:
    print(f'- policy network: {policy_path_1}')
    print(f'- value network: {value_path_1}')
print(f'player2: {player2}')
if policy_path_2 and value_path_2:
    print(f'- policy network: {policy_path_2}')
    print(f'- value network: {value_path_2}')
print('============================================')

print(f'Start evaluating {N_GAMES} games...')
n_player1_win, n_player2_win = 0, 0
for _ in range(N_GAMES):
    game_base = GameBase(config)
    if player1 == 'random agent':
        game_base.set_callback(random_player_callback, 1)
    else:
        game_base.set_callback(player1_callback, 1)
    if player2 == 'random agent':
        game_base.set_callback(random_player_callback, 2)
    else:
        game_base.set_callback(player2_callback, 2)
    game_base.run_game()
    player1_status, player2_status = [state.game_board_state.status for state in game_base.game_state.player_states]
    if _ == 0:
        print('-----------------------------')
    if player1_status == GameBoardState.Status.WIN or player2_status == GameBoardState.Status.LOSE:
        n_player1_win += 1
        print(f'- Game {_ + 1:02}: 1P wins')
    elif player2_status == GameBoardState.Status.WIN or player1_status == GameBoardState.Status.LOSE:
        n_player2_win += 1
        print(f'- Game {_ + 1:02}: 2P wins')
    else:
        n_player1_win += 0.5
        n_player2_win += 0.5
        print(f'- Game {_ + 1:02}: draw')
print('-----------------------------')
print(f'player1\'s win rate: {n_player1_win/N_GAMES} ({n_player1_win}/{N_GAMES})')
print(f'player2\'s win rate: {n_player2_win/N_GAMES} ({n_player2_win}/{N_GAMES})')
print('============================================')
