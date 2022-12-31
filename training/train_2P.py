'''
This is a terminal version of the 2P game for training
'''
import sys
sys.path.append("../")
import torch
from training.utils import select_act, normalize_game_state, ACTION_SIZE, plot_curve
from training.random_play import random_playcallback
from sorting_battle_gym.game_base import GameBase
from training.ppo_agent import PPOAgent

# training settings
LEGAL_ACT_COST = 1
MAX_NEGATIVE_REWARD = -10000
EPISODE_NUM = 500
TRAINING_STEP = 10

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
    model_player1.buffer.states.append([item for sublist in normalize_game_state(game_state)["grid"] for item in sublist])
    model_player1.buffer.actions.append(action)
    model_player1.buffer.log_probs.append(log_prob)

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])

    if game_state['game_end']:
        print("win_flag of P1: " + str(game_state['win_flag']))
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

# or load model
model_save_P1_folder = 'model/'
model_save_P2_folder = 'model/'
model_save_P1_name = 'training_model_2P_0.83.pt'
model_save_P2_name = 'training_model_2P_0.83.pt'
path_P1 = model_save_P1_folder + model_save_P1_name
path_P2 = model_save_P2_folder + model_save_P2_name

# model_player1 = torch.load(path_P1)
# model_player2 = torch.load(path_P2)

path_policy1 = model_save_P1_folder + 'training_model_2P_0.83_policy.pt'
path_value1 = model_save_P1_folder + 'training_model_2P_0.83_value.pt'

model_player1 = PPOAgent(50, ACTION_SIZE) #, path_policy1, path_value1)
model_player2 = PPOAgent(50, ACTION_SIZE, path_policy1, path_value1)
P1_win = 0
p1_win_rates = []

with open('training_log_2P.txt', 'w') as f:
    for i in range(EPISODE_NUM):
        game_base = GameBase(config)
        # set the callback function
        game_base.set_callback(player1_callback, 1)
        # game_base.set_callback(player2_callback, 2)
        game_base.set_callback(random_playcallback, 2)
        # run the game
        game_base.run_game()

        if model_player1.prev_score:
            P1_win += 1

        model_player1.buffer.rewards.append(model_player1.buffer.episode_rewards[1:]+[0])
        model_player1.buffer.episode_rewards = []
        model_player1.update_network()
        score1, score2 = [player_state.game_board_state.game_score_state.total_score \
                          for player_state in game_base.game_state.player_states]
        print("=================================================")
        print("EPISODE_NUM: " + str(i))
        print("score of P1: " + str(score1))
        print("score of P2: " + str(score2))
        print("=================================================")
        
        # log into file
        print("=================================================", file = f)
        print("EPISODE_NUM: " + str(i), file = f)
        print("score of P1: " + str(score1), file = f)
        print("score of P2: " + str(score2), file = f)

        if i % TRAINING_STEP == (TRAINING_STEP - 1):
            current_win_rate = P1_win/(i + 1)
            p1_win_rates.append(current_win_rate)
            print(f'step: {i + 1}, win rate: {current_win_rate} ({P1_win}/{i + 1})')
            print('model backup...')
            torch.save(model_player1, f'model/zero_backup/policy_{i + 1}.pt')
            torch.save(model_player1, f'model/zero_backup/value_{i + 1}.pt')
            print('image backup...')
            plot_curve(p1_win_rates, 'training step', f'win_rate / {TRAINING_STEP} games', \
                       'agent training win rate', f'image_backup/zero/win_rate_{i + 1}.jpg')
            print('=================================================')



print(f"P1 win rate: {P1_win}/{EPISODE_NUM} ({P1_win/EPISODE_NUM})")

# print the reward of each episode
plot_curve(p1_win_rates, 'training step', f'win_rate / {TRAINING_STEP} games', \
           'agent training win rate', 'zero_win_rate.jpg')

# save model, be careful of filename (version)
# torch.save(model_player1, path_P1)
# torch.save(model_player2, path_P2)