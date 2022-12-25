import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import MultivariateNormal
from neural_network import NeuralNetwork
from buffer import Buffer

# model settings
V_LR=1e-4
P_LR=1e-4
GAMMA=0.99
UPDATE_NUM=4
EPSILON=0.2

class ppo_agent():
    def __init__(self, observation_dimension, action_dimension):
        """
        Constructor of PPO Agent
        """
        self.counter = 0
        # step 1: initial policy & value parameters
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
        self.prev_score = 0

    def reset(self):
        """
        Reset previous score when starting a new game
        """
        self.prev_score = 0

    def act(self, state):
        self.counter += 1
        grid = state["grid"]
        grid = [item for sublist in grid for item in sublist]
        grid = torch.tensor(grid, dtype=torch.float).cuda()
        # grid = torch.tensor(grid, dtype=torch.float)
        action = self.policy_network(grid).detach()
      
        # Multivariate Normal Distribution for continuous action exploration
        dist = MultivariateNormal(action, self.cov_mat)
        action = dist.sample()
        log_prob = dist.log_prob(action)
        
        return action.data.cpu().numpy(), log_prob
      
    def update_network(self):
        state = torch.tensor(self.buffer.states, dtype=torch.float).cuda()
        action = torch.tensor(np.array(self.buffer.actions), dtype=torch.float).cuda()
        log_prob = torch.tensor(self.buffer.log_probs, dtype=torch.float).cuda()
        # state = torch.tensor(self.buffer.states, dtype=torch.float)
        # action = torch.tensor(np.array(self.buffer.actions), dtype=torch.float)
        # log_prob = torch.tensor(self.buffer.log_probs, dtype=torch.float

        # step 4: compute rewards_to_go
        for episode_rewards in reversed(self.buffer.rewards):
            discounted_reward = 0
            for r in reversed(episode_rewards):
                discounted_reward = r + discounted_reward * GAMMA
                self.buffer.rewards_to_go.insert(0, discounted_reward)
        
        rewards_to_go = torch.tensor(self.buffer.rewards_to_go, dtype=torch.float).cuda()
        # rewards_to_go = torch.tensor(self.buffer.rewards_to_go, dtype=torch.float

        # step 5: compute advantage estimate A based on the current value function V
        V = self.value_network(state).detach().squeeze()
        A = rewards_to_go - V
        A = (A - A.mean()) / (A.std() + 1e-10) # Normalize advantage
        for _ in range(UPDATE_NUM):
            # step 6: update the policy network'''
            pred_action = self.policy_network(state)
            dist = MultivariateNormal(pred_action, self.cov_mat)
            cur_log_prob = dist.log_prob(action)
            ratios = torch.exp(cur_log_prob-log_prob)
            policy_loss = (-torch.min(ratios * A, torch.clamp(ratios, 1-EPSILON, 1+EPSILON) * A)).mean()
            self.policy_optimizer.zero_grad()
            policy_loss.backward(retain_graph=True)
            self.policy_optimizer.step()

            # step 7: update the value network
            V = self.value_network(state).squeeze()
            value_loss = self.loss_func(V, rewards_to_go)
            self.value_optimizer.zero_grad()
            value_loss.backward()
            self.value_optimizer.step()

        # clear the buffer
        self.buffer = Buffer()
        self.counter = 0