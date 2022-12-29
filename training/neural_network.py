'''
This module contains Neural Network for training.
'''
import torch
import torch.nn as nn
import torch.nn.functional as F
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
    
class PolicyNetwork(nn.Module):
    def __init__(self, num_channels, channel_height, channel_width, num_output_channels, action_size):
        super(PolicyNetwork, self).__init__()
        self.channel_height = channel_height
        self.channel_width = channel_width
        self.num_output_channels = num_output_channels
        self.conv = nn.Conv2d(num_channels, num_output_channels, kernel_size=1)
        self.bn = nn.BatchNorm2d(num_output_channels)
        self.fc = nn.Linear(num_output_channels*channel_height*channel_width, action_size)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        x = x.view(-1, self.num_output_channels*self.channel_height*self.channel_width)
        x = self.fc(x)
        return x


class ValueNetwork(nn.Module):
    def __init__(self, num_channels, channel_height, channel_width, num_value_hidden_channels):
        super(ValueNetwork, self).__init__()
        self.channel_height = channel_height
        self.channel_width = channel_width
        self.conv = nn.Conv2d(num_channels, 1, kernel_size=1)
        self.bn = nn.BatchNorm2d(1)
        self.fc1 = nn.Linear(channel_height*channel_width, num_value_hidden_channels)
        self.fc2 = nn.Linear(num_value_hidden_channels, 1)
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        x = x.view(-1, self.channel_height*self.channel_width)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = self.tanh(x)
        return x