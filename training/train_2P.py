import sys
import torch
from training.utils import select_act
from sorting_battle_gym.game_base import GameBase
from training.ppo_agent import ppo_agent
sys.path.append("../")


# training settings
UPDATE_INTERVAL=8
EPISODE_NUM=10

# initialize the gym
config = {
    'player_count': 2,
    'player_swap_delay': 10,
    'player_select_delay': 50,
    'player_add_new_row_delay': 50,
    'realtime': False
}

def player1_callback(game_state):
    """
    Player1's callback function
    :param game_state: current game state
    :return: the action player1's going to act
    """
    # show_game_status(False, game_state['game_end'], game_state['level'], \
    # game_state['score'], game_state['grid'])

    # the model takes action according to current state of the game
    action, log_prob = model_player1.act(game_state)

    # the current state is stored to replay memory for future learning
    model_player1.buffer.states.append([item for sublist in game_state["grid"] for item in sublist])
    model_player1.buffer.actions.append(action)
    model_player1.buffer.log_probs.append(log_prob)

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])

    print("Reward: " + str(game_state["score"] - model_player1.prev_score - 1))
    model_player1.buffer.episode_rewards.append(game_state["score"] - model_player1.prev_score - 1)

    if model_player1.counter > UPDATE_INTERVAL:
        model_player1.buffer.rewards.append(model_player1.buffer.episode_rewards)
        model_player1.buffer.episode_rewards = []
        model_player1.update_network()

    # give the action to the gym
    model_player1.prev_score = game_state["score"]
    print(f'In P1, action_type: {action_type}, action_data: {action_data}')
    return action_type, action_data

def player2_callback(game_state):
    """
    Player2's callback function
    :param game_state: current game state
    :return: the action player2's going to act
    """
    # show_game_status(False, game_state['game_end'], game_state['level'], \
    # game_state['score'], game_state['grid'])

    # the model takes action according to current state of the game
    action, log_prob = model_player2.act(game_state)

    # the current state is stored to replay memory for future learning
    model_player2.buffer.states.append([item for sublist in game_state["grid"] for item in sublist])
    model_player2.buffer.actions.append(action)
    model_player2.buffer.log_probs.append(log_prob)

    # convert the action to the format that the gym can understand
    action_type, action_data = select_act(action, game_state["grid"])

    print("Reward: " + str(game_state["score"] - model_player2.prev_score - 1))
    model_player2.buffer.episode_rewards.append(game_state["score"] - model_player2.prev_score - 1)

    if model_player2.counter > UPDATE_INTERVAL:
        model_player2.buffer.rewards.append(model_player2.buffer.episode_rewards)
        model_player2.buffer.episode_rewards = []
        model_player2.update_network()

    # give the action to the gym
    model_player2.prev_score = game_state["score"]
    print(f'In P2, action_type: {action_type}, action_data: {action_data}')
    return action_type, action_data

model_player1 = ppo_agent(50, 1441)
model_player2 = ppo_agent(50, 1441)
# or load model
# model_player1 = torch.load(path_P1)
# model_player2 = torch.load(path_P2)

with open('training_log_2P.txt', 'w') as f:
    for i in range(EPISODE_NUM):
        game_base = GameBase(config)
        # set the callback function
        game_base.set_callback(player1_callback, 1)
        game_base.set_callback(player2_callback, 2)
        # run the game
        game_base.run_game()
        print("=================================================")
        print("EPISODE_NUM: " + str(i))
        print("score of P1: " + str(game_base.game_state.player_states[0].\
              game_board_state.game_score_state.total_score))
        print("score of P2: " + str(game_base.game_state.player_states[1].\
              game_board_state.game_score_state.total_score))
        print("=================================================")
        
        # log into file
        print("=================================================", file = f)
        print("EPISODE_NUM: " + str(i), file = f)
        print("score of P1: " + str(game_base.game_state.player_states[0].\
              game_board_state.game_score_state.total_score), file = f)
        print("score of P2: " + str(game_base.game_state.player_states[1].\
              game_board_state.game_score_state.total_score), file = f)

# save model, be careful of filename (version)
model_save_P1_folder = 'model/'
model_save_P2_folder = 'model/'
model_save_P1_name = 'training_model_2P_1_v0.pt'
model_save_P2_name = 'training_model_2P_2_v0.pt'
path_P1 = model_save_P1_folder + model_save_P1_name
path_P2 = model_save_P2_folder + model_save_P2_name
torch.save(model_player1, path_P1)
torch.save(model_player2, path_P2)