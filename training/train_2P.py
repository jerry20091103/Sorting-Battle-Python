'''
This is a terminal version of the 2P game for training
'''
import sys
sys.path.append("../")
from training.utils import select_act, normalize_game_state, ACTION_SIZE, plot_curve
from training.random_play import random_player_callback
from sorting_battle_gym.game_base import GameBase
from sorting_battle_gym.game_board_state import GameBoardState
from training.ppo_agent import PPOAgent

# training settings
LEGAL_ACT_COST = 1
MAX_NEGATIVE_REWARD = -10000
EPISODE_NUM = 10000
TRAINING_STEP = 50

# initialize the gym
config = {
    'player_count': 2,
    'player_swap_delay': 30,
    'player_select_delay': 50,
    'player_add_new_row_delay': 20,
    'realtime': False
}

def player1_callback(game_state, to_print=False):
    """
    Player1's callback function
    :param game_state: current game state
    :return: the action player1's going to act
    """
    # the model takes action according to current state of the game
    action, log_prob = model_player1.act(normalize_game_state(game_state))

    # the current state is stored to replay memory for future learning
    normalized_state = normalize_game_state(game_state)
    grid = normalized_state['grid'][:]
    grid = [item for sublist in grid for item in sublist]
    opp_grid = normalized_state['opponent_grid'][:]
    opp_grid = [item for sublist in opp_grid for item in sublist]
    features = grid + opp_grid
    model_player1.buffer.states.append(features)
    model_player1.buffer.actions.append(action)
    model_player1.buffer.log_probs.append(log_prob)

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])

    if game_state['game_end']:
        # print("win_flag of P1: " + str(game_state['win_flag']))
        if game_state['win_flag']:
            reward = - MAX_NEGATIVE_REWARD + (game_state['score'] - game_state['opponent_score'])
            model_player1.prev_score = 1 # means WIN
        else:
            reward = MAX_NEGATIVE_REWARD + (game_state['score'] - game_state['opponent_score'])
            model_player1.prev_score = 0 # means LOSE
    else:
        reward = game_state["score"] - model_player1.prev_score - LEGAL_ACT_COST
        model_player1.prev_score = game_state["score"]

    if to_print:
        print("Reward: " + str(reward))
    model_player1.buffer.episode_rewards.append(reward)

    # give the action to the gym
    if to_print:
        print(f'In P1, action_type: {action_type}, action_data: {action_data}')
    return action_type, action_data

# def player2_callback(game_state):
#     """
#     Player2's callback function
#     :param game_state: current game state
#     :return: the action player2's going to act
#     """
#     # the model takes action according to current state of the game
#     action= model_player2.act(normalize_game_state(game_state))[0]

#     # convert the action to the format that the gym can understand
#     action_type, action_data = select_act(action, game_state["grid"])
#     return action_type, action_data

# or load model
model_folder = 'model/1_backup/'
path_policy1 = model_folder + 'policy_10000.pt'
path_value1 = model_folder + 'value_10000.pt'

model_player1 = PPOAgent(100, ACTION_SIZE, path_policy1, path_value1) #, path_policy1, path_value1)
model_player1.set_training_mode()
P1_win = 0
p1_win_rates = []
latest_policy, latest_value = '', ''

for i in range(10000, 10000 + EPISODE_NUM):
    game_base = GameBase(config)
    # set the callback function
    game_base.set_callback(player1_callback, 1)
    game_base.set_callback(random_player_callback, 2)

    # run the game
    game_base.run_game()

    model_player1.buffer.rewards.append(model_player1.buffer.episode_rewards[1:]+[0])
    model_player1.buffer.episode_rewards = []
    model_player1.update_network()

    player1_states, player2_states = [player_state for player_state in\
            game_base.game_state.player_states]
    score1, score2 = [player_states.game_board_state.game_score_state.total_score\
            for player_states in [player1_states, player2_states]]
    player1_status, player2_status = [player_states.game_board_state.status\
            for player_states in [player1_states, player2_states]]

    if i == 0:
        print("=================================================")
    print(f"EPISODE_NUM: {i + 1}/{10000 + EPISODE_NUM}")
    print(f"score of P1: {score1}")
    print(f"score of P2: {score2}")
    if player1_status == GameBoardState.Status.WIN or player2_status == GameBoardState.Status.LOSE:
        P1_win += 1
        print('winner: P1')
    elif player2_status == GameBoardState.Status.WIN or player1_status == GameBoardState.Status.LOSE:
        P1_win += 0
        print('winner: P2')
    else:
        P1_win += 0.5
        print('draw .5-.5')
    print("=================================================")
    if i % TRAINING_STEP == (TRAINING_STEP - 1):
        current_win_rate = P1_win/TRAINING_STEP
        p1_win_rates.append(current_win_rate)
        print('win rate backup...')
        with open('train_win_rate.txt', 'w') as txt:
            print(p1_win_rates, file=txt)
        print(f'step: {i + 1}/{10000 + EPISODE_NUM}, win rate: {current_win_rate} ({P1_win}/{TRAINING_STEP})')
        print('model backup...')
        latest_policy = f'model/1_backup/policy_{i + 1}.pt'
        latest_value = f'model/1_backup/value_{i + 1}.pt'
        model_player1.save_model(latest_policy, latest_value)
        print('image backup...')
        plot_curve(p1_win_rates, 'training step', f'win_rate / {TRAINING_STEP} games', \
                    'agent training win rate', f'image_backup/1_backup/win_rate_{i + 1}.jpg')
        # print(f'image_backup/zero/win_rate_{i + 1}.jpg')
        print('=================================================')
        P1_win = 0
