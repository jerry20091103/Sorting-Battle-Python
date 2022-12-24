import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import MultivariateNormal
from sorting_battle_gym.game_board_state import GameBoardState              # load_grid
from sorting_battle_gym.game_controller_state import GameControllerState    # select() -> (0, 0) invalid
                                                                            # swap() -> True/False
from sorting_battle_gym.game_base import GameBase
import numpy as np

V_LR=1e-4
P_LR=1e-4
GAMMA=0.99
UPDATE_NUM=4
UPDATE_INTERVAL=8
EPSILON=0.2
EPISODE_NUM = 100
ACTION_SWAP = 1
ACTION_SELECT = 2

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

class NeuralNetwork(nn.Module):
    def __init__(self, in_dim, out_dim):
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(in_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, out_dim)
    
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        out = self.fc3(x)
        return out
        
class Buffer():
    def __init__(self):
        self.states = []
        self.actions = []
        self.log_probs = []
        self.rewards = []
        self.rewards_to_go = []
        self.episode_rewards = []

class ppo_agent():
    def __init__(self, observation_dimension, action_dimension):
        self.counter = 0
        '''step 1: initial policy & value parameters'''
        self.policy_network = NeuralNetwork(observation_dimension, action_dimension).cuda()
        self.value_network = NeuralNetwork(observation_dimension, 1).cuda()
        # self.policy_network = NeuralNetwork(observation_dimension, action_dimension)
        # self.value_network = NeuralNetwork(observation_dimension, 1)

        self.buffer = Buffer()
        self.cov_var = torch.full(size=(action_dimension,), fill_value=0.5)
        self.cov_mat = torch.diag(self.cov_var).cuda()
        # self.cov_mat = torch.diag(self.cov_var)

        self.loss_func = nn.MSELoss()
        self.policy_optimizer = torch.optim.Adam(self.policy_network.parameters(), lr = P_LR)
        self.value_optimizer = torch.optim.Adam(self.value_network.parameters(), lr = V_LR)

        # other vars
        self.prev_state = None

    def act(self, state):
        self.counter += 1
        grid = state["grid"]
        grid = [item for sublist in grid for item in sublist]
        grid = torch.tensor(grid, dtype=torch.float).cuda()
        # grid = torch.tensor(grid, dtype=torch.float)
        action = self.policy_network(grid).detach()
        """
        Multivariate Normal Distribution for continuous action exploration
        """
        dist = MultivariateNormal(action, self.cov_mat)
        action = dist.sample()
        log_prob = dist.log_prob(action)

        return action.data.cpu().numpy(), log_prob
      
    def update_network(self):
        state = torch.tensor(self.buffer.states, dtype=torch.float).cuda()
        action = torch.tensor(np.array(self.buffer.actions), dtype=torch.float).cuda()
        log_prob = torch.tensor(self.buffer.log_probs, dtype=torch.float).cuda()
        # state = torch.tensor(self.buffer.states, dtype=torch.float)
        # action = torch.tensor(self.buffer.actions, dtype=torch.float)
        # log_prob = torch.tensor(self.buffer.log_probs, dtype=torch.float)

        '''step 4: compute rewards_to_go'''
        for episode_rewards in reversed(self.buffer.rewards):
          discounted_reward = 0
          for r in reversed(episode_rewards):
            discounted_reward = r + discounted_reward * GAMMA
            self.buffer.rewards_to_go.insert(0, discounted_reward)
        
        rewards_to_go = torch.tensor(self.buffer.rewards_to_go, dtype=torch.float).cuda()
        # rewards_to_go = torch.tensor(self.buffer.rewards_to_go, dtype=torch.float)

        '''step 5: compute advantage estimate A based on the current value function V'''
        V = self.value_network(state).detach().squeeze()
        A = rewards_to_go - V
        A = (A - A.mean()) / (A.std() + 1e-10) # Normalize advantages

        for i in range(UPDATE_NUM):
          '''step 6: update the policy network'''
          pred_action = self.policy_network(state)
          dist = MultivariateNormal(pred_action, self.cov_mat)
          cur_log_prob = dist.log_prob(action)
          ratios = torch.exp(cur_log_prob-log_prob)
          policy_loss = (-torch.min(ratios * A, torch.clamp(ratios, 1-EPSILON, 1+EPSILON) * A)).mean()

          self.policy_optimizer.zero_grad()
          policy_loss.backward(retain_graph=True)
          self.policy_optimizer.step()

          '''step 7: update the value network'''
          V = self.value_network(state).squeeze()
          value_loss = self.loss_func(V, rewards_to_go)

          self.value_optimizer.zero_grad()
          value_loss.backward()
          self.value_optimizer.step()

        '''clear the buffer'''
        self.buffer = Buffer()
        self.counter = 0

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
  # print(f'action_type: {action_type}, action_data: {action_data}')
  try:
    if action_type == ACTION_SELECT:
      return game_board_state.game_controller_state.select(action_data)[0] > 0
    elif action_type == ACTION_SWAP:
      return game_board_state.game_controller_state.swap(action_data)
  except:
    return False

# def trans_act(action):
def trans_act(action, grid, CHOOSE_LEGAL=True):
  # print(action.argmax())
  # la = np 0, 0, 1, ... only check boundary
  # action[la == 0] = 0
  legal_action_space = []
  for i in range(len(action)):
    action_id = i
    action_type = 1
    action_data = [[8, 0], [9, 0]]
    pos_id = action_id // 32
    move_id = action_id % 32
    move_dir = move_id // 8
    move_type = move_id % 8

    action_data[0][0] = pos_id // 5
    action_data[0][1] = pos_id % 5
    
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
      action_data = [[pos_id // 5, pos_id % 5]] # [[], [], []]
      for i in range(1, move_type+2):
        if move_dir == 0:
          action_data.append([action_data[-1][0], action_data[-1][1] - 1])
        if move_dir == 1:
          action_data.append([action_data[-1][0], action_data[-1][1] + 1])
        if move_dir == 2:
          action_data.append([action_data[-1][0] - 1, action_data[-1][1]])
        if move_dir == 3:
          action_data.append([action_data[-1][0] + 1, action_data[-1][1]])
    
    if is_legal_action(action_type, action_data, grid):
      legal_action_space.append(action[i])
    else:
      legal_action_space.append(-10000)
    
  legal_action_space = np.array(legal_action_space)

  # original code
  if CHOOSE_LEGAL:
    action_id = legal_action_space.argmax()
  else:
    action_id = action.argmax()
  action_type = 1
  action_data = [[8, 0], [9, 0]]
  pos_id = action_id // 32
  move_id = action_id % 32
  move_dir = move_id // 8
  move_type = move_id % 8

  action_data[0][0] = pos_id // 5
  action_data[0][1] = pos_id % 5
  
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
    action_data = [[pos_id // 5, pos_id % 5]] # [[], [], []]
    for i in range(1, move_type+2):
      if move_dir == 0:
        action_data.append([action_data[-1][0], action_data[-1][1] - 1])
      if move_dir == 1:
        action_data.append([action_data[-1][0], action_data[-1][1] + 1])
      if move_dir == 2:
        action_data.append([action_data[-1][0] - 1, action_data[-1][1]])
      if move_dir == 3:
        action_data.append([action_data[-1][0] + 1, action_data[-1][1]])
  
  return action_type, action_data


