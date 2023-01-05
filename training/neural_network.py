'''
This module contains Neural Network for training.
'''
from torch import nn
import torch.nn.functional as F
class NeuralNetwork(nn.Module):
    '''
    This class contains Neural Network structure.
    '''
    def __init__(self, in_dim, out_dim):
        '''
        constructor of NeuralNetwork
        '''
        super(NeuralNetwork, self).__init__()
        self.fc1 = nn.Linear(in_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, out_dim)

    def forward(self, x_data):
        '''
        forward function of NeuralNetwork
        '''
        x_data = F.relu(self.fc1(x_data))
        x_data = F.relu(self.fc2(x_data))
        out = self.fc3(x_data)
        return out
